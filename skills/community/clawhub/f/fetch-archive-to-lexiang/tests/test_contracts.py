from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SkillContractTests(unittest.TestCase):
    def test_frontmatter_dependencies(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn('version: "4.1.0"', skill)
        self.assertIn("name: trans-doc-to-md", skill)
        self.assertIn('version: ">=3.0.0,<4.0.0"', skill)
        self.assertIn("name: upload-markdown-to-lexiang", skill)
        self.assertIn('version: ">=1.1.0,<2.0.0"', skill)

    def test_no_private_translation_script_or_openai_translation(self):
        self.assertFalse((SCRIPTS / "translate_gemini.py").exists())
        youtube = (SCRIPTS / "yt_download_transcribe.py").read_text(encoding="utf-8")
        self.assertNotIn("def translate_paragraphs", youtube)
        self.assertNotIn("from openai import", youtube)
        self.assertNotIn("OPENAI_API_KEY", youtube)
        self.assertNotIn("🇨🇳", youtube)

    def test_podcast_has_no_markdown_upload_stage(self):
        podcast = (SCRIPTS / "podcast_to_lexiang.py").read_text(encoding="utf-8")
        self.assertNotIn("def _find_markdown_uploader", podcast)
        self.assertNotIn("def upload_to_lexiang", podcast)
        self.assertNotIn("--space-id", podcast)
        self.assertNotIn("--parent-entry-id", podcast)
        self.assertNotIn("--no-upload", podcast)

    def test_youtube_markdown_is_source_only(self):
        module = load_module("youtube_contract", SCRIPTS / "yt_download_transcribe.py")
        content = module.generate_markdown(
            {
                "title": "Original Title",
                "channel": "Channel",
                "webpage_url": "https://example.com/video",
                "description": "Show notes",
            },
            [{"start": 0, "text": "Original transcript."}],
            "en",
        )
        self.assertIn("## 视频介绍", content)
        self.assertIn("## 逐字稿", content)
        self.assertIn("Original transcript.", content)
        self.assertNotIn("\n---\n", content)

    def test_podcast_markdown_is_source_only(self):
        module = load_module("podcast_contract", SCRIPTS / "podcast_to_lexiang.py")
        content = module.generate_markdown(
            [{"start": 0, "text": "原始逐字稿。"}],
            "原文标题",
            {"url": "https://example.com/podcast", "shownotes": "节目介绍"},
            language="zh",
        )
        self.assertLess(content.index("## 节目介绍"), content.index("## 逐字稿"))

    def test_article_standard_paths_and_metadata(self):
        article = (SCRIPTS / "fetch_article.py").read_text(encoding="utf-8")
        self.assertIn('output_path / "source.md"', article)
        self.assertIn('output_path / "meta.json"', article)
        for field in ("source_url", "source_title", "source_type", "language"):
            self.assertIn(f'"{field}"', article)

    def test_article_defaults_to_cdp_and_recognizes_custom_substack_domain(self):
        module = load_module("article_contract", SCRIPTS / "fetch_article.py")
        self.assertTrue(module._is_substack_site("https://www.a16z.news/p/example"))
        self.assertTrue(module._is_substack_site("https://example.substack.com/p/post"))
        self.assertIn("use_cdp: bool = True", (SCRIPTS / "fetch_article.py").read_text())

    def test_substack_noise_is_filtered_before_markdown_output(self):
        article = (SCRIPTS / "fetch_article.py").read_text(encoding="utf-8")
        for marker in (
            "discover more from ",
            "subscribe for more from ",
            "this newsletter is provided for informational purposes only",
        ):
            self.assertIn(marker, article)

    def test_substack_postprocessor_cuts_recommendations_and_byline(self):
        module = load_module("article_noise_contract", SCRIPTS / "fetch_article.py")
        markdown = (
            "[George](https://substack.com/@george)Jul 15, 2026\n\n"
            "Article body.\n\n"
            "![](images/subscribe.png)\n\n"
            "[Institutional AI vs Individual AI](https://example.com/related)\n"
        )
        cleaned = module._strip_substack_archive_noise(markdown, "George")
        self.assertEqual(cleaned, "Article body.")

    def test_scenarios_are_valid_json(self):
        with (ROOT / "tests" / "test-cases.json").open(encoding="utf-8") as handle:
            cases = json.load(handle)
        self.assertGreaterEqual(len(cases), 3)


if __name__ == "__main__":
    unittest.main()
