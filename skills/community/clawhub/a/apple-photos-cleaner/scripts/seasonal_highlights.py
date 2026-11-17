#!/usr/bin/env python3
"""
Seasonal Highlights: curate the best photos from each season of the year.

Selects top photos per season (spring, summer, fall, winter) using
quality scores, favorites, and scene context to build highlight reels.
"""

import sys
from typing import Any

from _common import (
    PhotosDB,
    computed_scores_sql,
    coredata_to_local,
    display_name,
    format_size,
    get_quality_score,
    has_timezone_offset,
    local_datetime_sql,
    original_filename_sql,
    run_script,
    tz_offset_sql,
    validate_year,
)
from _schema import FILE_SIZE, ORIGINAL_FILENAME, Degradation, get_schema

# Schema contract (T1.4): see _schema. Missing required → exit 5; missing optional → `degraded`.
REQUIRED_COLUMNS: tuple[str, ...] = (
    "ZASSET.ZDATECREATED",
    "ZASSET.ZFAVORITE",
    "ZASSET.ZFILENAME",
    "ZASSET.ZHEIGHT",
    "ZASSET.ZKIND",
    "ZASSET.ZLATITUDE",
    "ZASSET.ZLONGITUDE",
    "ZASSET.ZTRASHEDSTATE",
    "ZASSET.ZWIDTH",
    *FILE_SIZE,
)
# The seasonal score blends whichever of these exist.
SEASONAL_SCORE_COLUMNS = (
    "ZPLEASANTCOMPOSITIONSCORE",
    "ZPLEASANTLIGHTINGSCORE",
    "ZPLEASANTPATTERNSCORE",
    "ZFAILURESCORE",
    "ZNOISESCORE",
    "ZHARMONIOUSCOLORSCORE",
    "ZPLEASANTSYMMETRYSCORE",
    "ZPLEASANTWALLPAPERSCORE",
    "ZWEIGHTEDSCENECLASSIFICATIONSCORE",
)
OPTIONAL_COLUMNS: dict[str, tuple[str, ...]] = {
    "original_filenames": ORIGINAL_FILENAME,
    "scores": ("ZCOMPUTEDASSETATTRIBUTES.ZASSET", *(f"ZCOMPUTEDASSETATTRIBUTES.{c}" for c in SEASONAL_SCORE_COLUMNS)),
    "titles": ("ZADDITIONALASSETATTRIBUTES.ZTITLE",),
}

# Season definitions (Northern Hemisphere by default)
SEASONS_NH = {
    "winter": [12, 1, 2],
    "spring": [3, 4, 5],
    "summer": [6, 7, 8],
    "fall": [9, 10, 11],
}

SEASONS_SH = {
    "summer": [12, 1, 2],
    "fall": [3, 4, 5],
    "winter": [6, 7, 8],
    "spring": [9, 10, 11],
}

SEASON_EMOJI = {
    "spring": "🌸",
    "summer": "☀️",
    "fall": "🍂",
    "winter": "❄️",
}

MONTH_TO_SEASON_NH = {}
for season, months in SEASONS_NH.items():
    for m in months:
        MONTH_TO_SEASON_NH[m] = season

MONTH_TO_SEASON_SH = {}
for season, months in SEASONS_SH.items():
    for m in months:
        MONTH_TO_SEASON_SH[m] = season


def get_seasonal_highlights(
    db_path: str | None = None,
    year: str | None = None,
    top_n: int = 20,
    southern_hemisphere: bool = False,
) -> dict[str, Any]:
    """
    Select the best photos from each season.

    Args:
        db_path: Path to database
        year: Filter to specific year (or "all")
        top_n: Number of top photos per season
        southern_hemisphere: Use Southern Hemisphere season definitions

    Returns:
        Season-based photo highlights
    """
    month_to_season = MONTH_TO_SEASON_SH if southern_hemisphere else MONTH_TO_SEASON_NH

    with PhotosDB(db_path, require=REQUIRED_COLUMNS, operation="Seasonal highlights") as conn:
        name_col = original_filename_sql(get_schema(conn))
        cursor = conn.cursor()
        tz_available = has_timezone_offset(cursor)
        registry = get_schema(conn)
        degraded = Degradation(registry)
        degraded.check("original_filenames", *OPTIONAL_COLUMNS["original_filenames"])
        degraded.check("scores", *OPTIONAL_COLUMNS["scores"])
        degraded.check("titles", *OPTIONAL_COLUMNS["titles"])
        score_terms, score_join = computed_scores_sql(registry, *SEASONAL_SCORE_COLUMNS)

        where = ["a.ZTRASHEDSTATE != 1", "a.ZKIND = 0"]  # Photos only
        params: list = []
        if year and year != "all":
            year = validate_year(year)
            where.append(f"strftime('%Y', {local_datetime_sql(tz_available)}) = ?")
            params.append(year)

        query = f"""
            SELECT
                a.Z_PK, a.ZFILENAME, {name_col}, a.ZDATECREATED, a.ZFAVORITE,
                a.ZWIDTH, a.ZHEIGHT, a.ZLATITUDE, a.ZLONGITUDE,
                aa.ZORIGINALFILESIZE, {registry.select("ZADDITIONALASSETATTRIBUTES.ZTITLE", "aa")},
                {tz_offset_sql(tz_available)} AS tz_offset,
                {", ".join(score_terms)}
            FROM ZASSET a
            LEFT JOIN ZADDITIONALASSETATTRIBUTES aa ON a.Z_PK = aa.ZASSET
            {score_join}
            WHERE {" AND ".join(where)}
            ORDER BY a.ZDATECREATED DESC
        """
        cursor.execute(query, params)

        by_season: dict[str, list[dict]] = {
            "spring": [],
            "summer": [],
            "fall": [],
            "winter": [],
        }
        by_year_season: dict[str, dict[str, int]] = {}
        total_by_season: dict[str, int] = {
            "spring": 0,
            "summer": 0,
            "fall": 0,
            "winter": 0,
        }

        for row in cursor.fetchall():
            rd = dict(row)
            created = coredata_to_local(rd["ZDATECREATED"], rd["tz_offset"])
            if not created:
                continue

            month = created.month
            season = month_to_season.get(month, "winter")
            yr = str(created.year)
            total_by_season[season] += 1

            if yr not in by_year_season:
                by_year_season[yr] = {"spring": 0, "summer": 0, "fall": 0, "winter": 0}
            by_year_season[yr][season] += 1

            quality = get_quality_score(rd)
            is_fav = bool(rd.get("ZFAVORITE"))
            # Boost favorites significantly in ranking
            score = (quality or 0) + (0.3 if is_fav else 0)

            photo = {
                "id": rd["Z_PK"],
                "filename": rd["ZFILENAME"],
                "original_filename": rd["original_filename"],
                "title": rd.get("ZTITLE"),
                "created": created.isoformat(),
                "year": yr,
                "month": created.month,
                "is_favorite": is_fav,
                "quality_score": round(quality, 3) if quality else None,
                "combined_score": round(score, 3),
                "size": rd.get("ZORIGINALFILESIZE") or 0,
                "size_formatted": format_size(rd.get("ZORIGINALFILESIZE") or 0),
                "dimensions": f"{rd.get('ZWIDTH', 0)}x{rd.get('ZHEIGHT', 0)}",
                "has_location": bool(rd.get("ZLATITUDE")),
            }

            by_season[season].append(photo)

        # Sort each season by combined score and take top N
        highlights = {}
        for season in ["spring", "summer", "fall", "winter"]:
            by_season[season].sort(key=lambda p: p["combined_score"], reverse=True)
            top = by_season[season][:top_n]
            highlights[season] = {
                "emoji": SEASON_EMOJI[season],
                "total_photos": total_by_season[season],
                "highlights": top,
                "best_photo": top[0] if top else None,
                "favorites_in_top": sum(1 for p in top if p["is_favorite"]),
                "avg_quality": round(sum(p["combined_score"] for p in top) / max(1, len(top)), 3),
                "unique_years": sorted({p["year"] for p in top}),
            }

        # Year-season distribution
        distribution = [
            {
                "year": yr,
                **{s: ct for s, ct in info.items()},
            }
            for yr, info in sorted(by_year_season.items(), reverse=True)
        ]

        total_photos = sum(total_by_season.values())
        busiest_season = max(total_by_season, key=lambda s: total_by_season[s]) if total_photos else None

        return {
            "degraded": degraded.entries,
            "highlights": highlights,
            "distribution": distribution[:20],
            "summary": {
                "total_photos": total_photos,
                "by_season": total_by_season,
                "busiest_season": busiest_season,
                "busiest_emoji": SEASON_EMOJI.get(busiest_season, "") if busiest_season else "",
                "hemisphere": "southern" if southern_hemisphere else "northern",
                "top_n": top_n,
                "year_filter": year or "all years",
            },
        }


def format_summary(data: dict[str, Any]) -> str:
    """Format human-readable summary."""
    lines = []
    s = data["summary"]

    lines.append("🗓️  SEASONAL HIGHLIGHTS")
    lines.append("=" * 50)
    lines.append(f"Total photos:     {s['total_photos']:,}")
    lines.append(f"Hemisphere:       {s['hemisphere']}")
    lines.append(f"Year filter:      {s['year_filter']}")
    lines.append(f"Busiest season:   {s['busiest_emoji']} {s['busiest_season']}")
    lines.append("")

    for season in ["spring", "summer", "fall", "winter"]:
        info = data["highlights"][season]
        emoji = info["emoji"]
        lines.append(f"{emoji} {season.upper()} ({info['total_photos']:,} photos)")
        lines.append(f"   Avg quality: {info['avg_quality']:.3f}  |  Favorites in top: {info['favorites_in_top']}")

        if info["best_photo"]:
            bp = info["best_photo"]
            lines.append(f"   ⭐ Best: {display_name(bp)} ({bp['created'][:10]})")

        for p in info["highlights"][:5]:
            fav = "⭐" if p["is_favorite"] else "  "
            lines.append(f"   {fav} {display_name(p):40s} {p['created'][:10]}  Q={p['combined_score']:.3f}")
        lines.append("")

    if data["distribution"]:
        lines.append("Year distribution:")
        lines.append(f"  {'Year':<8} {'🌸 Spr':>8} {'☀️ Sum':>8} {'🍂 Fall':>8} {'❄️ Win':>8}")
        for row in data["distribution"][:10]:
            lines.append(
                f"  {row['year']:<8} {row.get('spring', 0):>8,} {row.get('summer', 0):>8,} "
                f"{row.get('fall', 0):>8,} {row.get('winter', 0):>8,}"
            )

    return "\n".join(lines)


def main():
    def add_args(parser):
        parser.add_argument("--year", help="Filter to specific year (YYYY, local capture time)")
        parser.add_argument("--top", type=int, default=20, help="Top N photos per season (default: 20)")
        parser.add_argument(
            "--southern",
            action="store_true",
            help="Use Southern Hemisphere seasons",
        )

    def invoke(db_path, args):
        return get_seasonal_highlights(
            db_path=db_path,
            year=args.year,
            top_n=args.top,
            southern_hemisphere=args.southern,
        )

    return run_script(
        description="Curate seasonal photo highlights",
        analyze_fn=invoke,
        format_fn=format_summary,
        extra_args_fn=add_args,
    )


if __name__ == "__main__":
    sys.exit(main())
