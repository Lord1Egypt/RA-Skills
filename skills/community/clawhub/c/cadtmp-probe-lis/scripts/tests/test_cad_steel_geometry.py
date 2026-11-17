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
SCRIPT = SKILL_DIR / "scripts" / "cad_steel_geometry.py"


class SteelGeometryTest(unittest.TestCase):
    def run_script(self, detail: dict, out_name: str = "out") -> tuple[dict, Path]:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        src = root / "detail.json"
        src.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
        out = root / out_name
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), str(src), "--out-dir", str(out)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return json.loads((out / "detail.steel.json").read_text(encoding="utf-8")), out

    def test_extracts_steel_members_sections_connections_materials_and_geometry(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 10000, 10000]}]},
            "files": [{"name": "steel.dwg"}],
            "text_records": [
                {"kind": "TEXT", "text": "钢结构设计总说明 1:100 单位：mm", "layer": "TITLE", "x": 100, "y": 9900, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "钢柱 GZ-1", "layer": "STEEL-COLUMN", "x": 1000, "y": 1000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "H400x200x8x13", "layer": "STEEL-SECTION", "x": 1200, "y": 1000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "Q355B", "layer": "STEEL-MATERIAL", "x": 1200, "y": 900, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "高强螺栓 10.9S", "layer": "CONNECTION", "x": 1300, "y": 1000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "热浸镀锌", "layer": "FINISH", "x": 1300, "y": 900, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "节点 JD-01", "layer": "NODE", "x": 1400, "y": 1000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "1轴", "layer": "GRID", "x": 100, "y": 100, "sheet": 1, "file": 0},
            ],
            "geometry_segments": [[[0, 0, 1000, 0], [1000, 0, 1000, 1000]]],
            "geometry_layers": [["STEEL-钢梁", "STEEL-钢梁"]],
        }
        result, out = self.run_script(detail)
        self.assertEqual(result["schema"], "cad-steel-geometry/v1")
        self.assertGreaterEqual(result["summary"]["drawing_types"], 1)
        self.assertGreaterEqual(result["summary"]["systems"], 1)
        self.assertGreaterEqual(result["summary"]["members"], 1)
        self.assertEqual(result["summary"]["sections"], 1)
        self.assertGreaterEqual(result["summary"]["connections"], 1)
        self.assertEqual(result["summary"]["materials"], 1)
        self.assertGreaterEqual(result["summary"]["finishes"], 1)
        self.assertGreaterEqual(result["summary"]["nodes"], 1)
        self.assertGreaterEqual(result["summary"]["grids"], 1)
        self.assertEqual(result["summary"]["geometry_segments"], 2)
        member = next(row for row in result["members"] if row["code"] == "GZ-1")
        self.assertEqual(member["category"], "steel_column")
        self.assertEqual(result["sections"][0]["section_type"], "h_section")
        self.assertEqual(result["materials"][0]["grade"], "Q355")
        self.assertEqual(result["connections"][0]["category"], "high_strength_bolt")
        self.assertEqual(result["connectivity"]["summary"]["open_endpoints"], 2)
        self.assertIn("不输出重量", result["boundary"])
        self.assertNotIn("quantity", result)
        self.assertNotIn("weight", result)
        self.assertTrue((out / "detail.steel.md").exists())
        self.assertTrue((out / "detail.steel.csv").exists())

    def test_missing_scale_and_geometry_enter_review(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 1000, 1000]}]},
            "files": [{"name": "steel.dwg"}],
            "text_records": [
                {"kind": "TEXT", "text": "钢结构设计总说明 单位：mm", "layer": "TITLE", "x": 10, "y": 10, "sheet": 1, "file": 0},
            ],
        }
        result, _out = self.run_script(detail)
        review_types = {row["type"] for row in result["review"]}
        self.assertIn("scale_unit", review_types)
        self.assertIn("input_geometry", review_types)
        self.assertEqual(result["summary"]["geometry_segments"], 0)

    def test_connectivity_marks_isolated_steel_segment(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 1000, 1000]}]},
            "files": [{"name": "steel.dwg"}],
            "text_records": [],
            "geometry_segments": [[[0, 0, 100, 0]]],
            "geometry_layers": [["STEEL-钢梁"]],
        }
        result, _out = self.run_script(detail)
        self.assertEqual(result["connectivity"]["summary"]["open_endpoints"], 2)
        self.assertEqual(result["connectivity"]["summary"]["isolated_segments"], 1)


if __name__ == "__main__":
    unittest.main()
