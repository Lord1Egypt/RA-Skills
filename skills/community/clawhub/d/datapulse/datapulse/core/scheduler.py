"""Lightweight schedule parsing and due-mission helpers."""

from __future__ import annotations

import asyncio
import json
import os
import re
from contextlib import AbstractContextManager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import TYPE_CHECKING

from .ops import WatchStatusStore
from .utils import watch_daemon_lock_path_from_env
from .watchlist import WatchlistStore, WatchMission

if TYPE_CHECKING:
    from datapulse.reader import DataPulseReader

_DURATION_RE = re.compile(r"^(?P<value>\d+)(?P<unit>[smhd]?)$")


def _parse_datetime(value: str) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _parse_duration_seconds(token: str) -> int | None:
    match = _DURATION_RE.match(str(token or "").strip().lower())
    if not match:
        return None
    value = int(match.group("value"))
    unit = match.group("unit") or "s"
    scale = {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 86400,
    }[unit]
    return max(1, value * scale)


def schedule_to_seconds(schedule: str) -> int | None:
    normalized = str(schedule or "").strip().lower()
    if normalized in {"", "manual", "off", "disabled"}:
        return None
    if normalized in {"@hourly", "hourly"}:
        return 3600
    if normalized in {"@daily", "daily"}:
        return 86400
    if normalized in {"@weekly", "weekly"}:
        return 7 * 86400
    for prefix in ("interval:", "every:"):
        if normalized.startswith(prefix):
            return _parse_duration_seconds(normalized.split(":", 1)[1])
    return None


def describe_schedule(schedule: str) -> str:
    normalized = str(schedule or "").strip().lower()
    if normalized in {"", "manual", "off", "disabled"}:
        return "manual"
    alias = {
        "@hourly": "hourly",
        "hourly": "hourly",
        "@daily": "daily",
        "daily": "daily",
        "@weekly": "weekly",
        "weekly": "weekly",
    }
    if normalized in alias:
        return alias[normalized]
    seconds = schedule_to_seconds(normalized)
    if seconds is None:
        return normalized or "manual"
    if seconds % 86400 == 0:
        return f"every {seconds // 86400}d"
    if seconds % 3600 == 0:
        return f"every {seconds // 3600}h"
    if seconds % 60 == 0:
        return f"every {seconds // 60}m"
    return f"every {seconds}s"


def next_run_at(mission: WatchMission, *, now: datetime | None = None) -> str | None:
    interval = schedule_to_seconds(mission.schedule)
    if interval is None or not mission.enabled:
        return None
    base = _parse_datetime(mission.last_run_at) or _parse_datetime(mission.created_at)
    if base is None:
        base = now or datetime.now(timezone.utc)
    return (base + timedelta(seconds=interval)).replace(microsecond=0).isoformat()


def is_watch_due(mission: WatchMission, *, now: datetime | None = None) -> bool:
    interval = schedule_to_seconds(mission.schedule)
    if interval is None or not mission.enabled:
        return False
    if now is None:
        now = datetime.now(timezone.utc)
    last_run = _parse_datetime(mission.last_run_at)
    if last_run is None:
        return True
    return now >= (last_run + timedelta(seconds=interval))


class WatchScheduler:
    """Helper that selects due missions from a watch store."""

    def __init__(self, store: WatchlistStore):
        self.store = store

    def due_missions(self, *, limit: int | None = None, now: datetime | None = None) -> list[WatchMission]:
        if now is None:
            now = datetime.now(timezone.utc)
        missions = [
            mission
            for mission in self.store.list_missions(include_disabled=False)
            if is_watch_due(mission, now=now)
        ]
        missions.sort(key=lambda mission: (mission.last_run_at or "", mission.created_at, mission.id))
        if limit and limit > 0:
            return missions[:limit]
        return missions


def _is_pid_running(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


class WatchDaemonLock(AbstractContextManager["WatchDaemonLock"]):
    """Single-process lock for the watch daemon runner."""

    def __init__(self, path: str | None = None):
        self.path = Path(path or watch_daemon_lock_path_from_env()).expanduser()
        self._locked = False

    def _payload(self) -> dict[str, object]:
        return {
            "pid": os.getpid(),
            "acquired_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        }

    def _maybe_remove_stale_lock(self) -> None:
        if not self.path.exists():
            return
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            self.path.unlink(missing_ok=True)
            return
        pid = int(raw.get("pid", 0) or 0)
        if not _is_pid_running(pid):
            self.path.unlink(missing_ok=True)

    def acquire(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._maybe_remove_stale_lock()
        try:
            fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError as exc:
            raise RuntimeError(f"Watch daemon lock already held: {self.path}") from exc
        try:
            payload = json.dumps(self._payload(), ensure_ascii=False).encode("utf-8")
            os.write(fd, payload)
        finally:
            os.close(fd)
        self._locked = True

    def release(self) -> None:
        if not self._locked:
            return
        self.path.unlink(missing_ok=True)
        self._locked = False

    def __enter__(self) -> "WatchDaemonLock":
        self.acquire()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.release()


class WatchDaemon:
    """Polls due watch missions and executes them under a lock."""

    def __init__(
        self,
        reader: "DataPulseReader",
        *,
        lock_path: str | None = None,
        status_store: WatchStatusStore | None = None,
    ):
        self.reader = reader
        self.lock = WatchDaemonLock(lock_path)
        self.status_store = status_store or WatchStatusStore()

    async def run_forever(
        self,
        *,
        poll_seconds: float = 60.0,
        max_cycles: int | None = None,
        due_limit: int | None = None,
        retry_attempts: int = 1,
        retry_base_delay: float = 1.0,
        retry_max_delay: float = 30.0,
        retry_backoff_factor: float = 2.0,
    ) -> dict[str, object]:
        cycles = 0
        last_payload: dict[str, object] = {}
        with self.lock:
            self.status_store.mark_started()
            try:
                while True:
                    cycles += 1
                    self.status_store.mark_cycle_started()
                    try:
                        last_payload = await self.reader.run_due_watches(
                            limit=due_limit,
                            retry_attempts=retry_attempts,
                            retry_base_delay=retry_base_delay,
                            retry_max_delay=retry_max_delay,
                            retry_backoff_factor=retry_backoff_factor,
                        )
                    except Exception as exc:
                        self.status_store.record_error(str(exc))
                        raise
                    self.status_store.record_cycle(last_payload)
                    if max_cycles is not None and cycles >= max_cycles:
                        break
                    await asyncio.sleep(max(0.1, float(poll_seconds)))
            finally:
                self.status_store.mark_stopped()
        return {
            "ok": True,
            "cycles": cycles,
            "last_result": last_payload,
        }
