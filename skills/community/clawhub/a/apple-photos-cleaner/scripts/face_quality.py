#!/usr/bin/env python3
"""
Face Quality Scoring: analyze detected faces to find the best and worst
portraits per person.

Uses Apple Photos' face detection attributes: quality measure, blur score,
yaw angle, smile score, face size, and center position to rank face photos.
"""

import sys
from typing import Any

from _common import (
    PhotosDB,
    _safe_float,
    coredata_to_local,
    display_name,
    format_size,
    has_timezone_offset,
    original_filename_sql,
    run_script,
    tz_offset_sql,
)
from _schema import FACES, FILE_SIZE, ORIGINAL_FILENAME, Degradation, get_schema

# Schema contract (T1.4): see _schema. Missing required → exit 5; missing optional → `degraded`.
REQUIRED_COLUMNS: tuple[str, ...] = (
    "ZASSET.ZDATECREATED",
    "ZASSET.ZFAVORITE",
    "ZASSET.ZFILENAME",
    "ZASSET.ZHEIGHT",
    "ZASSET.ZTRASHEDSTATE",
    "ZASSET.ZWIDTH",
    *FILE_SIZE,
)
OPTIONAL_COLUMNS: dict[str, tuple[str, ...]] = {
    "original_filenames": ORIGINAL_FILENAME,
    "faces": (*FACES, "face.quality"),
    "blur": ("face.blur",),
    "smile": ("face.smile",),
    "catalog_face_count": ("ZPERSON.ZFACECOUNT",),
    # compute_face_score() falls back to neutral values for these when absent
    "face_score": ("ZDETECTEDFACE.ZSIZE", "ZDETECTEDFACE.ZYAWANGLE", "ZDETECTEDFACE.ZFACEISINCENTER"),
}


def compute_face_score(row: dict) -> float:
    """
    Compute a composite face quality score from individual metrics.

    Higher is better. Components:
    - quality_measure: Apple's overall quality (0-1)
    - blur_score: inverted — lower blur is better
    - face_size: larger face = better portrait
    - yaw_angle: closer to 0 = more frontal
    - smile_score: detected smile (optional bonus)
    - center: face near center of frame (optional bonus)
    """
    quality = _safe_float(row.get("ZQUALITYMEASURE"), 0.5)
    blur = _safe_float(row.get("ZBLURSCORE"), 0.0)
    size = _safe_float(row.get("ZSIZE"), 0.0)
    yaw = abs(_safe_float(row.get("ZYAWANGLE"), 0.0))
    smile = _safe_float(row.get("ZSMILESCORE"), 0.0)
    in_center = _safe_float(row.get("ZFACEISINCENTER"), 0.0)

    # Normalize components to 0-1 range approximately
    quality_component = quality  # already 0-1
    blur_component = max(0, 1.0 - blur)  # less blur is better
    size_component = min(size, 1.0)  # cap at 1
    yaw_component = max(0, 1.0 - (yaw / 1.0))  # frontal is better
    smile_component = min(smile, 1.0)
    center_component = in_center

    # Weighted combination
    score = (
        quality_component * 0.35
        + blur_component * 0.20
        + size_component * 0.15
        + yaw_component * 0.15
        + smile_component * 0.10
        + center_component * 0.05
    )

    return score


def analyze_face_quality(
    db_path: str | None = None,
    person_name: str | None = None,
    top_n: int = 10,
) -> dict[str, Any]:
    """
    Analyze face quality for detected people.

    Args:
        db_path: Path to database
        person_name: Filter to specific person
        top_n: Number of best/worst photos to return per person

    Returns:
        Face quality analysis per person
    """
    with PhotosDB(db_path, require=REQUIRED_COLUMNS, operation="Face quality scoring") as conn:
        name_col = original_filename_sql(get_schema(conn))
        cursor = conn.cursor()
        tz_available = has_timezone_offset(cursor)

        # Check for face detection tables
        schema = get_schema(conn)
        degraded = Degradation(schema)
        degraded.check("original_filenames", *OPTIONAL_COLUMNS["original_filenames"])
        has_faces = degraded.check("faces", *OPTIONAL_COLUMNS["faces"])
        has_blur = degraded.check("blur", *OPTIONAL_COLUMNS["blur"])
        has_smile = degraded.check("smile", *OPTIONAL_COLUMNS["smile"])
        degraded.check("catalog_face_count", *OPTIONAL_COLUMNS["catalog_face_count"])
        degraded.check("face_score", *OPTIONAL_COLUMNS["face_score"])
        if not has_faces:
            return {
                "degraded": degraded.entries,
                "error": "Face detection or face quality data not found in this database version.",
                "people": [],
                "summary": {"total_people": 0, "total_faces": 0},
            }

        # macOS 15 renamed these foreign keys; the registry picks whichever exists.
        person_fk = schema.col("face.person_fk")
        asset_fk = schema.col("face.asset_fk")

        # Build face query
        select_cols = [
            f"df.{asset_fk} AS ZASSET",
            f"df.{person_fk} AS ZPERSON",
            "df.ZQUALITYMEASURE",
            "p.ZFULLNAME",
            schema.select("ZPERSON.ZFACECOUNT", "p"),
            "a.ZFILENAME",
            name_col,
            "a.ZDATECREATED",
            "a.ZFAVORITE",
            "a.ZWIDTH",
            "a.ZHEIGHT",
            "aa.ZORIGINALFILESIZE",
            f"{tz_offset_sql(tz_available)} AS tz_offset",
        ]

        optional_cols = {
            "ZBLURSCORE": "df.ZBLURSCORE",
            "ZSIZE": "df.ZSIZE",
            "ZYAWANGLE": "df.ZYAWANGLE",
            "ZSMILESCORE": "df.ZSMILESCORE",
            "ZFACEISINCENTER": "df.ZFACEISINCENTER",
            "ZCONFIDENCE": "df.ZCONFIDENCE",
        }
        for col, expr in optional_cols.items():
            if schema.has_column("ZDETECTEDFACE", col):
                select_cols.append(expr)

        where = [
            "a.ZTRASHEDSTATE != 1",
            "p.ZFULLNAME IS NOT NULL",
            "p.ZFULLNAME != ''",
        ]
        params: list[Any] = []
        if person_name:
            where.append("p.ZFULLNAME LIKE ?")
            params.append(f"%{person_name}%")

        query = f"""
            SELECT {", ".join(select_cols)}
            FROM ZDETECTEDFACE df
            JOIN ZPERSON p ON df.{person_fk} = p.Z_PK
            JOIN ZASSET a ON df.{asset_fk} = a.Z_PK
            LEFT JOIN ZADDITIONALASSETATTRIBUTES aa ON a.Z_PK = aa.ZASSET
            WHERE {" AND ".join(where)}
            ORDER BY p.ZFULLNAME, df.ZQUALITYMEASURE DESC
        """
        cursor.execute(query, params)

        # Group by person
        people_data: dict[str, dict] = {}
        total_faces = 0

        for row in cursor.fetchall():
            rd = dict(row)
            name = rd["ZFULLNAME"]
            total_faces += 1

            if name not in people_data:
                people_data[name] = {
                    "name": name,
                    "face_count": rd.get("ZFACECOUNT") or 0,
                    "faces": [],
                }

            face_score = compute_face_score(rd)
            created = coredata_to_local(rd["ZDATECREATED"], rd["tz_offset"])

            face = {
                "asset_id": rd["ZASSET"],
                "filename": rd["ZFILENAME"],
                "original_filename": rd["original_filename"],
                "created": created.isoformat() if created else None,
                "is_favorite": bool(rd.get("ZFAVORITE")),
                "size": rd.get("ZORIGINALFILESIZE") or 0,
                "size_formatted": format_size(rd.get("ZORIGINALFILESIZE") or 0),
                "dimensions": f"{rd.get('ZWIDTH', 0)}x{rd.get('ZHEIGHT', 0)}",
                "face_score": round(face_score, 4),
                "quality_measure": round(_safe_float(rd.get("ZQUALITYMEASURE")), 4),
                "blur_score": round(_safe_float(rd.get("ZBLURSCORE")), 4) if has_blur else None,
                "smile_score": round(_safe_float(rd.get("ZSMILESCORE")), 4) if has_smile else None,
            }
            people_data[name]["faces"].append(face)

        # Compute per-person stats
        people = []
        for _name, pdata in sorted(people_data.items()):
            faces = pdata["faces"]
            faces.sort(key=lambda f: f["face_score"], reverse=True)

            scores = [f["face_score"] for f in faces]
            avg_score = sum(scores) / len(scores) if scores else 0

            person_entry = {
                "name": pdata["name"],
                "total_faces": len(faces),
                "catalog_face_count": pdata["face_count"],
                "avg_quality": round(avg_score, 4),
                "best_score": round(max(scores), 4) if scores else None,
                "worst_score": round(min(scores), 4) if scores else None,
                "best_photos": faces[:top_n],
                "worst_photos": faces[-top_n:][::-1] if len(faces) > top_n else [],
            }
            people.append(person_entry)

        # Sort by total faces desc
        people.sort(key=lambda p: p["total_faces"], reverse=True)

        # Overall stats
        all_scores = [f["face_score"] for pdata in people_data.values() for f in pdata["faces"]]

        return {
            "degraded": degraded.entries,
            "people": people,
            "summary": {
                "total_people": len(people),
                "total_faces": total_faces,
                "avg_face_quality": round(sum(all_scores) / max(1, len(all_scores)), 4),
                "highest_avg_person": max(people, key=lambda p: p["avg_quality"])["name"] if people else None,
                "most_photographed": people[0]["name"] if people else None,
                "top_n": top_n,
            },
        }


def format_summary(data: dict[str, Any]) -> str:
    """Format human-readable summary."""
    lines = []
    s = data["summary"]

    if "error" in data:
        lines.append(f"⚠️  {data['error']}")
        return "\n".join(lines)

    lines.append("😀 FACE QUALITY SCORING")
    lines.append("=" * 50)
    lines.append(f"People identified:    {s['total_people']:,}")
    lines.append(f"Total face photos:    {s['total_faces']:,}")
    lines.append(f"Avg face quality:     {s['avg_face_quality']:.4f}")

    if s.get("highest_avg_person"):
        lines.append(f"Highest avg quality:  {s['highest_avg_person']}")
    if s.get("most_photographed"):
        lines.append(f"Most photographed:    {s['most_photographed']}")

    for person in data["people"][:10]:
        lines.append("")
        lines.append(f"👤 {person['name']}  ({person['total_faces']} faces, avg: {person['avg_quality']:.4f})")

        if person["best_photos"]:
            lines.append("   Best portraits:")
            for f in person["best_photos"][:3]:
                fav = "⭐" if f["is_favorite"] else "  "
                smile = f"  😊{f['smile_score']:.2f}" if f.get("smile_score") is not None else ""
                lines.append(f"   {fav} {display_name(f):35s} score={f['face_score']:.4f}{smile}")

        if person["worst_photos"]:
            lines.append("   Worst portraits:")
            for f in person["worst_photos"][:3]:
                blur_info = f"  blur={f['blur_score']:.2f}" if f.get("blur_score") is not None else ""
                lines.append(f"      {display_name(f):35s} score={f['face_score']:.4f}{blur_info}")

    return "\n".join(lines)


def main():
    def add_args(parser):
        parser.add_argument("--person", help="Filter to specific person name")
        parser.add_argument("--top", type=int, default=10, help="Top N best/worst per person (default: 10)")

    def invoke(db_path, args):
        return analyze_face_quality(
            db_path=db_path,
            person_name=args.person,
            top_n=args.top,
        )

    return run_script(
        description="Score face quality per person",
        analyze_fn=invoke,
        format_fn=format_summary,
        extra_args_fn=add_args,
    )


if __name__ == "__main__":
    sys.exit(main())
