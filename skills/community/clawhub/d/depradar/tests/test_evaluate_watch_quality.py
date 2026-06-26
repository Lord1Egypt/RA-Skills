"""
Integration-quality evaluation tests for /depradar.

Verifies the full pipeline produces sensible, actionable output
by running end-to-end with mock data and asserting quality invariants.
"""
import json
import os
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from lib.schema import (
    DepRadarReport, PackageUpdate, BreakingChange,
    GithubIssueItem, StackOverflowItem,
)


def make_breaking_change(symbol: str, change_type: str = "removed") -> BreakingChange:
    return BreakingChange(
        symbol=symbol,
        change_type=change_type,
        description=f"{symbol} was {change_type}",
        old_signature=None,
        new_signature=None,
        migration_note=f"Use new_{symbol} instead",
        source="changelog",
        confidence="high",
    )


def make_package_update(
    pkg_id: str,
    name: str,
    current: str,
    latest: str,
    bump: str,
    symbols: list,
    score: int = 0,
) -> PackageUpdate:
    return PackageUpdate(
        id=pkg_id,
        package=name,
        ecosystem="npm",
        current_version=current,
        latest_version=latest,
        semver_type=bump,
        has_breaking_changes=len(symbols) > 0,
        breaking_changes=[make_breaking_change(s) for s in symbols],
        impact_locations=[],
        impact_confidence="not_scanned",
        github_repo=f"org/{name}",
        score=score,
    )


def make_sample_report() -> DepRadarReport:
    breaking = [
        make_package_update("P1", "stripe", "7.0.0", "8.0.0", "major", ["constructEvent"], 87),
        make_package_update("P2", "openai", "0.28.0", "1.35.0", "major", ["Completion"], 79),
    ]
    return DepRadarReport(
        project_path="/test/project",
        dep_files_found=["package.json"],
        packages_scanned=15,
        packages_with_breaking_changes=breaking,
        packages_with_minor_updates=[
            make_package_update("P3", "axios", "1.5.0", "1.7.0", "minor", [], 22)
        ],
        packages_current=["lodash", "dayjs", "uuid"],
        packages_not_found=["@internal/lib"],
        github_issues=[
            GithubIssueItem(
                id="GI1", package="stripe", version="8.0.0",
                title="stripe v8 migration issue",
                url="https://github.com/stripe/stripe-node/issues/1234",
                body_snippet="constructEvent removed in v8",
                comments=12, labels=["breaking-change"], state="closed",
                resolution_snippet=None, created_at="2026-01-10T10:00:00Z",
                subs=None, score=65, cross_refs=[],
            )
        ],
        stackoverflow=[
            StackOverflowItem(
                id="SO1", package="stripe",
                question_title="How to migrate stripe v8?",
                question_url="https://stackoverflow.com/questions/9876",
                answer_count=3, is_answered=True,
                accepted_answer_snippet=None,
                tags=["stripe", "python"],
                view_count=1500, so_score=23,
                created_at="2026-01-12T00:00:00Z",
                subs=None, score=58, cross_refs=[],
            )
        ],
        reddit=[], hackernews=[], twitter=[],
        from_cache=False, cache_age_hours=None,
        depth="default", days_window=30,
    )


class TestReportSchemaIntegrity(unittest.TestCase):
    def test_roundtrip_serialization(self):
        report = make_sample_report()
        d = report.to_dict()
        restored = DepRadarReport.from_dict(d)

        self.assertEqual(restored.project_path, report.project_path)
        self.assertEqual(restored.packages_scanned, report.packages_scanned)
        self.assertEqual(
            len(restored.packages_with_breaking_changes),
            len(report.packages_with_breaking_changes)
        )
        self.assertEqual(restored.depth, report.depth)
        self.assertEqual(restored.days_window, report.days_window)

    def test_json_serializable(self):
        report = make_sample_report()
        d = report.to_dict()
        serialized = json.dumps(d)
        parsed = json.loads(serialized)
        self.assertIsInstance(parsed, dict)
        self.assertIn("packages_with_breaking_changes", parsed)

    def test_breaking_packages_sorted_after_score_all(self):
        from lib.score import score_all
        report = make_sample_report()
        score_all(report)
        scores = [p.score for p in report.packages_with_breaking_changes]
        self.assertEqual(scores, sorted(scores, reverse=True))


class TestScoringInvariants(unittest.TestCase):
    """Score properties that must always hold."""

    def test_removed_scores_higher_than_deprecated(self):
        from lib.score import score_package_update

        removed_pkg = make_package_update("P1", "foo", "1.0.0", "2.0.0", "major", ["fn"])
        removed_pkg.breaking_changes[0].change_type = "removed"
        removed_pkg.has_breaking_changes = True
        removed_pkg.release_date = "2026-03-01"

        deprecated_pkg = make_package_update("P2", "bar", "1.0.0", "2.0.0", "major", ["fn"])
        deprecated_pkg.breaking_changes[0].change_type = "deprecated"
        deprecated_pkg.has_breaking_changes = True
        deprecated_pkg.release_date = "2026-03-01"

        score_package_update(removed_pkg)
        score_package_update(deprecated_pkg)

        self.assertGreater(removed_pkg.score, deprecated_pkg.score)

    def test_score_bounded_0_to_100(self):
        from lib.score import score_package_update

        for change_type in ["removed", "deprecated", "renamed"]:
            pkg = make_package_update("P1", "foo", "1.0.0", "2.0.0", "major", ["fn"])
            pkg.breaking_changes[0].change_type = change_type
            pkg.release_date = "2026-03-01"
            score_package_update(pkg)
            self.assertGreaterEqual(pkg.score, 0)
            self.assertLessEqual(pkg.score, 100)

    def test_recent_release_higher_score(self):
        from lib.score import score_package_update

        recent_pkg = make_package_update("P1", "foo", "1.0.0", "2.0.0", "major", ["fn"])
        recent_pkg.release_date = "2026-03-20"  # recent

        old_pkg = make_package_update("P2", "foo", "1.0.0", "2.0.0", "major", ["fn"])
        old_pkg.release_date = "2025-06-01"  # old (staleness bonus 12 < recency gap of 21)

        score_package_update(recent_pkg)
        score_package_update(old_pkg)

        self.assertGreater(recent_pkg.score, old_pkg.score)

    def test_package_with_no_breaking_changes_lower_score(self):
        from lib.score import score_package_update

        with_bc = make_package_update("P1", "foo", "1.0.0", "2.0.0", "major", ["fn"])
        with_bc.release_date = "2026-03-01"

        without_bc = make_package_update("P2", "bar", "1.0.0", "1.1.0", "minor", [])
        without_bc.has_breaking_changes = False
        without_bc.release_date = "2026-03-01"

        score_package_update(with_bc)
        score_package_update(without_bc)

        self.assertGreater(with_bc.score, without_bc.score)


class TestRenderCompleteness(unittest.TestCase):
    """render() must return strings containing all critical information."""

    def _make_report(self) -> DepRadarReport:
        return DepRadarReport(
            project_path="/test",
            dep_files_found=["package.json"],
            packages_scanned=5,
            packages_with_breaking_changes=[
                make_package_update("P1", "stripe", "7.0.0", "8.0.0", "major",
                                    ["constructEvent", "Webhook"], 87)
            ],
            packages_with_minor_updates=[],
            packages_current=["lodash"],
        )

    def test_compact_contains_package_name(self):
        from lib.render import render
        report = self._make_report()
        text = render(report, emit_mode="compact")
        self.assertIn("stripe", text)

    def test_compact_contains_version_info(self):
        from lib.render import render
        report = self._make_report()
        text = render(report, emit_mode="compact")
        self.assertTrue("7.0.0" in text or "8.0.0" in text or "major" in text.lower())

    def test_json_is_valid(self):
        from lib.render import render
        report = self._make_report()
        text = render(report, emit_mode="json")
        parsed = json.loads(text)
        self.assertIn("packages_with_breaking_changes", parsed)

    def test_markdown_has_headers(self):
        from lib.render import render
        report = self._make_report()
        text = render(report, emit_mode="md")
        self.assertIn("#", text)

    def test_context_is_concise(self):
        from lib.render import render
        report = self._make_report()
        text = render(report, emit_mode="context")
        self.assertLess(len(text), 2000)
        self.assertIn("stripe", text)

    def test_render_returns_string(self):
        from lib.render import render
        report = self._make_report()
        for mode in ("compact", "json", "md", "context"):
            result = render(report, emit_mode=mode)
            self.assertIsInstance(result, str, f"render mode={mode} should return str")


class TestDepParserCompleteness(unittest.TestCase):
    def test_parses_all_fixture_formats(self):
        import shutil
        from lib.dep_parser import parse_all
        fixtures = Path(__file__).parent.parent / "fixtures" / "package_json_samples"

        # parse_all dispatches by basename — copy fixtures to temp files
        # with the canonical names that dep_parser recognises.
        node_fixture = fixtures / "node_sample.json"
        if node_fixture.exists():
            with tempfile.TemporaryDirectory() as tmp:
                pkg_json = os.path.join(tmp, "package.json")
                shutil.copy(str(node_fixture), pkg_json)
                deps, _ = parse_all([pkg_json])
                self.assertIsInstance(deps, dict)
                self.assertGreater(len(deps), 0)
                for name, dep in deps.items():
                    self.assertIsNotNone(dep.name)
                    self.assertIsNotNone(dep.ecosystem)

        req_fixture = fixtures / "python_requirements.txt"
        if req_fixture.exists():
            with tempfile.TemporaryDirectory() as tmp:
                req_file = os.path.join(tmp, "requirements.txt")
                shutil.copy(str(req_fixture), req_file)
                deps, _ = parse_all([req_file])
                self.assertIsInstance(deps, dict)
                self.assertGreater(len(deps), 0)

    def test_no_crash_on_empty_file(self):
        from lib.dep_parser import parse_all
        with tempfile.NamedTemporaryFile(suffix=".txt", mode="w", delete=False) as f:
            f.write("")
            fname = f.name
        try:
            deps, errors = parse_all([fname])
            # Returns (dict, errors) — should not crash
            self.assertIsInstance(deps, dict)
            self.assertIsInstance(errors, list)
        finally:
            os.unlink(fname)


class TestCacheRoundtrip(unittest.TestCase):
    def test_report_survives_cache_roundtrip(self):
        from lib import cache as cache_mod
        report = DepRadarReport(
            project_path="/test",
            dep_files_found=["package.json"],
            packages_scanned=3,
            packages_current=["foo", "bar"],
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            # cache uses APIWATCH_CACHE_DIR env var to override location
            with unittest.mock.patch.dict(os.environ, {"APIWATCH_CACHE_DIR": tmpdir}):
                key = "test_report_roundtrip_unique_eval"
                cache_mod.save(key, report.to_dict(), namespace="reports")
                loaded = cache_mod.load(key, ttl_hours=1, namespace="reports")
                self.assertIsNotNone(loaded)
                restored = DepRadarReport.from_dict(loaded)
                self.assertEqual(restored.project_path, report.project_path)
                self.assertEqual(restored.packages_scanned, report.packages_scanned)


if __name__ == "__main__":
    unittest.main()
