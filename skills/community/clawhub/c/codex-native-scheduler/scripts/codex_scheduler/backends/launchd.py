"""macOS launchd backend."""

from __future__ import annotations

import os
import plistlib
import shutil
from pathlib import Path
from typing import Any

from ..errors import BackendError
from ..util import parse_iso, secure_directory
from .base import Backend


class LaunchdBackend(Backend):
    name = "launchd"

    @property
    def domain(self) -> str:
        return f"gui/{os.getuid()}"

    def label(self, job: dict[str, Any]) -> str:
        return f"com.wufei.codex-native-scheduler.{job['id']}"

    def plist_path(self, job: dict[str, Any]) -> Path:
        return self.state_root / "jobs" / job["id"] / "backend" / "launchd.plist"

    def make_plist(self, job: dict[str, Any]) -> dict[str, Any]:
        job_dir = self.state_root / "jobs" / job["id"]
        schedule = job["schedule"]
        timer: dict[str, Any]
        if schedule["kind"] == "every":
            timer = {"StartInterval": int(schedule["seconds"])}
        else:
            if schedule["kind"] == "at":
                target = parse_iso(schedule["at"]).astimezone()
                calendar = {
                    "Month": target.month,
                    "Day": target.day,
                    "Hour": target.hour,
                    "Minute": target.minute,
                }
            elif schedule["kind"] == "daily":
                calendar = {
                    "Hour": int(schedule["hour"]),
                    "Minute": int(schedule["minute"]),
                }
            elif schedule["kind"] == "weekly":
                calendar = {
                    # launchd uses Sunday=0, Monday=1, ..., Saturday=6.
                    "Weekday": (int(schedule["weekday"]) + 1) % 7,
                    "Hour": int(schedule["hour"]),
                    "Minute": int(schedule["minute"]),
                }
            else:
                raise BackendError(f"unsupported launchd schedule: {schedule['kind']}")
            timer = {"StartCalendarInterval": calendar}
        return {
            "Label": self.label(job),
            "ProgramArguments": self.trigger_arguments(job),
            **timer,
            "StandardOutPath": str(job_dir / "backend" / "launchd.stdout.log"),
            "StandardErrorPath": str(job_dir / "backend" / "launchd.stderr.log"),
            "ProcessType": "Background",
            "RunAtLoad": False,
        }

    def _launchctl(self) -> str:
        candidate = shutil.which("launchctl") or "/bin/launchctl"
        if not Path(candidate).exists():
            raise BackendError("launchctl is unavailable")
        return candidate

    def register(self, job: dict[str, Any]) -> None:
        path = self.plist_path(job)
        secure_directory(path.parent)
        temporary = path.with_suffix(".plist.new")
        with temporary.open("wb") as handle:
            plistlib.dump(self.make_plist(job), handle, sort_keys=False)
        if os.name != "nt":
            temporary.chmod(0o600)
        previous = path.read_bytes() if path.exists() else None
        os.replace(temporary, path)

        launchctl = self._launchctl()
        self.execute(
            [launchctl, "bootout", f"{self.domain}/{self.label(job)}"],
            timeout=30,
        )
        result = self.execute(
            [launchctl, "bootstrap", self.domain, str(path)],
            timeout=30,
        )
        if result.returncode == 0:
            return

        detail = result.stderr.strip() or result.stdout.strip()
        if previous is not None:
            path.write_bytes(previous)
            if os.name != "nt":
                path.chmod(0o600)
            self.execute(
                [launchctl, "bootstrap", self.domain, str(path)],
                timeout=30,
            )
        raise BackendError(f"launchd rejected job {job['id']}: {detail}")

    def unregister(self, job: dict[str, Any]) -> None:
        launchctl = shutil.which("launchctl") or "/bin/launchctl"
        if not Path(launchctl).exists():
            return
        self.execute(
            [launchctl, "bootout", f"{self.domain}/{self.label(job)}"],
            timeout=30,
        )

    def status(self, job: dict[str, Any]) -> dict[str, Any]:
        launchctl = shutil.which("launchctl") or "/bin/launchctl"
        if not Path(launchctl).exists():
            return {"backend": self.name, "registered": False, "error": "unavailable"}
        result = self.execute(
            [launchctl, "print", f"{self.domain}/{self.label(job)}"],
            timeout=15,
        )
        return {
            "backend": self.name,
            "registered": result.returncode == 0,
            "label": self.label(job),
        }

    def doctor(self) -> dict[str, Any]:
        launchctl = shutil.which("launchctl") or "/bin/launchctl"
        available = Path(launchctl).exists()
        result = None
        if available:
            result = self.execute([launchctl, "print", self.domain], timeout=15)
        return {
            "backend": self.name,
            "available": bool(available and result and result.returncode == 0),
            "command": launchctl if available else None,
            "domain": self.domain,
            "detail": (
                None
                if result is None or result.returncode == 0
                else result.stderr.strip() or result.stdout.strip()
            ),
        }

