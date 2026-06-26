"""In-memory TTL cache — stdlib only, thread-safe."""

from __future__ import annotations

import threading
import time
from typing import Any, Hashable


class TTLCache:
    """Simple thread-safe TTL cache using a dict + expiry timestamps.

    Args:
        maxsize: Maximum number of entries.
        ttl: Default time-to-live in seconds for each entry.
    """

    def __init__(self, maxsize: int = 128, ttl: float = 300.0):
        self._maxsize = maxsize
        self._ttl = ttl
        self._data: dict[Hashable, tuple[Any, float]] = {}
        self._lock = threading.Lock()

    def get(self, key: Hashable, default: Any = None) -> Any:
        with self._lock:
            entry = self._data.get(key)
            if entry is None:
                return default
            value, expires_at = entry
            if time.monotonic() > expires_at:
                del self._data[key]
                return default
            return value

    def set(self, key: Hashable, value: Any, ttl: float | None = None) -> None:
        expires_at = time.monotonic() + (ttl if ttl is not None else self._ttl)
        with self._lock:
            self._data[key] = (value, expires_at)
            if len(self._data) > self._maxsize:
                self._evict()

    def delete(self, key: Hashable) -> bool:
        with self._lock:
            return self._data.pop(key, None) is not None

    def clear(self) -> None:
        with self._lock:
            self._data.clear()

    def __contains__(self, key: Hashable) -> bool:
        return self.get(key, _SENTINEL) is not _SENTINEL

    def __len__(self) -> int:
        with self._lock:
            now = time.monotonic()
            return sum(1 for _, (_, exp) in self._data.items() if exp > now)

    def _evict(self) -> None:
        """Remove expired entries, then oldest if still over capacity."""
        now = time.monotonic()
        expired = [k for k, (_, exp) in self._data.items() if exp <= now]
        for k in expired:
            del self._data[k]

        if len(self._data) > self._maxsize:
            # Remove oldest entry by expiry time
            oldest = min(self._data, key=lambda k: self._data[k][1])
            del self._data[oldest]


_SENTINEL = object()
