"""Tests for lib/github_issues.py — GitHub Issues search integration."""
import json
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from lib.schema import GithubIssueItem

FIXTURES = os.path.join(os.path.dirname(__file__), "..", "fixtures")


def load_fixture(name: str) -> dict:
    with open(os.path.join(FIXTURES, name)) as f:
        return json.load(f)


ISSUES_FIXTURE = load_fixture("github_issues_sample.json")

import lib.github_issues as gi


class TestParseIssue(unittest.TestCase):
    """_parse_issue(raw, package, idx) — internal parser."""

    def test_parses_basic_fields(self):
        raw = {
            "number": 123,
            "title": "stripe v8 breaking: constructEvent removed",
            "html_url": "https://github.com/stripe/stripe-node/issues/123",
            "state": "closed",
            "created_at": "2026-01-15T10:00:00Z",
            "body": "The webhooks.constructEvent method was removed in v8.",
            "comments": 5,
            "reactions": {"+1": 3},
            "labels": [{"name": "breaking-change"}],
            "user": {"login": "dev123"},
        }
        item = gi._parse_issue(raw, package="stripe", idx=1)
        self.assertIsInstance(item, GithubIssueItem)
        self.assertEqual(item.id, "GI1")
        self.assertEqual(item.state, "closed")
        self.assertIn("stripe", item.title.lower())
        self.assertEqual(item.comments, 5)
        self.assertEqual(item.package, "stripe")

    def test_handles_none_body(self):
        raw = {
            "number": 1,
            "title": "issue",
            "html_url": "https://github.com/foo/bar/issues/1",
            "state": "open",
            "created_at": "2026-01-01T00:00:00Z",
            "body": None,
            "comments": 0,
            "reactions": {},
            "labels": [],
            "user": {"login": "user"},
        }
        item = gi._parse_issue(raw, package="foo", idx=1)
        self.assertIsNotNone(item)
        self.assertIsNone(item.body_snippet)

    def test_assigns_sequential_id(self):
        raw = {
            "number": 42, "title": "t", "html_url": "u",
            "state": "open", "created_at": "2026-01-01T00:00:00Z",
            "body": "b", "comments": 0, "reactions": {}, "labels": [],
            "user": {"login": "u"},
        }
        item5 = gi._parse_issue(raw, "pkg", idx=5)
        self.assertEqual(item5.id, "GI5")

    def test_extracts_labels(self):
        raw = {
            "number": 1, "title": "t",
            "html_url": "https://github.com/foo/bar/issues/1",
            "state": "open", "created_at": "2026-01-01T00:00:00Z",
            "body": "body", "comments": 0, "reactions": {},
            "labels": [{"name": "breaking-change"}, {"name": "bug"}],
            "user": {"login": "u"},
        }
        item = gi._parse_issue(raw, "pkg", idx=1)
        self.assertIn("breaking-change", item.labels)
        self.assertIn("bug", item.labels)


class TestBuildQueries(unittest.TestCase):
    """_build_queries(package, repo, since_date, depth) — generate search queries."""

    def test_generates_multiple_queries(self):
        queries = gi._build_queries("stripe", "stripe/stripe-node", "2026-01-01", "default")
        self.assertGreater(len(queries), 0)
        for q in queries:
            self.assertIn("stripe", q)

    def test_includes_breaking_terms(self):
        queries = gi._build_queries("stripe", "stripe/stripe-node", "2026-01-01", "default")
        combined = " ".join(queries).lower()
        self.assertTrue(
            "break" in combined or "migration" in combined or "removed" in combined
        )

    def test_quick_mode_fewer_queries(self):
        quick = gi._build_queries("stripe", None, "2026-01-01", "quick")
        deep = gi._build_queries("stripe", None, "2026-01-01", "deep")
        self.assertLessEqual(len(quick), len(deep))

    def test_without_repo(self):
        queries = gi._build_queries("stripe", None, "2026-01-01", "default")
        self.assertGreater(len(queries), 0)


class TestDedupe(unittest.TestCase):
    """_dedupe(items) — remove duplicate issues by number."""

    def _make_item(self, n: int, title: str = "t") -> GithubIssueItem:
        return GithubIssueItem(
            id=f"GI{n}", package="stripe", version="8.0.0",
            title=title, url=f"https://github.com/x/y/issues/{n}",
            body_snippet=None, comments=0, labels=[], state="open",
            resolution_snippet=None, created_at="2026-01-01T00:00:00Z",
            subs=None, score=50, cross_refs=[],
        )

    def test_removes_duplicate_urls(self):
        items = [self._make_item(1), self._make_item(1)]
        deduped = gi._dedupe(items)
        urls = [i.url for i in deduped]
        self.assertEqual(len(set(urls)), len(deduped))

    def test_keeps_different_items(self):
        items = [self._make_item(1), self._make_item(2)]
        deduped = gi._dedupe(items)
        self.assertEqual(len(deduped), 2)


class TestScoreIssue(unittest.TestCase):
    def _make_item(self, labels=None, comments=0) -> GithubIssueItem:
        return GithubIssueItem(
            id="GI1", package="stripe", version="8.0.0",
            title="stripe v8 issue",
            url="https://github.com/x/y/issues/1",
            body_snippet=None, comments=comments,
            labels=labels or [], state="open",
            resolution_snippet=None, created_at="2026-01-15T00:00:00Z",
            subs=None, score=0, cross_refs=[],
        )

    def test_breaking_label_increases_score(self):
        without = gi._score_issue(self._make_item(labels=[]))
        with_breaking = gi._score_issue(self._make_item(labels=["breaking-change"]))
        self.assertGreater(with_breaking.score, without.score)

    def test_more_comments_higher_score(self):
        low = gi._score_issue(self._make_item(comments=0))
        high = gi._score_issue(self._make_item(comments=50))
        self.assertGreater(high.score, low.score)


class TestSearchIssuesWithMock(unittest.TestCase):
    @patch("lib.github_issues.get_json")
    def test_returns_list(self, mock_get):
        mock_get.return_value = {
            "total_count": 1,
            "items": [
                {
                    "number": 1, "title": "stripe v8 migration",
                    "html_url": "https://github.com/stripe/stripe-node/issues/1",
                    "state": "closed", "created_at": "2026-01-15T10:00:00Z",
                    "body": "constructEvent removed",
                    "comments": 10, "reactions": {"+1": 3},
                    "labels": [{"name": "breaking-change"}],
                    "user": {"login": "user"},
                }
            ]
        }
        # search_issues(packages, repos, days, depth, token)
        items = gi.search_issues(["stripe"], repos={}, token=None, days=30, depth="default")
        self.assertIsInstance(items, list)
        for item in items:
            self.assertEqual(type(item).__name__, "GithubIssueItem")

    @patch("lib.github_issues.get_json")
    def test_returns_empty_on_http_error(self, mock_get):
        from lib.http import HttpError
        mock_get.side_effect = HttpError("https://api.github.com/search/issues", 500, "err")
        items = gi.search_issues(["stripe"], repos={}, token=None, days=30, depth="default")
        self.assertIsInstance(items, list)

    @patch("lib.github_issues.get_json")
    def test_returns_empty_on_rate_limit(self, mock_get):
        from lib.http import RateLimitError
        mock_get.side_effect = RateLimitError("https://api.github.com/search/issues", 429, "limited")
        items = gi.search_issues(["stripe"], repos={}, token=None, days=30, depth="default")
        self.assertIsInstance(items, list)


if __name__ == "__main__":
    unittest.main()
