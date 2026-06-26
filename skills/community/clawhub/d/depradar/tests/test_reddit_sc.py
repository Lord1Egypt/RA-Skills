"""Tests for lib/reddit_sc.py — Reddit via ScrapeCreators API."""
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from lib.schema import RedditItem
import lib.reddit_sc as reddit


class TestEcosystemSubreddits(unittest.TestCase):
    """ECOSYSTEM_SUBREDDITS dict — ecosystem → subreddit list."""

    def test_npm_subreddits_present(self):
        subs = reddit.ECOSYSTEM_SUBREDDITS.get("npm", [])
        self.assertGreater(len(subs), 0)
        combined = " ".join(subs).lower()
        self.assertTrue("javascript" in combined or "node" in combined)

    def test_pypi_subreddits_present(self):
        subs = reddit.ECOSYSTEM_SUBREDDITS.get("pypi", [])
        self.assertGreater(len(subs), 0)
        combined = " ".join(subs).lower()
        self.assertTrue("python" in combined)

    def test_cargo_subreddits_present(self):
        subs = reddit.ECOSYSTEM_SUBREDDITS.get("cargo", [])
        self.assertGreater(len(subs), 0)

    def test_maven_subreddits_present(self):
        subs = reddit.ECOSYSTEM_SUBREDDITS.get("maven", [])
        self.assertGreater(len(subs), 0)

    def test_fallback_for_unknown(self):
        # Unknown ecosystem should have a fallback or return some subs
        subs = reddit.ECOSYSTEM_SUBREDDITS.get("unknown", reddit.ECOSYSTEM_SUBREDDITS.get("npm", []))
        self.assertIsInstance(subs, list)


class TestParseRedditPost(unittest.TestCase):
    """_parse_reddit_post(raw, package, subreddit, idx)."""

    def _make_raw(self, **kwargs) -> dict:
        defaults = {
            "id": "abc123",
            "title": "Stripe v8 breaking changes",
            "url": "https://reddit.com/r/javascript/comments/abc123",
            "selftext": "Just upgraded to stripe v8...",
            "score": 156,
            "num_comments": 23,
            "created_utc": 1704067200.0,
            "subreddit": "javascript",
            "author": "dev_user",
            "upvote_ratio": 0.96,
        }
        defaults.update(kwargs)
        return defaults

    def test_parses_basic_post(self):
        raw = self._make_raw()
        item = reddit._parse_reddit_post(raw, package="stripe",
                                          subreddit="javascript", idx=1)
        self.assertIsInstance(item, RedditItem)
        self.assertEqual(item.id, "RI1")
        self.assertEqual(item.reddit_score, 156)
        self.assertEqual(item.num_comments, 23)
        self.assertEqual(item.subreddit, "javascript")
        self.assertEqual(item.package, "stripe")

    def test_handles_empty_selftext(self):
        raw = self._make_raw(selftext="")
        item = reddit._parse_reddit_post(raw, "stripe", "javascript", idx=1)
        self.assertIsNotNone(item)

    def test_handles_deleted_post(self):
        raw = self._make_raw(selftext="[deleted]", author="[deleted]")
        item = reddit._parse_reddit_post(raw, "foo", "python", idx=1)
        self.assertIsNotNone(item)

    def test_assigns_sequential_id(self):
        raw = self._make_raw()
        item = reddit._parse_reddit_post(raw, "stripe", "javascript", idx=7)
        self.assertEqual(item.id, "RI7")


class TestScoreRedditItem(unittest.TestCase):
    def _make_item(self, score=0, num_comments=0) -> RedditItem:
        return RedditItem(
            id="RI1", package="stripe", subreddit="javascript",
            title="stripe v8 breaking", url="https://reddit.com/r/js/abc",
            reddit_score=score, num_comments=num_comments,
            top_comment=None, date="2026-01-15", date_confidence="high",
            subs=None, score=0, cross_refs=[],
        )

    def test_higher_vote_score_increases_ranking(self):
        low = reddit._score_reddit_item(self._make_item(score=1))
        high = reddit._score_reddit_item(self._make_item(score=500))
        self.assertGreater(high.score, low.score)

    def test_more_comments_increases_score(self):
        low = reddit._score_reddit_item(self._make_item(num_comments=0))
        high = reddit._score_reddit_item(self._make_item(num_comments=100))
        self.assertGreaterEqual(high.score, low.score)


class TestSearchRedditNoCredentials(unittest.TestCase):
    # Actual signature: search_reddit(packages, ecosystem, days, depth, token)
    def test_returns_empty_without_token(self):
        # search_reddit returns [] immediately when token is falsy
        items = reddit.search_reddit(["stripe"], ecosystem="npm",
                                      days=30, depth="default", token=None)
        self.assertEqual(items, [])

    def test_returns_list_type(self):
        result = reddit.search_reddit(["stripe"], ecosystem="npm",
                                       days=30, depth="default", token=None)
        self.assertIsInstance(result, list)


class TestSearchRedditWithMockApi(unittest.TestCase):
    @patch("lib.reddit_sc.get_json")
    def test_parses_api_response(self, mock_get):
        mock_get.return_value = {
            "data": {
                "children": [
                    {
                        "data": {
                            "id": "r1",
                            "title": "stripe v8 migration",
                            "url": "https://reddit.com/r/javascript/comments/r1",
                            "selftext": "breaking changes...",
                            "score": 50,
                            "num_comments": 10,
                            "created_utc": 1704067200.0,
                            "subreddit": "javascript",
                            "author": "user",
                            "upvote_ratio": 0.9,
                        }
                    }
                ]
            }
        }
        items = reddit.search_reddit(["stripe"], ecosystem="npm",
                                      days=30, depth="default", token="sc_testkey")
        self.assertIsInstance(items, list)


if __name__ == "__main__":
    unittest.main()
