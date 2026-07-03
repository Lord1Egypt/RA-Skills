#!/usr/bin/env python3
"""Meeting Cadence Optimizer: correlate meeting load with how days felt.

Reads back the user's "Evening Debrief" annotations (day_rating, meeting_count, cadence
feedback) and "Morning Check-In" annotations (energy), then computes the relationship
between meeting density and day quality. The math is done here -- deterministically -- so
the agent reports real numbers instead of inventing them.

  analyze --days 30
      Print the correlation analysis + a confidence level gated by how many debriefs
      exist. Read-only.

  save --days 30 [--dry-run]
      Run the analysis and also write it as a "Cadence Analysis" moment annotation.

Confidence gates (number of evening-debrief data points):
  <7  -> "insufficient"   (tell the user to keep using the daily routines)
  7-13 -> "low"
  14-29 -> "medium"
  30+  -> "high"

Auth: Fulcra via fulcra-api CLI / FULCRA_ACCESS_TOKEN. No tokens printed.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import concierge_bootstrap  # noqa: F401

import concierge_fulcra as cf  # noqa: E402
import fulcra_read  # noqa: E402

ANNOTATION_NAME = "Cadence Analysis"
ANNOTATION_DESC = "Meeting-cadence vs day-rating analysis from the concierge meeting-cadence-optimizer skill."
ANNOTATION_TAGS = ["cadence-analysis", "concierge"]
SOURCE = "com.fulcra.meeting-cadence-optimizer"


def _mean(xs: list[float]) -> float | None:
    return round(sum(xs) / len(xs), 2) if xs else None


def _confidence(n: int) -> str:
    if n < 7:
        return "insufficient"
    if n < 14:
        return "low"
    if n < 30:
        return "medium"
    return "high"


def analyze(days: float) -> dict[str, Any]:
    try:
        debriefs = fulcra_read.read_annotation_events("Evening Debrief", days=days)
    except Exception as exc:
        return {"ok": False, "error": f"could not read Evening Debrief annotations: {exc}"}

    points = []
    for ev in debriefs:
        d = ev.get("data")
        if not isinstance(d, dict):
            continue
        mc = d.get("meeting_count")
        dr = d.get("day_rating")
        if isinstance(mc, (int, float)) and isinstance(dr, (int, float)):
            points.append({"date": d.get("date") or (ev.get("recorded_at") or "")[:10],
                           "meeting_count": int(mc), "day_rating": float(dr),
                           "cadence_feedback": d.get("meeting_cadence_feedback")})

    n = len(points)
    confidence = _confidence(n)
    result: dict[str, Any] = {
        "ok": True,
        "analysis_period_days": days,
        "data_points": n,
        "confidence": confidence,
    }
    if n == 0:
        result["message"] = ("No evening debriefs with meeting_count + day_rating yet. "
                             "Keep doing the evening debrief and this will fill in.")
        return result

    ratings_by_count: dict[int, list[float]] = defaultdict(list)
    for p in points:
        ratings_by_count[p["meeting_count"]].append(p["day_rating"])
    day_rating_by_meeting_count = {str(k): _mean(v) for k, v in sorted(ratings_by_count.items())}

    # Best-rated meeting count (the "sweet spot"), among counts with >=1 sample.
    sweet_spot = max(day_rating_by_meeting_count.items(),
                     key=lambda kv: (kv[1] if kv[1] is not None else -1))[0]

    avg_meeting_count = _mean([p["meeting_count"] for p in points])
    avg_day_rating = _mean([p["day_rating"] for p in points])

    # Pearson correlation between meeting_count and day_rating (None if degenerate).
    corr = None
    if n >= 3:
        xs = [p["meeting_count"] for p in points]
        ys = [p["day_rating"] for p in points]
        mx, my = sum(xs) / n, sum(ys) / n
        sxx = sum((x - mx) ** 2 for x in xs)
        syy = sum((y - my) ** 2 for y in ys)
        sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        if sxx > 0 and syy > 0:
            corr = round(sxy / (sxx ** 0.5 * syy ** 0.5), 2)

    result.update({
        "avg_meeting_count": avg_meeting_count,
        "avg_day_rating": avg_day_rating,
        "day_rating_by_meeting_count": day_rating_by_meeting_count,
        "best_rated_meeting_count": int(sweet_spot),
        "meeting_count_vs_rating_correlation": corr,
        "too_many_feedback_count": sum(1 for p in points if p.get("cadence_feedback") == "too many"),
    })
    return result


def cmd_analyze(args: argparse.Namespace) -> dict:
    return analyze(args.days)


def cmd_save(args: argparse.Namespace) -> dict:
    analysis = analyze(args.days)
    if not analysis.get("ok"):
        return analysis
    if analysis.get("data_points", 0) == 0 and not args.dry_run:
        # Nothing meaningful to record yet; don't create an empty annotation.
        return {"ok": True, "skipped_write": True, **analysis}
    payload = {k: v for k, v in analysis.items() if k != "ok"}
    res = cf.record_moment(
        name=ANNOTATION_NAME, description=ANNOTATION_DESC, tags=ANNOTATION_TAGS,
        payload=payload, source=SOURCE,
        recorded_at=datetime.now(timezone.utc).isoformat(), dry_run=args.dry_run,
    )
    return {"ok": res.get("ok", False), "analysis": analysis, "fulcra": res}


def main() -> int:
    p = argparse.ArgumentParser(description="Meeting Cadence Optimizer")
    sub = p.add_subparsers(dest="command", required=True)
    an = sub.add_parser("analyze")
    an.add_argument("--days", type=float, default=30)
    sv = sub.add_parser("save")
    sv.add_argument("--days", type=float, default=30)
    sv.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    if args.command == "analyze":
        result = cmd_analyze(args)
    elif args.command == "save":
        result = cmd_save(args)
    else:
        result = {"ok": False, "error": "unknown command"}
    print(json.dumps(result, indent=2, sort_keys=True, default=str))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
