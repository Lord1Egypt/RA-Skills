#!/usr/bin/env python3
"""
Graceful degradation contract (ROADMAP T1.4).

Drops every column of the full fixture, one at a time, and runs every script
against the result. A script must never crash (exit 1). If the column is one of
its REQUIRED_COLUMNS it exits 5 (schema unsupported). Otherwise it succeeds, and
if the column feeds one of its OPTIONAL_COLUMNS sections, that section is listed
in the result's ``degraded``.
"""

import contextlib
import importlib
import io
import json
import logging
import sqlite3
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from test_new_scripts import create_full_test_db

from _common import ExitCode
from _schema import resolve

SCRIPTS = sorted(p.stem for p in (Path(__file__).resolve().parent.parent / "scripts").glob("[a-z]*.py"))


def script_args(script: str, tmp_path: Path) -> list[str]:
    return {
        "cleanup_executor": ["--category", "all_screenshots"],
        "smart_export": ["--output-dir", str(tmp_path / "export"), "--plan-only", "--format", "json"],
        "doctor": ["--format", "json"],
        # Search mode lists files (and so original names); inventory mode only counts scenes.
        "scene_search": ["--search", "beach"],
    }.get(script, [])


def required_columns(module, script: str) -> tuple[str, ...]:
    """REQUIRED_COLUMNS plus what the arguments used here additionally require."""
    if script == "cleanup_executor":
        return module.REQUIRED_COLUMNS + module.CATEGORY_COLUMNS["all_screenshots"]
    return module.REQUIRED_COLUMNS


# Optional columns the shared fixture lacks, so every declared section is exercised.
EXTRA_COLUMNS = [
    ("ZASSET", "ZCLOUDLOCALSTATE INTEGER DEFAULT 1"),
    ("ZASSET", "ZCLOUDISMYASSET INTEGER DEFAULT 1"),
    ("ZASSET", "ZCLOUDISDOWNLOADABLE INTEGER DEFAULT 1"),
    ("ZASSET", "ZKINDSUBTYPE INTEGER DEFAULT 2"),
    ("ZASSET", "ZPLAYBACKSTYLE INTEGER DEFAULT 3"),
    ("ZASSET", "ZLIBRARYSCOPE INTEGER DEFAULT 0"),
    ("ZASSET", "ZSHAREDLIBRARYSCOPEIDENTIFIER INTEGER"),
    ("ZADDITIONALASSETATTRIBUTES", "ZORIGINALFILENAME TEXT DEFAULT 'IMG_0001.HEIC'"),
    ("ZDETECTEDFACE", "ZQUALITYMEASURE REAL DEFAULT 0.6"),
    ("ZDETECTEDFACE", "ZBLURSCORE REAL DEFAULT 0.1"),
    ("ZDETECTEDFACE", "ZSMILESCORE REAL DEFAULT 0.5"),
    ("ZDETECTEDFACE", "ZSIZE REAL DEFAULT 0.2"),
    ("ZDETECTEDFACE", "ZYAWANGLE REAL DEFAULT 0.1"),
    ("ZDETECTEDFACE", "ZFACEISINCENTER INTEGER DEFAULT 1"),
    ("ZCOMPUTEDASSETATTRIBUTES", "ZHARMONIOUSCOLORSCORE REAL DEFAULT 0.5"),
    ("ZCOMPUTEDASSETATTRIBUTES", "ZPLEASANTWALLPAPERSCORE REAL DEFAULT 0.5"),
    ("ZCOMPUTEDASSETATTRIBUTES", "ZWEIGHTEDSCENECLASSIFICATIONSCORE REAL DEFAULT 0.5"),
    *(
        ("ZCOMPUTEDASSETATTRIBUTES", f"{column} REAL DEFAULT 0.5")
        for column in (
            "ZPLEASANTCOLORHUESCORE",
            "ZIMMERSIVENESSSCORE",
            "ZINTERACTIONSCORE",
            "ZPLEASANTSHARPSCORE",
            "ZTASTEFULLYBLURREDSCORE",
            "ZWELLFRAMEDSUBJECTSCORE",
            "ZWELLTIMEDSHOTSCORE",
        )
    ),
]


# Real libraries also carry a spatial R*Tree; nothing may trip the read-only guard over it.
RTREE = "CREATE VIRTUAL TABLE Z_RT_Asset_boundedByRect USING rtree(Z_PK, ZMINX, ZMAXX, ZMINY, ZMAXY)"


def create_rich_db() -> sqlite3.Connection:
    conn = create_full_test_db()
    for table, column in EXTRA_COLUMNS:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column}")
    conn.execute(RTREE)
    conn.commit()
    return conn


def fixture_columns() -> list[tuple[str, str]]:
    conn = create_rich_db()
    tables = [
        row[0]
        for row in conn.execute("SELECT name, sql FROM sqlite_master WHERE type = 'table' ORDER BY name")
        if not row[1].upper().startswith("CREATE VIRTUAL TABLE") and not row[0].startswith("Z_RT_")
    ]
    return [(table, row[1]) for table in tables for row in conn.execute(f'PRAGMA table_info("{table}")') if not row[5]]


def physical(names) -> set[str]:
    """Expand declared names (logical or physical) to every "ZTABLE.ZCOLUMN" they may resolve to."""
    return {f"{table}.{column}" for name in names for table, columns in [resolve(name)] for column in columns}


def run(script: str, db: Path, tmp_path: Path, extra: list[str] | None = None) -> tuple[int, str]:
    module = importlib.import_module(script)
    out = io.StringIO()
    argv = [script, "--db-path", str(db), *script_args(script, tmp_path), *(extra or [])]
    with (
        patch.object(sys, "argv", argv),
        contextlib.redirect_stdout(out),
        contextlib.redirect_stderr(io.StringIO()),
        patch("logging.basicConfig"),
    ):
        try:
            code = module.main()
        except SystemExit as exc:
            code = exc.code
    return code, out.getvalue()


@pytest.fixture(autouse=True)
def quiet_logging():
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)


def db_without(tmp_path: Path, table: str | None, column: str | None) -> Path:
    path = tmp_path / "Photos.sqlite"
    target = sqlite3.connect(path)
    create_rich_db().backup(target)
    if table:
        target.execute(f'ALTER TABLE "{table}" DROP COLUMN "{column}"')
        target.commit()
    target.close()
    return path


@pytest.mark.parametrize("script", SCRIPTS)
def test_every_script_declares_its_contract(script):
    module = importlib.import_module(script)
    assert isinstance(module.REQUIRED_COLUMNS, tuple)
    assert isinstance(module.OPTIONAL_COLUMNS, dict)
    for name in [*module.REQUIRED_COLUMNS, *(n for names in module.OPTIONAL_COLUMNS.values() for n in names)]:
        resolve(name)  # every declared name must be valid


def test_full_fixture_runs_clean(tmp_path):
    """With every declared column present, nothing is degraded."""
    db = db_without(tmp_path, None, None)
    failures = []
    for script in SCRIPTS:
        code, out = run(script, db, tmp_path)
        if code != ExitCode.OK:
            failures.append(f"{script}: exit {code}")
        elif "degraded" not in (result := json.loads(out)):
            failures.append(f"{script}: JSON result has no 'degraded' field")
        elif result["degraded"]:
            failures.append(f"{script}: degraded {result['degraded']}")
    assert not failures, failures


def test_every_declared_column_is_exercised():
    """Guard the guard: a declared column absent from the fixture is never dropped by the sweep."""
    present = {f"{table}.{column}" for table, column in fixture_columns()}
    unexercised = sorted(
        f"{script}: {name}"
        for script in SCRIPTS
        for name in (
            *importlib.import_module(script).REQUIRED_COLUMNS,
            *(n for names in importlib.import_module(script).OPTIONAL_COLUMNS.values() for n in names),
        )
        if not physical([name]) & present
    )
    assert not unexercised, unexercised


@pytest.mark.parametrize(("table", "column"), fixture_columns(), ids=lambda v: v)
def test_dropping_a_column_never_crashes(table, column, tmp_path):
    db = db_without(tmp_path, table, column)
    dropped = f"{table}.{column}"
    problems = []
    for script in SCRIPTS:
        module = importlib.import_module(script)
        if not hasattr(module, "REQUIRED_COLUMNS"):
            problems.append(f"{script}: no schema contract declared")
            continue
        code, out = run(script, db, tmp_path)
        if dropped in physical(required_columns(module, script)):
            if code != ExitCode.SCHEMA_UNSUPPORTED:
                problems.append(f"{script}: required column dropped, expected exit 5, got {code}")
            continue
        if code != ExitCode.OK:
            problems.append(f"{script}: exit {code} (declare it required, or degrade)")
            continue
        result = json.loads(out)
        if "degraded" not in result:
            problems.append(f"{script}: JSON result has no 'degraded' field")
            continue
        sections = [s for s, names in module.OPTIONAL_COLUMNS.items() if dropped in physical(names)]
        if sections:
            reported = {entry["section"] for entry in result["degraded"]}
            problems.extend(f"{script}: section {s!r} not reported as degraded" for s in sections if s not in reported)
    assert not problems, f"dropping {dropped}:\n" + "\n".join(problems)


def test_export_album_filter_finds_a_renumbered_junction_table(tmp_path):
    """smart_export used to hardcode Z_27ASSETS/Z_3ASSETS; Core Data renumbers them per version."""
    db = db_without(tmp_path, None, None)
    conn = sqlite3.connect(db)
    conn.executescript("""
        ALTER TABLE Z_27ASSETS RENAME TO Z_31ASSETS;
        ALTER TABLE Z_31ASSETS RENAME COLUMN Z_27ALBUMS TO Z_31ALBUMS;
        ALTER TABLE Z_31ASSETS RENAME COLUMN Z_3ASSETS TO Z_4ASSETS;
    """)
    title = conn.execute("SELECT ZTITLE FROM ZGENERICALBUM LIMIT 1").fetchone()[0]
    conn.close()

    import smart_export

    plan = smart_export.generate_export_plan(db_path=str(db), album_name=title, organize_by="album")
    assert plan["summary"]["total_photos"] > 0


def test_timeline_narrative_warns_about_degraded_sections(tmp_path):
    """--narrative bypasses JSON, so the warning must be in the text too."""
    db = db_without(tmp_path, "ZPERSON", "ZFULLNAME")
    with patch.object(sys, "argv", ["timeline_recap", "--db-path", str(db), "--narrative"]):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            import timeline_recap

            assert timeline_recap.main() == ExitCode.OK
    assert "Not fully available" in out.getvalue()
    assert "people: missing column(s): ZPERSON.ZFULLNAME" in out.getvalue()


def test_missing_catalog_face_count_is_null_not_zero(tmp_path):
    import people_analyzer

    db = db_without(tmp_path, "ZPERSON", "ZFACECOUNT")
    result = people_analyzer.analyze_people(db_path=str(db), min_photos=1)
    assert result["people"], "fixture should yield people"
    assert all(person["face_count"] is None for person in result["people"])
    assert "catalog_face_count" in {entry["section"] for entry in result["degraded"]}


# Arguments / data that make a script list at least one file, so an empty result can't pass vacuously.
ITEM_PRODUCING: dict[str, tuple[list[str], str]] = {
    "on_this_day": (["--date", "2025-03-03"], ""),
    "people_analyzer": (["--min-photos", "1"], ""),
    # Two photos with identical timestamp and dimensions form a timestamp_dimensions group.
    "duplicate_finder": (
        [],
        "UPDATE ZASSET SET ZDATECREATED = (SELECT ZDATECREATED FROM ZASSET WHERE Z_PK = 1), "
        "ZWIDTH = (SELECT ZWIDTH FROM ZASSET WHERE Z_PK = 1), ZHEIGHT = (SELECT ZHEIGHT FROM ZASSET WHERE Z_PK = 1), "
        "ZKIND = 0, ZDUPLICATEASSETVISIBILITYSTATE = 0 WHERE Z_PK IN (1, 2);",
    ),
    # A large local-only (unsynced) item is listed by name.
    "icloud_status": (
        [],
        "UPDATE ZASSET SET ZCLOUDLOCALSTATE = 0 WHERE Z_PK = 1;"
        "UPDATE ZADDITIONALASSETATTRIBUTES SET ZORIGINALFILESIZE = 50000000 WHERE ZASSET = 1;",
    ),
}


@pytest.mark.parametrize(
    "script", [s for s in SCRIPTS if "original_filenames" in importlib.import_module(s).OPTIONAL_COLUMNS]
)
def test_declared_sections_reach_the_output(script, tmp_path):
    """A declared section must affect what's shown: warning about data the output never contains misleads."""
    db = db_without(tmp_path, None, None)
    args, sql = ITEM_PRODUCING.get(script, ([], ""))
    if sql:
        conn = sqlite3.connect(db)
        conn.executescript(sql)
        conn.commit()
        conn.close()
    code, out = run(script, db, tmp_path, extra=args)
    assert code == ExitCode.OK
    assert '"original_filename"' in out, f"{script} declares original_filenames but never outputs it"
