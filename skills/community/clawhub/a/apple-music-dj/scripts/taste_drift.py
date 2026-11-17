#!/usr/bin/env python3
"""
taste_drift.py — How has your taste changed?

Compares your current taste with a dated snapshot saved by taste_profiler.py
(~/.apple-music-dj/snapshots/YYYY-MM-DD.json) and reports:
  - genres rising and falling
  - artists that entered or left your top 20
  - era shift
  - changes in variety / mainstream / energy
  - archetype change

Usage:
  python3 taste_drift.py                         # newest snapshot vs. ~90 days earlier
  python3 taste_drift.py --since 6m              # 30d, 12w, 6m, 1y or a number of days
  python3 taste_drift.py --from 2026-01-01       # compare against the snapshot nearest this date
  python3 taste_drift.py --profile profile.json  # use a fresh profile as "now"
  python3 taste_drift.py --format text           # human-readable (default: json)

Needs at least two snapshots (each fresh taste_profiler.py run saves one).
"""

import sys

if sys.version_info < (3, 10):
    sys.exit(
        f"ERROR: Python 3.10+ is required (you have "
        f"{sys.version_info.major}.{sys.version_info.minor}). Please upgrade."
    )

import argparse
import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path

from _common import list_snapshots, load_profile, make_snapshot
from taste_card import detect_archetype

DEFAULT_SINCE_DAYS = 90
MIN_GENRE_DELTA = 0.01  # ignore genre moves smaller than one percentage point
TOP_MOVERS = 3


# ── Parsing ──────────────────────────────────────────────────────

def parse_since(value: str) -> int:
    """'90d', '12w', '6m', '1y' or a bare number of days → days."""
    m = re.fullmatch(r"(\d+)\s*([dwmy]?)", value.strip().lower())
    if not m:
        raise ValueError(f"Can't read '{value}'. Try 90d, 12w, 6m or 1y.")
    n, unit = int(m.group(1)), m.group(2) or "d"
    return n * {"d": 1, "w": 7, "m": 30, "y": 365}[unit]


def parse_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"Can't read date '{value}'. Use YYYY-MM-DD.") from None


def pick_baseline(snapshots: list[tuple[str, Path]], current_date: date,
                  target: date) -> tuple[str, Path] | None:
    """The snapshot closest to `target` that is older than `current_date`."""
    older = [(d, p) for d, p in snapshots if parse_date(d) < current_date]
    if not older:
        return None
    return min(older, key=lambda s: abs((parse_date(s[0]) - target).days))


# ── Drift computation ────────────────────────────────────────────

def _weights(entries: list[dict], key: str) -> dict[str, float]:
    return {e[key]: e.get("weight", 0) for e in entries if e.get(key)}


def _score_delta(old: dict, new: dict, key: str) -> dict:
    a, b = old.get(key, 0.5), new.get(key, 0.5)
    return {"from": a, "to": b, "delta": round(b - a, 2)}


def compute_drift(old: dict, new: dict) -> dict:
    """Compare two snapshots (or profiles) and describe how taste moved."""
    old_g, new_g = _weights(old.get("genre_distribution", []), "genre"), _weights(new.get("genre_distribution", []), "genre")
    deltas = {g: round(new_g.get(g, 0) - old_g.get(g, 0), 3) for g in old_g.keys() | new_g.keys()}
    risers = sorted(((g, d) for g, d in deltas.items() if d >= MIN_GENRE_DELTA), key=lambda x: -x[1])[:TOP_MOVERS]
    fallers = sorted(((g, d) for g, d in deltas.items() if d <= -MIN_GENRE_DELTA), key=lambda x: x[1])[:TOP_MOVERS]

    old_names = {a["name"].lower(): a["name"] for a in old.get("top_artists", [])[:20]}
    new_names = {a["name"].lower(): a["name"] for a in new.get("top_artists", [])[:20]}
    new_artists = [new_names[k] for k in new_names if k not in old_names]
    dropped_artists = [old_names[k] for k in old_names if k not in new_names]

    old_eras, new_eras = _weights(old.get("era_distribution", []), "decade"), _weights(new.get("era_distribution", []), "decade")
    era_deltas = {d: round(new_eras.get(d, 0) - old_eras.get(d, 0), 3) for d in old_eras.keys() | new_eras.keys()}
    top_era_old = max(old_eras, key=old_eras.get) if old_eras else None
    top_era_new = max(new_eras, key=new_eras.get) if new_eras else None
    era_mover = max(era_deltas.items(), key=lambda x: abs(x[1])) if era_deltas else None

    arch_old, arch_new = detect_archetype(old)[0], detect_archetype(new)[0]

    drift = {
        "genres": {
            "risers": [{"genre": g, "delta": d} for g, d in risers],
            "fallers": [{"genre": g, "delta": d} for g, d in fallers],
        },
        "artists": {"new": new_artists, "dropped": dropped_artists},
        "eras": {
            "top_from": top_era_old,
            "top_to": top_era_new,
            "biggest_move": {"decade": era_mover[0], "delta": era_mover[1]} if era_mover and era_mover[1] else None,
        },
        "scores": {
            "variety": _score_delta(old, new, "variety_score"),
            "mainstream": _score_delta(old, new, "mainstream_score"),
            "energy_profile": {"from": old.get("energy_profile"), "to": new.get("energy_profile")},
        },
        "archetype": {"from": arch_old, "to": arch_new, "changed": arch_old != arch_new},
    }
    drift["narrative"] = build_narrative(drift)
    return drift


def _pct(delta: float) -> str:
    return f"{delta * 100:+.0f}%".replace("-", "−")


def build_narrative(drift: dict) -> str:
    """One readable line summarising the biggest moves."""
    parts = []
    risers, fallers = drift["genres"]["risers"], drift["genres"]["fallers"]
    if risers and fallers:
        parts.append(f"Your taste moved toward {risers[0]['genre']} ({_pct(risers[0]['delta'])}) "
                     f"and away from {fallers[0]['genre']} ({_pct(fallers[0]['delta'])}).")
    elif risers:
        parts.append(f"Your taste moved toward {risers[0]['genre']} ({_pct(risers[0]['delta'])}).")
    elif fallers:
        parts.append(f"Your taste moved away from {fallers[0]['genre']} ({_pct(fallers[0]['delta'])}).")

    new = drift["artists"]["new"]
    if new:
        extra = f" and {len(new) - 1} more" if len(new) > 1 else ""
        parts.append(f"{new[0]}{extra} entered your top 20.")

    eras = drift["eras"]
    if eras["top_from"] and eras["top_to"] and eras["top_from"] != eras["top_to"]:
        parts.append(f"Your center of gravity shifted from the {eras['top_from']} to the {eras['top_to']}.")

    if drift["archetype"]["changed"]:
        parts.append(f"You've gone from a {drift['archetype']['from']} to a {drift['archetype']['to']}.")

    return " ".join(parts) or "Your taste has been steady — no big moves."


def build_report(old_date: str, new_date: str, old: dict, new: dict) -> dict:
    drift = compute_drift(old, new)
    days = (parse_date(new_date) - parse_date(old_date)).days
    return {"period": {"from": old_date, "to": new_date, "days": days}, **drift}


# ── Text output ──────────────────────────────────────────────────

def format_text(report: dict) -> str:
    p = report["period"]
    lines = [f"Taste drift: {p['from']} → {p['to']} ({p['days']} days)", "", report["narrative"], ""]
    g = report["genres"]
    if g["risers"]:
        lines.append("Rising:   " + ", ".join(f"{x['genre']} {_pct(x['delta'])}" for x in g["risers"]))
    if g["fallers"]:
        lines.append("Falling:  " + ", ".join(f"{x['genre']} {_pct(x['delta'])}" for x in g["fallers"]))
    a = report["artists"]
    if a["new"]:
        lines.append("New top artists:     " + ", ".join(a["new"]))
    if a["dropped"]:
        lines.append("Fell out of top 20:  " + ", ".join(a["dropped"]))
    s = report["scores"]
    for label, key in (("Variety", "variety"), ("Mainstream", "mainstream")):
        lines.append(f"{label}: {s[key]['from']} → {s[key]['to']} ({s[key]['delta']:+.2f})")
    lines.append(f"Energy: {s['energy_profile']['from']} → {s['energy_profile']['to']}")
    arch = report["archetype"]
    lines.append(f"Archetype: {arch['from']}" + (f" → {arch['to']}" if arch["changed"] else " (unchanged)"))
    return "\n".join(lines)


# ── Main ─────────────────────────────────────────────────────────

def _load_snapshot(path: Path) -> dict:
    """Read a snapshot, turning I/O and JSON problems into the CLI's user-facing ValueError."""
    try:
        with open(path) as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        raise ValueError(f"Can't read snapshot {path.name}: {e}. Delete it or re-run taste_profiler.py.") from e
    if not isinstance(data, dict):
        raise ValueError(f"Snapshot {path.name} isn't a valid snapshot (expected a JSON object).")
    return data


def run(args, snapshot_dir: Path | None = None) -> dict:
    """Resolve 'now' and the baseline, then build the report. Raises ValueError with a user-facing message."""
    snapshots = list_snapshots(snapshot_dir)

    if args.profile:
        new = make_snapshot(load_profile(args.profile))
        new_date = new["generated_at"][:10]
    elif snapshots:
        new_date, new_path = snapshots[-1]
        new = _load_snapshot(new_path)
    else:
        raise ValueError("No snapshots yet. Run taste_profiler.py (each fresh build saves one), "
                         "then come back after your taste has had time to change.")

    current = parse_date(new_date)
    target = parse_date(args.from_date) if args.from_date else current - timedelta(days=parse_since(args.since))
    baseline = pick_baseline(snapshots, current, target)
    if not baseline:
        raise ValueError("Need at least two snapshots from different days to measure drift. "
                         "Run taste_profiler.py again later.")
    old_date, old_path = baseline
    return build_report(old_date, new_date, _load_snapshot(old_path), new)


def main():
    parser = argparse.ArgumentParser(description="Measure how your Apple Music taste has changed")
    parser.add_argument("--profile", default=None, help="Use this profile as 'now' instead of the newest snapshot")
    parser.add_argument("--since", default=f"{DEFAULT_SINCE_DAYS}d", help="How far back to compare (default: 90d)")
    parser.add_argument("--from", dest="from_date", default=None,
                        help="Compare against the snapshot nearest this date (YYYY-MM-DD)")
    parser.add_argument("--format", choices=["json", "text"], default="json")
    args = parser.parse_args()

    try:
        report = run(args)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    print(format_text(report) if args.format == "text" else json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
