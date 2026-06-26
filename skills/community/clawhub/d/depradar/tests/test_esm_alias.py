"""Tests for ESM import alias generation in detect_esm_cjs_transition().

Covers Fix 1 from changes3.txt: package[0] was taking the first *character*
of the package name as the import alias, producing `import @ from '@noble/hashes'`
(invalid JS) for scoped packages.
"""
import re
import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "lib"))
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


# ── Helper: the alias logic extracted for unit testing ────────────────────────

def _esm_alias(package: str) -> str:
    """Mirror of the alias derivation in detect_esm_cjs_transition."""
    pkg_base = package.lstrip("@").split("/")[-1]
    return re.sub(r"-([a-zA-Z])", lambda m: m.group(1).upper(), pkg_base)


# ── Unit tests for the alias formula ─────────────────────────────────────────

class TestEsmAliasFormula(unittest.TestCase):

    def test_scoped_package_alias_is_base_name(self):
        """@noble/hashes → hashes (not '@')."""
        self.assertEqual(_esm_alias("@noble/hashes"), "hashes")

    def test_angular_core_alias(self):
        """@angular/core → core."""
        self.assertEqual(_esm_alias("@angular/core"), "core")

    def test_unscoped_alias_unchanged(self):
        """chalk → chalk."""
        self.assertEqual(_esm_alias("chalk"), "chalk")

    def test_kebab_case_to_camel(self):
        """react-dom → reactDom."""
        self.assertEqual(_esm_alias("react-dom"), "reactDom")

    def test_node_fetch_alias(self):
        """node-fetch → nodeFetch."""
        self.assertEqual(_esm_alias("node-fetch"), "nodeFetch")

    def test_scoped_kebab_package(self):
        """@scope/my-pkg → myPkg."""
        self.assertEqual(_esm_alias("@scope/my-pkg"), "myPkg")

    def test_double_scoped_path(self):
        """@google/generative-ai → generativeAi."""
        self.assertEqual(_esm_alias("@google/generative-ai"), "generativeAi")

    def test_single_word_unscoped_unchanged(self):
        """lodash → lodash."""
        self.assertEqual(_esm_alias("lodash"), "lodash")

    def test_alias_never_starts_with_at(self):
        """No scoped package produces an alias starting with '@'."""
        for pkg in ["@noble/hashes", "@angular/core", "@my-org/my-lib"]:
            alias = _esm_alias(pkg)
            self.assertFalse(
                alias.startswith("@"),
                f"Alias for {pkg!r} starts with '@': {alias!r}",
            )

    def test_alias_is_valid_js_identifier(self):
        """Alias must match [a-zA-Z][a-zA-Z0-9]* (valid JS identifier)."""
        valid_id = re.compile(r"^[a-zA-Z_$][a-zA-Z0-9_$]*$")
        packages = [
            "@noble/hashes", "chalk", "react-dom", "node-fetch",
            "@angular/core", "@scope/my-pkg", "lodash",
        ]
        for pkg in packages:
            alias = _esm_alias(pkg)
            self.assertRegex(
                alias, valid_id,
                f"Alias {alias!r} for {pkg!r} is not a valid JS identifier",
            )


# ── Integration tests: detect_esm_cjs_transition() produces correct note ─────

class TestEsmMigrationNote(unittest.TestCase):

    def _call_detect(self, package: str):
        """Call detect_esm_cjs_transition with mocked manifests."""
        import importlib
        npm_mod = importlib.import_module("npm_registry")

        old_manifest = {"type": "commonjs"}
        new_manifest = {"type": "module"}   # ESM-only, no CJS compat

        with patch.object(npm_mod, "fetch_version_manifest") as mock_fetch:
            mock_fetch.side_effect = [old_manifest, new_manifest]
            result = npm_mod.detect_esm_cjs_transition(
                package, old_version="1.0.0", new_version="2.0.0"
            )
        return result

    def test_migration_note_not_empty(self):
        bc = self._call_detect("chalk")
        self.assertIsNotNone(bc)
        self.assertTrue(bc.migration_note)

    def test_migration_note_no_at_symbol_in_import(self):
        """The migration note must NOT contain `import @` (the old broken pattern)."""
        bc = self._call_detect("@noble/hashes")
        self.assertIsNotNone(bc)
        self.assertNotIn("import @", bc.migration_note)

    def test_migration_note_contains_correct_alias(self):
        """The alias in the note is 'hashes', not '@' or 'n'."""
        bc = self._call_detect("@noble/hashes")
        self.assertIsNotNone(bc)
        self.assertIn("hashes", bc.migration_note)

    def test_migration_note_contains_dynamic_import_hint(self):
        """Migration note should mention dynamic import() as a CJS/ESM bridge."""
        bc = self._call_detect("chalk")
        self.assertIsNotNone(bc)
        self.assertIn("await import(", bc.migration_note)

    def test_migration_note_valid_for_react_dom(self):
        """react-dom → reactDom alias, no raw 'r' alias."""
        bc = self._call_detect("react-dom")
        self.assertIsNotNone(bc)
        self.assertIn("reactDom", bc.migration_note)
        self.assertNotIn("import r from", bc.migration_note)

    def test_no_breaking_change_when_cjs_compat_present(self):
        """If the new version provides a 'require' export, no breaking change."""
        import importlib
        npm_mod = importlib.import_module("npm_registry")

        old_manifest = {"type": "commonjs"}
        new_manifest = {
            "type": "module",
            "exports": {".": {"require": "./index.cjs", "import": "./index.mjs"}},
        }
        with patch.object(npm_mod, "fetch_version_manifest") as mock_fetch:
            mock_fetch.side_effect = [old_manifest, new_manifest]
            result = npm_mod.detect_esm_cjs_transition("chalk", "4.0.0", "5.0.0")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
