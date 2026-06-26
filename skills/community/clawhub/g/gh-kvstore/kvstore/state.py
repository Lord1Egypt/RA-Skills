"""
In-memory key-value store with TTL support.
"""

import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Entry:
    key: str
    value: Any
    created_at: float = field(default_factory=time.monotonic)
    ttl_seconds: float | None = None

    @property
    def expired(self) -> bool:
        if self.ttl_seconds is None:
            return False
        return time.monotonic() - self.created_at > self.ttl_seconds

    @property
    def ttl_remaining(self) -> int | None:
        if self.ttl_seconds is None:
            return None
        remaining = self.ttl_seconds - (time.monotonic() - self.created_at)
        return max(0, int(remaining))


_store: dict[str, Entry] = {}
_hits: int = 0
_misses: int = 0


def set_key(key: str, value: Any, ttl_seconds: float | None = None) -> Entry:
    entry = Entry(key=key, value=value, ttl_seconds=ttl_seconds)
    _store[key] = entry
    return entry


def get_key(key: str) -> Entry | None:
    global _hits, _misses
    entry = _store.get(key)
    if entry is None:
        _misses += 1
        return None
    if entry.expired:
        del _store[key]
        _misses += 1
        return None
    _hits += 1
    return entry


def delete_key(key: str) -> bool:
    return _store.pop(key, None) is not None


def list_keys(prefix: str | None = None) -> list[str]:
    # Prune expired
    expired = [k for k, v in _store.items() if v.expired]
    for k in expired:
        del _store[k]

    if prefix:
        return sorted(k for k in _store if k.startswith(prefix))
    return sorted(_store.keys())


def flush_all() -> int:
    count = len(_store)
    _store.clear()
    return count


def stats() -> dict[str, int]:
    # Prune expired
    expired = [k for k, v in _store.items() if v.expired]
    for k in expired:
        del _store[k]
    return {"total_keys": len(_store), "hits": _hits, "misses": _misses}
