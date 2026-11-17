#!/usr/bin/env python3
"""car_maintenance.py — vehicle maintenance scheduler and 24-month timeline.

Computes what maintenance is OVERDUE / DUE SOON / OK for a vehicle using
dual intervals (every N km OR M months, whichever comes first — the way
real manufacturer schedules work), with severe-service adjustment,
next-due projections from annual mileage, cost ranges, and DIY difficulty.

Deterministic, stdlib-only, no network. Generic defaults — ALWAYS defer to
the owner's manual for your specific vehicle.

Usage:
    python3 scripts/car_maintenance.py tasks [--json]
    python3 scripts/car_maintenance.py status --km 84500 \
        --in-service 2021-03-10 \
        [--annual-km 18000] [--severe] \
        [--history '[{"task":"oil","km":63000,"date":"2026-01-15"}]'] \
        [--json]
    python3 scripts/car_maintenance.py timeline --km 84500 \
        --in-service 2021-03-10 [same options] [--json]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from typing import Any, Optional

__version__ = "1.0.0"

# ----------------------------------------------------------------------------
# Task library
# ----------------------------------------------------------------------------
# priority: "safety-critical" | "wear-item" | "standard"
# severe_km / severe_mo: explicit severe-service intervals; when --severe is
# set and no explicit values exist, SEVERE_GLOBAL_MULT is applied instead.
# km_repeat / mo_repeat: interval used after the FIRST service (coolant).
# cost_low/cost_high: typical indie-shop range, USD, parts + labor.
# diy: Easy | Moderate | Hard (typical home-mechanic difficulty).

SEVERE_GLOBAL_MULT = 0.75
DUE_SOON_KM_FRACTION = 0.20   # due soon when <= 20% of the km interval remains
DUE_SOON_DAYS = 30            # ... or <= 30 days remain on the time interval
TIMELINE_MONTHS = 24

TASK_LIBRARY: list[dict[str, Any]] = [
    {
        "id": "oil", "name": "Engine oil & filter change",
        "km": 10_000, "mo": 12, "severe_km": 5_000, "severe_mo": 6,
        "priority": "wear-item", "cost": (40, 90), "diy": "Easy",
        "notes": "The single most important service; severe = short trips, city, towing, dust.",
    },
    {
        "id": "tire_rotation", "name": "Tire rotation",
        "km": 8_000, "mo": 6,
        "priority": "safety-critical", "cost": (20, 50), "diy": "Easy",
        "notes": "Even tread wear; many shops do it free with oil changes.",
    },
    {
        "id": "engine_air_filter", "name": "Engine air filter",
        "km": 20_000, "mo": 24,
        "priority": "wear-item", "cost": (15, 40), "diy": "Easy",
        "notes": "Dusty conditions halve this; check at every oil change.",
    },
    {
        "id": "cabin_filter", "name": "Cabin (pollen) filter",
        "km": 20_000, "mo": 24,
        "priority": "standard", "cost": (20, 60), "diy": "Easy",
        "notes": "Affects HVAC flow and air quality, not engine health.",
    },
    {
        "id": "brake_fluid", "name": "Brake fluid replacement",
        "km": 40_000, "mo": 24,
        "priority": "safety-critical", "cost": (80, 150), "diy": "Moderate",
        "notes": "Hygroscopic fluid degrades boiling point; often missed for years.",
    },
    {
        "id": "spark_plugs", "name": "Spark plugs",
        "km": 60_000, "mo": 48,
        "priority": "wear-item", "cost": (100, 250), "diy": "Moderate",
        "notes": "Iridium plugs often 100k km; check manual before paying early.",
    },
    {
        "id": "coolant", "name": "Engine coolant replacement",
        "km": 100_000, "mo": 60, "km_repeat": 50_000, "mo_repeat": 36,
        "priority": "wear-item", "cost": (90, 180), "diy": "Moderate",
        "notes": "Long-life first fill, then shorter repeat intervals.",
    },
    {
        "id": "transmission_fluid", "name": "Transmission fluid replacement",
        "km": 100_000, "mo": 120, "severe_km": 60_000, "severe_mo": 72,
        "priority": "wear-item", "cost": (150, 350), "diy": "Hard",
        "notes": "Severe service (towing, city heat) roughly halves the interval.",
    },
    {
        "id": "drive_belt", "name": "Drive/serpentine belt inspection",
        "km": 100_000, "mo": 120,
        "priority": "wear-item", "cost": (0, 120), "diy": "Moderate",
        "notes": "Inspect at 100k km; replace only on cracks/glazing (cost shown is replacement).",
    },
    {
        "id": "battery_test", "name": "Battery load test (replace ~60 mo)",
        "km": None, "mo": 48,
        "priority": "wear-item", "cost": (0, 30), "diy": "Easy",
        "notes": "Free tests at most parts stores; average replacement life ~5 years.",
    },
    {
        "id": "wipers", "name": "Wiper blades",
        "km": None, "mo": 12,
        "priority": "safety-critical", "cost": (15, 50), "diy": "Easy",
        "notes": "Visibility item — replace at first streaking, at latest yearly.",
    },
    {
        "id": "inspection", "name": "Annual inspection / MOT",
        "km": None, "mo": 12,
        "priority": "safety-critical", "cost": (30, 120), "diy": "Easy",
        "notes": "Legally required in many regions; date-based only.",
    },
    {
        "id": "tire_swap", "name": "Winter/summer tire swap",
        "km": None, "mo": 6,
        "priority": "standard", "cost": (40, 100), "diy": "Moderate",
        "notes": "Seasonal, climate-dependent; date-based only.",
    },
]

TASKS_BY_ID: dict[str, dict[str, Any]] = {t["id"]: t for t in TASK_LIBRARY}

# Accept common alternative spellings in --history entries.
ALIASES: dict[str, str] = {
    "oil_change": "oil", "oilchange": "oil", "engine_oil": "oil",
    "rotation": "tire_rotation", "tires_rotation": "tire_rotation",
    "air_filter": "engine_air_filter", "engine_filter": "engine_air_filter",
    "cabin_air_filter": "cabin_filter", "pollen_filter": "cabin_filter",
    "brakes_fluid": "brake_fluid", "brakefluid": "brake_fluid",
    "plugs": "spark_plugs", "sparkplugs": "spark_plugs",
    "antifreeze": "coolant", "radiator_fluid": "coolant",
    "gearbox_oil": "transmission_fluid", "atf": "transmission_fluid",
    "transmission_oil": "transmission_fluid",
    "belt": "drive_belt", "serpentine_belt": "drive_belt",
    "battery": "battery_test", "battery_check": "battery_test",
    "wiper": "wipers", "wiper_blades": "wipers",
    "mot": "inspection", "annual_inspection": "inspection", "tüv": "inspection",
    "seasonal_tires": "tire_swap", "tire_change": "tire_swap",
    "winter_tires": "tire_swap",
}

PRIORITY_RANK = {"safety-critical": 0, "wear-item": 1, "standard": 2}
STATUS_RANK = {"OVERDUE": 0, "DUE SOON": 1, "OK": 2}

# ----------------------------------------------------------------------------
# Date helpers
# ----------------------------------------------------------------------------
DAYS_PER_MONTH_AVG = 30.4375


def parse_date(s: str) -> dt.date:
    """Parse YYYY-MM-DD (raises ValueError with a clear message on bad input)."""
    try:
        return dt.date.fromisoformat(s.strip())
    except ValueError as e:
        raise ValueError(f"invalid date {s!r}, expected YYYY-MM-DD: {e}") from e


def add_months(d: dt.date, months: int) -> dt.date:
    """Add calendar months, clamping the day to the month's length."""
    month_index = d.month - 1 + months
    year = d.year + month_index // 12
    month = month_index % 12 + 1
    day = min(d.day, _days_in_month(year, month))
    return dt.date(year, month, day)


def _days_in_month(year: int, month: int) -> int:
    if month == 12:
        nxt = dt.date(year + 1, 1, 1)
    else:
        nxt = dt.date(year, month + 1, 1)
    return (nxt - dt.timedelta(days=1)).day


def months_elapsed(start: dt.date, end: dt.date) -> float:
    """Fractional months between two dates (average-month basis)."""
    return (end - start).days / DAYS_PER_MONTH_AVG


# ----------------------------------------------------------------------------
# Core model
# ----------------------------------------------------------------------------
def normalize_task_id(name: str) -> str:
    """Normalize a history entry's task name to a library id ('' if unknown)."""
    key = name.strip().lower().replace(" ", "_").replace("-", "_")
    if key in TASKS_BY_ID:
        return key
    if key in ALIASES:
        return ALIASES[key]
    return ""


def effective_intervals(task: dict[str, Any], severe: bool,
                        done_before: bool) -> tuple[Optional[int], Optional[int]]:
    """Return (km_interval, mo_interval) for a task.

    Order of precedence:
      1. severe flag + explicit severe values -> use those;
      2. severe flag, no explicit values       -> scale both by SEVERE_GLOBAL_MULT;
      3. normal                                -> use km/mo (or *_repeat after
                                                 the first service, if defined).
    """
    km = task.get("km_repeat") if done_before and task.get("km_repeat") else task.get("km")
    mo = task.get("mo_repeat") if done_before and task.get("mo_repeat") else task.get("mo")
    if severe:
        if task.get("severe_km") is not None:
            km = task["severe_km"]
        elif km is not None:
            km = round(km * SEVERE_GLOBAL_MULT)
        if task.get("severe_mo") is not None:
            mo = task["severe_mo"]
        elif mo is not None:
            mo = max(1, round(mo * SEVERE_GLOBAL_MULT))
    return km, mo


def resolve_history(history_json: Optional[str],
                    in_service: dt.date) -> dict[str, dict[str, Any]]:
    """Parse --history JSON into {task_id: {"km": int, "date": date}}.

    Missing km defaults to 0; missing date defaults to the in-service date.
    Unknown task names print a warning to stderr and are ignored.
    """
    if not history_json:
        return {}
    try:
        entries = json.loads(history_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"--history is not valid JSON: {e}") from e
    if not isinstance(entries, list):
        raise ValueError("--history must be a JSON list of {task, km, date} objects")

    resolved: dict[str, dict[str, Any]] = {}
    for entry in entries:
        raw_id = str(entry.get("task", "")).strip()
        tid = normalize_task_id(raw_id)
        if not tid:
            print(f"warning: ignoring unknown history task {raw_id!r}",
                  file=sys.stderr)
            continue
        km = int(entry.get("km", 0) or 0)
        date_s = entry.get("date") or in_service.isoformat()
        resolved[tid] = {"km": km, "date": parse_date(str(date_s))}
    # Keep the LATEST entry per task if duplicated.
    return resolved


def compute_annual_km(current_km: float, in_service: dt.date,
                      today: dt.date, explicit: Optional[float]) -> float:
    """Annual mileage: explicit value, or fallback km / months-since-in-service * 12."""
    if explicit is not None:
        if explicit <= 0:
            raise ValueError("--annual-km must be positive")
        return float(explicit)
    months = months_elapsed(in_service, today)
    if months < 1.0:  # very new vehicle — annualize, with a sane floor
        return max(float(current_km) * 12.0, 1000.0)
    return current_km / months * 12.0


def km_at_date(current_km: float, today: dt.date, target: dt.date,
               annual_km: float) -> float:
    """Projected odometer at `target` given daily km derived from annual km."""
    days = (target - today).days
    per_day = annual_km / 365.0
    return round(current_km + days * per_day)


def date_at_km(current_km: float, today: dt.date, target_km: float,
               annual_km: float) -> dt.date:
    """Projected calendar date when the odometer reaches target_km."""
    per_day = annual_km / 365.0
    if per_day <= 0:
        return today
    days = (target_km - current_km) / per_day
    return today + dt.timedelta(days=round(days))


def evaluate_task(task: dict[str, Any], last_km: int, last_date: dt.date,
                  current_km: int, today: dt.date, annual_km: float,
                  severe: bool, done_before: bool) -> dict[str, Any]:
    """Evaluate one task: dual-interval status, next event, reason.

    Dual interval: a task is due when EITHER the km interval OR the month
    interval has elapsed since it was last done — whichever comes FIRST.
    """
    km_int, mo_int = effective_intervals(task, severe, done_before)

    km_due_at: Optional[int] = last_km + km_int if km_int else None
    date_due_at: Optional[dt.date] = add_months(last_date, mo_int) if mo_int else None

    km_remaining = (km_int - (current_km - last_km)) if km_int is not None else None
    days_remaining = ((date_due_at - today).days
                      if date_due_at is not None else None)

    status = "OK"
    reason = ""

    km_over = km_remaining is not None and km_remaining <= 0
    time_over = days_remaining is not None and days_remaining <= 0
    km_soon = (km_remaining is not None and 0 < km_remaining
               <= DUE_SOON_KM_FRACTION * km_int)
    time_soon = (days_remaining is not None and 0 < days_remaining <= DUE_SOON_DAYS)

    if km_over or time_over:
        status = "OVERDUE"
        bits = []
        if km_over:
            bits.append(f"{-km_remaining:+d} km vs interval" if km_over else "")
        if time_over:
            bits.append(f"{-days_remaining:+d} days vs interval")
        reason = ("overdue by km" if km_over and not time_over
                  else "overdue by time" if time_over and not km_over
                  else "overdue by both km and time") + f" ({'; '.join(bits)})"
    elif km_soon or time_soon:
        status = "DUE SOON"
        if km_soon and time_soon:
            reason = f"due in {km_remaining} km or {days_remaining} days (whichever first)"
        elif km_soon:
            reason = f"due in {km_remaining} km ({DUE_SOON_KM_FRACTION:.0%} threshold)"
        else:
            reason = f"due in {days_remaining} days ({DUE_SOON_DAYS}-day threshold)"
    else:
        parts = []
        if km_remaining is not None:
            parts.append(f"{km_remaining} km left")
        if days_remaining is not None:
            parts.append(f"{days_remaining} days left")
        reason = "; ".join(parts) if parts else "interval-based only"

    # Next event = earlier of the km-based event and the time-based event.
    # Overdue candidates are clamped to today at the current odometer: the
    # task is due NOW, not at the already-passed due point.
    candidates: list[dict[str, Any]] = []
    if km_due_at is not None:
        ev_date = date_at_km(current_km, today, km_due_at, annual_km)
        candidates.append({"date": max(ev_date, today),
                           "km": max(int(km_due_at), current_km),
                           "trigger": "km"})
    if date_due_at is not None:
        ev_km = km_at_date(current_km, today, date_due_at, annual_km)
        candidates.append({"date": max(date_due_at, today),
                           "km": max(ev_km, current_km),
                           "trigger": "time"})
    nxt = min(candidates, key=lambda c: (c["date"], 0 if c["trigger"] == "km" else 1))

    return {
        "task": task["id"],
        "name": task["name"],
        "priority": task["priority"],
        "status": status,
        "reason": reason,
        "interval_km": km_int,
        "interval_months": mo_int,
        "last_done_km": last_km,
        "last_done_date": last_date.isoformat(),
        "km_due_at": km_due_at,
        "date_due_at": date_due_at.isoformat() if date_due_at else None,
        "km_remaining": km_remaining,
        "days_remaining": days_remaining,
        "next": {"date": nxt["date"].isoformat(),
                 "km": int(nxt["km"]),
                 "trigger": nxt["trigger"]},
        "cost_range_usd": list(task["cost"]),
        "diy": task["diy"],
        "notes": task["notes"],
    }


def build_status(current_km: int, in_service: dt.date,
                 annual_km: float, severe: bool, done: dict[str, dict[str, Any]],
                 today: dt.date) -> list[dict[str, Any]]:
    """Evaluate every library task. No-history rule: last done = in-service @ 0 km
    (i.e. assume never done; both intervals count from the in-service date)."""
    results = []
    for task in TASK_LIBRARY:
        rec = done.get(task["id"])
        done_before = task["id"] in done
        last_km = rec["km"] if rec else 0
        last_date = rec["date"] if rec else in_service
        results.append(evaluate_task(task, last_km, last_date, current_km,
                                     today, annual_km, severe, done_before))
    results.sort(key=lambda r: (STATUS_RANK[r["status"]],
                                PRIORITY_RANK[r["priority"]],
                                r["next"]["date"]))
    return results


def build_timeline(current_km: int, in_service: dt.date,
                   annual_km: float, severe: bool, done: dict[str, dict[str, Any]],
                   today: dt.date,
                   months: int = TIMELINE_MONTHS) -> list[dict[str, Any]]:
    """Project services over the next `months` months, repeating each task as its
    interval recurs. Overdue items surface as events at today's date."""
    window_end = add_months(today, months)
    events: list[dict[str, Any]] = []
    for task in TASK_LIBRARY:
        rec = done.get(task["id"])
        done_before = task["id"] in done
        last_km = rec["km"] if rec else 0
        last_date = rec["date"] if rec else in_service
        for _ in range(200):  # hard cap: never loop forever
            ev = evaluate_task(task, last_km, last_date, current_km, today,
                               annual_km, severe, done_before)
            nxt = ev["next"]
            event_date = dt.date.fromisoformat(nxt["date"])
            if event_date > window_end:
                break
            events.append({
                "date": nxt["date"],
                "month": nxt["date"][:7],
                "task": task["id"],
                "name": task["name"],
                "priority": task["priority"],
                "km": nxt["km"],
                "trigger": nxt["trigger"],
                "interval_km": ev["interval_km"],
                "interval_months": ev["interval_months"],
                "cost_range_usd": ev["cost_range_usd"],
                "diy": ev["diy"],
            })
            # Advance the cursor past this event and repeat.
            last_km = max(last_km, nxt["km"])
            last_date = max(last_date, event_date)
            current_km = min(current_km, nxt["km"]) if nxt["km"] < current_km else current_km
            done_before = True  # coolant-style first/repeat intervals switch here
        # restore per-task starting point handled above via locals per iteration
    events.sort(key=lambda e: (e["date"], PRIORITY_RANK[e["priority"]]))
    return events


# ----------------------------------------------------------------------------
# Output
# ----------------------------------------------------------------------------
def _fmt_cost(rng: tuple[int, int] | list[int]) -> str:
    return f"${rng[0]}-${rng[1]}"


def print_tasks(as_json: bool) -> None:
    if as_json:
        payload = [
            {"id": t["id"], "name": t["name"], "km_interval": t["km"],
             "months_interval": t["mo"], "severe_km": t.get("severe_km"),
             "severe_mo": t.get("severe_mo"), "km_repeat": t.get("km_repeat"),
             "mo_repeat": t.get("mo_repeat"), "priority": t["priority"],
             "cost_range_usd": list(t["cost"]), "diy": t["diy"],
             "notes": t["notes"]}
            for t in TASK_LIBRARY
        ]
        print(json.dumps({"version": __version__, "tasks": payload}, indent=2))
        return
    w = (28, 10, 7, 11, 7, 16, 10, 9)
    print(f"{'Task':{w[0]}} {'km':>{w[1]}} {'mo':>{w[2]}} {'severe km':>{w[3]}} "
          f"{'sev mo':>{w[4]}} {'priority':{w[5]}} {'cost':>{w[6]}} {'DIY':>{w[7]}}")
    print("-" * (sum(w) + 8))
    for t in TASK_LIBRARY:
        skm = f"{t['severe_km']:,}" if t.get("severe_km") else "-"
        smo = str(t["severe_mo"]) if t.get("severe_mo") else "-"
        km = f"{t['km']:,}" if t["km"] else "time"
        rep = " *" if t.get("km_repeat") else ""
        print(f"{t['name'][:w[0] - 1]:{w[0]}} {km:>{w[1]}}{rep} {t['mo'] or '':>{w[2]}} "
              f"{skm:>{w[3]}} {smo:>{w[4]}} {t['priority']:{w[5]}} "
              f"{_fmt_cost(t['cost']):>{w[6]}} {t['diy']:>{w[7]}}")
    print("\n* coolant: first fill 100,000 km / 60 mo, then 50,000 km / 36 mo.")
    print("  Tasks without explicit severe values are scaled ×"
          f"{SEVERE_GLOBAL_MULT} under --severe.")


def print_status(results: list[dict[str, Any]], meta: dict[str, Any],
                 as_json: bool) -> None:
    if as_json:
        print(json.dumps({"meta": meta, "tasks": results}, indent=2))
        return
    w = (24, 9, 15, 12, 12, 10, 26)
    print(f"Vehicle: {meta['current_km']:,} km | in service {meta['in_service']} | "
          f"~{meta['annual_km']:,.0f} km/yr{' | SEVERE SERVICE' if meta['severe'] else ''}")
    print(f"{'Task':{w[0]}} {'Status':^{w[1]}} {'Priority':{w[2]}} "
          f"{'km due at':>{w[3]}} {'date due':>{w[4]}} {'next in':>{w[5]}}  Reason")
    print("-" * 118)
    for r in results:
        km_due = f"{r['km_due_at']:,}" if r["km_due_at"] else "-"
        date_due = r["date_due_at"] or "-"
        nxt = (f"{r['next']['date']}"
               if r["next"]["trigger"] == "time"
               else f"{r['next']['km']:,} km")
        marker = " ! " if r["status"] == "OVERDUE" else (" ~ " if r["status"] == "DUE SOON" else "   ")
        print(f"{marker}{r['name'][:w[0] - 3]:{w[0]}} {r['status']:^{w[1]}} "
              f"{r['priority']:{w[2]}} {km_due:>{w[3]}} {date_due:>{w[4]}} "
              f"{nxt:>{w[5]}}  {r['reason']}")
    overdue = [r for r in results if r["status"] == "OVERDUE"]
    soon = [r for r in results if r["status"] == "DUE SOON"]
    print("-" * 118)
    print(f"Summary: {len(overdue)} OVERDUE, {len(soon)} DUE SOON, "
          f"{len(results) - len(overdue) - len(soon)} OK")
    for r in overdue[:3]:
        cost = _fmt_cost(r["cost_range_usd"])
        print(f"  ! {r['name']}: {r['reason']} — typical cost {cost}, DIY {r['diy']}")


def print_timeline(events: list[dict[str, Any]], meta: dict[str, Any],
                   as_json: bool) -> None:
    if as_json:
        print(json.dumps({"meta": meta, "window_months": TIMELINE_MONTHS,
                          "events": events}, indent=2))
        return
    print(f"Next {TIMELINE_MONTHS} months | from {meta['today']} | "
          f"~{meta['annual_km']:,.0f} km/yr assumed")
    if not events:
        print("(no services projected in this window)")
        return
    by_month: dict[str, list[dict[str, Any]]] = {}
    for e in events:
        by_month.setdefault(e["month"], []).append(e)
    total_lo, total_hi = 0, 0
    for month in sorted(by_month):
        print(f"\n{month}")
        for e in by_month[month]:
            lo, hi = e["cost_range_usd"]
            total_lo += lo
            total_hi += hi
            km = f"~{e['km']:,} km" if e["trigger"] == "time" else f"{e['km']:,} km"
            trig = "time" if e["trigger"] == "time" else "km"
            print(f"  {e['date']}  {e['name'][:34]:34} {km:>12} ({trig} due)  "
                  f"{_fmt_cost(e['cost_range_usd'])}  DIY {e['diy']}")
    print(f"\nEstimated 24-month cost of projected services: "
          f"${total_lo}-{total_hi} (generic indie-shop ranges)")


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------
def _common_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--km", type=int, required=True, metavar="CURRENT_KM",
                   help="current odometer reading in km")
    p.add_argument("--in-service", required=True, metavar="YYYY-MM-DD",
                   help="vehicle first in-service / registration date")
    p.add_argument("--annual-km", type=float, default=None, metavar="EST",
                   help="estimated km per year (default: derived from km / age)")
    p.add_argument("--severe", action="store_true",
                   help="severe service: short trips, city, towing, dust, heat")
    p.add_argument("--history", default=None, metavar="JSON",
                   help='service history, e.g. \'[{"task":"oil","km":63000,'
                        '"date":"2026-01-15"}]\'')
    p.add_argument("--today", default=None, metavar="YYYY-MM-DD",
                   help=argparse.SUPPRESS)  # deterministic testing hook
    p.add_argument("--json", action="store_true", help="machine-readable output")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="car_maintenance.py",
        description="Vehicle maintenance scheduler: dual-interval (km OR months, "
                    "whichever first) status and a 24-month forward timeline.")
    parser.add_argument("--version", action="version",
                        version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_tasks = sub.add_parser("tasks", help="list the built-in task library")
    p_tasks.add_argument("--json", action="store_true", help="machine-readable output")

    p_status = sub.add_parser("status", help="what is overdue / due soon / ok")
    _common_args(p_status)

    p_tl = sub.add_parser("timeline", help="projected services, next 24 months")
    _common_args(p_tl)
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "tasks":
        print_tasks(args.json)
        return 0

    try:
        in_service = parse_date(args.in_service)
        today = parse_date(args.today) if args.today else dt.date.today()
        if in_service > today:
            raise ValueError("--in-service date is in the future")
        done = resolve_history(args.history, in_service)
        annual_km = compute_annual_km(args.km, in_service, today, args.annual_km)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    meta = {
        "current_km": args.km,
        "in_service": in_service.isoformat(),
        "annual_km": round(annual_km),
        "annual_km_source": "explicit" if args.annual_km is not None else "derived",
        "severe": bool(args.severe),
        "today": today.isoformat(),
    }

    if args.command == "status":
        results = build_status(args.km, in_service, annual_km, args.severe,
                               done, today)
        print_status(results, meta, args.json)
    else:
        events = build_timeline(args.km, in_service, annual_km, args.severe,
                                done, today)
        print_timeline(events, meta, args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
