#!/usr/bin/env python3
"""Shared Fulcra write helper for the concierge skills.

Every concierge skill that writes a structured record does the same three things:
  1. ensure a named MomentAnnotation definition exists (create once, reuse after,
     picking the oldest match deterministically so repeated/multi-machine runs converge),
  2. POST the payload to /ingest/v1/record as a moment (recorded_at = bare ISO scalar,
     matching fulcra-common's verified wire format),
  3. read it back and report verified_matches so callers never claim success from an
     HTTP code alone.

`record_moment` is that block, written once. Skills pass a human definition name, a
payload dict (stored JSON-encoded under "note"), a source tag, and dry_run. This replaces
the per-skill copies in event_debrief.py / relationship_crm.py.

Auth + low-level HTTP/tag/verify helpers are reused from fulcra_annotations.py.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fulcra_annotations as fa  # noqa: E402


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def find_definition(name: str, defs: list[dict[str, Any]] | None = None) -> dict[str, Any] | None:
    """Oldest active definition with this canonical name, or None. Deterministic so
    repeated runs (and multiple machines) converge on one def instead of duplicating."""
    if defs is None:
        defs = fa.list_annotations(include_deleted=False)
    target = name.strip().lower()
    matches = [a for a in defs if (a.get("name") or "").strip().lower() == target]
    matches.sort(key=lambda d: (d.get("created_at") is None, d.get("created_at", ""), d.get("id", "")))
    return matches[0] if matches else None


def ensure_moment_definition(name: str, description: str, tags: Sequence[str],
                             defs: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Return the existing definition or create a new moment definition. Raises
    RuntimeError on a failed create (callers convert to an error dict)."""
    existing = find_definition(name, defs)
    if existing:
        return existing
    payload = {
        "annotation_type": "moment",
        "name": name,
        "description": description,
        "tags": fa.resolve_tags(list(tags)),
        "measurement_spec": None,
        "spec": None,
    }
    status, body = fa.request("POST", "/user/v1alpha1/annotation", payload)
    if status != 200:
        raise RuntimeError(f"create definition {name!r} failed: HTTP {status}: {body[:300]}")
    return json.loads(body)


def record_moment(*, name: str, description: str, tags: Sequence[str], payload: dict[str, Any],
                  source: str, recorded_at: str | None = None, dry_run: bool = False) -> dict[str, Any]:
    """Ensure the named moment definition, then record `payload` (JSON-encoded under
    "note") as a moment and verify the write. Returns a result dict with ok/definition_id/
    recorded_at/verified_matches (or ok=False + error)."""
    recorded_at = recorded_at or _now_iso()
    note = json.dumps(payload, sort_keys=True)

    if dry_run:
        existing = find_definition(name)
        return {
            "ok": True, "dry_run": True,
            "definition": name,
            "definition_exists": bool(existing),
            "recorded_at": recorded_at,
            "note_chars": len(note),
            "source": source,
        }

    try:
        definition = ensure_moment_definition(name, description, tags)
    except RuntimeError as exc:
        return {"ok": False, "error": str(exc)}

    source_id = fa.annotation_source_id(definition)
    record = {
        "specversion": 1,
        "data": json.dumps({"note": note}, sort_keys=True),
        "metadata": {
            "data_type": "MomentAnnotation",
            "recorded_at": recorded_at,
            "source": [source, source_id],
            "tags": definition.get("tags") or [],
            "content_type": "application/json",
        },
    }
    status, body = fa.request("POST", "/ingest/v1/record", record)
    if status != 204:
        return {"ok": False, "error": f"ingest failed: HTTP {status}: {body[:300]}"}
    # Fulcra ingest is eventually consistent — a read-back immediately after the write often
    # returns 0. Retry a few times so verified_matches reflects reality rather than lag.
    import time
    matches = 0
    for attempt in range(4):
        matches = fa.verify_record(definition, recorded_at)
        if matches:
            break
        if attempt < 3:
            time.sleep(2)
    return {
        "ok": True,  # ok reflects accepted ingest (204); verified_matches reflects readback
        "definition_id": definition.get("id"),
        "recorded_at": recorded_at,
        "verified_matches": matches,
    }
