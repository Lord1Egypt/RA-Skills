#!/usr/bin/env python3
"""Errand Router — optimal order for multi-stop errand runs.

Solves a small Traveling Salesperson Problem with Time Windows (TSPTW):
- distance matrix via haversine (lat/lon) or Euclidean (local x/y)
- road factor 1.3 on straight-line distance
- travel time from configurable speed (default 30 km/h city)
- nearest-feasible-neighbor construction + 2-opt improvement
- full clock simulation: drive -> wait-for-open -> dwell -> drive ...
- flags stops that would be reached after closing

Stdlib only. Python 3.9+.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from typing import Optional, List

EARTH_RADIUS_KM = 6371.0
ROAD_FACTOR = 1.3
DEFAULT_SPEED_KMH = 30.0


# ---------------------------------------------------------------------------
# Data model


@dataclass
class Stop:
    name: str
    lat: Optional[float] = None
    lon: Optional[float] = None
    x: Optional[float] = None
    y: Optional[float] = None
    dwell_min: int = 10
    open_min: Optional[int] = None   # minutes from midnight; None = always open
    close_min: Optional[int] = None


@dataclass
class Problem:
    start: Stop
    stops: List[Stop]      # excluding start
    depart_min: int
    speed_kmh: float = DEFAULT_SPEED_KMH
    end_name: Optional[str] = None  # if set, route returns to this point


# ---------------------------------------------------------------------------
# Time helpers


def parse_hhmm(s):
    if s is None:
        return None
    h, m = s.strip().split(":")
    return int(h) * 60 + int(m)


def fmt_hhmm(mins):
    mins = int(round(mins))
    return f"{mins // 60:02d}:{mins % 60:02d}"


# ---------------------------------------------------------------------------
# Distance


def haversine_km(lat1, lon1, lat2, lon2):
    p1, l1, p2, l2 = map(math.radians, (lat1, lon1, lat2, lon2))
    a = (math.sin((p2 - p1) / 2) ** 2
         + math.cos(p1) * math.cos(p2) * math.sin((l2 - l1) / 2) ** 2)
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


def dist_km(a: Stop, b: Stop) -> float:
    if a.lat is not None and a.lon is not None and b.lat is not None and b.lon is not None:
        return haversine_km(a.lat, a.lon, b.lat, b.lon) * ROAD_FACTOR
    if a.x is not None and a.y is not None and b.x is not None and b.y is not None:
        return math.hypot(a.x - b.x, a.y - b.y) * ROAD_FACTOR  # type: ignore[union-attr]
    raise ValueError(f"mixed coordinate systems between '{a.name}' and '{b.name}'")


def drive_minutes(a: Stop, b: Stop, speed_kmh: float) -> float:
    return dist_km(a, b) / speed_kmh * 60.0


# ---------------------------------------------------------------------------
# Clock simulation


def simulate(problem: Problem, order) -> dict:
    """Simulate the clock over an ordered visit list (start first)."""
    t = problem.depart_min
    legs, violations = [], []
    total_km = total_drive = total_dwell = total_wait = 0.0

    for i in range(1, len(order)):
        prev, cur = order[i - 1], order[i]
        km = dist_km(prev, cur)
        drive = km / problem.speed_kmh * 60.0
        arrival = t + drive
        service = arrival
        wait = 0
        if cur.open_min is not None and arrival < cur.open_min:
            wait = cur.open_min - arrival
            service = cur.open_min
        depart = service + cur.dwell_min
        if cur.close_min is not None and service + cur.dwell_min > cur.close_min:
            violations.append({
                "stop": cur.name,
                "arrive": fmt_hhmm(arrival),
                "closes": fmt_hhmm(cur.close_min),
                "miss_by_min": int(service + cur.dwell_min - cur.close_min),
            })
        legs.append({
            "from": prev.name, "to": cur.name,
            "km": round(km, 2), "drive_min": round(drive, 1),
            "arrival": fmt_hhmm(arrival),
            "wait_min": round(wait, 1),
            "service_start": fmt_hhmm(service),
            "departure": fmt_hhmm(depart),
            "dwell_min": cur.dwell_min,
        })
        total_km += km
        total_drive += drive
        total_dwell += cur.dwell_min
        total_wait += wait
        t = depart

    return {
        "order": [s.name for s in order],
        "legs": legs,
        "violations": violations,
        "totals": {
            "km": round(total_km, 2),
            "drive_min": round(total_drive, 1),
            "dwell_min": int(total_dwell),
            "wait_min": round(total_wait, 1),
            "elapsed_min": round(total_drive + total_dwell + total_wait, 1),
            "finish": fmt_hhmm(problem.depart_min + total_drive + total_dwell + total_wait),
        },
    }


# ---------------------------------------------------------------------------
# Solver: nearest feasible neighbor + time-window-aware 2-opt


def walk_clock(problem: Problem, route):
    """Advance the clock through the route. Returns (finish_time, n_violations)."""
    t = problem.depart_min
    violations = 0
    for i in range(1, len(route)):
        cur = route[i]
        t += drive_minutes(route[i - 1], cur, problem.speed_kmh)
        if cur.open_min is not None and t < cur.open_min:
            t = cur.open_min
        if cur.close_min is not None and t + cur.dwell_min > cur.close_min:
            violations += 1
        t += cur.dwell_min
    return t, violations


def solve(problem: Problem) -> list:
    # --- construction: nearest feasible neighbor
    unvisited = list(problem.stops)
    route = [problem.start]
    t = problem.depart_min

    while unvisited:
        current = route[-1]
        feasible = []
        for cand in unvisited:
            arrival = t + drive_minutes(current, cand, problem.speed_kmh)
            service = max(arrival, cand.open_min if cand.open_min is not None else arrival)
            if cand.close_min is None or service + cand.dwell_min <= cand.close_min:
                feasible.append(cand)
        pool = feasible or unvisited   # if nothing feasible, take nearest anyway (flagged later)
        best = min(pool, key=lambda c: drive_minutes(current, c, problem.speed_kmh))
        route.append(best)
        unvisited.remove(best)
        arrival = t + drive_minutes(current, best, problem.speed_kmh)
        service = max(arrival, best.open_min if best.open_min is not None else arrival)
        t = service + best.dwell_min

    # --- return leg
    if problem.end_name is not None:
        route.append(problem.start if problem.end_name == problem.start.name
                     else _find(problem, problem.end_name))

    # --- improvement: 2-opt (accept strictly better: fewer violations, then time)
    improved = True
    while improved:
        improved = False
        base_finish, base_viol = walk_clock(problem, route)
        for i in range(1, len(route) - 1):
            for j in range(i + 1, len(route) - 1 if problem.end_name is None else len(route) - 1):
                if j <= i:
                    continue
                candidate = route[:i] + route[i:j + 1][::-1] + route[j + 1:]
                cand_finish, cand_viol = walk_clock(problem, candidate)
                better = (cand_viol, cand_finish) < (base_viol, base_finish)
                if better:
                    route = candidate
                    base_finish, base_viol = cand_finish, cand_viol
                    improved = True
    return route


def _find(problem: Problem, name: str) -> Stop:
    for s in [problem.start] + problem.stops:
        if s.name == name:
            return s
    raise ValueError(f"end name '{name}' not among stops")


# ---------------------------------------------------------------------------
# Parsing


def stop_from_dict(d: dict) -> Stop:
    return Stop(
        name=d["name"],
        lat=d.get("lat"), lon=d.get("lon"),
        x=d.get("x"), y=d.get("y"),
        dwell_min=int(d.get("dwell_min", d.get("dwell", 10))),
        open_min=parse_hhmm(d.get("open")),
        close_min=parse_hhmm(d.get("close")),
    )


def load_problem(path, end=None, depart_override=None, speed_override=None) -> Problem:
    with open(path) as f:
        data = json.load(f)
    start = stop_from_dict(data["start"])
    stops = [stop_from_dict(s) for s in data["stops"]]
    depart = parse_hhmm(depart_override or data.get("depart", "09:00"))
    speed = speed_override or data.get("speed_kmh", DEFAULT_SPEED_KMH)
    end_name = end if end is not None else data.get("end")
    return Problem(start, stops, depart, speed, end_name)


def parse_quick_stop(spec: str) -> Stop:
    """name,lat,lon[,dwell[,open,close]] — lat/lon mode only."""
    parts = [p.strip() for p in spec.split(",")]
    if len(parts) < 3:
        raise ValueError(f"bad stop spec '{spec}' — need name,lat,lon[,dwell[,open,close]]")
    name = parts[0]
    lat, lon = float(parts[1]), float(parts[2])
    dwell = int(parts[3]) if len(parts) > 3 else 10
    op = parts[4] if len(parts) > 4 else None
    cl = parts[5] if len(parts) > 5 else None
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        raise ValueError(f"bad lat/lon in '{spec}'")
    return Stop(name, lat=lat, lon=lon, dwell_min=dwell,
                open_min=parse_hhmm(op), close_min=parse_hhmm(cl))


# ---------------------------------------------------------------------------
# Reporting


def print_result(res: dict) -> None:
    print("=" * 62)
    print("ERRAND ROUTER — optimized visit order")
    print("=" * 62)
    print("ORDER : " + " → ".join(res["order"]))
    print("-" * 62)
    for leg in res["legs"]:
        wait = f" (wait {leg['wait_min']:.0f}m)" if leg["wait_min"] >= 1 else ""
        print(f"  {leg['from']:<14} → {leg['to']:<14} "
              f"{leg['km']:>6.2f} km  drive {leg['drive_min']:>5.1f}m  "
              f"arr {leg['arrival']}, in {leg['dwell_min']}m{wait}, "
              f"dep {leg['departure']}")
    print("-" * 62)
    t = res["totals"]
    print(f"TOTAL: {t['km']:.2f} km · {t['elapsed_min']:.0f} min "
          f"(drive {t['drive_min']:.0f} + dwell {t['dwell_min']} + wait {t['wait_min']:.0f})")
    print(f"FINISH: {t['finish']}")
    if res["violations"]:
        print("\n🚨 TIME-WINDOW VIOLATIONS")
        for v in res["violations"]:
            print(f"  {v['stop']}: arrive {v['arrive']}, closes {v['closes']} "
                  f"(miss by {v['miss_by_min']} min) — leave earlier or drop/reorder")
    else:
        print("✅ all stops reachable within opening hours")
    print("=" * 62)


# ---------------------------------------------------------------------------
# CLI


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Optimal errand run order (TSPTW)")
    sub = p.add_subparsers(dest="cmd", required=True)

    plan_p = sub.add_parser("plan", help="plan from a JSON problem file")
    plan_p.add_argument("file")
    plan_p.add_argument("--end", help="force end point name (default: return to start)")
    plan_p.add_argument("--depart", help="override departure time HH:MM")
    plan_p.add_argument("--speed", type=float, help="override speed km/h")
    plan_p.add_argument("--json", action="store_true")

    quick_p = sub.add_parser("quick", help="plan from CLI flags (lat/lon mode)")
    quick_p.add_argument("--start", required=True, help="name,lat,lon[,dwell]")
    quick_p.add_argument("--stop", action="append", required=True,
                         help="name,lat,lon[,dwell[,open,close]]")
    quick_p.add_argument("--depart", default="09:00")
    quick_p.add_argument("--speed", type=float, default=DEFAULT_SPEED_KMH)
    quick_p.add_argument("--no-return", action="store_true",
                         help="do not add the return-to-start leg")
    quick_p.add_argument("--json", action="store_true")

    args = p.parse_args(argv)

    if args.cmd == "plan":
        problem = load_problem(args.file, end=args.end, depart_override=args.depart,
                               speed_override=args.speed)
    else:
        sparts = [s.strip() for s in args.start.split(",")]
        start = Stop(sparts[0], lat=float(sparts[1]), lon=float(sparts[2]),
                     dwell_min=int(sparts[3]) if len(sparts) > 3 else 0)
        stops = [parse_quick_stop(s) for s in args.stop]
        end_name = None if args.no_return else start.name
        problem = Problem(start, stops, parse_hhmm(args.depart), args.speed, end_name)

    route = solve(problem)
    res = simulate(problem, route)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print_result(res)
    return 0 if not res["violations"] else 1


if __name__ == "__main__":
    sys.exit(main())
