# FILE_META
# INPUT:  PipelineOptions (for db_path override) or None
# OUTPUT: sqlite3.Connection (read-only, immutable URI)
# POS:    skill lib adapters/hermes — private SQLite access helper
# MISSION: Locate Hermes state.db and return a safe read-only connection.

"""Locate and open the Hermes SQLite store.

Access strategy:
  - ``HERMES_STATE_DB`` env var wins (useful for tests / non-default installs)
  - otherwise ``~/.hermes/state.db``

All connections are opened **read-only via URI immutable=1** so we never
risk corrupting a running Hermes instance that has the file open in WAL
mode.
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any

DEFAULT_STATE_DB = "~/.hermes/state.db"


class HermesNotInstalled(RuntimeError):
    """Raised when ~/.hermes/state.db cannot be located."""


def resolve_db_path(opts: Any = None) -> Path:
    """Resolve which state.db to read.

    Precedence: env ``HERMES_STATE_DB`` > ``opts.hermes_state_db`` > default.
    """
    env_override = os.environ.get("HERMES_STATE_DB")
    if env_override:
        return Path(env_override).expanduser()
    opts_override = getattr(opts, "hermes_state_db", None) if opts is not None else None
    if opts_override:
        return Path(opts_override).expanduser()
    return Path(DEFAULT_STATE_DB).expanduser()


def open_readonly(opts: Any = None) -> sqlite3.Connection:
    """Open the Hermes db read-only. Raises HermesNotInstalled if missing."""
    path = resolve_db_path(opts)
    if not path.is_file():
        raise HermesNotInstalled(f"Hermes state.db not found at {path}")
    # immutable=1 promises "the file will not change while open". It is the
    # right flag for read-only analysis; Hermes's own process is the writer.
    uri = f"file:{path}?mode=ro&immutable=1"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def table_exists(conn: sqlite3.Connection, name: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name = ? LIMIT 1",
        (name,),
    ).fetchone()
    return row is not None


def column_names(conn: sqlite3.Connection, table: str) -> list[str]:
    """Return column names for a table (used for schema compatibility probing)."""
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return [r[1] for r in rows]
