# -*- coding: utf-8 -*-
"""0.12.0 回归:语域词表扩容(含东方语域)+ narrate 量化叙事。"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import narrate_kit  # noqa: E402
from palette_forge import BRIEF_KEYWORDS, REGISTER_TAGS  # noqa: E402

DP = "01161E,124559,598392,AEC3B0,EFF6E0"


class TestLexiconExpansion(unittest.TestCase):
    """0.12.0 词表:新词映射到正确语域;东方语域就位;总词量达标。"""

    EXPECT = {
        "frontend_soft": ["侘寂", "棉麻", "奶咖", "松弛"],
        "frontend_deep": ["老钱风", "胡桃木", "深邃"],
        "frontend_bold": ["多巴胺", "节庆", "热烈"],
        "frontend_tech": ["赛博朋克", "霓虹", "终端"],
        "frontend_heritage": ["国风", "水墨", "敦煌", "宋韵", "青绿", "瓷器"],
    }

    def test_words_map_to_registers(self):
        for reg, words in self.EXPECT.items():
            for w in words:
                self.assertIn(w, BRIEF_KEYWORDS.get(reg, []), f"{w} 不在 {reg}")

    def test_heritage_register_tags(self):
        self.assertIn("frontend_heritage", REGISTER_TAGS)
        for t in ("warm", "mid", "dark"):
            self.assertIn(t, REGISTER_TAGS["frontend_heritage"])

    def test_total_frontend_words(self):
        n = sum(len(v) for k, v in BRIEF_KEYWORDS.items() if k.startswith("frontend_"))
        self.assertGreaterEqual(n, 90, f"前端语域总词量 {n} < 90")


class TestNarrate(unittest.TestCase):
    """narrate:数字溯源/双语/指纹链。"""

    REPORT = {
        "palette": DP.split(","),
        "gates": {
            "contrast": {"pass": True, "best": "16.68:1 (#01161E on #EFF6E0)", "threshold": "4.5:1"},
            "color_blind": {"pass": True, "detail": "OK"},
            "ai_slop": {"pass": True, "detail": "CLEAN"},
            "score": {"pass": True, "detail": "17/20 Excellent"},
        },
        "verdict": "PASS", "summary": {"gates_passed": "4/4", "issues_caught": 0},
        "fingerprint": "a" * 64,
    }
    ROLES = {"bg": "EFF6E0", "surface": "AEC3B0", "ink": "01161E",
             "ink2": "124559", "accent": "598392"}

    def test_numbers_traceable(self):
        body, verdict = narrate_kit.emit(self.REPORT, DP.split(","), self.ROLES, "Deep Pine")
        self.assertEqual(verdict, "PASS")
        self.assertIn("16.68:1", body)
        self.assertIn("17/20", body)
        self.assertIn("4/4", body)
        self.assertIn("a" * 16, body)
        self.assertIn("Deep Pine", body)
        # 双语都产出
        self.assertIn("background #EFF6E0", body)

    def test_fail_path_reports_detail(self):
        rep = json.loads(json.dumps(self.REPORT))  # 深拷贝防串改
        rep["gates"]["color_blind"]["pass"] = False
        rep["verdict"] = "FAIL"
        body, verdict = narrate_kit.emit(rep, DP.split(","), self.ROLES, "x")
        self.assertEqual(verdict, "FAIL")
        self.assertIn("撞色风险", body)


class TestCliEndToEnd(unittest.TestCase):
    def test_narrate_cli_theme(self):
        engine = os.path.join(ROOT, "scripts", "palette_forge.py")
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "n.md")
            r = subprocess.run(
                [sys.executable, engine, "narrate", "--theme", "Deep Pine",
                 "--name", "Deep Pine", "--out", out],
                capture_output=True, text=True, timeout=180)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertTrue(os.path.exists(out))
            self.assertIn("Deep Pine", open(out, encoding="utf-8").read())

    def test_narrate_cli_fail_palette_exits_1(self):
        # 全鲜艳刺眼板:report 应 FAIL,narrate 退出码跟随
        engine = os.path.join(ROOT, "scripts", "palette_forge.py")
        r = subprocess.run(
            [sys.executable, engine, "narrate",
             "--palette", "FF0000,00FF00,0000FF", "--name", "rgb"],
            capture_output=True, text=True, timeout=180)
        self.assertEqual(r.returncode, 1)


if __name__ == "__main__":
    unittest.main()
