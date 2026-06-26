"""Tests for lib/github_releases.py — GitHub Releases API integration."""
import json
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from lib.schema import PackageUpdate

FIXTURES = os.path.join(os.path.dirname(__file__), "..", "fixtures")


def load_fixture(name: str):
    with open(os.path.join(FIXTURES, name)) as f:
        return json.load(f)


STRIPE_RELEASE_LIST = load_fixture("github_release_stripe.json")

import lib.github_releases as gr


class TestResolveRepo(unittest.TestCase):
    """resolve_repo_from_npm/pypi — take a package NAME, fetch data, return owner/repo."""

    @patch("lib.github_releases.get_json")
    def test_resolve_from_npm_extracts_github_url(self, mock_get):
        mock_get.return_value = {
            "repository": {"url": "git+https://github.com/stripe/stripe-node.git"}
        }
        result = gr.resolve_repo_from_npm("stripe")
        self.assertEqual(result, "stripe/stripe-node")

    @patch("lib.github_releases.get_json")
    def test_resolve_from_npm_ssh_url(self, mock_get):
        mock_get.return_value = {
            "repository": {"url": "git@github.com:stripe/stripe-node.git"}
        }
        result = gr.resolve_repo_from_npm("stripe")
        self.assertEqual(result, "stripe/stripe-node")

    @patch("lib.github_releases.get_json")
    def test_resolve_from_npm_returns_none_for_non_github(self, mock_get):
        mock_get.return_value = {
            "repository": {"url": "https://gitlab.com/foo/bar.git"}
        }
        result = gr.resolve_repo_from_npm("stripe")
        self.assertIsNone(result)

    @patch("lib.github_releases.get_json")
    def test_resolve_from_npm_returns_none_on_not_found(self, mock_get):
        from lib.http import NotFoundError
        mock_get.side_effect = NotFoundError("https://registry.npmjs.org/nonexistent", 404, "not found")
        result = gr.resolve_repo_from_npm("nonexistent")
        self.assertIsNone(result)

    @patch("lib.github_releases.get_json")
    def test_resolve_from_pypi_extracts_github(self, mock_get):
        mock_get.return_value = {
            "info": {
                "project_urls": {
                    "Source": "https://github.com/openai/openai-python"
                },
                "home_page": "https://openai.com",
            }
        }
        result = gr.resolve_repo_from_pypi("openai")
        self.assertEqual(result, "openai/openai-python")

    @patch("lib.github_releases.get_json")
    def test_resolve_from_pypi_homepage_fallback(self, mock_get):
        mock_get.return_value = {
            "info": {
                "home_page": "https://github.com/foo/bar",
                "project_urls": {},
            }
        }
        result = gr.resolve_repo_from_pypi("foo")
        self.assertEqual(result, "foo/bar")


class TestParseRepoUrl(unittest.TestCase):
    """_parse_repo_url — extract owner/repo from various URL formats."""

    def test_https_github(self):
        result = gr._parse_repo_url("https://github.com/stripe/stripe-node")
        self.assertEqual(result, "stripe/stripe-node")

    def test_git_plus_https(self):
        result = gr._parse_repo_url("git+https://github.com/stripe/stripe-node.git")
        self.assertEqual(result, "stripe/stripe-node")

    def test_ssh(self):
        result = gr._parse_repo_url("git@github.com:stripe/stripe-node.git")
        self.assertEqual(result, "stripe/stripe-node")

    def test_returns_none_for_non_github(self):
        result = gr._parse_repo_url("https://gitlab.com/foo/bar")
        self.assertIsNone(result)

    def test_returns_none_for_empty(self):
        result = gr._parse_repo_url("")
        self.assertIsNone(result)


class TestFetchReleases(unittest.TestCase):
    """fetch_releases — calls GitHub Releases API."""

    @patch("lib.github_releases.get_json")
    def test_returns_list(self, mock_get):
        mock_get.return_value = STRIPE_RELEASE_LIST
        releases = gr.fetch_releases("stripe", "stripe-node", "2020-01-01", 10, None)
        self.assertIsInstance(releases, list)

    @patch("lib.github_releases.get_json")
    def test_respects_max_count(self, mock_get):
        mock_get.return_value = [
            {"tag_name": f"v{i}.0.0", "draft": False, "prerelease": False,
             "body": f"release {i}", "published_at": f"2026-0{i % 9 + 1}-01T00:00:00Z"}
            for i in range(1, 6)
        ]
        releases = gr.fetch_releases("stripe", "stripe-node", "2020-01-01", 3, None)
        self.assertLessEqual(len(releases), 3)

    @patch("lib.github_releases.get_json")
    def test_returns_empty_on_not_found(self, mock_get):
        from lib.http import NotFoundError
        mock_get.side_effect = NotFoundError("https://api.github.com/repos/x/y/releases", 404, "nf")
        releases = gr.fetch_releases("nonexistent", "repo", "2020-01-01", 10, None)
        self.assertIsInstance(releases, list)
        self.assertEqual(releases, [])


class TestFetchChangelogMd(unittest.TestCase):
    """fetch_changelog_md(owner, repo, token=None) — tries multiple filenames and branches."""

    @patch("lib.github_releases.get_text")
    def test_returns_content_on_success(self, mock_get_text):
        mock_get_text.return_value = "# Changelog\n\n## v8.0.0\n\n- Removed foo"
        result = gr.fetch_changelog_md("stripe", "stripe-node", token=None)
        self.assertIsNotNone(result)
        self.assertIn("Changelog", result)

    @patch("lib.github_releases.get_json")
    @patch("lib.github_releases.get_text")
    def test_returns_none_if_all_fail(self, mock_get_text, mock_get_json):
        from lib.http import NotFoundError
        mock_get_text.side_effect = NotFoundError("url", 404, "not found")
        mock_get_json.side_effect = NotFoundError("url", 404, "not found")
        result = gr.fetch_changelog_md("stripe", "stripe-node", token=None)
        self.assertIsNone(result)


class TestFetchPackageUpdates(unittest.TestCase):
    @patch("lib.github_releases.fetch_releases")
    @patch("lib.github_releases.resolve_repo_from_npm")
    def test_returns_none_when_no_repo(self, mock_resolve, mock_releases):
        mock_resolve.return_value = None
        result = gr.fetch_package_updates(
            "nonexistent", "1.0.0", github_repo=None, ecosystem="npm"
        )
        self.assertIsNone(result)

    @patch("lib.github_releases.fetch_releases")
    def test_returns_none_when_no_newer_releases(self, mock_releases):
        # All releases are older than current version
        mock_releases.return_value = []
        result = gr.fetch_package_updates(
            "stripe", "8.0.0", github_repo="stripe/stripe-node", ecosystem="npm"
        )
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
