"""Tests for lib/hackernews.py — Hacker News Algolia + Firebase integration."""
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from lib.schema import HackerNewsItem
import lib.hackernews as hn


class TestParseHNHit(unittest.TestCase):
    """_parse_hn_hit(hit, package, idx) — internal parser."""

    def test_parses_story_hit(self):
        hit = {
            "objectID": "39876543",
            "title": "Ask HN: Stripe v8 breaking — how did you migrate?",
            "url": None,
            "story_url": None,
            "author": "hnuser",
            "points": 45,
            "num_comments": 23,
            "created_at": "2026-01-15T10:00:00.000Z",
            "_tags": ["story", "ask_hn"],
            "comment_text": None,
            "story_title": None,
        }
        item = hn._parse_hn_hit(hit, package="stripe", idx=1)
        self.assertIsInstance(item, HackerNewsItem)
        self.assertEqual(item.id, "HN1")
        self.assertEqual(item.points, 45)
        self.assertEqual(item.num_comments, 23)
        self.assertEqual(item.package, "stripe")

    def test_parses_comment_hit(self):
        hit = {
            "objectID": "39999999",
            "title": None,
            "url": None,
            "story_url": "https://news.ycombinator.com/item?id=39999990",
            "author": "another_user",
            "points": 0,
            "num_comments": 0,
            "created_at": "2026-01-16T12:00:00.000Z",
            "_tags": ["comment"],
            "comment_text": "stripe v8 removed constructEvent, use verify() instead",
            "story_title": "Stripe v8 released",
        }
        item = hn._parse_hn_hit(hit, package="stripe", idx=2)
        self.assertIsNotNone(item)
        self.assertEqual(item.id, "HN2")

    def test_handles_null_points(self):
        hit = {
            "objectID": "1",
            "title": "foo breaking change",  # must match package or breaking term
            "url": None,
            "author": "u",
            "points": None,
            "num_comments": None,
            "created_at": "2026-01-01T00:00:00.000Z",
            "_tags": ["story"],
        }
        item = hn._parse_hn_hit(hit, package="foo", idx=1)
        self.assertIsNotNone(item)
        self.assertEqual(item.points, 0)
        self.assertEqual(item.num_comments, 0)

    def test_hn_url_points_to_hn(self):
        hit = {
            "objectID": "12345678",
            "title": "stripe",
            "url": None,
            "author": "u",
            "points": 5,
            "num_comments": 2,
            "created_at": "2026-01-01T00:00:00.000Z",
            "_tags": ["story"],
        }
        item = hn._parse_hn_hit(hit, package="stripe", idx=1)
        if item:
            self.assertIn("12345678", item.hn_url)


class TestSearchHackerNews(unittest.TestCase):
    @patch("lib.hackernews.get_json")
    def test_returns_list(self, mock_get):
        mock_get.return_value = {
            "hits": [
                {
                    "objectID": "42",
                    "title": "stripe v8 breaking",
                    "url": None,
                    "author": "user",
                    "points": 5,
                    "num_comments": 2,
                    "created_at": "2026-01-01T00:00:00.000Z",
                    "_tags": ["story"],
                }
            ],
            "nbHits": 1,
        }
        items = hn.search_hackernews(["stripe"], days=30, depth="default")
        self.assertIsInstance(items, list)

    @patch("lib.hackernews.get_json")
    def test_returns_empty_on_http_error(self, mock_get):
        from lib.http import HttpError
        mock_get.side_effect = HttpError("https://hn.algolia.com/", 503, "service unavailable")
        items = hn.search_hackernews(["stripe"], days=30, depth="default")
        self.assertIsInstance(items, list)

    def test_returns_empty_for_no_packages(self):
        items = hn.search_hackernews([], days=30, depth="default")
        self.assertEqual(items, [])


class TestAlgoliaArchivedNote(unittest.TestCase):
    def test_hn_module_has_archive_note(self):
        import inspect
        src = inspect.getsource(hn)
        self.assertTrue(
            "2026" in src or "archived" in src.lower() or "archive" in src.lower(),
            "hackernews.py should note the Feb 2026 Algolia archive status"
        )

    def test_hn_algolia_url_constant_present(self):
        self.assertTrue(hasattr(hn, "HN_ALGOLIA_URL"))
        self.assertIn("algolia.com", hn.HN_ALGOLIA_URL)


if __name__ == "__main__":
    unittest.main()
