"""Stdlib retry decorator and circuit breaker — zero external dependencies."""

from __future__ import annotations

import functools
import logging
import threading
import time
from typing import Any, Callable, TypeVar

logger = logging.getLogger("datapulse.retry")

_F = TypeVar("_F", bound=Callable[..., Any])


def retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    backoff_factor: float = 2.0,
    retryable: tuple[type[Exception], ...] = (Exception,),
    respect_retry_after: bool = True,
) -> Callable[[_F], _F]:
    """Retry decorator with exponential backoff.

    Args:
        max_attempts: Total attempts (including the first call).
        base_delay: Initial delay between retries in seconds.
        max_delay: Maximum delay cap.
        backoff_factor: Multiplier applied to delay after each retry.
        retryable: Exception types that trigger a retry.
        respect_retry_after: When True, honour RateLimitError.retry_after.
    """

    def decorator(func: _F) -> _F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delay = base_delay
            last_exc: Exception | None = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except retryable as exc:
                    last_exc = exc
                    if attempt >= max_attempts:
                        logger.warning(
                            "%s failed after %d attempts: %s",
                            func.__qualname__, max_attempts, exc,
                        )
                        raise
                    # 429-aware: use Retry-After when available
                    if (
                        respect_retry_after
                        and isinstance(exc, RateLimitError)
                        and exc.retry_after > 0
                    ):
                        wait = min(exc.retry_after, max_delay)
                    else:
                        wait = delay
                    logger.info(
                        "%s attempt %d/%d failed (%s), retrying in %.1fs",
                        func.__qualname__, attempt, max_attempts, exc, wait,
                    )
                    time.sleep(wait)
                    delay = min(delay * backoff_factor, max_delay)
            raise last_exc  # type: ignore[misc]  # unreachable but makes mypy happy

        return wrapper  # type: ignore[return-value]

    return decorator


class CircuitBreaker:
    """Simple circuit breaker to stop hammering failing services.

    States:
        CLOSED  — normal operation, calls pass through.
        OPEN    — calls are immediately rejected.
        HALF_OPEN — one trial call allowed; success → CLOSED, failure → OPEN.

    Thread-safe via a simple lock.
    """

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        name: str = "",
        rate_limit_weight: int = 2,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.name = name or "circuit"
        self.rate_limit_weight = rate_limit_weight
        self._state = self.CLOSED
        self._failure_count = 0
        self._last_failure_time: float = 0.0
        self._lock = threading.Lock()

    @property
    def state(self) -> str:
        with self._lock:
            if self._state == self.OPEN:
                if time.monotonic() - self._last_failure_time >= self.recovery_timeout:
                    self._state = self.HALF_OPEN
            return self._state

    def call(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        current = self.state
        if current == self.OPEN:
            raise CircuitBreakerOpen(
                f"Circuit '{self.name}' is open — service unavailable"
            )

        try:
            result = func(*args, **kwargs)
        except Exception as exc:
            self._record_failure(is_rate_limit=isinstance(exc, RateLimitError))
            raise
        else:
            self._record_success()
            return result

    def _record_failure(self, is_rate_limit: bool = False) -> None:
        with self._lock:
            increment = self.rate_limit_weight if is_rate_limit else 1
            self._failure_count += increment
            self._last_failure_time = time.monotonic()
            if self._failure_count >= self.failure_threshold:
                self._state = self.OPEN
                logger.warning(
                    "Circuit '%s' opened after %d failures",
                    self.name, self._failure_count,
                )

    def _record_success(self) -> None:
        with self._lock:
            self._failure_count = 0
            self._state = self.CLOSED

    def reset(self) -> None:
        with self._lock:
            self._failure_count = 0
            self._state = self.CLOSED
            self._last_failure_time = 0.0


class CircuitBreakerOpen(RuntimeError):
    """Raised when calling through an open circuit breaker."""


class RateLimitError(Exception):
    """Raised when a 429 / rate-limit response is received."""

    def __init__(self, message: str = "", retry_after: float = 0.0):
        super().__init__(message)
        self.retry_after = retry_after
