# -*- coding: utf-8 -*-
"""0.19.0 回归(先行):色彩导演子命令/report drama 闸/语域配方/match 下发。"""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

ENGINE = os.path.join(ROOT, "scripts", "palette_forge.py")
DP = "01161E,124559,598392,AEC3B0,EFF6E0"


def run(a, **kw):
    return subprocess.run([sys.executable, ENGINE] + a, capture_output=True,
                          text=True, encoding="utf-8", errors="replace", timeout=180, **kw)


class TestDirect(unittest.TestCase):
    """direct 单页快判:干净大域 PASS,中明高饱大域 FAIL。"""

    def test_pass_and_fail(self):
        r = run(["direct", "--zones", "5A0006:0.36,F7EFE5:0.42,3A2A1D:0.08,FFFFFF:0.14", "--bold"])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("PASS", r.stdout)
        r2 = run(["direct", "--zones", "E4572E:0.30,F5F5F0:0.40,333333:0.10,9ACD32:0.20"])
        self.assertEqual(r2.returncode, 1, "中明高饱大域应 FAIL")
        self.assertIn("FAIL", r2.stdout)

    def test_manifest_golden(self):
        r = run(["direct", "--manifest", os.path.join(ROOT, "tests", "fixtures_colorlab.json")])
        self.assertEqual(r.returncode, 0)
        self.assertIn("22/31", r.stdout)


class TestReportDrama(unittest.TestCase):
    """report 第五闸:--zones 给占比即加 drama 闸,gates JSON 可见。"""

    def test_drama_gate_present(self):
        r = run(["report", "--palette", DP,
                 "--zones", "EFF6E0:0.55,AEC3B0:0.22,598392:0.04,124559:0.04,01161E:0.15"])
        self.assertIn("drama", r.stdout, r.stdout[-400:])
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_drama_gate_violation(self):
        # 线与字档 accent 超占面(22%>15% cap,0.20 渲染实验后)→ drama FAIL → rc=1
        r = run(["report", "--palette", DP,
                 "--zones", "124559:0.22,EFF6E0:0.45,AEC3B0:0.18,598392:0.05,01161E:0.10"])
        self.assertIn('"drama"', r.stdout)
        self.assertIn('"pass":false', r.stdout.replace(" ", ""))


class TestRegisterRecipes(unittest.TestCase):
    """语域配方:5 条、register 字段指向合法语域、match 下发。"""

    def test_recipes(self):
        d = json.load(open(os.path.join(ROOT, "palettes", "themes.json"), encoding="utf-8"))
        rr = d.get("register_recipes") or {}
        self.assertGreaterEqual(len(rr), 5)
        reg_names = {v.get("register") for v in rr.values()}
        self.assertIn("frontend_soft", reg_names)
        self.assertIn("frontend_heritage", reg_names)
        for v in rr.values():
            self.assertTrue(v.get("strategy"), f"{v.get('name')} 缺 strategy")

    def test_match_emits_recipe(self):
        r = run(["match", "--brief", "莫兰迪素雅"])
        self.assertIn("配方: 莫兰迪", r.stdout)


if __name__ == "__main__":
    unittest.main()
