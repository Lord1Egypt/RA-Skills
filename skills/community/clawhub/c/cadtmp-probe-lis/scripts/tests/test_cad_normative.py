#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cad_normative 的边界与编号匹配测试。"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2]
sys_path = SKILL_DIR / "scripts"
import sys
if str(sys_path) not in sys.path:
    sys.path.insert(0, str(sys_path))

import cad_normative as norm  # noqa: E402


def payload_for(texts: list[str], standards: dict | None = None):
    data = {"text_records": [{"file": "结构总说明", "sheet": 1, "text": t} for t in texts]}
    if standards is None:
        path = SKILL_DIR / "rules" / "standards.json"
    else:
        temp = tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", suffix=".json")
        import json
        json.dump(standards, temp, ensure_ascii=False)
        temp.close()
        path = Path(temp.name)
    return norm.build_payload(data, path)


class CadNormativeTest(unittest.TestCase):
    def test_known_and_variant_ids_match(self):
        text = "依据 GB/T 50001-2017、JGJ/T 17-2008、CECS 289-2011、L13G7、04S519、13J104、GB 50203-2011。"
        p = payload_for([text])
        rows = {r["ref"]: r for r in p["refs"]}
        for code in ("GB/T50001-2017", "JGJ/T17-2008", "CECS289-2011", "L13G7",
                     "04S519", "13J104", "GB50203-2011"):
            self.assertIn(code, rows)
            self.assertTrue(rows[code]["matched"], code)
            self.assertTrue(rows[code]["kb_path"] or rows[code]["source_url"], code)

    def test_base_id_matches_year_edition(self):
        p = payload_for(["执行 GB50010-2010 及 GB50010-2010(2015年版)。"])
        rows = {r["ref"]: r for r in p["refs"]}
        self.assertTrue(rows["GB50010-2010"]["matched"])
        self.assertTrue(rows["GB50010-2010(2015年版)"]["matched"])
        self.assertEqual(rows["GB50010-2010"]["standard_id"], "GB50010-2010(2015年版)")

    def test_unknown_reference_is_reported_not_invented(self):
        p = payload_for(["补充执行 GB99999-2020。"])
        row = next(r for r in p["refs"] if r["ref"] == "GB99999-2020")
        self.assertFalse(row["matched"])
        self.assertEqual(row["status"], "unknown")
        self.assertEqual(row["rule_status"], "not-indexed")

    def test_legacy_atlas_status(self):
        p = payload_for(["构造做法按16G101-1执行。"])
        row = next(r for r in p["refs"] if r["ref"] == "16G101-1")
        self.assertTrue(row["matched"])
        self.assertEqual(row["status"], "legacy")

    def test_profile_conflict_requires_part_binding(self):
        p = payload_for(["梁混凝土强度等级C30。", "墙混凝土强度等级C40。"])
        self.assertEqual(p["profile"]["混凝土等级"], ["C30", "C40"])
        self.assertEqual(p["summary"]["conflict_count"], 1)
        self.assertEqual(p["conflicts"][0]["parameter"], "混凝土等级")

    def test_missing_required_inputs(self):
        p = payload_for(["混凝土结构按GB55008-2021执行。"])
        labels = {r["label"] for r in p["missing_inputs"]}
        self.assertTrue({"混凝土等级", "抗震等级", "保护层"} <= labels)
        self.assertGreater(p["summary"]["missing_input_count"], 0)

    def test_metadata_only_boundary(self):
        p = payload_for(["执行22G101-1与GB55008-2021。"])
        rows = {r["ref"]: r for r in p["refs"]}
        self.assertEqual(rows["22G101-1"]["rule_status"], "rule-covered")
        self.assertEqual(rows["GB55008-2021"]["rule_status"], "metadata-only")
        self.assertIn("不输出条文符合性结论", p["boundary"])

    def test_aliases_support_slash_and_edition(self):
        self.assertIn("GBT50001-2017", norm._aliases("GB/T 50001-2017"))
        self.assertIn("GB50010-2010", norm._aliases("GB50010-2010(2015年版)"))


if __name__ == "__main__":
    unittest.main()


class CadNormativeEdgeTest(unittest.TestCase):
    def test_current_edition_and_version_risk(self):
        p = payload_for(["本设计执行 GB55011/GB50011-2010(2016年版) 与 GB50068-2018。"])
        rows = {r["ref"]: r for r in p["refs"]}
        row = rows.get("GB50011-2010(2016年版)")
        self.assertIsNotNone(row)
        # 已索引且现行概率不为空；缺全文时保持风险提示
        self.assertIn("status", row)
        self.assertIn("rule_status", row)
        self.assertNotEqual(row["rule_status"], "unknown")

    def test_empty_and_garbage_text_no_crash(self):
        p = payload_for(["", "   ", "无规范引用", "图纸说明见结构总说明。"])
        self.assertIsInstance(p["refs"], list)
        self.assertEqual(p["refs"], [])
