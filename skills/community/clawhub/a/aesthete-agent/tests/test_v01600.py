# -*- coding: utf-8 -*-
"""0.16.0 回归:范例库检索/定点补丁/渲染闭环清单/明暗策略路由/SWISS 色条。"""
import os
import sys
import io
import re
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import exemplar_kit  # noqa: E402
import layout_recipes  # noqa: E402
import loop_kit  # noqa: E402
import page_audit  # noqa: E402
import scaffold_kit  # noqa: E402

DEEP_PINE = ["01161E", "124559", "598392", "AEC3B0", "EFF6E0"]

BAD_PAGE = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<style>
body{background:#D7AF70;color:#333333}
.small{font-size:10px;color:#333333}
.tight{letter-spacing:-0.02em}
.weak{color:#888888;background:#FFFFFF}
.h1big{font-size:32px;line-height:1.6}
</style></head><body><h1 class="h1big">测试</h1>
<p class="small tight">小字负字距</p><p class="weak">弱对比</p></body></html>"""


class TestExemplar(unittest.TestCase):
    """范例库:≥5 份、元数据齐全、检索命中与零命中显式报错。"""

    def test_library(self):
        allx = exemplar_kit.load_all()
        self.assertGreaterEqual(len(allx), 5, "范例不足 5 份")
        for e in allx:
            for k in ("kind", "register", "recipe", "techniques"):
                self.assertTrue(e["meta"].get(k), f"{e['file']} 缺元数据 {k}")
            self.assertNotIn("linear-gradient", e["html"], f"{e['file']} 含渐变")
            self.assertIn("exemplar", e["html"][:900], f"{e['file']} 头部缺 exemplar 注释")

    def test_retrieve_hit_and_miss(self):
        ranked, err = exemplar_kit.retrieve(kind="landing", register="light")
        self.assertFalse(err)
        self.assertEqual(ranked[0]["meta"]["recipe"], "EDIT-SPLIT")
        body, err2 = exemplar_kit.emit(kind="不存在", register=None)
        self.assertIsNone(body)
        self.assertIn("无命中范例", err2)

    def test_kinds_cover_five_recipes(self):
        allx = exemplar_kit.load_all()
        recipes = {e["meta"]["recipe"] for e in allx}
        self.assertEqual(len(recipes), 5, f"配方覆盖不全: {recipes}")


class TestPatch(unittest.TestCase):
    """定点补丁:机械类出字面对,应用后对应检查清零。"""

    def test_patches_literal_and_apply(self):
        findings, _ = page_audit.audit_page(BAD_PAGE, DEEP_PINE, 12)
        checks = {f["check"] for f in findings}
        for need in ("muddy_large_bg", "font_floor", "cjk_negative_tracking", "contrast_pair"):
            self.assertIn(need, checks, f"fixture 未触发 {need}")
        patches = page_audit.patches_for(findings, BAD_PAGE)
        lit = [p for p in patches if p["search"]]
        self.assertGreaterEqual(len(lit), 4, f"机械补丁不足: {lit}")
        for p in lit:
            self.assertIn(p["search"], BAD_PAGE, f"search 不在原文: {p['search']!r}")
        html = BAD_PAGE
        for p in lit:
            html = html.replace(p["search"], p["replace"])
        findings2, _ = page_audit.audit_page(html, DEEP_PINE, 12)
        after = {f["check"] for f in findings2}
        for gone in ("muddy_large_bg", "font_floor", "cjk_negative_tracking", "contrast_pair"):
            self.assertNotIn(gone, after, f"应用后 {gone} 仍命中")

    def test_tint_to_pale(self):
        tint = page_audit._tint_to_pale("D7AF70")
        self.assertLessEqual(page_audit.contrast_ratio(tint, "FFFFFF"), 1.31,
                             f"tint {tint} 仍不够浅")


class TestLoop(unittest.TestCase):
    """渲染闭环清单:命令按实参生成、五镜与停止条件在位。"""

    def test_checklist(self):
        md = loop_kit.emit("demo.html", DEEP_PINE, floor=12, bg="EFF6E0")
        self.assertIn("audit demo.html --palette " + ",".join(DEEP_PINE), md)
        self.assertIn("qc <首屏>.png --palette " + ",".join(DEEP_PINE), md)
        self.assertIn("--bg EFF6E0", md)
        for kw in ("五镜自审", "停止条件", "patch demo.html", "fullPage", "最多 5 轮"):
            self.assertIn(kw, md)
        self.assertEqual(len(loop_kit.FIVE_LENSES), 5)


class TestPickRecipe(unittest.TestCase):
    """明暗策略路由:浅优板浅底优先,灰阶/深板走暗幕;AUTO 真正生效。"""

    def test_routing(self):
        cases = {
            "DEEP_PINE": (DEEP_PINE, "EDIT-SPLIT"),
            "墨黑": (["111111", "333333", "666666", "999999", "EEEEEE"], "DARK-FOUR-ACT"),
            "糖果": (["FF6B9D", "FFD93D", "6BCB77", "4D96FF", "FF6B6B"], "EDIT-SPLIT"),
            "野莓": (["EA526F", "E76B74", "D7AF70", "937D64", "585B56"], "EDIT-SPLIT"),
        }
        for name, (pal, want) in cases.items():
            tk = scaffold_kit.derive({"hexes": pal}, name, "X", "")
            got = layout_recipes.pick_recipe(tk)
            self.assertEqual(got, want, f"{name}: 期望 {want} 实得 {got}")

    def test_auto_build(self):
        tk = scaffold_kit.derive({"hexes": DEEP_PINE}, "夜松", "NP", "")
        html = layout_recipes.build_recipe(tk, "AUTO")
        self.assertIn("layout-recipe", html)
        self.assertIn("menu-card", html, "AUTO 应落 EDIT-SPLIT(浅优板)")
        self.assertNotIn("night-hero", html, "浅优板 AUTO 不应落暗幕四幕")
        dark = scaffold_kit.derive({"hexes": ["111111", "333333", "666666", "999999", "EEEEEE"]},
                                   "墨", "INK", "")
        self.assertIn("night-hero", layout_recipes.build_recipe(dark, "AUTO"))

    def test_unknown_recipe(self):
        tk = scaffold_kit.derive({"hexes": DEEP_PINE}, "夜松", "NP", "")
        with self.assertRaises(ValueError):
            layout_recipes.build_recipe(tk, "不存在")


class TestDocSync(unittest.TestCase):
    """文档同步闸:SKILL 双语版本一致+0.16 三命令在两份 SKILL 均可见。"""

    def test_twin_version_and_commands(self):
        en = io.open(os.path.join(ROOT, "SKILL.md"), encoding="utf-8").read()
        zh = io.open(os.path.join(ROOT, "SKILL_ZH.md"), encoding="utf-8").read()
        ven = re.search(r"^version:\s*(\S+)", en, re.M).group(1)
        vzh = re.search(r"^version:\s*(\S+)", zh, re.M).group(1)
        self.assertEqual(ven, vzh, f"SKILL 双语版本漂移: {ven} vs {vzh}")
        for cmd in ("exemplar", "patch", "loop"):
            self.assertIn(cmd, en, f"SKILL.md 缺 {cmd}")
            self.assertIn(cmd, zh, f"SKILL_ZH.md 缺 {cmd}")


class TestTwoColorGuard(unittest.TestCase):
    """两色板不再裸 traceback:derive 抛 ValueError,scaffold 命令层守卫。"""

    def test_derive_rejects(self):
        with self.assertRaises(ValueError):
            scaffold_kit.derive({"hexes": ["111111", "EEEEEE"]}, "X", "X", "")


class TestSwissStripe(unittest.TestCase):
    """SWISS-POSTER 补品牌色条(挂账清)。"""

    def test_stripe(self):
        tk = scaffold_kit.derive({"hexes": DEEP_PINE}, "夜松", "NP", "")
        html = layout_recipes.build_recipe(tk, "SWISS-POSTER")
        self.assertIn("height:5px", html, "SWISS 缺页顶品牌色条")
        for other in ("EDIT-SPLIT", "EDITORIAL-MAG"):
            self.assertIn("height:5px", layout_recipes.build_recipe(tk, other))


if __name__ == "__main__":
    unittest.main()
