# -*- coding: utf-8 -*-
"""test_v03100 — 0.31.0 回归:打磨收口(judge round-3/4 四条轻微建议)。"""
import io
import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import layout_recipes  # noqa: E402
import scaffold_kit  # noqa: E402

DP = ["01161E", "124559", "598392", "AEC3B0", "EFF6E0"]


def build(recipe):
    tokens = scaffold_kit.derive({"hexes": DP}, "夜松", "NP", "")
    return layout_recipes.build_recipe(tokens, recipe)


class TestPolishFixes(unittest.TestCase):
    def test_es_lone_cross_removed(self):
        html = build("EDIT-SPLIT")
        self.assertNotIn('class="cross" style="right:0;top:-6px"', html)  # 孤立+号已撤
        self.assertIn("0.31:孤立 cross 记号撤除", html)                    # 撤除留痕

    def test_bp_gap_tightened(self):
        css = re.search(r"<style>(.*?)</style>", build("BLUEPRINT"), re.S).group(1)
        self.assertIn("padding:96px 0 48px", css)                # hero 底距 72→48
        self.assertIn(".hero + .sub{{padding-top:40px}}".replace("{{", "{").replace("}}", "}"), css)

    def test_sw_double_count_converged(self):
        html = build("SWISS-POSTER")
        # 红色小标+描边巨数并存已收敛:巨数为唯一节序号
        self.assertNotIn('<span class="no">01</span><span class="ghost-num"', html)
        self.assertNotIn('<span class="no">02</span><span class="ghost-num"', html)
        self.assertIn('class="ghost-num" style="display:block">01', html)  # 巨数保留

    def test_d4_lone_dot_removed(self):
        src = io.open(os.path.join(ROOT, "scripts", "scaffold_kit.py"),
                      encoding="utf-8").read()
        self.assertNotIn('r="4.5"', src)                          # 卡内孤点已撤
        self.assertIn("0.31:孤点撤除", src)                        # 撤除留痕


if __name__ == "__main__":
    unittest.main()
