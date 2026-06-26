"""Tests for scoped package name handling in migration notes (R2)."""
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts", "lib"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from changelog_parser import extract_migration_note, _BACKTICK_RE, _MIGRATION_RE


class TestMigrationNoteScoped(unittest.TestCase):
    def test_use_scoped_package_instead(self):
        result = extract_migration_note("use @noble/hashes/sha256 instead")
        self.assertIsNotNone(result)
        self.assertIn("@noble/hashes/sha256", result)

    def test_scoped_package_in_backticks(self):
        result = extract_migration_note("use `@google/genai` instead")
        self.assertIsNotNone(result)
        self.assertIn("@google/genai", result)

    def test_unscoped_package_unchanged(self):
        result = extract_migration_note("use express instead")
        self.assertIsNotNone(result)
        self.assertIn("express", result)

    def test_replace_with_scoped(self):
        result = extract_migration_note("replace with @scope/new-pkg")
        self.assertIsNotNone(result)
        self.assertIn("@scope/new-pkg", result)

    def test_now_using_scoped(self):
        result = extract_migration_note("now using @scope/pkg")
        self.assertIsNotNone(result)
        self.assertIn("@scope/pkg", result)

    def test_instead_use_scoped(self):
        result = extract_migration_note("instead use @noble/hashes")
        self.assertIsNotNone(result)
        self.assertIn("@noble/hashes", result)

    def test_migrate_to_scoped(self):
        result = extract_migration_note("migrate to @google/generative-ai")
        self.assertIsNotNone(result)
        self.assertIn("@google/generative-ai", result)

    def test_none_on_garbage(self):
        result = extract_migration_note("this is just some random text about nothing")
        self.assertIsNone(result)

    def test_scoped_with_slash_path(self):
        """@noble/hashes/sha256 has a path component with /."""
        result = extract_migration_note("use @noble/hashes/sha256 instead")
        self.assertIsNotNone(result)
        # Should preserve the full path including /sha256
        self.assertIn("noble", result)

    def test_backtick_re_captures_scoped(self):
        """_BACKTICK_RE should match scoped package names in backticks."""
        m = _BACKTICK_RE.search("`@angular/core`")
        self.assertIsNotNone(m)
        self.assertIn("@angular/core", m.group(0))

    def test_backtick_re_captures_path(self):
        """_BACKTICK_RE should match @scope/pkg/path in backticks."""
        m = _BACKTICK_RE.search("`@noble/hashes/sha256`")
        self.assertIsNotNone(m)

    def test_migration_re_has_five_groups(self):
        """All 5 alternation groups should accept @ prefix."""
        # Test each pattern variant
        patterns = [
            "use @scope/pkg instead",
            "replaced with @scope/pkg",
            "migrated to @scope/pkg",
            "now using @scope/pkg",
            "instead use @scope/pkg",
        ]
        for text in patterns:
            m = _MIGRATION_RE.search(text)
            self.assertIsNotNone(m, f"Pattern did not match: {text}")
            matched = next((g for g in m.groups() if g), None)
            self.assertIsNotNone(matched, f"No capture group matched: {text}")
            self.assertIn("scope", matched, f"@scope not captured in: {text}")


if __name__ == "__main__":
    unittest.main()
