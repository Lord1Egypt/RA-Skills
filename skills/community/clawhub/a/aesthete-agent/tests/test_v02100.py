# -*- coding: utf-8 -*-
"""0.21.0 回归:动效底座(五配方 reveal/IO/reduced-motion)+audit 动效检查+motion.md。"""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import layout_recipes  # noqa: E402
import page_audit  # noqa: E402
import scaffold_kit  # noqa: E402

DP = ["01161E", "124559", "598392", "AEC3B0", "EFF6E0"]
TK = None


def _tk():
    global TK
    if TK is None:
        TK = scaffold_kit.derive({"hexes": DP}, "夜松", "NP", "")
    return TK


class TestMotionBase(unittest.TestCase):
    """五配方动效底座:reveal/IO script/reduced-motion 三件套齐。"""

    def test_all_recipes_motion(self):
        for r in ("EDIT-SPLIT", "BLUEPRINT", "SWISS-POSTER", "EDITORIAL-MAG", "DARK-FOUR-ACT"):
            html = layout_recipes.build_recipe(_tk(), r)
            self.assertIn("reveal", html, f"{r} 缺 reveal")
            self.assertIn("IntersectionObserver", html, f"{r} 缺 IO script")
            self.assertIn("prefers-reduced-motion", html, f"{r} 缺 reduced-motion")

    def test_stagger_doses(self):
        """EDIT-SPLIT hero stagger ≤3 进入事件(dose M4)。"""
        html = layout_recipes.build_recipe(_tk(), "EDIT-SPLIT")
        n = html.count('class="reveal') + len([m for m in ['reveal d1', 'reveal d2'] if f'"{m}' in html])
        self.assertLessEqual(n, 6, f"进入事件过多: {n}")

    def test_no_scale_hover(self):
        """底座自身无 scale/rotate hover。"""
        css = layout_recipes.base_css(_tk())
        import re
        for m in re.finditer(r":hover\s*\{[^}]*\}", css):
            self.assertNotIn("scale", m.group(0))


class TestMotionAudit(unittest.TestCase):
    """audit 动效检查:scale hover/motion lag 两案。"""

    def test_scale_hover(self):
        page = ('<html lang="zh-CN"><head><style>.b:hover{transform:scale(1.3)}</style></head>'
                '<body><a class="b">x</a></body></html>')
        findings, _ = page_audit.audit_page(page, None, 12)
        self.assertIn("motion_scale_hover", {f["check"] for f in findings})

    def test_hover_lag(self):
        page = ('<html lang="zh-CN"><head><style>'
                '.b{transition:transform .18s ease}.b:hover{transform:translateY(-2px);transition:transform .8s ease}'
                '</style></head><body><a class="b">x</a></body></html>')
        findings, _ = page_audit.audit_page(page, None, 12)
        self.assertIn("motion_lag", {f["check"] for f in findings})

    def test_entry_transition_not_flagged(self):
        """进入编排 0.7s(非 hover)不得误报——M1 合法。"""
        page = ('<html lang="zh-CN"><head><style>'
                '.reveal{opacity:0;transform:translateY(24px);transition:opacity .7s ease,transform .7s ease}'
                '</style></head><body><h1 class="reveal">x</h1></body></html>')
        findings, _ = page_audit.audit_page(page, None, 12)
        self.assertNotIn("motion_lag", {f["check"] for f in findings})


class TestMotionDoc(unittest.TestCase):
    """motion.md 三行块+M1-M5。"""

    def test_doc(self):
        import io
        head = io.open(os.path.join(ROOT, "references", "motion.md"), encoding="utf-8").read()[:300]
        self.assertIn("何时读我", head)
        self.assertIn("回 INDEX", head)
        body = io.open(os.path.join(ROOT, "references", "motion.md"), encoding="utf-8").read()
        for kw in ("M1", "M2", "M3", "M4", "M5", "md5", "@supports"):
            self.assertIn(kw, body)


if __name__ == "__main__":
    unittest.main()
