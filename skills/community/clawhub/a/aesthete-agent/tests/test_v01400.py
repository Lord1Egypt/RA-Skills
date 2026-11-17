# -*- coding: utf-8 -*-
"""0.14.0 回归:布局配方库(五配方端到端)+布局 lint+法则文档。"""
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import scaffold_kit  # noqa: E402
import layout_recipes  # noqa: E402
import page_audit  # noqa: E402

DP = ["01161E", "124559", "598392", "AEC3B0", "EFF6E0"]
RECIPES = ["DARK-FOUR-ACT", "EDIT-SPLIT", "BLUEPRINT", "SWISS-POSTER", "EDITORIAL-MAG"]


class TestRecipes(unittest.TestCase):
    """五配方端到端:产出→自己的闸必须 PASS。"""

    def test_all_recipes_pass_own_gates(self):
        tokens = scaffold_kit.derive({"hexes": DP}, "夜松", "Night Pine", "")
        declared = tokens["PALETTE_DECL"].split(",")
        with tempfile.TemporaryDirectory() as td:
            for recipe in RECIPES:
                html = layout_recipes.build_recipe(tokens, recipe)
                p = os.path.join(td, recipe.lower() + ".html")
                with open(p, "w", encoding="utf-8") as f:
                    f.write(html)
                payload = page_audit.run(p, declared)
                self.assertEqual(payload["verdict"], "PASS",
                                 recipe + ": " + json_dumps(payload["findings"]))
                self.assertEqual(payload["counts"]["P0"], 0, recipe)
                self.assertEqual(payload["counts"]["P1"], 0, recipe)

    def test_recipe_structure_markers(self):
        tokens = scaffold_kit.derive({"hexes": DP}, "夜松", "Night Pine", "")
        markers = {"EDIT-SPLIT": "layout-recipe: EDIT-SPLIT",
                   "BLUEPRINT": "bento",
                   "SWISS-POSTER": "ghost-num",
                   "EDITORIAL-MAG": "bleed",
                   "DARK-FOUR-ACT": "night-hero"}
        for recipe, marker in markers.items():
            html = layout_recipes.build_recipe(tokens, recipe)
            self.assertIn(marker, html, recipe)

    def test_unknown_recipe_rejected(self):
        tokens = scaffold_kit.derive({"hexes": DP}, "夜松", "Night Pine", "")
        with self.assertRaises(ValueError):
            layout_recipes.build_recipe(tokens, "NOT-A-RECIPE")

    def test_dark_four_act_backward_compat(self):
        """build() 原入口继续工作(向后兼容)。"""
        tokens = scaffold_kit.derive({"hexes": DP}, "夜松", "Night Pine", "")
        self.assertIn("night-hero", scaffold_kit.build(tokens))


class TestLayoutLint(unittest.TestCase):
    """布局 lint:三等分/间距档/跑马灯(双向)。"""

    def _run(self, html):
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "t.html")
            with open(p, "w", encoding="utf-8") as f:
                f.write(html)
            return page_audit.run(p, DP)

    def test_equal_thirds_flagged(self):
        html = ('<style>.a{grid-column:span 4}.b{grid-column:span 4}.c{grid-column:span 4}</style>')
        findings = self._run(html)["findings"]
        self.assertIn("equal_thirds", {f["check"] for f in findings})

    def test_section_spacing_tier_flagged(self):
        html = "<style>\nsection{padding:70px 0}\n</style><section>x</section>"
        findings = self._run(html)["findings"]
        self.assertIn("section_spacing_tier", {f["check"] for f in findings})

    def test_marquee_count_flagged(self):
        html = ('<style>@keyframes m1{to{transform:translateX(-50%)}}'
                '.a{animation:m1 20s infinite linear}.b{animation:m1 30s infinite linear}</style>')
        findings = self._run(html)["findings"]
        self.assertIn("marquee_count", {f["check"] for f in findings})

    def test_clean_layout_no_flags(self):
        html = ('<style>\nsection{padding:96px 0}\n.a{grid-column:span 7}.b{grid-column:span 5}\n'
                '.c{animation:m 20s infinite linear}\n</style><section><div class="a"></div><div class="b"></div></section>')
        findings = self._run(html)["findings"]
        for f in findings:
            self.assertNotIn(f["check"], ("equal_thirds", "section_spacing_tier", "marquee_count"))


class TestCliEndToEnd(unittest.TestCase):
    def test_scaffold_recipe_cli(self):
        engine = os.path.join(ROOT, "scripts", "palette_forge.py")
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "page.html")
            r = subprocess.run(
                [sys.executable, engine, "scaffold", "--recipe", "EDIT-SPLIT",
                 "--palette", ",".join(DP), "--brand", "夜松", "--out", out],
                capture_output=True, text=True, timeout=180)
            self.assertEqual(r.returncode, 0, r.stderr)
            html = open(out, encoding="utf-8").read()
            self.assertIn("layout-recipe: EDIT-SPLIT", html)

    def test_scaffold_invalid_recipe_exit_2(self):
        engine = os.path.join(ROOT, "scripts", "palette_forge.py")
        r = subprocess.run(
            [sys.executable, engine, "scaffold", "--recipe", "NOPE",
             "--palette", ",".join(DP), "--brand", "x"],
            capture_output=True, text=True, timeout=180)
        self.assertEqual(r.returncode, 2)
        self.assertIn("未知配方", r.stderr)


class TestLayoutDoc(unittest.TestCase):
    def test_doc_structure(self):
        doc = open(os.path.join(ROOT, "references", "layout-composition.md"), encoding="utf-8").read()
        self.assertIn("何时读我", doc)
        self.assertIn("验收清单", doc)
        for kw in ("96", "64", "40", "7+5", "一屏一主角", "4+4+4"):
            self.assertIn(kw, doc)


def json_dumps(obj):
    import json
    return json.dumps(obj, ensure_ascii=False)


if __name__ == "__main__":
    unittest.main()
