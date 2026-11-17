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
SCRIPT = SKILL_DIR / "scripts" / "cad_measure.py"


class CadMeasureTest(unittest.TestCase):
    def run_measure(self, payload: dict, *extra: str) -> dict:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        src = root / "source.json"
        src.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        out = root / "out"
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), str(src), "--out-dir", str(out), *extra],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        result = json.loads((out / "cad-measurement-candidates.json").read_text(encoding="utf-8"))
        self.assertTrue((out / "cad-measurement-candidates.md").exists())
        self.assertTrue((out / "cad-measurement-candidates.csv").exists())
        return result

    def test_explicit_text_length_area_volume(self):
        result = self.run_measure({
            "schema": "cad-scan-detail/v1",
            "text_records": [
                {"kind": "TEXT", "text": "管长 3000mm", "layer": "NOTE", "x": 1, "y": 2},
                {"kind": "TEXT", "text": "房间面积 12.5m2", "layer": "NOTE", "x": 3, "y": 4},
                {"kind": "TEXT", "text": "体积 2.4m3", "layer": "NOTE", "x": 5, "y": 6},
            ],
        })
        by_kind = {row["kind"]: row for row in result["measurements"] if row["basis"] == "explicit_text"}
        self.assertEqual(by_kind["length"]["value"], 3.0)
        self.assertEqual(by_kind["area"]["value"], 12.5)
        self.assertEqual(by_kind["volume"]["value"], 2.4)
        self.assertTrue(all(row["final_quantity"] is False for row in result["measurements"]))
        self.assertEqual(result["summary"]["final_quantities"], 0)

    def test_polygon_area_converts_with_unit_and_scale(self):
        result = self.run_measure({
            "schema": "cad-descriptive-geometry/v7",
            "source_file": "building.dwg",
            "scale_unit_audit": [
                {"file": "building.dwg", "sheet": 1, "scales": ["1:100"], "units": ["mm"], "spaces": ["model"], "status": "candidate"}
            ],
            "room_boundaries": [
                {
                    "id": "room-boundary-1",
                    "file": "building.dwg",
                    "sheet": 1,
                    "rooms": ["办公室"],
                    "polygon": [[0, 0], [10000, 0], [10000, 5000], [0, 5000]],
                    "status": "candidate",
                    "evidence": [{"file_name": "building.dwg", "sheet": 1, "layer": "A-WALL"}],
                }
            ],
        })
        row = next(item for item in result["measurements"] if item["basis"] == "polygon")
        self.assertEqual(row["value"], 50.0)
        self.assertEqual(row["value_drawing_units"], 50000000.0)
        self.assertEqual(row["status"], "candidate")
        self.assertFalse(row["final_quantity"])

    def test_polygon_area_missing_unit_is_review(self):
        result = self.run_measure({
            "schema": "cad-descriptive-geometry/v7",
            "source_file": "building.dwg",
            "room_boundaries": [
                {
                    "id": "room-boundary-1",
                    "file": "building.dwg",
                    "sheet": 1,
                    "rooms": ["办公室"],
                    "polygon": [[0, 0], [1000, 0], [1000, 1000], [0, 1000]],
                    "status": "candidate",
                }
            ],
        })
        row = next(item for item in result["measurements"] if item["basis"] == "polygon")
        self.assertIsNone(row["value"])
        self.assertEqual(row["value_drawing_units"], 1000000.0)
        self.assertEqual(row["status"], "review")
        self.assertIn("缺", row["review_reason"])

    def test_bbox_area_is_never_candidate(self):
        result = self.run_measure({
            "schema": "cad-descriptive-geometry/v7",
            "scale_unit_audit": [{"scales": ["1:100"], "units": ["mm"], "spaces": ["model"], "status": "candidate"}],
            "stair_ramp_steps": [
                {
                    "id": "stair-ramp-step-1",
                    "status": "review",
                    "geometry": {"bbox": [0, 0, 2000, 1000], "bbox_area_drawing_units2": 2000000},
                }
            ],
        })
        row = next(item for item in result["measurements"] if item["basis"] == "bbox")
        self.assertEqual(row["status"], "review")
        self.assertIn("外接框", row["review_reason"])

    def test_volume_requires_explicit_parameter_and_stays_review(self):
        result = self.run_measure({
            "schema": "cad-descriptive-geometry/v7",
            "scale_unit_audit": [{"scales": ["1:100"], "units": ["mm"], "spaces": ["model"], "status": "candidate"}],
            "room_boundaries": [
                {
                    "id": "room-boundary-1",
                    "polygon": [[0, 0], [10000, 0], [10000, 5000], [0, 5000]],
                    "status": "candidate",
                }
            ],
        }, "--thickness-m", "0.1")
        volume = next(item for item in result["measurements"] if item["kind"] == "volume")
        self.assertEqual(volume["value"], 5.0)
        self.assertEqual(volume["status"], "review")
        self.assertIn("未做洞口", volume["review_reason"])

    def test_mep_route_length_is_evidence_not_final_pipe_length(self):
        result = self.run_measure({
            "schema": "cad-mep-geometry/v2",
            "scale_unit_audit": [{"scales": ["1:100"], "units": ["mm"], "spaces": ["model"], "status": "candidate"}],
            "route_segments": [
                {"id": "route-1", "geometry": [0, 0, 3000, 0], "length_drawing_units": 3000, "status": "candidate"}
            ],
        })
        row = next(item for item in result["measurements"] if item["kind"] == "length")
        self.assertEqual(row["value"], 3.0)
        self.assertEqual(row["status"], "review")
        self.assertIn("单段路由", row["review_reason"])

    def test_paper_space_applies_scale_only_when_explicit(self):
        result = self.run_measure({
            "schema": "cad-descriptive-geometry/v7",
            "scale_unit_audit": [{"scales": ["1:100"], "units": ["mm"], "spaces": ["paper"], "status": "candidate"}],
            "wall_segments": [
                {"id": "wall-1", "segment": [0, 0, 100, 0], "length_drawing_units": 100, "status": "candidate"}
            ],
        })
        row = next(item for item in result["measurements"] if item["kind"] == "length")
        self.assertEqual(row["value"], 10.0)
        self.assertTrue(row["scale_applied"])


if __name__ == "__main__":
    unittest.main()
