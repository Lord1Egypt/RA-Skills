#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2]
SCRIPT = SKILL_DIR / "scripts" / "cad_landscape_calibrate.py"


def make_detail():
    return {
        "files": [{"name": "某设计院景观.dwg"}],
        "meta": {"block_refs": {"T-银杏": 12, "S-紫薇": 8, "G-麦冬": 20, "未知块X": 3}, "insert_count": 43},
        "text_records": [{"kind": "TEXT", "text": "种植平面图", "layer": "TITLE", "x": 10, "y": 10, "file": 0, "sheet": 1}],
    }


class LandscapeCalibrateTest(unittest.TestCase):
    def run_calibrate(self, detail, institute="test_design", write=True):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        src = root / "detail.json"
        src.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
        out = root / "校准"
        cmd = [sys.executable, str(SCRIPT), str(src), "--institute", institute, "--out-dir", str(out)]
        override_file = root / f"{institute}_override.json"
        if write:
            cmd += ["--write-override", "--override-path", str(override_file)]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        result = json.loads((out / "detail.calibrate.json").read_text(encoding="utf-8"))
        return result, out, override_file

    def test_suggests_and_writes_override(self):
        result, out, override_file = self.run_calibrate(make_detail())
        self.assertFalse(result["final_quantity"])
        self.assertGreaterEqual(result["summary"]["suggestions"], 1)
        # T- / S- / G- 前缀应被推断
        cats = {row["suggested_category"] for row in result["suggestions"]}
        self.assertTrue(cats & {"乔木", "灌木", "地被"})
        self.assertTrue(override_file.exists())
        override = json.loads(override_file.read_text(encoding="utf-8"))
        self.assertIn("T-银杏", override["plant_block_aliases"])

    def test_without_write_no_file(self):
        result, out, override_file = self.run_calibrate(make_detail(), write=False)
        self.assertFalse(override_file.exists())

    def test_text_word_suggestions_write(self):
        detail = make_detail()
        detail["text_records"] = [
            {"kind": "TEXT", "text": "苗木图例 1-10 奇楠树 φ15cm", "layer": "苗木表", "x": 200, "y": 8000, "file": 0, "sheet": 1},
        ]
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        src = root / "detail.json"
        src.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
        out = root / "校准"
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), str(src), "--institute", "test_design", "--out-dir", str(out),
             "--write-override", "--write-text-words", "--override-path", str(root / "test_design_override.json")],
            capture_output=True, text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        result = json.loads((out / "detail.calibrate.json").read_text(encoding="utf-8"))
        words = {x["word"]: x for x in result.get("text_word_suggestions") or []}
        self.assertIn("奇楠树", words, words.keys())
        self.assertEqual(words["奇楠树"]["suggested_category"], "乔木")
        self.assertGreaterEqual(result["summary"]["text_auto_appliable"], 1)
        override_file = root / "test_design_override.json"
        self.assertTrue(override_file.exists())
        override = json.loads(override_file.read_text(encoding="utf-8"))
        self.assertIn("奇楠树", override.get("plant_trees", []))

    def test_verify_after_override(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        src = root / "detail.json"
        src.write_text(json.dumps(make_detail(), ensure_ascii=False), encoding="utf-8")
        out = root / "校准"
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), str(src), "--institute", "test_design", "--out-dir", str(out),
             "--write-override", "--verify", "--override-path", str(root / "test_design_override.json")],
            capture_output=True, text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        verify_out = out / "calibrate_verify.json"
        self.assertTrue(verify_out.exists(), proc.stdout + proc.stderr)
        verifies = json.loads(verify_out.read_text(encoding="utf-8"))
        self.assertEqual(len(verifies), 1)
        self.assertFalse(verifies[0]["final_quantity"])


if __name__ == "__main__":
    unittest.main()


class CalibrateSuggestionExcludeTests(unittest.TestCase):
    def test_suggest_text_word_rejects_nonplant(self):
        import sys as _sys
        _sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
        from cad_common import load_rules
        from cad_landscape_calibrate import suggest_text_word
        rules = load_rules(SKILL_DIR / "packs/landscape-geometry/rules.json")
        for bad in ("花砖", "振兴花园", "济南市槐荫区", "建设银行济南槐荫支行阳光新城分理处",
                    "槐荫区市政养护所宿舍", "济南市公安局槐荫分局"):
            self.assertEqual(suggest_text_word(bad, rules), ("", "", 0.0), bad)
        # 明确植物词仍建议
        self.assertEqual(suggest_text_word("紫叶矮樱", rules)[0], "乔木")
        self.assertEqual(suggest_text_word("柿树", rules)[0], "乔木")
