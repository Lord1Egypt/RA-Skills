#!/usr/bin/env python3
"""
Doctor: diagnose why a command can't run, and say how to fix it (ROADMAP T1.10).

Checks Python, where the Photos library is, Full Disk Access, the database
schema (macOS version, fingerprint, which features degrade), library size,
"Optimize Mac Storage", and optionally Automation permission for Photos.app.

Read-only. ``--schema-dump`` prints table definitions only (no rows) so a new
macOS schema can be shared in an issue (ROADMAP T1.2).
"""

import argparse
import importlib
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import Any

# Must be the first project import: on Python < 3.10 it exits with the fix before _common fails to import.
import _bootstrap
from _common import (
    DatabaseNotFoundError,
    ExitCode,
    PhotosDB,
    add_common_args,
    connect_db,
    emit_result,
    find_photos_db,
    format_size,
    handle_cli_error,
    setup_logging,
)
from _schema import OLDEST_SUPPORTED_MODEL_VERSION, SchemaRegistry, get_schema, macos_for_model_version

# Schema contract (T1.4): doctor reads whatever exists and reports the rest.
REQUIRED_COLUMNS: tuple[str, ...] = ()
OPTIONAL_COLUMNS: dict[str, tuple[str, ...]] = {}

SCRIPTS_DIR = Path(__file__).resolve().parent
# Next to the scripts so it ships with an installed copy (package data), not only in the repo.
FINGERPRINTS_PATH = SCRIPTS_DIR / "schema-fingerprints.json"
MIN_PYTHON = _bootstrap.MIN_PYTHON
SCHEMA_ISSUE_URL = "https://github.com/and3rn3t/apple-photos-cleaner/issues/new"
# Below this share of originals on disk, "Optimize Mac Storage" is probably on.
OPTIMIZED_THRESHOLD = 0.9

OK, WARN, FAIL, SKIP = "ok", "warn", "fail", "skip"


def check(name: str, status: str, detail: str, fix: str | None = None) -> dict[str, Any]:
    return {"name": name, "status": status, "detail": detail, "fix": fix}


def check_python() -> dict[str, Any]:
    version = ".".join(map(str, sys.version_info[:3]))
    if sys.version_info[:2] >= MIN_PYTHON:
        return check("python", OK, f"Python {version}")
    return check(
        "python",
        FAIL,
        f"Python {version} is older than {'.'.join(map(str, MIN_PYTHON))}",
        "Install a current Python (`brew install python`) and run with `python3` from it",
    )


def locate_database(path: str | None) -> tuple[str | None, dict[str, Any]]:
    """Resolve --db-path/--library (a .sqlite file or a .photoslibrary bundle) or the default location."""
    try:
        if path:
            resolved = PhotosDB(path).db_path
            if not os.path.exists(resolved):
                raise DatabaseNotFoundError(f"No Photos database at {resolved}")
        else:
            resolved = find_photos_db()
    except DatabaseNotFoundError as e:
        return None, check(
            "library",
            FAIL,
            str(e).splitlines()[0],
            "Pass the library explicitly: --library '/path/to/Photos Library.photoslibrary' "
            "(Photos > Settings > General shows its location)",
        )
    return resolved, check("library", OK, resolved)


def open_database(db_path: str) -> tuple[sqlite3.Connection | None, dict[str, Any]]:
    try:
        conn = connect_db(db_path)
        conn.execute("SELECT count(*) FROM sqlite_schema").fetchone()
    except PermissionError:
        return None, check(
            "read_access",
            FAIL,
            "macOS is blocking read access to the Photos database",
            "Grant Full Disk Access to the app running this command (Terminal, iTerm, VS Code, "
            "Claude…): System Settings > Privacy & Security > Full Disk Access, then restart that app",
        )
    except sqlite3.DatabaseError as e:
        return None, check(
            "read_access",
            FAIL,
            f"Could not read the database: {e}",
            "Check the path points at a Photos library's database/Photos.sqlite; if Photos is mid-upgrade, "
            "open Photos once and let it finish",
        )
    return conn, check("read_access", OK, "Photos.sqlite is readable (read-only)")


def load_known_fingerprints() -> dict[str, dict[str, Any]]:
    try:
        known: dict[str, dict[str, Any]] = json.loads(FINGERPRINTS_PATH.read_text(encoding="utf-8"))["fingerprints"]
    except (OSError, ValueError, KeyError):
        return {}
    return known


def script_modules() -> list[Any]:
    names = sorted(p.stem for p in SCRIPTS_DIR.glob("[a-z]*.py") if p.stem != "doctor")
    return [importlib.import_module(name) for name in names]


def feature_report(schema: SchemaRegistry, db_path: str | None = None) -> dict[str, Any]:
    """Check every script's declared contract against this library.

    A section listed in a script's ALTERNATE_SOURCES is still available when that source exists
    (e.g. scene labels from the search index on macOS 26), so it isn't reported as degraded.
    """
    unavailable, degraded, refused = [], [], []
    for module in script_modules():
        command = module.__name__
        if missing := schema.missing(*module.REQUIRED_COLUMNS):
            unavailable.append({"command": command, "missing": missing})
        alternates = getattr(module, "ALTERNATE_SOURCES", {})
        limitations = getattr(module, "SOURCE_LIMITATIONS", {})
        for section, names in module.OPTIONAL_COLUMNS.items():
            if missing := schema.missing(*names):
                if section in alternates and alternates[section](db_path):
                    continue
                degraded.append({"command": command, "section": section, "missing": missing})
            elif section in limitations and (reason := limitations[section](schema, db_path)):
                # Columns present, but the source the command will use can't supply this section.
                degraded.append({"command": command, "section": section, "missing": [], "reason": reason})
        for kind in ("CATEGORY_COLUMNS", "FILTER_COLUMNS"):
            for option, names in getattr(module, kind, {}).items():
                if missing := schema.missing(*names):
                    refused.append({"command": command, "option": option, "missing": missing})
    return {"unavailable_commands": unavailable, "degraded_sections": degraded, "unavailable_options": refused}


def check_schema(schema: SchemaRegistry) -> tuple[dict[str, Any], dict[str, Any]]:
    fingerprint = schema.fingerprint()
    model_version = schema.model_version()
    known = load_known_fingerprints().get(fingerprint)
    macos = known["macos"] if known else macos_for_model_version(model_version)
    info = {
        "fingerprint": fingerprint,
        "model_version": model_version,
        "macos": macos,
        "known_fingerprint": known is not None,
    }
    contribute = (
        f"Run `doctor.py --schema-dump > schema.sql` and attach it to an issue ({SCHEMA_ISSUE_URL}) "
        "so this schema becomes known. It contains table definitions only, no photos or metadata."
    )
    if known:
        return info, check("schema", OK, f"{macos} schema (known fingerprint)")
    if macos and model_version is not None and model_version < OLDEST_SUPPORTED_MODEL_VERSION:
        return info, check(
            "schema", WARN, f"{macos} schema (model {model_version}) is older than the tested range", contribute
        )
    if macos:
        return info, check(
            "schema", WARN, f"{macos} schema (model {model_version}), but this exact variant is new", contribute
        )
    label = f"model {model_version}" if model_version is not None else "no model version"
    return info, check("schema", WARN, f"Unrecognized schema ({label}); some features may be degraded", contribute)


def features_with_check(schema: SchemaRegistry, db_path: str) -> tuple[dict[str, Any], dict[str, Any]]:
    features = feature_report(schema, db_path)
    return features, check_features(features)


def check_features(features: dict[str, Any]) -> dict[str, Any]:
    unavailable = features["unavailable_commands"]
    degraded = features["degraded_sections"]
    refused = features["unavailable_options"]
    if not (unavailable or degraded or refused):
        return check("features", OK, "Every command and section is available")
    parts = []
    if unavailable:
        parts.append(f"unavailable: {', '.join(item['command'] for item in unavailable)}")
    if degraded:
        sections = ", ".join(f"{d['command']}.{d['section']}" for d in degraded)
        parts.append(f"degraded: {sections}")
    if refused:
        options = ", ".join(f"{r['command']} {r['option']}" for r in refused)
        parts.append(f"options refused: {options}")
    # A warning, not a failure: nothing is broken locally, this macOS version just lacks the data.
    return check(
        "features",
        WARN,
        "; ".join(parts),
        "These depend on columns this macOS version's Photos database doesn't have; see `features` in "
        "--format json for the exact columns. Nothing to fix locally. Report it if you think it's wrong.",
    )


def library_stats(conn: sqlite3.Connection, schema: SchemaRegistry) -> tuple[dict[str, Any], dict[str, Any]]:
    if not (schema.has("ZASSET.ZTRASHEDSTATE") and schema.has("ZASSET.ZKIND")):
        return {}, check("library_size", SKIP, "Asset columns not found")
    size_join = (
        "LEFT JOIN ZADDITIONALASSETATTRIBUTES aa ON a.Z_PK = aa.ZASSET"
        if schema.has("ZADDITIONALASSETATTRIBUTES.ZORIGINALFILESIZE")
        and schema.has("ZADDITIONALASSETATTRIBUTES.ZASSET")
        else ""
    )
    size_expr = "SUM(aa.ZORIGINALFILESIZE)" if size_join else "NULL"
    row = conn.execute(f"""
        SELECT COUNT(*) AS assets,
               SUM(a.ZKIND = 0) AS photos,
               SUM(a.ZKIND = 1) AS videos,
               {size_expr} AS bytes
        FROM ZASSET a
        {size_join}
        WHERE a.ZTRASHEDSTATE != 1
    """).fetchone()
    stats = {
        "assets": row["assets"] or 0,
        "photos": row["photos"] or 0,
        "videos": row["videos"] or 0,
        "original_bytes": row["bytes"],
        "original_size": format_size(row["bytes"]) if row["bytes"] is not None else None,
    }
    size = f", {stats['original_size']} of originals" if stats["original_size"] else ""
    return stats, check(
        "library_size", OK, f"{stats['assets']:,} assets ({stats['photos']:,} photos, {stats['videos']:,} videos){size}"
    )


def count_files(root: Path) -> int:
    total = 0
    for _dirpath, _dirnames, filenames in os.walk(root):
        total += sum(1 for name in filenames if not name.startswith("."))
    return total


def check_optimize_storage(db_path: str, assets: int | None) -> dict[str, Any]:
    """Heuristic: with "Optimize Mac Storage" on, many originals live only in iCloud."""
    originals = Path(db_path).resolve().parent.parent / "originals"
    if not assets or not originals.is_dir():
        return check("optimize_storage", SKIP, "Can't tell (no originals folder next to this database)")
    on_disk = count_files(originals)
    share = on_disk / assets
    if share >= OPTIMIZED_THRESHOLD:
        return check(
            "optimize_storage", OK, f"Originals appear to be on this Mac ({on_disk:,} files for {assets:,} assets)"
        )
    return check(
        "optimize_storage",
        WARN,
        f'"Optimize Mac Storage" looks on: about {share:.0%} of originals are on this Mac '
        f"({on_disk:,} files for {assets:,} assets)",
        "Analysis is unaffected. Exports of iCloud-only items need Photos to download them first; to keep "
        "everything local choose Photos > Settings > iCloud > Download Originals to this Mac",
    )


def check_automation(enabled: bool) -> dict[str, Any]:
    fix = (
        "System Settings > Privacy & Security > Automation: allow your terminal/agent app to control Photos. "
        "Only cleanup_executor and smart_export need this"
    )
    if not enabled:
        return check(
            "automation",
            SKIP,
            "Not checked (it can launch Photos and show a permission prompt)",
            "Run doctor with --check-automation to test it",
        )
    try:
        result = subprocess.run(
            ["osascript", "-e", 'tell application "Photos" to get name'],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        return check("automation", FAIL, f"Could not run osascript: {e}", fix)
    if result.returncode == 0:
        return check("automation", OK, "Photos.app accepts AppleScript automation")
    if "-1743" in result.stderr:
        return check("automation", FAIL, "Not authorized to send Apple events to Photos", fix)
    return check("automation", FAIL, result.stderr.strip() or "osascript failed", fix)


def diagnose(path: str | None, check_automation_flag: bool = False) -> dict[str, Any]:
    checks = [check_python()]
    report: dict[str, Any] = {"degraded": [], "checks": checks, "schema": None, "features": None, "library": None}

    db_path, located = locate_database(path)
    checks.append(located)
    conn = None
    if db_path:
        conn, readable = open_database(db_path)
        checks.append(readable)
    else:
        checks.append(check("read_access", SKIP, "Needs the library to be found"))

    if conn is not None and db_path is not None:
        try:
            schema = get_schema(conn)
            report["schema"], schema_check = guarded("schema", lambda: check_schema(schema), (None,))
            report["features"], features_check = guarded(
                "features", lambda: features_with_check(schema, db_path), (None,)
            )
            report["library"], size_check = guarded("library_size", lambda: library_stats(conn, schema), ({},))
            checks += [schema_check, features_check, size_check]
            checks.append(check_optimize_storage(db_path, (report["library"] or {}).get("assets")))
        finally:
            conn.close()
    else:
        checks += [
            check(name, SKIP, "Needs a readable database")
            for name in ("schema", "features", "library_size", "optimize_storage")
        ]

    checks.append(check_automation(check_automation_flag))
    report["ok"] = all(c["status"] != FAIL for c in checks)
    return report


def guarded(name: str, run: Any, fallback: tuple) -> tuple[Any, dict[str, Any]]:
    """Run one database-backed check; a database error fails that check instead of the whole report."""
    try:
        value, result = run()
    except sqlite3.DatabaseError as e:
        return fallback[0], check(
            name,
            FAIL,
            f"Database error while checking {name}: {e}",
            "Re-run with --verbose and include the output in an issue; this is a bug in the tool, not your library",
        )
    return value, result


def exit_code(report: dict[str, Any]) -> ExitCode:
    failed = {c["name"] for c in report["checks"] if c["status"] == FAIL}
    if "library" in failed:
        return ExitCode.DB_NOT_FOUND
    if "read_access" in failed:
        return ExitCode.PERMISSION_DENIED
    return ExitCode.ERROR if failed else ExitCode.OK


# Every report lists these, in this order; checks that couldn't run are "skip".
CHECK_NAMES = (
    "python",
    "library",
    "read_access",
    "schema",
    "features",
    "library_size",
    "optimize_storage",
    "automation",
)

ICONS = {OK: "✅", WARN: "⚠️ ", FAIL: "❌", SKIP: "⏭️ "}


def format_report(report: dict[str, Any]) -> str:
    lines = ["🩺 PHOTOS CLEANER DOCTOR", "=" * 50]
    for c in report["checks"]:
        lines.append(f"{ICONS[c['status']]} {c['name']}: {c['detail']}")
        if c["fix"] and c["status"] in (WARN, FAIL, SKIP):
            lines.append(f"     → {c['fix']}")
    if report["schema"]:
        lines += ["", f"Schema fingerprint: {report['schema']['fingerprint'][:16]}…"]
    lines += ["", "All good." if report["ok"] else "Fix the ❌ items above, then re-run doctor."]
    return "\n".join(lines)


def schema_dump(path: str | None) -> str:
    db_path, located = locate_database(path)
    if db_path is None:
        raise DatabaseNotFoundError(located["detail"])
    with PhotosDB(db_path) as conn:
        schema = get_schema(conn)
        header = [
            "-- apple-photos-cleaner schema dump: table definitions only, no rows.",
            f"-- fingerprint: {schema.fingerprint()}",
            f"-- model_version: {schema.model_version()}",
            f"-- macos (from model version): {macos_for_model_version(schema.model_version())}",
        ]
        return "\n".join(header + [f"{sql};" for sql in schema.ddl()]) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Diagnose setup problems: library location, permissions, schema, storage",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s
  %(prog)s --format json
  %(prog)s --library ~/Pictures/Other.photoslibrary --check-automation
  %(prog)s --schema-dump > schema.sql
        """,
    )
    add_common_args(parser, default_format="human")
    parser.add_argument(
        "--check-automation",
        action="store_true",
        help="Also test AppleScript access to Photos.app (may launch Photos and prompt)",
    )
    parser.add_argument(
        "--schema-dump", action="store_true", help="Print the database's table definitions (no rows) and exit"
    )

    args = parser.parse_args()
    setup_logging(verbose=args.verbose, quiet=args.quiet)
    path = args.db_path or args.library

    try:
        if args.schema_dump:
            sys.stdout.write(schema_dump(path))
            return ExitCode.OK
        report = diagnose(path, check_automation_flag=args.check_automation)
        if args.format != "human":
            emit_result(report, args)
        else:
            print(format_report(report))
        return exit_code(report)
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        return ExitCode.USER_ABORTED
    except Exception as e:
        return handle_cli_error(e)


if __name__ == "__main__":
    sys.exit(main())
