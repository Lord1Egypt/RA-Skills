from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2]
sys_path = SKILL_DIR / "scripts"

import sys
sys.path.insert(0, str(sys_path))

from cad_cache_admin import cache_cleanup, cache_stats, inspect_cache_file  # noqa: E402
from cad_scan_cache import (  # noqa: E402
    file_digest,
    save_cached_scan,
)


PROFILE = {
    "cache_version": 2,
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
RECS = [{"kind": "TEXT", "text": "A", "x": 1.0, "y": 1.0,
         "layer": "L", "sheet": 1}]
META = {"sheets": [{"id": 1, "texts": 1, "bbox": [0, 0, 10, 10]}]}
SEGS = [(0.0, 0.0, 1.0, 1.0)]
SEG_LAYERS = ["L"]


class CacheAdminTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.cache = self.root / "cache"
        self.cache.mkdir(parents=True, exist_ok=True)
        self.source = self.root / "sample.dxf"
        self.source.write_bytes(b"cad-cache-admin")

    def current(self, name="cad-scan-v2-current.sqlite"):
        path = self.cache / name
        saved = save_cached_scan(
            self.source, self.cache, file_digest(self.source), PROFILE,
            RECS, ["L"], META, SEGS, SEG_LAYERS, [],
        )
        return Path(saved or path)

    def legacy(self, name="cad-scan-v1-old.sqlite"):
        path = self.cache / name
        conn = sqlite3.connect(path)
        try:
            conn.execute("CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT)")
            conn.execute("INSERT INTO metadata VALUES('cache_version','1')")
            conn.execute("INSERT INTO metadata VALUES('source_sha256',?)", ("a" * 64,))
            conn.execute("INSERT INTO metadata VALUES('record_count','1')")
            conn.execute("INSERT INTO metadata VALUES('geometry_count','1')")
        finally:
            conn.close()
        return path

    def temp_file(self, name="writer.tmp"):
        path = self.cache / name
        path.write_bytes(b"partial")
        return path

    def corrupt_file(self, name="cad-scan-v2-corrupt.sqlite"):
        path = self.cache / name
        path.write_bytes(b"not sqlite")
        return path

    def unknown_file(self, name="keep.txt"):
        path = self.cache / name
        path.write_text("not cache")
        return path

    def mixed(self):
        return [self.current(), self.legacy(), self.temp_file(),
                self.corrupt_file(), self.unknown_file()]

    def test_inventory_classifies_five_categories(self):
        paths = self.mixed()
        stats = cache_stats(self.cache)
        self.assertEqual(set(stats["categories"]), {
            "current", "legacy", "temp", "corrupt", "unknown"})
        by_name = {Path(x["file"]).name: x for x in stats["files"]}
        self.assertEqual(by_name[paths[0].name]["category"], "current")
        self.assertEqual(by_name[paths[1].name]["category"], "legacy")
        self.assertEqual(by_name[paths[2].name]["category"], "temp")
        self.assertEqual(by_name[paths[3].name]["category"], "corrupt")
        self.assertEqual(by_name[paths[4].name]["category"], "unknown")
        self.assertEqual(stats["total"]["files"], 5)

    def test_inspect_current_reports_counts_and_profile(self):
        path = self.current()
        info = inspect_cache_file(path)
        self.assertEqual(info["category"], "current")
        self.assertEqual(info["record_count"], 1)
        self.assertEqual(info["geometry_count"], 1)
        self.assertEqual(len(info["source_sha256"]), 64)
        self.assertEqual(len(info["profile_sha256"]), 12)

    def test_dry_run_does_not_delete_any_file(self):
        paths = self.mixed()
        result = cache_cleanup(self.cache)
        self.assertTrue(result["dry_run"])
        self.assertEqual(result["candidate_files"], 2)
        self.assertEqual(result["removed_files"], 2)
        self.assertTrue(all(p.exists() for p in paths))
        self.assertIsNone(result["stats_after"])

    def test_apply_deletes_temp_and_legacy_only(self):
        paths = self.mixed()
        result = cache_cleanup(self.cache, dry_run=False)
        self.assertFalse(result["dry_run"])
        self.assertEqual(result["removed_files"], 2)
        self.assertEqual(result["failed"], [])
        self.assertFalse(paths[1].exists())
        self.assertFalse(paths[2].exists())
        self.assertTrue(paths[0].exists())
        self.assertTrue(paths[3].exists())
        self.assertTrue(paths[4].exists())
        self.assertIsNotNone(result["stats_after"])
        self.assertEqual(result["stats_after"]["total"]["files"], 3)

    def test_corrupt_and_unknown_never_cleanup(self):
        corrupt = self.corrupt_file()
        unknown = self.unknown_file()
        result = cache_cleanup(self.cache, dry_run=False)
        self.assertEqual(result["removed_files"], 0)
        self.assertEqual(result["candidate_files"], 0)
        self.assertTrue(corrupt.exists())
        self.assertTrue(unknown.exists())
        stats = cache_stats(self.cache)
        self.assertEqual(stats["categories"]["corrupt"]["files"], 1)
        self.assertEqual(stats["categories"]["unknown"]["files"], 1)

    def test_current_requires_explicit_flag_and_limit(self):
        path = self.current()
        no_limit = cache_cleanup(self.cache, include_current=True, dry_run=False)
        self.assertEqual(no_limit["removed_files"], 0)
        no_flag = cache_cleanup(
            self.cache, max_total_bytes=0, dry_run=False)
        self.assertEqual(no_flag["removed_files"], 0)
        self.assertTrue(path.exists())

    def test_current_capacity_cleanup_can_remove(self):
        path = self.current()
        result = cache_cleanup(
            self.cache, include_current=True, max_total_bytes=0, dry_run=False)
        self.assertEqual(result["removed_files"], 1)
        self.assertFalse(path.exists())
        self.assertEqual(result["stats_after"]["total"]["files"], 0)


if __name__ == "__main__":
    unittest.main()
