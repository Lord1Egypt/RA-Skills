#!/usr/bin/env python3
"""Persistent metadata cache and provider cooldown state (SQLite, stdlib only)."""

from __future__ import annotations

import json
import os
import sqlite3
import time
from pathlib import Path
from typing import Any, Callable, Dict, Optional

from common_config import get_env_str

Now = Callable[[], float]

_SCHEMA = """
CREATE TABLE IF NOT EXISTS lookups (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    expires_at REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS cooldowns (
    provider TEXT PRIMARY KEY,
    until REAL NOT NULL,
    reason TEXT
);
"""


def default_cache_path() -> Optional[Path]:
    """Return the cache file path, or None when caching is disabled."""
    if get_env_str("BOOK_CAPTURE_CACHE", "on").lower() in {"0", "off", "false", "no"}:
        return None
    explicit = get_env_str("BOOK_CAPTURE_CACHE_DIR", "")
    if explicit:
        base = Path(explicit).expanduser()
    else:
        xdg = os.getenv("XDG_CACHE_HOME", "").strip()
        base = (Path(xdg).expanduser() if xdg else Path.home() / ".cache") / "book-capture-obsidian"
    return base / "metadata.sqlite3"


class MetadataCache:
    """Key/value cache with expiry plus per-provider cooldowns.

    With ``path=None`` everything lives in memory for the current process, so
    callers never need to branch on whether caching is enabled.
    """

    def __init__(self, path: Optional[Path], now: Now = time.time):
        self._now = now
        self._path = path
        self._memory: Dict[str, Any] = {}
        self._memory_cooldowns: Dict[str, float] = {}
        self._conn: Optional[sqlite3.Connection] = None
        if path is not None:
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                self._conn = sqlite3.connect(str(path), timeout=5)
                self._conn.executescript(_SCHEMA)
                self._conn.commit()
            except Exception:
                # A broken cache must never break a capture; fall back to memory.
                self._conn = None

    @property
    def persistent(self) -> bool:
        return self._conn is not None

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        now = self._now()
        if self._conn is None:
            entry = self._memory.get(key)
            if entry and entry[1] > now:
                return entry[0]
            return None
        row = self._conn.execute(
            "SELECT value, expires_at FROM lookups WHERE key = ?", (key,)
        ).fetchone()
        if not row or row[1] <= now:
            return None
        try:
            value = json.loads(row[0])
        except ValueError:
            return None
        return value if isinstance(value, dict) else None

    def put(self, key: str, value: Dict[str, Any], ttl_days: float) -> None:
        expires_at = self._now() + max(0.0, ttl_days) * 86400.0
        if self._conn is None:
            self._memory[key] = (value, expires_at)
            return
        self._conn.execute(
            "INSERT OR REPLACE INTO lookups (key, value, expires_at) VALUES (?, ?, ?)",
            (key, json.dumps(value, ensure_ascii=False, sort_keys=True), expires_at),
        )
        self._conn.commit()

    def cooldown_until(self, provider: str) -> Optional[float]:
        now = self._now()
        if self._conn is None:
            until = self._memory_cooldowns.get(provider)
        else:
            row = self._conn.execute(
                "SELECT until FROM cooldowns WHERE provider = ?", (provider,)
            ).fetchone()
            until = row[0] if row else None
        return until if until and until > now else None

    def set_cooldown(self, provider: str, seconds: float, reason: str) -> float:
        until = self._now() + max(0.0, seconds)
        if self._conn is None:
            self._memory_cooldowns[provider] = until
            return until
        self._conn.execute(
            "INSERT OR REPLACE INTO cooldowns (provider, until, reason) VALUES (?, ?, ?)",
            (provider, until, reason),
        )
        self._conn.commit()
        return until

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None
