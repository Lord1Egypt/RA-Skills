# FILE_META
# INPUT:  server_url, secret_key, output_dir
# OUTPUT: manifest.json updated with server-side submissions (idempotent merge)
# POS:    skill scripts — utility, depends on query.py + adapters/openclaw/_manifest.py
# MISSION: Reconcile local manifest with server's /submissions so previously-submitted
#          sessions don't resurface in the scan list (e.g. after losing local state).

#!/usr/bin/env python3
"""Sync server-side submissions into the local OpenClaw manifest.

Walks ``GET /submissions`` page by page, adds any ``session_id`` missing
from ``manifest["submitted"]`` with a ``server_response="synced"`` marker
so future scans skip them just like locally-uploaded sessions.

Also clears ``manifest["rejected"]`` on a successful sweep — those entries
are a stale cache of past local filter decisions (turns_too_low / no_cache_trace
/ model_mismatch / …) that should be re-evaluated against the current config
whenever we're reconciling state anyway.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from lib.adapters.openclaw._manifest import load_manifest, save_manifest
from query import query_submissions


SYNC_PAGE_SIZE = 100


def sync_manifest_from_server(
    server_url: str,
    secret_key: str,
    output_dir: str,
) -> dict:
    """Merge all server-side session_ids into the local manifest.

    Returns ``{"added": int, "existing": int, "cleared_rejected": int,
    "total": int, "error": str|None}``. Idempotent for the submitted side:
    already-recorded submissions are left untouched so real upload timestamps
    are preserved; only brand-new entries get ``submitted_at`` from the server
    and ``server_response="synced"``.

    On a successful sweep, ``manifest["rejected"]`` is wiped — those entries
    are just a cache of past filter decisions, and we want them re-evaluated
    against the current config on the next scan. If the sweep fails mid-way,
    the manifest is left untouched.
    """
    # Fetch page 1 to learn the total count
    first = query_submissions(server_url, secret_key, page=1, page_size=SYNC_PAGE_SIZE)
    if "error" in first:
        return {
            "added": 0,
            "existing": 0,
            "cleared_rejected": 0,
            "total": 0,
            "error": first.get("message") or first["error"],
        }

    total = int(first.get("total") or 0)
    total_pages = (total + SYNC_PAGE_SIZE - 1) // SYNC_PAGE_SIZE
    all_items: list[dict] = list(first.get("items") or [])

    for page in range(2, total_pages + 1):
        resp = query_submissions(server_url, secret_key, page=page, page_size=SYNC_PAGE_SIZE)
        if "error" in resp:
            return {
                "added": 0,
                "existing": 0,
                "cleared_rejected": 0,
                "total": total,
                "error": resp.get("message") or resp["error"],
            }
        all_items.extend(resp.get("items") or [])

    # Sweep succeeded — safe to reconcile local state.
    manifest = load_manifest(output_dir)
    submitted = manifest.setdefault("submitted", {})
    rejected = manifest.get("rejected") or {}

    cleared_rejected = len(rejected)
    if cleared_rejected:
        manifest["rejected"] = {}

    added = 0
    existing = 0
    for item in all_items:
        session_id = item.get("session_id")
        if not session_id:
            continue
        key = f"{session_id}.trajectory.json"
        if key in submitted:
            existing += 1
            continue
        submitted[key] = {
            "submitted_at": item.get("submitted_at") or "",
            "server_response": "synced",
        }
        added += 1

    if added or cleared_rejected:
        save_manifest(output_dir, manifest)

    return {
        "added": added,
        "existing": existing,
        "cleared_rejected": cleared_rejected,
        "total": total,
        "error": None,
    }
