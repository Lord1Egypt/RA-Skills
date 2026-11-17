#!/usr/bin/env python3
"""
Generate timeline recaps: narrative summaries of photo activity over time.
Groups photos by day/event clusters and includes context like people, locations, scenes.
"""

import argparse
import sys
from datetime import date, timedelta
from typing import Any

from _common import (
    ExitCode,
    PhotosDB,
    add_common_args,
    coredata_to_local,
    detect_face_schema,
    emit_result,
    format_date_range,
    format_degraded,
    handle_cli_error,
    has_timezone_offset,
    local_datetime_sql,
    setup_logging,
    tz_offset_sql,
)
from _scenes import SEARCH_INDEX, IndexLabels, scene_source, search_index_available
from _schema import FACES, SCENES, Degradation, get_schema

# Schema contract (T1.4): see _schema. Missing required → exit 5; missing optional → `degraded`.
REQUIRED_COLUMNS: tuple[str, ...] = (
    "ZASSET.ZDATECREATED",
    "ZASSET.ZFAVORITE",
    "ZASSET.ZFILENAME",
    "ZASSET.ZKIND",
    "ZASSET.ZLATITUDE",
    "ZASSET.ZLONGITUDE",
    "ZASSET.ZTRASHEDSTATE",
    "ZADDITIONALASSETATTRIBUTES.ZASSET",
)
OPTIONAL_COLUMNS: dict[str, tuple[str, ...]] = {
    "people": FACES,
    "scenes": SCENES,
}
# A section whose columns are missing is still available when this source exists (doctor uses it).
ALTERNATE_SOURCES = {"scenes": search_index_available}


def generate_timeline(
    db_path: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    cluster_hours: int = 4,
) -> dict[str, Any]:
    """
    Generate a timeline recap for a date range.

    Args:
        db_path: Path to database
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        cluster_hours: Hours gap to consider photos part of same event

    Returns:
        Timeline dictionary
    """
    with PhotosDB(db_path, require=REQUIRED_COLUMNS, operation="Timeline recap") as conn:
        cursor = conn.cursor()
        schema = detect_face_schema(cursor)
        degraded = Degradation(get_schema(conn))
        has_faces = degraded.check("people", *OPTIONAL_COLUMNS["people"])
        # Scene names come from ZSCENECLASSIFICATION or, on macOS 26, Photos' search index (see _scenes).
        scenes_from = scene_source(conn)
        index_labels = IndexLabels(conn)  # filled in bulk below, only if the index is the source
        has_scenes = scenes_from is not None
        if scenes_from is None:
            degraded.check("scenes", *OPTIONAL_COLUMNS["scenes"])
        tz_available = has_timezone_offset(cursor)
        local_dt = local_datetime_sql(tz_available)

        # Date filters compare local capture time as text ("YYYY-MM-DD HH:MM:SS")
        where_clauses = ["a.ZTRASHEDSTATE != 1"]
        params: list = []

        if start_date:
            where_clauses.append(f"{local_dt} >= ?")
            params.append(f"{date.fromisoformat(start_date).isoformat()} 00:00:00")

        if end_date:
            where_clauses.append(f"{local_dt} <= ?")
            params.append(f"{date.fromisoformat(end_date).isoformat()} 23:59:59")

        # Get photos with metadata
        query = f"""
            SELECT
                a.Z_PK,
                a.ZFILENAME,
                a.ZDATECREATED,
                a.ZKIND,
                a.ZLATITUDE,
                a.ZLONGITUDE,
                a.ZFAVORITE,
                {tz_offset_sql(tz_available)} AS tz_offset
            FROM ZASSET a
            LEFT JOIN ZADDITIONALASSETATTRIBUTES aa ON a.Z_PK = aa.ZASSET
            WHERE {" AND ".join(where_clauses)}
            ORDER BY a.ZDATECREATED
        """

        cursor.execute(query, params)
        photos = []

        for row in cursor.fetchall():
            created = coredata_to_local(row["ZDATECREATED"], row["tz_offset"])
            if created:
                photos.append(
                    {
                        "id": row["Z_PK"],
                        "filename": row["ZFILENAME"],
                        "created": created,
                        "kind": "photo" if row["ZKIND"] == 0 else "video",
                        "latitude": row["ZLATITUDE"],
                        "longitude": row["ZLONGITUDE"],
                        "is_favorite": bool(row["ZFAVORITE"]),
                    }
                )

        # SQL orders by UTC; photos from different time zones can be out of order in local time
        photos.sort(key=lambda p: p["created"])

        if not photos:
            return {
                "degraded": degraded.entries,
                "timeline": [],
                "summary": {
                    "total_photos": 0,
                    "total_days": 0,
                    "total_events": 0,
                    "date_range": "Unknown",
                },
            }

        # Cluster photos into events
        events = []
        current_event = None
        cluster_delta = timedelta(hours=cluster_hours)

        for photo in photos:
            if current_event is None:
                # Start new event
                current_event = {
                    "start_time": photo["created"],
                    "end_time": photo["created"],
                    "photos": [photo],
                }
            else:
                # Check if photo belongs to current event
                time_gap = photo["created"] - current_event["end_time"]

                if time_gap <= cluster_delta:
                    # Add to current event
                    current_event["end_time"] = photo["created"]
                    current_event["photos"].append(photo)
                else:
                    # Close current event and start new one
                    events.append(current_event)
                    current_event = {
                        "start_time": photo["created"],
                        "end_time": photo["created"],
                        "photos": [photo],
                    }

        # Add last event
        if current_event:
            events.append(current_event)

        # Enrich events with additional data
        if scenes_from == SEARCH_INDEX:  # one batch for every photo in the timeline
            index_labels.preload(p["id"] for event in events for p in event["photos"])
        for event in events:
            photo_ids = [p["id"] for p in event["photos"]]
            event["photo_count"] = len(photo_ids)
            event["video_count"] = sum(1 for p in event["photos"] if p["kind"] == "video")
            event["favorites"] = sum(1 for p in event["photos"] if p["is_favorite"])

            placeholders = ",".join("?" * len(photo_ids))

            # Get people in this event (None when this library has no face data)
            if photo_ids and has_faces:
                cursor.execute(
                    f"""
                    SELECT DISTINCT p.ZFULLNAME, COUNT(df.{schema["asset_fk"]}) as count
                    FROM ZPERSON p
                    JOIN ZDETECTEDFACE df ON p.Z_PK = df.{schema["person_fk"]}
                    WHERE df.{schema["asset_fk"]} IN ({placeholders})
                    GROUP BY p.Z_PK
                    ORDER BY count DESC
                """,
                    photo_ids,
                )

                event["people"] = [{"name": row["ZFULLNAME"], "count": row["count"]} for row in cursor.fetchall()]
            else:
                event["people"] = [] if has_faces else None

            # Get scene classifications (None when this library has none)
            if photo_ids and scenes_from == SEARCH_INDEX:
                event["scenes"] = index_labels.top(photo_ids)
            elif photo_ids and has_scenes:
                cursor.execute(
                    f"""
                    SELECT DISTINCT sc.ZSCENENAME, COUNT(*) as count
                    FROM ZSCENECLASSIFICATION sc
                    WHERE sc.ZASSET IN ({placeholders})
                    GROUP BY sc.ZSCENENAME
                    ORDER BY count DESC
                    LIMIT 5
                """,
                    photo_ids,
                )

                event["scenes"] = [
                    {"scene": row["ZSCENENAME"], "count": row["count"]}
                    for row in cursor.fetchall()
                    if row["ZSCENENAME"]
                ]
            else:
                event["scenes"] = [] if has_scenes else None

            # Location summary
            locations = [(p["latitude"], p["longitude"]) for p in event["photos"] if p["latitude"] and p["longitude"]]

            if locations:
                avg_lat = sum(loc[0] for loc in locations) / len(locations)
                avg_lon = sum(loc[1] for loc in locations) / len(locations)
                event["location"] = {
                    "latitude": round(avg_lat, 4),
                    "longitude": round(avg_lon, 4),
                    "has_location": True,
                }
            else:
                event["location"] = {"has_location": False}

        # Group events by day
        timeline = []
        current_day: date | None = None
        day_events: list[dict[str, Any]] = []

        for event in events:
            event_date = event["start_time"].date()

            if current_day is None or event_date != current_day:
                # Save previous day
                if current_day is not None and day_events:
                    timeline.append(
                        {
                            "date": current_day.isoformat(),
                            "day_name": current_day.strftime("%A"),
                            "events": day_events,
                            "total_photos": sum(e["photo_count"] for e in day_events),
                        }
                    )

                # Start new day
                current_day = event_date
                day_events = [format_event(event)]
            else:
                # Add to current day
                day_events.append(format_event(event))

        # Add last day
        if current_day is not None and day_events:
            timeline.append(
                {
                    "date": current_day.isoformat(),
                    "day_name": current_day.strftime("%A"),
                    "events": day_events,
                    "total_photos": sum(e["photo_count"] for e in day_events),
                }
            )

        # Summary
        total_photos = sum(day["total_photos"] for day in timeline)

        return {
            "degraded": degraded.entries,
            "timeline": timeline,
            "summary": {
                "total_photos": total_photos,
                "total_days": len(timeline),
                "total_events": len(events),
                "date_range": format_date_range(
                    photos[0]["created"] if photos else None, photos[-1]["created"] if photos else None
                ),
            },
        }


def format_event(event: dict[str, Any]) -> dict[str, Any]:
    """Format event for output."""
    return {
        "time": event["start_time"].strftime("%H:%M"),
        "duration_minutes": int((event["end_time"] - event["start_time"]).total_seconds() / 60),
        "photo_count": event["photo_count"],
        "video_count": event["video_count"],
        "favorites": event["favorites"],
        "people": event["people"],
        "scenes": event["scenes"],
        "location": event["location"],
    }


def format_narrative(timeline_data: dict[str, Any]) -> str:
    """Format timeline as narrative text suitable for AI narration."""
    lines = []
    lines.append("📅 PHOTO TIMELINE RECAP")
    lines.append("=" * 50)
    lines.append("")

    summary = timeline_data["summary"]
    lines.append(f"Period: {summary['date_range']}")
    lines.append(f"Total: {summary['total_photos']} photos across {summary['total_days']} days")
    lines.append(f"Events: {summary['total_events']}")
    lines.append("")

    for day in timeline_data["timeline"]:
        lines.append(f"📆 {day['date']} ({day['day_name']}) - {day['total_photos']} photos")

        for event in day["events"]:
            duration = f"{event['duration_minutes']}m" if event["duration_minutes"] > 0 else "instant"
            lines.append(f"  🕐 {event['time']} ({duration})")
            lines.append(f"     {event['photo_count']} photos")

            if event["video_count"] > 0:
                lines[-1] += f", {event['video_count']} videos"
            if event["favorites"] > 0:
                lines[-1] += f" ⭐ {event['favorites']} favorites"
            lines.append("")

            if event["people"]:
                people_str = ", ".join(p["name"] for p in event["people"][:3])
                lines.append(f"     👥 {people_str}")

            if event["scenes"]:
                scenes_str = ", ".join(s["scene"] for s in event["scenes"][:3])
                lines.append(f"     🏷️  {scenes_str}")

            if event["location"]["has_location"]:
                loc = event["location"]
                lines.append(f"     📍 {loc['latitude']}, {loc['longitude']}")

            lines.append("")

        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate photo timeline recap",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Last week
  %(prog)s --start-date 2025-03-01 --end-date 2025-03-07

  # Last month
  %(prog)s --start-date 2025-02-01 --end-date 2025-02-28

  # Custom clustering (8-hour gaps = same event)
  %(prog)s --start-date 2025-03-01 --cluster-hours 8 --narrative
        """,
    )
    add_common_args(parser, human_aliases=("--human", "--narrative"))
    parser.add_argument("--start-date", help="Start date (YYYY-MM-DD, local capture time)")
    parser.add_argument("--end-date", help="End date (YYYY-MM-DD, local capture time, inclusive)")
    parser.add_argument(
        "--cluster-hours", type=int, default=4, help="Hours between photos to consider separate events (default: 4)"
    )

    args = parser.parse_args()
    setup_logging(verbose=args.verbose, quiet=args.quiet)

    try:
        db_path = args.db_path or args.library

        timeline = generate_timeline(
            db_path=db_path,
            start_date=args.start_date,
            end_date=args.end_date,
            cluster_hours=args.cluster_hours,
        )

        if args.format == "human":
            output_text = format_narrative(timeline) + format_degraded(timeline)
            if args.output:
                with open(args.output, "w") as f:
                    f.write(output_text)
                if not args.quiet:
                    print(f"Written to: {args.output}", file=sys.stderr)
            else:
                print(output_text)
        else:
            emit_result(timeline, args)

            if not args.output and not args.quiet:
                print("\n" + (format_narrative(timeline) + format_degraded(timeline)), file=sys.stderr)

        return 0

    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        return ExitCode.USER_ABORTED
    except Exception as e:
        return handle_cli_error(e)


if __name__ == "__main__":
    sys.exit(main())
