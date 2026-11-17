#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
import sqlite3
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

SKILL_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from cad_scan_cache import (  # noqa: E402
    CACHE_VERSION,
    file_digest,
    load_cached_scan,
    profile_for,
    save_cached_scan,
)

PROFILE = {
    "cache_version": CACHE_VERSION,
    "kind": "cad_scan_raw",
    "want": ["text"],
    "with_insert": False,
    "with_blocks": False,
    "with_geom": True,
    "with_geom_layer": True,
    "budget": 45.0,
    "max_rows": 200000,
    "no_sheet": False,
    "sheets": "grid",
    "sheet_min": 1,
    "sheet_bin": 1000.0,
}

RECS = [
    {"kind": "TEXT", "text": "A1", "x": 100.0, "y": 100.0,
     "layer": "L1", "sheet": 1},
    {"kind": "TEXT", "text": "B1", "x": 5000.0, "y": 5000.0,
     "layer": "L2", "sheet": 2},
]
META = {
    "block_refs": {"FRAME": 2},
    "insert_count": 2,
    "block_defs": ["FRAME"],
    "sheets": [
        {"id": 1, "texts": 1, "bbox": [0.0, 0.0, 1000.0, 1000.0]},
        {"id": 2, "texts": 1, "bbox": [5000.0, 5000.0, 6000.0, 6000.0]},
    ],
}
SEGS = [
    (0.0, 0.0, 100.0, 100.0),
    (5000.0, 5000.0, 5100.0, 5100.0),
]
SEG_LAYERS = ["L1", "L2"]


class CadScanCacheTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "sample.dxf"
        self.source.write_bytes(b"cad-fixture")
        self.cache = self.root / "cache"
        self.digest = file_digest(self.source)

    def save(self, notes=None, profile=None, recs=None, meta=None):
        return save_cached_scan(
            self.source, self.cache, self.digest, profile or PROFILE,
            RECS if recs is None else recs, ["L1", "L2"], META or {},
            SEGS, SEG_LAYERS, notes or [],
        )

    def save_with_segs(self, segs):
        return save_cached_scan(
            self.source, self.cache, self.digest, PROFILE,
            RECS, ["L1", "L2"], META, segs, SEG_LAYERS, [],
        )

    def test_full_roundtrip_and_layer_order(self):
        self.assertIsNotNone(self.save())
        loaded = load_cached_scan(self.source, self.cache, self.digest, PROFILE)
        self.assertIsNotNone(loaded)
        self.assertFalse(loaded["partial"])
        self.assertEqual(loaded["recs"], RECS)
        self.assertEqual(loaded["layers"], ["L1", "L2"])
        self.assertEqual(loaded["meta"], META)
        self.assertEqual(loaded["segs"], SEGS)
        self.assertEqual(loaded["seg_layers"], SEG_LAYERS)

    def test_digest_change_misses(self):
        self.save()
        self.assertIsNone(load_cached_scan(self.source, self.cache, "0" * 64, PROFILE))

    def test_profile_change_misses(self):
        self.save()
        other = dict(PROFILE)
        other["sheets"] = "frame"
        self.assertIsNone(load_cached_scan(self.source, self.cache, self.digest, other))

    def test_roi_filters_records_geometry_and_sheets(self):
        self.save()
        loaded = load_cached_scan(
            self.source, self.cache, self.digest, PROFILE,
            roi=(-100.0, -100.0, 1000.0, 1000.0),
        )
        self.assertTrue(loaded["partial"])
        self.assertEqual([r["text"] for r in loaded["recs"]], ["A1"])
        self.assertEqual(loaded["segs"], [SEGS[0]])
        self.assertEqual(loaded["seg_layers"], ["L1"])
        self.assertEqual([s["id"] for s in loaded["meta"]["sheets"]], [1])

    def test_sheet_filters_records_geometry_and_sheets(self):
        self.save()
        loaded = load_cached_scan(
            self.source, self.cache, self.digest, PROFILE, sheet=2,
        )
        self.assertTrue(loaded["partial"])
        self.assertEqual([r["text"] for r in loaded["recs"]], ["B1"])
        self.assertEqual(loaded["segs"], [SEGS[1]])
        self.assertEqual(loaded["seg_layers"], ["L2"])
        self.assertEqual([s["id"] for s in loaded["meta"]["sheets"]], [2])

    def test_partial_result_does_not_leak_block_statistics(self):
        self.save()
        loaded = load_cached_scan(
            self.source, self.cache, self.digest, PROFILE,
            roi=(-100.0, -100.0, 1000.0, 1000.0),
        )
        self.assertNotIn("block_refs", loaded["meta"])
        self.assertNotIn("insert_count", loaded["meta"])
        self.assertNotIn("block_defs", loaded["meta"])

    def test_geometry_bbox_columns_support_indexed_roi(self):
        path = self.save()
        self.assertIsNotNone(path)
        loaded = load_cached_scan(
            self.source, self.cache, self.digest, PROFILE,
            roi=(-100.0, -100.0, 1000.0, 1000.0),
        )
        self.assertEqual(loaded["segs"], [SEGS[0]])
        conn = sqlite3.connect(path)
        try:
            row = conn.execute(
                "SELECT xmin, ymin, xmax, ymax FROM geometry "
                "WHERE x1=5000.0 AND y1=5000.0"
            ).fetchone()
            self.assertEqual(row, (5000.0, 5000.0, 5100.0, 5100.0))
            plan = " ".join(map(str, conn.execute(
                "EXPLAIN QUERY PLAN SELECT x1 FROM geometry "
                "WHERE xmin <= 1000.0 AND xmax >= -100.0 "
                "AND ymin <= 1000.0 AND ymax >= -100.0"
            ).fetchall()))
        finally:
            conn.close()
        self.assertIn("geometry_bbox", plan)

    def test_invalid_geometry_prevents_cache_write(self):
        result = self.save_with_segs([(0.0, 0.0, float("nan"), 100.0)])
        self.assertIsNone(result)
        self.assertFalse(self.cache.exists() and any(self.cache.iterdir()))

    def test_incomplete_notes_prevent_cache_write(self):
        cases = (
            ["text 解码超 3s 预算，已终止"],
            ["line 解码失败：no rows"],
            ["文字数达上限 1，已截断"],
            ["DXF 几何解码不可用：missing ezdxf"],
        )
        for notes in cases:
            with self.subTest(notes=notes):
                cache = self.root / ("blocked-" + str(abs(hash(tuple(notes)))))
                result = save_cached_scan(
                    self.source, cache, self.digest, PROFILE,
                    RECS, ["L1"], META, SEGS, SEG_LAYERS, notes,
                )
                self.assertIsNone(result)
                self.assertFalse(cache.exists() and any(cache.iterdir()))

    def test_sheet_ids_stay_local_in_cache(self):
        self.save()
        loaded = load_cached_scan(self.source, self.cache, self.digest, PROFILE)
        self.assertEqual([s["id"] for s in loaded["meta"]["sheets"]], [1, 2])
        self.assertEqual([r["sheet"] for r in loaded["recs"]], [1, 2])

    def test_profile_includes_sheet_parameters(self):
        args = SimpleNamespace(
            with_insert=True, with_blocks=True, with_geom=True,
            with_geom_layer=True, budget=3.5, max_rows=7,
            no_sheet=True, sheets="frame", sheet_min=4, sheet_bin=900.0,
        )
        profile = profile_for(args, {"text", "mtext"})
        self.assertEqual(profile["no_sheet"], True)
        self.assertEqual(profile["sheets"], "frame")
        self.assertEqual(profile["sheet_min"], 4)
        self.assertEqual(profile["sheet_bin"], 900.0)


if __name__ == "__main__":
    unittest.main()
