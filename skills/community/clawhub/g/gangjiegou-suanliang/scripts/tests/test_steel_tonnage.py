#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""steel_tonnage 钢结构吨位估算测试（合成数据）。"""
import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import steel_tonnage as S  # noqa: E402


def steel_json(sections=None, members=None, geometry=None):
    return {"schema": "cad-steel-geometry/v1",
            "sections": sections or [], "members": members or [],
            "steel_geometry": geometry or []}


def sec(stype, text):
    return {"type": "section", "section_type": stype, "text": text,
            "evidence": [{"text": text}]}


def conn(category, text, **kwargs):
    row = {"type": "connection", "category": category, "raw": text,
           "evidence": [{"text": text}]}
    row.update(kwargs)
    return row


def fin(category, text):
    return {"type": "finish", "category": category, "raw": text,
            "evidence": [{"text": text}]}


class TestUnitWeight(unittest.TestCase):
    def test_h_section_4_parts(self):
        # HN400x200x8x13：A = 2*200*13 + (400-26)*8 = 8192 mm² → 64.31 kg/m（查表 65.4，偏差 -1.7%）
        p = S.parse_section(sec("h_section", "HN400x200x8x13"))
        self.assertAlmostEqual(p["kg_m"], 64.31, places=1)

    def test_h_section_2_parts_count_only(self):
        p = S.parse_section(sec("h_section", "H400x200"))
        self.assertEqual(p["kg_m"], 0.0)
        self.assertIn("仅计数", p["note"])

    def test_tube_with_wall(self):
        # Φ180x6：(180-6)*π*6*0.00785 ≈ 25.75
        p = S.parse_section(sec("tube", "Φ180x6"))
        self.assertAlmostEqual(p["kg_m"], 25.75, places=1)

    def test_tube_solid_fallback(self):
        # Φ25 无壁厚 → 实心圆钢 π/4*625*0.00785 ≈ 3.85
        p = S.parse_section(sec("tube", "Φ25"))
        self.assertAlmostEqual(p["kg_m"], 3.85, places=1)

    def test_rect_tube(self):
        # □100x100x4：(2*200-16)*4*0.00785 ≈ 12.06
        p = S.parse_section(sec("rect_tube", "□100x100x4"))
        self.assertAlmostEqual(p["kg_m"], 12.06, places=1)

    def test_angle_equal_leg(self):
        # L100x8：(200-8)*8*0.00785 ≈ 12.06
        p = S.parse_section(sec("angle", "L100x8"))
        self.assertAlmostEqual(p["kg_m"], 12.06, places=1)

    def test_purlin(self):
        # C200x70x20x2.5：(200+140)*2.5*0.00785 ≈ 6.67
        p = S.parse_section(sec("purlin_section", "C200x70x20x2.5"))
        self.assertAlmostEqual(p["kg_m"], 6.67, places=1)

    def test_channel_number_from_table(self):
        # [16 → GB/T 706 槽钢 16a = 17.24 kg/m（补表后可进吨位）
        p = S.parse_section(sec("channel", "[16"))
        self.assertAlmostEqual(p["kg_m"], 17.24, places=2)
        self.assertIn("GB/T 706", p["note"])

    def test_channel_letter_from_table(self):
        p = S.parse_section(sec("channel", "槽钢25b"))
        self.assertAlmostEqual(p["kg_m"], 31.335, places=2)

    def test_channel_with_dims_formula(self):
        # [200x75x9：2*75*9 + (200-18)*9 = 2988 mm² → 23.46 kg/m
        p = S.parse_section(sec("channel", "[200x75x9"))
        self.assertAlmostEqual(p["kg_m"], 23.46, places=1)

    def test_i_beam_from_table(self):
        # 工20a → GB/T 706 工字钢 27.929 kg/m
        p = S.parse_section(sec("", "工20a"))
        self.assertEqual(p["section_type"], "i_section")
        self.assertAlmostEqual(p["kg_m"], 27.929, places=2)

    def test_table_miss_count_only(self):
        p = S.parse_section(sec("channel", "[99"))
        self.assertEqual(p["kg_m"], 0.0)
        self.assertIn("无此规格", p["note"])

    def test_unknown_type_count_only(self):
        p = S.parse_section(sec("", "GT-1"))
        self.assertEqual(p["kg_m"], 0.0)


class TestLengths(unittest.TestCase):
    def test_explicit_lengths(self):
        members = [
            {"code": "GL-1", "evidence": [{"text": "GL-1 HN400x200x8x13 L=6000"}]},
            {"code": "GL-2", "evidence": [{"text": "长度4500"}]},
            {"code": "GL-3", "evidence": [{"text": "无长度标注"}]},
        ]
        out = S.explicit_lengths(members)
        self.assertAlmostEqual(out["GL-1"], 6.0)
        self.assertAlmostEqual(out["GL-2"], 4.5)
        self.assertNotIn("GL-3", out)

    def test_duplicate_code_accumulates_explicit_length(self):
        members = [
            {"code": "GL-1", "evidence": [{"text": "GL-1 L=6000"}]},
            {"code": "GL-1", "evidence": [{"text": "GL-1 长度4500"}]},
        ]
        out = S.explicit_lengths(members)
        self.assertAlmostEqual(out["GL-1"], 10.5)
        self.assertEqual(S.duplicate_member_codes(members),
                         [{"code": "GL-1", "count": 2}])

    def test_drawn_length_by_layer(self):
        geo = {"steel_geometry": [
            {"layer": "STEEL-BEAM", "geometry": [0, 0, 6000, 0]},
            {"layer": "STEEL-BEAM", "geometry": [0, 0, 0, 4000]},
            {"layer": "OTHER", "geometry": [0, 0, 3000, 0]},
        ]}
        out = S.drawn_length(geo)
        self.assertAlmostEqual(out["STEEL-BEAM"], 10.0)
        self.assertAlmostEqual(out["OTHER"], 3.0)


class TestGradesAndMemberMerge(unittest.TestCase):
    def member(self, code, text, category="steel_beam", system="roof"):
        return {"code": code, "name": code, "category": category,
                "system": system, "evidence": [{"text": text}]}

    def material(self, grade, text):
        return {"type": "material", "grade": grade,
                "evidence": [{"text": text}]}

    def test_same_code_instances_merge_with_grade_and_sections(self):
        text = "GL-1 HN400x200x8x13 L=6000 材质Q355"
        sections = [S.parse_section(sec("h_section", "HN400x200x8x13"))]
        rows, review = S.member_merge(
            [self.member("GL-1", text), self.member("GL-1", text)],
            sections,
            [sec("h_section", "HN400x200x8x13")],
            [self.material("Q355", text)],
        )
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["code"], "GL-1")
        self.assertEqual(row["instance_count"], 2)
        self.assertEqual(row["grade"], "Q355")
        self.assertEqual(row["section_texts"], ["HN400x200x8x13"])
        self.assertAlmostEqual(row["explicit_length_m"], 12.0)
        self.assertAlmostEqual(row["tonnage_t"][0], 0.65596, places=4)
        self.assertAlmostEqual(row["tonnage_t"][1], 0.88749, places=4)
        self.assertEqual(review, [])

    def test_multiple_grade_evidence_is_not_defaulted(self):
        text = "GL-2 HN400x200x8x13 L=4000 材质Q235"
        rows, review = S.member_merge(
            [self.member("GL-2", text)],
            [S.parse_section(sec("h_section", "HN400x200x8x13"))],
            [sec("h_section", "HN400x200x8x13")],
            [self.material("Q235", text), self.material("Q345", text)],
        )
        self.assertEqual(rows[0]["grade"], "mixed_grade")
        self.assertIn("多牌号证据冲突，不得默认归档", rows[0]["review_reasons"])
        self.assertTrue(any(r["code"] == "GL-2" for r in review))

    def test_missing_grade_is_unknown(self):
        text = "GL-3 HN300x150x6.5x9 L=5000"
        rows, _ = S.member_merge(
            [self.member("GL-3", text)],
            [S.parse_section(sec("h_section", "HN300x150x6.5x9"))],
            [sec("h_section", "HN300x150x6.5x9")],
            [],
        )
        self.assertEqual(rows[0]["grade"], "unknown_grade")
        self.assertTrue(rows[0]["tonnage_t"][0] > 0)

    def test_same_code_category_and_system_conflicts_are_reviewed(self):
        rows, review = S.member_merge(
            [self.member("GL-4", "GL-4 L=6000", "steel_beam", "roof"),
             self.member("GL-4", "GL-4 L=6000", "steel_column", "frame")],
            [], [], [],
        )
        self.assertEqual(rows[0]["conflicts"],
                         ["同编号构件类别冲突", "同编号跨系统冲突"])
        self.assertTrue(any("同编号构件类别冲突" in r["reasons"] for r in review))

    def test_build_outputs_grade_and_member_ledger(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            member_text = "GL-1 HN400x200x8x13 L=6000"
            material_text = "GL-1 材质Q345"
            data = steel_json(
                sections=[sec("h_section", "HN400x200x8x13")],
                members=[self.member("GL-1", member_text)],
            )
            data["materials"] = [self.material("Q345", material_text)]
            p = td / "x.steel.json"
            p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            prefix = td / "ton"
            S.build(str(p), str(prefix))
            out = json.loads((td / "ton.json").read_text(encoding="utf-8"))
            self.assertEqual(out["member_merge"][0]["grade"], "Q345")
            self.assertEqual(out["grade_counts"], {"Q345": 1})
            self.assertEqual(out["grade_tonnage"][0]["grade"], "Q345")
            self.assertIn("构件归并台账", (td / "ton.md").read_text(encoding="utf-8"))
            csv_text = (td / "ton.csv").read_text(encoding="utf-8-sig")
            self.assertIn("牌号吨位-Q345", csv_text)
            self.assertIn("构件归并-GL-1", csv_text)

    def test_nonlist_materials_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            data = steel_json(sections=[sec("h_section", "HN400x200x8x13")])
            data["materials"] = "Q345"
            p = td / "x.steel.json"
            p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            with self.assertRaises(SystemExit) as ctx:
                S.build(str(p), str(td / "ton"))
            self.assertIn("materials[]", str(ctx.exception))


class TestConnectionsAndFinishes(unittest.TestCase):
    def test_connection_categories_and_quantity_evidence(self):
        rows = [
            conn("high_strength_bolt", "高强螺栓 M20 8套"),
            conn("bolt", "普通螺栓 6个"),
            conn("bolt", "锚栓 4套"),
            conn("stud", "栓钉"),
            conn("plate_connection", "节点板 PL20x400x600"),
            conn("stiffener", "加劲肋"),
        ]
        summary, review, ledger = S.connection_ledger(rows)
        by_category = {x["category"]: x for x in summary}
        self.assertEqual(by_category["high_strength_bolt"]["count"], 8)
        self.assertEqual(by_category["bolt"]["count"], 6)
        self.assertEqual(by_category["anchor_bolt"]["count"], 4)
        self.assertEqual(by_category["stud"]["count"], 1)
        self.assertEqual(by_category["stud"]["count_basis"], "标注次数")
        self.assertEqual(by_category["stiffener"]["quantity_status"], "needs_review")
        self.assertTrue(any(r["type"] == "connection_count" and r["code"] == "栓钉"
                            for r in review))
        self.assertEqual(len(ledger), 6)

    def test_connection_missing_quantity_is_label_count_not_invented(self):
        summary, review, ledger = S.connection_ledger(
            [conn("high_strength_bolt", "高强螺栓 M20")])
        self.assertEqual(summary[0]["label_count"], 1)
        self.assertEqual(summary[0]["count"], 1)
        self.assertEqual(summary[0]["count_basis"], "标注次数")
        self.assertEqual(summary[0]["quantity_status"], "needs_review")
        self.assertIsNone(ledger[0]["evidence_quantity"])
        self.assertTrue(review)

    def test_connection_plate_enters_tonnage(self):
        rows, total = S.plate_tonnage_rows(
            [conn("plate_connection", "节点板 PL20x400x600")])
        self.assertEqual(len(rows), 1)
        self.assertAlmostEqual(rows[0]["kg"], 37.68, places=3)
        self.assertEqual(rows[0]["basis"], "厚×宽×长")
        self.assertAlmostEqual(total[0], 0.032028, places=6)
        self.assertAlmostEqual(total[1], 0.043332, places=6)

    def test_connection_plate_by_area_enters_tonnage(self):
        rows, total = S.plate_tonnage_rows(
            [conn("plate_connection", "板厚20 面积0.5m²")])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["basis"], "板厚×面积")
        self.assertAlmostEqual(rows[0]["kg"], 78.5, places=3)
        self.assertAlmostEqual(total[0], 0.066725, places=6)

    def test_connection_plate_without_dimensions_is_count_only(self):
        rows, total = S.plate_tonnage_rows([conn("plate_connection", "节点板")])
        self.assertEqual(rows, [])
        self.assertEqual(total, [0.0, 0.0])
        summary, review, _ledger = S.connection_ledger(
            [conn("plate_connection", "节点板")])
        self.assertEqual(summary[0]["count"], 1)
        self.assertEqual(summary[0]["count_basis"], "标注次数")
        self.assertTrue(any(r["type"] == "connection_count" for r in review))

    def test_finish_area_evidence(self):
        summary, review, ledger = S.finish_ledger([
            fin("primer", "底漆 面积100m2"),
            fin("topcoat", "面漆 涂装面积80㎡"),
            fin("hot_dip_galvanized", "热浸镀锌 面积50m²"),
            fin("fireproof_coating", "防火涂料 面积120m2"),
        ])
        by_category = {x["category"]: x for x in summary}
        self.assertEqual(by_category["primer"]["area_m2_band"], [85.0, 115.0])
        self.assertEqual(by_category["topcoat"]["area_m2_band"], [68.0, 92.0])
        self.assertEqual(by_category["hot_dip_galvanized"]["area_m2_band"],
                         [42.5, 57.5])
        self.assertEqual(by_category["fireproof_coating"]["area_m2_band"],
                         [102.0, 138.0])
        self.assertIsNone(by_category["fireproof_coating"]["fire_rating"])
        self.assertEqual(review, [])
        self.assertEqual(len(ledger), 4)

    def test_finish_missing_area_is_unavailable(self):
        summary, review, ledger = S.finish_ledger([
            fin("fireproof_coating", "防火涂料 两遍"),
        ])
        self.assertEqual(summary[0]["area_status"], "unavailable")
        self.assertIsNone(summary[0]["area_m2_band"])
        self.assertIsNone(summary[0]["fire_rating"])
        self.assertEqual(ledger[0]["area_status"], "unavailable")
        self.assertIn("防火涂料面积或范围证据缺失", review[0]["reasons"][0])

    def test_build_outputs_connection_and_finish_lists(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            data = steel_json(
                sections=[sec("h_section", "HN400x200x8x13")],
                members=[{"code": "GL-1",
                          "evidence": [{"text": "GL-1 L=6000"}]}],
            )
            data["connections"] = [
                conn("high_strength_bolt", "高强螺栓 M20 8套"),
                conn("stud", "栓钉"),
                conn("plate_connection", "节点板 PL20x400x600"),
            ]
            data["finishes"] = [
                fin("primer", "底漆 面积100m2"),
                fin("fireproof_coating", "防火涂料 两遍"),
            ]
            p = td / "x.steel.json"
            p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            prefix = td / "ton"
            S.build(str(p), str(prefix))
            out = json.loads((td / "ton.json").read_text(encoding="utf-8"))
            self.assertEqual(len(out["connection_summary"]), 3)
            self.assertEqual(len(out["connection_ledger"]), 3)
            self.assertEqual(out["connection_plate_total_t"][0] > 0, True)
            self.assertEqual(len(out["finish_summary"]), 4)
            self.assertEqual(len(out["finish_ledger"]), 2)
            self.assertEqual(out["finish_summary"][0]["area_m2_band"],
                             [85.0, 115.0])
            self.assertTrue(any(r["type"] == "connection_count"
                                for r in out["review_items"]))
            self.assertTrue(any(r["type"] == "finish_area"
                                for r in out["review_items"]))
            md = (td / "ton.md").read_text(encoding="utf-8")
            csv_text = (td / "ton.csv").read_text(encoding="utf-8-sig")
            self.assertIn("## 连接清单", md)
            self.assertIn("## 涂装清单", md)
            self.assertIn("## 复核清单", md)
            self.assertIn("连接-高强螺栓", csv_text)
            self.assertIn("涂装-底漆", csv_text)

    def test_nonlist_connections_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            data = steel_json(sections=[sec("h_section", "HN400x200x8x13")])
            data["connections"] = "M20"
            p = td / "x.steel.json"
            p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            with self.assertRaises(SystemExit) as ctx:
                S.build(str(p), str(td / "ton"))
            self.assertIn("connections[]", str(ctx.exception))


class TestBuild(unittest.TestCase):
    def test_end_to_end(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            data = steel_json(
                sections=[sec("h_section", "HN400x200x8x13"),
                          sec("h_section", "HN400x200x8x13"),
                          sec("channel", "[16"),
                          sec("rect_tube", "□100x100x4"),
                          sec("h_section", "H400x200")],
                members=[{"code": "GL-1", "evidence": [{"text": "GL-1 L=6000"}]},
                         {"code": "GL-2", "evidence": [{"text": "L=4000"}]}],
            )
            p = td / "x.steel.json"
            p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            prefix = td / "ton"
            S.build(str(p), str(prefix))
            out = json.loads((td / "ton.json").read_text(encoding="utf-8"))
            self.assertEqual(out["schema"], "cad-steel-tonnage/v0.2")
            self.assertFalse(out["final_quantity"])
            self.assertEqual(out["length_basis"], "explicit")
            self.assertAlmostEqual(out["length_used_m"], 10.0)
            # H 型 64.31、方管 12.12：加权分摊长度 → 总吨位 = (64.31*share+12.12*share)*10/1000
            lo, hi = out["total_t"]
            # 米重×次数权重：H 64.31×2、槽钢 17.24、方管 12.06 → 长度 10m 按权分摊
            # 权重和 157.92；总吨 = 10/157.92 × Σ(kg²×次数)/1000 ≈ 0.552
            self.assertAlmostEqual((lo + hi) / 2, 0.552, places=2)
            self.assertEqual(len(out["rows"]), 3)      # 槽钢补表后进吨位
            self.assertEqual(len(out["spec_rows"]), 4)  # 含仅计数的 H400x200
            md = (td / "ton.md").read_text(encoding="utf-8")
            self.assertEqual(out["total_basis"], "allocated_estimate")
            self.assertIn("final_quantity=false", md)
            self.assertIn("总吨位带（分摊草稿，不是答案）", md)
            self.assertNotIn("总吨位带（推荐）", md)
            self.assertIn("仅计数", md)

    def test_drawn_length_fallback(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            data = steel_json(
                sections=[sec("h_section", "HN300x150x6.5x9")],
                geometry=[{"layer": "STEEL", "geometry": [0, 0, 8000, 0]}],
            )
            p = td / "x.steel.json"
            p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            prefix = td / "ton"
            S.build(str(p), str(prefix))
            out = json.loads((td / "ton.json").read_text(encoding="utf-8"))
            self.assertEqual(out["length_basis"], "drawn")
            self.assertAlmostEqual(out["length_used_m"], 8.0)
            self.assertTrue(out["total_t"][0] > 0)

    def test_explicit_length_preferred_over_drawn(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            data = steel_json(
                sections=[sec("h_section", "HN400x200x8x13")],
                members=[{"code": "GL-1",
                          "evidence": [{"text": "GL-1 L=6000"}]}],
                geometry=[{"layer": "STEEL", "geometry": [0, 0, 8000, 0]}],
            )
            p = td / "x.steel.json"
            p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            prefix = td / "ton"
            S.build(str(p), str(prefix))
            out = json.loads((td / "ton.json").read_text(encoding="utf-8"))
            self.assertEqual(out["length_basis"], "explicit")
            self.assertAlmostEqual(out["length_used_m"], 6.0)
            self.assertEqual(out["drawn_length_by_layer"], {"STEEL": 8.0})

    def test_no_length_no_tonnage(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            data = steel_json(sections=[sec("h_section", "HN400x200x8x13")])
            p = td / "x.steel.json"
            p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            prefix = td / "ton"
            S.build(str(p), str(prefix))
            out = json.loads((td / "ton.json").read_text(encoding="utf-8"))
            self.assertEqual(out["length_basis"], "none")
            self.assertEqual(out["total_t"], [])

    def test_empty_raises(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "x.steel.json"
            p.write_text(json.dumps(steel_json(), ensure_ascii=False), encoding="utf-8")
            with self.assertRaises(SystemExit):
                S.build(str(p), str(Path(td) / "ton"))

    def test_noncontract_schema_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            p = td / "x.steel.json"
            p.write_text(json.dumps({"schema": "other/v1"}), encoding="utf-8")
            with self.assertRaises(SystemExit) as ctx:
                S.build(str(p), str(td / "ton"))
            self.assertIn("schema", str(ctx.exception))
            self.assertFalse((td / "ton.json").exists())

    def test_missing_required_array_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            p = td / "x.steel.json"
            p.write_text(json.dumps({"schema": "cad-steel-geometry/v1",
                                     "sections": []}), encoding="utf-8")
            with self.assertRaises(SystemExit) as ctx:
                S.build(str(p), str(td / "ton"))
            self.assertIn("缺少 members", str(ctx.exception))

    def test_nonobject_candidate_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            p = td / "x.steel.json"
            p.write_text(json.dumps({"schema": "cad-steel-geometry/v1",
                                     "sections": ["H400x200"],
                                     "members": [], "steel_geometry": []}),
                         encoding="utf-8")
            with self.assertRaises(SystemExit) as ctx:
                S.build(str(p), str(td / "ton"))
            self.assertIn("sections[0]", str(ctx.exception))

    def test_malformed_json_rejected_without_warning(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            p = td / "x.steel.json"
            p.write_text("{", encoding="utf-8")
            with self.assertRaises(SystemExit) as ctx:
                S.build(str(p), str(td / "ton"))
            self.assertIn("非契约 JSON", str(ctx.exception))


class TestTotalCaliberAndValidate(unittest.TestCase):
    """0.3.0：逐根口径优先、分摊字段改名、坐标透传、契约体检与场景值。"""

    def _write(self, td, data):
        p = Path(td) / "x.steel.json"
        p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return p

    def test_member_level_total_preferred_over_allocation(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            data = steel_json(
                sections=[sec("tube", "Φ1200x50"), sec("tube", "Φ1200x40")],
                members=[
                    {"code": "Z1", "x": 1000, "y": 2000,
                     "evidence": [{"text": "Z1 Φ1200x50 L=4500"}]},
                    {"code": "Z2", "evidence": [{"text": "Z2 Φ1200x40 L=4500"}]},
                ],
            )
            p = self._write(td, data)
            S.build(str(p), str(td / "ton"))
            out = json.loads((td / "ton.json").read_text(encoding="utf-8"))
            self.assertEqual(out["total_basis"], "member_level")
            self.assertEqual(out["total_t"], out["total_t_member_level"])
            self.assertNotEqual(out["total_t"], out["total_t_allocated_estimate"])
            row_sum = [round(sum(r["tonnage_t"][0] for r in out["member_merge"]), 2),
                       round(sum(r["tonnage_t"][1] for r in out["member_merge"]), 2)]
            self.assertEqual(out["total_t"], row_sum)
            md = (td / "ton.md").read_text(encoding="utf-8")
            self.assertIn("逐根构件台账求和（推荐口径）", md)
            self.assertIn("total_t_allocated_estimate", md)

    def test_member_coordinates_passthrough(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            data = steel_json(
                sections=[sec("tube", "Φ1200x50")],
                members=[{"code": "Z1", "x": 1000, "y": 2000, "z": 3500,
                          "rotation": 0,
                          "evidence": [{"text": "Z1 Φ1200x50 L=4500"}]}],
            )
            p = self._write(td, data)
            S.build(str(p), str(td / "ton"))
            out = json.loads((td / "ton.json").read_text(encoding="utf-8"))
            row = out["member_merge"][0]
            self.assertEqual((row["x"], row["y"], row["z"]), (1000, 2000, 3500))
            self.assertEqual(row["coord_unit"], "mm")
            self.assertEqual(row["location_status"], "provided")

    def test_all_known_grades_leave_no_unknown_residual(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            data = steel_json(
                sections=[sec("tube", "Φ1200x50")],
                members=[{"code": "Z1", "x": 1000, "y": 2000, "grade": "Q355",
                          "evidence": [{"text": "Z1 Φ1200x50 L=4500"}]}],
            )
            p = self._write(td, data)
            S.build(str(p), str(td / "ton"))
            out = json.loads((td / "ton.json").read_text(encoding="utf-8"))
            self.assertEqual([g["grade"] for g in out["grade_tonnage"]], ["Q355"])
            self.assertAlmostEqual(out["grade_tonnage"][0]["tonnage_t"][0],
                                   out["total_t"][0], places=2)

    def test_member_level_grade_keeps_plate_tonnage_in_unknown(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            data = steel_json(
                sections=[sec("tube", "Φ1200x50")],
                members=[{"code": "Z1", "grade": "Q355",
                          "evidence": [{"text": "Z1 Φ1200x50 L=4500"}]}],
            )
            data["connections"] = [conn("plate_connection", "节点板 PL20x400x600")]
            p = self._write(td, data)
            S.build(str(p), str(td / "ton"))
            out = json.loads((td / "ton.json").read_text(encoding="utf-8"))
            grades = {g["grade"]: g["tonnage_t"] for g in out["grade_tonnage"]}
            self.assertIn("Q355", grades)
            self.assertIn("unknown_grade", grades)
            self.assertEqual(grades["unknown_grade"],
                             [round(out["connection_plate_total_t"][0], 2),
                              round(out["connection_plate_total_t"][1], 2)])
            grade_sum = [sum(g["tonnage_t"][0] for g in out["grade_tonnage"]),
                         sum(g["tonnage_t"][1] for g in out["grade_tonnage"])]
            self.assertAlmostEqual(grade_sum[0], out["total_t"][0], places=2)
            self.assertAlmostEqual(grade_sum[1], out["total_t"][1], places=2)

    def test_validate_reports_count_only_and_unmatched(self):
        data = steel_json(
            sections=[sec("h_section", "H400x200")],
            members=[{"code": "GL-9", "evidence": [{"text": "GL-9"}]}],
        )
        rep = S.contract_health(data)
        self.assertEqual(rep["schema"], "cad-steel-contract-health/v1")
        self.assertEqual(rep["status"], "warn")
        self.assertEqual(rep["sections"][0]["status"], "count_only")
        self.assertIn("GL-9", rep["members"]["no_section"])
        text = S.format_health(rep)
        self.assertIn("契约可计算，但有需复核项", text)
        self.assertIn("只能计数", text)

    def test_validate_rejects_noncontract_schema(self):
        rep = S.contract_health({"schema": "other/v1"})
        self.assertEqual(rep["status"], "error")
        self.assertTrue(any("schema" in e for e in rep["errors"]))

    def test_validate_path_does_not_write_tonnage_files(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            p = self._write(td, steel_json(
                sections=[sec("tube", "Φ1200x50")],
                members=[{"code": "Z1", "evidence": [{"text": "Z1 Φ1200x50 L=4500"}]}]))
            rep = S.validate_path(str(p))
            self.assertNotEqual(rep["status"], "error")
            self.assertFalse((td / "ton.json").exists())

    def test_length_scenarios_are_labeled_estimates(self):
        rows = S.length_scenario_rows(
            [{"kg_m": 100.0, "count": 2}, {"kg_m": 0.0, "count": 3}], [4.0, 6.0])
        self.assertEqual([r["length_m"] for r in rows], [4.0, 6.0])
        self.assertAlmostEqual(rows[0]["total_t_band"][0], 0.68, places=3)
        self.assertAlmostEqual(rows[0]["total_t_band"][1], 0.92, places=3)
        self.assertIn("场景值", rows[0]["basis"])

    def test_empty_evidence_is_explained_in_report(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            p = self._write(td, steel_json(
                sections=[sec("tube", "Φ1200x50")],
                members=[{"code": "Z1", "evidence": [{"text": "Z1 Φ1200x50 L=4500"}]}]))
            S.build(str(p), str(td / "ton"))
            md = (td / "ton.md").read_text(encoding="utf-8")
            self.assertIn("输入无证据", md)
            self.assertIn("`connections[]` 为空", md)
            self.assertIn("`finishes[]` 为空", md)


if __name__ == "__main__":
    unittest.main()
