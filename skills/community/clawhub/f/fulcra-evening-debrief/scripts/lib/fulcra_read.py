#!/usr/bin/env python3
"""Read back Fulcra custom annotation events for the concierge skills.

The concierge writes its records as MomentAnnotation events whose `data` is a JSON
string (often `{"note": "<json-string>"}`). Reading them back means:
  1. list annotation definitions (to map a human name -> definition + source_id),
  2. GET /data/v1alpha1/event/MomentAnnotation over a time range,
  3. keep events whose source matches the definition's source_id,
  4. decode the (possibly double-encoded) `data` payload into a dict.

This is the read counterpart to fulcra_annotations.py. Skills that analyze history
(evening-debrief, meeting-cadence-optimizer) import `read_annotation_events`.

CLI:
  fulcra_read.py read --name "Event Debrief" --days 30 [--raw]
  fulcra_read.py names         # list all annotation definition names

Auth: same as fulcra_annotations (FULCRA_ACCESS_TOKEN or fulcra-api CLI). No tokens printed.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fulcra_annotations as fa  # noqa: E402


def _decode_data(raw: Any) -> Any:
    """Decode an event's `data` field. It may be a JSON string, a double-encoded
    JSON string (our writers store {"note": "<json>"}), or already a dict."""
    val = raw
    for _ in range(3):  # unwrap at most a few layers; stop when it stops being JSON text
        if isinstance(val, str):
            try:
                val = json.loads(val)
                continue
            except (json.JSONDecodeError, ValueError):
                return val
        if isinstance(val, dict) and set(val.keys()) == {"note"} and isinstance(val["note"], str):
            try:
                val = json.loads(val["note"])
                continue
            except (json.JSONDecodeError, ValueError):
                return val["note"]
        break
    return val


def find_definition(name: str) -> dict[str, Any] | None:
    target = name.strip().lower()
    matches = [a for a in fa.list_annotations(include_deleted=False)
               if (a.get("name") or "").strip().lower() == target]
    matches.sort(key=lambda d: (d.get("created_at") is None, d.get("created_at", ""), d.get("id", "")))
    return matches[0] if matches else None


def read_annotation_events(name: str, *, days: float = 30.0,
                           start: datetime | None = None,
                           end: datetime | None = None) -> list[dict[str, Any]]:
    """Return decoded events for the named annotation over a window, newest last.

    Each item: {"recorded_at": <iso>, "data": <decoded dict/str>, "raw": <event>}.
    Returns [] if the definition doesn't exist or has no events in range.
    Note: find_definition resolves the annotation id; we look up the FULL record to
    get its source_id (list_annotations is normalized and drops some fields)."""
    definition = find_definition(name)
    if not definition:
        return []
    # Pull the full definition so annotation_source_id has fulcra_source_id/id to work with.
    ann_id = definition.get("id")
    full = definition
    status, body = fa.request("GET", f"/user/v1alpha1/annotation/{ann_id}")
    if status == 200 and body:
        try:
            full = json.loads(body)
        except json.JSONDecodeError:
            full = definition
    source_id = fa.annotation_source_id(full)

    end = end or datetime.now(timezone.utc)
    start = start or (end - timedelta(days=days))
    query = urllib.parse.urlencode({"start_time": start.isoformat(), "end_time": end.isoformat()})
    status, body = fa.request("GET", f"/data/v1alpha1/event/MomentAnnotation?{query}")
    if status != 200:
        return []
    try:
        events = json.loads(body)
    except json.JSONDecodeError:
        return []

    out: list[dict[str, Any]] = []
    for ev in events:
        sources = ev.get("sources") or []
        if ev.get("source_id") != source_id and source_id not in sources:
            continue
        # Readback spills the written `data` payload's keys onto the event's top level:
        # data={"note": "<json>"} comes back as a top-level `note` field (no `data` key).
        # Prefer `note`, fall back to `data`, and decode the (possibly nested) JSON.
        raw_payload = ev.get("note") if ev.get("note") is not None else ev.get("data")
        out.append({
            "recorded_at": ev.get("recorded_at") or ev.get("time") or ev.get("start_time"),
            "data": _decode_data(raw_payload),
            "raw": ev,
        })
    out.sort(key=lambda e: e.get("recorded_at") or "")
    return out


def list_definition_names() -> list[str]:
    return sorted({(a.get("name") or "") for a in fa.list_annotations()} - {""})


def main() -> int:
    p = argparse.ArgumentParser(description="Read Fulcra custom annotation events")
    sub = p.add_subparsers(dest="command", required=True)

    rd = sub.add_parser("read")
    rd.add_argument("--name", required=True)
    rd.add_argument("--days", type=float, default=30)
    rd.add_argument("--raw", action="store_true", help="Include the raw event objects")

    sub.add_parser("names")

    args = p.parse_args()
    if args.command == "read":
        events = read_annotation_events(args.name, days=args.days)
        for e in events:
            if not args.raw:
                e.pop("raw", None)
        result = {"ok": True, "name": args.name, "days": args.days, "count": len(events), "events": events}
    elif args.command == "names":
        result = {"ok": True, "names": list_definition_names()}
    else:
        result = {"ok": False, "error": "unknown command"}
    print(json.dumps(result, indent=2, sort_keys=True, default=str))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
