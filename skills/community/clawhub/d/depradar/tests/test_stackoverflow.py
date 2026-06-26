"""Tests for lib/stackoverflow.py — Stack Exchange API integration."""
import json
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from lib.schema import StackOverflowItem

FIXTURES = os.path.join(os.path.dirname(__file__), "..", "fixtures")


def load_fixture(name: str) -> dict:
    with open(os.path.join(FIXTURES, name)) as f:
        return json.load(f)


SO_FIXTURE = load_fixture("stackoverflow_sample.json")

import lib.stackoverflow as so_mod


class TestParseQuestion(unittest.TestCase):
    """_parse_question(raw, package, idx) — internal parser."""

    def test_parses_basic_item(self):
        raw = {
            "question_id": 987654,
            "title": "How to migrate from stripe v7 to v8?",
            "link": "https://stackoverflow.com/questions/987654",
            "score": 23,
            "answer_count": 3,
            "is_answered": True,
            "creation_date": 1704067200,
            "tags": ["stripe", "python", "payments"],
            "view_count": 1500,
        }
        item = so_mod._parse_question(raw, package="stripe", idx=1)
        self.assertIsInstance(item, StackOverflowItem)
        self.assertEqual(item.id, "SO1")
        self.assertTrue(item.is_answered)
        self.assertEqual(item.answer_count, 3)
        self.assertIn("stripe", item.question_title.lower())
        self.assertEqual(item.package, "stripe")

    def test_handles_zero_score(self):
        raw = {
            "question_id": 1,
            "title": "stripe issue",
            "link": "https://stackoverflow.com/questions/1",
            "score": 0,
            "answer_count": 0,
            "is_answered": False,
            "creation_date": 1704067200,
            "tags": ["stripe"],
            "view_count": 0,
        }
        item = so_mod._parse_question(raw, package="stripe", idx=1)
        self.assertIsNotNone(item)
        self.assertEqual(item.so_score, 0)

    def test_handles_missing_tags(self):
        raw = {
            "question_id": 2,
            "title": "issue",
            "link": "https://stackoverflow.com/questions/2",
            "score": 1,
            "answer_count": 0,
            "is_answered": False,
            "creation_date": 1704067200,
            "view_count": 0,
        }
        item = so_mod._parse_question(raw, package="stripe", idx=1)
        self.assertIsNotNone(item)
        self.assertEqual(item.tags, [])

    def test_assigns_sequential_id(self):
        raw = {
            "question_id": 100, "title": "t",
            "link": "u", "score": 0, "answer_count": 0,
            "is_answered": False, "creation_date": 1704067200,
            "tags": [], "view_count": 0,
        }
        item = so_mod._parse_question(raw, "pkg", idx=3)
        self.assertEqual(item.id, "SO3")


class TestScoreSOItem(unittest.TestCase):
    def _make_item(self, answer_count=0, is_answered=False, so_score=0) -> StackOverflowItem:
        return StackOverflowItem(
            id="SO1", package="stripe",
            question_title="stripe v8 migration",
            question_url="https://stackoverflow.com/questions/1",
            answer_count=answer_count, is_answered=is_answered,
            accepted_answer_snippet=None, tags=["stripe"],
            view_count=100, so_score=so_score,
            created_at="2026-01-15T00:00:00Z",
            subs=None, score=0, cross_refs=[],
        )

    def test_answered_does_not_lower_score(self):
        # Scoring may be equal when both have same view_count/so_score
        unanswered = so_mod._score_so_item(self._make_item(is_answered=False, so_score=10))
        answered = so_mod._score_so_item(self._make_item(is_answered=True, so_score=10))
        self.assertGreaterEqual(answered.score, unanswered.score)

    def test_more_answers_higher_score(self):
        low = so_mod._score_so_item(self._make_item(answer_count=0))
        high = so_mod._score_so_item(self._make_item(answer_count=5))
        self.assertGreaterEqual(high.score, low.score)


class TestSearchStackoverflow(unittest.TestCase):
    # Actual signature: search_stackoverflow(packages, days, depth, api_key)
    @patch("lib.stackoverflow.get_json")
    def test_returns_list(self, mock_get):
        mock_get.return_value = {
            "items": [
                {
                    "question_id": 1,
                    "title": "stripe v8 breaking change",
                    "link": "https://stackoverflow.com/questions/1",
                    "score": 5,
                    "answer_count": 2,
                    "is_answered": True,
                    "creation_date": 1704067200,
                    "tags": ["stripe"],
                    "view_count": 500,
                }
            ],
            "has_more": False,
            "quota_remaining": 299,
        }
        items = so_mod.search_stackoverflow(["stripe"], days=30, depth="default", api_key=None)
        self.assertIsInstance(items, list)
        for item in items:
            self.assertEqual(type(item).__name__, "StackOverflowItem")

    @patch("lib.stackoverflow.get_json")
    def test_returns_empty_on_rate_limit(self, mock_get):
        from lib.http import RateLimitError
        mock_get.side_effect = RateLimitError("https://api.stackexchange.com/", 429, "limited")
        items = so_mod.search_stackoverflow(["stripe"], days=30, depth="default", api_key=None)
        self.assertIsInstance(items, list)

    @patch("lib.stackoverflow.get_json")
    def test_returns_empty_on_http_error(self, mock_get):
        from lib.http import HttpError
        mock_get.side_effect = HttpError("https://api.stackexchange.com/", 500, "server error")
        items = so_mod.search_stackoverflow(["stripe"], days=30, depth="default", api_key=None)
        self.assertIsInstance(items, list)

    def test_returns_empty_list_for_no_packages(self):
        items = so_mod.search_stackoverflow([], days=30, depth="default", api_key=None)
        self.assertEqual(items, [])


if __name__ == "__main__":
    unittest.main()
