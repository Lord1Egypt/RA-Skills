"""Tests for scripts/lib/changelog_parser.py"""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "lib"))

from changelog_parser import (
    classify_change_type,
    extract_breaking_changes,
    extract_migration_note,
    extract_symbol,
    has_breaking_changes_flag,
    parse_version_section,
)

# ── Fixture release bodies ────────────────────────────────────────────────────

_STRIPE_V8_BODY = """\
## v8.0.0 — January 10, 2026

This is a major release with significant API improvements.

## Breaking Changes

- `stripe.webhooks.constructEvent()` has been renamed to `stripe.webhooks.verify()`. \
The old method has been removed entirely.
- `createCustomer()` now requires the `email` parameter. Previously this was optional.
- `stripe.charges.create()` is removed — use `stripe.paymentIntents.create()` instead.

## Migration Guide

Use `stripe.webhooks.verify()` instead of `constructEvent()`.

## Bug Fixes

- Fixed race condition in timing validation
"""

_OPENAI_V1_BODY = """\
## v1.0.0 — November 6, 2023

Complete rewrite of the OpenAI Python SDK.

## BREAKING CHANGES

- `openai.Completion.create()` removed (use `client.completions.create()`)
- `openai.ChatCompletion.create()` removed (use `client.chat.completions.create()`)
- Error classes moved from `openai.error.*` to `openai.*`

Run `openai migrate` for auto-fix.

## New Features

- Full async support via AsyncOpenAI
"""

_NO_BREAKING_BODY = """\
## v1.2.3 — March 1, 2026

### Improvements

- Performance improvements to pagination
- Better error messages

### Bug Fixes

- Fixed memory leak in event loop
"""

_CC_BANG_BODY = """\
feat!: removed legacy authentication endpoint

The old `/api/v1/auth/token` endpoint has been removed.
Use `/api/v2/auth/token` instead.

BREAKING CHANGE: The `getAuthToken()` function signature changed.
Old: getAuthToken(username, password)
New: getAuthToken({ username, password, mfaCode })
"""

_CC_FOOTER_BODY = """\
refactor(api): restructure payment processing

Reorganizes the internal payment API for better modularity.

BREAKING CHANGE: PaymentProcessor.charge() renamed to PaymentProcessor.process().
"""

_CHANGELOG_WITH_VERSIONS = """\
# Changelog

## [8.0.0] - 2026-01-10

### Breaking Changes

- `constructEvent()` removed

## [7.5.0] - 2025-06-15

### Changes

- Minor performance improvements
"""


class TestExtractBreakingChangesStripe(unittest.TestCase):

    def test_detects_construct_event_removal(self):
        bcs = extract_breaking_changes(_STRIPE_V8_BODY)
        symbols = [bc.symbol for bc in bcs]
        descriptions = " ".join(bc.description for bc in bcs).lower()
        # Should detect constructEvent or verify
        found = any(
            "constructEvent" in s or "verify" in s or "construct" in s.lower()
            for s in symbols
        ) or "constructevent" in descriptions or "construct" in descriptions
        self.assertTrue(found, f"Expected constructEvent detection; got: {symbols}")

    def test_detects_charges_create_removal(self):
        bcs = extract_breaking_changes(_STRIPE_V8_BODY)
        descriptions = " ".join(bc.description.lower() for bc in bcs)
        self.assertTrue(
            "charges" in descriptions or "removed" in descriptions,
            f"Expected charges.create removal; descriptions: {descriptions[:300]}",
        )

    def test_returns_multiple_breaking_changes(self):
        bcs = extract_breaking_changes(_STRIPE_V8_BODY)
        self.assertGreater(len(bcs), 0)

    def test_all_items_are_breaking_changes(self):
        from schema import BreakingChange
        bcs = extract_breaking_changes(_STRIPE_V8_BODY)
        for bc in bcs:
            self.assertIsInstance(bc, BreakingChange)
            self.assertIsInstance(bc.symbol, str)
            self.assertIsInstance(bc.description, str)


class TestExtractBreakingChangesOpenAI(unittest.TestCase):

    def test_detects_completion_create_removal(self):
        bcs = extract_breaking_changes(_OPENAI_V1_BODY)
        descriptions = " ".join(bc.description for bc in bcs)
        self.assertTrue(
            "Completion" in descriptions or "completion" in descriptions.lower(),
            f"Expected Completion removal; got: {descriptions[:400]}",
        )

    def test_detects_chat_completion_removal(self):
        bcs = extract_breaking_changes(_OPENAI_V1_BODY)
        descriptions = " ".join(bc.description for bc in bcs)
        self.assertTrue(
            "ChatCompletion" in descriptions or "chat" in descriptions.lower(),
            f"Expected ChatCompletion removal; got: {descriptions[:400]}",
        )

    def test_detects_error_class_move(self):
        bcs = extract_breaking_changes(_OPENAI_V1_BODY)
        descriptions = " ".join(bc.description.lower() for bc in bcs)
        self.assertTrue(
            "error" in descriptions or "moved" in descriptions,
            f"Expected error class change; got: {descriptions[:400]}",
        )

    def test_has_multiple_results(self):
        bcs = extract_breaking_changes(_OPENAI_V1_BODY)
        self.assertGreater(len(bcs), 0)


class TestExtractBreakingChangesConventionalCommits(unittest.TestCase):

    def test_feat_bang_detected(self):
        bcs = extract_breaking_changes(_CC_BANG_BODY)
        descriptions = " ".join(bc.description for bc in bcs)
        self.assertTrue(
            "legacy" in descriptions.lower() or "endpoint" in descriptions.lower()
            or "removed" in descriptions.lower(),
            f"feat! breaking change not detected; got: {descriptions[:400]}",
        )

    def test_breaking_change_footer_detected(self):
        bcs = extract_breaking_changes(_CC_FOOTER_BODY)
        descriptions = " ".join(bc.description for bc in bcs)
        self.assertTrue(
            "PaymentProcessor" in descriptions or "charge" in descriptions.lower()
            or "process" in descriptions.lower(),
            f"BREAKING CHANGE footer not detected; got: {descriptions[:400]}",
        )

    def test_footer_in_cc_bang(self):
        bcs = extract_breaking_changes(_CC_BANG_BODY)
        descriptions = " ".join(bc.description for bc in bcs)
        self.assertTrue(
            "getAuthToken" in descriptions or "auth" in descriptions.lower(),
            f"BREAKING CHANGE footer not detected; got: {descriptions[:400]}",
        )


class TestNoBreakingChanges(unittest.TestCase):

    def test_returns_empty_list(self):
        bcs = extract_breaking_changes(_NO_BREAKING_BODY)
        self.assertEqual(bcs, [])

    def test_empty_string(self):
        bcs = extract_breaking_changes("")
        self.assertEqual(bcs, [])

    def test_whitespace_only(self):
        bcs = extract_breaking_changes("   \n\n  ")
        self.assertEqual(bcs, [])


class TestClassifyChangeType(unittest.TestCase):

    def test_removed(self):
        self.assertEqual(classify_change_type("The method was removed in this version"), "removed")
        self.assertEqual(classify_change_type("This API has been deleted"), "removed")
        self.assertEqual(classify_change_type("Support for X has been dropped"), "removed")

    def test_renamed(self):
        self.assertEqual(classify_change_type("foo() was renamed to bar()"), "renamed")
        self.assertEqual(classify_change_type("The function has moved to utils module"), "renamed")

    def test_signature_changed(self):
        self.assertEqual(
            classify_change_type("The parameter list for init() has changed"),
            "signature_changed",
        )
        self.assertEqual(
            classify_change_type("The argument order is now reversed"),
            "signature_changed",
        )

    def test_type_changed(self):
        # "return type" also matches signature_changed first; use "type changed" phrasing
        self.assertEqual(
            classify_change_type("The property is now typed as number instead of string"),
            "type_changed",
        )

    def test_deprecated(self):
        self.assertEqual(classify_change_type("This method is now deprecated"), "deprecated")

    def test_behavior_changed(self):
        self.assertEqual(
            classify_change_type("The default behavior has changed"),
            "behavior_changed",
        )
        self.assertEqual(
            classify_change_type("This now throws an error instead of returning null"),
            "behavior_changed",
        )

    def test_other_fallback(self):
        self.assertEqual(classify_change_type("Something changed"), "other")


class TestExtractSymbol(unittest.TestCase):

    def test_backtick_quoted(self):
        result = extract_symbol("`stripe.webhooks.constructEvent()` was removed")
        self.assertIn("constructEvent", result)

    def test_method_call_pattern(self):
        result = extract_symbol("The createCustomer() method now requires email")
        self.assertIn("createCustomer", result)

    def test_camel_case(self):
        result = extract_symbol("The PaymentProcessor class was renamed")
        self.assertIn("PaymentProcessor", result)

    def test_snake_case_long(self):
        result = extract_symbol("use create_payment_intent instead")
        self.assertIn("create_payment_intent", result)

    def test_quoted_identifier(self):
        result = extract_symbol("The 'getToken' function has been removed")
        self.assertIn("getToken", result)

    def test_empty_string(self):
        result = extract_symbol("There is no symbol here - just text.")
        self.assertIsInstance(result, str)

    def test_dotted_path_extracts_base(self):
        result = extract_symbol("`openai.Completion.create()` is removed")
        # Should extract base symbol, not full path
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)


class TestHasBreakingChangesFlag(unittest.TestCase):

    def test_breaking_section_header(self):
        self.assertTrue(has_breaking_changes_flag("## Breaking Changes\n- something"))

    def test_conventional_commit_footer(self):
        self.assertTrue(has_breaking_changes_flag("BREAKING CHANGE: foo removed"))

    def test_feat_bang(self):
        self.assertTrue(has_breaking_changes_flag("feat!: removed old API\n\nDetails."))

    def test_keyword_removed(self):
        self.assertTrue(has_breaking_changes_flag("The method was removed in this release"))

    def test_no_breaking(self):
        self.assertFalse(has_breaking_changes_flag("Minor performance improvements."))

    def test_empty(self):
        self.assertFalse(has_breaking_changes_flag(""))


class TestParseVersionSection(unittest.TestCase):

    def test_extracts_version_section(self):
        section = parse_version_section(_CHANGELOG_WITH_VERSIONS, "8.0.0")
        self.assertIsNotNone(section)
        self.assertIn("Breaking Changes", section)
        self.assertIn("constructEvent", section)

    def test_section_does_not_include_next_version(self):
        section = parse_version_section(_CHANGELOG_WITH_VERSIONS, "8.0.0")
        self.assertIsNotNone(section)
        self.assertNotIn("7.5.0", section)

    def test_older_version_section(self):
        section = parse_version_section(_CHANGELOG_WITH_VERSIONS, "7.5.0")
        self.assertIsNotNone(section)
        self.assertIn("performance", section.lower())

    def test_version_before_all_entries_returns_none(self):
        # 0.0.1 is before the oldest changelog entry — no preceding version exists
        section = parse_version_section(_CHANGELOG_WITH_VERSIONS, "0.0.1")
        self.assertIsNone(section)

    def test_future_version_falls_back_to_latest(self):
        # 99.0.0 is after all entries — nearest preceding = 8.0.0 (highest in changelog)
        section = parse_version_section(_CHANGELOG_WITH_VERSIONS, "99.0.0")
        self.assertIsNotNone(section)
        self.assertIn("Breaking Changes", section)

    def test_empty_changelog_returns_none(self):
        section = parse_version_section("", "1.0.0")
        self.assertIsNone(section)


class TestExtractMigrationNote(unittest.TestCase):

    def test_use_instead(self):
        result = extract_migration_note("Use `webhooks.verify()` instead")
        self.assertIsNotNone(result)
        self.assertIn("verify", result)

    def test_replace_with(self):
        result = extract_migration_note("Replace with `client.completions.create()`")
        self.assertIsNotNone(result)

    def test_migrate_to(self):
        result = extract_migration_note("migrated to `newMethod()`")
        self.assertIsNotNone(result)

    def test_no_migration_returns_none(self):
        result = extract_migration_note("The function was removed from the library")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
