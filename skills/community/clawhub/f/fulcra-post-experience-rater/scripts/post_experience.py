#!/usr/bin/env python3
"""Post-Experience Rater: a 15-second micro-rating, stored in Fulcra.

These ratings build the preference graph other concierge skills draw on (e.g. a future
restaurant recommender). The conversation is the agent's job; this script does the write.

  save --payload <file.json> [--dry-run]

Payload schema:
{
  "experience_type": "restaurant|hotel|event|person|other",
  "name": "Carbone",
  "scores": {"food": 5, "vibe": 4, "service": 3},   // any 1-5 keys; type-appropriate
  "would_return": true,
  "notes": "Too loud for a date night but the pasta was incredible. Bar seats are better.",
  "companions": ["Jordan"],
  "tags": ["italian", "west village", "special occasion"]
}

Writes one "Post-Experience Rating" moment annotation carrying the full JSON. Verifies
the write (verified_matches). Auth: Fulcra via fulcra-api CLI / FULCRA_ACCESS_TOKEN.
No tokens printed.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import concierge_bootstrap  # noqa: F401

import concierge_fulcra as cf  # noqa: E402

ANNOTATION_NAME = "Post-Experience Rating"
ANNOTATION_DESC = "Quick rating of a restaurant/hotel/event/person captured by the concierge post-experience-rater skill."
ANNOTATION_TAGS = ["post-experience", "concierge"]
SOURCE = "com.fulcra.post-experience"

KEEP = ("experience_type", "name", "scores", "would_return", "notes", "companions", "tags")


def cmd_save(args: argparse.Namespace) -> dict:
    payload = json.loads(Path(args.payload).read_text(encoding="utf-8-sig"))
    recorded_at = payload.get("timestamp") or datetime.now(timezone.utc).isoformat()
    record = {k: payload.get(k) for k in KEEP if payload.get(k) is not None}
    if not record.get("name"):
        return {"ok": False, "error": "payload needs at least a 'name'"}
    res = cf.record_moment(
        name=ANNOTATION_NAME, description=ANNOTATION_DESC, tags=ANNOTATION_TAGS,
        payload=record, source=SOURCE, recorded_at=recorded_at, dry_run=args.dry_run,
    )
    return {"ok": res.get("ok", False), "experience": record.get("name"), "fulcra": res,
            "payload_preview": record if args.dry_run else None}


def main() -> int:
    p = argparse.ArgumentParser(description="Post-Experience Rater")
    sub = p.add_subparsers(dest="command", required=True)
    sv = sub.add_parser("save")
    sv.add_argument("--payload", required=True)
    sv.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    result = cmd_save(args) if args.command == "save" else {"ok": False, "error": "unknown command"}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
