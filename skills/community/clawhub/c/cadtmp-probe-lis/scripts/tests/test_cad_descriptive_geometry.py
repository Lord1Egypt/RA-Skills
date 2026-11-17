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
SCRIPT = SKILL_DIR / "scripts" / "cad_descriptive_geometry.py"


class DescriptiveGeometryTest(unittest.TestCase):
    def test_extracts_candidate_evidence(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 100, 100]}]},
            "text_records": [
                {"kind": "MTEXT", "text": "一层平面图 1:100 单位：毫米", "layer": "TITLE", "x": 1.0, "y": 2.0, "sheet": 1},
                {"kind": "TEXT", "text": "办公室", "layer": "ROOM", "x": 3.0, "y": 4.0, "sheet": 1},
                {"kind": "TEXT", "text": "M1021 1000x2100", "layer": "DOOR", "x": 5.0, "y": 6.0, "sheet": 1},
                {"kind": "TEXT", "text": "地面 地101", "layer": "NOTE", "x": 7.0, "y": 8.0, "sheet": 1}
            ]
        }
        with tempfile.TemporaryDirectory() as temp:
            src = Path(temp) / "detail.json"
            src.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
            out = Path(temp) / "out"
            proc = subprocess.run([sys.executable, str(SCRIPT), str(src), "--out-dir", str(out)],
                                  capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            result = json.loads((out / "detail.descriptive.json").read_text(encoding="utf-8"))
            self.assertEqual(result["summary"]["views"], 1)
            self.assertEqual(result["summary"]["rooms"], 1)
            self.assertEqual(result["summary"]["openings"], 1)
            self.assertEqual(result["summary"]["practices"], 1)
            self.assertEqual(result["views"][0]["type"], "plan")
            self.assertEqual(result["openings"][0]["nominal_size"], ["1000", "2100"])
            self.assertEqual(result["scale_unit_audit"][0]["scales"], ["1:100"])
            self.assertEqual(result["scale_unit_audit"][0]["units"], ["mm"])
            self.assertTrue((out / "detail.descriptive.md").exists())
            self.assertTrue((out / "detail.descriptive.csv").exists())

    def test_parses_schedule_row_and_opening_summary(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 1000, 1000]}]},
            "text_records": [
                {"kind": "MTEXT", "text": "房间装修做法表", "layer": "TITLE", "x": 100, "y": 500, "sheet": 1},
                {"kind": "TEXT", "text": "办公室", "layer": "TABLE", "x": 100, "y": 400, "sheet": 1},
                {"kind": "TEXT", "text": "地101", "layer": "TABLE", "x": 300, "y": 400, "sheet": 1},
                {"kind": "TEXT", "text": "内墙201", "layer": "TABLE", "x": 400, "y": 400, "sheet": 1},
                {"kind": "TEXT", "text": "顶301", "layer": "TABLE", "x": 500, "y": 400, "sheet": 1},
                {"kind": "TEXT", "text": "踢401", "layer": "TABLE", "x": 600, "y": 400, "sheet": 1},
                {"kind": "TEXT", "text": "M1021 1000x2100 3樘", "layer": "TABLE", "x": 700, "y": 300, "sheet": 1},
                {"kind": "INSERT", "text": "M1021", "layer": "DOOR_BLOCK", "x": 800, "y": 300, "sheet": 1}
            ]
        }
        with tempfile.TemporaryDirectory() as temp:
            src = Path(temp) / "detail.json"
            src.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
            out = Path(temp) / "out"
            proc = subprocess.run([sys.executable, str(SCRIPT), str(src), "--out-dir", str(out)],
                                  capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            result = json.loads((out / "detail.descriptive.json").read_text(encoding="utf-8"))
            self.assertEqual(result["summary"]["room_schedules"], 1)
            schedule = result["room_schedules"][0]
            self.assertEqual(schedule["room"], "办公室")
            self.assertEqual([p["code"] for p in schedule["practices"]], ["地101", "内墙201", "顶301", "踢401"])
            self.assertEqual([p["part"] for p in schedule["practices"]], ["floor", "wall", "ceiling", "skirting"])
            self.assertEqual(schedule["missing_parts"], [])
            self.assertEqual(result["summary"]["opening_codes"], 1)
            opening = result["opening_summary"][0]
            self.assertEqual(opening["code"], "M1021")
            self.assertEqual(opening["nominal_size"], ["1000", "2100"])
            self.assertEqual(opening["record_count"], 2)
            self.assertEqual(opening["block_instance_count"], 1)
            self.assertEqual(opening["explicit_count"], 3)
            self.assertEqual(opening["count_basis"], "原文数量字段")

    def test_audits_scale_conflict_and_geometry_layers(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 1000, 1000]}]},
            "text_records": [
                {"kind": "MTEXT", "text": "平面图 1:100 单位：毫米", "layer": "TITLE", "x": 100, "y": 500, "sheet": 1},
                {"kind": "MTEXT", "text": "详图 1:50", "layer": "TITLE", "x": 100, "y": 400, "sheet": 1}
            ],
            "geometry_segments": [[[0, 0, 100, 0], [0, 0, 0, 200]]],
            "geometry_layers": [["A-AXIS", "A-WALL"]],
            "files": [{"name": "drawing.dwg"}]
        }
        with tempfile.TemporaryDirectory() as temp:
            src = Path(temp) / "detail.json"
            src.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
            out = Path(temp) / "out"
            proc = subprocess.run([sys.executable, str(SCRIPT), str(src), "--out-dir", str(out)],
                                  capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            result = json.loads((out / "detail.descriptive.json").read_text(encoding="utf-8"))
            self.assertEqual(result["scale_unit_audit"][0]["status"], "conflict")
            self.assertIn("比例冲突", result["scale_unit_audit"][0]["review_reason"])
            types = {row["type"]: row for row in result["geometry_index"]}
            self.assertEqual(types["axis"]["segment_count"], 1)
            self.assertEqual(types["axis"]["total_length_drawing_units"], 100)
            self.assertEqual(types["wall"]["segment_count"], 1)
            self.assertEqual(types["wall"]["total_length_drawing_units"], 200)
            self.assertEqual(types["axis"]["file"], "drawing.dwg")

    def test_filters_concrete_grades_and_keeps_review_evidence(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 1000, 1000]}]},
            "files": [{"name": "building.dwg"}],
            "text_records": [
                {"kind": "MTEXT", "text": "C30 混凝土 C35 C40", "layer": "NOTE", "x": 100, "y": 500, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "M1021 1000x2100", "layer": "DOOR", "x": 200, "y": 450, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "办公室", "layer": "ROOM", "x": 100, "y": 400, "sheet": 1, "file": 0},
                {"kind": "MTEXT", "text": "平面图 1:100 3.6m", "layer": "TITLE", "x": 100, "y": 300, "sheet": 1, "file": 0}
            ]
        }
        with tempfile.TemporaryDirectory() as temp:
            src = Path(temp) / "detail.json"
            src.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
            out = Path(temp) / "out"
            proc = subprocess.run([sys.executable, str(SCRIPT), str(src), "--out-dir", str(out)],
                                  capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            result = json.loads((out / "detail.descriptive.json").read_text(encoding="utf-8"))
            opening_codes = [row["code"] for row in result["openings"]]
            self.assertEqual(opening_codes, ["M1021"])
            self.assertEqual(result["summary"]["room_schedules"], 0)
            self.assertIn("识别到房间词，但本行未绑定做法编号", [row["reason"] for row in result["review"]])
            self.assertEqual(result["scale_unit_audit"][0]["file"], "building.dwg")
            self.assertEqual(result["scale_unit_audit"][0]["units"], ["m"])

    def test_builds_v3_room_boundary_and_attributes_opening_to_wall_and_room(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 100, 100]}]},
            "files": [{"name": "building.dwg"}],
            "text_records": [
                {"kind": "TEXT", "text": "办公室", "layer": "ROOM", "x": 50, "y": 40, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "M1021", "layer": "DOOR", "x": 50, "y": 80, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "地101 节点A", "layer": "NOTE", "x": 60, "y": 40, "sheet": 1, "file": 0}
            ],
            "geometry_segments": [
                [[0, 0, 100, 0], [100, 0, 100, 80], [100, 80, 0, 80], [0, 80, 0, 0]]
            ],
            "geometry_layers": [["A-WALL", "A-WALL", "A-WALL", "A-WALL"]]
        }
        with tempfile.TemporaryDirectory() as temp:
            src = Path(temp) / "detail.json"
            src.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
            out = Path(temp) / "out"
            proc = subprocess.run([sys.executable, str(SCRIPT), str(src), "--out-dir", str(out)],
                                  capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            result = json.loads((out / "detail.descriptive.json").read_text(encoding="utf-8"))
            self.assertEqual(result["schema"], "cad-descriptive-geometry/v7")
            boundary = result["room_boundaries"][0]
            self.assertEqual(boundary["file"], "building.dwg")
            self.assertEqual(boundary["bbox"], [0, 0, 100, 80])
            self.assertEqual(boundary["rooms"], ["办公室"])
            opening = result["openings"][0]["geometry"]
            self.assertEqual(opening["wall_layer"], "A-WALL")
            self.assertEqual(opening["wall_distance_drawing_units"], 0.0)
            self.assertEqual(opening["room_candidates"], ["办公室"])
            self.assertEqual(opening["status"], "candidate")
            node = result["node_detail_index"][0]
            self.assertEqual(node["practice_codes"], ["地101"])
            self.assertEqual(node["node_codes"], ["A"])
            self.assertEqual(node["status"], "candidate")

    def test_segments_wall_runs_and_marks_opening_zone(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 100, 100]}]},
            "files": [{"name": "building.dwg"}],
            "text_records": [
                {"kind": "TEXT", "text": "办公室 墙高3.0m", "layer": "ROOM", "x": 50, "y": 40, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "M1021", "layer": "DOOR", "x": 50, "y": 80, "sheet": 1, "file": 0}
            ],
            "geometry_segments": [
                [[0, 0, 100, 0], [100, 0, 100, 80], [100, 80, 0, 80], [0, 80, 0, 0]],
                [[45, 80, 55, 80]]
            ],
            "geometry_layers": [
                ["A-WALL", "A-WALL", "A-WALL", "A-WALL"],
                ["A-DOOR"]
            ]
        }
        with tempfile.TemporaryDirectory() as temp:
            src = Path(temp) / "detail.json"
            src.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
            out = Path(temp) / "out"
            proc = subprocess.run([sys.executable, str(SCRIPT), str(src), "--out-dir", str(out)],
                                  capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            result = json.loads((out / "detail.descriptive.json").read_text(encoding="utf-8"))
            top = [row for row in result["wall_segments"] if row["segment"] == [45, 80, 55, 80]]
            self.assertEqual(len(top), 1)
            self.assertEqual(top[0]["segment_kind"], "opening")
            self.assertEqual(top[0]["opening_codes"], ["M1021"])
            bottom = [row for row in result["wall_segments"] if row["segment"] == [0, 0, 100, 0]]
            self.assertEqual(len(bottom), 1)
            self.assertEqual(bottom[0]["segment_kind"], "clear")
            self.assertEqual(bottom[0]["height_status"], "candidate")
            self.assertEqual(bottom[0]["status"], "candidate")

    def test_wall_segment_without_height_remains_review(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 100, 100]}]},
            "files": [{"name": "building.dwg"}],
            "text_records": [
                {"kind": "TEXT", "text": "办公室", "layer": "ROOM", "x": 50, "y": 40, "sheet": 1, "file": 0}
            ],
            "geometry_segments": [
                [[0, 0, 100, 0], [100, 0, 100, 80], [100, 80, 0, 80], [0, 80, 0, 0]]
            ],
            "geometry_layers": [["A-WALL", "A-WALL", "A-WALL", "A-WALL"]]
        }
        with tempfile.TemporaryDirectory() as temp:
            src = Path(temp) / "detail.json"
            src.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
            out = Path(temp) / "out"
            proc = subprocess.run([sys.executable, str(SCRIPT), str(src), "--out-dir", str(out)],
                                  capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            result = json.loads((out / "detail.descriptive.json").read_text(encoding="utf-8"))
            self.assertTrue(result["wall_segments"])
            self.assertTrue(all(row["status"] == "review" for row in result["wall_segments"]))
            self.assertIn("wall_segment", [row["type"] for row in result["review"]])

    def test_missing_opening_geometry_remains_review(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 100, 100]}]},
            "files": [{"name": "building.dwg"}],
            "text_records": [
                {"kind": "TEXT", "text": "M1021", "layer": "DOOR", "x": 20, "y": 20, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "M1022", "layer": "DOOR", "sheet": 1, "file": 0}
            ]
        }
        with tempfile.TemporaryDirectory() as temp:
            src = Path(temp) / "detail.json"
            src.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
            out = Path(temp) / "out"
            proc = subprocess.run([sys.executable, str(SCRIPT), str(src), "--out-dir", str(out)],
                                  capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            result = json.loads((out / "detail.descriptive.json").read_text(encoding="utf-8"))
            self.assertTrue(all(row["geometry"]["status"] == "review" for row in result["openings"]))
            review_types = [row["type"] for row in result["review"]]
            self.assertIn("opening_geometry", review_types)
            self.assertIn("evidence", review_types)


    def test_ceiling_zone_with_access_and_elevation(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 100, 100]}]},
            "files": [{"name": "building.dwg"}],
            "text_records": [
                {"kind": "TEXT", "text": "办公室 吊顶标高2.8m", "layer": "ROOM", "x": 50, "y": 40, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "检修口 600x600", "layer": "NOTE", "x": 50, "y": 35, "sheet": 1, "file": 0}
            ],
            "geometry_segments": [
                [[0, 0, 100, 0], [100, 0, 100, 80], [100, 80, 0, 80], [0, 80, 0, 0]],
                [[40, 30, 60, 30], [60, 30, 60, 40], [60, 40, 40, 40], [40, 40, 40, 30]]
            ],
            "geometry_layers": [
                ["A-CEILING", "A-CEILING", "A-CEILING", "A-CEILING"],
                ["A-CEILING-ACCESS", "A-CEILING-ACCESS", "A-CEILING-ACCESS", "A-CEILING-ACCESS"]
            ]
        }
        with tempfile.TemporaryDirectory() as temp:
            src = Path(temp) / "detail.json"
            src.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
            out = Path(temp) / "out"
            proc = subprocess.run([sys.executable, str(SCRIPT), str(src), "--out-dir", str(out)],
                                  capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            result = json.loads((out / "detail.descriptive.json").read_text(encoding="utf-8"))
            self.assertEqual(result["schema"], "cad-descriptive-geometry/v7")
            self.assertGreaterEqual(result["summary"]["ceiling_zones"], 2)
            parent = next(row for row in result["ceiling_zones"] if row["zone_kind"] == "ceiling")
            child = next(row for row in result["ceiling_zones"] if row["zone_kind"] == "ceiling_access")
            self.assertEqual(parent["elevation_candidates"][0]["value_m"], 2.8)
            self.assertEqual(child["parent_zone_id"], parent["id"])
            self.assertIn("access", parent["features"])
            self.assertEqual(parent["status"], "candidate")
            self.assertEqual(child["status"], "candidate")
            self.assertGreater(result["summary"]["ceiling_zone_candidates"], 0)

    def test_ceiling_zone_without_elevation_remains_review(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 100, 100]}]},
            "files": [{"name": "building.dwg"}],
            "text_records": [],
            "geometry_segments": [
                [[0, 0, 100, 0], [100, 0, 100, 80], [100, 80, 0, 80], [0, 80, 0, 0]]
            ],
            "geometry_layers": [["A-CEILING", "A-CEILING", "A-CEILING", "A-CEILING"]]
        }
        with tempfile.TemporaryDirectory() as temp:
            src = Path(temp) / "detail.json"
            src.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
            out = Path(temp) / "out"
            proc = subprocess.run([sys.executable, str(SCRIPT), str(src), "--out-dir", str(out)],
                                  capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            result = json.loads((out / "detail.descriptive.json").read_text(encoding="utf-8"))
            self.assertEqual(len(result["ceiling_zones"]), 1)
            zone = result["ceiling_zones"][0]
            self.assertEqual(zone["elevation_status"], "review")
            self.assertEqual(zone["status"], "review")
            self.assertIn("ceiling_zone", [row["type"] for row in result["review"]])



    def test_stair_ramp_step_drafts_keep_area_materials_and_review(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 100, 100]}]},
            "files": [{"name": "building.dwg"}],
            "text_records": [
                {"kind": "TEXT", "text": "楼梯 宽1200 踏步260x160 18级 展开面积12.5m2 花岗岩面层", "layer": "A-STAIR-NOTE", "x": 50, "y": 40, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "无障碍坡道 坡度1:12 防滑地砖", "layer": "A-RAMP-NOTE", "x": 20, "y": 20, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "室外台阶 3级 石材", "layer": "A-STEP-NOTE", "x": 80, "y": 20, "sheet": 1, "file": 0}
            ],
            "geometry_segments": [
                [[0, 30, 100, 30], [100, 30, 100, 50], [100, 50, 0, 50], [0, 50, 0, 30]],
                [[0, 0, 30, 0], [30, 0, 30, 20], [30, 20, 0, 20], [0, 20, 0, 0]],
                [[70, 0, 100, 0], [100, 0, 100, 20], [100, 20, 70, 20], [70, 20, 70, 0]]
            ],
            "geometry_layers": [
                ["A-STAIR", "A-STAIR", "A-STAIR", "A-STAIR"],
                ["A-RAMP", "A-RAMP", "A-RAMP", "A-RAMP"],
                ["A-STEP", "A-STEP", "A-STEP", "A-STEP"]
            ]
        }
        with tempfile.TemporaryDirectory() as temp:
            src = Path(temp) / "detail.json"
            src.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
            out = Path(temp) / "out"
            proc = subprocess.run([sys.executable, str(SCRIPT), str(src), "--out-dir", str(out)],
                                  capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            result = json.loads((out / "detail.descriptive.json").read_text(encoding="utf-8"))
            self.assertEqual(result["schema"], "cad-descriptive-geometry/v7")
            self.assertEqual(result["summary"]["stair_ramp_steps"], 3)
            kinds = {row["kind"] for row in result["stair_ramp_steps"]}
            self.assertEqual(kinds, {"stair", "ramp", "step"})
            stair = next(row for row in result["stair_ramp_steps"] if row["kind"] == "stair")
            self.assertEqual(stair["pending_expanded_area"]["value"], 12.5)
            self.assertEqual(stair["pending_expanded_area"]["status"], "review")
            self.assertIn("花岗岩", [item["name"] for item in stair["materials"]])
            self.assertEqual(stair["count_candidates"], [18])
            self.assertEqual(stair["status"], "review")
            self.assertIn("stair_ramp_step", [row["type"] for row in result["review"]])

    def test_stair_without_area_keeps_pending_review(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 100, 100]}]},
            "files": [{"name": "building.dwg"}],
            "text_records": [
                {"kind": "TEXT", "text": "楼梯 踏步260x160 18级", "layer": "A-STAIR-NOTE", "x": 50, "y": 40, "sheet": 1, "file": 0}
            ],
            "geometry_segments": [
                [[0, 30, 100, 30], [100, 30, 100, 50], [100, 50, 0, 50], [0, 50, 0, 30]]
            ],
            "geometry_layers": [["A-STAIR", "A-STAIR", "A-STAIR", "A-STAIR"]]
        }
        with tempfile.TemporaryDirectory() as temp:
            src = Path(temp) / "detail.json"
            src.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
            out = Path(temp) / "out"
            proc = subprocess.run([sys.executable, str(SCRIPT), str(src), "--out-dir", str(out)],
                                  capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            result = json.loads((out / "detail.descriptive.json").read_text(encoding="utf-8"))
            row = result["stair_ramp_steps"][0]
            self.assertIsNone(row["pending_expanded_area"]["value"])
            self.assertEqual(row["pending_expanded_area"]["basis"], "missing_explicit_area")
            self.assertIn("不能自动换算", row["review_reason"])



    def test_exterior_wall_zones_extract_material_thickness_and_elevation(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 100, 100]}]},
            "files": [{"name": "building.dwg"}],
            "text_records": [
                {"kind": "TEXT", "text": "外墙保温 岩棉板 厚100mm 标高+3.600m", "layer": "A-EXT-WALL-NOTE", "x": 20, "y": 20, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "防火隔离带 岩棉 厚200mm 标高+6.000m", "layer": "A-FIRE-BARRIER-NOTE", "x": 50, "y": 20, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "女儿墙内侧 保温 厚80mm 标高+18.000m", "layer": "A-PARAPET-NOTE", "x": 80, "y": 20, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "外墙 真石漆", "layer": "A-FACADE-NOTE", "x": 20, "y": 70, "sheet": 1, "file": 0}
            ],
            "geometry_segments": [
                [[0, 0, 20, 0], [20, 0, 20, 20], [20, 20, 0, 20], [0, 20, 0, 0]],
                [[30, 0, 50, 0], [50, 0, 50, 20], [50, 20, 30, 20], [30, 20, 30, 0]],
                [[60, 0, 80, 0], [80, 0, 80, 20], [80, 20, 60, 20], [60, 20, 60, 0]],
                [[0, 50, 20, 50], [20, 50, 20, 70], [20, 70, 0, 70], [0, 70, 0, 50]]
            ],
            "geometry_layers": [
                ["A-EXT-WALL", "A-EXT-WALL", "A-EXT-WALL", "A-EXT-WALL"],
                ["A-FIRE-BARRIER", "A-FIRE-BARRIER", "A-FIRE-BARRIER", "A-FIRE-BARRIER"],
                ["A-PARAPET", "A-PARAPET", "A-PARAPET", "A-PARAPET"],
                ["A-FACADE-FINISH", "A-FACADE-FINISH", "A-FACADE-FINISH", "A-FACADE-FINISH"]
            ]
        }
        with tempfile.TemporaryDirectory() as temp:
            src = Path(temp) / "detail.json"
            src.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
            out = Path(temp) / "out"
            proc = subprocess.run([sys.executable, str(SCRIPT), str(src), "--out-dir", str(out)],
                                  capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            result = json.loads((out / "detail.descriptive.json").read_text(encoding="utf-8"))
            self.assertEqual(result["schema"], "cad-descriptive-geometry/v7")
            self.assertEqual(result["summary"]["exterior_wall_zones"], 4)
            kinds = {row["zone_kind"] for row in result["exterior_wall_zones"]}
            self.assertTrue({"insulation", "fire_barrier", "parapet_inner", "facade_finish"}.issubset(kinds))
            insulation = next(row for row in result["exterior_wall_zones"] if row["zone_kind"] == "insulation")
            self.assertEqual(insulation["thickness_candidates"][0]["value_mm"], 100.0)
            self.assertEqual(insulation["elevation_candidates"][0]["value_m"], 3.6)
            self.assertIn("岩棉", [item["name"] for item in insulation["materials"]])
            self.assertEqual(insulation["status"], "candidate")

    def test_exterior_wall_zone_without_geometry_remains_review(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 100, 100]}]},
            "files": [{"name": "building.dwg"}],
            "text_records": [
                {"kind": "TEXT", "text": "外墙保温 岩棉板 厚100mm 标高+3.600m", "layer": "A-EXT-WALL-NOTE", "x": 20, "y": 20, "sheet": 1, "file": 0}
            ]
        }
        with tempfile.TemporaryDirectory() as temp:
            src = Path(temp) / "detail.json"
            src.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
            out = Path(temp) / "out"
            proc = subprocess.run([sys.executable, str(SCRIPT), str(src), "--out-dir", str(out)],
                                  capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            result = json.loads((out / "detail.descriptive.json").read_text(encoding="utf-8"))
            row = result["exterior_wall_zones"][0]
            self.assertEqual(row["status"], "review")
            self.assertEqual(row["geometry"]["status"], "review")
            self.assertIn("未找到匹配", row["review_reason"])
            self.assertIn("exterior_wall_zone", [item["type"] for item in result["review"]])



if __name__ == "__main__":
    unittest.main()
