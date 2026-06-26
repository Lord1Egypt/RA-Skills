import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ExpenseSnapTests(unittest.TestCase):
    def setUp(self):
        self.base_dir = Path(__file__).parent
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_arg = ["--base-dir", self.temp_dir.name]

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_cli(self, *args):
        result = subprocess.run(
            [sys.executable, str(self.base_dir / "scripts" / "expense_snap.py"), *self.base_arg, *args],
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)

    def test_record_and_monthly_report(self):
        self.run_cli(
            "record",
            "--merchant",
            "Cafe Luna",
            "--date",
            "2026-03-22",
            "--total",
            "18.40",
            "--currency",
            "EUR",
            "--category",
            "meals",
            "--line-item",
            "Latte|4.50|1|beverages",
            "--line-item",
            "Sandwich|13.90|1|meals",
            "--budget",
            "meals|100",
        )
        listing = self.run_cli("list", "--month", "2026-03")
        report = self.run_cli("monthly-report", "--month", "2026-03")
        self.assertEqual(len(listing["receipts"]), 1)
        self.assertEqual(report["grandTotal"], 18.4)
        self.assertEqual(report["byCategory"][0]["budget"], 100.0)

    def test_export_csv(self):
        self.run_cli(
            "record",
            "--merchant",
            "Stationery Store",
            "--date",
            "2026-03-10",
            "--total",
            "12.00",
            "--currency",
            "EUR",
            "--category",
            "office",
        )
        output_path = Path(self.temp_dir.name) / "exports" / "march.csv"
        exported = self.run_cli("export-csv", "--month", "2026-03", "--output", str(output_path))
        self.assertEqual(exported["rows"], 1)
        self.assertTrue(output_path.exists())


if __name__ == "__main__":
    unittest.main()
