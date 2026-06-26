"""ClawShorts SQLite helper — tracks daily YouTube Shorts watch time.

One table:  daily_usage(ip, date, seconds)
Database:   ~/.clawshorts/clawshorts.db
"""
from __future__ import annotations

import logging
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

__all__ = [
    "add_device",
    "add_seconds",
    "get_device",
    "get_devices",
    "get_seconds",
    "get_seconds_readonly",
    "init_db",
    "remove_device",
    "reset_all",
    "reset_device",
    "update_device",
    "DB_DIR",
    "DB_PATH",
    "DEFAULT_LIMIT",
]

log = logging.getLogger(__name__)

DB_DIR = Path.home() / ".clawshorts"
DB_PATH = DB_DIR / "clawshorts.db"

# Default daily limit in seconds
DEFAULT_LIMIT: float = 300.0


# ---------------------------------------------------------------------------
# Connection context manager
# ---------------------------------------------------------------------------

@contextmanager
def _db(*, immediate: bool = False):
    """Yield a WAL-mode SQLite connection that auto-commits."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    if immediate:
        conn.execute("BEGIN IMMEDIATE")
    try:
        yield conn
        conn.commit()
    except BaseException:
        conn.rollback()
        raise
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

def init_db() -> None:
    """Create the devices and daily_usage tables if they don't exist."""
    with _db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS devices (
                ip        TEXT PRIMARY KEY,
                name      TEXT,
                limit_val REAL NOT NULL DEFAULT 300.0,
                enabled   INTEGER NOT NULL DEFAULT 1
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS daily_usage (
                ip      TEXT NOT NULL,
                date    TEXT NOT NULL,
                seconds REAL NOT NULL DEFAULT 0.0,
                PRIMARY KEY (ip, date)
            )
        """)
    # Security: set restrictive permissions (owner only)
    try:
        os.chmod(DB_PATH, 0o600)
    except OSError:
        pass
    log.info("DB ready: %s", DB_PATH)


# ---------------------------------------------------------------------------
# Device management
# ---------------------------------------------------------------------------

def add_device(ip: str, name: str | None = None, limit_val: float = DEFAULT_LIMIT) -> dict:
    """Add a device. Replaces if IP already exists. Returns the device dict."""
    with _db(immediate=True) as conn:
        conn.execute(
            """
            INSERT INTO devices(ip, name, limit_val, enabled)
            VALUES (?, ?, ?, 1)
            ON CONFLICT(ip) DO UPDATE SET
                name = excluded.name,
                limit_val = excluded.limit_val,
                enabled = 1
            """,
            (ip, name, limit_val),
        )
        return {"ip": ip, "name": name, "limit_val": limit_val, "enabled": True}


def get_device(ip: str) -> dict | None:
    """Return a device dict or None if not found."""
    conn = sqlite3.connect(str(DB_PATH), timeout=5, isolation_level=None)
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        row = conn.execute(
            "SELECT ip, name, limit_val, enabled FROM devices WHERE ip=?",
            (ip,),
        ).fetchone()
        if row:
            return {"ip": row[0], "name": row[1], "limit_val": row[2], "enabled": bool(row[3])}
        return None
    finally:
        conn.close()


def get_devices() -> list[dict]:
    """Return all configured devices."""
    conn = sqlite3.connect(str(DB_PATH), timeout=5, isolation_level=None)
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        rows = conn.execute(
            "SELECT ip, name, limit_val, enabled FROM devices WHERE enabled=1"
        ).fetchall()
        return [
            {"ip": r[0], "name": r[1], "limit_val": r[2], "enabled": bool(r[3])}
            for r in rows
        ]
    finally:
        conn.close()


def remove_device(ip: str) -> bool:
    """Remove a device. Returns True if found and deleted."""
    with _db(immediate=True) as conn:
        cur = conn.execute("DELETE FROM devices WHERE ip=?", (ip,))
        return cur.rowcount > 0


def update_device(ip: str, **kwargs: any) -> dict | None:
    """Update device fields. Supported: name, limit_val, enabled."""
    allowed = {"name", "limit_val", "enabled"}
    updates = {k: v for k, v in kwargs.items() if k in allowed}
    if not updates:
        return get_device(ip)
    set_clause = ", ".join(f"{k}=?" for k in updates)
    values = list(updates.values()) + [ip]
    with _db(immediate=True) as conn:
        conn.execute(f"UPDATE devices SET {set_clause} WHERE ip=?", values)
    return get_device(ip)


# ---------------------------------------------------------------------------
# Read / write
# ---------------------------------------------------------------------------

def add_seconds(ip: str, date: str, delta: float) -> None:
    """Add delta seconds to the daily total for the device.

    Non-positive deltas are ignored. Large deltas are capped to prevent abuse.
    """
    if delta <= 0:
        return
    # Cap delta to prevent abuse / clock skew (max 5 minutes per poll)
    delta = min(delta, 300)
    with _db(immediate=True) as conn:
        conn.execute(
            """
            INSERT INTO daily_usage(ip, date, seconds) VALUES(?, ?, ?)
            ON CONFLICT(ip, date) DO UPDATE SET seconds = seconds + excluded.seconds
            """,
            (ip, date, delta),
        )


def get_seconds(ip: str, date: str) -> float:
    """Return the total seconds watched for the device on the given date."""
    with _db() as conn:
        row = conn.execute(
            "SELECT seconds FROM daily_usage WHERE ip=? AND date=?", (ip, date)
        ).fetchone()
        return float(row[0]) if row else 0.0


def get_seconds_readonly(ip: str, date: str) -> float:
    """Return seconds for the device/date without transaction overhead.

    Use this for read-only, non-time-sensitive queries.
    """
    conn = sqlite3.connect(str(DB_PATH), timeout=5, isolation_level=None)
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        row = conn.execute(
            "SELECT seconds FROM daily_usage WHERE ip=? AND date=?", (ip, date)
        ).fetchone()
        return float(row[0]) if row else 0.0
    finally:
        conn.close()


def get_history(ip: str | None, start_date: str, end_date: str):
    """Return usage history rows for a date range.

    If ip is None, returns all devices.
    Returns: list of (date, ip, seconds, limit_val) tuples.
    """
    conn = sqlite3.connect(str(DB_PATH), timeout=5, isolation_level=None)
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        if ip:
            rows = conn.execute(
                """SELECT d.date, d.ip, d.seconds, COALESCE(dev.limit_val, 300) as limit_val
                   FROM daily_usage d
                   LEFT JOIN devices dev ON d.ip = dev.ip
                   WHERE d.date >= ? AND d.date <= ? AND d.ip = ?
                   ORDER BY d.date DESC""",
                (start_date, end_date, ip),
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT d.date, d.ip, d.seconds, COALESCE(dev.limit_val, 300) as limit_val
                   FROM daily_usage d
                   LEFT JOIN devices dev ON d.ip = dev.ip
                   WHERE d.date >= ? AND d.date <= ?
                   ORDER BY d.date DESC""",
                (start_date, end_date),
            ).fetchall()
        return rows
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Reset
# ---------------------------------------------------------------------------

def reset_device(ip: str) -> None:
    """Reset all usage records for a specific device."""
    with _db() as conn:
        conn.execute("DELETE FROM daily_usage WHERE ip=?", (ip,))


def reset_all() -> None:
    """Reset all usage records for all devices."""
    with _db() as conn:
        conn.execute("DELETE FROM daily_usage")
