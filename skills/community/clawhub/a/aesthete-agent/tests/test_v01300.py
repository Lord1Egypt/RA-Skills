# -*- coding: utf-8 -*-
"""0.13.0 回归:排版引擎(typography-system 法则 + typescale v2 流体/底座/字距令牌 + audit 排印检查)。"""
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import type_kit  # noqa: E402
import page_audit  # noqa: E402

DP = ["01161E", "124559", "598392", "AEC3B0", "EFF6E0"]


class TestTypescaleV2(unittest.TestCase):
    """流体字阶 + 排印底座 + 字距令牌。"""

    def test_fluid_clamp_math(self):
        tokens, checks = type_kit.build(16.0, 1.25, 12.0, fluid=True)
        self.assertEqual(checks["verdict"], "PASS")
        f = tokens["3xl"].get("fluid", "")
        self.assertTrue(f.startswith("clamp(") and "vw" in f, f)
        # 固定级(base/sm/xs)不发流体
        self.assertNotIn("fluid", tokens["base"])
        # 非 fluid 模式无该键
        t2, _ = type_kit.build(16.0, 1.25, 12.0)
        self.assertNotIn("fluid", t2["3xl"])

    def test_emit_base_and_track_tokens(self):
        with tempfile.TemporaryDirectory() as td:
            base = os.path.join(td, "type")
            type_kit.emit("夜松", base=16.0, ratio=1.25, out_base=base, fluid=True)
            css = open(base + ".css", encoding="utf-8").read()
            self.assertIn("--text-3xl:clamp(", css)
            self.assertIn("text-autospace:normal", css)
            self.assertIn("line-break:strict", css)
            self.assertIn("text-wrap:balance", css)
            self.assertIn("text-wrap:pretty", css)
            self.assertIn('"palt" 1', css)
            self.assertIn("--track-display:-0.02em;", css)
            self.assertIn("--track-caps:0.1em;", css)
            self.assertIn("--track-zh-display:0.01em;", css)
            j = __import__("json").load(open(base + ".json", encoding="utf-8"))
            self.assertTrue(j["fluid"])


class TestAuditTypography(unittest.TestCase):
    """排印检查:中文负字距 / display 行高松弛(双向)。"""

    def test_negative_tracking_flagged(self):
        html = ('<!doctype html><html lang="zh-CN"><style>'
                'h1{letter-spacing:-0.02em}</style><h1>标题</h1></html>')
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "t.html")
            with open(p, "w", encoding="utf-8") as f:
                f.write(html)
            findings = page_audit.run(p, DP)["findings"]
        checks = {f["check"] for f in findings}
        self.assertIn("cjk_negative_tracking", checks)

    def test_display_line_height_flagged(self):
        html = ('<!doctype html><html lang="zh-CN"><style>'
                'h1{font-size:44px;line-height:1.6}</style><h1>标题</h1></html>')
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "t.html")
            with open(p, "w", encoding="utf-8") as f:
                f.write(html)
            findings = page_audit.run(p, DP)["findings"]
        self.assertIn("display_line_height", {f["check"] for f in findings})

    def test_good_typography_clean(self):
        html = ('<!doctype html><html lang="zh-CN"><style>'
                'h1{font-size:44px;line-height:1.12}p{letter-spacing:0.01em}'
                '</style><h1>标题</h1><p>正文</p></html>')
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "t.html")
            with open(p, "w", encoding="utf-8") as f:
                f.write(html)
            findings = page_audit.run(p, DP)["findings"]
        typo = [f for f in findings if f["check"] in ("cjk_negative_tracking", "display_line_height")]
        self.assertEqual(typo, [])


class TestTypographyDoc(unittest.TestCase):
    """排印法则文档:三行块头 + 规则数 + 验收清单(preflight C6 同源结构)。"""

    def test_doc_structure(self):
        doc = open(os.path.join(ROOT, "references", "typography-system.md"), encoding="utf-8").read()
        self.assertIn("何时读我", doc)
        self.assertIn("验收清单", doc)
        for kw in ("text-autospace", "text-wrap: balance", "letter-spacing",
                   "tabular-nums", "font-weight: 200 900", "palt"):
            self.assertIn(kw, doc)


if __name__ == "__main__":
    unittest.main()
