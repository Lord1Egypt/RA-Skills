"""Tests for schema.py dataclass to_dict() / from_dict() roundtrips."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "lib"))

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


class TestBreakingChangeRoundtrip(unittest.TestCase):

    def _make(self, **kwargs):
        defaults = dict(
            symbol="stripe.webhooks.constructEvent",
            change_type="removed",
            description="`constructEvent` was removed; use `verify()` instead.",
            old_signature="constructEvent(payload, sig, secret): Event",
            new_signature=None,
            migration_note="Use `stripe.webhooks.verify()` instead.",
            source="release_notes",
            confidence="high",
        )
        defaults.update(kwargs)
        return BreakingChange(**defaults)

    def test_full_roundtrip(self):
        bc = self._make()
        d = bc.to_dict()
        bc2 = BreakingChange.from_dict(d)
        self.assertEqual(bc2.symbol, bc.symbol)
        self.assertEqual(bc2.change_type, bc.change_type)
        self.assertEqual(bc2.description, bc.description)
        self.assertEqual(bc2.old_signature, bc.old_signature)
        self.assertIsNone(bc2.new_signature)
        self.assertEqual(bc2.migration_note, bc.migration_note)
        self.assertEqual(bc2.source, bc.source)
        self.assertEqual(bc2.confidence, bc.confidence)

    def test_minimal_roundtrip(self):
        bc = BreakingChange(
            symbol="foo",
            change_type="other",
            description="some desc",
        )
        d = bc.to_dict()
        bc2 = BreakingChange.from_dict(d)
        self.assertEqual(bc2.symbol, "foo")
        self.assertEqual(bc2.change_type, "other")
        self.assertEqual(bc2.description, "some desc")
        self.assertIsNone(bc2.old_signature)
        self.assertIsNone(bc2.new_signature)
        self.assertIsNone(bc2.migration_note)
        self.assertEqual(bc2.source, "release_notes")
        self.assertEqual(bc2.confidence, "med")

    def test_to_dict_has_all_keys(self):
        bc = self._make()
        d = bc.to_dict()
        for key in ("symbol", "change_type", "description", "old_signature",
                    "new_signature", "migration_note", "source", "confidence"):
            self.assertIn(key, d)


class TestImpactLocationRoundtrip(unittest.TestCase):

    def test_full_roundtrip(self):
        loc = ImpactLocation(
            file_path="src/payments/webhook.ts",
            line_number=47,
            usage_text="const event = stripe.webhooks.constructEvent(payload, sig, secret);",
            detection_method="ast",
        )
        d = loc.to_dict()
        loc2 = ImpactLocation.from_dict(d)
        self.assertEqual(loc2.file_path, loc.file_path)
        self.assertEqual(loc2.line_number, loc.line_number)
        self.assertEqual(loc2.usage_text, loc.usage_text)
        self.assertEqual(loc2.detection_method, loc.detection_method)

    def test_default_detection_method(self):
        d = {
            "file_path": "app.py",
            "line_number": 10,
            "usage_text": "import openai",
        }
        loc = ImpactLocation.from_dict(d)
        self.assertEqual(loc.detection_method, "grep")


class TestPackageUpdateRoundtrip(unittest.TestCase):

    def _make_breaking_change(self):
        return BreakingChange(
            symbol="constructEvent",
            change_type="removed",
            description="Method removed in v8",
        )

    def _make_impact_location(self):
        return ImpactLocation(
            file_path="src/webhook.ts",
            line_number=42,
            usage_text="stripe.webhooks.constructEvent(...)",
        )

    def _make_sub_scores(self):
        return SubScores(severity=100, recency=85, impact=70, community=50)

    def test_full_roundtrip(self):
        pkg = PackageUpdate(
            id="P1",
            package="stripe",
            ecosystem="npm",
            current_version="7.0.0",
            latest_version="8.0.0",
            semver_type="major",
            has_breaking_changes=True,
            breaking_changes=[self._make_breaking_change()],
            changelog_url="https://github.com/stripe/stripe-node/releases/tag/v8.0.0",
            release_date="2026-01-10",
            release_notes_snippet="Major release with breaking webhook changes.",
            impact_locations=[self._make_impact_location()],
            impact_confidence="high",
            github_repo="stripe/stripe-node",
            subs=self._make_sub_scores(),
            score=88,
            cross_refs=["GI1", "SO1"],
        )
        d = pkg.to_dict()
        pkg2 = PackageUpdate.from_dict(d)

        self.assertEqual(pkg2.id, "P1")
        self.assertEqual(pkg2.package, "stripe")
        self.assertEqual(pkg2.ecosystem, "npm")
        self.assertEqual(pkg2.current_version, "7.0.0")
        self.assertEqual(pkg2.latest_version, "8.0.0")
        self.assertEqual(pkg2.semver_type, "major")
        self.assertTrue(pkg2.has_breaking_changes)
        self.assertEqual(len(pkg2.breaking_changes), 1)
        self.assertEqual(pkg2.breaking_changes[0].symbol, "constructEvent")
        self.assertEqual(pkg2.changelog_url, "https://github.com/stripe/stripe-node/releases/tag/v8.0.0")
        self.assertEqual(pkg2.release_date, "2026-01-10")
        self.assertEqual(len(pkg2.impact_locations), 1)
        self.assertEqual(pkg2.impact_locations[0].file_path, "src/webhook.ts")
        self.assertEqual(pkg2.impact_confidence, "high")
        self.assertEqual(pkg2.github_repo, "stripe/stripe-node")
        self.assertIsNotNone(pkg2.subs)
        self.assertEqual(pkg2.subs.severity, 100)
        self.assertEqual(pkg2.subs.recency, 85)
        self.assertEqual(pkg2.score, 88)
        self.assertEqual(pkg2.cross_refs, ["GI1", "SO1"])

    def test_minimal_roundtrip(self):
        pkg = PackageUpdate(
            id="P2",
            package="lodash",
            ecosystem="npm",
            current_version="4.0.0",
            latest_version="4.1.0",
            semver_type="minor",
        )
        d = pkg.to_dict()
        pkg2 = PackageUpdate.from_dict(d)
        self.assertFalse(pkg2.has_breaking_changes)
        self.assertEqual(pkg2.breaking_changes, [])
        self.assertIsNone(pkg2.subs)
        self.assertEqual(pkg2.score, 0)
        self.assertEqual(pkg2.cross_refs, [])

    def test_nested_breaking_changes_count(self):
        bcs = [
            BreakingChange("sym1", "removed", "desc1"),
            BreakingChange("sym2", "renamed", "desc2"),
        ]
        pkg = PackageUpdate(
            id="P3", package="openai", ecosystem="pypi",
            current_version="0.28.0", latest_version="1.0.0",
            semver_type="major", has_breaking_changes=True,
            breaking_changes=bcs,
        )
        d = pkg.to_dict()
        pkg2 = PackageUpdate.from_dict(d)
        self.assertEqual(len(pkg2.breaking_changes), 2)
        self.assertEqual(pkg2.breaking_changes[0].symbol, "sym1")
        self.assertEqual(pkg2.breaking_changes[1].symbol, "sym2")


class TestGithubIssueItemRoundtrip(unittest.TestCase):

    def test_full_roundtrip(self):
        item = GithubIssueItem(
            id="GI1",
            package="stripe",
            version="8.0.0",
            title="Breaking change: constructEvent removed",
            url="https://github.com/stripe/stripe-node/issues/1842",
            body_snippet="After upgrading, constructEvent is gone.",
            comments=23,
            labels=["breaking-change"],
            state="open",
            resolution_snippet=None,
            created_at="2026-01-11T08:15:00Z",
            subs=SubScores(severity=80, recency=100, impact=69, community=50),
            score=74,
            cross_refs=["P1"],
        )
        d = item.to_dict()
        item2 = GithubIssueItem.from_dict(d)
        self.assertEqual(item2.id, "GI1")
        self.assertEqual(item2.package, "stripe")
        self.assertEqual(item2.comments, 23)
        self.assertEqual(item2.labels, ["breaking-change"])
        self.assertEqual(item2.state, "open")
        self.assertIsNotNone(item2.subs)
        self.assertEqual(item2.subs.severity, 80)
        self.assertEqual(item2.score, 74)

    def test_defaults_on_from_dict(self):
        d = {"id": "GI2", "package": "foo", "title": "Issue", "url": "http://x.com"}
        item = GithubIssueItem.from_dict(d)
        self.assertEqual(item.comments, 0)
        self.assertEqual(item.labels, [])
        self.assertEqual(item.state, "open")
        self.assertEqual(item.score, 0)


class TestStackOverflowItemRoundtrip(unittest.TestCase):

    def test_full_roundtrip(self):
        item = StackOverflowItem(
            id="SO1",
            package="stripe",
            question_title="stripe webhooks constructEvent not a function after upgrade",
            question_url="https://stackoverflow.com/questions/78800042",
            answer_count=4,
            is_answered=True,
            accepted_answer_snippet="Use stripe.webhooks.verify() instead.",
            tags=["stripe", "node.js", "webhooks"],
            view_count=3200,
            so_score=28,
            created_at="2026-01-11T08:00:00Z",
            subs=SubScores(severity=40, recency=100, impact=52, community=55),
            score=52,
            cross_refs=["P1"],
        )
        d = item.to_dict()
        item2 = StackOverflowItem.from_dict(d)
        self.assertEqual(item2.id, "SO1")
        self.assertEqual(item2.question_title, item.question_title)
        self.assertTrue(item2.is_answered)
        self.assertEqual(item2.view_count, 3200)
        self.assertEqual(item2.so_score, 28)
        self.assertEqual(item2.answer_count, 4)

    def test_defaults(self):
        d = {
            "id": "SO2",
            "package": "pkg",
            "question_title": "Q",
            "question_url": "http://x.com",
        }
        item = StackOverflowItem.from_dict(d)
        self.assertFalse(item.is_answered)
        self.assertEqual(item.answer_count, 0)
        self.assertEqual(item.view_count, 0)
        self.assertEqual(item.so_score, 0)


class TestRedditItemRoundtrip(unittest.TestCase):

    def test_full_roundtrip(self):
        item = RedditItem(
            id="RI1",
            package="stripe",
            subreddit="webdev",
            title="Stripe v8 webhook changes are killing me",
            url="https://reddit.com/r/webdev/comments/abc123",
            reddit_score=142,
            num_comments=37,
            top_comment="The rename to verify() is documented in MIGRATION.md.",
            date="2026-01-12",
            date_confidence="high",
            subs=SubScores(severity=0, recency=100, impact=36, community=60),
            score=55,
            cross_refs=["P1"],
        )
        d = item.to_dict()
        item2 = RedditItem.from_dict(d)
        self.assertEqual(item2.id, "RI1")
        self.assertEqual(item2.subreddit, "webdev")
        self.assertEqual(item2.reddit_score, 142)
        self.assertEqual(item2.num_comments, 37)
        self.assertEqual(item2.top_comment, item.top_comment)

    def test_defaults(self):
        d = {
            "id": "RI2",
            "package": "pkg",
            "subreddit": "programming",
            "title": "T",
            "url": "http://x.com",
        }
        item = RedditItem.from_dict(d)
        self.assertEqual(item.reddit_score, 0)
        self.assertEqual(item.num_comments, 0)
        self.assertIsNone(item.top_comment)
        self.assertEqual(item.date_confidence, "low")


class TestHackerNewsItemRoundtrip(unittest.TestCase):

    def test_full_roundtrip(self):
        item = HackerNewsItem(
            id="HN1",
            package="openai",
            title="OpenAI Python library v1.0 — Complete rewrite",
            url="https://github.com/openai/openai-python/releases/tag/v1.0.0",
            hn_url="https://news.ycombinator.com/item?id=38123456",
            points=487,
            num_comments=203,
            top_comment="The migration guide is actually pretty good.",
            date="2023-11-07",
            date_confidence="high",
            subs=SubScores(severity=0, recency=10, impact=63, community=62),
            score=50,
            cross_refs=["P2"],
        )
        d = item.to_dict()
        item2 = HackerNewsItem.from_dict(d)
        self.assertEqual(item2.id, "HN1")
        self.assertEqual(item2.points, 487)
        self.assertEqual(item2.num_comments, 203)
        self.assertEqual(item2.url, item.url)
        self.assertEqual(item2.hn_url, item.hn_url)

    def test_none_url(self):
        item = HackerNewsItem(
            id="HN2", package="pkg", title="T", url=None,
            hn_url="https://news.ycombinator.com/item?id=1",
        )
        d = item.to_dict()
        item2 = HackerNewsItem.from_dict(d)
        self.assertIsNone(item2.url)


class TestTwitterItemRoundtrip(unittest.TestCase):

    def test_full_roundtrip(self):
        item = TwitterItem(
            id="TW1",
            package="stripe",
            text="Just got hit by the stripe v8 breaking change in constructEvent. "
                 "Had to rewrite all webhook handlers. @stripe please better changelogs!",
            author_handle="webdevjane",
            likes=384,
            reposts=72,
            replies=31,
            date="2026-01-11",
            url="https://twitter.com/webdevjane/status/123456789",
            subs=SubScores(severity=0, recency=100, impact=27, community=93),
            score=62,
            cross_refs=["P1"],
        )
        d = item.to_dict()
        item2 = TwitterItem.from_dict(d)
        self.assertEqual(item2.id, "TW1")
        self.assertEqual(item2.author_handle, "webdevjane")
        self.assertEqual(item2.likes, 384)
        self.assertEqual(item2.reposts, 72)
        self.assertEqual(item2.replies, 31)

    def test_defaults(self):
        d = {
            "id": "TW2",
            "package": "pkg",
            "text": "Some tweet",
            "author_handle": "user",
        }
        item = TwitterItem.from_dict(d)
        self.assertEqual(item.likes, 0)
        self.assertEqual(item.reposts, 0)
        self.assertIsNone(item.date)
        self.assertIsNone(item.url)


class TestDepRadarReportRoundtrip(unittest.TestCase):

    def _make_report(self):
        bc = BreakingChange(
            symbol="constructEvent",
            change_type="removed",
            description="Removed in v8",
        )
        loc = ImpactLocation(
            file_path="src/webhook.ts",
            line_number=42,
            usage_text="stripe.webhooks.constructEvent(payload, sig, secret)",
        )
        pkg_breaking = PackageUpdate(
            id="P1",
            package="stripe",
            ecosystem="npm",
            current_version="7.0.0",
            latest_version="8.0.0",
            semver_type="major",
            has_breaking_changes=True,
            breaking_changes=[bc],
            impact_locations=[loc],
            impact_confidence="high",
            github_repo="stripe/stripe-node",
            score=88,
        )
        pkg_minor = PackageUpdate(
            id="P2",
            package="lodash",
            ecosystem="npm",
            current_version="4.17.20",
            latest_version="4.17.21",
            semver_type="patch",
            score=12,
        )
        gh_issue = GithubIssueItem(
            id="GI1",
            package="stripe",
            version="8.0.0",
            title="constructEvent removed in v8",
            url="https://github.com/stripe/stripe-node/issues/1842",
            comments=23,
            labels=["breaking-change"],
            state="open",
        )
        so_item = StackOverflowItem(
            id="SO1",
            package="stripe",
            question_title="stripe webhooks constructEvent not a function",
            question_url="https://stackoverflow.com/questions/78800042",
            answer_count=4,
            is_answered=True,
            view_count=3200,
            so_score=28,
        )
        reddit_item = RedditItem(
            id="RI1",
            package="stripe",
            subreddit="webdev",
            title="Stripe v8 breaking changes",
            url="https://reddit.com/r/webdev/comments/abc",
            reddit_score=142,
            num_comments=37,
        )
        hn_item = HackerNewsItem(
            id="HN1",
            package="openai",
            title="OpenAI Python v1.0 complete rewrite",
            url="https://github.com/openai/openai-python",
            hn_url="https://news.ycombinator.com/item?id=38123",
            points=487,
            num_comments=203,
        )
        tw_item = TwitterItem(
            id="TW1",
            package="stripe",
            text="stripe v8 broke all my webhooks",
            author_handle="devuser",
            likes=384,
        )
        return DepRadarReport(
            project_path="/home/user/my-project",
            dep_files_found=["package.json"],
            packages_scanned=10,
            packages_with_breaking_changes=[pkg_breaking],
            packages_with_minor_updates=[pkg_minor],
            packages_current=["axios", "express"],
            packages_not_found=["unknown-pkg"],
            github_issues=[gh_issue],
            stackoverflow=[so_item],
            reddit=[reddit_item],
            hackernews=[hn_item],
            twitter=[tw_item],
            registry_errors={"bad-pkg": "Not found"},
            community_errors={},
            scan_errors={},
            from_cache=False,
            cache_age_hours=None,
            depth="default",
            days_window=30,
            generated_at="2026-03-27T12:00:00Z",
        )

    def test_full_roundtrip(self):
        report = self._make_report()
        d = report.to_dict()
        report2 = DepRadarReport.from_dict(d)

        self.assertEqual(report2.project_path, "/home/user/my-project")
        self.assertEqual(report2.packages_scanned, 10)
        self.assertEqual(report2.dep_files_found, ["package.json"])
        self.assertEqual(len(report2.packages_with_breaking_changes), 1)
        self.assertEqual(len(report2.packages_with_minor_updates), 1)
        self.assertEqual(report2.packages_current, ["axios", "express"])
        self.assertEqual(report2.packages_not_found, ["unknown-pkg"])

        pkg = report2.packages_with_breaking_changes[0]
        self.assertEqual(pkg.package, "stripe")
        self.assertTrue(pkg.has_breaking_changes)
        self.assertEqual(len(pkg.breaking_changes), 1)
        self.assertEqual(len(pkg.impact_locations), 1)

        self.assertEqual(len(report2.github_issues), 1)
        self.assertEqual(len(report2.stackoverflow), 1)
        self.assertEqual(len(report2.reddit), 1)
        self.assertEqual(len(report2.hackernews), 1)
        self.assertEqual(len(report2.twitter), 1)
        self.assertEqual(report2.registry_errors, {"bad-pkg": "Not found"})
        self.assertFalse(report2.from_cache)
        self.assertEqual(report2.depth, "default")
        self.assertEqual(report2.days_window, 30)
        self.assertEqual(report2.generated_at, "2026-03-27T12:00:00Z")

    def test_empty_report_roundtrip(self):
        report = DepRadarReport(
            project_path="/tmp/empty",
            dep_files_found=[],
        )
        d = report.to_dict()
        report2 = DepRadarReport.from_dict(d)
        self.assertEqual(report2.project_path, "/tmp/empty")
        self.assertEqual(report2.packages_scanned, 0)
        self.assertEqual(report2.packages_with_breaking_changes, [])
        self.assertEqual(report2.packages_with_minor_updates, [])

    def test_to_dict_has_all_top_level_keys(self):
        report = self._make_report()
        d = report.to_dict()
        expected_keys = [
            "project_path", "dep_files_found", "packages_scanned",
            "packages_with_breaking_changes", "packages_with_minor_updates",
            "packages_current", "packages_not_found",
            "github_issues", "stackoverflow", "reddit", "hackernews", "twitter",
            "registry_errors", "community_errors", "scan_errors",
            "from_cache", "cache_age_hours", "depth", "days_window", "generated_at",
        ]
        for key in expected_keys:
            self.assertIn(key, d, f"Missing key: {key}")


if __name__ == "__main__":
    unittest.main()
