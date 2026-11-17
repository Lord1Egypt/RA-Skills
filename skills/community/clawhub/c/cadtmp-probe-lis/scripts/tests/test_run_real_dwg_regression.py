#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2]
import sys
sys.path.insert(0, str(SKILL_DIR / "scripts"))
from run_real_dwg_regression import _cache_hits_from_json  # noqa: E402


class CacheHelperTest(unittest.TestCase):
    def test_cache_hits_parsed(self):
        with tempfile.TemporaryDirectory(prefix="cad-regcache-") as tmp:
            path = Path(tmp) / "report.json"
            path.write_text(json.dumps({"cache": {"hits": 3, "misses": 1}}), encoding="utf-8")
            self.assertEqual(_cache_hits_from_json(path), 3)

    def test_missing_cache_returns_none(self):
        with tempfile.TemporaryDirectory(prefix="cad-regcache-") as tmp:
            path = Path(tmp) / "report.json"
            path.write_text(json.dumps({"summary": {}}), encoding="utf-8")
            self.assertEqual(_cache_hits_from_json(path), 0)

    def test_invalid_json_returns_none(self):
        with tempfile.TemporaryDirectory(prefix="cad-regcache-") as tmp:
            path = Path(tmp) / "report.json"
            path.write_text("not json", encoding="utf-8")
            self.assertIsNone(_cache_hits_from_json(path))


if __name__ == "__main__":
    unittest.main()
