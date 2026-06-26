#!/usr/bin/env python3
"""Tests for append_sighting."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import append_sighting  # noqa: E402
from bird_json_util import load_doc  # noqa: E402


class TestAppend(unittest.TestCase):
    def test_appends_observation(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td)
            with patch(
                "sys.argv",
                [
                    "append_sighting.py",
                    "--workspace",
                    str(ws),
                    "--species",
                    "Test Bird",
                    "--source",
                    "text",
                    "--notes",
                    "n1",
                ],
            ):
                self.assertEqual(append_sighting.main(), 0)
            doc = load_doc(ws)
            self.assertEqual(len(doc["observations"]), 1)
            self.assertEqual(doc["observations"][0]["species"], "Test Bird")
            self.assertEqual(doc["observations"][0]["notes"], "n1")


if __name__ == "__main__":
    unittest.main()
