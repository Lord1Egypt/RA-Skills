import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from cad_scan import angle_bucket, analyse
from cad_interpret import _scope_key


class RotationAggregationTest(unittest.TestCase):
    def test_angle_bucket_normalizes(self):
        self.assertEqual(angle_bucket(0.0), 0)
        self.assertEqual(angle_bucket(5.0), 1)
        self.assertEqual(angle_bucket(185.0), 1)   # 185%180=5
        self.assertEqual(angle_bucket(-10.0), 34)  # (-10)%180=170 -> 34
        self.assertIsNone(angle_bucket(None))
        self.assertIsNone(angle_bucket("bad"))

    def test_analyse_splits_same_position_by_rotation(self):
        recs = [
            {"kind": "TEXT", "text": "KL1(3A) 300x700", "x": 1000, "y": 1000, "file": 0, "sheet": 1, "rotation": 0},
            {"kind": "TEXT", "text": "KL2(2) 300x600", "x": 1000, "y": 1000, "file": 0, "sheet": 1, "rotation": 90},
        ]
        res = analyse(recs, ["S-梁"], {}, dedupe=5000.0, count_by="pos")
        # 同一图框内同位置但不同旋转角 -> 拆成两个标注位置
        members = res["members"]["梁"]
        self.assertEqual(len(members), 2)
        self.assertTrue(all(d["pos_n"] == 1 for d in members.values()))

    def test_analyse_merges_same_rotation(self):
        recs = [
            {"kind": "TEXT", "text": "KL1(3A) 300x700", "x": 1000, "y": 1000, "file": 0, "sheet": 1, "rotation": 0},
            {"kind": "TEXT", "text": "2C25；3C22", "x": 1003, "y": 1005, "file": 0, "sheet": 1, "rotation": 0},
        ]
        res = analyse(recs, ["S-梁"], {}, dedupe=5000.0, count_by="pos")
        members = res["members"]["梁"]
        self.assertEqual(len(members), 1)
        self.assertEqual(next(iter(members.values()))["pos_n"], 1)

    def test_scope_key_none_rotation_backward_compatible(self):
        self.assertEqual(_scope_key({"file": 0, "sheet": "1"}),
                         _scope_key({"file": 0, "sheet": "1", "rotation": None}))

    def test_scope_key_rotation_splits(self):
        self.assertNotEqual(_scope_key({"rotation": 0}), _scope_key({"rotation": 90}))


if __name__ == "__main__":
    unittest.main()
