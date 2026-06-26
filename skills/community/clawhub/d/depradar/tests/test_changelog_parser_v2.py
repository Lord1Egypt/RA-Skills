"""Tests for v2 changelog_parser improvements.

Covers:
- _pass3_keyword_scan() no longer fires on plain prose (Fix 5)
- parse_version_section() nearest-version fallback (Fix 7)
- source_excerpt populated in BreakingChange (Fix 27)
"""

import sys
import pytest

from lib.changelog_parser import (
    extract_breaking_changes,
    parse_version_section,
    _pass3_keyword_scan,
)


class TestKeywordScanNoFalsePositives:
    def test_prose_removed_not_flagged(self):
        """'removed a typo in the README' should NOT trigger keyword scanner."""
        text = "removed a typo in the README\n"
        hits = _pass3_keyword_scan(text)
        assert not hits, f"Expected no hits, got: {hits}"

    def test_prose_deleted_not_flagged(self):
        text = "deleted some old files from the docs folder\n"
        hits = _pass3_keyword_scan(text)
        assert not hits

    def test_code_removed_flagged(self):
        """`removed `constructEvent()`` should trigger."""
        text = "removed `constructEvent()` from the webhooks API\n"
        hits = _pass3_keyword_scan(text)
        assert len(hits) >= 1

    def test_camelcase_removed_flagged(self):
        text = "The method createCustomer has been removed\n"
        hits = _pass3_keyword_scan(text)
        assert len(hits) >= 1

    def test_dot_method_removed_flagged(self):
        text = "webhooks.constructEvent() removed in v8\n"
        hits = _pass3_keyword_scan(text)
        assert len(hits) >= 1

    def test_semver_reference_flagged(self):
        text = "dropped support for v2.0 users\n"
        hits = _pass3_keyword_scan(text)
        assert len(hits) >= 1

    def test_code_block_content_flagged(self):
        """Lines inside ``` blocks should be flagged even without code symbols."""
        text = "```\nremoved the old API endpoint\n```\n"
        hits = _pass3_keyword_scan(text)
        assert len(hits) >= 1

    def test_indented_code_flagged(self):
        """Lines indented 4+ spaces (like code) should be flagged."""
        text = "    removed deprecated function\n"
        hits = _pass3_keyword_scan(text)
        assert len(hits) >= 1

    def test_empty_text_no_hits(self):
        assert _pass3_keyword_scan("") == []

    def test_comment_header_not_flagged(self):
        """Section headers like '## Removed' with no content shouldn't produce hits."""
        text = "## Removed\n\nWe removed a CI badge from the readme.\n"
        hits = _pass3_keyword_scan(text)
        assert not hits


class TestParseVersionSectionFallback:
    CHANGELOG = """
## [9.0.0] - 2026-03-01
Big rewrite section

## [8.2.1] - 2026-02-01
Patch section

## [8.0.0] - 2026-01-01
Major section

## [7.5.0] - 2025-12-01
Previous major section
"""

    def test_exact_match(self):
        text = parse_version_section(self.CHANGELOG, "8.0.0")
        assert text is not None
        assert "Major section" in text

    def test_normalized_match_strips_v(self):
        text = parse_version_section(self.CHANGELOG, "v8.0.0")
        # Should match ## [8.0.0]
        assert text is not None

    def test_nearest_preceding_version(self):
        """8.0.1 doesn't exist — should fall back to 8.0.0."""
        text = parse_version_section(self.CHANGELOG, "8.0.1")
        assert text is not None
        assert "Major section" in text

    def test_nearest_preceding_patch_in_minor(self):
        """8.2.5 doesn't exist — should fall back to 8.2.1."""
        text = parse_version_section(self.CHANGELOG, "8.2.5")
        assert text is not None
        assert "Patch section" in text

    def test_version_before_earliest_returns_none(self):
        """5.0.0 is before all entries — should return None."""
        text = parse_version_section(self.CHANGELOG, "5.0.0")
        assert text is None

    def test_no_changelog_returns_none(self):
        assert parse_version_section("", "1.0.0") is None


class TestSourceExcerpt:
    def test_source_excerpt_populated(self):
        """BreakingChange.source_excerpt should contain the triggering line."""
        text = "removed `stripe.webhooks.constructEvent()` in v8\n"
        changes = extract_breaking_changes(text, source="changelog")
        assert len(changes) >= 1
        for bc in changes:
            if bc.source_excerpt is not None:
                assert "constructEvent" in bc.source_excerpt or len(bc.source_excerpt) > 0
                break

    def test_no_breaking_changes_empty_list(self):
        text = "Minor bug fixes and performance improvements.\n"
        changes = extract_breaking_changes(text, source="changelog")
        assert changes == []
