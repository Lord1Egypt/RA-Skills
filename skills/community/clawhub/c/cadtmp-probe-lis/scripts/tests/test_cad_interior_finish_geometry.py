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
SCRIPT = SKILL_DIR / "scripts" / "cad_deep_geometry.py"


class InteriorFinishTest(unittest.TestCase):
    def run_script(self, detail, out_name="out"):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        src = root / "detail.json"
        src.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
        out = root / out_name
        proc = subprocess.run([sys.executable, str(SCRIPT), str(src), "--pack", "interior_finish", "--out-dir", str(out)], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return json.loads((out / "detail.interior_finish.json").read_text(encoding="utf-8")), out

    def test_ExtractsInteriorFinish_candidates_and_geometry(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 50000, 50000]}]},
            "files": [{"name": "精装修平面.dwg"}],
            "text_records": [{"kind": "TEXT", "text": text, "layer": "TITLE", "x": 1000, "y": 49000, "sheet": 1, "file": 0} for text in ["精装修平面 1:50 单位：mm", "地面做法 DM-01 标高 0.050", "墙面乳胶漆", "柜体 固定家具"]],
            "geometry_segments": [[[0, 0, 40000, 0], [40000, 0, 40000, 40000], [40000, 40000, 0, 40000]]],
            "geometry_layers": [["INT-FLOOR-地面", "INT-FLOOR-地面", "INT-FLOOR-地面"]],
        }
        result, out = self.run_script(detail)
        self.assertEqual(result["schema"], "cad-interior-finish-geometry/v1")
        self.assertGreaterEqual(result["summary"]["drawing_types"], 1)
        self.assertGreaterEqual(result["summary"]["systems"], 1)
        self.assertGreaterEqual(result["summary"]["components"], 1)
        self.assertGreaterEqual(result["summary"]["references"], 1)
        self.assertEqual(len(result["interior_finish_geometry"]), 3)
        self.assertIn("不输出", result["boundary"])
        self.assertTrue((out / "detail.interior_finish.md").exists())
        self.assertTrue((out / "detail.interior_finish.csv").exists())
        contract = result["contract"]
        sections = {row["section"] for row in contract["candidates"] + contract["review_candidates"]}
        self.assertTrue(sections & {"components", "references", "interior_finish_geometry"})
        self.assertTrue(all(row["final_quantity"] is False for row in contract["candidates"] + contract["review_candidates"]))

    def test_building_notes_insulation_and_schedule_are_classified(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 50000, 50000]}]},
            "files": [{"name": "建筑总说明.dwg"}],
            "text_records": [
                {"kind": "TEXT", "text": "建筑总说明 1:100 单位：mm", "layer": "TITLE", "x": 1000, "y": 49000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "外墙外保温 岩棉 传热系数", "layer": "NOTE", "x": 1000, "y": 48000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "楼面做法表 地面做法", "layer": "TITLE", "x": 1000, "y": 47000, "sheet": 1, "file": 0},
            ],
            "geometry_segments": [[[0, 0, 40000, 0], [40000, 0, 40000, 40000]]],
            "geometry_layers": [["INT-WALL-保温", "INT-FLOOR-地面"]],
        }
        result, _out = self.run_script(detail)
        systems = {row["system"] for row in result["systems"]}
        cats = {row["category"] for row in result["components"]}
        self.assertIn("insulation", systems)
        self.assertIn("insulation", cats)

    def test_missing_scale_and_geometry_enter_review(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 1000, 1000]}]},
            "files": [{"name": "精装修平面.dwg"}],
            "text_records": [{"kind": "TEXT", "text": "精装修平面 单位：mm", "layer": "TITLE", "x": 10, "y": 10, "sheet": 1, "file": 0}],
        }
        result, _out = self.run_script(detail)
        review_types = {row["type"] for row in result["review"]}
        self.assertIn("scale_unit", review_types)
        self.assertIn("input_geometry", review_types)
        self.assertEqual(len(result["interior_finish_geometry"]), 0)


if __name__ == "__main__":
    unittest.main()
