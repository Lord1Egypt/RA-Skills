#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest import mock

SKILL_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

import cad_scan  # noqa: E402


def build_case():
    block_rows = [
        [0x100, "TREE-A", None, None],
        [0x101, "*MODEL_SPACE", None, None],
        [0x102, "SHRUB-B", None, None],
    ]
    # owner for block TREE-A = 0x100, SHRUB-B = 0x102, modelspace = 0x101
    placement_rows = [
        [0x10, 0, 0x101],
        [0x20, 0, 0x100],
        [0x21, 0, 0x100],
        [0x30, 0, 0x102],
    ]
    geom_rows = {
        0x10: ([(1000, 1000, 2000, 1000)], {"L-TREE"}),
        0x20: ([(0, 0, 1, 0), (1, 0, 1, 1)], {"L-PLANT"}),
        0x21: ([(0, 0, 1, 1)], {"L-PLANT"}),
        0x30: ([(5, 5, 6, 6)], {"L-SHRUB"}),
    }
    return block_rows, placement_rows, geom_rows


class DwgBlockGeomTests(unittest.TestCase):
    def test_build_groups_by_owner(self):
        block_rows, placement_rows, geom_rows = build_case()
        out, notes = cad_scan._build_dwg_block_geometries(block_rows, placement_rows, geom_rows)
        self.assertEqual(sorted(out), ["SHRUB-B", "TREE-A"])
        self.assertEqual(len(out["TREE-A"]["segments"]), 3)
        self.assertEqual(out["TREE-A"]["layers"], ["L-PLANT"])
        self.assertNotIn("*MODEL_SPACE", out)
        self.assertFalse(notes)

    def test_missing_placements_falls_back_with_note(self):
        block_rows, _, geom_rows = build_case()
        out, notes = cad_scan._build_dwg_block_geometries(block_rows, [], geom_rows)
        self.assertEqual(out, {})
        self.assertTrue(any("实体归属表" in n for n in notes))

    def test_no_named_blocks(self):
        out, notes = cad_scan._build_dwg_block_geometries([[0x0, "*MODEL_SPACE", None, None]], [], {})
        self.assertEqual(out, {})
        self.assertTrue(any("未解出命名块" in n for n in notes))

    def test_max_blocks_truncation(self):
        block_rows, placement_rows, geom_rows = build_case()
        out, notes = cad_scan._build_dwg_block_geometries(
            block_rows, placement_rows, geom_rows, max_blocks=1
        )
        self.assertLessEqual(len(out), 1)
        self.assertTrue(any("已截断" in n for n in notes))

    @mock.patch("cad_scan._rows")
    def test_wrapper_uses_worker_rows(self, mock_rows):
        blocks, placements, _ = build_case()
        side_effect = {
            "blocks": [[r[0], r[1], None, None] for r in blocks],
            "placements": [[r[0], r[1], r[2]] for r in placements],
            "line": [],
            "lwpoly": [
                [0x20, None, [0, 0, 1, 0, 1, 0, 2, 1], "L-PLANT"],
                [0x30, None, [5, 5, 6, 6], "L-SHRUB"],
            ],
        }

        def fake_rows(name, path, budget, notes):
            return side_effect.get(name) or []

        mock_rows.side_effect = fake_rows
        logs = []
        out, notes = cad_scan.dwg_block_geometries("/tmp/x.dwg", 30.0, logs.append)
        self.assertIn("TREE-A", out)
        # line rows absent in mock => lwpoly only; flat pts yield 3 edge segs
        self.assertEqual(len(out["TREE-A"]["segments"]), 3)
        self.assertIn("SHRUB-B", out)


if __name__ == "__main__":
    unittest.main()


class BigDrawingGuardTests(unittest.TestCase):
    @mock.patch("cad_scan._rows")
    def test_geometry_segments_roi_filters(self, mock_rows):
        mock_rows.side_effect = lambda name, path, budget, notes: {
            "line": [[1, None, [0, 0, 50, 0], "L"], [2, None, [100, 100, 110, 100], "L"]],
            "lwpoly": [],
        }[name]
        segs, notes = cad_scan.geometry_segments("/tmp/x.dwg", 30.0, lambda m: None, roi=(5, -5, 20, 5))
        self.assertEqual(len(segs), 1)
        self.assertFalse(notes)

    @mock.patch("cad_scan._rows")
    def test_geometry_segments_max_rows_truncates(self, mock_rows):
        mock_rows.side_effect = lambda name, path, budget, notes: {
            "line": [[1, None, [0, 0, 1, 0], "L"], [2, None, [2, 0, 3, 0], "L"], [3, None, [4, 0, 5, 0], "L"]],
            "lwpoly": [],
        }[name]
        segs, notes = cad_scan.geometry_segments("/tmp/x.dwg", 30.0, lambda m: None, max_rows=2)
        self.assertEqual(len(segs), 2)
        self.assertTrue(any("已截断" in n for n in notes))

    @mock.patch("cad_scan._rows")
    def test_dwg_records_roi_filters(self, mock_rows):
        def fake(name, path, budget, notes):
            if name == "layers":
                return [[1, "L-TREE", None, None]]
            if name == "text":
                return [[1, "乔-国槐", [10, 10], "L-TREE"]]
            return []

        mock_rows.side_effect = fake
        recs, _, notes, _ = cad_scan.dwg_records("/tmp/x.dwg", {"text"}, 30.0, 200000, lambda m: None, roi=(20, 20, 30, 30))
        self.assertEqual(recs, [])
        recs2, _, notes2, _ = cad_scan.dwg_records("/tmp/x.dwg", {"text"}, 30.0, 200000, lambda m: None, roi=(0, 0, 20, 20))
        self.assertEqual(len(recs2), 1)

    @mock.patch("cad_scan._rows")
    def test_dxf_records_roi_filters(self, mock_rows):
        mock_rows.side_effect = lambda name, path, budget, notes: []
        from pathlib import Path as P
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            dxf = P(td) / "t.dxf"
            dxf.write_text('''0
SECTION
2
HEADER
0
ENDSEC
0
SECTION
2
ENTITIES
0
TEXT
8
L-TREE
10
10
20
10
1
乔-国槐
0
TEXT
8
L-SHRUB
10
100
20
100
1
紫薇
0
ENDSEC
0
EOF
''', encoding="utf-8")
            recs, _, notes, _ = cad_scan.dxf_records(str(dxf), 200000, lambda m: None)
            self.assertEqual(len(recs), 2)
            recs2, _, notes2, _ = cad_scan.dxf_records(str(dxf), 200000, lambda m: None, roi=(50, 50, 200, 200))
            self.assertEqual(len(recs2), 1)
            self.assertEqual(recs2[0]["text"], "紫薇")


class GarbleBlockNameTests(unittest.TestCase):
    def test_is_garble_name(self):
        self.assertTrue(cad_scan._is_garble_name("@` @`@@``@`€@`燖`繞`郂€@€"))
        self.assertFalse(cad_scan._is_garble_name("A"))
        self.assertFalse(cad_scan._is_garble_name("乔木-国槐"))

    def test_build_sanitizes_garble_block_keys(self):
        block_rows = [[0x10, "@` @`@@``@`€@`燖`繞`郂€", None, None],
                      [0x11, "A", None, None], [0x12, "*MODEL_SPACE", None, None]]
        placement_rows = [[0x20, 0, 0x10], [0x21, 0, 0x11]]
        geom = {0x20: ([(0, 0, 1, 1)], {"L"}), 0x21: ([(2, 2, 3, 3)], {"L"})}
        out, notes = cad_scan._build_dwg_block_geometries(block_rows, placement_rows, geom)
        self.assertEqual(sorted(out), ["A", "_BLK#1"])
        self.assertTrue(any("疑似乱码" in n for n in notes))

    @mock.patch("cad_scan._rows")
    def test_dwg_records_notes_empty_and_garble_insert_names(self, mock_rows):
        def fake(name, path, budget, notes):
            if name == "layers":
                return [[1, "L-PLANT", None, None]]
            if name == "insert":
                # worker 输出格式：[handle, 块名/空串, 坐标, 图层]
                return [[0x10, "", [100.0, 100.0], "L-PLANT"],
                        [0x11, "", [200.0, 200.0], "L-PLANT"]]
            if name == "blocks":
                return [[0x20, "@` @`@@``@`€@`燖`繞`郂€", None, None]]
            return []
        mock_rows.side_effect = fake
        recs, _, notes, meta = cad_scan.dwg_records(
            "/tmp/x.dwg", {"insert"}, 30.0, 200000, lambda m: None, want_blocks=True)
        self.assertEqual(meta["insert_count"], 2)
        self.assertTrue(any("块引用名解码为空" in n for n in notes))
        self.assertEqual(sorted(meta["block_defs"]), ["_BLK#1"])
