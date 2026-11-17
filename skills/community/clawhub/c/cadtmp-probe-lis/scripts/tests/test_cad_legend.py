import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys_path = ROOT / "scripts"
import sys  # noqa: E402
sys.path.insert(0, str(sys_path))
from cad_legend import analyze_file  # noqa: E402
from cad_contract import validate_contract_payload  # noqa: E402


class CadLegendTest(unittest.TestCase):
    def _detail(self):
        return {
            "schema": "cad-scan-detail",
            "source_file": "legend.json",
            "files": [{"name": "x.dwg"}],
            "layers": ["消防水", "照明回路", "风机盘管"],
            "text_records": [
                {"kind": "TEXT", "text": "火灾报警 烟感", "x": 0, "y": 0, "layer": "火警", "file": 0},
                {"kind": "INSERT", "text": "消火栓", "x": 10, "y": 10, "layer": "水", "file": 0},
            ],
            "meta": {"block_refs": {"喷淋": 3}},
        }

    def test_legend_matches_and_contract(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "legend.json"
            path.write_text(json.dumps(self._detail(), ensure_ascii=False), encoding="utf-8")
            result = analyze_file(path, max_matches=100)
        self.assertEqual(validate_contract_payload(result), [])
        matches = result["legend_matches"]
        self.assertGreaterEqual(len(matches), 1)
        disc = {row["discipline"] for row in matches}
        self.assertTrue(disc & {"消防水", "电气消防报警", "暖通", "给排水", "电气照明"})
        # 契约候选应含图例匹配且 final_quantity=false
        candidates = result["contract"]["candidates"]
        self.assertTrue(candidates)
        self.assertTrue(all(row["final_quantity"] is False for row in candidates))
        rows = result["contract"]["candidates"] + result["contract"]["review_candidates"]
        self.assertTrue(any(row["section"] == "legend_matches" for row in rows))

    def test_symbol_fingerprint_block_match(self):
        detail = {
            "files": [{"name": "x.dwg"}],
            "layers": [],
            "text_records": [{"kind": "INSERT", "text": "消火栓", "x": 0, "y": 0, "layer": "W", "file": 0}],
            "meta": {"block_refs": {"消火栓": 2, "命名不规范_SN-01": 9}},
        }
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "legend.json"
            path.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
            result = analyze_file(path, max_matches=100)
        self.assertEqual(validate_contract_payload(result), [])
        rows = {row["id"]: row for row in result["legend_matches"]}
        # 块引用命中符号指纹（消防水），且同名 INSERT 文字不覆盖块指纹
        block_row = rows.get("block:消火栓")
        self.assertIsNotNone(block_row)
        self.assertEqual(block_row["method"], "legend_symbol_fingerprint")
        self.assertEqual(block_row["semantic"], "fire_suppression")
        text_ids = [x["id"] for x in result["legend_matches"] if x["id"].startswith("text:消火栓")]
        self.assertEqual(text_ids, [])

    def test_empty_detail_ok(self):
        detail = {"files": [], "layers": [], "text_records": [], "meta": {}}
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "empty.json"
            path.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
            result = analyze_file(path, max_matches=100)
        self.assertEqual(validate_contract_payload(result), [])

    def test_no_match_does_not_output_false_positive(self):
        detail = {
            "files": [{"name": "x.dwg"}],
            "layers": ["XK-2026", "SN_8837", "哈希图层-B_45"],
            "text_records": [{"kind": "TEXT", "text": "普通注释 无图例语义", "x": 0, "y": 0, "layer": "XK-2026", "file": 0}],
            "meta": {"block_refs": {"B_无语义_77": 3}},
        }
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "nomatch.json"
            path.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
            result = analyze_file(path, max_matches=100)
        self.assertEqual(validate_contract_payload(result), [])
        self.assertEqual(result["legend_matches"], [])
        self.assertEqual(result["contract"]["candidates"], [])
        self.assertEqual(result["contract"]["review_candidates"], [])

    def test_contract_confidence_tier_boundary(self):
        # 混入低置信/无命中文本：候选置信应落 contract 的三档边界内，且无命中内容不输出
        detail = {
            "files": [{"name": "x.dwg"}],
            "layers": ["消防水", "无名普通层"],
            "text_records": [{"kind": "INSERT", "text": "消火栓", "x": 0, "y": 0, "layer": "W", "file": 0}],
            "meta": {"block_refs": {"喷淋": 2}},
        }
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "tier.json"
            path.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
            result = analyze_file(path, max_matches=100)
        self.assertEqual(validate_contract_payload(result), [])
        self.assertTrue(result["legend_matches"])
        for row in result["legend_matches"]:
            self.assertGreaterEqual(row["confidence"], 0.5)
        tiers = {row["confidence_tier"] for row in result["contract"]["candidates"]}
        self.assertTrue(tiers <= {"confirmed_evidence", "inferred_candidate"})


if __name__ == "__main__":
    unittest.main()
