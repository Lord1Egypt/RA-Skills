"""Tests for community signal title relevance filter (R14)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts", "lib"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from score import _title_is_probably_relevant, _community_pain_count


def _make_report_with_hn(title: str, package: str):
    """Build a minimal DepRadarReport with one HackerNews item."""
    from schema import DepRadarReport, HackerNewsItem
    item = HackerNewsItem(
        id="HN1",
        package=package,
        title=title,
        url="https://news.ycombinator.com/item?id=1",
        hn_url="https://news.ycombinator.com/item?id=1",
        points=10,
        num_comments=5,
        date="2026-01-15",
        subs=None,
        score=50,
        cross_refs=[],
    )
    return DepRadarReport(
        project_path="/test",
        dep_files_found=[],
        packages_scanned=1,
        hackernews=[item],
    )


class TestTitleIsProbablyRelevant(unittest.TestCase):
    def test_flutter_checklist_rejected_for_commander(self):
        self.assertFalse(
            _title_is_probably_relevant("Flutter Pre-Launch Checklist", "commander")
        )

    def test_package_name_in_title_accepted(self):
        self.assertTrue(
            _title_is_probably_relevant("commander breaking change in v10", "commander")
        )

    def test_technical_word_accepted(self):
        self.assertTrue(
            _title_is_probably_relevant("API deprecated removed", "commander")
        )

    def test_unrelated_newsletter_rejected(self):
        self.assertFalse(
            _title_is_probably_relevant("Weekly JavaScript Newsletter #42", "commander")
        )

    def test_tutorial_rejected(self):
        self.assertFalse(
            _title_is_probably_relevant("Complete Tutorial for Beginners", "express")
        )

    def test_direct_package_mention_wins_over_unrelated_word(self):
        # "commander" in title trumps any unrelated platform word
        self.assertTrue(
            _title_is_probably_relevant("commander flutter integration guide", "commander")
        )

    def test_migration_keyword_accepted(self):
        self.assertTrue(
            _title_is_probably_relevant("migration guide upgrade breaking", "webpack")
        )

    def test_youtube_video_rejected(self):
        self.assertFalse(
            _title_is_probably_relevant("YouTube course for learning JavaScript", "axios")
        )

    def test_scoped_package_base_name_extracted(self):
        # @angular/core → base is "core"
        self.assertTrue(
            _title_is_probably_relevant("angular core breaking change", "@angular/core")
        )

    def test_empty_title_returns_false(self):
        self.assertFalse(_title_is_probably_relevant("", "commander"))

    def test_changelog_keyword_accepted(self):
        self.assertTrue(
            _title_is_probably_relevant("webpack changelog update release notes", "webpack")
        )

    def test_android_ios_platform_rejected(self):
        # Mobile platform content should be rejected for a JS package
        self.assertFalse(
            _title_is_probably_relevant("iOS Android Swift development checklist", "chalk")
        )


class TestCommunityPainCountFiltering(unittest.TestCase):
    def test_flutter_checklist_not_counted(self):
        """Noise titles should not inflate community pain count."""
        report = _make_report_with_hn("Flutter Pre-Launch Checklist", "commander")
        # version_range="10.0.0" means major=10; HN item has no version mention
        count = _community_pain_count("commander", report, version_range="10.0.0")
        self.assertEqual(count, 0.0)

    def test_direct_mention_counted(self):
        """Relevant titles should be counted."""
        report = _make_report_with_hn("commander breaking change in v10", "commander")
        count = _community_pain_count("commander", report, version_range="10.0.0")
        self.assertGreater(count, 0.0)

    def test_version_mismatch_not_counted(self):
        """Signals mentioning a different major version should be excluded."""
        report = _make_report_with_hn("commander v8 migration", "commander")
        count = _community_pain_count("commander", report, version_range="10.0.0")
        self.assertEqual(count, 0.0)

    def test_version_match_counted(self):
        """Signals mentioning the right major version should be counted."""
        report = _make_report_with_hn("commander v10 breaks my script", "commander")
        count = _community_pain_count("commander", report, version_range="10.0.0")
        self.assertGreater(count, 0.0)


if __name__ == "__main__":
    unittest.main()
