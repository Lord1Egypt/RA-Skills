#!/usr/bin/env python3
"""
On This Day / Memory Lane: see what you photographed on today's date in prior years.
A richer version of Apple's Memories with people, scenes, and quality context.
"""

import sys
from collections import defaultdict
from datetime import date, datetime
from typing import Any

from _common import (
    QUALITY_SCORE_COLUMNS,
    PhotosDB,
    computed_scores_sql,
    coredata_to_local,
    detect_face_schema,
    display_name,
    format_size,
    get_quality_score,
    has_timezone_offset,
    is_screenshot,
    local_datetime_sql,
    original_filename_sql,
    run_script,
    tz_offset_sql,
)
from _scenes import SEARCH_INDEX, IndexLabels, scene_source, search_index_available
from _schema import FACES, FILE_SIZE, ORIGINAL_FILENAME, QUALITY_SCORES, SCENES, Degradation, get_schema

# Schema contract (T1.4): see _schema. Missing required → exit 5; missing optional → `degraded`.
REQUIRED_COLUMNS: tuple[str, ...] = (
    "ZASSET.ZDATECREATED",
    "ZASSET.ZFAVORITE",
    "ZASSET.ZFILENAME",
    "ZASSET.ZISDETECTEDSCREENSHOT",
    "ZASSET.ZKIND",
    "ZASSET.ZLATITUDE",
    "ZASSET.ZLONGITUDE",
    "ZASSET.ZTRASHEDSTATE",
    *FILE_SIZE,
)
OPTIONAL_COLUMNS: dict[str, tuple[str, ...]] = {
    "original_filenames": ORIGINAL_FILENAME,
    "quality": QUALITY_SCORES,
    "people": FACES,
    "scenes": SCENES,
}
# A section whose columns are missing is still available when this source exists (doctor uses it).
ALTERNATE_SOURCES = {"scenes": search_index_available}


def on_this_day(
    db_path: str | None = None,
    target_date: str | None = None,
    window_days: int = 0,
) -> dict[str, Any]:
    """
    Find photos taken on this date in previous years.

    Args:
        db_path: Path to database
        target_date: Date to look up (YYYY-MM-DD), defaults to today
        window_days: Include photos +/- this many days around the target date

    Returns:
        On-this-day results dictionary
    """
    if target_date:
        target = date.fromisoformat(target_date)
    else:
        target = date.today()

    month = target.month
    day = target.day

    with PhotosDB(db_path, require=REQUIRED_COLUMNS, operation="On This Day") as conn:
        name_col = original_filename_sql(get_schema(conn))
        cursor = conn.cursor()
        schema = detect_face_schema(cursor)
        registry = get_schema(conn)
        degraded = Degradation(registry)
        degraded.check("original_filenames", *OPTIONAL_COLUMNS["original_filenames"])
        degraded.check("quality", *OPTIONAL_COLUMNS["quality"])
        has_faces = degraded.check("people", *OPTIONAL_COLUMNS["people"])
        # Scene names come from ZSCENECLASSIFICATION or, on macOS 26, Photos' search index (see _scenes).
        scenes_from = scene_source(conn)
        index_labels = IndexLabels(conn)  # filled in bulk below, only if the index is the source
        has_scenes = scenes_from is not None
        if scenes_from is None:
            degraded.check("scenes", *OPTIONAL_COLUMNS["scenes"])
        score_terms, score_join = computed_scores_sql(registry, *QUALITY_SCORE_COLUMNS)
        tz_available = has_timezone_offset(cursor)
        local_dt = local_datetime_sql(tz_available)

        # Build date matching condition
        if window_days > 0:
            # Match a range of month-day combinations
            date_conditions = []
            for offset in range(-window_days, window_days + 1):
                d = date(2000, month, day)  # Use a leap year as base
                try:
                    from datetime import timedelta

                    d = d + timedelta(days=offset)
                    date_conditions.append(
                        f"(CAST(strftime('%m', {local_dt}) AS INTEGER) = {d.month} "
                        f"AND CAST(strftime('%d', {local_dt}) AS INTEGER) = {d.day})"
                    )
                except ValueError:
                    continue
            date_filter = "(" + " OR ".join(date_conditions) + ")"
        else:
            date_filter = (
                f"CAST(strftime('%m', {local_dt}) AS INTEGER) = {month} "
                f"AND CAST(strftime('%d', {local_dt}) AS INTEGER) = {day}"
            )

        # Exclude current year's photos (we want memories, not today's photos)
        current_year = datetime.now().year

        query = f"""
            SELECT
                a.Z_PK,
                a.ZFILENAME,
                {name_col},
                a.ZDATECREATED,
                a.ZKIND,
                a.ZFAVORITE,
                a.ZLATITUDE,
                a.ZLONGITUDE,
                a.ZISDETECTEDSCREENSHOT,
                aa.ZORIGINALFILESIZE,
                {", ".join(score_terms)},
                {tz_offset_sql(tz_available)} AS tz_offset
            FROM ZASSET a
            LEFT JOIN ZADDITIONALASSETATTRIBUTES aa ON a.Z_PK = aa.ZASSET
            {score_join}
            WHERE a.ZTRASHEDSTATE != 1
            AND {date_filter}
            AND strftime('%Y', {local_dt}) != ?
            ORDER BY a.ZDATECREATED DESC
        """

        cursor.execute(query, (str(current_year),))

        # Group by year
        by_year = defaultdict(list)
        total_photos = 0

        for row in cursor.fetchall():
            created = coredata_to_local(row["ZDATECREATED"], row["tz_offset"])
            if not created:
                continue

            quality = get_quality_score(row)
            year_str = str(created.year)
            years_ago = current_year - created.year
            size = row["ZORIGINALFILESIZE"] or 0

            photo = {
                "id": row["Z_PK"],
                "filename": row["ZFILENAME"],
                "original_filename": row["original_filename"],
                "created": created.isoformat(),
                "year": created.year,
                "years_ago": years_ago,
                "kind": "photo" if row["ZKIND"] == 0 else "video",
                "is_favorite": bool(row["ZFAVORITE"]),
                "is_screenshot": is_screenshot(row),
                "quality_score": round(quality, 3) if quality else None,
                "size": size,
                "size_formatted": format_size(size),
                "latitude": row["ZLATITUDE"],
                "longitude": row["ZLONGITUDE"],
            }

            by_year[year_str].append(photo)
            total_photos += 1

        # Enrich each year group with people and scenes
        year_summaries = []
        if scenes_from == SEARCH_INDEX:  # one batch for every photo across the years shown
            index_labels.preload(p["id"] for photos in by_year.values() for p in photos)
        for year_str in sorted(by_year.keys()):
            photos = by_year[year_str]
            photo_ids = [p["id"] for p in photos]
            years_ago = current_year - int(year_str)

            placeholders = ",".join("?" * len(photo_ids))

            # Get people (None when this library has no face data)
            people: list[dict[str, Any]] | None = [] if has_faces else None
            if photo_ids and has_faces:
                cursor.execute(
                    f"""
                    SELECT DISTINCT p.ZFULLNAME, COUNT(df.{schema["asset_fk"]}) as count
                    FROM ZPERSON p
                    JOIN ZDETECTEDFACE df ON p.Z_PK = df.{schema["person_fk"]}
                    WHERE df.{schema["asset_fk"]} IN ({placeholders})
                    AND p.ZFULLNAME IS NOT NULL AND p.ZFULLNAME != ''
                    GROUP BY p.Z_PK
                    ORDER BY count DESC
                    LIMIT 5
                """,
                    photo_ids,
                )
                people = [{"name": row["ZFULLNAME"], "count": row["count"]} for row in cursor.fetchall()]

            # Get scenes (None when this library has no scene data)
            scenes: list[dict[str, Any]] | None = [] if has_scenes else None
            if photo_ids and scenes_from == SEARCH_INDEX:
                scenes = index_labels.top(photo_ids)
            elif photo_ids and has_scenes:
                cursor.execute(
                    f"""
                    SELECT sc.ZSCENENAME, COUNT(*) as count
                    FROM ZSCENECLASSIFICATION sc
                    WHERE sc.ZASSET IN ({placeholders})
                    AND sc.ZSCENENAME IS NOT NULL
                    GROUP BY sc.ZSCENENAME
                    ORDER BY count DESC
                    LIMIT 5
                """,
                    photo_ids,
                )
                scenes = [
                    {"scene": row["ZSCENENAME"], "count": row["count"]}
                    for row in cursor.fetchall()
                    if row["ZSCENENAME"]
                ]

            # Best photo for this year
            non_screenshots = [p for p in photos if not p["is_screenshot"]]
            best = None
            if non_screenshots:
                scored = [p for p in non_screenshots if p["quality_score"] is not None]
                if scored:
                    best = max(scored, key=lambda p: p["quality_score"])
                else:
                    favorites = [p for p in non_screenshots if p["is_favorite"]]
                    best = favorites[0] if favorites else non_screenshots[0]

            favorites_count = sum(1 for p in photos if p["is_favorite"])
            total_size = sum(p["size"] for p in photos)

            year_summaries.append(
                {
                    "year": int(year_str),
                    "years_ago": years_ago,
                    "photo_count": len(photos),
                    "favorites": favorites_count,
                    "total_size": total_size,
                    "total_size_formatted": format_size(total_size),
                    "people": people,
                    "scenes": scenes,
                    "best_photo": best,
                    "photos": photos,
                }
            )

        # Sort by years ago (most recent first)
        year_summaries.sort(key=lambda x: x["years_ago"])

        return {
            "degraded": degraded.entries,
            "target_date": target.isoformat(),
            "target_month_day": f"{target.strftime('%B')} {target.day}",
            "window_days": window_days,
            "years": year_summaries,
            "summary": {
                "total_photos": total_photos,
                "years_with_photos": len(year_summaries),
            },
        }


def format_summary(data: dict[str, Any]) -> str:
    """Format on-this-day results as human-readable summary."""
    lines = []
    lines.append("📅 ON THIS DAY")
    lines.append("=" * 50)
    lines.append("")

    lines.append(f"Date: {data['target_month_day']}")
    if data["window_days"]:
        lines.append(f"Window: ±{data['window_days']} days")
    lines.append(
        f"Photos found: {data['summary']['total_photos']:,} across {data['summary']['years_with_photos']} years"
    )
    lines.append("")

    if not data["years"]:
        lines.append("No photos found for this date in previous years.")
        return "\n".join(lines)

    for year_data in data["years"]:
        years_ago = year_data["years_ago"]
        year_label = f"{years_ago} year{'s' if years_ago != 1 else ''} ago" if years_ago > 0 else "This year"
        fav_str = f", ⭐ {year_data['favorites']}" if year_data["favorites"] else ""

        lines.append(f"📆 {year_data['year']} ({year_label})")
        lines.append(f"   {year_data['photo_count']} photos{fav_str}")

        if year_data["people"]:
            names = ", ".join(p["name"] for p in year_data["people"][:3])
            lines.append(f"   👥 {names}")

        if year_data["scenes"]:
            scene_str = ", ".join(s["scene"] for s in year_data["scenes"][:3])
            lines.append(f"   🏷️  {scene_str}")

        if year_data["best_photo"]:
            bp = year_data["best_photo"]
            q_str = f" Q:{bp['quality_score']:.2f}" if bp["quality_score"] else ""
            lines.append(f"   📸 Best: {display_name(bp)}{q_str}")

        lines.append("")

    return "\n".join(lines)


def main():
    def add_args(parser):
        parser.add_argument("--date", help="Target date (YYYY-MM-DD), defaults to today")
        parser.add_argument(
            "--window", type=int, default=0, help="Include photos ± this many days around target (default: 0)"
        )

    def invoke(db_path, args):
        return on_this_day(
            db_path=db_path,
            target_date=args.date,
            window_days=args.window,
        )

    return run_script(
        description="Show photos from this date in previous years",
        analyze_fn=invoke,
        format_fn=format_summary,
        extra_args_fn=add_args,
        epilog="""
Examples:
  # Today's date in previous years
  %(prog)s --human

  # Specific date
  %(prog)s --date 2026-03-03 --human

  # With a 2-day window (±2 days)
  %(prog)s --window 2 --human
        """,
    )


if __name__ == "__main__":
    sys.exit(main())
