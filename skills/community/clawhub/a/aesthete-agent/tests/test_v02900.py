# -*- coding: utf-8 -*-
"""test_v02900 — 0.29.0 回归:默认即最佳·色彩。

Radix 12 角色对齐(官方 docs 口径)/文字步 APCA Lc 保证进派生器(60/90,high 75/95,
调墨到位不达即拒产)/OKLCH 感知坐标注释/color-mix(in oklab) 透明变体/--contrast 旋钮。"""
import io
import os
import re
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
SCRIPTS = os.path.join(ROOT, "scripts")
ENGINE = os.path.join(SCRIPTS, "palette_forge.py")
TMP = tempfile.mkdtemp(prefix="t290_")
PAL = "01161E,124559,598392,AEC3B0,EFF6E0"
sys.path.insert(0, SCRIPTS)

import token_sheet  # noqa: E402


def run(args):
    return subprocess.run([sys.executable, ENGINE] + args, capture_output=True,
                          text=True, encoding="utf-8", errors="replace")


class TestRadixRoles(unittest.TestCase):
    """12 步角色名对齐 Radix 官方(每步=具体 UI 角色)。"""

    def test_role_names_official(self):
        self.assertEqual(token_sheet.STEP_ROLES,
                         ["app-bg", "sub-bg", "el-bg", "el-hover-bg", "el-active-bg",
                          "border-subtle", "border", "border-hover",
                          "solid", "solid-hover", "text-low", "text-high"])

    def test_css_step_tokens_named_by_role(self):
        out = os.path.join(TMP, "tok")
        payload, rc = token_sheet.emit([h.upper() for h in PAL.split(",")],
                                       name="回归", out_base=out)
        self.assertEqual(rc, 0, payload["problems"])
        css = io.open(out + ".css", encoding="utf-8").read()
        self.assertIn("--step-01-app-bg:", css)
        self.assertIn("--step-09-solid:", css)          # Radix step9=实心钮
        self.assertIn("--step-11-text-low:", css)
        self.assertIn("--step-12-text-high:", css)
        self.assertNotIn("ink-deep", css)               # 旧口径已废

    def test_scale12_monotonic_light_to_dark(self):
        out = os.path.join(TMP, "tok2")
        token_sheet.emit([h.upper() for h in PAL.split(",")], name="回归", out_base=out)
        js = __import__("json").load(io.open(out + ".json", encoding="utf-8"))
        lums = [token_sheet._lum(h) for h in js["scale12"].values()]
        self.assertEqual(lums, sorted(lums, reverse=True), "step1 最浅→step12 最深")


class TestTextStepGuarantee(unittest.TestCase):
    """文字步保证进派生器:APCA Lc 60/90(对 step-2 底),high=75/95;不达即拒产。"""

    def test_standard_guarantee_measured(self):
        raw = token_sheet.scale12([h.upper() for h in PAL.split(",")])
        tuned, measured = token_sheet.tune_text_steps(raw)
        self.assertGreaterEqual(measured["text-low"], 60.0)
        self.assertGreaterEqual(measured["text-high"], 90.0)
        self.assertGreaterEqual(
            token_sheet._apca_lc(tuned[11], tuned[2]), 60.0)
        self.assertGreaterEqual(
            token_sheet._apca_lc(tuned[12], tuned[2]), 90.0)

    def test_high_contrast_stricter(self):
        out_s = os.path.join(TMP, "cs")
        out_h = os.path.join(TMP, "ch")
        ps, _ = token_sheet.emit([h.upper() for h in PAL.split(",")], out_base=out_s)
        ph, _ = token_sheet.emit([h.upper() for h in PAL.split(",")], out_base=out_h,
                                 contrast="high")
        self.assertGreaterEqual(ps["scale12_apca"]["text-low"], 60.0)  # 原映射色可已超标
        self.assertGreaterEqual(ph["scale12_apca"]["text-low"], 75.0)
        # text-high 理想 92 受底色物理上限约束(浅灰底纯黑≈94.9 上限),硬底线=90
        self.assertGreaterEqual(ph["scale12_apca"]["text-high"], 90.0)
        # 高档下正文字墨也更深(WCAG 7.0)
        self.assertGreaterEqual(ph["ratios"]["ink/bg"], ps["ratios"]["ink/bg"])

    def test_dark_text_floor_never_below_standard(self):
        """任何底色下,文字步硬底线 60/90 不可破——物理不可达理想值时降到底线以上。"""
        for pal in ("FAF3DD,D7AF70,937D64,585B56,251111",   # 暖浅底
                    "0F172A,1E293B,334155,94A3B8,E2E8F0"):  # 冷深板(浅端仍居首)
            raw = token_sheet.scale12([h.upper() for h in pal.split(",")])
            _, m = token_sheet.tune_text_steps(
                raw, {"text-low": 75.0, "text-high": 92.0})
            self.assertGreaterEqual(m["text-low"], 60.0, pal)
            self.assertGreaterEqual(m["text-high"], 90.0, pal)

    def test_apca_function_sanity(self):
        lc_black_white = token_sheet._apca_lc("000000", "FFFFFF")
        self.assertGreater(lc_black_white, 100.0)
        self.assertLess(token_sheet._apca_lc("777777", "888888"), 15.0)  # 近色=低 Lc


class TestTokenOutput(unittest.TestCase):
    """OKLCH 感知坐标注释+color-mix 透明变体+--contrast CLI 旋钮。"""

    def test_oklch_comment_and_colormix(self):
        out = os.path.join(TMP, "ok")
        token_sheet.emit([h.upper() for h in PAL.split(",")], out_base=out)
        css = io.open(out + ".css", encoding="utf-8").read()
        self.assertRegex(css, r"--step-01-app-bg: #[0-9A-F]{6};\s*/\* oklch\([\d.]+ [\d.]+ [\d.]+\) \*/")
        self.assertIn("color-mix(in oklab,", css)
        self.assertIn("--step-03-el-bg-a12:", css)

    def test_cli_contrast_flag(self):
        out = os.path.join(TMP, "cli")
        r = run(["tokens", "--palette", PAL, "--contrast", "high", "--out", out])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("contrast=high", r.stdout)
        js = __import__("json").load(io.open(out + ".json", encoding="utf-8"))
        self.assertEqual(js["scale12_contrast"], "high")

    def test_docgen_when_table_current(self):
        """tokens 新旗标后 --help 面变化 → COMMANDS.md 必须再生(C4 同口径)。"""
        sys.path.insert(0, SCRIPTS)
        import docgen
        doc = docgen.build()
        self.assertIn("--contrast", doc)


if __name__ == "__main__":
    unittest.main()
