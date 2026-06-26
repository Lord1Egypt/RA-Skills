#!/usr/bin/env python3
"""Tests for export_csv."""

from __future__ import annotations

import csv
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import export_csv  # noqa: E402
from bird_json_util import save_doc  # noqa: E402


class TestExportMain(unittest.TestCase):
    def test_missing_bird_json(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td)
            with patch("sys.argv", ["export_csv.py", "--workspace", str(ws)]):
                self.assertEqual(export_csv.main(), 2)

    def test_stdout_with_summary_errors(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td)
            save_doc(ws, {"observations": []})
            with patch(
                "sys.argv",
                ["export_csv.py", "--workspace", str(ws), "--output", "-", "--summary"],
            ):
                self.assertEqual(export_csv.main(), 3)


class TestExportCsv(unittest.TestCase):
    def test_writes_rows_and_summary(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td)
            doc = {
                "version": 1,
                "location_query": "上海",
                "country_code": "CN",
                "region": {
                    "code": "CN-31",
                    "name": "Shanghai",
                    "name_cn": "上海",
                    "kind": "region",
                    "parent": "CN",
                    "match_score": 0.9,
                },
                "observations": [
                    {
                        "time_utc": "2026-01-02T10:00:00+00:00",
                        "species": "A",
                        "notes": "n1",
                        "source": "text",
                        "image_path": None,
                        "birdid_stdout": None,
                    },
                    {
                        "time_utc": "2026-01-03T11:00:00+00:00",
                        "species": "A",
                        "notes": "",
                        "source": "photo",
                        "image_path": "/x/a.jpg",
                        "birdid_stdout": None,
                    },
                ],
            }
            save_doc(ws, doc)
            main_csv = ws / "workspace" / "out.csv"
            sum_csv = ws / "workspace" / "out_by_species.csv"
            export_csv.write_observations_csv(doc, main_csv, excel_bom=False)
            export_csv.write_summary_csv(doc, sum_csv, excel_bom=False)
            text = main_csv.read_text(encoding="utf-8")
            self.assertIn("ebird_region_code", text)
            self.assertIn("CN-31", text)
            self.assertIn("A", text)
            with sum_csv.open(encoding="utf-8", newline="") as fh:
                rows = list(csv.DictReader(fh))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["species"], "A")
            self.assertEqual(rows[0]["count"], "2")

    def test_stdout_mode(self) -> None:
        doc = {
            "location_query": "",
            "country_code": "",
            "region": None,
            "observations": [{"time_utc": "t", "species": "S", "notes": "", "source": "text"}],
        }
        buf = io.StringIO()
        with patch("sys.stdout", buf):
            export_csv.write_observations_csv(doc, None, excel_bom=False)
        out = buf.getvalue()
        self.assertIn("species", out.splitlines()[0])
        self.assertIn("S", out)


if __name__ == "__main__":
    unittest.main()
