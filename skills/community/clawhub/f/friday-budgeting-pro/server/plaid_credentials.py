"""
server/plaid_credentials.py — Per-user Plaid credential resolution.

Loads Plaid API credentials for a given user from the ``plaid_config`` table,
falling back to environment variables when the DB has no entry.

This module is intentionally lightweight with no circular imports so it can
be used by both server.main and server.health_monitor.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


def get_plaid_credentials(
    user_id: str | None,
    db_path: str | Path | None = None,
) -> tuple[str | None, str | None, str]:
    """Load Plaid credentials for *user_id* from the DB, falling back to env vars.

    Priority order:
    1. ``plaid_config`` table row for the given ``user_id``
    2. ``PLAID_CLIENT_ID`` / ``PLAID_SECRET`` / ``PLAID_ENV`` environment variables

    Parameters
    ----------
    user_id : str or None
        The user whose credentials to load.  When ``None``, only env vars are
        consulted.
    db_path : str or Path or None
        Path to the SQLite database.  Defaults to ``server.paths.DB_PATH``.

    Returns
    -------
    tuple[client_id, secret, plaid_env]
        All three values may be ``None`` (for client_id and secret) or
        ``'sandbox'`` (for plaid_env) when not configured.
    """
    if db_path is None:
        import server.paths

        db_path = server.paths.DB_PATH

    if user_id:
        try:
            import sqlite3

            conn = sqlite3.connect(str(db_path))
            conn.row_factory = sqlite3.Row
            try:
                row = conn.execute(
                    "SELECT client_id, secret, plaid_env FROM plaid_config WHERE user_id = ?",
                    (user_id,),
                ).fetchone()
                if row:
                    return row["client_id"], row["secret"], row["plaid_env"]
            finally:
                conn.close()
        except Exception:
            pass  # fall through to env vars

    return (
        os.environ.get("PLAID_CLIENT_ID"),
        os.environ.get("PLAID_SECRET"),
        os.environ.get("PLAID_ENV", "sandbox"),
    )
