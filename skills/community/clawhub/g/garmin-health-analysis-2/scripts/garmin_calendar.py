#!/usr/bin/env python3
"""
Fetch the Garmin Connect calendar: trips, races/events, naps, weigh-ins.

The Garmin calendar-service carries more than workouts. Luis adds trips and
races in the Garmin app, and this is where they land:

  jetLagTrip        one item PER DAY of a trip. This is the ONLY source for
                    FUTURE trips; get_stats().isJetLagDay only reports days
                    that have already happened.
  event             a race or booked event, WITH a title and usually a URL.
  wellnessActivity  Health Snapshot etc.
  nap               recorded naps.
  userTimeChanged   timezone change -- the tell for a flight day.
  weight            weigh-in day.
  bloodpressure     blood-pressure day.
  activity          recorded activities.

Endpoint: GET /calendar-service/year/{year}/month/{month-1}  (0-indexed month)
via the client's get_scheduled_workouts(year, month).

TRIPS also have their own API, which the calendar does NOT expose:
  GET    /jetlag-service/jetlag/trip        list trips (with flights)
  POST   /jetlag-service/jetlag/trip        create
  PUT    /jetlag-service/jetlag/trip        replace
  DELETE /jetlag-service/jetlag/trip/{id}   delete
  GET    /jetlag-service/jetlag/status/daily/{date}  guidance
That path can CREATE and EDIT trips, so `trip-add` / `trip-update` /
`trip-delete` below write them. Requires garminconnect >= 0.3.18.

Outputs JSON to stdout for parsing by the agent.
"""

import json
import sys
import argparse
from datetime import date, datetime
from pathlib import Path

# Import auth helper
sys.path.insert(0, str(Path(__file__).parent))
from garmin_auth import get_client

try:
    from garminconnect import Garmin  # noqa: F401  (import-time dependency check)
except ImportError:
    print('{"error": "garminconnect not installed. Run: pip3 install garminconnect"}', file=sys.stderr)
    sys.exit(1)

# Jet Lag trip write support arrived in garminconnect 0.3.18. Guard on the
# attribute rather than a version string, so it fails with a clear message
# instead of an AttributeError deep in the library.
def _trip_api_available(client):
    return all(hasattr(client, m) for m in
               ("get_jetlag_trips", "add_jetlag_trip", "update_jetlag_trip", "delete_jetlag_trip"))

_TRIP_UPGRADE_HINT = ("Trip writing needs garminconnect >= 0.3.18 "
                     "(pip3 install --upgrade garminconnect)")


def _normalize_timestamp(ts):
    """Garmin stores trip times with a fractional second (e.g. '...T15:45:00.0').

    Live testing on 2026-10-17: a time WITHOUT the '.0' was rejected with
    HTTP 500, while the same trip with '.0' succeeded. Normalise, so a caller
    can pass either form.
    """
    if not isinstance(ts, str):
        return ts
    if "." in ts.split("T")[-1]:
        return ts
    return ts + ".0"


def _load_flights(arg_flights, arg_file):
    """Flights come in as --flights '<json>' or --flights-file <path>."""
    raw = None
    if arg_flights:
        raw = arg_flights
    elif arg_file:
        raw = Path(arg_file).read_text()
    if not raw:
        raise ValueError("provide --flights '<json>' or --flights-file <path>")
    data = json.loads(raw)
    if isinstance(data, dict):
        data = data.get("flights") or []
    if not isinstance(data, list) or not data:
        raise ValueError("flights must be a non-empty JSON list")
    out = []
    for f in data:
        f = dict(f)
        for k in ("originTimestamp", "destinationTimestamp"):
            if f.get(k):
                f[k] = _normalize_timestamp(f[k])
        out.append(f)
    return out


def add_months(d, n):
    """Return the first day of the month n months from d."""
    y = d.year + (d.month - 1 + n) // 12
    m = (d.month - 1 + n) % 12 + 1
    return date(y, m, 1)


def month_start(d):
    return d.replace(day=1)


def _normalize(item):
    """Flatten one calendar item to a stable shape."""
    return {
        "date": item.get("date"),
        "item_type": item.get("itemType"),
        "title": item.get("title"),
        "url": item.get("url"),
        "activity_type_id": item.get("activityTypeId"),
        "duration_seconds": item.get("duration"),
        "distance_m": item.get("distance"),
        "calories": item.get("calories"),
        "weight_kg": item.get("weight"),
    }


def fetch_calendar(client, months_back=12, months_fwd=6):
    """Fetch every calendar item across a month window.

    Returns {"items": [...], "start": ..., "end": ..., "count": n}. A month that
    errors is reported in "errors" rather than aborting the whole window, because
    calendar-service has a history floor (months before ~2024-12 return nothing)
    and a single bad month should not hide the rest.
    """
    today = date.today()
    start = add_months(month_start(today), -months_back)
    end = add_months(month_start(today), months_fwd)

    items, errors = [], []
    seen = set()
    m = start
    while m <= end:
        try:
            r = client.get_scheduled_workouts(m.year, m.month) or {}
            for i in r.get("calendarItems") or []:
                if not (i.get("date") and i.get("itemType")):
                    continue
                # calendar-service re-yields some items across adjacent months
                # (an event near a month boundary arrives twice), so dedupe on the
                # natural key. Without this, `races` listed each event two or
                # more times.
                key = (i.get("date"), i.get("itemType"), i.get("title"), i.get("url"))
                if key in seen:
                    continue
                seen.add(key)
                items.append(_normalize(i))
        except Exception as e:
            errors.append(f"{m.year}-{m.month:02d}: {type(e).__name__}: {str(e)[:120]}")
        m = add_months(m, 1)

    items.sort(key=lambda x: (x["date"] or "", x["item_type"] or ""))
    out = {
        "items": items,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "count": len(items),
    }
    if errors:
        out["errors"] = errors
    return out


def _trips(client, months_back, months_fwd, with_names=False):
    """Trips only, one row per flagged day.

    Past days can be labelled from get_stats().jetLagTripName; future days
    cannot (the name is only published after the day has passed).
    """
    cal = fetch_calendar(client, months_back, months_fwd)
    today = date.today()
    days = sorted({i["date"] for i in cal["items"] if i["item_type"] == "jetLagTrip"})

    names = {}
    if with_names:
        for d in days:
            if d > today.isoformat():
                continue
            try:
                names[d] = (client.get_stats(d) or {}).get("jetLagTripName")
            except Exception:
                names[d] = None

    trips = [{"date": d, "is_future": d > today.isoformat(),
              "trip_name": names.get(d)} for d in days]

    # Group consecutive days into trip windows for a readable summary.
    windows = []
    for t in trips:
        if windows and (date.fromisoformat(t["date"]) - date.fromisoformat(windows[-1]["end"])).days == 1:
            windows[-1]["end"] = t["date"]
            windows[-1]["days"] += 1
            windows[-1]["trip_name"] = windows[-1]["trip_name"] or t["trip_name"]
        else:
            windows.append({"start": t["date"], "end": t["date"], "days": 1,
                            "trip_name": t["trip_name"]})

    out = {"trips": trips, "windows": windows, "count": len(trips),
           "start": cal["start"], "end": cal["end"]}
    if "errors" in cal:
        out["errors"] = cal["errors"]
    return out


def _trip_write(client, mode, args):
    """trip-list / trip-add / trip-update / trip-delete."""
    if not _trip_api_available(client):
        return {"error": _TRIP_UPGRADE_HINT}

    if mode == "trip-list":
        trips = client.get_jetlag_trips() or []
        return {"trips": trips, "count": len(trips)}

    if mode == "trip-delete":
        if not args.trip_id:
            return {"error": "--trip-id is required for trip-delete"}
        # SAFETY GATE (security-audit 2026-10-17): deleting a trip mutates the
        # user's Garmin account and cannot be undone from here. Without
        # --confirm-delete this branch is READ-ONLY: it resolves the trip and
        # reports exactly what would be removed. The caller must show that to
        # the user and get an explicit yes before re-running with the flag.
        target = next((t for t in (client.get_jetlag_trips() or [])
                       if str(t.get("tripId")) == str(args.trip_id)), None)
        if not args.confirm_delete:
            return {"confirmation_required": True,
                    "dry_run": True,
                    "would_delete": target or {"tripId": str(args.trip_id), "found": False},
                    "hint": "nothing was changed; re-run with --confirm-delete to delete this trip"}
        if target is None:
            return {"error": f"no trip with id {args.trip_id}; nothing deleted"}
        client.delete_jetlag_trip(args.trip_id)
        return {"deleted": str(args.trip_id), "trips": client.get_jetlag_trips() or []}

    # trip-add / trip-update share the same payload
    if not args.start or not args.end:
        return {"error": "--start and --end are required (YYYY-MM-DD)"}
    try:
        flights = _load_flights(args.flights, args.flights_file)
    except Exception as e:
        return {"error": f"flights: {e}"}

    if mode == "trip-update":
        if not args.trip_id:
            return {"error": "--trip-id is required for trip-update"}
        # SAFETY GATE: the trip API is a full REPLACE, so an incomplete flight
        # list silently drops legs. Preview the current trip and the exact
        # payload unless --confirm-update is passed.
        current = next((t for t in (client.get_jetlag_trips() or [])
                        if str(t.get("tripId")) == str(args.trip_id)), None)
        if not args.confirm_update:
            return {"confirmation_required": True,
                    "dry_run": True,
                    "current": current,
                    "would_write": {"start": args.start, "end": args.end, "flights": flights},
                    "hint": "this REPLACES the whole trip; nothing was changed. "
                            "re-run with --confirm-update to apply"}
        if current is None:
            return {"error": f"no trip with id {args.trip_id}; nothing updated"}
        client.update_jetlag_trip(args.trip_id, args.start, args.end, flights)
        got = [t for t in (client.get_jetlag_trips() or [])
               if str(t.get("tripId")) == str(args.trip_id)]
        return {"updated": str(args.trip_id), "trip": got[0] if got else None}

    created = client.add_jetlag_trip(args.start, args.end, flights)
    tid = created.get("tripId") if isinstance(created, dict) else None
    got = [t for t in (client.get_jetlag_trips() or [])
           if str(t.get("tripId")) == str(tid)]
    return {"created": created, "read_back": got[0] if got else None}


def main():
    parser = argparse.ArgumentParser(description="Fetch or edit the Garmin Connect calendar")
    parser.add_argument("metric", choices=["calendar", "trips", "races", "events", "nap", "summary",
                                           "trip-list", "trip-add", "trip-update", "trip-delete"],
                        help="calendar=all items, trips=jetLagTrip days, races/events=event items, nap=naps, "
                             "summary=counts by type, trip-list/-add/-update/-delete=Jet Lag trip API")
    parser.add_argument("--months-back", type=int, default=12, help="Months of history to scan (default: 12)")
    parser.add_argument("--months-fwd", type=int, default=6, help="Months ahead to scan (default: 6)")
    parser.add_argument("--with-names", action="store_true",
                        help="For trips: also label past days with the trip name from get_stats (one call per past day)")
    parser.add_argument("--start", help="Trip start date YYYY-MM-DD (trip-add/trip-update)")
    parser.add_argument("--end", help="Trip end date YYYY-MM-DD (trip-add/trip-update)")
    parser.add_argument("--trip-id", help="Trip id (trip-update/trip-delete)")
    parser.add_argument("--flights", help="Flights as a JSON list (trip-add/trip-update)")
    parser.add_argument("--flights-file", help="Path to a JSON file holding the flights list")
    parser.add_argument("--confirm-delete", action="store_true",
                        help="Required to actually delete a trip. Without it, trip-delete only previews.")
    parser.add_argument("--confirm-update", action="store_true",
                        help="Required to actually replace a trip (the API is a full replace). Without it, trip-update only previews.")
    args = parser.parse_args()

    client = get_client()
    if not client:
        print('{"error": "Not authenticated. Run: python3 scripts/garmin_auth.py login --email YOUR_EMAIL --password YOUR_PASSWORD"}')
        sys.exit(1)

    if args.metric.startswith("trip-"):
        result = _trip_write(client, args.metric, args)
    elif args.metric == "trips":
        result = _trips(client, args.months_back, args.months_fwd, args.with_names)
    elif args.metric in ("races", "events"):
        cal = fetch_calendar(client, args.months_back, args.months_fwd)
        evs = [i for i in cal["items"] if i["item_type"] == "event"]
        result = {"events": evs, "count": len(evs), "start": cal["start"], "end": cal["end"]}
        if "errors" in cal:
            result["errors"] = cal["errors"]
    elif args.metric == "nap":
        cal = fetch_calendar(client, args.months_back, args.months_fwd)
        naps = [i for i in cal["items"] if i["item_type"] == "nap"]
        result = {"naps": naps, "count": len(naps), "start": cal["start"], "end": cal["end"]}
        if "errors" in cal:
            result["errors"] = cal["errors"]
    elif args.metric == "summary":
        cal = fetch_calendar(client, args.months_back, args.months_fwd)
        counts = {}
        for i in cal["items"]:
            counts[i["item_type"]] = counts.get(i["item_type"], 0) + 1
        trip_days = [i["date"] for i in cal["items"] if i["item_type"] == "jetLagTrip"]
        future = [d for d in trip_days if d > date.today().isoformat()]
        result = {"by_type": dict(sorted(counts.items(), key=lambda x: -x[1])),
                  "trip_days": len(trip_days), "future_trip_days": sorted(future),
                  "start": cal["start"], "end": cal["end"]}
        if "errors" in cal:
            result["errors"] = cal["errors"]
    else:
        result = fetch_calendar(client, args.months_back, args.months_fwd)

    print(json.dumps(result, indent=2))

    # An error dict is a failure, not data (same contract as garmin_data.py).
    if isinstance(result, dict) and result.get("error"):
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    # A preview is not a completed mutation. Exit 2 so no caller can mistake
    # "here is what would happen" for "it happened" (security-audit 2026-10-17).
    if isinstance(result, dict) and result.get("confirmation_required"):
        print("Confirmation required; nothing was changed.", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
