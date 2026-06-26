#!/usr/bin/env python3
"""钉钉表格 Skill 的安全与辅助函数测试。"""

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import create_sheet
import export_sheet
import import_sheet
import mcporter_utils


class TestResolveSafePath(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(__file__).parent.resolve()
        self.allowed_file = self.test_dir / "allowed.csv"

    def test_path_traversal_attack(self):
        old_env = os.environ.get("OPENCLAW_WORKSPACE")
        try:
            os.environ["OPENCLAW_WORKSPACE"] = str(self.test_dir)
            with self.assertRaises(ValueError):
                import_sheet.resolve_safe_path("../etc/passwd")
        finally:
            if old_env:
                os.environ["OPENCLAW_WORKSPACE"] = old_env
            else:
                os.environ.pop("OPENCLAW_WORKSPACE", None)

    def test_absolute_path_outside_root(self):
        old_env = os.environ.get("OPENCLAW_WORKSPACE")
        try:
            os.environ["OPENCLAW_WORKSPACE"] = str(self.test_dir)
            with self.assertRaises(ValueError):
                import_sheet.resolve_safe_path("/etc/passwd")
        finally:
            if old_env:
                os.environ["OPENCLAW_WORKSPACE"] = old_env
            else:
                os.environ.pop("OPENCLAW_WORKSPACE", None)

    def test_relative_path_within_root(self):
        old_env = os.environ.get("OPENCLAW_WORKSPACE")
        old_cwd = os.getcwd()
        try:
            os.environ["OPENCLAW_WORKSPACE"] = str(self.test_dir)
            os.chdir(self.test_dir)
            result = import_sheet.resolve_safe_path("allowed.csv")
            self.assertEqual(result, self.allowed_file)
        finally:
            os.chdir(old_cwd)
            if old_env:
                os.environ["OPENCLAW_WORKSPACE"] = old_env
            else:
                os.environ.pop("OPENCLAW_WORKSPACE", None)


class TestFileExtensionValidation(unittest.TestCase):
    def test_allowed_extensions(self):
        for ext in [".csv", ".tsv"]:
            self.assertTrue(import_sheet.validate_file_extension(f"test{ext}"))

    def test_case_insensitive(self):
        self.assertTrue(import_sheet.validate_file_extension("test.CSV"))
        self.assertTrue(import_sheet.validate_file_extension("test.TSV"))

    def test_disallowed_extensions(self):
        for ext in [".exe", ".sh", ".py", ".md"]:
            self.assertFalse(import_sheet.validate_file_extension(f"test{ext}"))


class TestFileSizeValidation(unittest.TestCase):
    def test_small_file(self):
        small_file = Mock()
        small_file.stat.return_value.st_size = 1024
        self.assertTrue(import_sheet.validate_file_size(small_file))

    def test_large_file(self):
        large_file = Mock()
        large_file.stat.return_value.st_size = 11 * 1024 * 1024
        self.assertFalse(import_sheet.validate_file_size(large_file))


class TestNodeUrlValidation(unittest.TestCase):
    def test_valid_url(self):
        result = export_sheet.extract_node_uuid(
            "https://alidocs.dingtalk.com/i/nodes/DnRL6jAJMNX9kAgycoLy2vOo8yMoPYe1"
        )
        self.assertEqual(result, "DnRL6jAJMNX9kAgycoLy2vOo8yMoPYe1")

    def test_invalid_urls(self):
        invalid = [
            "not a url",
            "http://alidocs.dingtalk.com/i/nodes/abc123",
            "https://alidocs.dingtalk.com/i/nodes/",
            "https://alidocs.dingtalk.com/i/nodes/abc 123",
            "https://evil.com/i/nodes/abc123",
        ]
        for url in invalid:
            self.assertIsNone(export_sheet.extract_node_uuid(url), f"应该无效：{url}")


class TestParseResponse(unittest.TestCase):
    def test_flat_response(self):
        output = '{"nodeId": "abc123"}'
        result = create_sheet.parse_response(output)
        self.assertEqual(result, {"nodeId": "abc123"})

    def test_nested_result(self):
        output = '{"success": true, "result": {"sheetId": "sheet_1", "name": "Sheet1"}}'
        result = create_sheet.parse_response(output)
        self.assertEqual(result["sheetId"], "sheet_1")
        self.assertEqual(result["name"], "Sheet1")

    def test_invalid_json(self):
        self.assertIsNone(create_sheet.parse_response("not json"))


class TestRunMcporter(unittest.TestCase):
    def test_function_signature(self):
        import inspect

        sig = inspect.signature(create_sheet.run_mcporter)
        params = list(sig.parameters.keys())
        self.assertEqual(params[0], "tool")
        self.assertEqual(params[1], "args")
        self.assertEqual(params[2], "timeout")

    def test_consistent_signatures(self):
        import inspect

        sig_create = list(inspect.signature(create_sheet.run_mcporter).parameters.keys())
        sig_import = list(inspect.signature(import_sheet.run_mcporter).parameters.keys())
        sig_export = list(inspect.signature(export_sheet.run_mcporter).parameters.keys())
        self.assertEqual(sig_create, sig_import)
        self.assertEqual(sig_create, sig_export)


class TestSheetHelpers(unittest.TestCase):
    def test_matrix_range_address(self):
        self.assertEqual(mcporter_utils.matrix_range_address(3, 2), "A1:B3")
        self.assertEqual(mcporter_utils.matrix_range_address(1, 27), "A1:AA1")

    def test_normalize_table(self):
        rows = [["a", "b"], ["c"]]
        self.assertEqual(mcporter_utils.normalize_table(rows), [["a", "b"], ["c", ""]])

    def test_detect_delimiter(self):
        self.assertEqual(import_sheet.detect_delimiter(Path("data.csv")), ",")
        self.assertEqual(import_sheet.detect_delimiter(Path("data.tsv")), "\t")


class TestLimits(unittest.TestCase):
    def test_import_limits(self):
        self.assertEqual(import_sheet.MAX_ROWS, 5000)
        self.assertEqual(import_sheet.MAX_COLUMNS, 200)

    def test_export_limits(self):
        self.assertEqual(export_sheet.MAX_EXPORT_ROWS, 10000)
        self.assertEqual(export_sheet.MAX_EXPORT_COLUMNS, 500)


if __name__ == "__main__":
    unittest.main(verbosity=2)
