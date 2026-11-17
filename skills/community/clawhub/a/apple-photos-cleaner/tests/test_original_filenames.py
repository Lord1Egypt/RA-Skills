#!/usr/bin/env python3
"""
Original filenames for people, storage names for identity (#38).

On current macOS ZASSET.ZFILENAME is Photos' internal storage name (a UUID), so
previews listed "B3E2E2AA-….jpeg". The name the user knows lives in
ZADDITIONALASSETATTRIBUTES.ZORIGINALFILENAME. It is display-only: the AppleScript
cross-check must keep comparing against ZFILENAME.
"""

import sqlite3

import pytest
from test_new_scripts import create_full_test_db

from _common import build_identifier_lists, display_name


@pytest.fixture
def db_path(tmp_path) -> str:
    """The full fixture with UUID-style storage names and real original names, like a modern library."""
    path = tmp_path / "Photos.sqlite"
    conn = sqlite3.connect(path)
    create_full_test_db().backup(conn)
    conn.executescript("""
        ALTER TABLE ZADDITIONALASSETATTRIBUTES ADD COLUMN ZORIGINALFILENAME TEXT;
        UPDATE ZADDITIONALASSETATTRIBUTES SET ZORIGINALFILENAME = 'Original_' || ZASSET || '.HEIC';
        UPDATE ZASSET SET ZFILENAME = 'UUID-' || Z_PK || '.heic';
    """)
    conn.commit()
    conn.close()
    return str(path)


def test_display_name_prefers_the_original():
    assert display_name({"filename": "UUID-1.heic", "original_filename": "IMG_1.HEIC"}) == "IMG_1.HEIC"
    assert display_name({"filename": "UUID-1.heic", "original_filename": None}) == "UUID-1.heic"
    assert display_name({"filename": "UUID-1.heic"}) == "UUID-1.heic"


def test_cleanup_preview_shows_original_names(db_path):
    from cleanup_executor import format_summary, get_cleanup_candidates

    data = get_cleanup_candidates(db_path=db_path, category="all_screenshots")
    candidate = data["candidates"][0]
    assert candidate["filename"].startswith("UUID-")
    assert candidate["original_filename"].startswith("Original_")
    summary = format_summary(data)
    assert candidate["original_filename"] in summary
    assert candidate["filename"] not in summary
    assert data["degraded"] == []


def test_applescript_identity_still_uses_the_storage_name(db_path):
    """The cross-check compares the resolved item's filename with ZFILENAME; the display name must not leak in."""
    from cleanup_executor import generate_trash_applescript, get_cleanup_candidates

    candidates = get_cleanup_candidates(db_path=db_path, category="all_screenshots")["candidates"]
    _, names = build_identifier_lists(candidates)
    assert candidates[0]["filename"] in names
    assert "Original_" not in names
    assert "Original_" not in generate_trash_applescript(candidates)


def test_export_plan_items_carry_both_names(db_path):
    from smart_export import generate_export_plan

    plan = generate_export_plan(db_path=db_path, favorites_only=True)
    items = [item for folder in plan["folders"].values() for item in folder["items"]]
    assert items
    assert all(i["filename"].startswith("UUID-") and i["original_filename"].startswith("Original_") for i in items)


@pytest.mark.parametrize(
    ("module", "call", "items"),
    [
        ("junk_finder", lambda m, db: m.find_junk(db_path=db), lambda r: r["screenshots"]),
        ("best_photos", lambda m, db: m.find_best_photos(db_path=db, min_quality=0.0), lambda r: r["top_photos"]),
        ("storage_analyzer", lambda m, db: m.analyze_storage(db_path=db), lambda r: r["storage_hogs"]),
    ],
)
def test_reports_include_original_names(db_path, module, call, items):
    import importlib

    result = call(importlib.import_module(module), db_path)
    listed = items(result)
    assert listed, f"{module}: fixture should yield items"
    assert all(i["original_filename"].startswith("Original_") for i in listed)


def test_missing_column_degrades_to_storage_names(tmp_path):
    from cleanup_executor import format_summary, get_cleanup_candidates

    path = tmp_path / "Photos.sqlite"
    conn = sqlite3.connect(path)
    create_full_test_db().backup(conn)
    conn.close()
    data = get_cleanup_candidates(db_path=str(path), category="all_screenshots")
    assert data["candidates"][0]["original_filename"] is None
    assert data["candidates"][0]["filename"] in format_summary(data)
    assert {
        "section": "original_filenames",
        "reason": "missing column(s): ZADDITIONALASSETATTRIBUTES.ZORIGINALFILENAME",
    } in data["degraded"]
