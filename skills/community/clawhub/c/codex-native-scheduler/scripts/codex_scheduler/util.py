"""Shared filesystem, process, and parsing helpers."""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
import uuid
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from .errors import SchedulerError

SCHEMA_VERSION = 1
JOB_ID = re.compile(r"job-\d{8}T\d{6}Z-[0-9a-f]{8}")
ENVIRONMENT_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
RELATIVE_TOKEN = re.compile(
    r"(?P<value>\d+(?:\.\d+)?)\s*"
    r"(?P<unit>weeks?|week|w|days?|day|d|hours?|hour|hrs?|hr|h|"
    r"minutes?|minute|mins?|min|m|seconds?|second|secs?|sec|s)",
    re.IGNORECASE,
)


def now_local() -> dt.datetime:
    return dt.datetime.now().astimezone()


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.UTC)


def iso(value: dt.datetime | None = None) -> str:
    return (value or now_utc()).isoformat(timespec="seconds")


def parse_iso(value: str) -> dt.datetime:
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise SchedulerError(f"invalid ISO 8601 timestamp: {value!r}") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=now_local().tzinfo)
    return parsed


def ceil_minute(value: dt.datetime) -> dt.datetime:
    if value.second or value.microsecond:
        return value.replace(second=0, microsecond=0) + dt.timedelta(minutes=1)
    return value.replace(second=0, microsecond=0)


def parse_duration(value: str, *, minimum_seconds: int = 60) -> int:
    raw = value.strip().lower()
    position = 0
    seconds = 0.0
    matched = False
    for match in RELATIVE_TOKEN.finditer(raw):
        if raw[position : match.start()].strip(" ,"):
            matched = False
            break
        matched = True
        amount = float(match.group("value"))
        unit = match.group("unit").lower()
        if unit.startswith("w"):
            seconds += amount * 7 * 24 * 3600
        elif unit.startswith("d"):
            seconds += amount * 24 * 3600
        elif unit.startswith("h"):
            seconds += amount * 3600
        elif unit.startswith("m"):
            seconds += amount * 60
        else:
            seconds += amount
        position = match.end()
    if not matched or raw[position:].strip(" ,"):
        raise SchedulerError(
            f"invalid duration: {value!r}; use values such as 30m, 2h, or 1d"
        )
    rounded = int(seconds)
    if rounded < minimum_seconds:
        raise SchedulerError(
            f"duration must be at least {minimum_seconds} seconds"
        )
    if rounded % 60:
        raise SchedulerError("schedules use minute precision")
    return rounded


def parse_at(value: str, *, now: dt.datetime | None = None) -> dt.datetime:
    current = now or now_local()
    raw = value.strip()
    relative = raw.lower()
    for prefix in ("now+", "+"):
        if relative.startswith(prefix):
            relative = relative[len(prefix) :].strip()
            break
    try:
        seconds = parse_duration(relative)
    except SchedulerError:
        normalized = raw.replace("Z", "+00:00")
        try:
            target = dt.datetime.fromisoformat(normalized)
        except ValueError as exc:
            raise SchedulerError(
                "invalid time; use an ISO 8601 timestamp or a duration such as 4h"
            ) from exc
        if target.tzinfo is None:
            target = target.replace(tzinfo=current.tzinfo)
        else:
            target = target.astimezone()
    else:
        target = current + dt.timedelta(seconds=seconds)
    target = ceil_minute(target)
    if target <= current:
        raise SchedulerError("scheduled time must be in the future; use run-now")
    return target


def secure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    if os.name != "nt":
        path.chmod(0o700)


def atomic_write_text(path: Path, content: str, *, private: bool = True) -> None:
    secure_directory(path.parent)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    temporary.write_text(content, encoding="utf-8")
    if private and os.name != "nt":
        temporary.chmod(0o600)
    os.replace(temporary, path)


def atomic_write_json(path: Path, payload: Any) -> None:
    atomic_write_text(
        path,
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SchedulerError(f"cannot read {path}: {exc}") from exc


def make_id(prefix: str = "") -> str:
    stamp = now_utc().strftime("%Y%m%dT%H%M%SZ")
    token = uuid.uuid4().hex[:8]
    return f"{prefix}{stamp}-{token}"


def is_job_id(value: str) -> bool:
    return JOB_ID.fullmatch(value) is not None


def resolve_executable(name_or_path: str) -> Path:
    candidate = shutil.which(name_or_path)
    if candidate is None:
        expanded = Path(name_or_path).expanduser()
        candidate = str(expanded) if expanded.exists() else None
    if candidate is None:
        raise SchedulerError(f"executable was not found: {name_or_path}")
    path = Path(candidate).resolve()
    if not path.is_file():
        raise SchedulerError(f"executable is not a file: {path}")
    if os.name != "nt" and not os.access(path, os.X_OK):
        raise SchedulerError(f"executable is not executable: {path}")
    return path


def resolve_codex_command(requested: str | None = None) -> list[str]:
    launcher = resolve_executable(requested or "codex")
    try:
        first_line = launcher.open("rb").readline(512).decode("utf-8", "replace")
    except OSError as exc:
        raise SchedulerError(f"cannot inspect Codex launcher: {exc}") from exc
    if first_line.startswith("#!") and "node" in first_line.lower():
        node = resolve_executable("node")
        return [str(node), str(launcher)]
    return [str(launcher)]


def entrypoint_path() -> Path:
    return Path(__file__).resolve().parents[1] / "codex-schedule"


def state_root_from_environment() -> Path:
    explicit = os.environ.get("CODEX_SCHEDULER_STATE_DIR")
    if explicit:
        return Path(explicit).expanduser().resolve()
    codex_home = Path(
        os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))
    ).expanduser()
    return (codex_home / "codex-native-scheduler").resolve()


def captured_environment(
    requested: Iterable[str], assignments: Iterable[str]
) -> tuple[dict[str, str], list[str]]:
    captured: dict[str, str] = {}
    missing: list[str] = []
    baseline = [
        "HOME",
        "PATH",
        "CODEX_HOME",
        "LANG",
        "LC_ALL",
        "LC_CTYPE",
        "TMPDIR",
        "TEMP",
        "TMP",
        "USERPROFILE",
        "APPDATA",
        "LOCALAPPDATA",
        "SystemRoot",
        "WINDIR",
        "COMSPEC",
        "PATHEXT",
    ]
    for key in [*baseline, *requested]:
        if key in os.environ:
            captured[key] = os.environ[key]
        elif key not in baseline:
            missing.append(key)
    for assignment in assignments:
        key, separator, value = assignment.partition("=")
        if not separator or ENVIRONMENT_NAME.fullmatch(key) is None:
            raise SchedulerError(f"invalid environment assignment: {assignment!r}")
        captured[key] = value
    captured.setdefault("HOME", str(Path.home()))
    captured["PYTHONUNBUFFERED"] = "1"
    return captured, missing


def run_checked(
    arguments: list[str],
    *,
    timeout: float | None = 30,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        arguments,
        text=True,
        capture_output=True,
        timeout=timeout,
        env=env,
        check=False,
    )


def platform_name() -> str:
    override = os.environ.get("CODEX_SCHEDULER_PLATFORM")
    if override:
        return override
    if sys.platform == "darwin":
        return "launchd"
    if sys.platform.startswith("linux"):
        return "systemd"
    if os.name == "nt" or sys.platform == "win32":
        return "task-scheduler"
    return "unsupported"


def process_start_token(pid: int) -> str | None:
    """Return a value that changes when an operating-system PID is reused."""
    if pid <= 0:
        return None
    if sys.platform.startswith("linux"):
        try:
            raw = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8")
            fields_after_command = raw.rsplit(") ", 1)[1].split()
            # /proc stat field 3 begins at index 0 after the command field.
            return fields_after_command[19]
        except (OSError, IndexError):
            return None
    if sys.platform == "darwin":
        result = run_checked(
            ["/bin/ps", "-o", "lstart=", "-p", str(pid)],
            timeout=5,
        )
        return result.stdout.strip() or None if result.returncode == 0 else None
    if os.name == "nt":
        try:
            import ctypes
            from ctypes import wintypes

            process = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)
            if not process:
                return None
            creation = wintypes.FILETIME()
            exit_time = wintypes.FILETIME()
            kernel = wintypes.FILETIME()
            user = wintypes.FILETIME()
            try:
                ok = ctypes.windll.kernel32.GetProcessTimes(
                    process,
                    ctypes.byref(creation),
                    ctypes.byref(exit_time),
                    ctypes.byref(kernel),
                    ctypes.byref(user),
                )
                if not ok:
                    return None
                return f"{creation.dwHighDateTime}:{creation.dwLowDateTime}"
            finally:
                ctypes.windll.kernel32.CloseHandle(process)
        except (AttributeError, OSError):
            return None
    return None


def process_alive(pid: int | None, start_token: str | None = None) -> bool:
    if not pid or pid <= 0:
        return False
    if os.name == "nt":
        try:
            import ctypes

            process = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)
            if not process:
                return False
            exit_code = ctypes.c_ulong()
            try:
                if not ctypes.windll.kernel32.GetExitCodeProcess(
                    process,
                    ctypes.byref(exit_code),
                ):
                    return False
                if exit_code.value != 259:  # STILL_ACTIVE
                    return False
            finally:
                ctypes.windll.kernel32.CloseHandle(process)
        except (AttributeError, OSError):
            return False
    else:
        try:
            os.kill(pid, 0)
        except (OSError, ProcessLookupError):
            return False
    if sys.platform.startswith("linux"):
        try:
            raw = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8")
            if raw.rsplit(") ", 1)[1].split()[0] == "Z":
                return False
        except (OSError, IndexError):
            return False
    elif sys.platform == "darwin":
        state = run_checked(
            ["/bin/ps", "-o", "stat=", "-p", str(pid)],
            timeout=5,
        )
        if state.returncode != 0 or state.stdout.lstrip().startswith("Z"):
            return False
    if start_token is None:
        return True
    return process_start_token(pid) == start_token


def terminate_process_tree(pid: int, *, grace_seconds: float = 10) -> None:
    """Request termination, then force a still-running process tree to stop."""
    if not process_alive(pid):
        return
    if os.name == "nt":
        run_checked(
            ["taskkill", "/PID", str(pid), "/T"],
            timeout=max(5, grace_seconds),
        )
    else:
        try:
            os.killpg(pid, signal.SIGTERM)
        except ProcessLookupError:
            return
    deadline = time.monotonic() + grace_seconds
    while process_alive(pid) and time.monotonic() < deadline:
        time.sleep(0.1)
    if not process_alive(pid):
        return
    if os.name == "nt":
        run_checked(["taskkill", "/PID", str(pid), "/T", "/F"], timeout=15)
    else:
        try:
            os.killpg(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
