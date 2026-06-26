"""Tests for multi-version pagination in github_releases.py.

Covers Fix 1 (changes4.txt):
- fetch_releases() stop_at_version parameter
- Multi-major version jump detection + higher release cap
- _collect_intermediate_bodies() uses all fetched releases
"""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "lib"))
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from github_releases import (
    fetch_releases,
    _collect_intermediate_bodies,
    fetch_package_updates,
    DEPTH_CONFIG,
)


# ── Helpers ────────────────────────────────────────────────────────────────────

def _make_release(tag: str, body: str = "", published: str = "2024-06-01T00:00:00Z") -> dict:
    return {
        "tag_name": tag,
        "body": body,
        "published_at": published,
        "html_url": f"https://github.com/test/repo/releases/tag/{tag}",
    }


def _releases_range(start: int, end: int, prefix: str = "v1.") -> list:
    """Generate releases from prefix+end down to prefix+start (newest-first)."""
    return [_make_release(f"{prefix}{i}.0") for i in range(end, start - 1, -1)]


# ── DEPTH_CONFIG ───────────────────────────────────────────────────────────────

class TestDepthConfig(unittest.TestCase):

    def test_depth_config_has_major_caps(self):
        for mode in ("quick", "default", "deep"):
            self.assertIn("max_releases_major", DEPTH_CONFIG[mode],
                          f"{mode} mode missing max_releases_major")

    def test_major_cap_larger_than_normal_cap(self):
        for mode in ("quick", "default", "deep"):
            normal = DEPTH_CONFIG[mode]["max_releases"]
            major  = DEPTH_CONFIG[mode]["max_releases_major"]
            self.assertGreater(major, normal,
                               f"{mode}: major cap ({major}) must exceed normal cap ({normal})")

    def test_default_mode_caps(self):
        cfg = DEPTH_CONFIG["default"]
        self.assertEqual(cfg["max_releases"], 10)
        self.assertGreaterEqual(cfg["max_releases_major"], 100)

    def test_deep_mode_caps(self):
        cfg = DEPTH_CONFIG["deep"]
        self.assertEqual(cfg["max_releases"], 20)
        self.assertGreaterEqual(cfg["max_releases_major"], 300)


# ── fetch_releases() stop_at_version ──────────────────────────────────────────

class TestFetchReleasesStopAtVersion(unittest.TestCase):

    def _mock_get_json(self, page_data: list):
        """Return a get_json mock that yields page_data on first call, then []."""
        call_count = [0]
        def _get_json(url, headers=None, params=None):
            call_count[0] += 1
            if call_count[0] == 1:
                return page_data
            return []
        return _get_json

    def test_stop_at_version_stops_pagination(self):
        """stop_at_version=1.0.0 stops once that release is encountered."""
        releases = [
            _make_release("v1.3.0"),
            _make_release("v1.2.0"),
            _make_release("v1.1.0"),
            _make_release("v1.0.0"),  # ← stop here
            _make_release("v0.9.0"),
        ]
        with patch("github_releases.get_json", side_effect=self._mock_get_json(releases)):
            result = fetch_releases("owner", "repo", "2020-01-01", max_count=100,
                                    stop_at_version="1.0.0")
        # Should include 1.0.0 but stop there — 0.9.0 NOT included
        tags = [r["tag_name"] for r in result]
        self.assertIn("v1.3.0", tags)
        self.assertIn("v1.0.0", tags)
        self.assertNotIn("v0.9.0", tags)

    def test_stop_at_version_with_v_prefix(self):
        """stop_at_version handles tags with/without 'v' prefix consistently."""
        releases = [
            _make_release("v2.0.0"),
            _make_release("1.5.0"),   # tag without 'v'
            _make_release("v1.0.0"),  # stop here
            _make_release("v0.8.0"),
        ]
        with patch("github_releases.get_json", side_effect=self._mock_get_json(releases)):
            result = fetch_releases("owner", "repo", "2020-01-01", max_count=100,
                                    stop_at_version="v1.0.0")
        tags = [r["tag_name"] for r in result]
        self.assertNotIn("v0.8.0", tags)

    def test_no_stop_at_version_uses_max_count(self):
        """Without stop_at_version, max_count is the sole limit."""
        releases = [_make_release(f"v1.{i}.0") for i in range(20, 0, -1)]
        with patch("github_releases.get_json", side_effect=self._mock_get_json(releases)):
            result = fetch_releases("owner", "repo", "2020-01-01", max_count=5)
        self.assertEqual(len(result), 5)

    def test_stop_at_version_below_all_releases(self):
        """stop_at_version older than all releases → fetch up to max_count."""
        releases = [_make_release(f"v2.{i}.0") for i in range(10, 0, -1)]
        with patch("github_releases.get_json", side_effect=self._mock_get_json(releases)):
            result = fetch_releases("owner", "repo", "2020-01-01", max_count=3,
                                    stop_at_version="1.0.0")
        self.assertEqual(len(result), 3)


# ── _collect_intermediate_bodies() ────────────────────────────────────────────

class TestCollectIntermediateBodies(unittest.TestCase):

    def test_collects_all_versions_between_current_and_latest(self):
        """All versions strictly between current and latest are included."""
        releases = [
            _make_release("v1.3.0", body="body 1.3"),
            _make_release("v1.2.0", body="body 1.2"),
            _make_release("v1.1.0", body="body 1.1"),
            _make_release("v1.0.0", body="body 1.0"),   # current — excluded
        ]
        result = _collect_intermediate_bodies(releases, "1.0.0", "1.3.0")
        self.assertIn("body 1.3", result)
        self.assertIn("body 1.2", result)
        self.assertIn("body 1.1", result)
        self.assertNotIn("body 1.0", result)

    def test_excludes_versions_newer_than_latest(self):
        """Releases newer than latest are excluded."""
        releases = [
            _make_release("v1.5.0", body="future"),
            _make_release("v1.3.0", body="latest"),
            _make_release("v1.1.0", body="old"),
        ]
        result = _collect_intermediate_bodies(releases, "1.0.0", "1.3.0")
        self.assertNotIn("future", result)
        self.assertIn("latest", result)

    def test_thirty_releases_all_collected(self):
        """30-release span — all bodies present (validates no cap applied)."""
        releases = [_make_release(f"v1.{i}.0", body=f"body {i}") for i in range(30, 0, -1)]
        result = _collect_intermediate_bodies(releases, "0.8.0", "1.30.0")
        for i in range(1, 31):
            self.assertIn(f"body {i}", result)

    def test_returns_empty_when_no_bodies(self):
        """Releases with no body text → empty result."""
        releases = [_make_release("v1.1.0", body=""), _make_release("v1.0.0", body="")]
        result = _collect_intermediate_bodies(releases, "0.9.0", "1.1.0")
        self.assertEqual(result.strip(), "")

    def test_sections_separated_by_divider(self):
        """Multiple releases are separated by '---' dividers."""
        releases = [
            _make_release("v1.2.0", body="change A"),
            _make_release("v1.1.0", body="change B"),
        ]
        result = _collect_intermediate_bodies(releases, "1.0.0", "1.2.0")
        self.assertIn("---", result)


if __name__ == "__main__":
    unittest.main()
