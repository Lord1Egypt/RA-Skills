from __future__ import annotations

import importlib.util
import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_brief.py"
SPEC = importlib.util.spec_from_file_location("render_brief", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def sample_payload() -> dict:
    return json.loads((ROOT / "tests" / "fixtures" / "valid.json").read_text(encoding="utf-8"))


class RenderBriefTests(unittest.TestCase):
    def test_valid_payload_renders_markdown_and_html(self) -> None:
        payload = MODULE.validate(sample_payload())
        markdown = MODULE.render_markdown(payload)
        rendered_html = MODULE.render_html(payload)
        self.assertIn("Alex的校园晨报", markdown)
        self.assertIn("示例新闻 7", markdown)
        self.assertIn("<!doctype html>", rendered_html)
        self.assertIn("https://example.com/news/7", rendered_html)

    def test_invalid_url_is_rejected(self) -> None:
        payload = sample_payload()
        payload["general_news"][0]["url"] = "javascript:alert(1)"
        with self.assertRaises(MODULE.BriefValidationError):
            MODULE.validate(payload)


if __name__ == "__main__":
    unittest.main()
