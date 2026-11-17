#!/usr/bin/env python3
"""
Smart export of photos organized by year/month, person, album, or location.
Uses AppleScript to trigger actual exports from Photos.app.

Items are targeted by their stable asset UUID (ZASSET.ZUUID), never by filename.
Photos filenames are not unique, so a filename search can match assets that the
export filters deliberately excluded — exporting more than the plan showed.
See export_with_applescript for the matching rules.
"""

import argparse
import io
import os
import re
import shlex
import subprocess
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any

from _common import (
    ExitCode,
    PhotosDB,
    add_common_args,
    build_identifier_lists,
    coredata_to_local,
    detect_face_schema,
    emit_result,
    escape_applescript,
    format_size,
    handle_cli_error,
    has_timezone_offset,
    local_datetime_sql,
    original_filename_sql,
    plan_token,
    require_uuid_support,
    sanitize_folder_name,
    setup_logging,
    tz_offset_sql,
)
from _schema import FACES, FILE_SIZE, ORIGINAL_FILENAME, Degradation, SchemaUnsupportedError, album_junction, get_schema

# Schema contract (T1.4): see _schema. Missing required → exit 5; missing optional → `degraded`.
REQUIRED_COLUMNS: tuple[str, ...] = (
    "ZASSET.ZDATECREATED",
    "ZASSET.ZFAVORITE",
    "ZASSET.ZFILENAME",
    "ZASSET.ZLATITUDE",
    "ZASSET.ZLONGITUDE",
    "ZASSET.ZTRASHEDSTATE",
    "asset.uuid",
    *FILE_SIZE,
)
# Export writes files, so a filter it cannot apply exactly refuses (exit 5) rather than degrading.
FILTER_COLUMNS: dict[str, tuple[str, ...]] = {
    "person": FACES,
    "album": ("ZGENERICALBUM.ZTITLE",),
}
OPTIONAL_COLUMNS: dict[str, tuple[str, ...]] = {"original_filenames": ORIGINAL_FILENAME}

# Counters reported back by the generated AppleScript.
_RESULT_RE = re.compile(r"EXPORTED:(\d+)\s+SKIPPED:(\d+)")


def generate_export_plan(
    db_path: str | None = None,
    organize_by: str = "year_month",
    favorites_only: bool = False,
    start_date: str | None = None,
    end_date: str | None = None,
    person_name: str | None = None,
    album_name: str | None = None,
) -> dict[str, Any]:
    """
    Generate an export plan showing what will be exported.

    Args:
        db_path: Path to database
        organize_by: How to organize ('year_month', 'person', 'album', 'location')
        favorites_only: Only export favorites
        start_date: Start date filter (YYYY-MM-DD)
        end_date: End date filter (YYYY-MM-DD)
        person_name: Export only photos with this person
        album_name: Export only from this album

    Returns:
        Export plan dictionary
    """
    with PhotosDB(db_path, require=REQUIRED_COLUMNS, operation="Export") as conn:
        name_col = original_filename_sql(get_schema(conn))
        degraded = Degradation(get_schema(conn))
        degraded.check("original_filenames", *OPTIONAL_COLUMNS["original_filenames"])
        cursor = conn.cursor()
        require_uuid_support(cursor, "Export")
        face_schema = detect_face_schema(cursor)
        registry = get_schema(conn)
        if person_name:
            registry.require(*FILTER_COLUMNS["person"], operation="Export --person")
        if album_name:
            registry.require(*FILTER_COLUMNS["album"], operation="Export --album")
        tz_available = has_timezone_offset(cursor)
        local_dt = local_datetime_sql(tz_available)

        # Build WHERE clauses
        where_clauses = ["a.ZTRASHEDSTATE != 1"]
        params: list[Any] = []

        if favorites_only:
            where_clauses.append("a.ZFAVORITE = 1")

        # Date filters compare local capture time as text ("YYYY-MM-DD HH:MM:SS"); both ends inclusive
        if start_date:
            where_clauses.append(f"{local_dt} >= ?")
            params.append(f"{date.fromisoformat(start_date).isoformat()} 00:00:00")

        if end_date:
            where_clauses.append(f"{local_dt} <= ?")
            params.append(f"{date.fromisoformat(end_date).isoformat()} 23:59:59")

        # Base query
        query = f"""
            SELECT
                a.Z_PK,
                a.ZUUID,
                a.ZFILENAME,
                {name_col},
                a.ZDATECREATED,
                a.ZLATITUDE,
                a.ZLONGITUDE,
                aa.ZORIGINALFILESIZE,
                {tz_offset_sql(tz_available)} AS tz_offset
            FROM ZASSET a
            LEFT JOIN ZADDITIONALASSETATTRIBUTES aa ON a.Z_PK = aa.ZASSET
        """

        # Add person filter if specified
        if person_name:
            query += f"""
                JOIN ZDETECTEDFACE df ON a.Z_PK = df.{face_schema["asset_fk"]}
                JOIN ZPERSON p ON df.{face_schema["person_fk"]} = p.Z_PK
            """
            where_clauses.append("p.ZFULLNAME = ?")
            params.append(person_name)

        # Add album filter if specified
        if album_name:
            # The join table's name and columns are numbered per schema version (Z_27ASSETS, …).
            junction = album_junction(registry)
            if junction is None:
                raise SchemaUnsupportedError(
                    "No album membership table found in this Photos database; Export --album cannot run."
                )
            table, album_col, asset_col = junction
            query += f"""
                JOIN {table} ga ON a.Z_PK = ga.{asset_col}
                JOIN ZGENERICALBUM album ON ga.{album_col} = album.Z_PK
            """
            where_clauses.append("album.ZTITLE = ?")
            params.append(album_name)

        query += " WHERE " + " AND ".join(where_clauses)
        query += " ORDER BY a.ZDATECREATED"

        cursor.execute(query, params)

        # Organize results
        organized = defaultdict(list)
        total_size = 0
        total_count = 0

        for row in cursor.fetchall():
            asset_id = row["Z_PK"]
            filename = row["ZFILENAME"]
            created = coredata_to_local(row["ZDATECREATED"], row["tz_offset"])
            size = row["ZORIGINALFILESIZE"] or 0

            total_size += size
            total_count += 1

            # Determine organization key
            if organize_by == "year_month":
                if created:
                    key = f"{created.year}/{created.strftime('%m-%B')}"
                else:
                    key = "Unknown"

            elif organize_by == "person" and person_name:
                key = person_name

            elif organize_by == "album" and album_name:
                key = album_name

            elif organize_by == "location":
                if row["ZLATITUDE"] and row["ZLONGITUDE"]:
                    # Round to 2 decimal places for grouping
                    lat = round(row["ZLATITUDE"], 2)
                    lon = round(row["ZLONGITUDE"], 2)
                    key = f"loc_{lat}_{lon}"
                else:
                    key = "no_location"

            else:
                key = "all"

            organized[key].append(
                {
                    "id": asset_id,
                    "uuid": row["ZUUID"],
                    "filename": filename,
                    "original_filename": row["original_filename"],
                    "created": created.isoformat() if created else None,
                    "size": size,
                }
            )

        # Convert to serializable format
        plan: dict[str, Any] = {
            "organize_by": organize_by,
            "filters": {
                "favorites_only": favorites_only,
                "start_date": start_date,
                "end_date": end_date,
                "person_name": person_name,
                "album_name": album_name,
            },
            # Filters refuse with exit 5 rather than degrade; only display names can be degraded.
            "degraded": degraded.entries,
            "folders": {},
            "summary": {
                "total_photos": total_count,
                "total_size": total_size,
                "total_size_formatted": format_size(total_size),
                "folder_count": len(organized),
            },
        }

        for folder_name, items in organized.items():
            folder_size = sum(item["size"] for item in items)
            plan["folders"][folder_name] = {
                "count": len(items),
                "size": folder_size,
                "size_formatted": format_size(folder_size),
                "items": items,
            }

        return plan


def export_with_applescript(items: list[dict[str, Any]], output_dir: str, folder_name: str = "") -> tuple[int, int]:
    """
    Use AppleScript to export specific assets from Photos.app.

    Each asset is looked up by its exact Photos identifier (``<UUID>/L0/001``),
    derived from ZASSET.ZUUID. Two guards keep the export bounded to the plan:

    1. **Identity, not filename.** Photos filenames are not unique, so the old
       ``search for`` approach could export an asset the filters had excluded —
       a different photo that merely shared a name with a planned one.
    2. **Filename cross-check.** After resolving an id we confirm the returned
       item's filename matches what the database reported. Any mismatch, or any
       id that fails to resolve, is skipped rather than exported.

    Args:
        items: Assets to export, each needing a "uuid" and "filename"
        output_dir: Base output directory
        folder_name: Subfolder name (if organizing)

    Returns:
        An ``(exported, skipped)`` count pair. ``(0, len(items))`` on failure.

    Raises:
        ValueError: If folder_name escapes output_dir, or an item has no UUID
    """
    # Create output directory, with path traversal protection
    if folder_name:
        safe_folder = sanitize_folder_name(folder_name)
        export_path = os.path.join(output_dir, safe_folder)
    else:
        export_path = output_dir

    # Verify resolved path is inside output_dir
    # (commonpath, not startswith: "/out-evil" starts with "/out" but isn't inside it)
    real_export = os.path.realpath(export_path)
    real_output = os.path.realpath(output_dir)
    if os.path.commonpath([real_export, real_output]) != real_output:
        raise ValueError(f"Path traversal detected in folder name: {folder_name!r}")

    id_list, name_list = build_identifier_lists(items)
    Path(export_path).mkdir(parents=True, exist_ok=True)
    escaped_path = escape_applescript(export_path)

    applescript = f"""
set targetIds to {{{id_list}}}
set targetNames to {{{name_list}}}
set toExport to {{}}
set skippedCount to 0

tell application "Photos"
    repeat with i from 1 to count of targetIds
        try
            set theItem to media item id (item i of targetIds)
            if (filename of theItem) is equal to (item i of targetNames) then
                set end of toExport to theItem
            else
                set skippedCount to skippedCount + 1
            end if
        on error
            -- id did not resolve (already deleted, or not in this library)
            set skippedCount to skippedCount + 1
        end try
    end repeat

    set exportedCount to count of toExport
    if exportedCount > 0 then
        set destFolder to POSIX file "{escaped_path}" as alias
        export toExport to destFolder
    end if
end tell

return "EXPORTED:" & (exportedCount as text) & " SKIPPED:" & (skippedCount as text)
"""

    try:
        result = subprocess.run(
            ["osascript", "-e", applescript],
            capture_output=True,
            text=True,
            timeout=600,
        )
        if result.returncode != 0:
            print(f"  AppleScript error: {result.stderr.strip()}", file=sys.stderr)
            return 0, len(items)

        match = _RESULT_RE.search(result.stdout)
        if not match:
            print(f"  Unexpected AppleScript output: {result.stdout.strip()!r}", file=sys.stderr)
            return 0, len(items)
        return int(match.group(1)), int(match.group(2))
    except subprocess.TimeoutExpired:
        print("  Export timed out (>600 s)", file=sys.stderr)
        return 0, len(items)
    except Exception as e:
        print(f"Error running AppleScript: {e}", file=sys.stderr)
        return 0, len(items)


def export_params(args: argparse.Namespace) -> dict[str, Any]:
    """The arguments that decide what is exported and where (hashed into the token)."""
    return {
        "organize_by": args.organize_by,
        "favorites": args.favorites,
        "start_date": args.start_date,
        "end_date": args.end_date,
        "person": args.person,
        "album": args.album,
        "output_dir": os.path.realpath(args.output_dir),
    }


def export_command(args: argparse.Namespace, token: str) -> str:
    """The exact command line that performs this plan's export."""
    # Interpreter + absolute script path: runnable as-is from any working directory.
    argv = [sys.executable, os.path.abspath(__file__)]
    if args.db_path:
        argv += ["--db-path", args.db_path]
    elif args.library:
        argv += ["--library", args.library]
    argv += ["--output-dir", args.output_dir, "--organize-by", args.organize_by]
    if args.favorites:
        argv.append("--favorites")
    for flag in ("start_date", "end_date", "person", "album"):
        value = getattr(args, flag)
        if value is not None:
            argv += [f"--{flag.replace('_', '-')}", value]
    argv += ["--confirm", token]
    return shlex.join(argv)


def format_plan(plan: dict[str, Any]) -> str:
    """Human-readable export plan, ending with the command that executes it."""
    lines = [
        "📤 EXPORT PLAN",
        "=" * 50,
        f"Organization: {plan['organize_by']}",
        f"Total photos: {plan['summary']['total_photos']:,}",
        f"Total size: {plan['summary']['total_size_formatted']}",
        f"Folders: {plan['summary']['folder_count']}",
        "",
        "Folders:",
    ]
    for folder_name, folder_info in sorted(plan["folders"].items()):
        lines.append(f"  {folder_name}/")
        lines.append(f"    {folder_info['count']:,} items, {folder_info['size_formatted']}")
    lines += [
        "",
        f"Confirmation token: {plan['confirm_token']}",
        "To export exactly this plan, run:",
        f"    {plan['next_command']}",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Smart export of Apple Photos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show export plan for all photos by year/month
  %(prog)s --output-dir ~/Pictures/Export --plan-only

  # Export favorites from 2025 organized by month
  %(prog)s --output-dir ~/Pictures/Export --favorites --start-date 2025-01-01

  # Export photos with a specific person
  %(prog)s --output-dir ~/Pictures/Export --person "Alex" --organize-by person

  # Export specific album
  %(prog)s --output-dir ~/Pictures/Export --album "Vacation 2025" --organize-by album

  # Run the export the plan describes, using the token the plan printed
  %(prog)s --output-dir ~/Pictures/Export --favorites --confirm <token>

Note: Actual export requires Photos.app and proper permissions.
Export writes copies into --output-dir; it never alters the library. Without
--confirm it only prints the plan and its token (exit code 11); --confirm must
match the current plan, or nothing is written.
        """,
    )
    add_common_args(parser, default_format="human")
    parser.add_argument("--output-dir", required=True, help="Output directory for exports")
    parser.add_argument(
        "--organize-by",
        choices=["year_month", "person", "album", "location"],
        default="year_month",
        help="How to organize exports",
    )
    parser.add_argument("--favorites", action="store_true", help="Export only favorites")
    parser.add_argument("--start-date", help="Start date (YYYY-MM-DD, local capture time)")
    parser.add_argument("--end-date", help="End date (YYYY-MM-DD, local capture time, inclusive)")
    parser.add_argument("--person", help="Export only photos with this person")
    parser.add_argument("--album", help="Export only from this album")
    parser.add_argument("--plan-only", action="store_true", help="Show export plan without actually exporting")
    parser.add_argument("--confirm", metavar="TOKEN", help="Confirmation token from the plan; required to export")

    args = parser.parse_args()
    setup_logging(verbose=args.verbose, quiet=args.quiet)
    if args.confirm and args.plan_only:
        parser.error("--confirm and --plan-only are mutually exclusive")

    try:
        db_path = args.db_path or args.library

        plan = generate_export_plan(
            db_path=db_path,
            organize_by=args.organize_by,
            favorites_only=args.favorites,
            start_date=args.start_date,
            end_date=args.end_date,
            person_name=args.person,
            album_name=args.album,
        )
        uuids = [item["uuid"] for folder in plan["folders"].values() for item in folder["items"]]
        token = plan_token("smart_export", export_params(args), uuids)
        plan["confirm_token"] = token
        plan["next_command"] = export_command(args, token)

        if args.plan_only or args.confirm != token:
            if args.format != "human":
                emit_result(plan, args)
            else:
                print(format_plan(plan))
            if args.plan_only:
                return ExitCode.OK
            reason = "is stale: the plan changed since it was shown" if args.confirm else "is missing"
            print(
                f"Not exported: the confirmation token {reason}. Show the user the plan, "
                f"then re-run with --confirm {token}",
                file=sys.stderr,
            )
            return ExitCode.CONFIRMATION_REQUIRED

        # Progress goes to stderr in JSON mode so stdout stays one JSON document.
        # --quiet drops progress lines; the plan (human) or result (json) is still the output.
        progress = io.StringIO() if args.quiet else sys.stderr if args.format != "human" else sys.stdout
        if args.format == "human":
            print(format_plan(plan))
        print(f"Exporting to: {args.output_dir}\n", file=progress)

        total_exported = 0
        total_skipped = 0
        for folder_name, folder_info in plan["folders"].items():
            print(f"Exporting {folder_name}... ", end="", flush=True, file=progress)

            exported, skipped = export_with_applescript(folder_info["items"], args.output_dir, folder_name)
            total_exported += exported
            total_skipped += skipped

            if skipped:
                print(f"✓ {exported:,} exported, {skipped:,} skipped", file=progress)
            else:
                print(f"✓ {exported:,} exported", file=progress)

        # The outcome isn't progress: in human mode it's the result (stdout, even with --quiet),
        # in JSON mode it's in the result object; skipped items are a problem (always stderr).
        if args.format == "human":
            print(f"\nExport complete: {total_exported:,} exported, {total_skipped:,} skipped.")
        if total_skipped:
            print(
                f"{total_skipped:,} item(s) skipped: they could not be resolved in Photos, "
                "or their filename no longer matches.",
                file=sys.stderr,
            )
        if args.format != "human":
            emit_result(
                {
                    "degraded": plan["degraded"],
                    "output_dir": args.output_dir,
                    "exported": total_exported,
                    "skipped": total_skipped,
                    "confirm_token": token,
                },
                args,
            )

        return ExitCode.OK

    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        return ExitCode.USER_ABORTED
    except Exception as e:
        return handle_cli_error(e)


if __name__ == "__main__":
    sys.exit(main())
