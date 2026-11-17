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
SCRIPT = SKILL_DIR / "scripts" / "cad_structural_geometry.py"


class StructuralGeometryTest(unittest.TestCase):
    def run_script(self, detail, out_name="out"):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        src = root / "detail.json"
        src.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
        out = root / out_name
        proc = subprocess.run([sys.executable, str(SCRIPT), str(src), "--out-dir", str(out)], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return json.loads((out / "detail.structural.json").read_text(encoding="utf-8")), out

    def test_extracts_structure_members_rebar_node_grid_and_geometry(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 10000, 10000]}]},
            "files": [{"name": "structure.dwg"}],
            "text_records": [
                {"kind": "TEXT", "text": "结构平面图 1:100 单位：mm", "layer": "TITLE", "x": 100, "y": 9900, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "KL1 连梁", "layer": "BEAM", "x": 1000, "y": 1000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "混凝土强度 C30 HRB400", "layer": "NOTE", "x": 1100, "y": 1000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "纵筋 HRB400@200 箍筋 C8@100", "layer": "REBAR", "x": 1200, "y": 1000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "节点 JD-01", "layer": "NODE", "x": 1300, "y": 1000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "1轴", "layer": "GRID", "x": 100, "y": 100, "sheet": 1, "file": 0},
            ],
            "geometry_segments": [[[0, 0, 1000, 0], [1000, 0, 1000, 1000]]],
            "geometry_layers": [["S-BEAM-梁", "S-BEAM-梁"]],
        }
        result, out = self.run_script(detail)
        self.assertEqual(result["schema"], "cad-structural-geometry/v1")
        self.assertGreaterEqual(result["summary"]["drawing_types"], 1)
        self.assertGreaterEqual(result["summary"]["systems"], 1)
        self.assertGreaterEqual(result["summary"]["members"], 1)
        self.assertGreaterEqual(result["summary"]["rebars"], 1)
        self.assertGreaterEqual(result["summary"]["nodes"], 1)
        self.assertGreaterEqual(result["summary"]["grids"], 1)
        self.assertEqual(result["summary"]["structural_geometry"], 2)
        self.assertIn("不输出混凝土体积", result["boundary"])
        member = next(row for row in result["members"] if row["code"] == "KL1")
        self.assertEqual(member["category"], "beam")
        self.assertTrue(result["rebars"][0]["rebar_spec"])
        self.assertTrue((out / "detail.structural.md").exists())
        self.assertTrue((out / "detail.structural.csv").exists())
        contract = result["contract"]
        sections = {row["section"] for row in contract["candidates"] + contract["review_candidates"]}
        self.assertTrue(sections & {"members", "rebars", "structural_geometry"})
        self.assertTrue(all(row["final_quantity"] is False for row in contract["candidates"] + contract["review_candidates"]))

    def test_civil_defense_structure_terms_are_classified(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 10000, 10000]}]},
            "files": [{"name": "人防结构.dwg"}],
            "text_records": [
                {"kind": "TEXT", "text": "人防结构平面图 1:100 单位：mm", "layer": "TITLE", "x": 100, "y": 9900, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "临空墙 Q1", "layer": "S-WALL", "x": 1000, "y": 1000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "门框墙 MKQ1", "layer": "S-WALL", "x": 1200, "y": 1000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "人防顶板 250厚", "layer": "S-SLAB", "x": 1300, "y": 1000, "sheet": 1, "file": 0},
            ],
            "geometry_segments": [[[0, 0, 1000, 0], [1000, 0, 1000, 1000]]],
            "geometry_layers": [["S-WALL-临空墙", "S-SLAB-人防顶板"]],
        }
        result, _out = self.run_script(detail)
        systems = {row["system"] for row in result["systems"]}
        members = {row["category"] for row in result["members"]}
        self.assertIn("civil_defense", systems)
        self.assertIn("wall", members)
        self.assertIn("slab", members)

    def test_missing_scale_and_geometry_enter_review(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 1000, 1000]}]},
            "files": [{"name": "structure.dwg"}],
            "text_records": [{"kind": "TEXT", "text": "结构平面 单位：mm", "layer": "TITLE", "x": 10, "y": 10, "sheet": 1, "file": 0}],
        }
        result, _out = self.run_script(detail)
        review_types = {row["type"] for row in result["review"]}
        self.assertIn("scale_unit", review_types)
        self.assertEqual(result["summary"]["structural_geometry"], 0)


if __name__ == "__main__":
    unittest.main()
