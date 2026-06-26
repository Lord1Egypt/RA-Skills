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
    "get_config",
    "get_device",
    "get_device_config",
    "get_devices",
    "get_seconds",
    "get_seconds_readonly",
    "init_db",
    "remove_device",
    "reset_all",
    "reset_device",
    "reset_device_config",
    "set_config",
    "update_device",
    "update_device_screen",
    "update_device_threshold",
    "migrate_schema",
    "DB_DIR",
    "DB_PATH",
    "DEFAULT_LIMIT",
    # Config key constants
    "CONFIG_KEYS",
    "KEY_SHORTS_WIDTH_THRESHOLD",
    "KEY_SHORTS_MAX_ASPECT_RATIO",
    "KEY_SHORTS_FALLBACK_HEIGHT_RATIO",
    "KEY_SHORTS_DELTA_CAP",
    "KEY_DEFAULT_SCREEN_WIDTH",
    "KEY_DEFAULT_SCREEN_HEIGHT",
    # Hardcoded defaults (last resort fallback)
    "DEFAULTS",
]

log = logging.getLogger(__name__)

DB_DIR = Path.home() / ".clawshorts"
DB_PATH = DB_DIR / "clawshorts.db"

# Default daily limit in seconds
DEFAULT_LIMIT: float = 300.0

# ---------------------------------------------------------------------------
# Config key constants
# ---------------------------------------------------------------------------

KEY_SHORTS_WIDTH_THRESHOLD = "shorts_width_threshold"
KEY_SHORTS_MAX_ASPECT_RATIO = "shorts_max_aspect_ratio"
KEY_SHORTS_FALLBACK_HEIGHT_RATIO = "shorts_fallback_height_ratio"
KEY_SHORTS_DELTA_CAP = "shorts_delta_cap"
KEY_DEFAULT_SCREEN_WIDTH = "default_screen_width"
KEY_DEFAULT_SCREEN_HEIGHT = "default_screen_height"

CONFIG_KEYS = [
    KEY_SHORTS_WIDTH_THRESHOLD,
    KEY_SHORTS_MAX_ASPECT_RATIO,
    KEY_SHORTS_FALLBACK_HEIGHT_RATIO,
    KEY_SHORTS_DELTA_CAP,
    KEY_DEFAULT_SCREEN_WIDTH,
    KEY_DEFAULT_SCREEN_HEIGHT,
]

# Last-resort hardcoded defaults (used only if DB read fails)
DEFAULTS = {
    KEY_SHORTS_WIDTH_THRESHOLD: 0.30,
    KEY_SHORTS_MAX_ASPECT_RATIO: 1.3,
    KEY_SHORTS_FALLBACK_HEIGHT_RATIO: 0.4,
    KEY_SHORTS_DELTA_CAP: 300.0,
    KEY_DEFAULT_SCREEN_WIDTH: 1920.0,
    KEY_DEFAULT_SCREEN_HEIGHT: 1080.0,
}

# Config key → devices table column mapping (None = not per-device overridable)
KEY_TO_DEVICE_COLUMN = {
    KEY_SHORTS_WIDTH_THRESHOLD: "width_threshold",
    KEY_SHORTS_MAX_ASPECT_RATIO: "max_aspect_ratio",
    KEY_SHORTS_FALLBACK_HEIGHT_RATIO: "fallback_height_ratio",
    KEY_SHORTS_DELTA_CAP: "delta_cap",
    KEY_DEFAULT_SCREEN_WIDTH: "screen_width",
    KEY_DEFAULT_SCREEN_HEIGHT: "screen_height",
}


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
    # Run schema migration (adds config table + new device columns if needed)
    migrate_schema()
    # Security: set restrictive permissions (owner only)
    try:
        os.chmod(DB_PATH, 0o600)
    except OSError:
        pass
    log.info("DB ready: %s", DB_PATH)


# ---------------------------------------------------------------------------
# Schema migration
# ---------------------------------------------------------------------------

def migrate_schema() -> None:
    """Zero-downtime migration: add config table and device columns if not exist."""
    with _db() as conn:
        # --- config table ---
        conn.execute("""
            CREATE TABLE IF NOT EXISTS config (
                key          TEXT PRIMARY KEY,
                value        REAL NOT NULL,
                description  TEXT,
                updated_at   TEXT DEFAULT (datetime('now'))
            )
        """)

        # Seed global defaults only for keys not yet present
        defaults = [
            (KEY_SHORTS_WIDTH_THRESHOLD, 0.30, "player width must be < this ratio of screen width"),
            (KEY_SHORTS_MAX_ASPECT_RATIO, 1.3, "portrait aspect ratio cap; ar < this = portrait"),
            (KEY_SHORTS_FALLBACK_HEIGHT_RATIO, 0.4, "fallback: player height must exceed this ratio of screen height"),
            (KEY_SHORTS_DELTA_CAP, 300.0, "max seconds accumulated per poll (prevents clock jumps)"),
            (KEY_DEFAULT_SCREEN_WIDTH, 1920.0, "fallback assumed screen width"),
            (KEY_DEFAULT_SCREEN_HEIGHT, 1080.0, "fallback assumed screen height"),
        ]
        for key, value, description in defaults:
            conn.execute(
                """
                INSERT OR IGNORE INTO config (key, value, description)
                VALUES (?, ?, ?)
                """,
                (key, value, description),
            )

        # --- devices table new columns ---
        new_device_columns = [
            ("screen_width", "INTEGER"),
            ("screen_height", "INTEGER"),
            ("width_threshold", "REAL"),
            ("max_aspect_ratio", "REAL"),
            ("fallback_height_ratio", "REAL"),
            ("delta_cap", "REAL"),
        ]
        # Get existing columns
        existing = {row[1] for row in conn.execute("PRAGMA table_info(devices)").fetchall()}
        for col_name, col_type in new_device_columns:
            if col_name not in existing:
                conn.execute(f"ALTER TABLE devices ADD COLUMN {col_name} {col_type}")
        # updated_at column
        if "updated_at" not in existing:
            conn.execute("ALTER TABLE devices ADD COLUMN updated_at TEXT")
            conn.execute("UPDATE devices SET updated_at = datetime('now') WHERE updated_at IS NULL")

    log.info("Schema migration complete.")


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
    """Return a device dict or None if not found. Includes all per-device config columns."""
    conn = sqlite3.connect(str(DB_PATH), timeout=5, isolation_level=None)
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        row = conn.execute(
            """SELECT ip, name, limit_val, enabled,
                      screen_width, screen_height,
                      width_threshold, max_aspect_ratio,
                      fallback_height_ratio, delta_cap
               FROM devices WHERE ip=?""",
            (ip,),
        ).fetchone()
        if row:
            return {
                "ip": row[0],
                "name": row[1],
                "limit_val": row[2],
                "enabled": bool(row[3]),
                "screen_width": row[4],
                "screen_height": row[5],
                "width_threshold": row[6],
                "max_aspect_ratio": row[7],
                "fallback_height_ratio": row[8],
                "delta_cap": row[9],
            }
        return None
    finally:
        conn.close()


def get_devices() -> list[dict]:
    """Return all configured devices. Includes per-device config columns."""
    conn = sqlite3.connect(str(DB_PATH), timeout=5, isolation_level=None)
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        rows = conn.execute(
            """SELECT ip, name, limit_val, enabled,
                      screen_width, screen_height,
                      width_threshold, max_aspect_ratio,
                      fallback_height_ratio, delta_cap
               FROM devices WHERE enabled=1"""
        ).fetchall()
        return [
            {
                "ip": r[0],
                "name": r[1],
                "limit_val": r[2],
                "enabled": bool(r[3]),
                "screen_width": r[4],
                "screen_height": r[5],
                "width_threshold": r[6],
                "max_aspect_ratio": r[7],
                "fallback_height_ratio": r[8],
                "delta_cap": r[9],
            }
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
    """Update device fields. Supported: name, limit_val, enabled, and all per-device config columns."""
    allowed = {
        "name", "limit_val", "enabled",
        "screen_width", "screen_height",
        "width_threshold", "max_aspect_ratio",
        "fallback_height_ratio", "delta_cap",
    }
    updates = {k: v for k, v in kwargs.items() if k in allowed}
    if not updates:
        return get_device(ip)
    set_clause = ", ".join(f"{k}=?" for k in updates)
    values = list(updates.values()) + [ip]
    with _db(immediate=True) as conn:
        conn.execute(f"UPDATE devices SET {set_clause} WHERE ip=?", values)
    return get_device(ip)


# ---------------------------------------------------------------------------
# Global config management
# ---------------------------------------------------------------------------

def get_config(key: str) -> float | None:
    """Return a global config value, or None if not found."""
    conn = sqlite3.connect(str(DB_PATH), timeout=5, isolation_level=None)
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        row = conn.execute(
            "SELECT value FROM config WHERE key=?", (key,)
        ).fetchone()
        return float(row[0]) if row else None
    finally:
        conn.close()


def set_config(key: str, value: float) -> None:
    """Set a global config value (upsert)."""
    with _db(immediate=True) as conn:
        conn.execute(
            """INSERT INTO config (key, value, updated_at)
               VALUES (?, ?, datetime('now'))
               ON CONFLICT(key) DO UPDATE SET
                   value = excluded.value,
                   updated_at = datetime('now')""",
            (key, value),
        )


def get_all_config() -> dict[str, float]:
    """Return all global config key-value pairs."""
    conn = sqlite3.connect(str(DB_PATH), timeout=5, isolation_level=None)
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        rows = conn.execute("SELECT key, value FROM config").fetchall()
        return {key: float(value) for key, value in rows}
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Per-device config helpers
# ---------------------------------------------------------------------------

def get_device_config(ip: str) -> dict | None:
    """Return per-device config columns, or None if device not found."""
    return get_device(ip)


def update_device_screen(ip: str, width: int, height: int) -> dict | None:
    """Update device screen resolution."""
    return update_device(ip, screen_width=width, screen_height=height)


def update_device_threshold(
    ip: str,
    width_threshold: float | None = None,
    max_aspect_ratio: float | None = None,
    fallback_height_ratio: float | None = None,
    delta_cap: float | None = None,
) -> dict | None:
    """Update one or more detection thresholds for a device."""
    kwargs = {}
    if width_threshold is not None:
        kwargs["width_threshold"] = width_threshold
    if max_aspect_ratio is not None:
        kwargs["max_aspect_ratio"] = max_aspect_ratio
    if fallback_height_ratio is not None:
        kwargs["fallback_height_ratio"] = fallback_height_ratio
    if delta_cap is not None:
        kwargs["delta_cap"] = delta_cap
    if not kwargs:
        return get_device(ip)
    return update_device(ip, **kwargs)


def reset_device_config(ip: str) -> dict | None:
    """Clear per-device threshold overrides → NULL (falls back to global defaults).

    Note: screen_width/screen_height are NOT reset — they are stable device
    properties set by auto-detection and should persist across config resets.
    """
    threshold_cols = [
        "width_threshold", "max_aspect_ratio",
        "fallback_height_ratio", "delta_cap",
    ]
    set_clause = ", ".join(f"{col}=NULL" for col in threshold_cols)
    with _db(immediate=True) as conn:
        conn.execute(f"UPDATE devices SET {set_clause} WHERE ip=?", (ip,))
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
