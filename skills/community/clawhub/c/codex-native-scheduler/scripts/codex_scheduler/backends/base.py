"""Backend protocol and shared helpers."""

from __future__ import annotations

import abc
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any

from ..util import run_checked

Executor = Callable[..., subprocess.CompletedProcess[str]]


class Backend(abc.ABC):
    name = "unknown"

    def __init__(self, *, state_root: Path, execute: Executor | None = None) -> None:
        self.state_root = state_root
        self.execute = execute or run_checked

    @abc.abstractmethod
    def register(self, job: dict[str, Any]) -> None:
        """Register or replace one native job."""

    @abc.abstractmethod
    def unregister(self, job: dict[str, Any]) -> None:
        """Remove one native job if it exists."""

    @abc.abstractmethod
    def status(self, job: dict[str, Any]) -> dict[str, Any]:
        """Return a serializable native status."""

    @abc.abstractmethod
    def doctor(self) -> dict[str, Any]:
        """Return backend availability and diagnostics."""

    def trigger_arguments(self, job: dict[str, Any]) -> list[str]:
        return self.runner_arguments(job, "_trigger")

    def runner_arguments(
        self,
        job: dict[str, Any],
        command: str,
    ) -> list[str]:
        return [
            job["python_command"],
            job["runner_entrypoint"],
            "--state-dir",
            str(self.state_root),
            command,
            job["id"],
        ]
