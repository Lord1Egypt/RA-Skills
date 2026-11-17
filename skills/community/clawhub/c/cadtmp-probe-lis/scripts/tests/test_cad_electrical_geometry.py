#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2]
SCRIPT = SKILL_DIR / "scripts" / "cad_electrical_geometry.py"


class ElectricalGeometryTest(unittest.TestCase):
    def run_script(self, detail: dict, out_name: str = "out") -> tuple[dict, Path]:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        src = root / "detail.json"
        src.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
        out = root / out_name
        import subprocess
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(src), "--out-dir", str(out)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads((out / "detail.electrical.json").read_text(encoding="utf-8")), out

    def test_extracts_electrical_systems_routes_circuits_equipment_lightning(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 10000, 10000]}]},
            "files": [{"name": "电气.dwg"}],
            "text_records": [
                {"kind": "TEXT", "text": "照明平面图 1:100 单位：mm", "layer": "TITLE", "x": 100, "y": 9900, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "WL1 回路", "layer": "E-CIRCUIT", "x": 1000, "y": 1000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "WDZ-BYJ-3X2.5-PC20", "layer": "E-WIRE", "x": 1100, "y": 1000, "sheet": 1, "file": 0},
                {"kind": "INSERT", "text": "配电箱 AL1", "layer": "E-EQUIP", "x": 1500, "y": 1500, "sheet": 1, "file": 0},
                {"kind": "INSERT", "text": "应急灯", "layer": "E-EQUIP", "x": 1600, "y": 1500, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "引下线 测试卡", "layer": "E-LIGHTNING", "x": 2000, "y": 2000, "sheet": 1, "file": 0},
            ],
            "geometry_segments": [[[0, 0, 1000, 0], [1000, 0, 1000, 1000]]],
            "geometry_layers": [["E-TRAY-JDG", "E-TRAY-JDG"]],
        }
        result, out = self.run_script(detail)
        self.assertEqual(result["schema"], "cad-electrical-geometry/v1")
        self.assertEqual(result["summary"]["drawing_types"], 1)
        self.assertEqual(result["summary"]["route_segments"], 2)
        self.assertEqual(result["summary"]["equipment"], 3)
        self.assertEqual(result["summary"]["circuits"], 1)
        self.assertEqual(result["summary"]["specs"], 1)
        self.assertEqual(result["summary"]["lightning"], 1)
        systems = {row["system"] for row in result["systems"]}
        self.assertIn("lighting", systems)
        self.assertEqual(result["route_segments"][0]["route_class"], "conduit")
        equipment_by_name = {row["name"]: row for row in result["equipment"]}
        self.assertEqual(equipment_by_name["配电箱 AL1"]["category"], "distribution_box")
        self.assertEqual(equipment_by_name["应急灯"]["category"], "emergency_device")
        self.assertEqual(result["circuits"][0]["circuit_id"], "WL1")
        self.assertEqual(result["circuits"][0]["system"], "lighting")
        self.assertEqual(result["lightning"][0]["system"], "lightning_protection")
        self.assertIn("不输出工程量", result["boundary"])
        self.assertNotIn("quantity", result)
        self.assertNotIn("material_quantity", result)
        contract = result["contract"]
        self.assertEqual(contract["schema"], "cad-file-reader/v0")
        self.assertGreater(contract["summary"]["total"], 0)
        self.assertTrue(all(row["final_quantity"] is False for row in contract["candidates"] + contract["review_candidates"]))
        self.assertTrue((out / "detail.electrical.md").exists())
        self.assertTrue((out / "detail.electrical.csv").exists())

    def test_missing_scale_and_geometry_enter_review(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 1000, 1000]}]},
            "files": [{"name": "电气.dwg"}],
            "text_records": [
                {"kind": "TEXT", "text": "电气平面图 单位：mm", "layer": "TITLE", "x": 10, "y": 10, "sheet": 1, "file": 0},
            ],
        }
        result, _out = self.run_script(detail)
        review_types = {row["type"] for row in result["review"]}
        self.assertIn("scale_unit", review_types)
        self.assertIn("input_geometry", review_types)
        self.assertEqual(result["summary"]["route_segments"], 0)
        self.assertTrue(result["boundary"].startswith("只输出电气识图候选"))

    def test_lightning_without_geometry_goes_review(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 1000, 1000]}]},
            "files": [{"name": "电气.dwg"}],
            "text_records": [
                {"kind": "TEXT", "text": "防雷平面图 1:100 单位：mm", "layer": "TITLE", "x": 10, "y": 10, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "引下线", "layer": "", "x": 20, "y": 20, "sheet": 1, "file": 0},
            ],
        }
        result, _out = self.run_script(detail)
        lightning = result["lightning"]
        self.assertTrue(lightning)
        self.assertEqual(lightning[0]["status"], "review")



    def test_fire_weak_current_intelligent_domains(self):
        detail = {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 10000, 10000]}]},
            "files": [{"name": "消防弱电.dwg"}],
            "text_records": [
                {"kind": "TEXT", "text": "消防平面图 1:100 单位：mm", "layer": "TITLE", "x": 100, "y": 9900, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "火灾自动报警 1:100 单位：mm", "layer": "E-FAS", "x": 1000, "y": 1000, "sheet": 1, "file": 0},
                {"kind": "INSERT", "text": "感烟探测器", "layer": "E-FIRE", "x": 1100, "y": 1100, "sheet": 1, "file": 0},
                {"kind": "INSERT", "text": "防火卷帘", "layer": "E-FIRE", "x": 1110, "y": 1110, "sheet": 1, "file": 0},
                {"kind": "INSERT", "text": "消防泵", "layer": "E-FIRE", "x": 1120, "y": 1120, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "综合布线平面 1:100 单位：mm", "layer": "E-PDS", "x": 2000, "y": 2000, "sheet": 1, "file": 0},
                {"kind": "INSERT", "text": "信息点", "layer": "E-WEAK", "x": 2100, "y": 2100, "sheet": 1, "file": 0},
                {"kind": "INSERT", "text": "网络机柜", "layer": "E-WEAK", "x": 2110, "y": 2110, "sheet": 1, "file": 0},
                {"kind": "INSERT", "text": "门禁读卡器", "layer": "E-WEAK", "x": 2120, "y": 2120, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "智能化平面 1:100 单位：mm", "layer": "E-BAS", "x": 3000, "y": 3000, "sheet": 1, "file": 0},
                {"kind": "INSERT", "text": "DDC", "layer": "E-BAS", "x": 3100, "y": 3100, "sheet": 1, "file": 0},
                {"kind": "INSERT", "text": "智能面板", "layer": "E-BAS", "x": 3110, "y": 3110, "sheet": 1, "file": 0},
            ],
            "geometry_segments": [[[0, 0, 500, 0], [500, 0, 500, 500]]],
            "geometry_layers": [["E-FIRE-LOOP", "E-SIGNAL-BUS"]],
        }
        result, _out = self.run_script(detail)
        summary = result["summary"]
        self.assertGreater(summary["fire_protection"], 0)
        self.assertGreater(summary["weak_current"], 0)
        self.assertGreater(summary["intelligent_building"], 0)
        fire_rows = result["fire_protection"]
        systems = {row.get("system") for row in fire_rows}
        self.assertTrue(systems & {"fire_alarm", "fire_pump", "fire_linking"})
        weak_sys = {row.get("system") for row in result["weak_current"]}
        self.assertTrue(weak_sys & {"pds", "access_control", "information_network", "weak_current_other"})
        intel_sys = {row.get("system") for row in result["intelligent_building"]}
        self.assertTrue(intel_sys & {"building_automation", "smart_lighting", "ibms", "weak_current_other"})
        route_sys = {row.get("route_class") for row in result["route_segments"]}
        self.assertTrue(route_sys & {"fire_loop", "signal_bus"})
        contract = result["contract"]
        contract_sections = {row.get("section") for row in contract["candidates"] + contract["review_candidates"]}
        self.assertTrue(contract_sections & {"fire_protection", "weak_current", "intelligent_building"})


if __name__ == "__main__":
    unittest.main()
