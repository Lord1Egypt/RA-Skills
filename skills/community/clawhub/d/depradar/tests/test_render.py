"""Tests for scripts/lib/render.py"""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "lib"))

from dates import days_ago, today_utc
from render import (
    _has_security,
    render,
    render_compact,
    render_context,
    render_json,
    render_markdown,
)
from schema import (
    DepRadarReport,
    BreakingChange,
    GithubIssueItem,
    HackerNewsItem,
    ImpactLocation,
    PackageUpdate,
    RedditItem,
    StackOverflowItem,
    SubScores,
    TwitterItem,
)


def _make_breaking_pkg(
    pkg_id="P1",
    package="stripe",
    current="7.0.0",
    latest="8.0.0",
    score=88,
    breaking_changes=None,
    impact_locations=None,
):
    bcs = breaking_changes or [
        BreakingChange(
            symbol="constructEvent",
            change_type="removed",
            description="`stripe.webhooks.constructEvent()` was removed. Use `verify()` instead.",
            migration_note="Use `stripe.webhooks.verify()` instead.",
        )
    ]
    locs = impact_locations or [
        ImpactLocation(
            file_path="src/payments/webhook.ts",
            line_number=47,
            usage_text="const event = stripe.webhooks.constructEvent(payload, sig, secret);",
        )
    ]
    return PackageUpdate(
        id=pkg_id,
        package=package,
        ecosystem="npm",
        current_version=current,
        latest_version=latest,
        semver_type="major",
        has_breaking_changes=True,
        breaking_changes=bcs,
        changelog_url=f"https://github.com/stripe/stripe-node/releases/tag/v{latest}",
        release_date=today_utc(),
        release_notes_snippet="Major release with breaking webhook changes.",
        impact_locations=locs,
        impact_confidence="high",
        github_repo="stripe/stripe-node",
        subs=SubScores(severity=100, recency=100, impact=100, community=50),
        score=score,
    )


def _make_minor_pkg(
    pkg_id="P2",
    package="axios",
    current="1.3.0",
    latest="1.5.0",
    score=25,
):
    return PackageUpdate(
        id=pkg_id,
        package=package,
        ecosystem="npm",
        current_version=current,
        latest_version=latest,
        semver_type="minor",
        has_breaking_changes=False,
        score=score,
        release_date=days_ago(10),
    )


def _make_full_report():
    breaking_pkg = _make_breaking_pkg()
    openai_pkg = _make_breaking_pkg(
        pkg_id="P2",
        package="openai",
        current="0.28.0",
        latest="1.0.0",
        score=75,
        breaking_changes=[
            BreakingChange(
                symbol="Completion.create",
                change_type="removed",
                description="`openai.Completion.create()` removed. Use `client.completions.create()`.",
            ),
            BreakingChange(
                symbol="ChatCompletion.create",
                change_type="removed",
                description="`openai.ChatCompletion.create()` removed.",
            ),
        ],
        impact_locations=[],
    )
    minor_axios = _make_minor_pkg("P3", "axios", "1.3.0", "1.5.0")
    minor_express = _make_minor_pkg("P4", "express", "4.18.0", "4.19.0")
    minor_dotenv = _make_minor_pkg("P5", "dotenv", "16.0.0", "16.3.0")
    gh_issue = GithubIssueItem(
        id="GI1",
        package="stripe",
        version="8.0.0",
        title="Breaking change: constructEvent removed in v8",
        url="https://github.com/stripe/stripe-node/issues/1842",
        comments=23,
        labels=["breaking-change"],
        state="open",
        created_at=today_utc(),
        score=74,
    )
    return DepRadarReport(
        project_path="/home/user/my-saas-project",
        dep_files_found=["package.json"],
        packages_scanned=8,
        packages_with_breaking_changes=[breaking_pkg, openai_pkg],
        packages_with_minor_updates=[minor_axios, minor_express, minor_dotenv],
        packages_current=["lodash", "cors", "helmet"],
        packages_not_found=["private-internal-pkg"],
        github_issues=[gh_issue],
        depth="default",
        days_window=30,
        generated_at="2026-03-27T12:00:00Z",
    )


class TestRenderCompact(unittest.TestCase):

    def setUp(self):
        self.report = _make_full_report()
        self.output = render_compact(self.report)

    def test_contains_package_name(self):
        self.assertIn("stripe", self.output)

    def test_contains_version_transition(self):
        self.assertIn("7.0.0", self.output)
        self.assertIn("8.0.0", self.output)

    def test_contains_breaking_changes_section(self):
        self.assertIn("BREAKING", self.output.upper())

    def test_contains_minor_updates_section(self):
        self.assertIn("axios", self.output)

    def test_contains_current_packages(self):
        self.assertIn("current", self.output.lower())

    def test_contains_packages_scanned(self):
        self.assertIn("8", self.output)

    def test_2_breaking_present(self):
        # Should mention both stripe and openai
        self.assertIn("openai", self.output)

    def test_3_minor_updates_present(self):
        self.assertIn("express", self.output)

    def test_empty_report_shows_up_to_date(self):
        empty = DepRadarReport(
            project_path="/tmp/proj",
            dep_files_found=["package.json"],
            packages_scanned=5,
            packages_current=["stripe", "lodash", "axios", "express", "dotenv"],
        )
        output = render_compact(empty)
        self.assertIn("up to date", output.lower())


class TestRenderJson(unittest.TestCase):

    def setUp(self):
        self.report = _make_full_report()
        self.output = render_json(self.report)

    def test_is_valid_json(self):
        parsed = json.loads(self.output)
        self.assertIsInstance(parsed, dict)

    def test_contains_packages_scanned(self):
        parsed = json.loads(self.output)
        self.assertEqual(parsed["packages_scanned"], 8)

    def test_contains_required_keys(self):
        parsed = json.loads(self.output)
        required = [
            "project_path", "packages_scanned",
            "packages_with_breaking_changes", "packages_with_minor_updates",
            "packages_current", "packages_not_found",
            "github_issues", "stackoverflow", "reddit", "hackernews", "twitter",
            "depth", "days_window", "generated_at",
        ]
        for key in required:
            self.assertIn(key, parsed, f"Missing key: {key}")

    def test_breaking_changes_in_output(self):
        parsed = json.loads(self.output)
        breaking = parsed["packages_with_breaking_changes"]
        self.assertEqual(len(breaking), 2)
        packages = [p["package"] for p in breaking]
        self.assertIn("stripe", packages)
        self.assertIn("openai", packages)

    def test_github_issues_in_output(self):
        parsed = json.loads(self.output)
        self.assertEqual(len(parsed["github_issues"]), 1)


class TestRenderMarkdown(unittest.TestCase):

    def setUp(self):
        self.report = _make_full_report()
        self.output = render_markdown(self.report)

    def test_contains_breaking_changes_header(self):
        self.assertIn("## ⚠️ Breaking Changes", self.output)

    def test_contains_package_headers(self):
        self.assertIn("stripe", self.output)
        self.assertIn("openai", self.output)

    def test_contains_minor_updates_table(self):
        self.assertIn("## 🟡 Minor Updates", self.output)
        self.assertIn("axios", self.output)

    def test_contains_up_to_date_section(self):
        self.assertIn("Up to Date", self.output)
        self.assertIn("lodash", self.output)

    def test_changelog_link_present(self):
        self.assertIn("Release notes", self.output)
        self.assertIn("https://github.com", self.output)

    def test_breaking_change_symbol_in_output(self):
        self.assertIn("constructEvent", self.output)

    def test_migration_note_present(self):
        self.assertIn("verify", self.output)

    def test_impact_locations_present(self):
        self.assertIn("webhook.ts", self.output)

    def test_markdown_table_format(self):
        self.assertIn("|", self.output)


class TestRenderContext(unittest.TestCase):

    def setUp(self):
        self.report = _make_full_report()
        self.output = render_context(self.report)

    def test_short_summary(self):
        # Context output should be shorter than full markdown
        md_output = render_markdown(self.report)
        self.assertLess(len(self.output), len(md_output))

    def test_mentions_breaking_count(self):
        self.assertTrue(
            "2" in self.output or "breaking" in self.output.lower(),
            f"Expected count/breaking in context; got: {self.output[:200]}"
        )

    def test_mentions_package_names(self):
        self.assertIn("stripe", self.output)

    def test_no_breaking_changes_returns_one_liner(self):
        empty = DepRadarReport(
            project_path="/tmp/proj",
            dep_files_found=[],
            days_window=30,
        )
        output = render_context(empty)
        self.assertIn("No breaking", output)

    def test_context_mentions_change_type(self):
        # Should mention the symbol/change type
        self.assertTrue(
            "constructEvent" in self.output
            or "removed" in self.output
            or "stripe" in self.output
        )


class TestRenderDispatcher(unittest.TestCase):

    def setUp(self):
        self.report = _make_full_report()

    def test_compact_mode(self):
        result = render(self.report, emit_mode="compact")
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_json_mode(self):
        result = render(self.report, emit_mode="json")
        parsed = json.loads(result)
        self.assertIsInstance(parsed, dict)

    def test_md_mode(self):
        result = render(self.report, emit_mode="md")
        self.assertIn("## ⚠️ Breaking Changes", result)

    def test_context_mode(self):
        result = render(self.report, emit_mode="context")
        self.assertIn("stripe", result)

    def test_unknown_mode_defaults_to_compact(self):
        result = render(self.report, emit_mode="unknown_mode")
        compact_result = render_compact(self.report)
        self.assertEqual(result, compact_result)

    def test_default_mode_is_compact(self):
        result = render(self.report)
        compact_result = render_compact(self.report)
        self.assertEqual(result, compact_result)


class TestHasSecurity(unittest.TestCase):

    def test_cve_keyword(self):
        pkg = PackageUpdate(
            id="P1", package="pkg", ecosystem="npm",
            current_version="1.0.0", latest_version="2.0.0",
            semver_type="major",
            release_notes_snippet="Patches CVE-2026-12345 remote code execution.",
        )
        self.assertTrue(_has_security(pkg))

    def test_security_keyword(self):
        pkg = PackageUpdate(
            id="P1", package="pkg", ecosystem="npm",
            current_version="1.0.0", latest_version="2.0.0",
            semver_type="minor",
            release_notes_snippet="Includes security fix for HTTP header injection.",
        )
        self.assertTrue(_has_security(pkg))

    def test_vulnerability_keyword(self):
        pkg = PackageUpdate(
            id="P1", package="pkg", ecosystem="npm",
            current_version="1.0.0", latest_version="2.0.0",
            semver_type="patch",
            release_notes_snippet="Fixed vulnerability in dependency parsing.",
        )
        self.assertTrue(_has_security(pkg))

    def test_vuln_keyword(self):
        pkg = PackageUpdate(
            id="P1", package="pkg", ecosystem="npm",
            current_version="1.0.0", latest_version="2.0.0",
            semver_type="patch",
            release_notes_snippet="Resolves a vuln reported by the security team.",
        )
        self.assertTrue(_has_security(pkg))

    def test_no_security_keywords(self):
        pkg = PackageUpdate(
            id="P1", package="pkg", ecosystem="npm",
            current_version="1.0.0", latest_version="2.0.0",
            semver_type="minor",
            release_notes_snippet="Performance improvements and bug fixes.",
        )
        self.assertFalse(_has_security(pkg))

    def test_none_snippet(self):
        pkg = PackageUpdate(
            id="P1", package="pkg", ecosystem="npm",
            current_version="1.0.0", latest_version="2.0.0",
            semver_type="minor",
            release_notes_snippet=None,
        )
        self.assertFalse(_has_security(pkg))


if __name__ == "__main__":
    unittest.main()
