#!/usr/bin/env python3
"""Concierge readiness check: what's installed and wired up.

The wrapper uses this to degrade gracefully -- run what's available, skip (and name)
what isn't, never block the whole sequence on one missing piece.

  status

Reports, per concierge skill: whether its directory + entry script exist. Plus:
  - fulcra_auth : can we get a Fulcra token? (non-fatal probe)
  - attio_key   : is ATTIO_API_KEY configured? (does NOT validate it over the network)

No secrets are printed -- only booleans.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import concierge_bootstrap  # noqa: F401

SKILLS_DIR = Path.home() / ".claude" / "skills"

# skill dir -> entry script under scripts/
SKILLS = {
    "subjective-checkin": "fulcra_checkin.py",
    "morning-briefing": "collect.py",
    "post-experience-rater": "post_experience.py",
    "evening-debrief": "evening_debrief.py",
    "meeting-cadence-optimizer": "cadence.py",
    "event-debrief": "event_debrief.py",
    "relationship-crm": "relationship_crm.py",
}


def check_fulcra() -> dict:
    try:
        sys.path.insert(0, str(Path.home() / ".fulcra-concierge" / "lib"))
        import fulcra_annotations as fa
        tok = fa.access_token()  # raises/exits if unavailable
        return {"available": bool(tok)}
    except SystemExit:
        return {"available": False, "reason": "no Fulcra token (run: uv tool run fulcra-api auth login)"}
    except Exception as exc:
        return {"available": False, "reason": str(exc)[:200]}


def check_attio() -> dict:
    try:
        import concierge_secrets as s
        return {"configured": s.has_secret("ATTIO_API_KEY")}
    except Exception as exc:
        return {"configured": False, "reason": str(exc)[:200]}


def main() -> int:
    argparse.ArgumentParser(description="Concierge readiness").parse_args()
    skills = {}
    for name, entry in SKILLS.items():
        d = SKILLS_DIR / name
        skills[name] = {
            "installed": d.is_dir(),
            "entry_ok": (d / "scripts" / entry).exists(),
        }
    result = {
        "ok": True,
        "skills": skills,
        "installed_count": sum(1 for v in skills.values() if v["entry_ok"]),
        "fulcra_auth": check_fulcra(),
        "attio_key": check_attio(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
