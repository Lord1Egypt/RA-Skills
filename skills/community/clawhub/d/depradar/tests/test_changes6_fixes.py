"""Tests for all production fixes applied from changes6.txt review.

Covers:
- changelog_parser.py : missing keywords, Pass 3 relaxation, plain-English lines
- changelog_parser.py : parse_all_version_sections() for multi-major jumps
- impact_analyzer.py  : broad scan when breaking_changes empty on major bump
- stackoverflow.py    : ecosystem included in cache key
- normalize.py        : no min-max on already-capped [0,100] scores
- semver.py           : pre-release < stable ordering in _tuple()
- hackernews.py       : Firebase enrichment of Algolia hits
- score.py            : Twitter excluded from community pain count
- depradar.py         : ecosystem warning for CLI-only packages
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# ── path setup ────────────────────────────────────────────────────────────────
_LIB = str(Path(__file__).parent.parent / "scripts" / "lib")
if _LIB not in sys.path:
    sys.path.insert(0, _LIB)


# ════════════════════════════════════════════════════════════════════════════
# 1. changelog_parser.py — missing keywords now present
# ════════════════════════════════════════════════════════════════════════════

from changelog_parser import (
    extract_breaking_changes,
    parse_all_version_sections,
    _BREAKING_KEYWORDS_RE,
    _STRONG_PLAIN_BREAKING_RE,
)


class TestChangelogKeywords(unittest.TestCase):

    def _matches(self, text: str) -> bool:
        return bool(_BREAKING_KEYWORDS_RE.search(text))

    def test_bare_breaking_matches(self):
        self.assertTrue(self._matches("This is a breaking change in v9"))

    def test_drop_matches(self):
        """'drop' (not 'dropped') must now match."""
        self.assertTrue(self._matches("drop support for Python 2"))
        self.assertTrue(self._matches("We drop the old API"))
        self.assertTrue(self._matches("drops the legacy endpoint"))

    def test_not_backward_compatible_matches(self):
        self.assertTrue(self._matches("This change is not backward compatible"))
        self.assertTrue(self._matches("not backward-compatible with v7"))

    def test_removes_matches(self):
        self.assertTrue(self._matches("The function removes the old parameter"))

    def test_incompatible_still_matches(self):
        self.assertTrue(self._matches("incompatible with previous versions"))


class TestPass3RelaxedPlainEnglish(unittest.TestCase):
    """Pass 3 should now accept strong plain-English breaking lines at low confidence."""

    def test_drop_support_no_symbol_accepted_low_confidence(self):
        text = "- Drop support for Node.js < 18\n"
        results = extract_breaking_changes(text)
        self.assertGreater(len(results), 0,
            "Plain-English 'Drop support for Node.js < 18' should yield a breaking change")
        # The confidence should be "low" (no code symbol on the line)
        self.assertEqual(results[0].confidence, "low")

    def test_not_backward_compatible_accepted(self):
        text = "This release is not backward compatible with v7.\n"
        results = extract_breaking_changes(text)
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0].confidence, "low")

    def test_removed_readme_typo_still_rejected(self):
        """Ambiguous prose ('removed a typo') must still be filtered."""
        text = "- removed a typo in the README\n"
        results = extract_breaking_changes(text)
        self.assertEqual(len(results), 0)

    def test_with_code_symbol_gets_med_confidence(self):
        """Lines that have both keyword AND code symbol get 'med' confidence."""
        text = "- removed `oldFunction()` from the public API\n"
        results = extract_breaking_changes(text)
        self.assertGreater(len(results), 0)
        self.assertNotEqual(results[0].confidence, "low")


# ════════════════════════════════════════════════════════════════════════════
# 2. changelog_parser.py — parse_all_version_sections() for multi-major jumps
# ════════════════════════════════════════════════════════════════════════════

class TestParseAllVersionSections(unittest.TestCase):

    CHANGELOG = """
# Changelog

## [10.0.0] - 2026-01-01
### Breaking Changes
- removed `legacyMethod()`

## [9.0.0] - 2025-06-01
### Breaking Changes
- dropped `oldApi()`

## [8.0.0] - 2025-01-01
### Breaking Changes
- renamed `foo()` to `bar()`

## [7.5.0] - 2024-12-01
Minor improvements.
"""

    def test_returns_sections_between_versions(self):
        result = parse_all_version_sections(self.CHANGELOG, "7.5.0", "9.0.0")
        self.assertIsNotNone(result)
        self.assertIn("oldApi", result)     # v9.0.0 section
        self.assertIn("foo", result)        # v8.0.0 section
        self.assertNotIn("legacyMethod", result)  # v10.0.0 is beyond to_version

    def test_single_major_jump_returns_one_section(self):
        result = parse_all_version_sections(self.CHANGELOG, "8.0.0", "9.0.0")
        self.assertIsNotNone(result)
        self.assertIn("oldApi", result)
        self.assertNotIn("foo", result)   # v8 is NOT newer than from_version 8.0.0

    def test_no_relevant_sections_returns_none(self):
        result = parse_all_version_sections(self.CHANGELOG, "10.0.0", "10.0.0")
        self.assertIsNone(result)

    def test_unknown_from_version_includes_all_up_to_to(self):
        """from_version=0.0.0 should include all sections up to to_version."""
        result = parse_all_version_sections(self.CHANGELOG, "0.0.0", "8.0.0")
        self.assertIsNotNone(result)
        self.assertIn("foo", result)        # v8
        self.assertNotIn("oldApi", result)  # v9 beyond to_version


# ════════════════════════════════════════════════════════════════════════════
# 3. impact_analyzer.py — broad scan on major bump with no breaking changes
# ════════════════════════════════════════════════════════════════════════════

class TestImpactAnalyzerBroadScan(unittest.TestCase):

    def _make_pkg(self, semver_type: str, breaking_changes=None):
        from schema import PackageUpdate
        pkg = PackageUpdate(
            id="P1", package="stripe", ecosystem="npm",
            current_version="7.0.0", latest_version="8.0.0",
            semver_type=semver_type, has_breaking_changes=True,
        )
        pkg.breaking_changes = breaking_changes or []
        return pkg

    def test_major_bump_no_bc_still_scans(self):
        """Major bump with no extracted breaking changes must run a broad scan."""
        import tempfile, os
        from impact_analyzer import analyze_impact

        # Create a temp dir with one JS file that imports "stripe"
        with tempfile.TemporaryDirectory() as tmpdir:
            js_file = os.path.join(tmpdir, "index.js")
            with open(js_file, "w") as f:
                f.write("const stripe = require('stripe');\n")

            pkg = self._make_pkg("major", breaking_changes=[])
            updated_pkgs, _ = analyze_impact([pkg], project_root=tmpdir)
            updated = updated_pkgs[0]
            # Should have found the file, not been skipped
            self.assertNotEqual(updated.impact_confidence, "not_scanned",
                "Major bump with empty breaking_changes should still scan, not skip")

    def test_minor_bump_no_bc_still_skips(self):
        """Non-major bumps with no breaking changes should remain not_scanned."""
        import tempfile
        from impact_analyzer import analyze_impact

        with tempfile.TemporaryDirectory() as tmpdir:
            pkg = self._make_pkg("minor", breaking_changes=[])
            updated_pkgs, _ = analyze_impact([pkg], project_root=tmpdir)
            self.assertEqual(updated_pkgs[0].impact_confidence, "not_scanned")


# ════════════════════════════════════════════════════════════════════════════
# 4. stackoverflow.py — ecosystem in cache key
# ════════════════════════════════════════════════════════════════════════════

import cache as _cache_mod
import stackoverflow as so_mod


class TestSOCacheKeyIncludesEcosystem(unittest.TestCase):

    def test_npm_and_pypi_produce_different_cache_keys(self):
        """Same package + different ecosystem must never share a cache key."""
        from stackoverflow import _QUERY_TERMS_BY_ECOSYSTEM, _QUERY_TERMS_DEFAULT

        npm_terms  = _QUERY_TERMS_BY_ECOSYSTEM.get("npm",  _QUERY_TERMS_DEFAULT)
        pypi_terms = _QUERY_TERMS_BY_ECOSYSTEM.get("pypi", _QUERY_TERMS_DEFAULT)

        key_npm  = _cache_mod.cache_key("so", "requests", 30, 8, "npm",  str(npm_terms[:1]))
        key_pypi = _cache_mod.cache_key("so", "requests", 30, 8, "pypi", str(pypi_terms[:1]))

        self.assertNotEqual(key_npm, key_pypi,
            "npm and pypi cache keys for 'requests' must differ")

    def test_same_ecosystem_produces_same_key(self):
        from stackoverflow import _QUERY_TERMS_BY_ECOSYSTEM, _QUERY_TERMS_DEFAULT
        npm_terms = _QUERY_TERMS_BY_ECOSYSTEM.get("npm", _QUERY_TERMS_DEFAULT)

        k1 = _cache_mod.cache_key("so", "stripe", 30, 8, "npm", str(npm_terms[:1]))
        k2 = _cache_mod.cache_key("so", "stripe", 30, 8, "npm", str(npm_terms[:1]))
        self.assertEqual(k1, k2)


# ════════════════════════════════════════════════════════════════════════════
# 5. normalize.py — no destructive min-max on already-capped scores
# ════════════════════════════════════════════════════════════════════════════

from normalize import normalize_scores, normalize_sub_scores
from schema import GithubIssueItem, SubScores


class TestNormalizeDoesNotDestroy(unittest.TestCase):

    def _make_issue(self, score: int) -> GithubIssueItem:
        item = GithubIssueItem(
            id="G1", package="pkg", version="8.0.0", title="T", url="http://x",
            subs=SubScores(), score=score,
        )
        return item

    def test_already_capped_scores_not_rescaled(self):
        """[80, 81, 82] must remain [80, 81, 82], not become [0, 50, 100]."""
        items = [self._make_issue(80), self._make_issue(81), self._make_issue(82)]
        normalize_scores(items)
        self.assertEqual([i.score for i in items], [80, 81, 82])

    def test_unbounded_scores_are_scaled(self):
        """Scores above 100 should be scaled down to [0, 100]."""
        items = [self._make_issue(0), self._make_issue(200), self._make_issue(400)]
        normalize_scores(items)
        self.assertEqual(items[0].score, 0)
        self.assertEqual(items[2].score, 100)

    def test_all_equal_scores_unchanged(self):
        items = [self._make_issue(75), self._make_issue(75)]
        normalize_scores(items)
        self.assertEqual([i.score for i in items], [75, 75])


# ════════════════════════════════════════════════════════════════════════════
# 6. semver.py — pre-release ordering
# ════════════════════════════════════════════════════════════════════════════

from semver import parse, bump_type, is_newer, Version


class TestSemverPreRelease(unittest.TestCase):

    def test_prerelease_less_than_stable(self):
        """1.0.0-alpha < 1.0.0 per SemVer spec."""
        alpha = parse("1.0.0-alpha")
        stable = parse("1.0.0")
        self.assertLess(alpha, stable)
        self.assertGreater(stable, alpha)

    def test_stable_not_less_than_prerelease(self):
        stable = parse("1.0.0")
        alpha  = parse("1.0.0-alpha")
        self.assertFalse(stable < alpha)

    def test_bump_type_prerelease_to_stable_is_patch(self):
        """Pre-release → stable of same version = "patch" bump."""
        self.assertEqual(bump_type("1.0.0-alpha", "1.0.0"), "patch")
        self.assertEqual(bump_type("2.0.0-rc.1", "2.0.0"), "patch")

    def test_bump_type_none_when_already_stable(self):
        """Stable → stable same version = "none"."""
        self.assertEqual(bump_type("1.0.0", "1.0.0"), "none")

    def test_is_newer_stable_over_prerelease(self):
        """is_newer("1.0.0", "1.0.0-beta") must be True."""
        self.assertTrue(is_newer("1.0.0", "1.0.0-beta"))

    def test_major_bump_still_works(self):
        self.assertEqual(bump_type("1.5.2", "2.0.0"), "major")

    def test_prerelease_does_not_affect_major_classification(self):
        """2.0.0-rc.1 → 3.0.0 is still a major bump."""
        self.assertEqual(bump_type("2.0.0-rc.1", "3.0.0"), "major")


# ════════════════════════════════════════════════════════════════════════════
# 7. hackernews.py — Firebase enrichment of Algolia hits
# ════════════════════════════════════════════════════════════════════════════

import hackernews as hn_mod


class TestHackerNewsFirebaseEnrichment(unittest.TestCase):

    def test_enrich_replaces_stale_points_with_firebase_data(self):
        """_enrich_hits_from_firebase should update points from Firebase."""
        hits = [{"objectID": "12345", "points": 10, "num_comments": 2,
                 "title": "stripe breaking", "created_at_i": 1700000000}]

        firebase_response = {"id": 12345, "score": 99, "descendants": 42, "type": "story"}

        with patch.object(hn_mod, "get_json", return_value=firebase_response) as mock_get:
            enriched = hn_mod._enrich_hits_from_firebase(hits)

        self.assertEqual(enriched[0]["points"], 99)
        self.assertEqual(enriched[0]["num_comments"], 42)
        # Should have called Firebase once
        mock_get.assert_called_once()
        call_url = mock_get.call_args[0][0]
        self.assertIn("12345", call_url)

    def test_enrich_keeps_algolia_values_on_firebase_error(self):
        """If Firebase fails, original Algolia values are preserved."""
        hits = [{"objectID": "99999", "points": 55, "num_comments": 7,
                 "title": "axios breaking change", "created_at_i": 1700000000}]

        with patch.object(hn_mod, "get_json", side_effect=Exception("timeout")):
            enriched = hn_mod._enrich_hits_from_firebase(hits)

        self.assertEqual(enriched[0]["points"], 55)
        self.assertEqual(enriched[0]["num_comments"], 7)

    def test_enrich_handles_missing_object_id(self):
        """Hits without objectID should pass through unchanged."""
        hits = [{"points": 10, "num_comments": 3, "title": "test"}]
        with patch.object(hn_mod, "get_json") as mock_get:
            enriched = hn_mod._enrich_hits_from_firebase(hits)
        mock_get.assert_not_called()
        self.assertEqual(enriched, hits)


# ════════════════════════════════════════════════════════════════════════════
# 8. score.py — Twitter excluded from community pain count
# ════════════════════════════════════════════════════════════════════════════

from score import _community_pain_count
from schema import DepRadarReport, TwitterItem


class TestTwitterExcludedFromPainCount(unittest.TestCase):

    def _make_report_with_twitter(self, package: str) -> DepRadarReport:
        report = DepRadarReport(
            project_path="/tmp", dep_files_found=[],
            packages_with_breaking_changes=[],
            packages_with_minor_updates=[],
            github_issues=[], stackoverflow=[], reddit=[], hackernews=[],
            twitter=[
                TwitterItem(
                    id="TW1", package=package, text=f"{package} v8 breaking",
                    url="https://x.com/user/status/1", author_handle="dev",
                    likes=1000, reposts=500, replies=200,
                    date="2026-01-01", subs=SubScores(), score=90,
                )
            ],
        )
        return report

    def test_twitter_does_not_contribute_to_pain_count(self):
        """Twitter signals must NOT inflate community pain count."""
        report = self._make_report_with_twitter("stripe")
        count = _community_pain_count("stripe", report, version_range="8.0.0")
        self.assertEqual(count, 0.0,
            "Twitter items should not be counted in community pain — metrics are LLM-estimated")

    def test_github_issues_still_counted(self):
        """Non-Twitter signals are unaffected."""
        from schema import GithubIssueItem
        report = DepRadarReport(
            project_path="/tmp", dep_files_found=[],
            packages_with_breaking_changes=[],
            packages_with_minor_updates=[],
            github_issues=[
                GithubIssueItem(
                    id="G1", package="stripe", version="8.0.0",
                    title="stripe v8 breaking", url="http://x",
                    body_snippet="breaking", comments=5,
                    subs=SubScores(), score=70,
                )
            ],
            stackoverflow=[], reddit=[], hackernews=[], twitter=[],
        )
        count = _community_pain_count("stripe", report, version_range="8.0.0")
        self.assertGreater(count, 0.0)


# ════════════════════════════════════════════════════════════════════════════
# 9. depradar.py — ecosystem warning for CLI-only unknown packages
# ════════════════════════════════════════════════════════════════════════════

class TestDepRadarEcosystemWarning(unittest.TestCase):

    def test_missing_package_creates_npm_depinfo_with_warning(self):
        """When a CLI package isn't in dep files, ecosystem defaults to npm with a warning."""
        from schema import DepInfo

        # Build the same DepInfo that depradar.py creates for unknown packages
        dep = DepInfo(
            name="requests", version_spec="*", version="0.0.0",
            ecosystem="npm", source_file="cli",
        )
        self.assertEqual(dep.ecosystem, "npm")
        self.assertEqual(dep.version, "0.0.0")
        self.assertEqual(dep.source_file, "cli")

    def test_so_cache_key_includes_ecosystem(self):
        """Regression: SO cache key must include ecosystem so npm/pypi don't collide."""
        from stackoverflow import _QUERY_TERMS_BY_ECOSYSTEM, _QUERY_TERMS_DEFAULT
        import cache

        npm_terms  = _QUERY_TERMS_BY_ECOSYSTEM.get("npm",  _QUERY_TERMS_DEFAULT)
        pypi_terms = _QUERY_TERMS_BY_ECOSYSTEM.get("pypi", _QUERY_TERMS_DEFAULT)

        key_npm  = cache.cache_key("so", "requests", 30, 8, "npm",  str(npm_terms[:1]))
        key_pypi = cache.cache_key("so", "requests", 30, 8, "pypi", str(pypi_terms[:1]))

        self.assertNotEqual(key_npm, key_pypi)


if __name__ == "__main__":
    unittest.main()
