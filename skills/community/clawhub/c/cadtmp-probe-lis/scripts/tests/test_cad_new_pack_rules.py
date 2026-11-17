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


def make_detail(kind):
    if kind == "bridge":
        return {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 50000, 50000]}]},
            "files": [{"name": "桥型布置.dwg"}],
            "text_records": [
                {"kind": "TEXT", "text": "桥型布置 1:100 单位：mm", "layer": "TITLE", "x": 1000, "y": 49000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "桥墩 ZA-01 支座", "layer": "BRIDGE-PIER", "x": 2000, "y": 30000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "K1+250 路线中线", "layer": "ROAD-LINE", "x": 3000, "y": 20000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "隧道洞口 明洞", "layer": "TUNNEL-PORTAL", "x": 4000, "y": 10000, "sheet": 1, "file": 0},
            ],
            "geometry_segments": [[[0, 0, 40000, 0], [40000, 0, 40000, 40000]]],
            "geometry_layers": [["BRIDGE-BEAM", "ROAD-LINE"]],
        }
    if kind == "pile":
        return {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 30000, 30000]}]},
            "files": [{"name": "桩基平面.dwg"}],
            "text_records": [
                {"kind": "TEXT", "text": "桩基平面 1:100 单位：mm", "layer": "TITLE", "x": 1000, "y": 29000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "PHC 桩 P01 承台", "layer": "PILE", "x": 2000, "y": 20000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "基坑支护 锚索 内支撑", "layer": "SUPPORT", "x": 3000, "y": 10000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "挡土墙 边坡 标高 2.900", "layer": "SLOPE", "x": 4000, "y": 5000, "sheet": 1, "file": 0},
            ],
            "geometry_segments": [[[0, 0, 20000, 0], [20000, 0, 20000, 20000]]],
            "geometry_layers": [["PILE-ZHUANG", "SUPPORT"]],
        }

    if kind == "dwsw":
        return {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 50000, 50000]}]},
            "files": [{"name": "门窗楼梯保温防水.dwg"}],
            "text_records": [
                {"kind": "TEXT", "text": "门窗表 1:100 单位：mm", "layer": "TITLE", "x": 1000, "y": 49000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "FM01 防火门 窗 C1", "layer": "DOOR", "x": 2000, "y": 30000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "楼梯梯段 踏步 扶手", "layer": "STAIR", "x": 3000, "y": 20000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "外墙保温 挤塑板 防水卷材", "layer": "INSUL-WATER", "x": 4000, "y": 10000, "sheet": 1, "file": 0},
            ],
            "geometry_segments": [[[0, 0, 40000, 0], [40000, 0, 40000, 40000]]],
            "geometry_layers": [["DOOR", "INSUL"]],
        }
    if kind == "firegreen":
        return {
            "meta": {"sheets": [{"id": 1, "bbox": [0, 0, 50000, 50000]}]},
            "files": [{"name": "防火节能绿建.dwg"}],
            "text_records": [
                {"kind": "TEXT", "text": "防火分区 FH-01 疏散路线 1:100 单位：mm", "layer": "TITLE", "x": 1000, "y": 49000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "防火门 FM 防火卷帘", "layer": "FIRE", "x": 2000, "y": 30000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "无障碍坡道 无障碍卫生间", "layer": "ACCESSIBLE", "x": 3000, "y": 20000, "sheet": 1, "file": 0},
                {"kind": "TEXT", "text": "光伏板 节能层 雨水花园", "layer": "GREEN-ENERGY", "x": 4000, "y": 10000, "sheet": 1, "file": 0},
            ],
            "geometry_segments": [[[0, 0, 40000, 0], [40000, 0, 40000, 40000]]],
            "geometry_layers": [["FIRE-ZONE", "GREEN"]],
        }



class NewPackRulesTest(unittest.TestCase):
    def run_pack(self, detail, pack, suffix, schema, geo_key):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src = root / "detail.json"
            src.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
            out = root / "out"
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), str(src), "--pack", pack, "--out-dir", str(out)],
                capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = json.loads((out / f"detail.{suffix}.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["schema"], schema)
            self.assertGreaterEqual(payload["summary"]["drawing_types"], 1)
            self.assertGreaterEqual(payload["summary"]["systems"], 1)
            self.assertGreaterEqual(payload["summary"]["components"], 1)
            self.assertGreaterEqual(payload["summary"]["references"], 1)
            self.assertIn("不输出", payload["boundary"])
            self.assertGreaterEqual(len(payload[geo_key]), 1)
            cands = payload["contract"]["candidates"] + payload["contract"]["review_candidates"]
            self.assertTrue(all(row["final_quantity"] is False for row in cands))

    def test_bridge_tunnel_road_traffic_pack(self):
        self.run_pack(make_detail("bridge"), "bridge_tunnel_road_traffic", "bridge_tunnel_road_traffic", "cad-bridge-tunnel-road-traffic/v1", "bridge_tunnel_road_traffic")

    def test_pile_foundation_slope_pack(self):
        self.run_pack(make_detail("pile"), "pile_foundation_slope", "pile_foundation_slope", "cad-pile-foundation-slope/v1", "pile_foundation_slope_geometry")

    def test_doors_windows_stairs_insulation_waterproof_pack(self):
        self.run_pack(make_detail("dwsw"), "doors_windows_stairs_insulation_waterproof", "doors_windows_stairs_insulation_waterproof", "cad-doors-windows-stairs-insulation-waterproof/v1", "doors_windows_stairs_insulation_waterproof")

    def test_fire_prevention_accessibility_green_energy_pack(self):
        self.run_pack(make_detail("firegreen"), "fire_prevention_accessibility_green_energy", "fire_prevention_accessibility_green_energy", "cad-fire-prevention-accessibility-green-energy/v1", "fire_prevention_accessibility_green_energy_geometry")


if __name__ == "__main__":
    unittest.main()
