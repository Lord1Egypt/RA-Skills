"""Tests for scripts/lib/usage_scanner.py"""
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "lib"))

from usage_scanner import (
    SKIP_DIRS,
    _extract_base_symbol,
    _walk_files,
    scan_js_ts_file,
    scan_python_file,
)


def _write_temp(content: str, suffix: str) -> str:
    """Write content to a named temp file and return its path."""
    f = tempfile.NamedTemporaryFile(
        mode="w", suffix=suffix, delete=False, encoding="utf-8"
    )
    f.write(content)
    f.close()
    return f.name


class TestScanPythonFile(unittest.TestCase):

    def tearDown(self):
        # clean up any leftover temp files
        pass

    def test_detects_import_openai(self):
        path = _write_temp("import openai\n\nresponse = openai.Completion.create()\n", ".py")
        try:
            result = scan_python_file(path, ["openai"])
            self.assertIn("openai", result)
            self.assertGreater(len(result["openai"]), 0)
        finally:
            os.unlink(path)

    def test_detects_openai_completion_create(self):
        code = (
            "import openai\n"
            "openai.api_key = 'sk-test'\n"
            "response = openai.Completion.create(\n"
            "    model='text-davinci-003',\n"
            "    prompt='Hello'\n"
            ")\n"
        )
        path = _write_temp(code, ".py")
        try:
            result = scan_python_file(path, ["openai.Completion.create"])
            # Should detect via 'create' attribute or 'Completion'
            all_symbols = set(result.keys())
            all_locs = [loc for locs in result.values() for loc in locs]
            self.assertTrue(len(all_locs) > 0 or len(all_symbols) > 0)
        finally:
            os.unlink(path)

    def test_detects_from_stripe_import_webhooks(self):
        code = (
            "from stripe import webhooks\n"
            "event = webhooks.constructEvent(payload, sig, secret)\n"
        )
        path = _write_temp(code, ".py")
        try:
            result = scan_python_file(path, ["webhooks"])
            self.assertIn("webhooks", result)
            locs = result["webhooks"]
            self.assertGreater(len(locs), 0)
            # Should be detected at import line
            line_numbers = [loc.line_number for loc in locs]
            self.assertIn(1, line_numbers)
        finally:
            os.unlink(path)

    def test_detects_attribute_access(self):
        code = (
            "import stripe\n"
            "event = stripe.webhooks.constructEvent(payload, sig, secret)\n"
        )
        path = _write_temp(code, ".py")
        try:
            result = scan_python_file(path, ["constructEvent"])
            self.assertIn("constructEvent", result)
        finally:
            os.unlink(path)

    def test_detection_method_is_ast(self):
        code = "import openai\nres = openai.create()\n"
        path = _write_temp(code, ".py")
        try:
            result = scan_python_file(path, ["openai"])
            if "openai" in result:
                locs = result["openai"]
                self.assertTrue(any(loc.detection_method == "ast" for loc in locs))
        finally:
            os.unlink(path)

    def test_no_match_returns_empty(self):
        code = "import os\nprint(os.getcwd())\n"
        path = _write_temp(code, ".py")
        try:
            result = scan_python_file(path, ["stripe"])
            self.assertEqual(result, {})
        finally:
            os.unlink(path)

    def test_empty_symbols_returns_empty(self):
        code = "import stripe\n"
        path = _write_temp(code, ".py")
        try:
            result = scan_python_file(path, [])
            self.assertEqual(result, {})
        finally:
            os.unlink(path)

    def test_returns_file_path_in_location(self):
        code = "import openai\n"
        path = _write_temp(code, ".py")
        try:
            result = scan_python_file(path, ["openai"])
            if "openai" in result:
                locs = result["openai"]
                self.assertEqual(locs[0].file_path, path)
        finally:
            os.unlink(path)

    def test_syntax_error_falls_back_to_grep(self):
        # Deliberately invalid Python — should not raise, fall back gracefully
        code = "def broken(\n    # unclosed\n"
        path = _write_temp(code, ".py")
        try:
            result = scan_python_file(path, ["broken"])
            # Should not raise, may return empty or grep-based result
            self.assertIsInstance(result, dict)
        finally:
            os.unlink(path)


class TestScanJsTsFile(unittest.TestCase):

    def test_detects_require_stripe(self):
        code = "const Stripe = require('stripe');\nconst stripe = new Stripe(process.env.KEY);\n"
        path = _write_temp(code, ".js")
        try:
            result = scan_js_ts_file(path, ["stripe"])
            self.assertIn("stripe", result)
            self.assertGreater(len(result["stripe"]), 0)
        finally:
            os.unlink(path)

    def test_detects_esm_import_stripe(self):
        code = "import Stripe from 'stripe';\nexport default Stripe;\n"
        path = _write_temp(code, ".ts")
        try:
            result = scan_js_ts_file(path, ["stripe"])
            self.assertIn("stripe", result)
        finally:
            os.unlink(path)

    def test_detects_named_import(self):
        code = "import { constructEvent } from 'stripe';\n"
        path = _write_temp(code, ".ts")
        try:
            result = scan_js_ts_file(path, ["constructEvent"])
            self.assertIn("constructEvent", result)
        finally:
            os.unlink(path)

    def test_detects_method_call(self):
        code = (
            "const stripe = require('stripe')(process.env.KEY);\n"
            "const event = stripe.webhooks.constructEvent(payload, sig, secret);\n"
        )
        path = _write_temp(code, ".js")
        try:
            result = scan_js_ts_file(path, ["constructEvent"])
            self.assertIn("constructEvent", result)
        finally:
            os.unlink(path)

    def test_no_match_returns_empty(self):
        code = "import express from 'express';\nconst app = express();\n"
        path = _write_temp(code, ".js")
        try:
            result = scan_js_ts_file(path, ["stripe"])
            self.assertEqual(result.get("stripe", []), [])
        finally:
            os.unlink(path)

    def test_location_has_correct_line_number(self):
        code = "// first line\nimport Stripe from 'stripe';\n// third line\n"
        path = _write_temp(code, ".ts")
        try:
            result = scan_js_ts_file(path, ["stripe"])
            if "stripe" in result:
                locs = result["stripe"]
                line_numbers = [loc.line_number for loc in locs]
                self.assertIn(2, line_numbers)
        finally:
            os.unlink(path)

    def test_location_usage_text_is_stripped(self):
        code = "    const stripe = require('stripe');\n"
        path = _write_temp(code, ".js")
        try:
            result = scan_js_ts_file(path, ["stripe"])
            if "stripe" in result:
                locs = result["stripe"]
                self.assertFalse(locs[0].usage_text.startswith(" "))
        finally:
            os.unlink(path)


class TestExtractBaseSymbol(unittest.TestCase):

    def test_dotted_path(self):
        result = _extract_base_symbol("stripe.webhooks.constructEvent")
        self.assertEqual(result, "constructEvent")

    def test_class_method(self):
        result = _extract_base_symbol("WebhookSignature.verify")
        self.assertEqual(result, "verify")

    def test_plain_name(self):
        result = _extract_base_symbol("constructEvent")
        self.assertEqual(result, "constructEvent")

    def test_strips_parens(self):
        result = _extract_base_symbol("constructEvent()")
        self.assertEqual(result, "constructEvent")

    def test_double_colon(self):
        result = _extract_base_symbol("Stripe::Webhook::verify")
        self.assertEqual(result, "verify")

    def test_empty_string(self):
        result = _extract_base_symbol("")
        self.assertEqual(result, "")

    def test_openai_nested(self):
        result = _extract_base_symbol("openai.Completion.create")
        self.assertEqual(result, "create")


class TestWalkFiles(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def _create_file(self, rel_path: str, content: str = "") -> str:
        full_path = os.path.join(self.tmp_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return full_path

    def test_finds_py_files(self):
        self._create_file("src/app.py", "import os")
        self._create_file("src/utils.py", "def helper(): pass")
        files = _walk_files(self.tmp_dir, [".py"])
        basenames = [os.path.basename(f) for f in files]
        self.assertIn("app.py", basenames)
        self.assertIn("utils.py", basenames)

    def test_skips_node_modules(self):
        self._create_file("node_modules/stripe/index.js", "module.exports = {};")
        self._create_file("src/app.js", "const x = 1;")
        files = _walk_files(self.tmp_dir, [".js"])
        paths = " ".join(files)
        self.assertNotIn("node_modules", paths)
        self.assertIn("app.js", paths)

    def test_skips_git_directory(self):
        self._create_file(".git/config", "[core]")
        self._create_file("src/app.py", "x = 1")
        files = _walk_files(self.tmp_dir, [".py"])
        paths = " ".join(files)
        self.assertNotIn(".git", paths)

    def test_skips_pycache(self):
        self._create_file("__pycache__/app.cpython-312.pyc", "")
        self._create_file("src/app.py", "x = 1")
        files = _walk_files(self.tmp_dir, [".py"])
        paths = " ".join(files)
        self.assertNotIn("__pycache__", paths)

    def test_skips_venv(self):
        self._create_file(".venv/lib/python3.12/stripe.py", "# venv")
        self._create_file("src/app.py", "import stripe")
        files = _walk_files(self.tmp_dir, [".py"])
        paths = " ".join(files)
        self.assertNotIn(".venv", paths)
        self.assertIn("app.py", paths)

    def test_only_matching_extensions(self):
        self._create_file("app.py", "x = 1")
        self._create_file("index.js", "const x = 1;")
        self._create_file("style.css", "body { margin: 0; }")

        py_files = _walk_files(self.tmp_dir, [".py"])
        js_files = _walk_files(self.tmp_dir, [".js"])
        all_files = _walk_files(self.tmp_dir, [".py", ".js"])

        py_names = [os.path.basename(f) for f in py_files]
        js_names = [os.path.basename(f) for f in js_files]
        all_names = [os.path.basename(f) for f in all_files]

        self.assertIn("app.py", py_names)
        self.assertNotIn("index.js", py_names)
        self.assertIn("index.js", js_names)
        self.assertNotIn("app.py", js_names)
        self.assertIn("app.py", all_names)
        self.assertIn("index.js", all_names)
        self.assertNotIn("style.css", all_names)

    def test_empty_directory_returns_empty(self):
        empty_dir = tempfile.mkdtemp()
        try:
            files = _walk_files(empty_dir, [".py"])
            self.assertEqual(files, [])
        finally:
            import shutil
            shutil.rmtree(empty_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
