"""Lightweight per-negotiation trace logging.

The trace is intentionally local and append-only. sshsign remains the
source of truth for shared workflow state; this file is an operator aid for
answering "which process sent which card and why?" after a Telegram report.
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any


def trace_path(output_dir: str | Path) -> Path:
    return Path(output_dir) / "trace.ndjson"


def write_trace(
    output_dir: str | Path,
    event_type: str,
    **fields: Any,
) -> None:
    """Append one structured trace event.

    Best effort by design: tracing must never break the negotiation flow.
    """
    if not output_dir:
        return
    record = {
        "ts": time.time(),
        "event_type": event_type,
        "pid": os.getpid(),
    }
    for key, value in fields.items():
        if value is not None:
            record[key] = value
    try:
        p = trace_path(output_dir)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, sort_keys=True) + "\n")
    except OSError:
        pass

