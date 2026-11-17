#!/usr/bin/env python3
"""
Screen recordings are not screenshots (#37).

Photos sets ZISDETECTEDSCREENSHOT on screen recordings too. Found on a real
macOS 26 library: `cleanup_executor --category old_screenshots` listed a .mov,
so "delete old screenshots" would have deleted screen recordings as well.
"""

import sqlite3

import pytest
from test_new_scripts import create_full_test_db

from _common import SCREEN_RECORDING_SQL, SCREENSHOT_SQL, is_screen_recording, is_screenshot

RECORDING_UUID = "SCREEN-RECORDING-UUID"


@pytest.fixture
def db_with_recording(tmp_path) -> str:
    """The full fixture plus one old screen recording: a copy of its old screenshot, made a video."""
    path = tmp_path / "Photos.sqlite"
    conn = sqlite3.connect(path)
    create_full_test_db().backup(conn)
    conn.executescript(f"""
        CREATE TEMP TABLE rec AS SELECT * FROM ZASSET WHERE ZISDETECTEDSCREENSHOT = 1 LIMIT 1;
        UPDATE rec SET Z_PK = 9001, ZUUID = '{RECORDING_UUID}', ZFILENAME = 'ScreenRecording.mov', ZKIND = 1;
        INSERT INTO ZASSET SELECT * FROM rec;
        INSERT INTO ZADDITIONALASSETATTRIBUTES (ZASSET, ZORIGINALFILESIZE, ZORIGINALWIDTH, ZORIGINALHEIGHT)
            VALUES (9001, 25000000, 1920, 1080);
    """)
    conn.commit()
    conn.close()
    return str(path)


class TestDefinitions:
    @pytest.mark.parametrize(
        ("flag", "kind", "screenshot", "recording"),
        [(1, 0, True, False), (1, 1, False, True), (0, 0, False, False), (0, 1, False, False)],
    )
    def test_python_and_sql_agree(self, flag, kind, screenshot, recording):
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            f"SELECT ? AS ZISDETECTEDSCREENSHOT, ? AS ZKIND, "
            f"(SELECT {SCREENSHOT_SQL} FROM (SELECT ? AS ZISDETECTEDSCREENSHOT, ? AS ZKIND) a) AS s, "
            f"(SELECT {SCREEN_RECORDING_SQL} FROM (SELECT ? AS ZISDETECTEDSCREENSHOT, ? AS ZKIND) a) AS r",
            (flag, kind, flag, kind, flag, kind),
        ).fetchone()
        assert is_screenshot(row) is screenshot is bool(row["s"])
        assert is_screen_recording(row) is recording is bool(row["r"])
        assert is_screenshot(dict(row)) is screenshot

    def test_rows_without_kind_fall_back_to_the_flag(self):
        assert is_screenshot({"ZISDETECTEDSCREENSHOT": 1})


class TestCleanup:
    @pytest.mark.parametrize("category", ["old_screenshots", "all_screenshots"])
    def test_screenshot_categories_exclude_recordings(self, db_with_recording, category):
        from cleanup_executor import get_cleanup_candidates

        data = get_cleanup_candidates(db_path=db_with_recording, category=category, screenshot_age_days=30)
        uuids = {c["uuid"] for c in data["candidates"]}
        assert RECORDING_UUID not in uuids
        assert uuids, "the fixture's real screenshot is still a candidate"

    def test_screen_recordings_category(self, db_with_recording):
        from cleanup_executor import get_cleanup_candidates

        data = get_cleanup_candidates(db_path=db_with_recording, category="screen_recordings")
        assert [c["uuid"] for c in data["candidates"]] == [RECORDING_UUID]
        assert data["summary"]["category"] == "screen_recordings"


def test_junk_finder_reports_recordings_separately(db_with_recording):
    from junk_finder import find_junk

    junk = find_junk(db_path=db_with_recording)
    assert [r["filename"] for r in junk["screen_recordings"]] == ["ScreenRecording.mov"]
    assert "ScreenRecording.mov" not in {s["filename"] for s in junk["screenshots"] + junk["old_screenshots"]}
    assert junk["totals"]["screen_recordings"] == 1
    # Conservative savings (old screenshots + bursts) must not include the 25 MB recording.
    conservative = junk["estimated_savings"]["conservative"]["bytes"]
    assert conservative == sum(s["size"] for s in junk["old_screenshots"]) + sum(
        b["size"] for b in junk["burst_leftovers"]
    )


def test_library_analysis_counts(db_with_recording):
    from library_analysis import analyze_library

    by_type = analyze_library(db_path=db_with_recording)["by_type"]
    assert by_type["screen_recordings"] == 1
    assert by_type["screenshots"] == 1  # the fixture's single real screenshot


def test_storage_analyzer_sources(db_with_recording):
    from storage_analyzer import analyze_storage

    by_source = analyze_storage(db_path=db_with_recording)["by_source"]
    assert by_source["screen_recordings"]["count"] == 1
    assert by_source["screen_recordings"]["total_bytes"] == 25_000_000
    assert by_source["screenshots"]["count"] == 1


def test_storage_human_output_labels_each_source(db_with_recording):
    from storage_analyzer import analyze_storage, format_summary

    text = format_summary(analyze_storage(db_path=db_with_recording))
    section = text.split("By Source:")[1].split("\n\n")[0]
    labels = [line.split(":")[0].strip() for line in section.strip().splitlines()]
    assert sorted(labels) == ["Photos & Videos", "Screen Recordings", "Screenshots"]
