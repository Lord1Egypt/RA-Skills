from __future__ import annotations

from collections import Counter
from typing import Any


def summarize_sport_label(sport: str) -> str:
    s = sport.lower()
    if "run" in s:
        return "run"
    if "ride" in s or "cycle" in s:
        return "ride"
    if "tennis" in s:
        return "tennis"
    if "weight" in s:
        return "weight training"
    return s


def sanitize_activity_name(name: str, max_len: int = 80) -> str:
    text = name.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    text = "".join(ch for ch in text if ch.isprintable())
    text = " ".join(text.split())
    if len(text) > max_len:
        text = text[: max_len - 1].rstrip() + "…"
    return text


def _recent_state_hints(recent_state: dict[str, Any] | None) -> tuple[list[str], list[str], list[str], list[str], list[dict[str, Any]]]:
    recent = (recent_state or {}).get("recent", [])
    recent_sports: list[str] = []
    recent_families: list[str] = []
    recent_openings: list[str] = []
    recent_targets: list[str] = []
    recent_days: list[dict[str, Any]] = []

    for item in recent:
        if not isinstance(item, dict):
            continue
        sports = item.get("sports", [])
        if isinstance(sports, list):
            recent_sports.extend([summarize_sport_label(v) for v in sports if isinstance(v, str)])
        family = item.get("joke_family") or item.get("family")
        if isinstance(family, str) and family:
            recent_families.append(family)
        opening = item.get("opening_style")
        if isinstance(opening, str) and opening:
            recent_openings.append(opening)
        targets = item.get("joke_targets", [])
        if isinstance(targets, list):
            recent_targets.extend([v for v in targets if isinstance(v, str)])

        day_record = {
            "date": item.get("date"),
            "sports": [summarize_sport_label(v) for v in sports if isinstance(v, str)] if isinstance(sports, list) else [],
            "count": int(item.get("count", 0) or 0),
            "distance_km": float(item.get("distance_km", 0) or 0),
            "moving_minutes": int(item.get("moving_minutes", 0) or 0),
            "elevation_m": int(item.get("elevation_m", 0) or 0),
            "activity_names": [sanitize_activity_name(v) for v in item.get("activity_names", []) if isinstance(v, str)],
            "dominant_sport": summarize_sport_label(item.get("dominant_sport")) if isinstance(item.get("dominant_sport"), str) else None,
        }
        recent_days.append(day_record)

    return recent_sports, recent_families[-3:], recent_openings[-3:], recent_targets[-5:], recent_days[-7:]


def _consecutive_same_sport_days(current_sports: list[str], recent_days: list[dict[str, Any]]) -> int:
    if not current_sports:
        return 0
    wanted = set(current_sports)
    streak = 0
    for day in reversed(recent_days):
        sports = set(day.get("sports", []))
        if not sports:
            break
        if sports & wanted:
            streak += 1
        else:
            break
    return streak


def _recent_load_summary(day: dict[str, Any], recent_days: list[dict[str, Any]]) -> dict[str, Any]:
    current_distance = float(day.get("total_km", 0) or 0)
    current_minutes = int(day.get("total_min", 0) or 0)
    current_elev = int(day.get("total_elev", 0) or 0)

    if not recent_days:
        return {
            "days_considered": 0,
            "avg_distance_km": 0.0,
            "avg_moving_minutes": 0,
            "avg_elevation_m": 0,
            "distance_vs_recent": "no_recent_context",
            "minutes_vs_recent": "no_recent_context",
            "elevation_vs_recent": "no_recent_context",
        }

    n = len(recent_days)
    avg_distance = round(sum(float(d.get("distance_km", 0) or 0) for d in recent_days) / n, 2)
    avg_minutes = round(sum(int(d.get("moving_minutes", 0) or 0) for d in recent_days) / n)
    avg_elev = round(sum(int(d.get("elevation_m", 0) or 0) for d in recent_days) / n)

    def compare(current: float, avg: float) -> str:
        if avg <= 0:
            return "no_recent_context"
        if current >= avg * 1.35:
            return "well_above_recent"
        if current >= avg * 1.1:
            return "above_recent"
        if current <= avg * 0.65:
            return "well_below_recent"
        if current <= avg * 0.9:
            return "below_recent"
        return "near_recent"

    return {
        "days_considered": n,
        "avg_distance_km": avg_distance,
        "avg_moving_minutes": avg_minutes,
        "avg_elevation_m": avg_elev,
        "distance_vs_recent": compare(current_distance, avg_distance),
        "minutes_vs_recent": compare(current_minutes, avg_minutes),
        "elevation_vs_recent": compare(current_elev, avg_elev),
    }


def build_roast_context(day: dict[str, Any], tone: str, spice: int, recent_state: dict[str, Any] | None = None) -> dict[str, Any]:
    summaries = day.get("summaries", [])
    sport_labels = [summarize_sport_label(s.get("sport", "activity")) for s in summaries]
    counts = Counter(sport_labels)
    dominant_sport = counts.most_common(1)[0][0] if counts else None
    recent_sports, recent_families, recent_openings, recent_targets, recent_days = _recent_state_hints(recent_state)
    consecutive_days = _consecutive_same_sport_days(sport_labels, recent_days)
    load_summary = _recent_load_summary(day, recent_days)

    return {
        "date": day.get("date"),
        "activity_count": day.get("count", 0),
        "sports": sport_labels,
        "dominant_sport": dominant_sport,
        "activity_names": [sanitize_activity_name(s.get("name")) for s in summaries if s.get("name")],
        "totals": {
            "distance_km": day.get("total_km", 0),
            "moving_minutes": day.get("total_min", 0),
            "elevation_m": day.get("total_elev", 0),
            "kudos": day.get("total_kudos", 0),
        },
        "effort": {
            "avg_hr": next((s.get("avg_hr") for s in summaries if s.get("avg_hr") is not None), None),
            "max_hr": next((s.get("max_hr") for s in summaries if s.get("max_hr") is not None), None),
        },
        "pattern_hints": {
            "indoor_count": day.get("indoor_count", 0),
            "repeat_sport_recently": any(s in recent_sports for s in sport_labels),
            "consecutive_same_sport_days": consecutive_days,
            "recent_load": load_summary,
        },
        "recent_activity_context": {
            "days_considered": len(recent_days),
            "recent_days": recent_days,
            "last_day": recent_days[-1] if recent_days else None,
        },
        "roast_memory": {
            "recent_families": recent_families,
            "recent_openings": recent_openings,
            "recent_targets": recent_targets,
        },
        "style": {
            "tone": tone,
            "spice": spice,
            "target": "one short paragraph",
            "voice": "funny, dry, slightly mean but not cruel",
        },
    }
