"""Tests for scripts/lib/semver.py"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "lib"))

from semver import (
    Version,
    bump_type,
    extract_numeric,
    is_breaking,
    is_newer,
    latest_stable,
    newer_versions,
    parse,
)


class TestParse(unittest.TestCase):

    def test_plain_semver(self):
        v = parse("1.2.3")
        self.assertIsNotNone(v)
        self.assertEqual(v.major, 1)
        self.assertEqual(v.minor, 2)
        self.assertEqual(v.patch, 3)
        self.assertEqual(v.pre, "")

    def test_v_prefix(self):
        v = parse("v1.2.3")
        self.assertIsNotNone(v)
        self.assertEqual(v.major, 1)
        self.assertEqual(v.minor, 2)
        self.assertEqual(v.patch, 3)

    def test_uppercase_v_prefix(self):
        v = parse("V2.0.0")
        self.assertIsNotNone(v)
        self.assertEqual(v.major, 2)

    def test_caret_range(self):
        v = parse("^1.2.3")
        self.assertIsNotNone(v)
        self.assertEqual(v.major, 1)
        self.assertEqual(v.minor, 2)
        self.assertEqual(v.patch, 3)

    def test_tilde_range(self):
        v = parse("~1.4.2")
        self.assertIsNotNone(v)
        self.assertEqual(v.major, 1)
        self.assertEqual(v.minor, 4)
        self.assertEqual(v.patch, 2)

    def test_gte_range(self):
        v = parse(">=2.0.0")
        self.assertIsNotNone(v)
        self.assertEqual(v.major, 2)

    def test_pypi_specifier_eq(self):
        v = parse("==1.4.5")
        self.assertIsNotNone(v)
        self.assertEqual(v.major, 1)
        self.assertEqual(v.minor, 4)
        self.assertEqual(v.patch, 5)

    def test_pypi_compat_release(self):
        v = parse("~=1.4.2")
        self.assertIsNotNone(v)
        self.assertEqual(v.major, 1)
        self.assertEqual(v.minor, 4)

    def test_pypi_range_takes_first(self):
        v = parse(">=1.0,<2.0")
        self.assertIsNotNone(v)
        self.assertEqual(v.major, 1)
        self.assertEqual(v.minor, 0)

    def test_prerelease(self):
        v = parse("1.2.3-alpha.1")
        self.assertIsNotNone(v)
        self.assertEqual(v.major, 1)
        self.assertEqual(v.minor, 2)
        self.assertEqual(v.patch, 3)
        self.assertIn("alpha", v.pre)

    def test_rc_prerelease(self):
        v = parse("2.0.0-rc.2")
        self.assertIsNotNone(v)
        self.assertIn("rc", v.pre)

    def test_go_pseudo_version(self):
        v = parse("v1.2.3-20230101120000-abcdef123456")
        self.assertIsNotNone(v)
        self.assertEqual(v.major, 1)
        self.assertEqual(v.minor, 2)
        self.assertEqual(v.patch, 3)

    def test_major_minor_only(self):
        v = parse("1.2")
        self.assertIsNotNone(v)
        self.assertEqual(v.major, 1)
        self.assertEqual(v.minor, 2)
        self.assertEqual(v.patch, 0)

    def test_major_only(self):
        v = parse("3")
        self.assertIsNotNone(v)
        self.assertEqual(v.major, 3)

    def test_empty_string_returns_none(self):
        self.assertIsNone(parse(""))

    def test_none_string_returns_none(self):
        self.assertIsNone(parse(None))  # type: ignore[arg-type]

    def test_invalid_returns_none(self):
        self.assertIsNone(parse("not-a-version"))

    def test_star_wildcard_returns_none(self):
        self.assertIsNone(parse("*"))

    def test_repr(self):
        v = Version(1, 2, 3)
        self.assertEqual(repr(v), "1.2.3")

    def test_repr_with_pre(self):
        v = Version(1, 2, 3, "alpha.1")
        self.assertEqual(repr(v), "1.2.3-alpha.1")

    def test_comparison_lt(self):
        self.assertLess(parse("1.0.0"), parse("2.0.0"))

    def test_comparison_eq(self):
        self.assertEqual(parse("1.2.3"), parse("1.2.3"))

    def test_comparison_gt(self):
        self.assertGreater(parse("2.1.0"), parse("1.9.9"))


class TestExtractNumeric(unittest.TestCase):

    def test_caret(self):
        self.assertEqual(extract_numeric("^4.17.0"), "4.17.0")

    def test_gte_lt(self):
        result = extract_numeric(">=1.0,<2")
        self.assertEqual(result, "1.0.0")

    def test_compat_release(self):
        result = extract_numeric("~=1.4.2")
        self.assertEqual(result, "1.4.2")

    def test_plain(self):
        self.assertEqual(extract_numeric("1.2.3"), "1.2.3")

    def test_invalid_returns_none(self):
        self.assertIsNone(extract_numeric("*"))


class TestBumpType(unittest.TestCase):

    def test_major_bump(self):
        self.assertEqual(bump_type("7.0.0", "8.0.0"), "major")

    def test_minor_bump(self):
        self.assertEqual(bump_type("1.2.0", "1.3.0"), "minor")

    def test_patch_bump(self):
        self.assertEqual(bump_type("1.2.3", "1.2.4"), "patch")

    def test_no_bump_same_version(self):
        self.assertEqual(bump_type("1.0.0", "1.0.0"), "none")

    def test_no_bump_older_latest(self):
        self.assertEqual(bump_type("2.0.0", "1.9.9"), "none")

    def test_unknown_current(self):
        self.assertEqual(bump_type("not-valid", "1.0.0"), "unknown")

    def test_unknown_latest(self):
        self.assertEqual(bump_type("1.0.0", "not-valid"), "unknown")

    def test_major_bump_from_range(self):
        self.assertEqual(bump_type("^7.0.0", "8.0.0"), "major")

    def test_minor_bump_cross_patch(self):
        self.assertEqual(bump_type("1.0.9", "1.1.0"), "minor")


class TestIsBreaking(unittest.TestCase):

    def test_major_is_breaking(self):
        self.assertTrue(is_breaking("7.0.0", "8.0.0"))

    def test_minor_not_breaking(self):
        self.assertFalse(is_breaking("1.2.0", "1.3.0"))

    def test_patch_not_breaking(self):
        self.assertFalse(is_breaking("1.2.3", "1.2.4"))

    def test_same_version_not_breaking(self):
        self.assertFalse(is_breaking("1.0.0", "1.0.0"))


class TestNewerVersions(unittest.TestCase):

    def test_returns_newer_sorted(self):
        versions = ["7.0.0", "8.0.0", "6.0.0", "9.0.0", "10.0.0"]
        result = newer_versions(versions, "7.0.0")
        self.assertIn("8.0.0", result)
        self.assertIn("9.0.0", result)
        self.assertIn("10.0.0", result)
        self.assertNotIn("7.0.0", result)
        self.assertNotIn("6.0.0", result)

    def test_sorted_newest_first(self):
        versions = ["8.0.0", "9.0.0", "10.0.0"]
        result = newer_versions(versions, "7.0.0")
        self.assertEqual(result[0], "10.0.0")

    def test_empty_when_no_newer(self):
        result = newer_versions(["1.0.0", "0.9.0"], "2.0.0")
        self.assertEqual(result, [])

    def test_empty_list(self):
        result = newer_versions([], "1.0.0")
        self.assertEqual(result, [])

    def test_invalid_baseline_returns_empty(self):
        result = newer_versions(["1.0.0", "2.0.0"], "invalid")
        self.assertEqual(result, [])

    def test_skips_invalid_versions_in_list(self):
        versions = ["bad-version", "2.0.0", "3.0.0"]
        result = newer_versions(versions, "1.0.0")
        self.assertNotIn("bad-version", result)
        self.assertIn("2.0.0", result)


class TestLatestStable(unittest.TestCase):

    def test_returns_highest_stable(self):
        versions = ["1.0.0", "2.0.0", "2.1.0", "3.0.0-alpha"]
        result = latest_stable(versions)
        self.assertEqual(result, "2.1.0")

    def test_skips_prereleases(self):
        versions = ["1.0.0", "2.0.0-beta.1", "2.0.0-rc.1"]
        result = latest_stable(versions)
        self.assertEqual(result, "1.0.0")

    def test_all_prereleases_returns_none(self):
        versions = ["1.0.0-alpha", "2.0.0-beta"]
        result = latest_stable(versions)
        self.assertIsNone(result)

    def test_empty_list_returns_none(self):
        result = latest_stable([])
        self.assertIsNone(result)

    def test_single_stable(self):
        self.assertEqual(latest_stable(["1.0.0"]), "1.0.0")

    def test_with_v_prefix(self):
        versions = ["v1.0.0", "v2.0.0", "v3.0.0-rc.1"]
        result = latest_stable(versions)
        self.assertEqual(result, "v2.0.0")

    def test_multiple_patch_versions(self):
        versions = ["1.0.0", "1.0.1", "1.0.2", "1.1.0"]
        result = latest_stable(versions)
        self.assertEqual(result, "1.1.0")


if __name__ == "__main__":
    unittest.main()
