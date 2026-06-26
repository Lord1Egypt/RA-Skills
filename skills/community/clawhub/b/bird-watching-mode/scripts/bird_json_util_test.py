#!/usr/bin/env python3
"""Tests for bird_json_util."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from bird_json_util import (  # noqa: E402
    default_doc,
    infer_country_code,
    load_doc,
    save_doc,
    workspace_bird_path,
)


class TestInferCountry(unittest.TestCase):
    def test_country(self) -> None:
        self.assertEqual(
            infer_country_code({"kind": "country", "code": "CN", "parent": ""}),
            "CN",
        )

    def test_region_with_parent(self) -> None:
        self.assertEqual(
            infer_country_code(
                {"kind": "region", "code": "CN-31", "parent": "CN"},
            ),
            "CN",
        )

    def test_region_code_split(self) -> None:
        self.assertEqual(
            infer_country_code({"kind": "region", "code": "AU-SA", "parent": ""}),
            "AU",
        )


class TestLoadSave(unittest.TestCase):
    def test_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td)
            doc = default_doc()
            doc["location_query"] = "test"
            save_doc(ws, doc)
            p = workspace_bird_path(ws)
            self.assertTrue(p.is_file())
            loaded = load_doc(ws)
            self.assertEqual(loaded["location_query"], "test")
            self.assertEqual(loaded["observations"], [])

    def test_merge_invalid_observations_reset(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td)
            p = workspace_bird_path(ws)
            p.parent.mkdir(parents=True)
            p.write_text(json.dumps({"observations": "bad"}), encoding="utf-8")
            loaded = load_doc(ws)
            self.assertEqual(loaded["observations"], [])


if __name__ == "__main__":
    unittest.main()
