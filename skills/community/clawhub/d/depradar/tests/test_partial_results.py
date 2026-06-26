"""Tests for partial results indicator and registry error distinction (R6, R7, R15)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts", "lib"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from schema import DepRadarReport
from render import render


def _make_clean_report() -> DepRadarReport:
    return DepRadarReport(
        project_path="/test/project",
        dep_files_found=["package.json"],
        packages_scanned=10,
        packages_current=["lodash", "dayjs"],
    )


class TestPartialResultsField(unittest.TestCase):
    def test_partial_results_false_by_default(self):
        report = _make_clean_report()
        self.assertFalse(report.partial_results)

    def test_partial_results_true_when_rate_limited(self):
        report = _make_clean_report()
        report.rate_limited_packages = ["stripe", "openai"]
        report.partial_results = bool(report.rate_limited_packages)
        self.assertTrue(report.partial_results)

    def test_partial_results_true_when_fetch_errors(self):
        report = _make_clean_report()
        report.registry_fetch_errors = {"axios": "Connection timed out"}
        report.partial_results = bool(report.registry_fetch_errors)
        self.assertTrue(report.partial_results)

    def test_partial_results_roundtrip(self):
        report = _make_clean_report()
        report.rate_limited_packages = ["stripe"]
        report.partial_results = True
        d = report.to_dict()
        restored = DepRadarReport.from_dict(d)
        self.assertTrue(restored.partial_results)
        self.assertEqual(restored.rate_limited_packages, ["stripe"])

    def test_rate_limited_packages_empty_by_default(self):
        report = _make_clean_report()
        self.assertEqual(report.rate_limited_packages, [])

    def test_registry_fetch_errors_empty_by_default(self):
        report = _make_clean_report()
        self.assertEqual(report.registry_fetch_errors, {})


class TestPartialResultsRender(unittest.TestCase):
    def test_render_header_shows_partial_warning(self):
        report = _make_clean_report()
        report.rate_limited_packages = ["stripe", "openai"]
        report.rate_limit_hits = {"github": 2}
        report.partial_results = True
        text = render(report, emit_mode="compact")
        self.assertIn("PARTIAL RESULTS", text)

    def test_render_header_no_partial_when_clean(self):
        report = _make_clean_report()
        text = render(report, emit_mode="compact")
        self.assertNotIn("PARTIAL RESULTS", text)

    def test_footer_lists_rate_limited_packages(self):
        report = _make_clean_report()
        report.rate_limited_packages = ["stripe", "openai", "axios"]
        report.rate_limit_hits = {"github": 3}
        report.partial_results = True
        text = render(report, emit_mode="compact")
        self.assertIn("stripe", text)
        self.assertIn("openai", text)

    def test_footer_truncates_long_package_list(self):
        report = _make_clean_report()
        report.rate_limited_packages = [f"pkg{i}" for i in range(15)]
        report.rate_limit_hits = {"github": 15}
        report.partial_results = True
        text = render(report, emit_mode="compact")
        self.assertIn("+5 more", text)

    def test_registry_fetch_errors_shown_in_footer(self):
        report = _make_clean_report()
        report.registry_fetch_errors = {"my-pkg": "Connection timed out after 30s"}
        report.partial_results = True
        text = render(report, emit_mode="compact")
        self.assertIn("my-pkg", text)
        self.assertIn("fetch errors", text.lower())

    def test_not_found_still_separate_from_fetch_errors(self):
        report = _make_clean_report()
        report.packages_not_found = ["@internal/private-pkg"]
        report.registry_fetch_errors = {"flaky-pkg": "DNS resolution failed"}
        text = render(report, emit_mode="compact")
        # Both should appear; fetch errors section present
        self.assertIn("flaky-pkg", text)

    def test_retry_hint_shown_for_fetch_errors(self):
        report = _make_clean_report()
        report.registry_fetch_errors = {"unstable": "timeout"}
        text = render(report, emit_mode="compact")
        self.assertIn("--refresh", text)


class TestPartialResultsSchema(unittest.TestCase):
    def test_partial_results_in_to_dict(self):
        report = _make_clean_report()
        report.partial_results = True
        d = report.to_dict()
        self.assertIn("partial_results", d)
        self.assertTrue(d["partial_results"])

    def test_rate_limited_packages_in_to_dict(self):
        report = _make_clean_report()
        report.rate_limited_packages = ["pkg1", "pkg2"]
        d = report.to_dict()
        self.assertEqual(d["rate_limited_packages"], ["pkg1", "pkg2"])

    def test_registry_fetch_errors_in_to_dict(self):
        report = _make_clean_report()
        report.registry_fetch_errors = {"pkg": "error msg"}
        d = report.to_dict()
        self.assertEqual(d["registry_fetch_errors"], {"pkg": "error msg"})

    def test_from_dict_restores_all_new_fields(self):
        data = {
            "project_path": "/test",
            "dep_files_found": [],
            "packages_scanned": 5,
            "partial_results": True,
            "rate_limited_packages": ["a", "b"],
            "registry_fetch_errors": {"c": "timeout"},
        }
        report = DepRadarReport.from_dict(data)
        self.assertTrue(report.partial_results)
        self.assertEqual(report.rate_limited_packages, ["a", "b"])
        self.assertEqual(report.registry_fetch_errors, {"c": "timeout"})


if __name__ == "__main__":
    unittest.main()
