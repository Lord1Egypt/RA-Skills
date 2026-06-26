from __future__ import annotations

import os
import threading
import time
from dataclasses import dataclass, field


_SOURCE_INTERVALS: dict[str, float] = {
    # East Money throttles aggressively; default to a conservative local pace.
    "eastmoney": float(os.environ.get("AKSHARE_EASTMONEY_INTERVAL_SECONDS", "12.0")),
    "sina": 1.5,
    "jin10": 1.5,
    "nbs": 1.0,
    "pbc": 1.0,
    "cfdc": 1.0,
    "jsl": 1.5,
    "cmec": 1.0,
    "sse": 1.0,
    "shfe": 1.0,
    "dce": 1.0,
    "csindex": 1.0,
    "swindex": 1.0,
    "safe": 1.0,
    "amac": 1.0,
    "legulegu": 1.5,
    "99futures": 1.0,
    "akshare": 1.5,
}

_DEFAULT_INTERVAL = 1.5

_MAX_CONCURRENT = int(os.environ.get("AKSHARE_MAX_CONCURRENT", "1"))


@dataclass
class RateLimiter:
    _global_semaphore: threading.Semaphore = field(
        default_factory=lambda: threading.Semaphore(_MAX_CONCURRENT)
    )
    _source_lock: threading.Lock = field(default_factory=threading.Lock)
    _source_last_call: dict[str, float] = field(default_factory=dict)
    _thread_depth: dict[int, int] = field(default_factory=dict)

    def acquire(self, source: str = "") -> None:
        thread_id = threading.get_ident()
        depth = self._thread_depth.get(thread_id, 0)
        if depth == 0:
            self._global_semaphore.acquire()
        self._thread_depth[thread_id] = depth + 1

        interval = _SOURCE_INTERVALS.get(source, _DEFAULT_INTERVAL)

        with self._source_lock:
            last = self._source_last_call.get(source, 0.0)
            elapsed = time.monotonic() - last
            if elapsed < interval:
                time.sleep(interval - elapsed)
            self._source_last_call[source] = time.monotonic()

    def release(self) -> None:
        thread_id = threading.get_ident()
        depth = self._thread_depth.get(thread_id, 0)
        if depth <= 1:
            self._thread_depth.pop(thread_id, None)
            self._global_semaphore.release()
        else:
            self._thread_depth[thread_id] = depth - 1


rate_limiter = RateLimiter()
