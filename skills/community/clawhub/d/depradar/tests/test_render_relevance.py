"""Tests for community signal display relevance filtering in render.py.

Covers:
- Fix 2 (changes3.txt): noisy titles like "Flutter Pre-Launch Checklist" must
  not appear as the example title in compact/markdown output.
- Fix 3: retry hint flag name corrected to --refresh.
- Enhancement 1: [AST] / [pattern] badge next to affected file lines.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "lib"))
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from schema import (
    DepRadarReport, BreakingChange, GithubIssueItem, HackerNewsItem,
    ImpactLocation, PackageUpdate, RedditItem, StackOverflowItem,
)
from render import render


# ── Helpers ───────────────────────────────────────────────────────────────────

def _breaking_pkg(name: str = "commander") -> PackageUpdate:
    return PackageUpdate(
        id="P1", package=name, ecosystem="npm",
        current_version="9.0.0", latest_version="10.0.0",
        semver_type="major", has_breaking_changes=True,
        breaking_changes=[BreakingChange(name, "removed", "test removal")],
    )


def _hn_item(title: str, package: str = "commander", points: int = 100, score: int = 80) -> HackerNewsItem:
    return HackerNewsItem(
        id="HN1", package=package, title=title,
        url="https://hn.com/item?id=1", hn_url="https://hn.com/item?id=1",
        points=points, score=score,
    )


def _gi_item(title: str, package: str = "commander", score: int = 80) -> GithubIssueItem:
    return GithubIssueItem(
        id="GI1", package=package, version="10", title=title, url="https://github.com/x",
        score=score,
    )


def _so_item(title: str, package: str = "commander", score: int = 80) -> StackOverflowItem:
    return StackOverflowItem(
        id="SO1", package=package, question_title=title,
        question_url="https://stackoverflow.com/q/1", score=score,
    )


def _reddit_item(title: str, package: str = "commander", score: int = 80) -> RedditItem:
    return RedditItem(
        id="R1", package=package, subreddit="javascript", title=title,
        url="https://reddit.com/r/1", score=score,
    )


def _compact(pkg, **kwargs) -> str:
    report = DepRadarReport(
        project_path="/test", dep_files_found=[],
        packages_with_breaking_changes=[pkg],
        **kwargs,
    )
    return render(report, emit_mode="compact")


# ── Fix 2: Community signal display relevance filter ─────────────────────────

class TestCommunitySignalDisplayFilter(unittest.TestCase):

    def test_flutter_checklist_not_shown_for_commander_hn(self):
        """'Flutter Pre-Launch Checklist' must NOT appear as example title."""
        pkg = _breaking_pkg("commander")
        noisy = _hn_item("Flutter Pre-Launch Checklist", package="commander", points=999, score=99)
        text = _compact(pkg, hackernews=[noisy])
        self.assertNotIn("Flutter Pre-Launch Checklist", text)

    def test_relevant_hn_title_is_shown(self):
        """An on-topic HN title IS shown as the example."""
        pkg = _breaking_pkg("commander")
        item = _hn_item("commander v10 breaking change", package="commander", score=80)
        text = _compact(pkg, hackernews=[item])
        self.assertIn("commander v10 breaking change", text)

    def test_signal_count_shows_total_not_filtered(self):
        """Total count shows ALL signals, even if example title is filtered."""
        pkg = _breaking_pkg("commander")
        noisy1 = _gi_item("Flutter Pre-Launch Checklist", package="commander", score=90)
        noisy2 = _gi_item("Android weekly roundup", package="commander", score=85)
        on_topic = _gi_item("commander breaking API change", package="commander", score=50)
        text = _compact(pkg, github_issues=[noisy1, noisy2, on_topic])
        # 3 issues total must be mentioned
        self.assertIn("3 GitHub issue(s)", text)

    def test_count_shown_even_when_all_noisy(self):
        """If all signals are noisy, count is shown but no example title."""
        pkg = _breaking_pkg("commander")
        noisy1 = _hn_item("Flutter checklist weekly", package="commander", points=500, score=95)
        noisy2 = _hn_item("YouTube tutorial roundup", package="commander", points=100, score=40)
        text = _compact(pkg, hackernews=[noisy1, noisy2])
        # Count of items still shown (no silent omission)
        self.assertIn("2 HN item(s)", text)
        # But neither noisy title appears
        self.assertNotIn("Flutter checklist weekly", text)
        self.assertNotIn("YouTube tutorial roundup", text)

    def test_so_question_title_filtered(self):
        """Noisy SO question title is filtered out."""
        pkg = _breaking_pkg("commander")
        noisy = _so_item("Android tutorial for beginners", package="commander", score=90)
        on_topic = _so_item("commander deprecated option throws error", package="commander", score=50)
        text = _compact(pkg, stackoverflow=[noisy, on_topic])
        self.assertNotIn("Android tutorial for beginners", text)
        self.assertIn("commander deprecated option throws error", text)

    def test_reddit_title_filtered(self):
        """Noisy Reddit title is filtered out."""
        pkg = _breaking_pkg("commander")
        noisy = _reddit_item("iOS weekly newsletter", package="commander", score=90)
        on_topic = _reddit_item("commander v10 removed callback API", package="commander", score=50)
        text = _compact(pkg, reddit=[noisy, on_topic])
        self.assertNotIn("iOS weekly newsletter", text)

    def test_github_title_filtered(self):
        """Noisy GitHub issue title is filtered out in compact mode."""
        pkg = _breaking_pkg("commander")
        noisy = _gi_item("YouTube video tutorial", package="commander", score=90)
        on_topic = _gi_item("commander API removed in v10", package="commander", score=30)
        text = _compact(pkg, github_issues=[noisy, on_topic])
        self.assertNotIn("YouTube video tutorial", text)
        self.assertIn("commander API removed in v10", text)

    def test_markdown_mode_filters_noisy_hn(self):
        """Noisy HN title is also filtered in markdown mode."""
        pkg = _breaking_pkg("commander")
        noisy = _hn_item("Flutter Pre-Launch Checklist", package="commander", points=999, score=99)
        on_topic = _hn_item("commander breaking change migration", package="commander", points=10, score=20)
        report = DepRadarReport(
            project_path="/test", dep_files_found=[],
            packages_with_breaking_changes=[pkg],
            hackernews=[noisy, on_topic],
        )
        text = render(report, emit_mode="md")
        self.assertNotIn("Flutter Pre-Launch Checklist", text)


# ── Fix 3: Retry hint uses --refresh (correct flag name) ─────────────────────

class TestRetryHintFlagName(unittest.TestCase):

    def _report_with_fetch_errors(self, n: int = 2) -> DepRadarReport:
        errors = {f"pkg-{i}": f"timeout after 10s" for i in range(n)}
        return DepRadarReport(
            project_path="/test", dep_files_found=[],
            registry_fetch_errors=errors,
        )

    def test_retry_hint_uses_refresh_flag(self):
        """Retry hint must say --refresh, not --no-cache."""
        report = self._report_with_fetch_errors(2)
        text = render(report, emit_mode="compact")
        self.assertIn("--refresh", text)
        self.assertNotIn("--no-cache", text)

    def test_retry_hint_appears_exactly_once(self):
        """Retry hint appears once even when multiple packages had fetch errors."""
        report = self._report_with_fetch_errors(3)
        text = render(report, emit_mode="compact")
        self.assertEqual(text.count("--refresh"), 1)

    def test_retry_hint_not_shown_when_no_errors(self):
        """No retry hint when registry_fetch_errors is empty."""
        report = DepRadarReport(project_path="/test", dep_files_found=[])
        text = render(report, emit_mode="compact")
        self.assertNotIn("--refresh", text)


# ── Enhancement 1: [AST] / [pattern] confidence badge ────────────────────────

class TestImpactConfidenceBadge(unittest.TestCase):

    def _report_with_impact(self, detection_method: str) -> str:
        pkg = PackageUpdate(
            id="P1", package="stripe", ecosystem="npm",
            current_version="7.0.0", latest_version="8.0.0",
            semver_type="major", has_breaking_changes=True,
            breaking_changes=[BreakingChange("sym", "removed", "desc")],
            impact_locations=[
                ImpactLocation(
                    file_path="src/billing.ts",
                    line_number=42,
                    usage_text="import { createPaymentIntent } from 'stripe'",
                    detection_method=detection_method,
                )
            ],
            impact_confidence="high",
        )
        report = DepRadarReport(
            project_path="/test", dep_files_found=[],
            packages_with_breaking_changes=[pkg],
        )
        return render(report, emit_mode="compact")

    def test_ast_detection_shows_ast_badge(self):
        text = self._report_with_impact("ast")
        self.assertIn("[AST]", text)

    def test_grep_detection_shows_pattern_badge(self):
        text = self._report_with_impact("grep")
        self.assertIn("[pattern]", text)

    def test_ast_badge_on_same_line_as_file(self):
        text = self._report_with_impact("ast")
        for line in text.splitlines():
            if "src/billing.ts" in line:
                self.assertIn("[AST]", line)
                break
        else:
            self.fail("Impact file line not found in output")

    def test_pattern_badge_on_same_line_as_file(self):
        text = self._report_with_impact("grep")
        for line in text.splitlines():
            if "src/billing.ts" in line:
                self.assertIn("[pattern]", line)
                break
        else:
            self.fail("Impact file line not found in output")


if __name__ == "__main__":
    unittest.main()
