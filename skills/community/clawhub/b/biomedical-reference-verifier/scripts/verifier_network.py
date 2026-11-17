"""Minimal network scheduling primitives shared by verifier providers."""

from __future__ import annotations

import contextlib
import email.utils
import threading
import time
import urllib.error
from collections.abc import Callable, Iterable
from typing import TypeVar

T = TypeVar("T")


class RateLimiter:
    def __init__(self, requests_per_second: float, max_concurrent: int) -> None:
        self.min_interval = 1.0 / max(requests_per_second, 0.1)
        self.lock = threading.Lock()
        self.next_start = 0.0
        self.semaphore = threading.BoundedSemaphore(max(1, max_concurrent))

    @contextlib.contextmanager
    def slot(self) -> Iterable[None]:
        self.semaphore.acquire()
        try:
            with self.lock:
                now = time.monotonic()
                if now < self.next_start:
                    time.sleep(self.next_start - now)
                    now = time.monotonic()
                self.next_start = max(now, self.next_start) + self.min_interval
            yield
        finally:
            self.semaphore.release()


def retry_delay(exc: BaseException, attempt: int) -> float | None:
    """Return a bounded retry delay, or None for permanent failures."""
    if isinstance(exc, urllib.error.HTTPError):
        if exc.code in {404, 400, 401, 403, 422}:
            return None
        if exc.code == 429:
            raw = exc.headers.get("Retry-After") if exc.headers else None
            if raw:
                try:
                    return min(10.0, max(0.0, float(raw)))
                except ValueError:
                    try:
                        parsed = email.utils.parsedate_to_datetime(raw).timestamp() - time.time()
                        return min(10.0, max(0.0, parsed))
                    except (TypeError, ValueError, OverflowError):
                        pass
            return min(4.0, 1.0 * (2 ** (attempt - 1)))
        if 500 <= exc.code <= 599:
            return min(4.0, 1.0 * (2 ** (attempt - 1)))
        return None
    if isinstance(exc, (urllib.error.URLError, TimeoutError)):
        return min(2.0, 0.5 * (2 ** (attempt - 1)))
    return None


def run_with_retry(operation: Callable[[float, int], T], first_timeout: float, retries: int = 1) -> T:
    """Run one request with a short first timeout and one bounded retry."""
    timeout = max(0.5, first_timeout)
    for attempt in range(1, retries + 2):
        try:
            return operation(timeout, attempt)
        except BaseException as exc:
            delay = retry_delay(exc, attempt)
            if attempt > retries or delay is None:
                raise
            time.sleep(delay)
            timeout = min(8.0, timeout * 2.0)
    raise RuntimeError("unreachable")
