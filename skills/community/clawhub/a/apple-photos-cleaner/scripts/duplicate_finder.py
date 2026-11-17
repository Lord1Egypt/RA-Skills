#!/usr/bin/env python3
"""
Find duplicate photos and suggest which to keep based on quality scores.
"""

import sys
from collections import defaultdict
from typing import Any

from _common import (
    QUALITY_SCORE_COLUMNS,
    PhotosDB,
    computed_scores_sql,
    coredata_to_local,
    display_name,
    format_size,
    get_quality_score,
    has_timezone_offset,
    is_favorite,
    is_screenshot,
    original_filename_sql,
    run_script,
    tz_offset_sql,
)
from _schema import FILE_SIZE, ORIGINAL_FILENAME, QUALITY_SCORES, Degradation, get_schema

# Schema contract (T1.4): see _schema. Missing required → exit 5; missing optional → `degraded`.
REQUIRED_COLUMNS: tuple[str, ...] = (
    "ZASSET.ZDATECREATED",
    "ZASSET.ZFAVORITE",
    "ZASSET.ZFILENAME",
    "ZASSET.ZHEIGHT",
    "ZASSET.ZISDETECTEDSCREENSHOT",
    "ZASSET.ZKIND",
    "ZASSET.ZTRASHEDSTATE",
    "ZASSET.ZWIDTH",
    *FILE_SIZE,
)
OPTIONAL_COLUMNS: dict[str, tuple[str, ...]] = {
    "original_filenames": ORIGINAL_FILENAME,
    # Apple's own duplicate detection (macOS 13+); without it only timestamp+dimension matching runs.
    "apple_duplicates": ("ZASSET.ZDUPLICATEASSETVISIBILITYSTATE",),
    # Quality only influences which copy is recommended to keep.
    "keep_quality": QUALITY_SCORES,
}


def find_duplicates(db_path: str | None = None) -> dict[str, Any]:
    """
    Find duplicate photos using multiple detection methods.

    Returns:
        Dictionary with duplicate groups and recommendations
    """
    with PhotosDB(db_path, require=REQUIRED_COLUMNS, operation="Duplicate detection") as conn:
        name_col = original_filename_sql(get_schema(conn))
        cursor = conn.cursor()
        tz_available = has_timezone_offset(cursor)
        schema = get_schema(conn)
        degraded = Degradation(schema)
        degraded.check("original_filenames", *OPTIONAL_COLUMNS["original_filenames"])
        has_apple_duplicates = degraded.check("apple_duplicates", *OPTIONAL_COLUMNS["apple_duplicates"])
        degraded.check("keep_quality", *OPTIONAL_COLUMNS["keep_quality"])
        score_terms, score_join = computed_scores_sql(schema, *QUALITY_SCORE_COLUMNS)
        scores = ",\n                ".join(score_terms)

        duplicate_groups = []

        # Method 1: Apple's built-in duplicate detection
        apple_rows = (
            cursor.execute(f"""
            SELECT
                a.Z_PK,
                a.ZFILENAME,
                {name_col},
                a.ZDATECREATED,
                a.ZWIDTH,
                a.ZHEIGHT,
                a.ZFAVORITE,
                a.ZISDETECTEDSCREENSHOT,
                a.ZDUPLICATEASSETVISIBILITYSTATE,
                aa.ZORIGINALFILESIZE,
                {tz_offset_sql(tz_available)} AS tz_offset,
                {scores}
            FROM ZASSET a
            LEFT JOIN ZADDITIONALASSETATTRIBUTES aa ON a.Z_PK = aa.ZASSET
            {score_join}
            WHERE a.ZTRASHEDSTATE != 1
            AND a.ZDUPLICATEASSETVISIBILITYSTATE > 0
            ORDER BY a.ZDATECREATED
        """)
            if has_apple_duplicates
            else []
        )

        apple_duplicates: dict[Any, list[dict[str, Any]]] = {}
        for row in apple_rows:
            state = row["ZDUPLICATEASSETVISIBILITYSTATE"]
            if state not in apple_duplicates:
                apple_duplicates[state] = []
            apple_duplicates[state].append(row)

        # Create groups from Apple's detection
        for _state, items in apple_duplicates.items():
            if len(items) > 1:
                group = create_duplicate_group(items, "apple_builtin")
                duplicate_groups.append(group)

        # Method 2: Same timestamp + same dimensions
        not_caught_by_apple = "AND a.ZDUPLICATEASSETVISIBILITYSTATE = 0" if has_apple_duplicates else ""
        cursor.execute(f"""
            SELECT
                a.Z_PK,
                a.ZFILENAME,
                {name_col},
                a.ZDATECREATED,
                a.ZWIDTH,
                a.ZHEIGHT,
                a.ZFAVORITE,
                a.ZISDETECTEDSCREENSHOT,
                aa.ZORIGINALFILESIZE,
                {tz_offset_sql(tz_available)} AS tz_offset,
                {scores}
            FROM ZASSET a
            LEFT JOIN ZADDITIONALASSETATTRIBUTES aa ON a.Z_PK = aa.ZASSET
            {score_join}
            WHERE a.ZTRASHEDSTATE != 1
            AND a.ZKIND = 0  -- photos only
            {not_caught_by_apple}
            ORDER BY a.ZDATECREATED, a.ZWIDTH, a.ZHEIGHT
        """)

        # Group by (timestamp_rounded, width, height)
        timestamp_groups = defaultdict(list)
        for row in cursor:
            # Round timestamp to nearest second
            timestamp = int(row["ZDATECREATED"]) if row["ZDATECREATED"] else 0
            key = (timestamp, row["ZWIDTH"], row["ZHEIGHT"])
            timestamp_groups[key].append(row)

        # Add groups with multiple items
        for _key, items in timestamp_groups.items():
            if len(items) > 1:
                group = create_duplicate_group(items, "timestamp_dimensions")
                duplicate_groups.append(group)

        # Calculate totals
        total_duplicates = sum(len(g["items"]) for g in duplicate_groups)
        total_can_delete = sum(len(g["items"]) - 1 for g in duplicate_groups)

        total_size = sum(sum(item["size"] for item in g["items"]) for g in duplicate_groups)

        potential_savings = sum(
            sum(item["size"] for item in g["items"] if not item["recommended_keep"]) for g in duplicate_groups
        )

        return {
            "degraded": degraded.entries,
            "duplicate_groups": duplicate_groups,
            "summary": {
                "total_groups": len(duplicate_groups),
                "total_duplicates": total_duplicates,
                "can_delete": total_can_delete,
                "total_size": total_size,
                "total_size_formatted": format_size(total_size),
                "potential_savings": potential_savings,
                "potential_savings_formatted": format_size(potential_savings),
            },
        }


def create_duplicate_group(items: list[Any], detection_method: str) -> dict[str, Any]:
    """
    Create a duplicate group with recommendation on which to keep.

    Args:
        items: List of duplicate items (sqlite rows)
        detection_method: How duplicates were detected

    Returns:
        Duplicate group dict
    """
    processed_items = []

    for item in items:
        created = coredata_to_local(item["ZDATECREATED"], item["tz_offset"])
        quality = get_quality_score(item)

        processed_items.append(
            {
                "id": item["Z_PK"],
                "filename": item["ZFILENAME"],
                "original_filename": dict(item).get("original_filename"),
                "created": created.isoformat() if created else None,
                "size": item["ZORIGINALFILESIZE"] or 0,
                "size_formatted": format_size(item["ZORIGINALFILESIZE"] or 0),
                "width": item["ZWIDTH"],
                "height": item["ZHEIGHT"],
                "is_favorite": is_favorite(item),
                "is_screenshot": is_screenshot(item),
                "quality_score": round(quality, 3) if quality is not None else None,
            }
        )

    # Decide which to keep
    # Priority: favorite > highest quality > largest file
    best_item_idx = 0
    best_score = -1

    for idx, item in enumerate(processed_items):
        score = 0

        # Favorite gets huge boost
        if item["is_favorite"]:
            score += 1000

        # Screenshot gets penalty
        if item["is_screenshot"]:
            score -= 100

        # Quality score
        if item["quality_score"] is not None:
            score += item["quality_score"] * 100

        # File size (normalized)
        score += item["size"] / 1000000  # MB

        if score > best_score:
            best_score = score
            best_item_idx = idx

    # Mark recommended keep
    for idx, item in enumerate(processed_items):
        item["recommended_keep"] = idx == best_item_idx

    return {
        "detection_method": detection_method,
        "items": processed_items,
        "recommended_keep_id": processed_items[best_item_idx]["id"],
    }


def format_summary(duplicates: dict[str, Any]) -> str:
    """Format duplicate findings as human-readable summary."""
    lines = []
    lines.append("👥 DUPLICATE FINDER RESULTS")
    lines.append("=" * 50)
    lines.append("")

    summary = duplicates["summary"]

    lines.append(f"Found {summary['total_groups']} duplicate groups")
    lines.append(f"Total duplicates: {summary['total_duplicates']}")
    lines.append(f"Can safely delete: {summary['can_delete']}")
    lines.append(f"Total size: {summary['total_size_formatted']}")
    lines.append(f"Potential savings: {summary['potential_savings_formatted']}")
    lines.append("")

    if duplicates["duplicate_groups"]:
        lines.append("Sample groups (showing first 5):")
        for i, group in enumerate(duplicates["duplicate_groups"][:5], 1):
            lines.append(f"\nGroup {i} ({group['detection_method']}):")
            for item in group["items"]:
                keep_marker = "✓ KEEP" if item["recommended_keep"] else "  DELETE"
                quality_str = f"Q:{item['quality_score']}" if item["quality_score"] else "Q:N/A"
                fav_str = "★" if item["is_favorite"] else " "
                lines.append(
                    f"  {keep_marker} {fav_str} {display_name(item)} ({item['size_formatted']}, {quality_str})"
                )

    return "\n".join(lines)


def main():
    return run_script(
        description="Find duplicate photos in Apple Photos library",
        analyze_fn=lambda db_path, _args: find_duplicates(db_path),
        format_fn=format_summary,
        epilog="""
Examples:
  %(prog)s
  %(prog)s --output duplicates.json
  %(prog)s --human
        """,
    )


if __name__ == "__main__":
    sys.exit(main())
