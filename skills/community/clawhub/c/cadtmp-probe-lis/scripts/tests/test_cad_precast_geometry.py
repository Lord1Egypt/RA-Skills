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


class PrecastTest(unittest.TestCase):
    def run_script(self, detail, out_name="out"):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        src = root / "detail.json"
        src.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
        out = root / out_name
        proc = subprocess.run([sys.executable, str(SCRIPT), str(src), "--pack", "precast", "--out-dir", str(out)], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return json.loads((out / "detail.precast.json").read_text(encoding="utf-8")), out

    def test_ExtractsPrecast_candidates_and_geometry(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 50000, 50000]}]},
            "files": [{"name": "叠合板拆分.dwg"}],
            "text_records": [{"kind": "TEXT", "text": text, "layer": "TITLE", "x": 1000, "y": 49000, "sheet": 1, "file": 0} for text in ["叠合板拆分 1:100 单位：mm", "预制墙 PCW-01 标高 2.900", "桁架筋 叠合板", "预埋件 MJ-01"]],
            "geometry_segments": [[[0, 0, 40000, 0], [40000, 0, 40000, 40000], [40000, 40000, 0, 40000]]],
            "geometry_layers": [["PC-SLAB-叠合板", "PC-SLAB-叠合板", "PC-SLAB-叠合板"]],
        }
        result, out = self.run_script(detail)
        self.assertEqual(result["schema"], "cad-precast-geometry/v1")
        self.assertGreaterEqual(result["summary"]["drawing_types"], 1)
        self.assertGreaterEqual(result["summary"]["systems"], 1)
        self.assertGreaterEqual(result["summary"]["components"], 1)
        self.assertGreaterEqual(result["summary"]["references"], 1)
        self.assertEqual(len(result["precast_geometry"]), 3)
        self.assertIn("不输出", result["boundary"])
        self.assertTrue((out / "detail.precast.md").exists())
        self.assertTrue((out / "detail.precast.csv").exists())
        contract = result["contract"]
        sections = {row["section"] for row in contract["candidates"] + contract["review_candidates"]}
        self.assertTrue(sections & {"components", "references", "precast_geometry"})
        self.assertTrue(all(row["final_quantity"] is False for row in contract["candidates"] + contract["review_candidates"]))

    def test_missing_scale_and_geometry_enter_review(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 1000, 1000]}]},
            "files": [{"name": "叠合板拆分.dwg"}],
            "text_records": [{"kind": "TEXT", "text": "叠合板拆分 单位：mm", "layer": "TITLE", "x": 10, "y": 10, "sheet": 1, "file": 0}],
        }
        result, _out = self.run_script(detail)
        review_types = {row["type"] for row in result["review"]}
        self.assertIn("scale_unit", review_types)
        self.assertIn("input_geometry", review_types)
        self.assertEqual(len(result["precast_geometry"]), 0)


if __name__ == "__main__":
    unittest.main()
