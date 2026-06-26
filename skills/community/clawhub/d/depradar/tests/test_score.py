"""Tests for scripts/lib/score.py"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "lib"))

from dates import days_ago, today_utc
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
from score import (
    SEVERITY_MAP,
    enrich_package_community_scores,
    score_all,
    score_github_issue,
    score_hackernews_item,
    score_package_update,
    score_reddit_item,
    score_stackoverflow_item,
)


def _make_package(
    package="stripe",
    current="7.0.0",
    latest="8.0.0",
    btype="major",
    has_breaking=True,
    breaking_changes=None,
    impact_confidence="not_scanned",
    release_date=None,
    idx=1,
):
    bcs = breaking_changes or []
    return PackageUpdate(
        id=f"P{idx}",
        package=package,
        ecosystem="npm",
        current_version=current,
        latest_version=latest,
        semver_type=btype,
        has_breaking_changes=has_breaking,
        breaking_changes=bcs,
        impact_confidence=impact_confidence,
        release_date=release_date or today_utc(),
    )


class TestScorePackageUpdate(unittest.TestCase):

    def test_removed_change_scores_high(self):
        bc_removed = BreakingChange("constructEvent", "removed", "Method removed")
        bc_deprecated = BreakingChange("legacyFn", "deprecated", "Function deprecated")
        pkg_removed = _make_package(breaking_changes=[bc_removed])
        pkg_deprecated = _make_package(breaking_changes=[bc_deprecated])
        score_package_update(pkg_removed)
        score_package_update(pkg_deprecated)
        self.assertGreater(pkg_removed.score, pkg_deprecated.score)

    def test_deprecated_scores_lowest_of_breaking(self):
        change_types = ["removed", "renamed", "signature_changed",
                        "behavior_changed", "type_changed", "deprecated"]
        scores = {}
        for ctype in change_types:
            bc = BreakingChange("sym", ctype, "desc")
            pkg = _make_package(breaking_changes=[bc])
            score_package_update(pkg)
            scores[ctype] = pkg.score
        # "removed" should have highest severity
        self.assertGreaterEqual(scores["removed"], scores["deprecated"])
        self.assertGreaterEqual(scores["removed"], scores["renamed"])

    def test_score_range_0_100(self):
        bc = BreakingChange("sym", "removed", "desc")
        pkg = _make_package(breaking_changes=[bc])
        score_package_update(pkg)
        self.assertGreaterEqual(pkg.score, 0)
        self.assertLessEqual(pkg.score, 100)

    def test_has_subs_after_scoring(self):
        bc = BreakingChange("sym", "removed", "desc")
        pkg = _make_package(breaking_changes=[bc])
        score_package_update(pkg)
        self.assertIsNotNone(pkg.subs)
        self.assertIsInstance(pkg.subs, SubScores)

    def test_minor_update_scores_lower_than_breaking(self):
        bc = BreakingChange("sym", "removed", "desc")
        breaking_pkg = _make_package(
            breaking_changes=[bc],
            release_date=today_utc(),
        )
        minor_pkg = _make_package(
            has_breaking=False,
            btype="minor",
            latest="7.1.0",
            current="7.0.0",
            release_date=today_utc(),
        )
        score_package_update(breaking_pkg)
        score_package_update(minor_pkg)
        self.assertGreater(breaking_pkg.score, minor_pkg.score)

    def test_high_impact_confidence_increases_score(self):
        bc = BreakingChange("sym", "removed", "desc")
        pkg_high = _make_package(breaking_changes=[bc], impact_confidence="high")
        pkg_not_scanned = _make_package(breaking_changes=[bc], impact_confidence="not_scanned")
        score_package_update(pkg_high)
        score_package_update(pkg_not_scanned)
        # high confidence should score >= not_scanned
        self.assertGreaterEqual(pkg_high.score, pkg_not_scanned.score)

    def test_recent_release_scores_higher(self):
        bc = BreakingChange("sym", "removed", "desc")
        pkg_recent = _make_package(breaking_changes=[bc], release_date=today_utc())
        pkg_old = _make_package(breaking_changes=[bc], release_date=days_ago(180))
        score_package_update(pkg_recent)
        score_package_update(pkg_old)
        self.assertGreater(pkg_recent.score, pkg_old.score)


class TestScoreGithubIssue(unittest.TestCase):

    def test_breaking_change_label_boosts_score(self):
        item_breaking = GithubIssueItem(
            id="GI1", package="stripe", version="8.0.0",
            title="Breaking change", url="http://x.com",
            labels=["breaking-change"], comments=10,
            created_at=today_utc(),
        )
        item_regular = GithubIssueItem(
            id="GI2", package="stripe", version="8.0.0",
            title="Regular issue", url="http://x.com",
            labels=[], comments=10,
            created_at=today_utc(),
        )
        score_github_issue(item_breaking)
        score_github_issue(item_regular)
        self.assertGreater(item_breaking.score, item_regular.score)

    def test_more_comments_higher_score(self):
        item_many = GithubIssueItem(
            id="GI3", package="pkg", version="1.0.0",
            title="Issue with many comments", url="http://x.com",
            comments=50, created_at=today_utc(),
        )
        item_few = GithubIssueItem(
            id="GI4", package="pkg", version="1.0.0",
            title="Issue with few comments", url="http://x.com",
            comments=2, created_at=today_utc(),
        )
        score_github_issue(item_many)
        score_github_issue(item_few)
        self.assertGreater(item_many.score, item_few.score)

    def test_score_range_0_100(self):
        item = GithubIssueItem(
            id="GI5", package="pkg", version="1.0.0",
            title="T", url="http://x.com",
            comments=1000, labels=["breaking-change"],
            created_at=today_utc(),
        )
        score_github_issue(item)
        self.assertGreaterEqual(item.score, 0)
        self.assertLessEqual(item.score, 100)

    def test_assigns_subs(self):
        item = GithubIssueItem(
            id="GI6", package="pkg", version="1.0.0",
            title="T", url="http://x.com", created_at=today_utc(),
        )
        score_github_issue(item)
        self.assertIsNotNone(item.subs)

    def test_bug_label_higher_than_no_label(self):
        item_bug = GithubIssueItem(
            id="GI7", package="pkg", version="1.0.0",
            title="T", url="http://x.com",
            labels=["bug"], comments=5, created_at=today_utc(),
        )
        item_none = GithubIssueItem(
            id="GI8", package="pkg", version="1.0.0",
            title="T", url="http://x.com",
            labels=[], comments=5, created_at=today_utc(),
        )
        score_github_issue(item_bug)
        score_github_issue(item_none)
        self.assertGreaterEqual(item_bug.score, item_none.score)


class TestScoreStackOverflowItem(unittest.TestCase):

    def test_answered_with_high_views(self):
        item = StackOverflowItem(
            id="SO1", package="stripe",
            question_title="Q", question_url="http://x.com",
            answer_count=4, is_answered=True,
            view_count=3200, so_score=28,
            created_at=today_utc(),
        )
        score_stackoverflow_item(item)
        self.assertGreater(item.score, 0)
        self.assertLessEqual(item.score, 100)

    def test_high_views_increases_score(self):
        item_high = StackOverflowItem(
            id="SO2", package="p",
            question_title="Q", question_url="http://x.com",
            view_count=10000, so_score=50, answer_count=5,
            created_at=today_utc(),
        )
        item_low = StackOverflowItem(
            id="SO3", package="p",
            question_title="Q", question_url="http://x.com",
            view_count=10, so_score=2, answer_count=1,
            created_at=today_utc(),
        )
        score_stackoverflow_item(item_high)
        score_stackoverflow_item(item_low)
        self.assertGreater(item_high.score, item_low.score)

    def test_assigns_subs(self):
        item = StackOverflowItem(
            id="SO4", package="p",
            question_title="Q", question_url="http://x.com",
        )
        score_stackoverflow_item(item)
        self.assertIsNotNone(item.subs)

    def test_score_range_0_100(self):
        item = StackOverflowItem(
            id="SO5", package="p",
            question_title="Q", question_url="http://x.com",
            view_count=100000, so_score=9999, answer_count=100,
        )
        score_stackoverflow_item(item)
        self.assertLessEqual(item.score, 100)


class TestScoreRedditItem(unittest.TestCase):

    def test_high_engagement_scores_higher(self):
        item_hot = RedditItem(
            id="RI1", package="stripe", subreddit="webdev",
            title="T", url="http://x.com",
            reddit_score=500, num_comments=120, date=today_utc(),
        )
        item_cold = RedditItem(
            id="RI2", package="stripe", subreddit="webdev",
            title="T", url="http://x.com",
            reddit_score=2, num_comments=0, date=today_utc(),
        )
        score_reddit_item(item_hot)
        score_reddit_item(item_cold)
        self.assertGreater(item_hot.score, item_cold.score)

    def test_log1p_scaling_does_not_overflow(self):
        item = RedditItem(
            id="RI3", package="p", subreddit="r",
            title="T", url="http://x.com",
            reddit_score=999999, num_comments=999999,
        )
        score_reddit_item(item)
        self.assertLessEqual(item.score, 100)

    def test_assigns_subs(self):
        item = RedditItem(
            id="RI4", package="p", subreddit="r",
            title="T", url="http://x.com",
        )
        score_reddit_item(item)
        self.assertIsNotNone(item.subs)

    def test_zero_engagement(self):
        item = RedditItem(
            id="RI5", package="p", subreddit="r",
            title="T", url="http://x.com",
            reddit_score=0, num_comments=0,
        )
        score_reddit_item(item)
        self.assertGreaterEqual(item.score, 0)


class TestScoreHackerNewsItem(unittest.TestCase):

    def test_high_points_increases_score(self):
        item_high = HackerNewsItem(
            id="HN1", package="openai",
            title="T", url=None, hn_url="http://hn.com",
            points=500, num_comments=200, date=today_utc(),
        )
        item_low = HackerNewsItem(
            id="HN2", package="openai",
            title="T", url=None, hn_url="http://hn.com",
            points=5, num_comments=2, date=today_utc(),
        )
        score_hackernews_item(item_high)
        score_hackernews_item(item_low)
        self.assertGreater(item_high.score, item_low.score)

    def test_score_range_0_100(self):
        item = HackerNewsItem(
            id="HN3", package="p",
            title="T", url=None, hn_url="http://hn.com",
            points=99999, num_comments=99999,
        )
        score_hackernews_item(item)
        self.assertLessEqual(item.score, 100)

    def test_assigns_subs(self):
        item = HackerNewsItem(
            id="HN4", package="p",
            title="T", url=None, hn_url="http://hn.com",
        )
        score_hackernews_item(item)
        self.assertIsNotNone(item.subs)


class TestScoreAll(unittest.TestCase):

    def _make_report(self):
        bc = BreakingChange("constructEvent", "removed", "Removed in v8")
        pkg_breaking = PackageUpdate(
            id="P1", package="stripe", ecosystem="npm",
            current_version="7.0.0", latest_version="8.0.0",
            semver_type="major", has_breaking_changes=True,
            breaking_changes=[bc],
            release_date=today_utc(),
        )
        pkg_minor1 = PackageUpdate(
            id="P2", package="lodash", ecosystem="npm",
            current_version="4.17.20", latest_version="4.17.21",
            semver_type="patch", release_date=today_utc(),
        )
        pkg_minor2 = PackageUpdate(
            id="P3", package="axios", ecosystem="npm",
            current_version="1.3.0", latest_version="1.5.0",
            semver_type="minor", release_date=days_ago(10),
        )
        gh_issue = GithubIssueItem(
            id="GI1", package="stripe", version="8.0.0",
            title="Breaking", url="http://x.com",
            labels=["breaking-change"], comments=23,
            created_at=today_utc(),
        )
        so_item = StackOverflowItem(
            id="SO1", package="stripe",
            question_title="Q", question_url="http://x.com",
            answer_count=4, is_answered=True,
            view_count=3200, so_score=28,
        )
        return DepRadarReport(
            project_path="/tmp/project",
            dep_files_found=["package.json"],
            packages_scanned=3,
            packages_with_breaking_changes=[pkg_breaking],
            packages_with_minor_updates=[pkg_minor1, pkg_minor2],
            github_issues=[gh_issue],
            stackoverflow=[so_item],
        )

    def test_score_all_assigns_scores(self):
        report = self._make_report()
        result = score_all(report)
        for pkg in result.packages_with_breaking_changes:
            self.assertGreater(pkg.score, 0)
        for pkg in result.packages_with_minor_updates:
            self.assertIsNotNone(pkg.score)

    def test_score_all_sorts_breaking_desc(self):
        bc1 = BreakingChange("sym1", "removed", "d1")
        bc2 = BreakingChange("sym2", "deprecated", "d2")
        pkg1 = PackageUpdate(
            id="P1", package="pkg1", ecosystem="npm",
            current_version="1.0.0", latest_version="2.0.0",
            semver_type="major", has_breaking_changes=True,
            breaking_changes=[bc1], release_date=today_utc(),
        )
        pkg2 = PackageUpdate(
            id="P2", package="pkg2", ecosystem="npm",
            current_version="1.0.0", latest_version="2.0.0",
            semver_type="major", has_breaking_changes=True,
            breaking_changes=[bc2], release_date=today_utc(),
        )
        # Force different scores by ordering
        report = DepRadarReport(
            project_path="/tmp", dep_files_found=[],
            packages_with_breaking_changes=[pkg2, pkg1],  # intentionally reversed
        )
        result = score_all(report)
        scores = [p.score for p in result.packages_with_breaking_changes]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_community_signals_count(self):
        """More community signals for a package should raise its community sub-score."""
        bc = BreakingChange("sym", "removed", "d")
        pkg = PackageUpdate(
            id="P1", package="stripe", ecosystem="npm",
            current_version="7.0.0", latest_version="8.0.0",
            semver_type="major", has_breaking_changes=True,
            breaking_changes=[bc], release_date=today_utc(),
        )
        # 3 community signals — titles reference the package so they pass relevance filter
        gi1 = GithubIssueItem(id="GI1", package="stripe", version="8", title="stripe breaking change in v8", url="u")
        gi2 = GithubIssueItem(id="GI2", package="stripe", version="8", title="stripe API removed in v8", url="u")
        so1 = StackOverflowItem(id="SO1", package="stripe", question_title="stripe deprecated method", question_url="u")
        report = DepRadarReport(
            project_path="/tmp", dep_files_found=[],
            packages_with_breaking_changes=[pkg],
            github_issues=[gi1, gi2],
            stackoverflow=[so1],
        )
        score_all(report)
        # Community sub-score should be > 0
        self.assertIsNotNone(pkg.subs)
        self.assertGreater(pkg.subs.community, 0)


class TestSeverityMap(unittest.TestCase):

    def test_removed_is_max(self):
        self.assertEqual(SEVERITY_MAP["removed"], 100)

    def test_deprecated_is_low(self):
        self.assertLess(SEVERITY_MAP["deprecated"], SEVERITY_MAP["removed"])

    def test_all_known_types_present(self):
        expected = [
            "removed", "renamed", "signature_changed",
            "behavior_changed", "type_changed", "deprecated", "other"
        ]
        for t in expected:
            self.assertIn(t, SEVERITY_MAP)


if __name__ == "__main__":
    unittest.main()
