#!/usr/bin/env python3
"""Opt-in local anonymous product event writer; never sends network traffic."""

from __future__ import annotations
from datetime import datetime, timezone
import json
import os
from pathlib import Path

ALLOWED = {"skill", "event", "status", "error_category", "duration_bucket", "platform"}


def sanitize(event: dict) -> dict:
    clean = {key: str(value)[:80] for key, value in event.items() if key in ALLOWED and value is not None}
    clean["timestamp"] = datetime.now(timezone.utc).isoformat()
    return clean


def emit(event: dict, environ: dict | None = None) -> bool:
    target = (environ or os.environ).get("DATAIFY_TELEMETRY_FILE", "").strip()
    if not target:
        return False
    path = Path(target).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(sanitize(event), ensure_ascii=False) + "\n")
    return True
