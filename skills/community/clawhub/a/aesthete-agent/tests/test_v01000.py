# -*- coding: utf-8 -*-
"""0.10.0 回归:chartpal 图表色板三型 + typescale 字阶。"""
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import chart_kit  # noqa: E402
import type_kit  # noqa: E402

DP = ["01161E", "124559", "598392", "AEC3B0", "EFF6E0"]


class TestChartPal(unittest.TestCase):
    """三型派生:CVD 区分度/单调坡/中性中点。"""

    def test_categorical_distinct(self):
        series, checks = chart_kit.categorical(DP, 5)
        self.assertEqual(checks["verdict"], "PASS",
                         f"min_dE={checks['min_pair_dE_cvd']} l_range={checks['l_range']}")
        self.assertGreaterEqual(checks["min_pair_dE_cvd"], 0.10)
        self.assertGreaterEqual(checks["l_range"], 0.20)
        for h in series:
            self.assertIn(h, [x.upper() for x in DP])

    def test_sequential_monotonic(self):
        series, checks = chart_kit.sequential("598392", 7)
        self.assertEqual(checks["verdict"], "PASS")
        self.assertTrue(checks["monotonic"])
        self.assertGreaterEqual(checks["min_step"], 0.03)
        self.assertEqual(len(series), 7)

    def test_diverging_neutral_mid(self):
        series, checks = chart_kit.diverging("124559", "BC6C25", 7)
        self.assertEqual(checks["verdict"], "PASS")
        self.assertTrue(checks["midpoint_neutral"])
        self.assertTrue(checks["arch"])
        self.assertEqual(len(series), 7)
        # 偶数入参自动补成奇数
        s2, c2 = chart_kit.diverging("124559", "BC6C25", 6)
        self.assertEqual(len(s2), 7)


class TestTypeScale(unittest.TestCase):
    """字阶:下限钳制/等比数学/单调/CSS 产物。"""

    def test_floor_and_ratio(self):
        tokens, checks = type_kit.build(16.0, 1.25, 12.0)
        self.assertEqual(checks["verdict"], "PASS")
        self.assertTrue(checks["monotonic"])
        self.assertEqual(tokens["base"]["px"], 16.0)
        self.assertAlmostEqual(tokens["lg"]["px"], 20.0, delta=0.1)
        self.assertIn("xs", checks["clamped_steps"])
        self.assertEqual(tokens["xs"]["px"], 12.0)

    def test_emit_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            base = os.path.join(td, "type")
            payload = type_kit.emit("夜松", base=16.0, ratio=1.25, out_base=base)
            css = open(base + ".css", encoding="utf-8").read()
            self.assertIn("--text-base:16px/1.7;", css)
            self.assertIn("--font-tnum", css)
            html = open(base + ".html", encoding="utf-8").read()
            self.assertIn("tabular-nums", html)
            self.assertEqual(payload["verdict"], "PASS")
            self.assertEqual(len(payload["fingerprint"]), 64)


class TestCliEndToEnd(unittest.TestCase):
    def test_chartpal_cli(self):
        engine = os.path.join(ROOT, "scripts", "palette_forge.py")
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "chart")
            r = subprocess.run(
                [sys.executable, engine, "chartpal", "--kind", "categorical",
                 "--palette", ",".join(DP), "--series", "5", "--out", out],
                capture_output=True, text=True, timeout=120)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue(os.path.exists(out + ".json"))
            self.assertTrue(os.path.exists(out + ".html"))

    def test_typescale_cli(self):
        engine = os.path.join(ROOT, "scripts", "palette_forge.py")
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "type")
            r = subprocess.run(
                [sys.executable, engine, "typescale", "--name", "t", "--out", out],
                capture_output=True, text=True, timeout=120)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue(os.path.exists(out + ".css"))


if __name__ == "__main__":
    unittest.main()
