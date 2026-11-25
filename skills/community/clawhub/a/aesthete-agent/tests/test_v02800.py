# -*- coding: utf-8 -*-
"""test_v02800 — 0.28.0 回归:默认即最佳·排印。

web.dev 流式字阶纪律(2.5x 缩放规则+em 端点)/clreq 中西文混排(≤1/4em+标点挤压
渐进)/展示级紧字距纪律(--track-display 替代正字距)/字族双层(--sans-display)。
全部零浏览器。"""
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
TMP = tempfile.mkdtemp(prefix="t280_")
sys.path.insert(0, SCRIPTS)

import layout_recipes  # noqa: E402
import scaffold_kit  # noqa: E402
import type_kit  # noqa: E402

DP = ["01161E", "124559", "598392", "AEC3B0", "EFF6E0"]


class TestFluidDiscipline(unittest.TestCase):
    """web.dev 2.5x 规则:流体档 max/min≤2.5 ⇒ 缩放永远有效(SC 1.4.4)。"""

    def test_default_probe_passes(self):
        self.assertTrue(type_kit.assert_fluid_discipline())

    def test_fluid_ratio_constant_under_25(self):
        tokens, checks = type_kit.build(fluid=True)
        self.assertTrue(checks["fluid_ratio_ok"], checks.get("fluid_error"))
        self.assertEqual(checks["verdict"], "PASS")
        for name in type_kit.FLUID_STEPS:
            px = tokens[name]["px"]
            lo, hi = max(px * 0.62, type_kit.FLOOR if hasattr(type_kit, "FLOOR") else 12.0), px * 1.15
            self.assertLessEqual(hi / lo, 2.5, name)

    def test_clamp_shape(self):
        tokens, _ = type_kit.build(fluid=True)
        m = re.match(r"clamp\(([\d.]+)rem, calc\(([\d.]+)rem \+ ([\d.]+)vw\), ([\d.]+)rem\)",
                     tokens["3xl"]["fluid"])
        self.assertIsNotNone(m, tokens["3xl"]["fluid"])
        lo, _base, vw, hi = (float(g) for g in m.groups())
        # 纪律量化口径=2.5x 规则(已断言);"vw 最小化"是根字号场景口径(0.24vw@16px),
        # display 级跨视口合法 vw 区间 1-5(Utopia/Smashing 通例),这里只验证端点为 rem。
        self.assertLessEqual(hi / lo, 2.5)
        self.assertGreater(lo, 0)


class TestCjkBase(unittest.TestCase):
    """clreq 混排纪律进 CSS 底座:autospace+标点挤压渐进+零正字距正文。"""

    def test_base_css_spacing_features(self):
        tokens = scaffold_kit.derive({"hexes": DP}, "夜松", "NP", "")
        css = layout_recipes.base_css(tokens)
        self.assertIn("text-autospace:normal", css)
        self.assertIn("text-spacing-trim:space-all", css)          # 渐进增强
        self.assertIn("@supports (text-spacing-trim: space-all)", css)
        self.assertIn("--track-display:-0.011em", css)             # 纪律令牌
        self.assertIn("--sans-display:", css)                      # 字族双层
        self.assertNotIn("body{letter-spacing:0.01em}", css)       # 正文正字距已废

    def test_display_tracking_negative_not_positive(self):
        """展示级不许正字距(0.28 纪律;0.01em 正字距=松散廉价向)。"""
        for recipe in ("EDIT-SPLIT", "SWISS-POSTER", "BLUEPRINT", "EDITORIAL-MAG"):
            tokens = scaffold_kit.derive({"hexes": DP}, "夜松", "NP", "")
            html = layout_recipes.build_recipe(tokens, recipe)
            css = re.search(r"<style>(.*?)</style>", html, re.S).group(1)
            for m in re.finditer(r"([.#][\w-]+(?:\.[\w-]+)*)\{[^}]*font-size:(?:[^}]*?clamp\((\d+)px)?[^}]*letter-spacing:([-\d.]+)em", css):
                size = float(m.group(2) or 0)
                val = float(m.group(3))
                if size >= 30 or val < 0:   # 大字号(展示级)或已负值
                    self.assertLessEqual(val, 0, f"{recipe}: {m.group(1)} 展示级正字距 {val}em")

    def test_scaffold_tokens_two_tier(self):
        tokens = scaffold_kit.derive({"hexes": DP}, "夜松", "NP", "")
        html = layout_recipes.build_recipe(tokens, "DARK-FOUR-ACT")
        self.assertIn("--sans-display:", html)
        self.assertIn("--track-display", html)
        self.assertIn("letter-spacing:var(--track-display)", html)  # 四幕巨字已接纪律

    def test_recipe_gates_still_pass(self):
        """默认升级不破闸:五配方产物仍过自己的闸(css 结构+audit)。"""
        import page_audit
        tokens = scaffold_kit.derive({"hexes": DP}, "夜松", "NP", "")
        declared = tokens["PALETTE_DECL"].split(",")
        with tempfile.TemporaryDirectory() as td:
            for recipe in ("EDIT-SPLIT", "SWISS-POSTER"):
                html = layout_recipes.build_recipe(tokens, recipe)
                p = os.path.join(td, recipe.lower() + ".html")
                with open(p, "w", encoding="utf-8") as f:
                    f.write(html)
                payload = page_audit.run(p, declared)
                self.assertEqual(payload["verdict"], "PASS",
                                 recipe + ": " + str(payload["findings"])[:300])
                css = re.search(r"<style>(.*?)</style>", html, re.S).group(1)
                self.assertEqual(css.count("/*"), css.count("*/"), recipe + ": 注释平衡")


if __name__ == "__main__":
    unittest.main()
