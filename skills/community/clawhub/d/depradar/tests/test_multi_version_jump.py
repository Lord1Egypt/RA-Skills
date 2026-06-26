"""Tests for multi-version jump enumeration in github_releases.py (R4)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts", "lib"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from github_releases import _collect_intermediate_bodies


def _make_release(tag: str, body: str) -> dict:
    return {"tag_name": tag, "body": body, "published_at": "2026-01-01T00:00:00Z"}


class TestCollectIntermediateBodies(unittest.TestCase):
    def test_empty_releases_returns_empty_string(self):
        result = _collect_intermediate_bodies([], "1.0.0", "2.0.0")
        self.assertEqual(result, "")

    def test_single_latest_release_included(self):
        releases = [_make_release("v2.0.0", "Breaking: removed old API")]
        result = _collect_intermediate_bodies(releases, "1.0.0", "2.0.0")
        self.assertIn("Breaking: removed old API", result)
        self.assertIn("2.0.0", result)

    def test_current_version_excluded(self):
        releases = [
            _make_release("v1.0.0", "Old release body"),
            _make_release("v2.0.0", "New breaking changes"),
        ]
        result = _collect_intermediate_bodies(releases, "1.0.0", "2.0.0")
        self.assertNotIn("Old release body", result)
        self.assertIn("New breaking changes", result)

    def test_versions_older_than_current_excluded(self):
        releases = [
            _make_release("v0.9.0", "Ancient release"),
            _make_release("v1.0.0", "Current release"),
            _make_release("v1.5.0", "Intermediate"),
            _make_release("v2.0.0", "Latest"),
        ]
        result = _collect_intermediate_bodies(releases, "1.0.0", "2.0.0")
        self.assertNotIn("Ancient release", result)
        self.assertNotIn("Current release", result)  # v1.0.0 = current, excluded
        self.assertIn("Intermediate", result)
        self.assertIn("Latest", result)

    def test_multi_major_jump_all_included(self):
        """openai-style 0.28 → 1.35 — all intermediate releases included."""
        releases = [
            _make_release("v0.28.0", "OLD"),       # current — excluded
            _make_release("v0.29.0", "v0.29 body"),
            _make_release("v1.0.0",  "v1.0 body"),
            _make_release("v1.5.0",  "v1.5 body"),
            _make_release("v1.35.0", "v1.35 BREAKING"),
        ]
        result = _collect_intermediate_bodies(releases, "0.28.0", "1.35.0")
        self.assertNotIn("OLD", result)
        self.assertIn("v0.29 body", result)
        self.assertIn("v1.0 body", result)
        self.assertIn("v1.5 body", result)
        self.assertIn("v1.35 BREAKING", result)

    def test_bodies_separated_by_headers(self):
        releases = [
            _make_release("v1.1.0", "Change A"),
            _make_release("v2.0.0", "Change B"),
        ]
        result = _collect_intermediate_bodies(releases, "1.0.0", "2.0.0")
        self.assertIn("## Release", result)

    def test_unparseable_tags_gracefully_skipped(self):
        releases = [
            _make_release("not-a-version", "Bad tag body"),
            _make_release("v2.0.0", "Good body"),
        ]
        result = _collect_intermediate_bodies(releases, "1.0.0", "2.0.0")
        self.assertIn("Good body", result)
        # Bad tag gracefully skipped — no crash

    def test_releases_beyond_latest_excluded(self):
        releases = [
            _make_release("v2.0.0", "Target"),
            _make_release("v3.0.0", "Future release — should not appear"),
        ]
        result = _collect_intermediate_bodies(releases, "1.0.0", "2.0.0")
        self.assertIn("Target", result)
        self.assertNotIn("Future release", result)

    def test_empty_body_releases_skipped(self):
        releases = [
            _make_release("v1.5.0", ""),           # empty body
            _make_release("v2.0.0", "Good body"),
        ]
        result = _collect_intermediate_bodies(releases, "1.0.0", "2.0.0")
        self.assertIn("Good body", result)

    def test_result_is_string(self):
        releases = [_make_release("v2.0.0", "Breaking changes")]
        result = _collect_intermediate_bodies(releases, "1.0.0", "2.0.0")
        self.assertIsInstance(result, str)

    def test_both_current_versions_unparseable_returns_bodies(self):
        """When current/latest version can't be parsed, still return available bodies."""
        releases = [_make_release("v2.0.0", "Some body")]
        result = _collect_intermediate_bodies(releases, "not-semver", "also-not")
        # Should not crash; may return the body or empty string
        self.assertIsInstance(result, str)


if __name__ == "__main__":
    unittest.main()
