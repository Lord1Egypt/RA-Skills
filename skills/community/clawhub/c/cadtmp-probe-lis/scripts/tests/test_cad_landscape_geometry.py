#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2]
SCRIPT = SKILL_DIR / "scripts" / "cad_landscape_geometry.py"


def circle_segments(cx, cy, r, n=24):
    pts = []
    for i in range(n):
        ang = 2.0 * math.pi * i / n
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return [[round(pts[i][0], 3), round(pts[i][1], 3),
             round(pts[(i + 1) % n][0], 3), round(pts[(i + 1) % n][1], 3)] for i in range(n)]


def rectangle_segments(x1, y1, x2, y2):
    return [[x1, y1, x2, y1], [x2, y1, x2, y2], [x2, y2, x1, y2], [x1, y2, x1, y1]]


def make_detail():
    # 硬景：一个大闭合环（2000x2000，主环）+ 一个细缝小环（过滤项）
    segs = rectangle_segments(0.0, 0.0, 2000.0, 2000.0)
    segs += rectangle_segments(100.0, 100.0, 200.0, 200.0)
    layers = ["景观铺地"] * 8
    return {
        "files": [{"name": "landscape.dwg"}],
        "text_records": [
            {"kind": "TEXT", "text": "种植平面图 1:500 单位：mm", "layer": "TITLE", "x": 100, "y": 9000, "sheet": 1, "file": 0},
            {"kind": "TEXT", "text": "国槐 胸径12cm", "layer": "苗木表", "x": 200, "y": 8000, "sheet": 1, "file": 0},
            {"kind": "TEXT", "text": "紫薇 高度2m", "layer": "苗木表", "x": 210, "y": 7800, "sheet": 1, "file": 0},
            # 无意义块名：交给几何指纹判定
            {"kind": "INSERT", "text": "GC200", "x": 1000.0, "y": 1000.0, "layer": "苗木", "file": 0},
            {"kind": "INSERT", "text": "GC200", "x": 3000.0, "y": 1000.0, "layer": "苗木", "file": 0},
            {"kind": "INSERT", "text": "GC200", "x": 5000.0, "y": 1000.0, "layer": "苗木", "file": 0},
        ],
        "meta": {
            "block_refs": {"乔-国槐": 12, "灌-紫薇": 8, "T-银杏": 3, "停车位01": 445, "GC200": 3},
            "insert_count": 500,
        },
        "layers": ["景观铺地", "铺装面积", "L-波打", "地被层-1", "苗木"],
        "geometry_segments": [segs],
        "geometry_layers": [layers],
    }


def make_fingerprint_detail():
    segs = []
    layers = []
    # 乔木：3 个大圆（无意义块 GC200）
    for i, cx in enumerate((1000.0, 3000.0, 5000.0)):
        segs += circle_segments(cx, 1000.0, 300.0)
        layers += ["苗木"] * 24
    # 灌木：3 组双圆（GC88）
    for i, cx in enumerate((1000.0, 3000.0, 5000.0)):
        segs += circle_segments(cx, 6000.0, 100.0)
        segs += circle_segments(cx + 300.0, 6000.0, 100.0)
        layers += ["苗木"] * 48
    # 地被/绿篱：3 条长条带（GC66）
    for i, cx in enumerate((1000.0, 4000.0, 7000.0)):
        segs += rectangle_segments(cx, 11000.0, cx + 800.0, 11050.0)
        layers += ["地被层-1"] * 4
    # 硬景：两个相邻大闭合环 → 应聚成一个区块候选
    segs += rectangle_segments(0.0, 15000.0, 2000.0, 17000.0)
    segs += rectangle_segments(1600.0, 15000.0, 3600.0, 17000.0)
    layers += ["景观铺地"] * 8
    inserts = [
        {"kind": "INSERT", "text": "GC200", "x": 1000.0, "y": 1000.0, "layer": "苗木", "file": 0},
        {"kind": "INSERT", "text": "GC200", "x": 3000.0, "y": 1000.0, "layer": "苗木", "file": 0},
        {"kind": "INSERT", "text": "GC200", "x": 5000.0, "y": 1000.0, "layer": "苗木", "file": 0},
        {"kind": "INSERT", "text": "GC88", "x": 1000.0, "y": 6000.0, "layer": "苗木", "file": 0},
        {"kind": "INSERT", "text": "GC88", "x": 3000.0, "y": 6000.0, "layer": "苗木", "file": 0},
        {"kind": "INSERT", "text": "GC88", "x": 5000.0, "y": 6000.0, "layer": "苗木", "file": 0},
        {"kind": "INSERT", "text": "GC66", "x": 1400.0, "y": 11025.0, "layer": "地被层-1", "file": 0},
        {"kind": "INSERT", "text": "GC66", "x": 4400.0, "y": 11025.0, "layer": "地被层-1", "file": 0},
        {"kind": "INSERT", "text": "GC66", "x": 7400.0, "y": 11025.0, "layer": "地被层-1", "file": 0},
    ]
    return {
        "files": [{"name": "landscape.dwg"}],
        "text_records": [{"kind": "TEXT", "text": "种植平面图", "layer": "TITLE", "x": 10, "y": 10, "file": 0}] + inserts,
        "meta": {"block_refs": {k: 3 for k in ("GC200", "GC88", "GC66")}, "insert_count": 9},
        "layers": ["苗木", "地被层-1"],
        "geometry_segments": [segs],
        "geometry_layers": [layers],
    }


class LandscapeGeometryTest(unittest.TestCase):
    def run_script(self, detail):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        src = root / "detail.json"
        src.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
        out = root / "out"
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), str(src), "--out-dir", str(out)],
            capture_output=True, text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return json.loads((out / "detail.landscape.json").read_text(encoding="utf-8")), out

    def test_plant_text_block_and_paving(self):
        result, out = self.run_script(make_detail())
        self.assertEqual(result["schema"], "cad-landscape-geometry/v1")
        self.assertGreaterEqual(result["summary"]["plant_legends"], 1)
        self.assertGreaterEqual(result["summary"]["plant_block_legends"], 2)
        categories = {row["category"] for row in result["plant_block_legends"]}
        self.assertTrue("乔木" in categories or "灌木" in categories)
        paving = {row["layer"]: row for row in result["paving_closed_areas"]}
        row = paving.get("景观铺地")
        self.assertIsNotNone(row)
        self.assertEqual(row["status"], "candidate")
        self.assertGreaterEqual(row["closed_ring_candidates"], 1)
        # 小环应被过滤到 filtered 项
        self.assertGreaterEqual(row.get("filtered_ring_candidates", 0), 1)
        contract = result["contract"]
        for item in contract["candidates"] + contract["review_candidates"]:
            self.assertIs(item["final_quantity"], False)
        self.assertTrue((out / "detail.landscape.md").exists())
        self.assertTrue((out / "detail.landscape.csv").exists())

    def test_no_geometry_enters_review_or_empty(self):
        detail = make_detail()
        detail["geometry_segments"] = []
        detail["geometry_layers"] = []
        result, _out = self.run_script(detail)
        self.assertEqual(result["summary"]["paving_closed_areas"], 0)

    def test_plant_schedule_link_and_region_anchor(self):
        detail = make_fingerprint_detail()
        # 苗木表文字靠近 GC88（灌木双圆）所在插入点
        detail["text_records"].append({"kind": "TEXT", "text": "紫薇 高度2m", "layer": "苗木表",
                                       "x": 1000.0, "y": 5900.0, "file": 0, "sheet": 1})
        result, out = self.run_script(detail)
        links = result.get("plant_schedule_links") or []
        fp_rows = {r.get("name"): r for r in result.get("plant_block_fingerprints") or []}
        # 灌木块应有回溯（紫薇=灌木一致）
        gc88 = fp_rows.get("GC88")
        self.assertIsNotNone(gc88)
        self.assertEqual(gc88.get("link_status"), "consistent", gc88)
        # 硬景含大环的区块应带复核锚点
        pav = next((r for r in result["paving_closed_areas"] if r.get("region_candidates")), None)
        self.assertIsNotNone(pav)
        self.assertIn("review_label", pav["region_candidates"][0])
        self.assertIn("anchor_center", pav["region_candidates"][0])
        contract = result["contract"]
        for item in contract["candidates"] + contract["review_candidates"]:
            self.assertIs(item["final_quantity"], False)

    def test_block_geom_prefers_block_definition(self):
        detail = make_fingerprint_detail()
        # 用块定义几何覆盖 GC200：单 INSERT + 块内大圆也能稳定判乔木
        block_segs = circle_segments(0.0, 0.0, 300.0)
        detail["meta"]["block_geometries"] = {"GC200": {"segments": block_segs, "layers": ["苗木"] * 24}}
        inserts = [r for r in detail["text_records"] if r["kind"] == "INSERT" and r["text"] == "GC200"]
        # 只保留一个 GC200 插入点也不应被 min_instances 拦掉
        detail["text_records"] = [r for r in detail["text_records"] if not (r["kind"] == "INSERT" and r["text"] == "GC200")]
        detail["text_records"] += inserts[:1]
        result, _out = self.run_script(detail)
        fps = {r.get("name"): r for r in result.get("plant_block_fingerprints") or []}
        self.assertTrue("GC200" in fps, fps)
        self.assertEqual(fps["GC200"]["category"], "乔木")
        self.assertTrue(any(ev.get("supports", [{}])[0].get("source") == "block_definition"
                            for ev in (fps["GC200"].get("evidence") or [])))

    def test_block_geom_fingerprint(self):
        result, _out = self.run_script(make_fingerprint_detail())
        fps = result.get("plant_block_fingerprints") or []
        self.assertGreaterEqual(len(fps), 3, fps)
        by_name = {row.get("name"): row for row in fps}
        self.assertTrue("GC200" in by_name)
        self.assertEqual(by_name["GC200"]["category"], "乔木")
        self.assertTrue("GC88" in by_name)
        self.assertEqual(by_name["GC88"]["category"], "灌木")
        self.assertTrue("GC66" in by_name)
        self.assertEqual(by_name["GC66"]["category"], "地被")
        for row in fps:
            self.assertTrue(row["instance_count"] >= 3)
            self.assertIn(row["method"], ("block_geom_fingerprint",))
        contract = result["contract"]
        for item in contract["candidates"] + contract["review_candidates"]:
            self.assertIs(item["final_quantity"], False)


    def test_block_legend_has_schedule_link(self):
        detail = make_detail()
        # 给块名候选补上坐标，让块名图例也能与苗木表交叉验证（不只是几何指纹）
        detail["text_records"] += [
            {"kind": "INSERT", "text": "乔-国槐", "x": 200.0, "y": 8000.0, "layer": "苗木", "file": 0, "sheet": 1},
            {"kind": "INSERT", "text": "灌-紫薇", "x": 210.0, "y": 7800.0, "layer": "苗木", "file": 0, "sheet": 1},
        ]
        result, _out = self.run_script(detail)
        blocks = {r.get("name") or r.get("plant"): r for r in result.get("plant_block_legends") or []}
        guohuai = blocks.get("乔-国槐")
        self.assertIsNotNone(guohuai)
        self.assertEqual(guohuai["category"], "乔木")
        self.assertEqual(guohuai.get("link_status"), "consistent", guohuai)
        # 交叉验证表应包含块名图例条目
        links = result.get("plant_schedule_links") or []
        self.assertTrue(any(r.get("block_name") == "乔-国槐" for r in links), links)
        contract = result["contract"]
        for item in contract["candidates"] + contract["review_candidates"]:
            self.assertIs(item["final_quantity"], False)


    def test_green_area_closed_ring_and_contract(self):
        detail = make_detail()
        # 在地被层加一个闭合矩形，应生成“绿地/地被闭合域”候选（不算量）
        detail["geometry_segments"][0] += rectangle_segments(0.0, 12000.0, 1500.0, 13500.0)
        detail["geometry_layers"][0] += ["地被层"] * 4
        result, _out = self.run_script(detail)
        greens = {r["layer"]: r for r in result.get("green_area_candidates") or []}
        self.assertIn("地被层", greens)
        self.assertGreaterEqual(greens["地被层"]["closed_ring_candidates"], 1, greens["地被层"])
        self.assertEqual(greens["地被层"]["status"], "candidate")
        contract = result["contract"]
        for item in contract["candidates"] + contract["review_candidates"]:
            self.assertIs(item["final_quantity"], False)


    def test_pdf_geometry_review_candidates(self):
        detail = make_detail()
        detail["pdf_geometry_segments"] = [
            {"page": 2, "segments": [[0, 0, 100, 0], [100, 0, 100, 100]]},
            {"page": 3, "segments": [[0, 0, 200, 0], [200, 0, 200, 200]]},
        ]
        result, _out = self.run_script(detail)
        rows = result.get("pdf_geometry_candidates") or []
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["status"], "review")
        self.assertIn("pdf_no_layer_geometry", rows[0]["review_reasons"])
        self.assertEqual(rows[0]["page"], 2)
        self.assertGreaterEqual(rows[0]["segment_count"], 2)
        contract = result["contract"]
        for item in contract["candidates"] + contract["review_candidates"]:
            self.assertIs(item["final_quantity"], False)


    def test_plant_legend_spec_extraction(self):
        detail = make_detail()
        detail["text_records"][1] = {"kind": "TEXT", "text": "苗木图例  1-10 香樟  φ15cm", "layer": "苗木表", "x": 200, "y": 8000, "sheet": 1, "file": 0}
        detail["text_records"][2] = {"kind": "TEXT", "text": "地被图例  小叶黄杨  25盆/m2", "layer": "苗木表", "x": 210, "y": 7800, "sheet": 1, "file": 0}
        result, _out = self.run_script(detail)
        rows = {r.get("plant"): r for r in result["plant_legends"]}
        self.assertIn("香樟", rows, rows.keys())
        self.assertEqual(rows["香樟"]["spec"], "φ15cm")
        self.assertIn("小叶黄杨", rows, rows.keys())
        self.assertEqual(rows["小叶黄杨"]["spec"], "25盆/m2")
        self.assertTrue(all("苗木图例" not in r.get("plant","") for r in result["plant_legends"]), [r.get("plant") for r in result["plant_legends"]])

    def test_plant_coverage_audit_unclassified(self):
        detail = make_detail()
        detail["text_records"][1] = {"kind": "TEXT", "text": "苗木图例 1-10 奇楠树 φ15cm", "layer": "苗木表", "x": 200, "y": 8000, "file": 0}
        result, _out = self.run_script(detail)
        audit = result.get("audit") or {}
        top = {x["word"]: x for x in audit.get("top") or []}
        self.assertIn("奇楠树", top, top.keys())
        self.assertGreaterEqual(audit.get("unclassified_legend_words", 0), 1)

    def test_plant_coverage_audit_ignores_header_words(self):
        detail = make_detail()
        detail["text_records"] = [
            {"kind": "TEXT", "text": "植物配置图", "layer": "TITLE", "x": 10, "y": 10, "file": 0},
            {"kind": "TEXT", "text": "苗木图例 1-10 奇楠树 φ15cm", "layer": "苗木表", "x": 200, "y": 8000, "file": 0},
        ]
        result, _out = self.run_script(detail)
        audit = result.get("audit") or {}
        top = {x["word"] for x in audit.get("top") or []}
        self.assertNotIn("植物配置图", top, top)
        self.assertIn("奇楠树", top, top)

    def test_plant_english_alias_classification(self):
        detail = make_detail()
        detail["text_records"] = [
            {"kind": "TEXT", "text": "Tree 1-10 Magnolia 15cm", "layer": "苗木表", "x": 200, "y": 8000, "file": 0},
            {"kind": "TEXT", "text": "Shrub Viburnum 2m", "layer": "灌木", "x": 210, "y": 7800, "file": 0},
            {"kind": "TEXT", "text": "Groundcover lawn 25m2", "layer": "地被", "x": 220, "y": 7600, "file": 0},
        ]
        result, _out = self.run_script(detail)
        cats = {r["category"] for r in result["plant_legends"]}
        self.assertIn("乔木", cats)
        self.assertIn("灌木", cats)
        self.assertIn("地被", cats)


if __name__ == "__main__":
    unittest.main()


class SplitRulesTests(unittest.TestCase):
    def test_load_rules_merges_theme_files(self):
        import sys as _sys
        _sys.path.insert(0, str(SKILL_DIR / "scripts"))
        from cad_common import load_rules
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            (td / "rules.json").write_text(json.dumps({"a": [1], "m": {"x": 1}}), encoding="utf-8")
            (td / "rules").mkdir()
            (td / "rules" / "plants.json").write_text(
                json.dumps({"a": [2], "m": {"y": 2}, "z": 3}), encoding="utf-8")
            d = load_rules(td / "rules.json")
            self.assertEqual(d["a"], [2])
            self.assertEqual(d["m"], {"x": 1, "y": 2})
            self.assertEqual(d["z"], 3)


class PlantExcludePhraseTests(unittest.TestCase):
    def test_plant_classify_excludes_nonplant_phrases(self):
        import sys as _sys
        _sys.path.insert(0, str(SKILL_DIR / "scripts"))
        from cad_common import load_rules
        from cad_landscape_geometry import plant_classify
        rules = load_rules(SKILL_DIR / "packs/landscape-geometry/rules.json")
        for txt in ("花砖", "地址：山东省济南…", "建设银行济南槐荫支行阳光新城分理处",
                    "树形饱满，舒展", "主景树,分枝点2.5-3.0m", "黄河路桥宿舍"):
            self.assertEqual(plant_classify(txt, rules), ("", ""), txt)
        # 真实植物仍命中
        self.assertEqual(plant_classify("国槐", rules)[0], "乔木")
        self.assertEqual(plant_classify("紫薇", rules)[0], "灌木")
        self.assertEqual(plant_classify("云 杉", rules)[0], "乔木")
        self.assertEqual(plant_classify("晚樱", rules)[0], "乔木")
        self.assertEqual(plant_classify("兰花鼠尾草", rules)[0], "地被")
