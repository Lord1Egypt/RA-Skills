"""
In-memory rate limiter state.

Implements a sliding window counter using a deque of timestamps.
"""

import time
from collections import deque
from dataclasses import dataclass, field


@dataclass
class RateLimit:
    key: str
    max_requests: int
    window_seconds: int
    timestamps: deque = field(default_factory=deque)

    def _prune(self) -> None:
        """Remove timestamps outside the current window."""
        cutoff = time.monotonic() - self.window_seconds
        while self.timestamps and self.timestamps[0] < cutoff:
            self.timestamps.popleft()

    @property
    def remaining(self) -> int:
        self._prune()
        return max(0, self.max_requests - len(self.timestamps))

    @property
    def allowed(self) -> bool:
        return self.remaining > 0

    @property
    def retry_after(self) -> int:
        """Seconds until the next request would be allowed."""
        if self.allowed:
            return 0
        self._prune()
        if not self.timestamps:
            return 0
        oldest = self.timestamps[0]
        wait = (oldest + self.window_seconds) - time.monotonic()
        return max(0, int(wait) + 1)

    def consume(self) -> bool:
        """Try to consume one request. Returns True if allowed."""
        self._prune()
        if len(self.timestamps) >= self.max_requests:
            return False
        self.timestamps.append(time.monotonic())
        return True

    def reset(self) -> None:
        """Clear all timestamps."""
        self.timestamps.clear()


# Global state — simple dict, reset on import
_limits: dict[str, RateLimit] = {}


def get_limit(key: str) -> RateLimit | None:
    return _limits.get(key)


def create_limit(key: str, max_requests: int, window_seconds: int) -> RateLimit:
    rl = RateLimit(key=key, max_requests=max_requests, window_seconds=window_seconds)
    _limits[key] = rl
    return rl


def delete_limit(key: str) -> bool:
    return _limits.pop(key, None) is not None


def list_limits() -> list[RateLimit]:
    return list(_limits.values())
