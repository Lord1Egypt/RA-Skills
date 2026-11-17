# -*- coding: utf-8 -*-
"""0.18.0 回归(先行):字体资产管线(preset/auto/假粗禁令)。"""
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import font_kit  # noqa: E402
import page_audit  # noqa: E402

PAGE = "<html lang=\"zh-CN\"><head><style>body{--serif:'Noto Serif SC',serif}h1{font:900 40px/1.1 var(--serif)}</style></head><body><h1>夜松巨标</h1></body></html>"


class TestFontKit(unittest.TestCase):

    def test_none_noop(self):
        with tempfile.TemporaryDirectory() as td:
            html, copied = font_kit.emit_faces(td, "none", PAGE)
            self.assertEqual(copied, [])
            self.assertNotIn("Aesthete Serif", html)

    def test_preset(self):
        with tempfile.TemporaryDirectory() as td:
            html, copied = font_kit.emit_faces(td, "preset", PAGE)
            self.assertGreaterEqual(len(copied), 1, "preset 未落盘")
            for c in copied:
                self.assertTrue(os.path.exists(c))
                self.assertLess(os.path.getsize(c), 300_000)
            self.assertIn('@font-face{font-family:"Aesthete Serif"', html)
            self.assertIn("--serif:'Aesthete Serif'", html)
            self.assertIn('font-weight:900', html)

    def test_auto_subset(self):
        try:
            import fontTools  # noqa: F401
        except ImportError:
            self.skipTest("fonttools 未安装")
        if font_kit.find_vf() is None:
            self.skipTest("本机无思源宋 VF 源")
        with tempfile.TemporaryDirectory() as td:
            html, copied = font_kit.emit_faces(td, "auto", PAGE)
            self.assertEqual(len(copied), 1)
            w = os.path.getsize(copied[0])
            self.assertGreater(w, 1000)
            self.assertLess(w, 400_000, f"auto 子集过大: {w}")
            self.assertIn("page-serif-900.woff2", html)

    def test_collect_chars(self):
        chars = font_kit.collect_chars(PAGE)
        self.assertIn("夜", chars)
        self.assertIn("标", chars)


class TestFakeBoldLint(unittest.TestCase):

    def test_fake_bold_flagged(self):
        page = ('<html lang="zh-CN"><head><style>h1{font:900 40px/1.1 sans-serif}</style></head>'
                '<body><h1>标题</h1></body></html>')
        findings, _ = page_audit.audit_page(page, None, 12)
        self.assertIn("fake_bold", {f["check"] for f in findings})

    def test_real_weight_clean(self):
        page = ('<html lang="zh-CN"><head><style>@font-face{font-family:"X";src:url(x.woff2);'
                'font-weight:900}h1{font:900 40px/1.1 "X"}</style></head><body><h1>标题</h1></body></html>')
        findings, _ = page_audit.audit_page(page, None, 12)
        self.assertNotIn("fake_bold", {f["check"] for f in findings})


if __name__ == "__main__":
    unittest.main()
