#!/usr/bin/env python3
"""
promote-profile.py — Mine the event log and draft new profile entries.

Reads web-access-log.json, finds services with enough observations to
characterize, and prints a draft profile in profiles.md format.

Usage:
    python3 scripts/promote-profile.py
    python3 scripts/promote-profile.py --min-events 3
    python3 scripts/promote-profile.py --service "my-api.com"
    python3 scripts/promote-profile.py --write   # append drafts to profiles.md

The agent or user reviews the output and decides whether to keep it.
Nothing is written to profiles.md without --write flag.
"""

from __future__ import annotations

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

SCRIPT_DIR = Path(__file__).resolve().parent
MODULE_DIR = SCRIPT_DIR.parent

_WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", Path.home() / ".openclaw" / "workspace"))
DATA_DIR = _WORKSPACE / "data" / "agent-tollbooth"

# Read-only reference bundled with the skill — never written to
BUNDLE_PROFILES_PATH = MODULE_DIR / "references" / "profiles.md"
# Write target — lives outside the skill bundle in workspace data dir
PROFILES_PATH = DATA_DIR / "profiles.md"
LOG_PATH = DATA_DIR / "web-access-log.json"

# Minimum events before a service is considered promotable
DEFAULT_MIN_EVENTS = 5

# Event types that signal friction (worth documenting)
FRICTION_EVENTS = {"429", "timeout", "auth_failure"}
# Event types that signal working patterns
SUCCESS_EVENTS = {"success", "cache_hit", "workaround"}


def _load_log() -> list[dict]:
    if not LOG_PATH.exists():
        return []
    try:
        return json.loads(LOG_PATH.read_text(encoding="utf-8") or "[]")
    except json.JSONDecodeError:
        return []


def _load_known_profiles() -> set[str]:
    """Return lowercased set of service names already in either profiles file."""
    known = set()
    for path in (BUNDLE_PROFILES_PATH, PROFILES_PATH):
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("## "):
                known.add(line[3:].strip().lower())
    return known


def _analyze_service(service: str, events: list[dict]) -> dict:
    """Summarize observations for a single service."""
    friction: list[dict] = []
    successes: list[dict] = []
    misses: list[dict] = []

    for e in events:
        et = e.get("event_type", "")
        if et in FRICTION_EVENTS:
            friction.append(e)
        elif et in SUCCESS_EVENTS:
            successes.append(e)
        elif et == "profile_miss":
            misses.append(e)

    # Derive safe pattern hints from success events
    worked_hints = [e["worked"] for e in successes if e.get("worked")]

    # Derive failure hints from friction events
    failure_hints = [e["detail"] for e in friction]

    # First and last seen
    all_ts = [e["timestamp"] for e in events if e.get("timestamp")]
    first_seen = min(all_ts)[:10] if all_ts else "unknown"

    return {
        "service": service,
        "total_events": len(events),
        "friction_count": len(friction),
        "success_count": len(successes),
        "miss_count": len(misses),
        "worked_hints": worked_hints,
        "failure_hints": failure_hints,
        "first_seen": first_seen,
    }


def _draft_profile(analysis: dict) -> str:
    """Generate a profile.md-format draft from analysis data."""
    s = analysis["service"]
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    lines = [
        f"## {s}",
        "",
        f"- **Endpoint:** `{s}` (observed — verify exact endpoint)",
        f"- **Auth:** Unknown — check service docs",
    ]

    if analysis["worked_hints"]:
        unique_hints = list(dict.fromkeys(analysis["worked_hints"]))  # dedup, preserve order
        for hint in unique_hints[:3]:
            lines.append(f"- **Observed working:** {hint}")

    if analysis["failure_hints"]:
        unique_failures = list(dict.fromkeys(analysis["failure_hints"]))
        for hint in unique_failures[:3]:
            lines.append(f"- **Observed failure:** {hint}")

    if analysis["friction_count"] > 0:
        lines.append(f"- **Safe pattern:** Sequential requests recommended — {analysis['friction_count']} friction events logged")
    else:
        lines.append(f"- **Safe pattern:** No friction logged — {analysis['success_count']} successful calls observed")

    lines.append(f"- **Cache:** Recommended — add TTL appropriate to data freshness needs")
    lines.append(f"- **First observed:** {analysis['first_seen']}")
    lines.append(f"- **Auto-drafted:** {today} by promote-profile.py from {analysis['total_events']} events — review and refine before trusting")
    lines.append("")

    return "\n".join(lines)


def _append_to_profiles(draft: str) -> None:
    """Append a draft profile to the workspace profiles file (never the bundle)."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    content = PROFILES_PATH.read_text(encoding="utf-8") if PROFILES_PATH.exists() else ""
    if not content.endswith("\n"):
        content += "\n"
    content += "\n---\n\n" + draft
    PROFILES_PATH.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Promote frequently-observed services to profile entries"
    )
    parser.add_argument(
        "--min-events",
        type=int,
        default=DEFAULT_MIN_EVENTS,
        help=f"Minimum events before promoting (default: {DEFAULT_MIN_EVENTS})",
    )
    parser.add_argument(
        "--service",
        default=None,
        help="Analyze a specific service name instead of scanning all",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Append draft profiles to references/profiles.md (default: dry-run, print only)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Include services already in profiles.md (re-draft existing profiles)",
    )
    args = parser.parse_args()

    events = _load_log()
    if not events:
        print("No events in log yet. Hit some walls first.")
        return 0

    known_profiles = _load_known_profiles()

    # Group events by service
    by_service: dict[str, list[dict]] = defaultdict(list)
    for e in events:
        svc = e.get("service", "unknown")
        by_service[svc].append(e)

    # Filter to target service if specified
    if args.service:
        svc_lower = args.service.lower()
        by_service = {
            k: v for k, v in by_service.items()
            if svc_lower in k.lower()
        }
        if not by_service:
            print(f"No events found for service matching '{args.service}'")
            return 1

    candidates = []
    for service, svc_events in by_service.items():
        if len(svc_events) < args.min_events:
            continue
        if not args.all and service.lower() in known_profiles:
            continue  # Already profiled
        analysis = _analyze_service(service, svc_events)
        candidates.append(analysis)

    if not candidates:
        print(f"No unprofiled services with {args.min_events}+ events found.")
        print(f"Total services in log: {len(by_service)}")
        for svc, evts in sorted(by_service.items(), key=lambda x: -len(x[1])):
            status = "✓ profiled" if svc.lower() in known_profiles else f"{len(evts)} events (need {args.min_events})"
            print(f"  {svc}: {status}")
        return 0

    # Sort by total events descending (most-observed first)
    candidates.sort(key=lambda x: -x["total_events"])

    drafted = []
    for analysis in candidates:
        draft = _draft_profile(analysis)
        drafted.append((analysis["service"], draft))

    if args.write:
        for service, draft in drafted:
            _append_to_profiles(draft)
            print(f"✓ Drafted and appended profile for: {service}")
        print(f"\nWrote {len(drafted)} profile(s) to {PROFILES_PATH} (workspace — bundle is untouched)")
        print("Review them — auto-drafted profiles need human verification before trusting.")
    else:
        print(f"Found {len(drafted)} promotable service(s). Dry run — use --write to append.\n")
        print("=" * 60)
        for service, draft in drafted:
            print(draft)
            print("-" * 60)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
