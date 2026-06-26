# FILE_META
# INPUT:  PipelineOptions (hermes_state_db override, session_id filter, ...)
# OUTPUT: iterable of SessionHandle (one per Hermes session on disk)
# POS:    skill lib adapters/hermes — session enumeration
# MISSION: Enumerate Hermes sessions via direct SQLite read (read-only, immutable URI).

"""Enumerate Hermes sessions.

Strategy:
  1. Open ``~/.hermes/state.db`` read-only.
  2. ``SELECT session_id, started_at, model, ... FROM sessions``.
  3. Probe for optional columns before referencing them so we survive
     minor schema drift across Hermes versions.

We do **not** shell out to ``hermes sessions list`` even though it
exists: the CLI requires an interactive Hermes install and may block on
config prompts. Direct SQLite reads are strictly local and side-effect
free.

NOTE: Not validated against a real Hermes install yet (see docs/adapter-
design.md §12 risk #2). Column name assumptions are based on public docs;
schema drift protection is implemented but specific field names may need
adjustment after a real-data smoke test in P1-8.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Any, Iterable

from .. import SessionHandle
from ._db import column_names, open_readonly, table_exists, HermesNotInstalled


# Fields we try to read from ``sessions``. The first existing column in
# each tuple wins; ``None`` fallback means the field is optional.
_CANDIDATE_COLS: dict[str, tuple[str, ...]] = {
    "session_id": ("session_id", "id"),
    "started_at": ("started_at", "created_at"),
    "model": ("model", "default_model"),
    "cwd": ("cwd", "working_dir"),
    "message_count": ("message_count", "msg_count"),
}


def _parse_ts(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        # assume unix seconds if <1e12, else milliseconds
        ts = float(value)
        if ts > 1e12:
            ts /= 1000
        return datetime.fromtimestamp(ts, tz=timezone.utc)
    if isinstance(value, str):
        s = value.replace("Z", "+00:00") if value.endswith("Z") else value
        try:
            return datetime.fromisoformat(s)
        except ValueError:
            return None
    return None


def _pick_column(available: set[str], candidates: tuple[str, ...]) -> str | None:
    for c in candidates:
        if c in available:
            return c
    return None


def discover(opts: Any = None) -> Iterable[SessionHandle]:
    """Yield one SessionHandle per Hermes session.

    Raises ``HermesNotInstalled`` if the state.db is missing — callers
    decide whether that's fatal (user ran with --adapter hermes) or
    expected (auto-probing available adapters).
    """
    conn = open_readonly(opts)
    try:
        if not table_exists(conn, "sessions"):
            return

        cols = set(column_names(conn, "sessions"))
        chosen: dict[str, str | None] = {
            key: _pick_column(cols, candidates)
            for key, candidates in _CANDIDATE_COLS.items()
        }
        if chosen["session_id"] is None:
            raise RuntimeError(
                f"Hermes schema has no session_id column; saw: {sorted(cols)}"
            )

        select_list = []
        for key, col in chosen.items():
            if col is None:
                select_list.append(f"NULL AS {key}")
            else:
                select_list.append(f"{col} AS {key}")

        query = f"SELECT {', '.join(select_list)} FROM sessions ORDER BY started_at"
        for row in conn.execute(query):
            yield _row_to_handle(row, opts)
    finally:
        conn.close()


def _row_to_handle(row: sqlite3.Row, _opts: Any) -> SessionHandle:
    d = dict(row)
    started = _parse_ts(d.get("started_at"))
    return SessionHandle(
        adapter="hermes",
        session_id=str(d["session_id"]),
        path=None,  # sessions live inside the SQLite DB, no individual file
        cwd=d.get("cwd"),
        model=d.get("model"),
        started_at=started,
        size_bytes=0,  # populated in parse.py (cost of messages SELECT)
        extras={
            "message_count": d.get("message_count"),
        },
    )


__all__ = ["discover", "HermesNotInstalled"]
