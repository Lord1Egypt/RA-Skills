#!/usr/bin/env python3
"""
Scene / Content Search: query photos by ML-detected scene classifications.
Search by content type (beach, sunset, dog, food), generate content inventory.
"""

import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from _common import (
    PhotosDB,
    coredata_to_local,
    display_name,
    format_size,
    has_timezone_offset,
    local_datetime_sql,
    original_filename_sql,
    run_script,
    tz_offset_sql,
    validate_year,
)
from _scenes import (
    CONFIDENCE_LIMITATION,
    DATABASE,
    SEARCH_INDEX,
    SearchIndex,
    confidence_limited,
    scene_source,
    search_index_available,
)
from _schema import FILE_SIZE, ORIGINAL_FILENAME, SCENES, Degradation, get_schema

# Schema contract (T1.4): see _schema. Missing required → exit 5; missing optional → `degraded`.
REQUIRED_COLUMNS: tuple[str, ...] = (
    "ZASSET.ZDATECREATED",
    "ZASSET.ZFAVORITE",
    "ZASSET.ZFILENAME",
    "ZASSET.ZKIND",
    "ZASSET.ZLATITUDE",
    "ZASSET.ZLONGITUDE",
    "ZASSET.ZTRASHEDSTATE",
    *FILE_SIZE,
)
# Scene names come from ZSCENECLASSIFICATION (older macOS) or Photos' search index (macOS 26); see _scenes.
OPTIONAL_COLUMNS: dict[str, tuple[str, ...]] = {
    "original_filenames": ORIGINAL_FILENAME,
    "scenes": SCENES,
    "scene_confidence": ("ZSCENECLASSIFICATION.ZCONFIDENCE",),
}
# A section whose columns are missing is still available when this source exists (doctor uses it).
ALTERNATE_SOURCES = {"scenes": search_index_available}
# A section that stays limited because of which source was chosen (doctor reports the reason).
SOURCE_LIMITATIONS = {"scene_confidence": confidence_limited}


def search_scenes(
    db_path: str | None = None,
    search_term: str | None = None,
    min_confidence: float = 0.0,
    top_n: int = 50,
    year: str | None = None,
) -> dict[str, Any]:
    """
    Search photos by scene classification or generate content inventory.

    Scene labels come from ZSCENECLASSIFICATION on older libraries and from Photos' search index on
    macOS 26 (see _scenes). With neither, the result is an error with ``scenes`` degraded.

    Args:
        db_path: Path to database
        search_term: Scene name to search for (None = show inventory)
        min_confidence: Minimum confidence score for scene matches (database source only)
        top_n: Number of results to return for search
        year: Filter to specific year

    Returns:
        Scene search/inventory dictionary
    """
    with PhotosDB(db_path, require=REQUIRED_COLUMNS, operation="Scene search") as conn:
        cursor = conn.cursor()
        tz_available = has_timezone_offset(cursor)
        schema = get_schema(conn)
        degraded = Degradation(schema)

        year_filter = ""
        year_params: list = []
        if year:
            year = validate_year(year)
            year_filter = f"AND strftime('%Y', {local_datetime_sql(tz_available)}) = ?"
            year_params = [year]

        source = scene_source(conn)
        ctx = SceneQuery(cursor, schema, degraded, min_confidence, year_filter, year_params, tz_available, source)
        if source is None:
            degraded.check("scenes", *OPTIONAL_COLUMNS["scenes"])
            return _unavailable(ctx, search_term)
        if source == DATABASE:
            degraded.check("scene_confidence", *OPTIONAL_COLUMNS["scene_confidence"])
        else:
            degraded.note("scene_confidence", CONFIDENCE_LIMITATION)
        if search_term:
            return _search_by_scene(ctx, search_term, top_n)
        return _generate_inventory(ctx)


@dataclass
class SceneQuery:
    cursor: Any
    schema: Any
    degraded: Degradation
    min_confidence: float
    year_filter: str
    year_params: list
    tz_available: bool
    source: str | None

    @property
    def confidence(self) -> str:
        """SQL for a row's confidence; NULL when the column is gone (the filter then passes every row)."""
        return "sc.ZCONFIDENCE" if self.schema.has("ZSCENECLASSIFICATION.ZCONFIDENCE") else "NULL"

    @property
    def index_path(self) -> str:
        return str(self.cursor.connection.db_file)


def _unavailable(ctx: SceneQuery, search_term: str | None) -> dict[str, Any]:
    error = (
        "Scene labels aren't available: this library's ZSCENECLASSIFICATION has no scene names, "
        "and no Photos search index (database/search/psi.sqlite) was found next to it."
    )
    if search_term:
        return {
            "error": error,
            "degraded": ctx.degraded.entries,
            "mode": "search",
            "source": None,
            "search_term": search_term,
            "results": [],
            "related_scenes": [],
            "summary": {"total_matches": 0, "shown": 0, "total_size": 0, "total_size_formatted": "0 B"},
        }
    return {
        "error": error,
        "degraded": ctx.degraded.entries,
        "mode": "inventory",
        "source": None,
        "scenes": [],
        "categories": {},
        "summary": {"total_scenes": 0, "total_tagged_photos": 0, "total_photos": 0, "coverage": 0},
    }


def _asset_rows(ctx: SceneQuery, where: str, params: list) -> list:
    """Non-trashed assets matching *where* (and the year filter), with the columns a result needs."""
    name_col = original_filename_sql(ctx.schema)
    ctx.cursor.execute(
        f"""
        SELECT a.Z_PK, a.ZUUID, a.ZFILENAME, {name_col}, a.ZDATECREATED, a.ZKIND, a.ZFAVORITE,
               a.ZLATITUDE, a.ZLONGITUDE, aa.ZORIGINALFILESIZE,
               {tz_offset_sql(ctx.tz_available)} AS tz_offset
        FROM ZASSET a
        LEFT JOIN ZADDITIONALASSETATTRIBUTES aa ON a.Z_PK = aa.ZASSET
        WHERE a.ZTRASHEDSTATE != 1 AND {where}
        {ctx.year_filter}
        """,
        [*params, *ctx.year_params],
    )
    return list(ctx.cursor.fetchall())


def _result(row: Any, scene: str, confidence: float | None) -> dict[str, Any]:
    created = coredata_to_local(row["ZDATECREATED"], row["tz_offset"])
    size = row["ZORIGINALFILESIZE"] or 0
    return {
        "id": row["Z_PK"],
        "filename": row["ZFILENAME"],
        "original_filename": row["original_filename"],
        "created": created.isoformat() if created else None,
        "kind": "photo" if row["ZKIND"] == 0 else "video",
        "is_favorite": bool(row["ZFAVORITE"]),
        "size": size,
        "size_formatted": format_size(size),
        "scene": scene,
        "confidence": round(confidence, 3) if confidence else None,
        "latitude": row["ZLATITUDE"],
        "longitude": row["ZLONGITUDE"],
    }


def _search_result(ctx: SceneQuery, search_term: str, results: list, total_matches: int, related: list) -> dict:
    total_size = sum(r["size"] for r in results)
    return {
        "degraded": ctx.degraded.entries,
        "mode": "search",
        "source": ctx.source,
        "search_term": search_term,
        "results": results,
        "related_scenes": related,
        "summary": {
            "total_matches": total_matches,
            "shown": len(results),
            "total_size": total_size,
            "total_size_formatted": format_size(total_size),
            "min_confidence": ctx.min_confidence,
        },
    }


def _search_by_scene(ctx: SceneQuery, search_term: str, top_n: int) -> dict[str, Any]:
    """Search photos matching a scene label."""
    # Only search results list files, so only this path can lose original names.
    ctx.degraded.check("original_filenames", *OPTIONAL_COLUMNS["original_filenames"])
    if ctx.source == SEARCH_INDEX:
        return _search_by_scene_in_index(ctx, search_term, top_n)

    conf = ctx.confidence
    cursor = ctx.cursor
    name_col = original_filename_sql(ctx.schema)
    search_pattern = f"%{search_term.lower()}%"
    cursor.execute(
        f"""
        SELECT
            a.Z_PK, a.ZFILENAME, {name_col}, a.ZDATECREATED, a.ZKIND, a.ZFAVORITE,
            a.ZLATITUDE, a.ZLONGITUDE, aa.ZORIGINALFILESIZE,
            {tz_offset_sql(ctx.tz_available)} AS tz_offset,
            sc.ZSCENENAME,
            {conf} AS ZCONFIDENCE
        FROM ZASSET a
        JOIN ZSCENECLASSIFICATION sc ON a.Z_PK = sc.ZASSET
        LEFT JOIN ZADDITIONALASSETATTRIBUTES aa ON a.Z_PK = aa.ZASSET
        WHERE a.ZTRASHEDSTATE != 1
        AND LOWER(sc.ZSCENENAME) LIKE ?
        AND ({conf} >= ? OR {conf} IS NULL)
        {ctx.year_filter}
        ORDER BY ZCONFIDENCE DESC NULLS LAST, a.ZDATECREATED DESC
        LIMIT ?
    """,
        (search_pattern, ctx.min_confidence, *ctx.year_params, top_n),
    )
    results = [_result(row, row["ZSCENENAME"], row["ZCONFIDENCE"]) for row in cursor.fetchall()]

    cursor.execute(
        f"""
        SELECT COUNT(*) as total
        FROM ZASSET a
        JOIN ZSCENECLASSIFICATION sc ON a.Z_PK = sc.ZASSET
        LEFT JOIN ZADDITIONALASSETATTRIBUTES aa ON a.Z_PK = aa.ZASSET
        WHERE a.ZTRASHEDSTATE != 1
        AND LOWER(sc.ZSCENENAME) LIKE ?
        AND ({conf} >= ? OR {conf} IS NULL)
        {ctx.year_filter}
    """,
        (search_pattern, ctx.min_confidence, *ctx.year_params),
    )
    total_matches = cursor.fetchone()["total"]

    related_scenes = []
    if results:
        photo_ids = [r["id"] for r in results[:100]]
        placeholders = ",".join("?" * len(photo_ids))
        cursor.execute(
            f"""
            SELECT sc.ZSCENENAME, COUNT(DISTINCT sc.ZASSET) as count
            FROM ZSCENECLASSIFICATION sc
            WHERE sc.ZASSET IN ({placeholders})
            AND LOWER(sc.ZSCENENAME) NOT LIKE ?
            GROUP BY sc.ZSCENENAME
            ORDER BY count DESC
            LIMIT 10
        """,
            [*photo_ids, search_pattern],
        )
        related_scenes = [
            {"scene": row["ZSCENENAME"], "count": row["count"]} for row in cursor.fetchall() if row["ZSCENENAME"]
        ]
    return _search_result(ctx, search_term, results, total_matches, related_scenes)


def _search_by_scene_in_index(ctx: SceneQuery, search_term: str, top_n: int) -> dict[str, Any]:
    """macOS 26: labels (and their synonyms) from the search index, then photos from ZASSET by UUID."""
    with SearchIndex(ctx.index_path) as index:
        matches = index.search(search_term)
    label_of: dict[str, str] = {}
    for label in sorted(matches):  # deterministic label when a photo matches several
        for asset_uuid in matches[label]:
            label_of.setdefault(asset_uuid, label)

    rows: list = []
    uuids = list(label_of)
    for start in range(0, len(uuids), 900):
        chunk = uuids[start : start + 900]
        rows += _asset_rows(ctx, f"upper(a.ZUUID) IN ({','.join('?' * len(chunk))})", chunk)
    # Newest first; undated photos last (reverse=True puts the False "is dated" key at the end).
    rows.sort(key=lambda row: (row["ZDATECREATED"] is not None, row["ZDATECREATED"] or 0), reverse=True)
    results = [_result(row, label_of[row["ZUUID"].upper()], None) for row in rows[:top_n]]

    related_scenes: list[dict] = []
    if results:
        with SearchIndex(ctx.index_path) as index:
            counts = index.labels_for(row["ZUUID"] for row in rows[: min(len(results), 100)])
        related_scenes = [{"scene": label, "count": n} for label, n in counts.most_common() if label not in matches][
            :10
        ]
    return _search_result(ctx, search_term, results, len(rows), related_scenes)


def _categorize(scene: str | None) -> str:
    """Bucket a scene label into a broad category for the inventory."""
    scene_lower = scene.lower() if scene else ""
    if any(w in scene_lower for w in ["dog", "cat", "bird", "fish", "animal", "pet", "horse"]):
        return "animals"
    elif any(
        w in scene_lower for w in ["food", "meal", "dinner", "lunch", "breakfast", "dessert", "cake", "pizza", "coffee"]
    ):
        return "food_drink"
    elif any(
        w in scene_lower
        for w in [
            "beach",
            "ocean",
            "mountain",
            "lake",
            "forest",
            "park",
            "garden",
            "sunset",
            "sunrise",
            "sky",
            "snow",
            "field",
            "river",
            "waterfall",
        ]
    ):
        return "nature_outdoor"
    elif any(
        w in scene_lower
        for w in ["sport", "swim", "run", "ball", "game", "gym", "fitness", "soccer", "basketball", "baseball"]
    ):
        return "sports"
    elif any(
        w in scene_lower
        for w in ["car", "road", "street", "building", "house", "city", "bridge", "train", "airplane", "boat"]
    ):
        return "urban_travel"
    elif any(
        w in scene_lower
        for w in ["face", "selfie", "portrait", "people", "group", "family", "baby", "child", "wedding"]
    ):
        return "people"
    else:
        return "other"


def _inventory_result(ctx: SceneQuery, all_scenes: list[dict]) -> dict[str, Any]:
    categories: dict[str, list] = defaultdict(list)
    for scene_data in all_scenes:
        categories[_categorize(scene_data["scene"])].append(scene_data)
    total_tagged = sum(s["photo_count"] for s in all_scenes)
    ctx.cursor.execute(
        f"""
        SELECT COUNT(*) as total FROM ZASSET a
        LEFT JOIN ZADDITIONALASSETATTRIBUTES aa ON a.Z_PK = aa.ZASSET
        WHERE a.ZTRASHEDSTATE != 1 {ctx.year_filter}
    """,
        ctx.year_params,
    )
    total_all = ctx.cursor.fetchone()["total"]
    return {
        "degraded": ctx.degraded.entries,
        "mode": "inventory",
        "source": ctx.source,
        "scenes": all_scenes,
        "categories": {k: v for k, v in sorted(categories.items())},
        "summary": {
            "total_scenes": len(all_scenes),
            "total_tagged_photos": total_tagged,
            "total_photos": total_all,
            "coverage": round(total_tagged / total_all * 100, 1) if total_all else 0,
            "min_confidence": ctx.min_confidence,
        },
    }


def _generate_inventory(ctx: SceneQuery) -> dict[str, Any]:
    """Generate a complete content inventory by scene type."""
    if ctx.source == SEARCH_INDEX:
        with SearchIndex(ctx.index_path) as index:
            labels = index.inventory()
        present = {row["ZUUID"].upper() for row in _asset_rows(ctx, "a.ZUUID IS NOT NULL", [])}
        counted = ((label, len(uuids & present)) for label, uuids in labels.items() if label)
        all_scenes = [
            {"scene": label, "photo_count": n, "avg_confidence": None}
            for label, n in sorted(counted, key=lambda item: (-item[1], item[0]))
            if n
        ]
        return _inventory_result(ctx, all_scenes)

    conf = ctx.confidence
    ctx.cursor.execute(
        f"""
        SELECT
            sc.ZSCENENAME,
            COUNT(DISTINCT sc.ZASSET) as photo_count,
            AVG({conf}) as avg_confidence
        FROM ZSCENECLASSIFICATION sc
        JOIN ZASSET a ON sc.ZASSET = a.Z_PK
        LEFT JOIN ZADDITIONALASSETATTRIBUTES aa ON a.Z_PK = aa.ZASSET
        WHERE a.ZTRASHEDSTATE != 1
        AND sc.ZSCENENAME IS NOT NULL
        AND ({conf} >= ? OR {conf} IS NULL)
        {ctx.year_filter}
        GROUP BY sc.ZSCENENAME
        ORDER BY photo_count DESC
    """,
        (ctx.min_confidence, *ctx.year_params),
    )
    all_scenes = [
        {
            "scene": row["ZSCENENAME"],
            "photo_count": row["photo_count"],
            "avg_confidence": round(row["avg_confidence"], 3) if row["avg_confidence"] else None,
        }
        for row in ctx.cursor.fetchall()
    ]
    return _inventory_result(ctx, all_scenes)


def format_summary(data: dict[str, Any]) -> str:
    """Format scene search/inventory as human-readable summary."""
    lines = []
    lines.append("🏷️  SCENE / CONTENT SEARCH")
    lines.append("=" * 50)
    lines.append("")
    if "error" in data:
        lines.append(f"⚠️  {data['error']}")
        return "\n".join(lines)

    if data["mode"] == "search":
        summary = data["summary"]
        lines.append(f'Search: "{data["search_term"]}"')
        lines.append(f"Matches: {summary['total_matches']:,} (showing {summary['shown']})")
        lines.append(f"Total size: {summary['total_size_formatted']}")
        lines.append("")

        lines.append("Results:")
        for r in data["results"][:20]:
            fav = " ★" if r["is_favorite"] else ""
            conf = f" ({r['confidence']:.2f})" if r["confidence"] else ""
            lines.append(f"  {display_name(r)} | {r['scene']}{conf}{fav}")

        if data["related_scenes"]:
            lines.append("")
            lines.append("Related scenes:")
            for rs in data["related_scenes"]:
                lines.append(f"  {rs['scene']}: {rs['count']} photos")

    else:  # inventory
        summary = data["summary"]
        lines.append(f"Unique scene labels: {summary['total_scenes']:,}")
        lines.append(f"Scene-tagged entries: {summary['total_tagged_photos']:,}")
        lines.append(f"Library total: {summary['total_photos']:,}")
        lines.append("")

        if data["categories"]:
            lines.append("By Category:")
            for cat_name, scenes in sorted(data["categories"].items()):
                cat_total = sum(s["photo_count"] for s in scenes)
                lines.append(f"\n  📂 {cat_name.replace('_', ' ').title()} ({cat_total:,} photos)")
                for scene in scenes[:8]:
                    lines.append(f"    {scene['scene']}: {scene['photo_count']:,}")
                if len(scenes) > 8:
                    lines.append(f"    ... and {len(scenes) - 8} more")

        lines.append("")
        lines.append("Top 20 Scene Labels:")
        for scene in data["scenes"][:20]:
            lines.append(f"  {scene['scene']}: {scene['photo_count']:,}")

    lines.append("")
    return "\n".join(lines)


def main():
    def add_args(parser):
        parser.add_argument("--search", help="Scene name to search for")
        parser.add_argument("--min-confidence", type=float, default=0.0, help="Minimum confidence score (default: 0.0)")
        parser.add_argument("--top", type=int, default=50, help="Number of search results (default: 50)")
        parser.add_argument("--year", help="Filter to specific year (YYYY, local capture time)")

    def invoke(db_path, args):
        return search_scenes(
            db_path=db_path,
            search_term=args.search,
            min_confidence=args.min_confidence,
            top_n=args.top,
            year=args.year,
        )

    return run_script(
        description="Search photos by scene/content or generate content inventory",
        analyze_fn=invoke,
        format_fn=format_summary,
        extra_args_fn=add_args,
        epilog="""
Examples:
  # Content inventory
  %(prog)s --human

  # Search for beach photos
  %(prog)s --search beach --human

  # Search for dogs with high confidence
  %(prog)s --search dog --min-confidence 0.5 --human

  # Content inventory for 2025
  %(prog)s --year 2025 --human
        """,
    )


if __name__ == "__main__":
    sys.exit(main())
