"""Tests for minified file exclusion and generic symbol filtering (R1, R3)."""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts", "lib"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from usage_scanner import _is_minified, SKIP_DIRS, _GENERIC_SYMBOLS


class TestIsMinified(unittest.TestCase):
    def test_min_js_returns_true(self):
        self.assertTrue(_is_minified("hls.min.js"))

    def test_min_css_returns_true(self):
        self.assertTrue(_is_minified("styles.min.css"))

    def test_min_mjs_returns_true(self):
        self.assertTrue(_is_minified("bundle.min.mjs"))

    def test_bundle_js_returns_true(self):
        self.assertTrue(_is_minified("app.bundle.js"))

    def test_chunk_js_returns_true(self):
        self.assertTrue(_is_minified("main.chunk.js"))

    def test_regular_js_returns_false(self):
        self.assertFalse(_is_minified("app.js"))

    def test_regular_ts_returns_false(self):
        self.assertFalse(_is_minified("components.ts"))

    def test_path_with_dir_min_js(self):
        self.assertTrue(_is_minified("public/js/hls.min.js"))

    def test_case_insensitive(self):
        self.assertTrue(_is_minified("VENDOR.MIN.JS"))


class TestSkipDirs(unittest.TestCase):
    def test_public_in_skip_dirs(self):
        self.assertIn("public", SKIP_DIRS)

    def test_static_in_skip_dirs(self):
        self.assertIn("static", SKIP_DIRS)

    def test_assets_in_skip_dirs(self):
        self.assertIn("assets", SKIP_DIRS)

    def test_wwwroot_in_skip_dirs(self):
        self.assertIn("wwwroot", SKIP_DIRS)

    def test_media_in_skip_dirs(self):
        self.assertIn("media", SKIP_DIRS)

    def test_node_modules_still_in_skip_dirs(self):
        self.assertIn("node_modules", SKIP_DIRS)


class TestGenericSymbols(unittest.TestCase):
    def test_client_in_generic_symbols(self):
        self.assertIn("Client", _GENERIC_SYMBOLS)

    def test_config_in_generic_symbols(self):
        self.assertIn("Config", _GENERIC_SYMBOLS)

    def test_request_in_generic_symbols(self):
        self.assertIn("Request", _GENERIC_SYMBOLS)

    def test_response_in_generic_symbols(self):
        self.assertIn("Response", _GENERIC_SYMBOLS)

    def test_handler_in_generic_symbols(self):
        self.assertIn("Handler", _GENERIC_SYMBOLS)

    def test_specific_symbol_not_generic(self):
        self.assertNotIn("constructEvent", _GENERIC_SYMBOLS)

    def test_webhook_not_generic(self):
        self.assertNotIn("Webhook", _GENERIC_SYMBOLS)

    def test_python_lowercase_client(self):
        self.assertIn("client", _GENERIC_SYMBOLS)


class TestMinifiedFileSkippedInScan(unittest.TestCase):
    def test_minified_file_appears_in_skipped(self):
        """scan_project should skip .min.js files and list them in skipped."""
        from usage_scanner import scan_project
        from schema import BreakingChange

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a .min.js file with content that would otherwise match
            min_file = os.path.join(tmpdir, "vendor.min.js")
            with open(min_file, "w") as f:
                f.write("var constructEvent = function() {};\n" * 100)

            bc = BreakingChange(
                symbol="constructEvent",
                change_type="removed",
                description="constructEvent removed",
                old_signature=None,
                new_signature=None,
                migration_note=None,
                source="test",
                confidence="high",
            )
            results, skipped = scan_project([bc], tmpdir, ecosystem="npm")
            # The min file should be in skipped, not in results
            skipped_paths = [s.split(":")[0] for s in skipped]
            self.assertTrue(
                any("vendor.min.js" in s for s in skipped),
                f"vendor.min.js not in skipped: {skipped}"
            )


if __name__ == "__main__":
    unittest.main()
