#!/usr/bin/env python3
"""
Scene labels from Photos' search index on macOS 26 (#35).

The fixture mirrors what a real macOS 26.7.2 library showed: ZSCENECLASSIFICATION
keyed by numeric ZSCENEIDENTIFIER / ZASSETATTRIBUTES with no names, and
database/search/psi.sqlite holding NUL-terminated labels (category 1500), their
synonyms (1501, owning_groupid → 1500), little-endian UUID halves, and an FTS5
table that must never be touched.
"""

import contextlib
import io
import json
import sqlite3
import sys
from pathlib import Path
from unittest.mock import patch

from test_new_scripts import create_full_test_db

from _common import ExitCode
from _scenes import (
    DATABASE,
    SEARCH_INDEX,
    SearchIndex,
    halves_to_uuid,
    scene_source,
    search_index_available,
    uuid_to_halves,
)

UUID = "BBBBBBBB-0000-0000-0000-00000000000{}".format
# label groups (category 1500) → photos; photo 7 is trashed, so it must never be counted
LABELS = {"Beach": [1, 7], "Outdoor": [1, 2], "Dog": [9]}
SYNONYMS = {"Seaside": "Beach"}


def make_index(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    psi = sqlite3.connect(path)
    psi.executescript("""
        CREATE TABLE groups(category INT2, owning_groupid INT, content_string TEXT, normalized_string TEXT,
                            lookup_identifier TEXT, score REAL, token_ranges_0 INT8, token_ranges_1 INT8);
        CREATE TABLE assets(uuid_0 INT, uuid_1 INT, creationDate INT, UNIQUE(uuid_0, uuid_1));
        CREATE TABLE ga(groupid INT, assetid INT, PRIMARY KEY(groupid, assetid));
        CREATE VIRTUAL TABLE prefix USING fts5(content='groups', normalized_string, category UNINDEXED);
    """)
    asset_rowid = {}
    for pk in sorted({pk for pks in LABELS.values() for pk in pks}):
        cur = psi.execute("INSERT INTO assets(uuid_0, uuid_1) VALUES (?, ?)", uuid_to_halves(UUID(pk)))
        asset_rowid[pk] = cur.lastrowid
    group_rowid = {}
    for label, pks in LABELS.items():
        cur = psi.execute(
            "INSERT INTO groups(category, owning_groupid, content_string, normalized_string, lookup_identifier) "
            "VALUES (1500, 0, ?, ?, 'opaque-id')",
            (label + "\x00", label.lower() + "\x00"),
        )
        group_rowid[label] = cur.lastrowid
        psi.executemany("INSERT INTO ga VALUES (?, ?)", [(cur.lastrowid, asset_rowid[pk]) for pk in pks])
    for synonym, owner in SYNONYMS.items():
        psi.execute(
            "INSERT INTO groups(category, owning_groupid, content_string, normalized_string) VALUES (1501, ?, ?, ?)",
            (group_rowid[owner], synonym + "\x00", synonym.lower() + "\x00"),
        )
    psi.commit()
    psi.close()


def make_library(root: Path, *, macos26: bool = True, index: bool = True) -> Path:
    bundle = root / "Lib.photoslibrary"
    (bundle / "database").mkdir(parents=True)
    db = bundle / "database" / "Photos.sqlite"
    conn = sqlite3.connect(db)
    create_full_test_db().backup(conn)
    if macos26:
        conn.executescript("""
            DROP TABLE ZSCENECLASSIFICATION;
            CREATE TABLE ZSCENECLASSIFICATION (Z_PK INTEGER PRIMARY KEY, ZCLASSIFICATIONTYPE INTEGER,
                ZSCENEIDENTIFIER INTEGER, ZASSETATTRIBUTES INTEGER, ZCONFIDENCE FLOAT);
            INSERT INTO ZSCENECLASSIFICATION VALUES (1, 0, 2147482999, 1, 0.9);
        """)
    conn.commit()
    conn.close()
    if index:
        make_index(bundle / "database" / "search" / "psi.sqlite")
    return bundle


def run(script: str, *argv: str) -> tuple[int, dict]:
    import importlib

    out = io.StringIO()
    with (
        patch.object(sys, "argv", [script, *argv]),
        contextlib.redirect_stdout(out),
        contextlib.redirect_stderr(io.StringIO()),
    ):
        code = importlib.import_module(script).main()
    return code, json.loads(out.getvalue())


def test_uuid_halves_round_trip():
    for pk in range(1, 10):
        assert halves_to_uuid(*uuid_to_halves(UUID(pk))) == UUID(pk)


class TestSource:
    def test_macos26_library_uses_the_search_index(self, tmp_path):
        from _common import connect_db

        conn = connect_db(str(make_library(tmp_path) / "database" / "Photos.sqlite"))
        assert scene_source(conn) == SEARCH_INDEX
        conn.close()

    def test_older_library_keeps_the_database(self, tmp_path):
        from _common import connect_db

        conn = connect_db(str(make_library(tmp_path, macos26=False) / "database" / "Photos.sqlite"))
        assert scene_source(conn) == DATABASE
        conn.close()

    def test_neither_source(self, tmp_path):
        from _common import connect_db

        conn = connect_db(str(make_library(tmp_path, index=False) / "database" / "Photos.sqlite"))
        assert scene_source(conn) is None
        conn.close()

    def test_index_without_expected_tables_is_not_a_source(self, tmp_path):
        bundle = make_library(tmp_path, index=False)
        psi = bundle / "database" / "search" / "psi.sqlite"
        psi.parent.mkdir()
        sqlite3.connect(psi).execute("CREATE TABLE unrelated (x)").connection.commit()
        assert not search_index_available(str(bundle / "database" / "Photos.sqlite"))


class TestSceneSearch:
    def test_search(self, tmp_path):
        code, result = run("scene_search", "--library", str(make_library(tmp_path)), "--search", "beach")
        assert code == ExitCode.OK
        assert result["source"] == SEARCH_INDEX
        assert [(r["id"], r["scene"], r["confidence"]) for r in result["results"]] == [(1, "Beach", None)]
        assert result["summary"]["total_matches"] == 1  # the trashed photo 7 is excluded
        assert {"scene": "Outdoor", "count": 1} in result["related_scenes"]
        reasons = {d["section"]: d["reason"] for d in result["degraded"]}
        assert "no per-photo confidence" in reasons["scene_confidence"]
        assert "scenes" not in reasons

    def test_synonyms_find_their_label(self, tmp_path):
        _, result = run("scene_search", "--library", str(make_library(tmp_path)), "--search", "seaside")
        assert [(r["id"], r["scene"]) for r in result["results"]] == [(1, "Beach")]

    def test_year_filter(self, tmp_path):
        lib = str(make_library(tmp_path))
        _, in_year = run("scene_search", "--library", lib, "--search", "outdoor", "--year", "2025")
        assert [r["id"] for r in in_year["results"]] == [2]

    def test_inventory(self, tmp_path):
        code, result = run("scene_search", "--library", str(make_library(tmp_path)))
        assert code == ExitCode.OK
        counts = {s["scene"]: s["photo_count"] for s in result["scenes"]}
        assert counts == {"Outdoor": 2, "Beach": 1, "Dog": 1}  # NUL stripped, trashed excluded
        assert {s["scene"] for s in result["categories"]["animals"]} == {"Dog"}
        assert {s["scene"] for s in result["categories"]["nature_outdoor"]} == {"Beach"}

    def test_no_source_degrades_instead_of_failing(self, tmp_path):
        code, result = run("scene_search", "--library", str(make_library(tmp_path, index=False)), "--search", "beach")
        assert code == ExitCode.OK
        assert "error" in result
        assert "scenes" in {d["section"] for d in result["degraded"]}

    def test_older_library_unchanged(self, tmp_path):
        _, result = run("scene_search", "--library", str(make_library(tmp_path, macos26=False)), "--search", "beach")
        assert result["source"] == DATABASE
        assert result["results"] and result["results"][0]["confidence"] is not None


def test_on_this_day_and_timeline_use_the_index(tmp_path):
    lib = str(make_library(tmp_path))
    _, memories = run("on_this_day", "--library", lib, "--date", "2026-03-03")
    scenes = {s["scene"] for year in memories["years"] for s in year["scenes"] or []}
    assert {"Beach", "Outdoor"} <= scenes
    assert "scenes" not in {d["section"] for d in memories["degraded"]}

    _, timeline = run("timeline_recap", "--library", lib)
    event_scenes = {
        s["scene"] for day in timeline["timeline"] for event in day["events"] for s in event["scenes"] or []
    }
    assert {"Beach", "Outdoor", "Dog"} <= event_scenes


def test_doctor_counts_the_index_as_a_scene_source(tmp_path):
    lib = str(make_library(tmp_path))
    _, report = run("doctor", "--library", lib, "--format", "json")
    features = report["features"]
    assert not any(d["section"] == "scenes" for d in features["degraded_sections"])
    assert "scene_search" not in {u["command"] for u in features["unavailable_commands"]}

    _, without = run("doctor", "--library", str(make_library(tmp_path / "b", index=False)), "--format", "json")
    assert ("scene_search", "scenes") in {
        (d["command"], d["section"]) for d in without["features"]["degraded_sections"]
    }


class TestReviewFixes:
    def test_index_missing_a_query_column_is_not_a_source(self, tmp_path):
        bundle = make_library(tmp_path)
        psi = sqlite3.connect(bundle / "database" / "search" / "psi.sqlite")
        psi.execute("ALTER TABLE groups DROP COLUMN owning_groupid")
        psi.commit()
        psi.close()
        assert not search_index_available(str(bundle / "database" / "Photos.sqlite"))

    def test_doctor_reports_the_confidence_limitation(self, tmp_path):
        _, report = run("doctor", "--library", str(make_library(tmp_path)), "--format", "json")
        entry = next(d for d in report["features"]["degraded_sections"] if d["section"] == "scene_confidence")
        assert entry["command"] == "scene_search"
        assert "no per-photo confidence" in entry["reason"]

    def test_human_output_shows_the_error(self, tmp_path):
        from scene_search import format_summary, search_scenes

        lib = make_library(tmp_path, index=False)
        text = format_summary(search_scenes(db_path=str(lib / "database" / "Photos.sqlite")))
        assert "Scene labels aren't available" in text
        assert "Library total" not in text

    def test_undated_photos_sort_last(self, tmp_path):
        lib = make_library(tmp_path)
        conn = sqlite3.connect(lib / "database" / "Photos.sqlite")
        # Photo 1 predates the Core Data epoch (2001), so its timestamp is negative; photo 2 is undated.
        conn.execute("UPDATE ZASSET SET ZDATECREATED = -86400 * 365 WHERE Z_PK = 1")
        conn.execute("UPDATE ZASSET SET ZDATECREATED = NULL WHERE Z_PK = 2")
        conn.commit()
        conn.close()
        _, result = run("scene_search", "--library", str(lib), "--search", "outdoor", "--top", "1")
        assert [r["id"] for r in result["results"]] == [1]

    def test_related_scenes_only_come_from_shown_results(self, tmp_path):
        # "outdoor" matches photos 1 and 2; --top 1 shows only photo 2 (newest), which has no other label.
        _, result = run("scene_search", "--library", str(make_library(tmp_path)), "--search", "outdoor", "--top", "1")
        assert [r["id"] for r in result["results"]] == [2]
        assert result["related_scenes"] == []


def test_timeline_opens_the_index_once_for_all_events(tmp_path):
    """Reopening and querying the index per event made a real 15.7k-photo timeline take ~9 s."""
    lib = make_library(tmp_path)
    opened = []
    real_init = SearchIndex.__init__

    def counting_init(self, db_path):
        opened.append(db_path)
        real_init(self, db_path)

    with patch.object(SearchIndex, "__init__", counting_init):
        _, timeline = run("timeline_recap", "--library", str(lib))
    events = sum(len(day["events"]) for day in timeline["timeline"])
    assert events > 2, "fixture should span several events"
    # One open to choose the source (scene_source) and one to load every label; none per event.
    assert len(opened) <= 2


def test_only_the_requested_photos_labels_are_loaded(tmp_path):
    """on_this_day shows a few photos; it must not read every photo's labels from the index."""
    lib = make_library(tmp_path)
    requested = []
    real = SearchIndex.labels_for_uuids

    def recording(self, uuids):
        uuids = list(uuids)
        requested.extend(uuids)
        return real(self, uuids)

    with patch.object(SearchIndex, "labels_for_uuids", recording):
        run("on_this_day", "--library", str(lib), "--date", "2026-03-03")
    # Only the March-3 photos (1 and 2) were asked about, not the whole indexed library (1, 2, 7, 9).
    assert set(requested) == {UUID(1), UUID(2)}
