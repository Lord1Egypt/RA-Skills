import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from cad_compare import compare_files  # noqa: E402
from cad_contract import validate_contract_payload  # noqa: E402


class CadCompareTest(unittest.TestCase):
    def test_added_removed_moved_and_unchanged(self):
        base = {
            "layers": ["A", "B"],
            "meta": {"block_refs": {"door": 2, "old": 1}},
            "text_records": [
                {"kind": "TEXT", "text": "kept", "x": 0, "y": 0, "layer": "A", "file": 0},
                {"kind": "TEXT", "text": "gone", "x": 10, "y": 0, "layer": "A", "file": 0},
                {"kind": "TEXT", "text": "move", "x": 100, "y": 100, "layer": "A", "file": 0},
            ],
            "geometry_segments": [[[0, 0, 100, 0], [200, 0, 300, 0]]],
            "geometry_layers": [["A", "A"]],
        }
        target = {
            "layers": ["A", "C"],
            "meta": {"block_refs": {"door": 3, "new": 1}},
            "text_records": [
                {"kind": "TEXT", "text": "kept", "x": 0, "y": 0, "layer": "A", "file": 0},
                {"kind": "TEXT", "text": "added", "x": 20, "y": 0, "layer": "A", "file": 0},
                {"kind": "TEXT", "text": "move", "x": 150, "y": 100, "layer": "A", "file": 0},
            ],
            "geometry_segments": [[[0, 0, 100, 0], [210, 0, 310, 0], [400, 0, 500, 0]]],
            "geometry_layers": [["A", "A", "A"]],
        }
        with tempfile.TemporaryDirectory() as temp:
            a = Path(temp) / "base.json"; b = Path(temp) / "target.json"
            a.write_text(json.dumps(base, ensure_ascii=False), encoding="utf-8")
            b.write_text(json.dumps(target, ensure_ascii=False), encoding="utf-8")
            result = compare_files(a, b, 1, 100)
        self.assertEqual(validate_contract_payload(result), [])
        changes = {row["change_type"] for row in result["drawing_changes"]}
        self.assertIn("removed_layer", changes)
        self.assertIn("added_layer", changes)
        self.assertIn("block_count_changed", changes)
        self.assertIn("added_block", changes)
        self.assertIn("removed_block", changes)
        self.assertIn("added_text", changes)
        self.assertIn("removed_text", changes)
        self.assertIn("moved_text", changes)
        self.assertIn("added_geometry", changes)
        self.assertIn("moved_geometry", changes)
        self.assertEqual(result["summary"]["moved_text"], 1)
        self.assertEqual(result["summary"]["added_geometry"], 1)
        self.assertEqual(result["summary"]["moved_geometry"], 1)

    def test_same_detail_has_no_changes(self):
        data = {
            "layers": ["A"],
            "meta": {"block_refs": {"B": 1}},
            "text_records": [{"kind": "TEXT", "text": "x", "x": 1, "y": 2, "layer": "A", "file": 0}],
            "geometry_segments": [[[0, 0, 1, 1]]],
            "geometry_layers": [["A"]],
        }
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "detail.json"
            path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            result = compare_files(path, path, 1, 100)
        self.assertEqual(validate_contract_payload(result), [])
        self.assertEqual(result["summary"]["changes_output"], 0)

    def test_geometry_only_change_reports_no_text_change(self):
        base = {
            "layers": ["A"],
            "meta": {"block_refs": {"B": 1}},
            "text_records": [{"kind": "TEXT", "text": "same", "x": 1, "y": 2, "layer": "A", "file": 0}],
            "geometry_segments": [[[0, 0, 100, 0]]],
            "geometry_layers": [["A"]],
        }
        target = {
            "layers": ["A"],
            "meta": {"block_refs": {"B": 1}},
            "text_records": [{"kind": "TEXT", "text": "same", "x": 1, "y": 2, "layer": "A", "file": 0}],
            "geometry_segments": [[[0, 0, 100, 0], [500, 0, 600, 0]]],
            "geometry_layers": [["A", "A"]],
        }
        with tempfile.TemporaryDirectory() as temp:
            a = Path(temp) / "base.json"; b = Path(temp) / "target.json"
            a.write_text(json.dumps(base, ensure_ascii=False), encoding="utf-8")
            b.write_text(json.dumps(target, ensure_ascii=False), encoding="utf-8")
            result = compare_files(a, b, 1, 100)
        self.assertEqual(validate_contract_payload(result), [])
        self.assertEqual(result["summary"]["added_text"], 0)
        self.assertEqual(result["summary"]["removed_text"], 0)
        self.assertEqual(result["summary"]["moved_text"], 0)
        self.assertGreater(result["summary"]["added_geometry"], 0)
        changes = {row["change_type"] for row in result["drawing_changes"]}
        self.assertNotIn("added_text", changes)
        self.assertIn("added_geometry", changes)

    def test_empty_input_returns_empty_contract(self):
        blank = {"files": [], "layers": [], "text_records": [], "geometry_segments": [], "geometry_layers": [], "meta": {}}
        with tempfile.TemporaryDirectory() as temp:
            a = Path(temp) / "empty_a.json"; b = Path(temp) / "empty_b.json"
            a.write_text(json.dumps(blank, ensure_ascii=False), encoding="utf-8")
            b.write_text(json.dumps(blank, ensure_ascii=False), encoding="utf-8")
            result = compare_files(a, b, 1, 100)
        self.assertEqual(validate_contract_payload(result), [])
        self.assertEqual(result["summary"]["changes_output"], 0)
        self.assertEqual(result["drawing_changes"], [])
        self.assertEqual(result["change_summary"], {})


if __name__ == "__main__":
    unittest.main()
