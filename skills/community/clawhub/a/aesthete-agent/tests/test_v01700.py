# -*- coding: utf-8 -*-
"""0.17.0 回归(先行):布局卷三新检查 + audit var() 三刀。"""
import os
import json
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import page_audit  # noqa: E402

MONO = """<!DOCTYPE html><html lang="zh-CN"><head><style>
section{padding:96px 0}
section.sub{padding:96px 0}
section.alt{padding:96px 0}
section.more{padding:96px 0}
</style></head><body><section>一</section><section class="sub">二</section>
<section class="alt">三</section><section class="more">四</section></body></html>"""

WEAK_HERO = """<!DOCTYPE html><html lang="zh-CN"><head><style>
body{font:400 16px/1.75 sans-serif}
h1{font-size:22px}
</style></head><body><h1>标题</h1><p>正文</p></body></html>"""

FEW_PARA = """<!DOCTYPE html><html lang="zh-CN"><head><style>
.dropcap>p:first-of-type::first-letter{initial-letter:3 2}
</style></head><body><div class="dropcap"><p>只有一段。</p></div></body></html>"""


class TestLayoutChecks(unittest.TestCase):
    """布局卷三新检查:只抓真实病灶,正常页零误报。"""

    def test_monotony(self):
        findings, _ = page_audit.audit_page(MONO, None, 12)
        self.assertIn("section_spacing_monotony", {f["check"] for f in findings})

    def test_protagonist_ratio(self):
        findings, _ = page_audit.audit_page(WEAK_HERO, None, 12)
        self.assertIn("protagonist_ratio", {f["check"] for f in findings})

    def test_dropcap_precondition(self):
        findings, _ = page_audit.audit_page(FEW_PARA, None, 12)
        self.assertIn("dropcap_precondition", {f["check"] for f in findings})

    def test_healthy_page_clean(self):
        good = """<!DOCTYPE html><html lang="zh-CN"><head><style>
body{font:400 16px/1.75 sans-serif}
h1{font-size:clamp(40px,5.8vw,76px)}
section{padding:96px 0}
section.sub{padding:64px 0}
section.tight{padding:40px 0}
</style></head><body><h1>巨字主角</h1>
<section>一</section><section class="sub">二</section><section class="tight">三</section>
</body></html>"""
        findings, _ = page_audit.audit_page(good, None, 12)
        checks = {f["check"] for f in findings}
        for banned in ("section_spacing_monotony", "protagonist_ratio", "dropcap_precondition"):
            self.assertNotIn(banned, checks)


class TestVarAudit(unittest.TestCase):
    """var() 三刀:注释剥离/令牌解析/结构类名大底。"""

    def test_comment_not_flagged(self):
        page = ('<!DOCTYPE html><html lang="zh-CN"><head><style>body{color:#333333}</style></head>'
                '<body><!-- linear-gradient is banned here --><p>教程文本:backdrop-filter:blur 别用 ✅</p></body></html>')
        findings, _ = page_audit.audit_page(page, None, 12)
        checks = {f["check"] for f in findings}
        self.assertNotIn("gradient", checks, "注释里的渐变一词被误判")
        self.assertNotIn("glassmorphism", checks, "正文提及 blur 被误判")
        self.assertNotIn("emoji", checks, "正文符号被误判")

    def test_var_resolved_contrast(self):
        page = ('<html lang="zh-CN"><head><style>'
                ':root{--muted:#888888}'
                '.card{color:var(--muted);background:#FFFFFF}'
                '</style></head><body><p class="card">x</p></body></html>')
        findings, _ = page_audit.audit_page(page, None, 12)
        self.assertIn("contrast_pair", {f["check"] for f in findings}, "var() 文字对比未解析")

    def test_var_fallback(self):
        page = ('<html lang="zh-CN"><head><style>'
                '.card{color:var(--nope, #888888);background:#FFFFFF}'
                '</style></head><body><p class="card">x</p></body></html>')
        findings, _ = page_audit.audit_page(page, None, 12)
        self.assertIn("contrast_pair", {f["check"] for f in findings}, "var() fallback 未解析")

    def test_structural_class_bg(self):
        page = ('<html lang="zh-CN"><head><style>'
                '.hero-band{background:#D7AF70;color:#333333}'
                '</style></head><body><div class="hero-band">x</div></body></html>')
        findings, _ = page_audit.audit_page(page, None, 12)
        self.assertIn("muddy_large_bg", {f["check"] for f in findings}, "结构语义类名大底未查")

    def test_real_recipe_still_clean(self):
        """回归:引擎自身配方页审计不得新增 P0/P1 误报。"""
        import layout_recipes
        import scaffold_kit
        tk = scaffold_kit.derive({"hexes": ["01161E", "124559", "598392", "AEC3B0", "EFF6E0"]},
                                 "夜松", "NP", "")
        html = layout_recipes.build_recipe(tk, "EDIT-SPLIT")
        findings, _ = page_audit.audit_page(html, None, 12)
        bad = [f for f in findings if f["sev"] in ("P0", "P1")]
        self.assertEqual(bad, [], f"配方页出现 P0/P1: {bad}")


class TestColorDirector(unittest.TestCase):
    """配色引擎(0.19 先行入库):manifest 金标=20 PASS/29,与设计意图 100% 一致。"""

    def test_manifest_golden(self):
        import color_director
        cases = json.load(open(os.path.join(ROOT, "tests", "fixtures_colorlab.json"),
                               encoding="utf-8"))
        n_pass = 0
        for case in cases:
            out = color_director.analyze(case["page"], [tuple(z) for z in case["zones"]],
                                         acts=[list(map(tuple, a)) for a in case["acts"]] if case.get("acts") else None,
                                         focal=tuple(case["focal"]) if case.get("focal") else None,
                                         bold=case.get("bold", False),
                                         last_act_loud=case.get("last_act_loud"),
                                         accent_share=case.get("accent_share"),
                                         palette=case.get("palette"),
                                         cap=case.get("cap"),
                                         only=case.get("only"))
            verdict = out.get("verdict") if isinstance(out, dict) else getattr(out, "verdict", None)
            if verdict is None and isinstance(out, dict):
                verdict = "PASS" if not out.get("violations") else "FAIL"
            self.assertIn(verdict, ("PASS", "FAIL"), f"非法裁决 {verdict}: {case.get('page')}")
            expect = case.get("expected")
            if expect:
                self.assertEqual(verdict, expect,
                                 f"{case.get('page')}: 期望 {expect} 实得 {verdict}")
            if verdict == "PASS":
                n_pass += 1
        self.assertEqual(n_pass, len([c for c in cases if c.get("expected") == "PASS"]),
                         f"金标漂移: PASS {n_pass}/{len(cases)}")


if __name__ == "__main__":
    unittest.main()
