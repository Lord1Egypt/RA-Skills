#!/usr/bin/env python3
"""Tests for summarize-merged.py."""

import contextlib
import importlib.util
import io
import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

spec = importlib.util.spec_from_file_location(
    "summarize_merged", SCRIPTS_DIR / "summarize-merged.py"
)
summarize_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(summarize_mod)


class TestPodcastSummary(unittest.TestCase):
    def test_ok_status_without_transcript_is_not_ready(self):
        self.assertEqual(
            summarize_mod.display_transcript_status(
                {
                    "transcript_status": "ok",
                    "transcript": "",
                }
            ),
            "ok",
        )

    def test_ready_transcript_is_displayed_for_ok_transcript(self):
        data = {
            "output_stats": {"total_articles": 1},
            "topics": {
                "llm": {
                    "articles": [
                        {
                            "title": "Waymo Autonomy",
                            "source_name": "Training Data",
                            "source_type": "podcast",
                            "show_name": "Training Data",
                            "quality_score": 10,
                            "transcript_status": "ok",
                            "transcript": "Speaker | 00:00 - 00:05 Autonomy is a product problem.",
                            "duration_seconds": 3600,
                        }
                    ]
                }
            },
        }

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            summarize_mod.summarize(data)

        text = output.getvalue()
        self.assertIn("[podcast] Waymo Autonomy", text)
        self.assertIn("Podcast: Training Data · transcript=ready", text)
        self.assertIn("Duration: 3600s", text)


if __name__ == "__main__":
    unittest.main()
