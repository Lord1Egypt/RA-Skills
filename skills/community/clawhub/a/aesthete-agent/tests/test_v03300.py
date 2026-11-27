# -*- coding: utf-8 -*-
"""test_v03300 — 0.33.0 回归:响应式艺术方向(容器查询渐进+断点戏剧+法则入文档)。"""
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


class TestContainerBase(unittest.TestCase):
    """容器查询渐进底座:.wrap 成为查询容器(组件按所处空间响应)。"""

    def test_base_css_container_support(self):
        tokens = scaffold_kit.derive({"hexes": DP}, "夜松", "NP", "")
        css = layout_recipes.base_css(tokens)
        self.assertIn("@supports (container-type: inline-size)", css)
        self.assertIn("container-type:inline-size", css)


class TestMobileArtDirection(unittest.TestCase):
    """断点戏剧:窄容器下 EDIT-SPLIT 数据先行(menu-card 反转到文案上方)。"""

    def test_es_mobile_reorder(self):
        tokens = scaffold_kit.derive({"hexes": DP}, "夜松", "NP", "")
        css = re.search(r"<style>(.*?)</style>",
                        layout_recipes.build_recipe(tokens, "EDIT-SPLIT"), re.S).group(1)
        self.assertIn("@container (max-width: 720px)", css)
        self.assertIn("flex-direction:column-reverse", css)
        self.assertIn("出货清单先行", css)

    def test_css_structure_intact(self):
        for recipe in ("EDIT-SPLIT", "SWISS-POSTER", "BLUEPRINT", "EDITORIAL-MAG"):
            tokens = scaffold_kit.derive({"hexes": DP}, "夜松", "NP", "")
            css = re.search(r"<style>(.*?)</style>",
                            layout_recipes.build_recipe(tokens, recipe), re.S).group(1)
            self.assertEqual(css.count("/*"), css.count("*/"), recipe)
            self.assertEqual(css.count("{"), css.count("}"), recipe)


class TestDocRule(unittest.TestCase):
    """断点戏剧法则入 layout-composition.md。"""

    def test_doc_has_rule(self):
        doc = io.open(os.path.join(ROOT, "references", "layout-composition.md"),
                      encoding="utf-8").read()
        self.assertIn("断点戏剧", doc)
        self.assertIn("容器口径优先", doc)
        self.assertIn("数据先行反转", doc)


if __name__ == "__main__":
    unittest.main()
