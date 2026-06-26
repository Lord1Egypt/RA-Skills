"""End-to-end parser test."""
import sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from extract_title_block import extract_title_block
from extract_bom import extract_bom
from extract_dimensions import extract_dimensions

TEXT = (ROOT / "examples" / "sample_drawing.txt").read_text(encoding="utf-8")

class TestParser(unittest.TestCase):
    def test_title(self):
        t = extract_title_block(TEXT, standard="GB")
        self.assertEqual(t["drawing_no"], "GB-2024-001")
        self.assertEqual(t["scale"], "1:2")
    def test_bom(self):
        b = extract_bom(TEXT)
        self.assertEqual(len(b), 3)
        self.assertEqual(b[0]["qty"], 4)
    def test_dim(self):
        d = extract_dimensions(TEXT)
        fits = [x for x in d if "fit" in x]
        self.assertEqual(fits[0]["fit"], "H7/g6")

if __name__ == "__main__":
    unittest.main()
