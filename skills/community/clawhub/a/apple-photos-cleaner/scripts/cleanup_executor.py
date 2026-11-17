#!/usr/bin/env python3
"""
Cleanup Executor: perform batch cleanup operations via AppleScript.
Supports moving junk photos to trash. Execution needs the confirmation token
printed by the preview (see _common.plan_token), so what runs is exactly what
the user was shown.
All actions go through Photos.app for safety — nothing touches the database directly.

Items are targeted by their stable asset UUID (ZASSET.ZUUID), never by filename.
Photos filenames are not unique — the same IMG_0042.HEIC can appear many times
across devices and re-imports — so filename matching risks trashing the wrong
photo. See generate_trash_applescript for the matching rules.
"""

import argparse
import os
import re
import shlex
import subprocess
import sys
from typing import Any

from _common import (
    LOCAL_IDENTIFIER_SUFFIX,
    SCREEN_RECORDING_SQL,
    SCREENSHOT_SQL,
    ExitCode,
    PhotosDB,
    add_common_args,
    build_identifier_lists,
    coredata_to_local,
    display_name,
    emit_result,
    format_size,
    handle_cli_error,
    has_timezone_offset,
    original_filename_sql,
    plan_token,
    positive_int,
    require_uuid_support,
    setup_logging,
    tz_offset_sql,
)
from _schema import BURSTS, FILE_SIZE, ORIGINAL_FILENAME, QUALITY_SCORES, Degradation, get_schema

# Schema contract (T1.4): see _schema. Missing required → exit 5; missing optional → `degraded`.
REQUIRED_COLUMNS: tuple[str, ...] = (
    "ZASSET.ZDATECREATED",
    "ZASSET.ZFILENAME",
    "ZASSET.ZTRASHEDSTATE",
    "asset.uuid",
    *FILE_SIZE,
)
# A mutating command never acts on partial data: a category whose columns are missing
# refuses (exit 5) instead of degrading.
CATEGORY_COLUMNS: dict[str, tuple[str, ...]] = {
    "old_screenshots": ("ZASSET.ZISDETECTEDSCREENSHOT", "ZASSET.ZKIND"),
    "all_screenshots": ("ZASSET.ZISDETECTEDSCREENSHOT", "ZASSET.ZKIND"),
    "screen_recordings": ("ZASSET.ZISDETECTEDSCREENSHOT", "ZASSET.ZKIND"),
    "burst_leftovers": BURSTS,
    "low_quality": ("ZASSET.ZKIND", "ZASSET.ZISDETECTEDSCREENSHOT", *QUALITY_SCORES),
    "duplicates": ("ZASSET.ZDUPLICATEASSETVISIBILITYSTATE", "ZASSET.ZFAVORITE"),
}
OPTIONAL_COLUMNS: dict[str, tuple[str, ...]] = {"original_filenames": ORIGINAL_FILENAME}

# Maximum items per AppleScript batch (Photos.app can be slow with large batches)
MAX_BATCH_SIZE = 50

# Counters reported back by the generated AppleScript.
_RESULT_RE = re.compile(r"DELETED:(\d+)\s+SKIPPED:(\d+)")

# Re-exported for callers and tests that import it from this module.
__all__ = ["LOCAL_IDENTIFIER_SUFFIX", "generate_trash_applescript", "require_uuid_support"]


def get_cleanup_candidates(
    db_path: str | None = None,
    category: str = "old_screenshots",
    screenshot_age_days: int = 30,
    quality_threshold: float = 0.3,
    limit: int = 500,
) -> dict[str, Any]:
    """
    Get cleanup candidates for a specific category.

    Args:
        db_path: Path to database
        category: Type of cleanup ('old_screenshots', 'burst_leftovers',
                  'low_quality', 'duplicates', 'all_screenshots')
        screenshot_age_days: Age threshold for old screenshots
        quality_threshold: Quality score threshold for low quality
        limit: Maximum candidates to return

    Returns:
        Cleanup candidates dictionary
    """
    with PhotosDB(db_path, require=REQUIRED_COLUMNS, operation="Cleanup") as conn:
        name_col = original_filename_sql(get_schema(conn))
        degraded = Degradation(get_schema(conn))
        degraded.check("original_filenames", *OPTIONAL_COLUMNS["original_filenames"])
        cursor = conn.cursor()
        tz_available = has_timezone_offset(cursor)
        require_uuid_support(cursor, "Cleanup")
        schema = get_schema(conn)
        schema.require(*CATEGORY_COLUMNS[category], operation=f"Cleanup category {category!r}")

        candidates = []

        if category in ("old_screenshots", "all_screenshots", "screen_recordings"):
            from datetime import datetime, timedelta

            from _common import datetime_to_coredata

            # Screenshots are photos only; screen recordings carry the same flag but are videos.
            kind = SCREEN_RECORDING_SQL if category == "screen_recordings" else SCREENSHOT_SQL
            where = f"a.ZTRASHEDSTATE != 1 AND {kind}"
            params: list[Any] = []

            if category == "old_screenshots":
                cutoff = datetime.now() - timedelta(days=screenshot_age_days)
                cutoff_ts = datetime_to_coredata(cutoff)
                where += " AND a.ZDATECREATED < ?"
                params.append(cutoff_ts)

            params.append(limit)
            cursor.execute(
                f"""
                SELECT
                    a.Z_PK, a.ZUUID, a.ZFILENAME, {name_col}, a.ZDATECREATED,
                    aa.ZORIGINALFILESIZE,
                    {tz_offset_sql(tz_available)} AS tz_offset
                FROM ZASSET a
                LEFT JOIN ZADDITIONALASSETATTRIBUTES aa ON a.Z_PK = aa.ZASSET
                WHERE {where}
                ORDER BY a.ZDATECREATED
                LIMIT ?
            """,
                params,
            )

            for row in cursor.fetchall():
                created = coredata_to_local(row["ZDATECREATED"], row["tz_offset"])
                candidates.append(
                    {
                        "id": row["Z_PK"],
                        "uuid": row["ZUUID"],
                        "filename": row["ZFILENAME"],
                        "original_filename": row["original_filename"],
                        "created": created.isoformat() if created else None,
                        "size": row["ZORIGINALFILESIZE"] or 0,
                        "size_formatted": format_size(row["ZORIGINALFILESIZE"] or 0),
                        "category": category,
                    }
                )

        elif category == "burst_leftovers":
            cursor.execute(
                f"""
                SELECT
                    a.Z_PK, a.ZUUID, a.ZFILENAME, {name_col}, a.ZDATECREATED,
                    aa.ZORIGINALFILESIZE,
                    {tz_offset_sql(tz_available)} AS tz_offset
                FROM ZASSET a
                LEFT JOIN ZADDITIONALASSETATTRIBUTES aa ON a.Z_PK = aa.ZASSET
                WHERE a.ZTRASHEDSTATE != 1
                AND a.ZAVALANCHEKIND > 0
                AND (a.ZAVALANCHEPICKTYPE IS NULL OR a.ZAVALANCHEPICKTYPE = 0)
                ORDER BY a.ZDATECREATED
                LIMIT ?
            """,
                (limit,),
            )

            for row in cursor.fetchall():
                created = coredata_to_local(row["ZDATECREATED"], row["tz_offset"])
                candidates.append(
                    {
                        "id": row["Z_PK"],
                        "uuid": row["ZUUID"],
                        "filename": row["ZFILENAME"],
                        "original_filename": row["original_filename"],
                        "created": created.isoformat() if created else None,
                        "size": row["ZORIGINALFILESIZE"] or 0,
                        "size_formatted": format_size(row["ZORIGINALFILESIZE"] or 0),
                        "category": "burst_leftovers",
                    }
                )

        elif category == "low_quality":
            from _common import build_asset_query, get_quality_score

            query = build_asset_query(
                where_clauses=[
                    "a.ZTRASHEDSTATE != 1",
                    "a.ZKIND = 0",
                    "a.ZISDETECTEDSCREENSHOT != 1",
                ],
                join_additional=True,
                tz_offset_available=tz_available,
                join_computed=True,
                order_by="ZFAILURESCORE DESC",
                schema=schema,
                limit=limit * 3,  # fetch more since we filter by quality
            )
            cursor.execute(query)

            for row in cursor.fetchall():
                quality = get_quality_score(row)
                if quality is not None and quality < quality_threshold:
                    created = coredata_to_local(row["ZDATECREATED"], row["tz_offset"])
                    candidates.append(
                        {
                            "id": row["Z_PK"],
                            "uuid": row["ZUUID"],
                            "filename": row["ZFILENAME"],
                            "original_filename": row["original_filename"],
                            "created": created.isoformat() if created else None,
                            "size": row["ZORIGINALFILESIZE"] or 0,
                            "size_formatted": format_size(row["ZORIGINALFILESIZE"] or 0),
                            "quality_score": round(quality, 3),
                            "category": "low_quality",
                        }
                    )
                    if len(candidates) >= limit:
                        break

        elif category == "duplicates":
            cursor.execute(
                f"""
                SELECT
                    a.Z_PK, a.ZUUID, a.ZFILENAME, {name_col}, a.ZDATECREATED,
                    a.ZFAVORITE,
                    aa.ZORIGINALFILESIZE,
                    {tz_offset_sql(tz_available)} AS tz_offset,
                    a.ZDUPLICATEASSETVISIBILITYSTATE
                FROM ZASSET a
                LEFT JOIN ZADDITIONALASSETATTRIBUTES aa ON a.Z_PK = aa.ZASSET
                WHERE a.ZTRASHEDSTATE != 1
                AND a.ZDUPLICATEASSETVISIBILITYSTATE > 0
                AND a.ZFAVORITE != 1
                ORDER BY a.ZDATECREATED
                LIMIT ?
            """,
                (limit,),
            )

            for row in cursor.fetchall():
                created = coredata_to_local(row["ZDATECREATED"], row["tz_offset"])
                candidates.append(
                    {
                        "id": row["Z_PK"],
                        "uuid": row["ZUUID"],
                        "filename": row["ZFILENAME"],
                        "original_filename": row["original_filename"],
                        "created": created.isoformat() if created else None,
                        "size": row["ZORIGINALFILESIZE"] or 0,
                        "size_formatted": format_size(row["ZORIGINALFILESIZE"] or 0),
                        "category": "duplicates",
                    }
                )

        total_size = sum(c["size"] for c in candidates)

        return {
            # Categories refuse with exit 5 rather than degrade; only display names can be degraded.
            "degraded": degraded.entries,
            "candidates": candidates,
            "summary": {
                "category": category,
                "count": len(candidates),
                "total_size": total_size,
                "total_size_formatted": format_size(total_size),
            },
        }


def generate_trash_applescript(candidates: list[dict[str, Any]]) -> str:
    """
    Generate AppleScript to move specific assets to trash.

    Each asset is looked up by its exact Photos identifier (``<UUID>/L0/001``),
    derived from ZASSET.ZUUID. Two guards make this safe:

    1. **Identity, not filename.** Photos filenames are not unique, so the old
       filename-matching approach could trash an unrelated photo that happened
       to share a name with a cleanup candidate.
    2. **Filename cross-check.** After resolving an id we confirm the returned
       item's filename matches what the database reported. Any mismatch, or any
       id that fails to resolve, is skipped rather than deleted.

    The script reports ``DELETED:<n> SKIPPED:<n>`` so the caller can record what
    actually happened instead of assuming the whole batch succeeded.

    Args:
        candidates: Cleanup candidates, each needing a "uuid" and "filename"

    Returns:
        AppleScript string

    Raises:
        ValueError: If any candidate is missing a UUID
    """
    id_list, name_list = build_identifier_lists(candidates)

    script = f"""
set targetIds to {{{id_list}}}
set targetNames to {{{name_list}}}
set itemsToDelete to {{}}
set skippedCount to 0

tell application "Photos"
    repeat with i from 1 to count of targetIds
        try
            set theItem to media item id (item i of targetIds)
            if (filename of theItem) is equal to (item i of targetNames) then
                set end of itemsToDelete to theItem
            else
                set skippedCount to skippedCount + 1
            end if
        on error
            -- id did not resolve (already deleted, or not in this library)
            set skippedCount to skippedCount + 1
        end try
    end repeat

    set deletedCount to count of itemsToDelete
    if deletedCount > 0 then
        delete itemsToDelete
    end if
end tell

return "DELETED:" & (deletedCount as text) & " SKIPPED:" & (skippedCount as text)
"""
    return script


def execute_cleanup(
    candidates: list[dict[str, Any]],
    dry_run: bool = True,
    batch_size: int = MAX_BATCH_SIZE,
) -> dict[str, Any]:
    """
    Execute cleanup by moving candidates to trash via AppleScript.

    Args:
        candidates: List of cleanup candidates
        dry_run: If True, show what would happen without doing it
        batch_size: Number of items per AppleScript batch

    Returns:
        Execution results
    """
    total = len(candidates)
    total_size = sum(c["size"] for c in candidates)
    results: dict[str, Any] = {
        "dry_run": dry_run,
        "total_candidates": total,
        "total_size": total_size,
        "total_size_formatted": format_size(total_size),
        "batches": [],
        "errors": [],
        "success_count": 0,
        "skipped_count": 0,
    }

    if dry_run:
        results["message"] = (
            f"DRY RUN: Would move {total} items ({format_size(total_size)}) to Recently Deleted. "
            f"Run with --execute to proceed."
        )
        return results

    # Process in batches
    for i in range(0, total, batch_size):
        batch = candidates[i : i + batch_size]
        batch_num = i // batch_size + 1

        try:
            script = generate_trash_applescript(batch)
        except ValueError as e:
            results["batches"].append({"batch": batch_num, "count": len(batch), "status": "error", "error": str(e)})
            results["errors"].append(str(e))
            continue

        try:
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                text=True,
                timeout=120,
            )

            if result.returncode == 0:
                output = result.stdout.strip()
                match = _RESULT_RE.search(output)
                if match:
                    deleted, skipped = int(match.group(1)), int(match.group(2))
                else:
                    # Unparseable output: assume nothing was deleted rather than
                    # over-reporting success.
                    deleted, skipped = 0, len(batch)

                results["batches"].append(
                    {
                        "batch": batch_num,
                        "count": len(batch),
                        "status": "success",
                        "deleted": deleted,
                        "skipped": skipped,
                        "output": output,
                    }
                )
                results["success_count"] += deleted
                results["skipped_count"] += skipped
            else:
                results["batches"].append(
                    {
                        "batch": batch_num,
                        "count": len(batch),
                        "status": "error",
                        "error": result.stderr.strip(),
                    }
                )
                results["errors"].append(result.stderr.strip())

        except subprocess.TimeoutExpired:
            results["errors"].append(f"Batch {batch_num} timed out")
        except Exception as e:
            results["errors"].append(f"Batch {batch_num}: {e!s}")

    message = f"Moved {results['success_count']}/{total} items to Recently Deleted."
    if results["skipped_count"]:
        message += (
            f" Skipped {results['skipped_count']} (asset not found in Photos, or its "
            f"filename no longer matched the database)."
        )
    message += " Check Recently Deleted in Photos.app to confirm or recover."
    results["message"] = message
    return results


def format_summary(data: dict[str, Any]) -> str:
    """Format cleanup candidates/results as human-readable summary."""
    lines = []
    lines.append("🧹 CLEANUP EXECUTOR")
    lines.append("=" * 50)
    lines.append("")

    if "candidates" in data:
        s = data["summary"]
        lines.append(f"Category: {s['category']}")
        lines.append(f"Candidates: {s['count']:,}")
        lines.append(f"Total size: {s['total_size_formatted']}")
        lines.append("")

        lines.append("Items to clean up:")
        for c in data["candidates"][:20]:
            lines.append(f"  {display_name(c)} ({c['size_formatted']})")
            if c.get("quality_score") is not None:
                lines.append(f"    Quality: {c['quality_score']:.3f}")

        if len(data["candidates"]) > 20:
            lines.append(f"  ... and {len(data['candidates']) - 20} more")
        lines.append("")
        if "confirm_token" in data:
            lines.append(f"Confirmation token: {data['confirm_token']}")
            lines.append("⚠️  To execute exactly these items, run:")
            lines.append(f"    {data['next_command']}")
        lines.append("    Items will be moved to Recently Deleted (recoverable for 30 days)")

    elif "message" in data:
        lines.append(data["message"])
        if data.get("errors"):
            lines.append("")
            lines.append("Errors:")
            for err in data["errors"]:
                lines.append(f"  ⚠️  {err}")

    lines.append("")
    return "\n".join(lines)


def selection_params(args: argparse.Namespace) -> dict[str, Any]:
    """The arguments that decide which assets are candidates (hashed into the token)."""
    return {
        "category": args.category,
        "screenshot_age": args.screenshot_age,
        "quality_threshold": args.quality_threshold,
        "limit": args.limit,
    }


def execute_command(args: argparse.Namespace, token: str) -> str:
    """The exact command line that executes this preview."""
    # Interpreter + absolute script path: runnable as-is from any working directory.
    argv = [sys.executable, os.path.abspath(__file__)]
    if args.db_path:
        argv += ["--db-path", args.db_path]
    elif args.library:
        argv += ["--library", args.library]
    for flag, value in selection_params(args).items():
        argv += [f"--{flag.replace('_', '-')}", str(value)]
    argv += ["--execute", "--confirm", token]
    return shlex.join(argv)


def emit_preview(data: dict[str, Any], args: argparse.Namespace) -> None:
    if args.format == "human":
        print(format_summary(data))
        return
    emit_result(data, args)
    if not args.output and not args.quiet:
        print("\n" + format_summary(data), file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Execute cleanup operations via AppleScript",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview old screenshots to clean up
  %(prog)s --category old_screenshots --human

  # Preview burst leftovers
  %(prog)s --category burst_leftovers --human

  # Move exactly the previewed screenshots to trash, using the token the preview printed
  %(prog)s --category old_screenshots --execute --confirm <token>

Categories:
  old_screenshots   - Screenshots older than --screenshot-age days (photos only)
  all_screenshots   - All screenshots (photos only)
  burst_leftovers   - Unpicked burst photos
  low_quality       - Photos below --quality-threshold
  duplicates        - Apple-detected duplicates (non-favorites only)
  screen_recordings - Screen recordings (videos Photos flags like screenshots)

⚠️  SAFETY: --execute requires --confirm with the token from the preview. If the
    candidates changed since the preview, nothing runs and a fresh token is
    printed (exit code 11). Items are moved to Recently Deleted, not permanently
    deleted; you have 30 days to recover them in Photos.app.
        """,
    )
    add_common_args(parser)
    parser.add_argument(
        "--category",
        required=True,
        choices=[
            "old_screenshots",
            "all_screenshots",
            "screen_recordings",
            "burst_leftovers",
            "low_quality",
            "duplicates",
        ],
        help="Category of items to clean up",
    )
    parser.add_argument("--screenshot-age", type=int, default=30, help="Screenshot age in days (default: 30)")
    parser.add_argument(
        "--quality-threshold", type=float, default=0.3, help="Quality threshold for low_quality category (default: 0.3)"
    )
    parser.add_argument("--limit", type=positive_int, default=500, help="Maximum items to process (default: 500)")
    parser.add_argument(
        "--execute", action="store_true", help="Actually perform the cleanup (moves to Recently Deleted)"
    )
    parser.add_argument(
        "--confirm", metavar="TOKEN", help="Confirmation token from the preview (required with --execute)"
    )
    parser.add_argument(
        "--batch-size",
        type=positive_int,
        default=MAX_BATCH_SIZE,
        help=f"Items per AppleScript batch (default: {MAX_BATCH_SIZE})",
    )

    args = parser.parse_args()
    setup_logging(verbose=args.verbose, quiet=args.quiet)
    if args.confirm and not args.execute:
        parser.error("--confirm only applies together with --execute")

    try:
        db_path = args.db_path or args.library

        # Get candidates
        data = get_cleanup_candidates(
            db_path=db_path,
            category=args.category,
            screenshot_age_days=args.screenshot_age,
            quality_threshold=args.quality_threshold,
            limit=args.limit,
        )

        token = plan_token("cleanup_executor", selection_params(args), [c["uuid"] for c in data["candidates"]])
        data["confirm_token"] = token
        data["next_command"] = execute_command(args, token)

        if not data["candidates"]:
            message = f"No cleanup candidates found for category: {args.category}"
            if args.format == "human":
                print(message)  # the result itself, so --quiet doesn't drop it
            else:
                emit_result(data, args)
                if not args.quiet:
                    print(message, file=sys.stderr)
            return ExitCode.OK

        if args.execute and args.confirm != token:
            emit_preview(data, args)
            reason = "is stale: the candidates changed since the preview" if args.confirm else "is missing"
            print(
                f"\nNot executed: the confirmation token {reason}. Show the user the preview above, "
                f"then re-run with --confirm {token}",
                file=sys.stderr,
            )
            return ExitCode.CONFIRMATION_REQUIRED

        if not args.execute:
            emit_preview(data, args)
            return ExitCode.OK

        result = execute_cleanup(
            candidates=data["candidates"],
            dry_run=False,
            batch_size=args.batch_size,
        )
        result["degraded"] = data["degraded"]
        result["confirm_token"] = token
        if args.format == "human":
            print(format_summary(result))
        else:
            emit_result(result, args)

        return 0

    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        return ExitCode.USER_ABORTED
    except Exception as e:
        return handle_cli_error(e)


if __name__ == "__main__":
    sys.exit(main())
