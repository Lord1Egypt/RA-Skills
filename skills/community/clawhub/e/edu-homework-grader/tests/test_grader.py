"""End-to-end grading test."""
import json, sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from grade_objective import grade_objective
from grade_subjective import grade_subjective

HW = json.loads((ROOT / "examples" / "sample_homework.json").read_text(encoding="utf-8"))
KEY = json.loads((ROOT / "examples" / "sample_key.json").read_text(encoding="utf-8"))

class TestGrader(unittest.TestCase):
    def test_mc(self):
        r = grade_objective(HW["items"][0], KEY["Q1"])
        self.assertEqual(r["earned"], 2.0)
    def test_fib_synonym(self):
        r = grade_objective(HW["items"][1], KEY["Q2"])
        self.assertEqual(r["earned"], 3.0)
    def test_subjective(self):
        r = grade_subjective(HW["items"][2], KEY["Q3"], None)
        self.assertEqual(r["earned"], 10.0)

if __name__ == "__main__":
    unittest.main()
