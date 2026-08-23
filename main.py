__version__ = "1.0.0"
import os
import json

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.metrics import dp


class NovaNotes(App):

    def build(self):

        self.title = "Nova Notes"

        # Black app background
        Window.clearcolor = (0, 0, 0, 1)

        # -------------------------------------------------
        # FILE WHERE NOTES ARE SAVED
        # -------------------------------------------------

        self.notes_file = os.path.join(
            self.user_data_dir,
            "nova_notes.json"
        )

        # Load existing notes
        self.notes = self.load_saved_notes()

        # -------------------------------------------------
        # MAIN SCREEN
        # -------------------------------------------------

        main = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10)
        )

        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        title = Label(
            text="Nova Notes",
            font_size=dp(32),
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(65)
        )

        main.add_widget(title)

        # -------------------------------------------------
        # NOTE INPUT
        # -------------------------------------------------

        self.note_input = TextInput(
            hint_text="Write your note here...",
            multiline=True,
            font_size=dp(18),
            size_hint_y=None,
            height=dp(160),
            padding=dp(12),
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0, 0, 0, 1)
        )

        main.add_widget(self.note_input)

        # -------------------------------------------------
        # COLOR SELECTOR
        # -------------------------------------------------

        color_row = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10)
        )

        color_text = Label(
            text="Color:",
            font_size=dp(18),
            color=(1, 1, 1, 1),
            size_hint_x=None,
            width=dp(70)
        )

        self.color_spinner = Spinner(
            text="White",
            values=[
                "Red",
                "Green",
                "Black",
                "Blue",
                "White",
                "Gold",
                "Silver",
                "Gray"
            ],
            font_size=dp(17)
        )

        color_row.add_widget(color_text)
        color_row.add_widget(self.color_spinner)

        main.add_widget(color_row)

        # -------------------------------------------------
        # SAVE BUTTON
        # -------------------------------------------------

        save_button = Button(
            text="Save Note",
            font_size=dp(20),
            size_hint_y=None,
            height=dp(60),
            background_normal="",
            background_color=(0.15, 0.15, 0.45, 1)
        )

        save_button.bind(
            on_press=self.save_note
        )

        main.add_widget(save_button)

        # -------------------------------------------------
        # MY NOTES
        # -------------------------------------------------

        notes_title = Label(
            text="My Notes",
            font_size=dp(28),
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(65)
        )

        main.add_widget(notes_title)

        # -------------------------------------------------
        # SCROLL AREA
        # -------------------------------------------------

        scroll = ScrollView(
            do_scroll_x=False
        )

        self.notes_box = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            size_hint_y=None
        )

        self.notes_box.bind(
            minimum_height=self.notes_box.setter(
                "height"
            )
        )

        scroll.add_widget(
            self.notes_box
        )

        main.add_widget(scroll)

        # -------------------------------------------------
        # SHOW NOTES
        # -------------------------------------------------

        self.refresh_notes()

        return main

    # =====================================================
    # LOAD NOTES
    # =====================================================

    def load_saved_notes(self):

        if not os.path.exists(self.notes_file):
            return []

        try:

            with open(
                self.notes_file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                if isinstance(data, list):
                    return data

                return []

        except Exception:

            return []

    # =====================================================
    # SAVE NOTES TO FILE
    # =====================================================

    def save_notes_to_file(self):

        try:

            with open(
                self.notes_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.notes,
                    file,
                    ensure_ascii=False,
                    indent=2
                )

        except Exception as error:

            print(
                "Could not save notes:",
                error
            )

    # =====================================================
    # SAVE A NEW NOTE
    # =====================================================

    def save_note(self, instance):

        text = self.note_input.text.strip()

        if text == "":
            return

        color = self.color_spinner.text

        new_note = {
            "text": text,
            "color": color
        }

        self.notes.append(new_note)

        self.save_notes_to_file()

        self.note_input.text = ""

        self.color_spinner.text = "White"

        self.refresh_notes()

    # =====================================================
    # GET COLOR
    # =====================================================

    def get_text_color(self, color):

        if color == "Red":
            return (1, 0, 0, 1)

        if color == "Green":
            return (0, 1, 0, 1)

        if color == "Black":
            return (0, 0, 0, 1)

        if color == "Blue":
            return (0, 0.4, 1, 1)

        if color == "White":
            return (1, 1, 1, 1)

        if color == "Gold":
            return (1, 0.84, 0, 1)

        if color == "Silver":
            return (0.75, 0.75, 0.75, 1)

        if color == "Gray":
            return (0.5, 0.5, 0.5, 1)

        return (1, 1, 1, 1)

    # =====================================================
    # DISPLAY NOTES
    # =====================================================

    def refresh_notes(self):

        self.notes_box.clear_widgets()

        if len(self.notes) == 0:

            empty = Label(
                text="No notes yet.",
                font_size=dp(18),
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height=dp(60)
            )

            self.notes_box.add_widget(empty)

            return

        # Show newest note first
        for index in range(
            len(self.notes) - 1,
            -1,
            -1
        ):

            note = self.notes[index]

            text = note.get(
                "text",
                ""
            )

            color = note.get(
                "color",
                "White"
            )

            self.create_note_row(
                index,
                text,
                color
            )

    # =====================================================
    # CREATE ONE SAVED NOTE
    # =====================================================

    def create_note_row(
        self,
        index,
        text,
        color
    ):

        row = BoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(80)
        )

        # -------------------------------------------------
        # NOTE TEXT
        # -------------------------------------------------

        note_label = Label(
            text=text,
            font_size=dp(20),
            color=self.get_text_color(color),
            halign="left",
            valign="middle"
        )

        note_label.bind(
            size=lambda widget, value:
            setattr(
                widget,
                "text_size",
                (widget.width, None)
            )
        )

        # -------------------------------------------------
        # DELETE BUTTON
        # -------------------------------------------------

        delete_button = Button(
            text="Delete",
            font_size=dp(17),
            size_hint_x=None,
            width=dp(105),
            background_normal="",
            background_color=(0.45, 0.05, 0.05, 1)
        )

        delete_button.bind(
            on_press=lambda button:
            self.delete_note(index)
        )

        row.add_widget(
            note_label
        )

        row.add_widget(
            delete_button
        )

        self.notes_box.add_widget(
            row
        )

    # =====================================================
    # DELETE NOTE
    # =====================================================

    def delete_note(self, index):

        if 0 <= index < len(self.notes):

            self.notes.pop(index)

            self.save_notes_to_file()

            self.refresh_notes()


# =========================================================
# START APP
# =========================================================

if __name__ == "__main__":

    NovaNotes().run()