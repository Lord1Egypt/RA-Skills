import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from cad_semantics import analyze_file  # noqa: E402
from cad_contract import validate_contract_payload  # noqa: E402


class CadSemanticsTest(unittest.TestCase):
    def test_layer_block_and_unknown_semantics(self):
        detail = {
            "schema": "cad-scan-detail",
            "source_file": "sample.json",
            "files": [{"name": "sample.dwg"}],
            "layers": ["建筑墙体", "S-梁", "未知图层"],
            "text_records": [
                {"kind": "TEXT", "text": "墙体", "x": 0, "y": 0, "layer": "建筑墙体", "file": 0},
                {"kind": "INSERT", "text": "空调室内机", "x": 10, "y": 10, "layer": "AC-IN", "file": 0},
                {"kind": "TEXT", "text": " Bedroom", "x": 20, "y": 10, "layer": "ROOM", "file": 0},
            ],
            "geometry_segments": [[[0, 0, 100, 0]]],
            "geometry_layers": [["建筑墙体"]],
            "meta": {"block_refs": {"空调室内机": 1, "$D1": 2}, "block_defs": ["空调室内机"]},
        }
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "detail.json"
            path.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
            result = analyze_file(path, 10, 10, 10, 10)
        errors = validate_contract_payload(result)
        self.assertEqual(errors, [])
        semantics = {row["layer"]: row["semantic"] for row in result["semantic_layers"]}
        self.assertEqual(semantics["建筑墙体"], "architecture")
        self.assertEqual(semantics["S-梁"], "structure")
        self.assertEqual(semantics["未知图层"], "unknown")
        contract = result["contract"]
        unknown = next(row for row in contract["review_candidates"] if row["text"] == "未知图层")
        self.assertEqual(unknown["confidence_tier"], "review_required")
        self.assertIn("low_confidence_inference", unknown["review_reasons"])
        raw_blocks = {row["block_name"]: row for row in result["semantic_blocks"]}
        self.assertEqual(raw_blocks["空调室内机"]["semantic"], "equipment")
        contract = result["contract"]
        review_blocks = {row["text"]: row for row in contract["review_candidates"] if row["kind"] == "block" and row["block_name"]}
        self.assertEqual(review_blocks["$D1"]["confidence_tier"], "review_required")
        self.assertIn("missing_block_definition", review_blocks["$D1"]["review_reasons"])
        self.assertEqual(result["summary"]["block_instances"], 1)
        raw_instance = result["block_instances"][0]
        self.assertEqual(raw_instance["block_semantic"], "equipment")
        self.assertGreaterEqual(raw_instance["linked_text_count"], 1)
        instance = next(row for row in contract["candidates"] if row["block_name"] == "空调室内机" and row["section"] == "block_instances")
        self.assertEqual(instance["confidence_tier"], "inferred_candidate")

    def test_unlinked_block_instance_is_review(self):
        detail = {
            "files": [{"name": "sample.dwg"}],
            "layers": [],
            "text_records": [{"kind": "INSERT", "text": "未知块", "x": 0, "y": 0, "layer": None, "file": 0}],
            "geometry_segments": [], "geometry_layers": [],
            "meta": {"block_refs": {"未知块": 1}},
        }
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "detail.json"
            path.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
            result = analyze_file(path, 10, 10, 10, 10)
        self.assertEqual(validate_contract_payload(result), [])
        raw = result["block_instances"][0]
        self.assertIn("ambiguous_text_binding", raw["review_reasons"])
        review = next(row for row in result["contract"]["review_candidates"] if row["section"] == "block_instances")
        self.assertEqual(review["confidence_tier"], "review_required")


if __name__ == "__main__":
    unittest.main()
