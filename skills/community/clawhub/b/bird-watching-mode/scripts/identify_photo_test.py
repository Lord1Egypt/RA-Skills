#!/usr/bin/env python3
"""Tests for identify_photo command building."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import identify_photo  # noqa: E402


class TestBirdidCmd(unittest.TestCase):
    def test_country_only(self) -> None:
        img = Path("/tmp/x.jpg")
        cmd = identify_photo.birdid_cmd_for_region(
            img,
            {"kind": "country", "code": "CN", "parent": ""},
            top=3,
            extra_args=[],
        )
        self.assertIn("--birdid", cmd)
        self.assertIn("identify", cmd)
        self.assertIn("-t3", cmd)
        self.assertIn("-c", cmd)
        idx = cmd.index("-c")
        self.assertEqual(cmd[idx + 1], "CN")
        self.assertNotIn("-r", cmd)

    def test_subregion(self) -> None:
        img = Path("/tmp/x.jpg")
        cmd = identify_photo.birdid_cmd_for_region(
            img,
            {"kind": "region", "code": "CN-31", "parent": "CN"},
            top=5,
            extra_args=["--no-yolo"],
        )
        self.assertIn("-c", cmd)
        self.assertIn("-r", cmd)
        ri = cmd.index("-r")
        self.assertEqual(cmd[ri + 1], "CN-31")
        self.assertIn("--no-yolo", cmd)


if __name__ == "__main__":
    unittest.main()
