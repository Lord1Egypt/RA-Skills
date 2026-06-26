from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "assets" / "theme" / "control-ui-overrides.css"
JS = ROOT / "assets" / "theme" / "control-ui-overlay.js"


class OpenClaw20260609ComposerAdapterTest(unittest.TestCase):
    def test_css_targets_nested_chat_main_composer(self):
        css = CSS.read_text(encoding="utf-8")

        self.assertIn(".shell--chat .chat-main > .agent-chat__input", css)
        self.assertIn(".shell--chat .chat-main > .chat-thread", css)
        self.assertIn("2026.6.9 chat-workbench composer adapter", css)

    def test_css_orders_usage_settings_send_controls(self):
        css = CSS.read_text(encoding="utf-8")

        self.assertIn("2026.6.9 composer right controls order adapter", css)
        self.assertIn(
            "grid-template-columns: auto auto minmax(0, 1fr) auto auto auto",
            css,
        )
        self.assertIn(".shell--chat .agent-chat__toolbar .chat-controls__quota", css)
        self.assertIn("grid-area: auto !important", css)
        self.assertIn("grid-row: 1 / auto !important", css)
        self.assertIn("grid-column: 4 !important", css)
        self.assertIn(".shell--chat .chat-settings-popover-wrapper", css)
        self.assertIn("grid-column: 5 !important", css)
        self.assertIn(".shell--chat .agent-chat__toolbar-right", css)
        self.assertIn("grid-column: 6 !important", css)

    def test_overlay_metrics_finds_nested_composer_first(self):
        js = JS.read_text(encoding="utf-8")

        self.assertIn(".chat-main > .agent-chat__input", js)
        self.assertIn("queryChatComposer", js)
        self.assertIn("isChatMainComposer", js)
        self.assertIn("chatMainComposerBottom", js)


if __name__ == "__main__":
    unittest.main()
