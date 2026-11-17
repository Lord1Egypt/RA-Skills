"""Execution policy and observable runtime state for the verifier."""

from __future__ import annotations

import threading
import time
from collections import Counter
from dataclasses import dataclass, field


MODE_GRACE_SECONDS = {"fast": 0.0, "balanced": 2.5, "strict": None}


@dataclass
class QueryEvent:
    provider: str
    status: str
    elapsed_ms: int
    attempt: int = 1
    detail: str = ""


@dataclass
class RuntimeMetrics:
    mode: str = "balanced"
    started: float = field(default_factory=time.monotonic)
    reused: int = 0
    doi_recovered: int = 0
    requests: Counter = field(default_factory=Counter)
    statuses: Counter = field(default_factory=Counter)
    events: list[QueryEvent] = field(default_factory=list)
    phases: dict[str, float] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def record(self, provider: str, status: str, elapsed: float, attempt: int = 1, detail: str = "") -> None:
        with self._lock:
            self.requests[provider] += 1
            self.statuses[status] += 1
            self.events.append(QueryEvent(provider, status, int(elapsed * 1000), attempt, detail[:240]))

    @property
    def elapsed_seconds(self) -> float:
        return time.monotonic() - self.started

    def finish_phase(self, name: str, started: float) -> None:
        self.phases[name] = round(time.monotonic() - started, 3)


def grace_for_mode(mode: str, override: float | None) -> float | None:
    if override is not None:
        return max(0.0, override)
    return MODE_GRACE_SECONDS[mode]
