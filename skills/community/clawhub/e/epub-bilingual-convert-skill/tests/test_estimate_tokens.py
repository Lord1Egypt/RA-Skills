import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("estimate_tokens", ROOT / "scripts" / "estimate_tokens.py")
estimate_tokens = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(estimate_tokens)


def article(num, title, paragraphs, plain_text=None, section="Chapter", complete=False):
    return {
        "num": num,
        "title": title,
        "section": section,
        "href": f"chapter-{num}.xhtml",
        "paragraphs": paragraphs,
        "plain_text": plain_text if plain_text is not None else "\n\n".join(paragraphs),
        "image_filename": None,
        "title_dest_language": "标题" if complete else None,
        "section_dest_language": "章节" if complete else None,
        "translated_paragraphs": ["译文"] * len(paragraphs) if complete else None,
        "summary_dest_language": "摘要" if complete else None,
    }


class EstimateTokensTest(unittest.TestCase):
    def payload(self):
        return {
            "epub_title": "Fixture Book",
            "input_epub": "/tmp/fixture.epub",
            "output_dir": "/tmp/out",
            "target_language": "Simplified Chinese",
            "total_articles": 6,
            "articles": [
                article(1, "Tiny", ["a" * 100], section="Intro"),
                article(2, "Huge", ["b" * 9000], plain_text="s" * 8000),
                article(3, "Medium", ["c" * 4000]),
                article(4, "Small", ["d" * 500]),
                article(5, "Large", ["e" * 7000]),
                article(6, "Done", ["f" * 1200], complete=True),
            ],
        }

    def test_estimate_includes_paragraphs_metadata_and_summary_sources(self):
        result = estimate_tokens.estimate_payload(self.payload(), max_source_chars=8000, retry_buffer=0.15, top=5)

        paragraph_chars = sum(
            len(paragraph)
            for item in self.payload()["articles"]
            for paragraph in item["paragraphs"]
        )
        metadata_chars = sum(
            len(item["title"]) + len(item["section"])
            for item in self.payload()["articles"]
        )
        summary_chars = sum(len(item["plain_text"]) for item in self.payload()["articles"])

        self.assertEqual(result["source_chars"]["paragraphs"], paragraph_chars)
        self.assertEqual(result["source_chars"]["metadata"], metadata_chars)
        self.assertEqual(result["source_chars"]["summary"], summary_chars)
        self.assertEqual(result["scope"], "full extraction")

    def test_batches_use_configurable_source_character_limit(self):
        result = estimate_tokens.estimate_payload(self.payload(), max_source_chars=5000, retry_buffer=0.15, top=5)

        self.assertEqual(result["batching"]["max_source_chars"], 5000)
        self.assertEqual(result["batching"]["estimated_paragraph_batches"], 5)

    def test_retry_buffer_affects_total_token_range(self):
        lower = estimate_tokens.estimate_payload(self.payload(), max_source_chars=8000, retry_buffer=0.10, top=5)
        higher = estimate_tokens.estimate_payload(self.payload(), max_source_chars=8000, retry_buffer=0.25, top=5)

        self.assertGreater(higher["tokens"]["total"]["max"], lower["tokens"]["total"]["max"])
        self.assertEqual(higher["tokens"]["retry_buffer_ratio"], 0.25)

    def test_largest_articles_are_limited_to_top_five(self):
        result = estimate_tokens.estimate_payload(self.payload(), max_source_chars=8000, retry_buffer=0.15, top=5)

        largest = result["largest_articles"]
        self.assertEqual(len(largest), 5)
        self.assertEqual([item["title"] for item in largest[:3]], ["Huge", "Large", "Medium"])

    def test_cli_prints_human_readable_report_by_default(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "extraction.json"
            path.write_text(json.dumps(self.payload()), encoding="utf-8")

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = estimate_tokens.main([str(path)])

        report = output.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("EPUB: Fixture Book", report)
        self.assertIn("Estimator: lightweight character heuristic", report)
        self.assertIn("Estimated translation tokens:", report)
        self.assertIn("Largest articles by source chars:", report)
        self.assertIn("No cost estimate included.", report)


if __name__ == "__main__":
    unittest.main()
