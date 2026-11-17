"""Linux transient systemd user timer backend."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from ..errors import BackendError
from ..util import parse_iso
from .base import Backend

SYSTEMD_WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


class SystemdBackend(Backend):
    name = "systemd"

    def unit(self, job: dict[str, Any]) -> str:
        return f"codex-native-scheduler-{job['id']}"

    def timer_unit(self, job: dict[str, Any]) -> str:
        return f"{self.unit(job)}.timer"

    def service_unit(self, job: dict[str, Any]) -> str:
        return f"{self.unit(job)}.service"

    def _command(self, name: str) -> str:
        result = shutil.which(name)
        if not result:
            raise BackendError(f"{name} is unavailable")
        return str(Path(result).resolve())

    def timer_arguments(self, job: dict[str, Any]) -> list[str]:
        schedule = job["schedule"]
        if schedule["kind"] == "at":
            target = parse_iso(schedule["at"]).astimezone()
            return [
                f"--on-calendar={target.strftime('%Y-%m-%d %H:%M:00')}",
                "--timer-property=Persistent=true",
            ]
        if schedule["kind"] == "daily":
            return [
                f"--on-calendar=*-*-* {int(schedule['hour']):02d}:"
                f"{int(schedule['minute']):02d}:00",
                "--timer-property=Persistent=true",
            ]
        if schedule["kind"] == "weekly":
            weekday = SYSTEMD_WEEKDAYS[int(schedule["weekday"])]
            return [
                f"--on-calendar={weekday} *-*-* {int(schedule['hour']):02d}:"
                f"{int(schedule['minute']):02d}:00",
                "--timer-property=Persistent=true",
            ]
        if schedule["kind"] == "every":
            seconds = int(schedule["seconds"])
            anchor = parse_iso(schedule["anchor"]).astimezone()
            return [
                f"--on-calendar={anchor.strftime('%Y-%m-%d %H:%M:%S')}",
                f"--on-unit-active={seconds}s",
                "--timer-property=Persistent=true",
            ]
        raise BackendError(f"unsupported systemd schedule: {schedule['kind']}")

    def trigger_arguments(self, job: dict[str, Any]) -> list[str]:
        # The timer service stays short. Each wake receives a unique transient
        # service cgroup so long Codex runs survive the launcher's exit and
        # parallel overlap remains possible.
        return [
            self._command("systemd-run"),
            "--user",
            "--collect",
            "--quiet",
            *self.runner_arguments(job, "_execute-trigger"),
        ]

    def register(self, job: dict[str, Any]) -> None:
        systemd_run = self._command("systemd-run")
        self.unregister(job)
        arguments = [
            systemd_run,
            "--user",
            f"--unit={self.unit(job)}",
            "--collect",
            "--quiet",
            "--service-type=exec",
            *self.timer_arguments(job),
            *self.trigger_arguments(job),
        ]
        result = self.execute(arguments, timeout=30)
        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip()
            raise BackendError(f"systemd-run rejected job {job['id']}: {detail}")

    def unregister(self, job: dict[str, Any]) -> None:
        systemctl = shutil.which("systemctl")
        if not systemctl:
            return
        self.execute(
            [
                systemctl,
                "--user",
                "stop",
                self.timer_unit(job),
                self.service_unit(job),
            ],
            timeout=30,
        )
        self.execute(
            [
                systemctl,
                "--user",
                "reset-failed",
                self.timer_unit(job),
                self.service_unit(job),
            ],
            timeout=30,
        )

    def status(self, job: dict[str, Any]) -> dict[str, Any]:
        systemctl = shutil.which("systemctl")
        if not systemctl:
            return {"backend": self.name, "registered": False, "error": "unavailable"}
        result = self.execute(
            [
                systemctl,
                "--user",
                "show",
                self.timer_unit(job),
                "--property=LoadState",
                "--property=ActiveState",
                "--property=NextElapseUSecRealtime",
                "--no-pager",
            ],
            timeout=15,
        )
        values = {}
        for line in result.stdout.splitlines():
            key, separator, value = line.partition("=")
            if separator:
                values[key] = value
        return {
            "backend": self.name,
            "registered": result.returncode == 0
            and values.get("LoadState") == "loaded",
            "unit": self.timer_unit(job),
            "native": values,
        }

    def doctor(self) -> dict[str, Any]:
        systemd_run = shutil.which("systemd-run")
        systemctl = shutil.which("systemctl")
        available = bool(systemd_run and systemctl)
        detail = None
        if available:
            result = self.execute(
                [systemctl, "--user", "show-environment"],
                timeout=15,
            )
            available = result.returncode == 0
            if not available:
                detail = result.stderr.strip() or result.stdout.strip()
        linger = None
        loginctl = shutil.which("loginctl")
        if loginctl:
            import os

            result = self.execute(
                [loginctl, "show-user", str(os.getuid()), "--property=Linger"],
                timeout=15,
            )
            if result.returncode == 0:
                linger = result.stdout.strip().partition("=")[2] or None
        return {
            "backend": self.name,
            "available": available,
            "systemd_run": systemd_run,
            "systemctl": systemctl,
            "linger": linger,
            "logout_limitation": linger != "yes",
            "detail": detail,
        }
