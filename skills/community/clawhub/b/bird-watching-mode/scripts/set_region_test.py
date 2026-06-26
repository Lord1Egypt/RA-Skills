#!/usr/bin/env python3
"""Tests for set_region (mocked region-query)."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import set_region  # noqa: E402


class TestRunRegionQuery(unittest.TestCase):
    @patch("set_region.subprocess.run")
    def test_parses_json_lines(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='{"score":0.9,"code":"CN-31","name":"Shanghai","name_cn":"上海","kind":"region","parent":"CN"}\n',
            stderr="",
        )
        rows = set_region.run_region_query("shanghai", limit=5)
        self.assertEqual(len(rows), 1)
        self.assertAlmostEqual(rows[0][0], 0.9)
        self.assertEqual(rows[0][1]["code"], "CN-31")


class TestSetRegionMain(unittest.TestCase):
    @patch("set_region.run_region_query")
    def test_writes_bird_json(self, mock_rq: MagicMock) -> None:
        mock_rq.return_value = [
            (
                0.95,
                {
                    "score": 0.95,
                    "code": "CN-31",
                    "name": "Shanghai",
                    "name_cn": "上海",
                    "kind": "region",
                    "parent": "CN",
                },
            ),
        ]
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td)
            with patch("sys.argv", ["set_region.py", "--workspace", str(ws), "--location", "上海"]):
                rc = set_region.main()
            self.assertEqual(rc, 0)
            from bird_json_util import load_doc

            doc = load_doc(ws)
            self.assertEqual(doc["country_code"], "CN")
            self.assertEqual(doc["region"]["code"], "CN-31")

    @patch("set_region.run_region_query")
    def test_disambiguate_exits_3(self, mock_rq: MagicMock) -> None:
        mock_rq.return_value = [
            (0.91, {"score": 0.91, "code": "A", "name": "a", "name_cn": "", "kind": "country", "parent": ""}),
            (0.90, {"score": 0.90, "code": "B", "name": "b", "name_cn": "", "kind": "country", "parent": ""}),
        ]
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td)
            argv = [
                "set_region.py",
                "--workspace",
                str(ws),
                "--location",
                "x",
                "--disambiguate",
            ]
            with patch("sys.argv", argv):
                rc = set_region.main()
            self.assertEqual(rc, 3)


if __name__ == "__main__":
    unittest.main()
