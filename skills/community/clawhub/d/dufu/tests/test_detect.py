import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DetectTests(unittest.TestCase):
    def test_detect_json_reports_signals_without_probability(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/detect.py"), "--file", str(ROOT / "fixtures/sample.txt"), "--json"],
            check=True,
            capture_output=True,
            text=True,
        )
        data = json.loads(result.stdout)
        self.assertIn("赋能", data["hits"]["abstract_terms"])
        self.assertTrue(data["heuristic_flags"])
        self.assertNotIn("probability", data)

    def test_release_fixtures_cover_success_failure_and_five_cases(self):
        self.assertTrue((ROOT / "fixtures/success.json").exists())
        self.assertTrue((ROOT / "fixtures/failure.json").exists())
        cases = json.loads((ROOT / "fixtures/cases.json").read_text(encoding="utf-8"))
        self.assertEqual(len(cases), 5)


if __name__ == "__main__":
    unittest.main()
