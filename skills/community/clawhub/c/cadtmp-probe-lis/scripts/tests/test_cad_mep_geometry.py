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
SCRIPT = SKILL_DIR / "scripts" / "cad_mep_geometry.py"


class MepGeometryTest(unittest.TestCase):
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
        return json.loads((out / "detail.mep.json").read_text(encoding="utf-8")), out

    def test_extracts_mep_systems_routes_equipment_labels_and_risers(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 10000, 10000]}]},
            "files": [{"name": "mep.dwg"}],
            "text_records": [
                {"kind": "TEXT", "text": "给排水系统图 1:100 单位：mm", "layer": "TITLE", "x": 100, "y": 9900, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "JL-1", "layer": "PIPE-LABEL", "x": 1000, "y": 1000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "DN100", "layer": "PIPE-LABEL", "x": 1100, "y": 1000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "WDZ-BYJ-3X2.5-PC20", "layer": "WIRE-LABEL", "x": 2000, "y": 2000, "sheet": 1, "file": 0},
                {"kind": "INSERT", "text": "水泵", "layer": "EQUIP", "x": 1500, "y": 1500, "sheet": 1, "file": 0},
                {"kind": "INSERT", "text": "VALVE", "layer": "EQUIP", "x": 1600, "y": 1500, "sheet": 1, "file": 0},
            ],
            "geometry_segments": [[[0, 0, 1000, 0], [1000, 0, 1000, 1000]]],
            "geometry_layers": [["PIPE-给水", "PIPE-给水"]],
        }
        result, out = self.run_script(detail)
        self.assertEqual(result["schema"], "cad-mep-geometry/v2")
        self.assertEqual(result["summary"]["drawing_types"], 1)
        self.assertEqual(result["summary"]["route_segments"], 2)
        self.assertEqual(result["summary"]["equipment"], 2)
        self.assertEqual(result["summary"]["risers"], 1)
        systems = {row["system"] for row in result["systems"]}
        self.assertIn("plumbing", systems)
        self.assertIn("water_supply", systems)
        routes = result["route_segments"]
        self.assertTrue(all(row["route_class"] == "water_pipe" for row in routes))
        self.assertTrue(all(row["status"] == "candidate" for row in routes))
        equipment_by_name = {row["name"]: row for row in result["equipment"]}
        self.assertEqual(equipment_by_name["水泵"]["category"], "pump")
        self.assertEqual(equipment_by_name["VALVE"]["category"], "valve")
        label_types = {row["label_type"] for row in result["labels"]}
        self.assertIn("pipe_spec", label_types)
        self.assertIn("circuit_spec", label_types)
        circuit = next(row for row in result["labels"] if row["label_type"] == "circuit_spec")
        self.assertEqual(circuit["text"], "WDZ-BYJ-3X2.5-PC20")
        self.assertEqual(result["risers"][0]["id"], "JL-1")
        self.assertEqual(result["risers"][0]["system"], "water_supply")
        self.assertEqual(result["summary"]["vertical_routes"], 1)
        self.assertEqual(result["vertical_routes"][0]["id"], "JL-1")
        self.assertEqual(result["vertical_routes"][0]["route_class"], "water_pipe")
        self.assertEqual(result["vertical_routes"][0]["status"], "candidate")
        self.assertEqual(result["summary"]["topology_components"], 1)
        self.assertEqual(result["topology"]["components"][0]["topology_class"], "open-candidate")
        self.assertEqual(result["topology"]["components"][0]["open_endpoint_count"], 2)
        self.assertEqual(result["connectivity"]["summary"]["open_endpoints"], 2)
        self.assertIn("不输出工程量", result["boundary"])
        self.assertNotIn("quantity", result)
        self.assertNotIn("material_quantity", result)
        self.assertTrue((out / "detail.mep.md").exists())
        self.assertTrue((out / "detail.mep.csv").exists())

    def test_missing_scale_and_geometry_enter_review(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 1000, 1000]}]},
            "files": [{"name": "mep.dwg"}],
            "text_records": [
                {"kind": "TEXT", "text": "电气平面图 单位：mm", "layer": "TITLE", "x": 10, "y": 10, "sheet": 1, "file": 0},
            ],
        }
        result, _out = self.run_script(detail)
        review_types = {row["type"] for row in result["review"]}
        self.assertIn("scale_unit", review_types)
        self.assertIn("input_geometry", review_types)
        self.assertEqual(result["summary"]["route_segments"], 0)
        self.assertTrue(result["boundary"].startswith("只输出安装识图候选"))

    def test_connectivity_marks_isolated_segment(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 1000, 1000]}]},
            "files": [{"name": "mep.dwg"}],
            "text_records": [],
            "geometry_segments": [[[0, 0, 100, 0]]],
            "geometry_layers": [["PIPE-给水"]],
        }
        result, _out = self.run_script(detail)
        self.assertEqual(result["connectivity"]["summary"]["open_endpoints"], 2)
        self.assertEqual(result["connectivity"]["summary"]["isolated_segments"], 1)

    def test_mep_relations_flag_system_conflict(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 1000, 1000]}]},
            "files": [{"name": "mep.dwg"}],
            "text_records": [
                {"kind": "TEXT", "text": "水泵 P-1", "layer": "EQUIP", "x": 0, "y": 0, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "JL-1", "layer": "RISER", "x": 500, "y": 500, "sheet": 1, "file": 0},
            ],
            "geometry_segments": [[[0, 0, 100, 0], [100, 0, 200, 0]]],
            "geometry_layers": [["PIPE-给水", "PIPE-给水"]],
        }
        result, _out = self.run_script(detail)
        self.assertGreaterEqual(result["summary"]["mep_relations"], 1)
        self.assertIn("mep_relations", result)
        self.assertTrue(any(row["relation_type"] == "equipment_to_route" for row in result["mep_relations"]))
        self.assertTrue(any(row["relation_type"] == "endpoint_connection" for row in result["mep_relations"]))
        self.assertTrue(any(row["status"] == "candidate" for row in result["mep_relations"]))

    def test_topology_closed_loop_and_vertical_geometry_review(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 3000, 3000]}]},
            "files": [{"name": "mep.dwg"}],
            "text_records": [
                {"kind": "TEXT", "text": "给排水系统图 1:100 单位：mm", "layer": "TITLE", "x": 10, "y": 2990, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "JL-1 向上", "layer": "PIPE-LABEL", "x": 500, "y": 500, "sheet": 1, "file": 0},
            ],
            "geometry_segments": [[
                [0, 0, 1000, 0],
                [1000, 0, 1000, 1000],
                [1000, 1000, 0, 1000],
                [0, 1000, 0, 0],
                [2000, 0, 3000, 0],
            ]],
            "geometry_layers": [[
                "PIPE-给水", "PIPE-给水", "PIPE-给水", "PIPE-给水", "立管-给水",
            ]],
        }
        result, _out = self.run_script(detail)
        self.assertEqual(result["topology"]["summary"]["closed_loop_candidates"], 1)
        self.assertEqual(result["topology"]["summary"]["open_components"], 1)
        self.assertEqual(result["summary"]["vertical_routes"], 2)
        vertical = result["vertical_routes"]
        self.assertEqual(vertical[0]["id"], "JL-1")
        self.assertEqual(vertical[0]["direction"], "up")
        self.assertEqual(vertical[0]["status"], "candidate")
        geometry_only = next(row for row in vertical if row["id"] is None)
        self.assertEqual(geometry_only["route_class"], "water_pipe")
        self.assertEqual(geometry_only["status"], "review")
        self.assertIn("无立管编号", geometry_only["review_reason"])
        self.assertTrue(any(row["type"] == "vertical_route" for row in result["review"]))
        self.assertTrue(any(row["type"] == "topology" for row in result["review"]))


if __name__ == "__main__":
    unittest.main()
