#!/usr/bin/env python3
"""安全功能测试用例（v0.2.0 — 适配 --args JSON 传参）"""

import sys
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

import create_doc
import import_docs
import export_docs


class TestResolveSafePath(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp()).resolve()
        self.allowed_file = self.test_dir / "allowed.md"
        self.allowed_file.write_text('# Test')

    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_path_traversal_attack(self):
        """目录遍历攻击 - 应拒绝"""
        old_env = os.environ.get('OPENCLAW_WORKSPACE')
        try:
            os.environ['OPENCLAW_WORKSPACE'] = str(self.test_dir)
            with self.assertRaises(ValueError):
                import_docs.resolve_safe_path("../etc/passwd")
        finally:
            if old_env:
                os.environ['OPENCLAW_WORKSPACE'] = old_env
            else:
                os.environ.pop('OPENCLAW_WORKSPACE', None)

    def test_absolute_path_outside_root(self):
        """绝对路径超出允许范围 - 应拒绝"""
        old_env = os.environ.get('OPENCLAW_WORKSPACE')
        try:
            os.environ['OPENCLAW_WORKSPACE'] = str(self.test_dir)
            with self.assertRaises(ValueError):
                import_docs.resolve_safe_path("/etc/passwd")
        finally:
            if old_env:
                os.environ['OPENCLAW_WORKSPACE'] = old_env
            else:
                os.environ.pop('OPENCLAW_WORKSPACE', None)

    def test_relative_path_within_root(self):
        """相对路径在允许范围内 - 应通过"""
        old_env = os.environ.get('OPENCLAW_WORKSPACE')
        old_cwd = os.getcwd()
        try:
            os.environ['OPENCLAW_WORKSPACE'] = str(self.test_dir)
            os.chdir(self.test_dir)
            result = import_docs.resolve_safe_path("allowed.md")
            self.assertEqual(result, self.allowed_file)
        finally:
            os.chdir(old_cwd)
            if old_env:
                os.environ['OPENCLAW_WORKSPACE'] = old_env
            else:
                os.environ.pop('OPENCLAW_WORKSPACE', None)


class TestFileExtensionValidation(unittest.TestCase):
    def test_allowed_extensions(self):
        for ext in ['.md', '.txt', '.markdown']:
            self.assertTrue(
                import_docs.validate_file_extension(f"test{ext}"),
                f"{ext} 应该被允许"
            )

    def test_case_insensitive(self):
        self.assertTrue(import_docs.validate_file_extension("test.MD"))
        self.assertTrue(import_docs.validate_file_extension("test.TXT"))

    def test_disallowed_extensions(self):
        for ext in ['.exe', '.sh', '.py', '.pdf']:
            self.assertFalse(
                import_docs.validate_file_extension(f"test{ext}"),
                f"{ext} 不应该被允许"
            )


class TestFileSizeValidation(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp()).resolve()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_small_file(self):
        small_file = self.test_dir / "small.md"
        small_file.write_text("# Small")
        self.assertTrue(import_docs.validate_file_size(small_file))

    def test_large_file(self):
        large_file = self.test_dir / "large.md"
        with open(large_file, 'w') as f:
            f.write('x' * (11 * 1024 * 1024))
        self.assertFalse(import_docs.validate_file_size(large_file))


class TestDocUrlValidation(unittest.TestCase):
    def test_valid_url(self):
        """有效 URL 应提取出 UUID"""
        result = export_docs.extract_doc_uuid(
            "https://alidocs.dingtalk.com/i/nodes/DnRL6jAJMNX9kAgycoLy2vOo8yMoPYe1"
        )
        self.assertEqual(result, "DnRL6jAJMNX9kAgycoLy2vOo8yMoPYe1")

    def test_invalid_urls(self):
        """无效 URL 应返回 None"""
        invalid = [
            "not a url",
            "http://alidocs.dingtalk.com/i/nodes/abc123",   # http 非 https
            "https://alidocs.dingtalk.com/i/nodes/",        # 空 ID
            "https://alidocs.dingtalk.com/i/nodes/abc 123", # 含空格
            "https://evil.com/i/nodes/abc123",              # 错误域名
        ]
        for url in invalid:
            result = export_docs.extract_doc_uuid(url)
            self.assertIsNone(result, f"应该无效：{url}")


class TestParseResponse(unittest.TestCase):
    """测试 parse_response 处理嵌套 result 结构"""

    def test_flat_response(self):
        """顶层直接返回的情况"""
        output = '{"rootDentryUuid": "abc123"}'
        result = create_doc.parse_response(output)
        self.assertEqual(result, {"rootDentryUuid": "abc123"})

    def test_nested_result(self):
        """嵌套 result 的情况（create_doc 实际返回格式）"""
        output = '{"success": true, "result": {"dentryUuid": "xyz", "pcUrl": "https://..."}}'
        result = create_doc.parse_response(output)
        self.assertEqual(result["dentryUuid"], "xyz")
        self.assertEqual(result["pcUrl"], "https://...")

    def test_invalid_json(self):
        """非法 JSON 应返回 None"""
        result = create_doc.parse_response("not json")
        self.assertIsNone(result)


class TestRunMcporter(unittest.TestCase):
    """测试 run_mcporter 函数签名和超时"""

    def test_function_signature(self):
        """验证 run_mcporter 接受 (tool, args, timeout) 签名"""
        import inspect
        sig = inspect.signature(create_doc.run_mcporter)
        params = list(sig.parameters.keys())
        self.assertEqual(params[0], 'tool')
        self.assertEqual(params[1], 'args')
        self.assertEqual(params[2], 'timeout')

    def test_consistent_signatures(self):
        """三个脚本的 run_mcporter 签名一致"""
        import inspect
        sig_create = list(inspect.signature(create_doc.run_mcporter).parameters.keys())
        sig_import = list(inspect.signature(import_docs.run_mcporter).parameters.keys())
        sig_export = list(inspect.signature(export_docs.run_mcporter).parameters.keys())
        self.assertEqual(sig_create, sig_import)
        self.assertEqual(sig_create, sig_export)


class TestContentLimits(unittest.TestCase):
    """测试内容长度常量"""

    def test_create_doc_limit(self):
        self.assertEqual(create_doc.MAX_CONTENT_LENGTH, 50000)

    def test_import_docs_limit(self):
        self.assertEqual(import_docs.MAX_CONTENT_LENGTH, 50000)

    def test_export_docs_limit(self):
        self.assertEqual(export_docs.MAX_CONTENT_LENGTH, 100000)


if __name__ == '__main__':
    unittest.main(verbosity=2)
