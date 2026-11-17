"""Windows Task Scheduler 2.0 XML backend."""

from __future__ import annotations

import datetime as dt
import getpass
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from ..errors import BackendError
from ..util import parse_iso, secure_directory
from .base import Backend

TASK_NS = "http://schemas.microsoft.com/windows/2004/02/mit/task"
ET.register_namespace("", TASK_NS)
WINDOWS_WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def element(parent: ET.Element, name: str, text: str | None = None) -> ET.Element:
    child = ET.SubElement(parent, f"{{{TASK_NS}}}{name}")
    if text is not None:
        child.text = text
    return child


class TaskSchedulerBackend(Backend):
    name = "task-scheduler"

    def task_name(self, job: dict[str, Any]) -> str:
        return f"\\CodexNativeScheduler-{job['id']}"

    def xml_path(self, job: dict[str, Any]) -> Path:
        return self.state_root / "jobs" / job["id"] / "backend" / "task.xml"

    def make_xml(self, job: dict[str, Any]) -> ET.ElementTree:
        root = ET.Element(f"{{{TASK_NS}}}Task", {"version": "1.4"})
        registration = element(root, "RegistrationInfo")
        element(registration, "Description", f"Codex scheduler job {job['id']}")

        triggers = element(root, "Triggers")
        schedule = job["schedule"]
        now = dt.datetime.now().astimezone().replace(second=0, microsecond=0)
        if schedule["kind"] == "at":
            trigger = element(triggers, "TimeTrigger")
            target = parse_iso(schedule["at"]).astimezone()
            element(trigger, "StartBoundary", target.strftime("%Y-%m-%dT%H:%M:%S"))
        elif schedule["kind"] == "every":
            trigger = element(triggers, "TimeTrigger")
            repetition = element(trigger, "Repetition")
            minutes = int(schedule["seconds"]) // 60
            element(repetition, "Interval", f"PT{minutes}M")
            element(repetition, "StopAtDurationEnd", "false")
            anchor = parse_iso(schedule["anchor"]).astimezone()
            element(trigger, "StartBoundary", anchor.strftime("%Y-%m-%dT%H:%M:%S"))
        elif schedule["kind"] == "daily":
            trigger = element(triggers, "CalendarTrigger")
            start = now.replace(
                hour=int(schedule["hour"]),
                minute=int(schedule["minute"]),
            )
            element(trigger, "StartBoundary", start.strftime("%Y-%m-%dT%H:%M:%S"))
        elif schedule["kind"] == "weekly":
            trigger = element(triggers, "CalendarTrigger")
            start = now.replace(
                hour=int(schedule["hour"]),
                minute=int(schedule["minute"]),
            )
            element(trigger, "StartBoundary", start.strftime("%Y-%m-%dT%H:%M:%S"))
        else:
            raise BackendError(
                f"unsupported Task Scheduler schedule: {schedule['kind']}"
            )
        element(trigger, "Enabled", "true")
        if schedule["kind"] == "daily":
            daily = element(trigger, "ScheduleByDay")
            element(daily, "DaysInterval", "1")
        elif schedule["kind"] == "weekly":
            weekly = element(trigger, "ScheduleByWeek")
            element(weekly, "WeeksInterval", "1")
            days = element(weekly, "DaysOfWeek")
            element(days, WINDOWS_WEEKDAYS[int(schedule["weekday"])])

        principals = element(root, "Principals")
        principal = element(principals, "Principal")
        principal.set("id", "Author")
        user = getpass.getuser()
        domain = os.environ.get("USERDOMAIN")
        element(principal, "UserId", f"{domain}\\{user}" if domain else user)
        element(principal, "LogonType", "InteractiveToken")
        element(principal, "RunLevel", "LeastPrivilege")

        settings = element(root, "Settings")
        # Always let the scheduler runner observe each wake. It records
        # skipped_overlap itself when the job policy is skip.
        element(settings, "MultipleInstancesPolicy", "Parallel")
        element(settings, "DisallowStartIfOnBatteries", "false")
        element(settings, "StopIfGoingOnBatteries", "false")
        element(settings, "AllowHardTerminate", "true")
        element(settings, "StartWhenAvailable", "true")
        element(settings, "RunOnlyIfNetworkAvailable", "false")
        element(settings, "AllowStartOnDemand", "true")
        element(settings, "Enabled", "true")
        element(settings, "ExecutionTimeLimit", "PT0S")
        element(settings, "Priority", "7")

        actions = element(root, "Actions")
        actions.set("Context", "Author")
        command = element(actions, "Exec")
        arguments = self.trigger_arguments(job)
        element(command, "Command", arguments[0])
        element(command, "Arguments", subprocess.list2cmdline(arguments[1:]))
        element(command, "WorkingDirectory", str(Path(job["runner_entrypoint"]).parent))
        return ET.ElementTree(root)

    def _schtasks(self) -> str:
        candidate = shutil.which("schtasks") or shutil.which("schtasks.exe")
        if not candidate:
            raise BackendError("schtasks.exe is unavailable")
        return candidate

    def register(self, job: dict[str, Any]) -> None:
        path = self.xml_path(job)
        secure_directory(path.parent)
        self.make_xml(job).write(
            path,
            encoding="utf-16",
            xml_declaration=True,
        )
        result = self.execute(
            [
                self._schtasks(),
                "/Create",
                "/TN",
                self.task_name(job),
                "/XML",
                str(path),
                "/F",
            ],
            timeout=30,
        )
        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip()
            raise BackendError(f"Task Scheduler rejected job {job['id']}: {detail}")

    def unregister(self, job: dict[str, Any]) -> None:
        candidate = shutil.which("schtasks") or shutil.which("schtasks.exe")
        if not candidate:
            return
        self.execute(
            [candidate, "/Delete", "/TN", self.task_name(job), "/F"],
            timeout=30,
        )

    def status(self, job: dict[str, Any]) -> dict[str, Any]:
        candidate = shutil.which("schtasks") or shutil.which("schtasks.exe")
        if not candidate:
            return {"backend": self.name, "registered": False, "error": "unavailable"}
        result = self.execute(
            [candidate, "/Query", "/TN", self.task_name(job), "/FO", "LIST"],
            timeout=15,
        )
        return {
            "backend": self.name,
            "registered": result.returncode == 0,
            "task": self.task_name(job),
        }

    def doctor(self) -> dict[str, Any]:
        candidate = shutil.which("schtasks") or shutil.which("schtasks.exe")
        return {
            "backend": self.name,
            "available": candidate is not None,
            "command": candidate,
            "live_canary_required": False,
        }
