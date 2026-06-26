"""End-to-end sanity test for the analyzer."""
import json, sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from compute_ratios import compute_ratios
from detect_red_flags import detect_red_flags

FIN = json.loads((ROOT / "examples" / "sample_financials.json").read_text(encoding="utf-8"))

class TestAnalyzer(unittest.TestCase):
    def test_ratios(self):
        r = compute_ratios(FIN)
        self.assertAlmostEqual(r["profitability"]["gross_margin"], 0.4, places=4)
        self.assertAlmostEqual(r["leverage"]["debt_ratio"], 7000/12000, places=3)
    def test_red_flags(self):
        flags = detect_red_flags(FIN)
        codes = [f["code"] for f in flags]
        for expected in ("RF01", "RF02", "RF03"):
            self.assertIn(expected, codes, msg=f"{expected} should fire on the example data")

if __name__ == "__main__":
    unittest.main()
