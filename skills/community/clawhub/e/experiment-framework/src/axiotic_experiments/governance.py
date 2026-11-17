from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class ButlerError(RuntimeError):
    pass


def _default_butler() -> Path:
    candidates = (
        Path(os.environ.get("BUTLER_CLI", "")),
        Path.home() / ".agents/skills/butler/scripts/butler.py",
        Path.home() / ".codex/skills/butler/scripts/butler.py",
    )
    for path in candidates:
        if str(path) and path.is_file():
            return path
    raise ButlerError("Butler CLI not found; set BUTLER_CLI")


@dataclass(frozen=True)
class ButlerGate:
    verdict: str
    payload: dict[str, Any]


@dataclass(frozen=True)
class ButlerReservation:
    reservation_id: str
    payload: dict[str, Any]


class Butler:
    def __init__(self, cli: Path | None = None):
        self.cli = cli or _default_butler()

    def gpu_gate(self, project: str, requested_gpu_hours: float) -> ButlerGate:
        """Return a read-only preview. This method does not authorize a launch."""
        completed = self._run(
            "gpu-gate",
            "--project",
            project,
            "--request",
            str(requested_gpu_hours),
        )
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise ButlerError("Butler returned invalid gate output") from exc
        verdict = str(payload.get("verdict", ""))
        if completed.returncode != 0 or verdict != "proceed":
            raise ButlerError(f"Butler GPU gate refused launch: {verdict or 'unknown'}")
        return ButlerGate(verdict=verdict, payload=payload)

    def gpu_reserve(
        self,
        *,
        project: str,
        job: str,
        gpus: int,
        hours: float,
        estimated_cost: float | None = None,
        currency: str = "GBP",
        disk_gb: int = 0,
    ) -> ButlerReservation:
        command = (
            "gpu-reserve",
            "--project",
            project,
            "--job",
            job,
            "--reservation-id",
            job,
            "--gpus",
            str(gpus),
            "--hours",
            str(hours),
            "--currency",
            currency,
            "--disk-gb",
            str(disk_gb),
        )
        if estimated_cost is not None:
            command += ("--estimated-cost", str(estimated_cost))
        completed = self._run(*command)
        payload = self._payload(completed, "reservation")
        verdict = str(payload.get("verdict", ""))
        if completed.returncode != 0 or verdict not in {"reserved", "already_reserved"}:
            reason = payload.get("reason") or verdict or "unknown"
            raise ButlerError(f"Butler GPU reservation refused launch: {reason}")
        reservation = payload.get("reservation")
        if not isinstance(reservation, dict):
            raise ButlerError("Butler reservation output omitted the reservation")
        reservation_id = str(reservation.get("reservation_id", ""))
        if reservation_id != job:
            raise ButlerError("Butler returned the wrong reservation identity")
        return ButlerReservation(reservation_id=reservation_id, payload=payload)

    def gpu_reconcile(
        self,
        *,
        project: str,
        reservation_id: str,
        actual_gpu_hours: float,
        actual_cost: float | None = None,
        retained_disk_gb: int = 0,
        outcome: str = "completed",
        note: str = "",
    ) -> None:
        command = (
            "gpu-reconcile",
            "--project",
            project,
            "--reservation-id",
            reservation_id,
            "--actual-gpu-hours",
            str(actual_gpu_hours),
            "--retained-disk-gb",
            str(retained_disk_gb),
            "--outcome",
            outcome,
            "--note",
            note,
        )
        if actual_cost is not None:
            command += ("--actual-cost", str(actual_cost))
        completed = self._run(*command)
        payload = self._payload(completed, "reconciliation")
        verdict = str(payload.get("verdict", ""))
        if completed.returncode != 0 or verdict not in {
            "reconciled",
            "already_reconciled",
        }:
            reason = payload.get("reason") or verdict or "unknown"
            raise ButlerError(f"Butler failed to reconcile GPU reservation: {reason}")

    def gpu_log(
        self,
        *,
        project: str,
        job: str,
        gpus: int,
        hours: float,
    ) -> None:
        completed = self._run(
            "gpu-log",
            "--project",
            project,
            "--job",
            job,
            "--gpus",
            str(gpus),
            "--hours",
            str(hours),
        )
        if completed.returncode:
            raise ButlerError(
                completed.stderr.strip() or "Butler failed to log GPU usage"
            )

    @staticmethod
    def _payload(
        completed: subprocess.CompletedProcess[str],
        operation: str,
    ) -> dict[str, Any]:
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise ButlerError(f"Butler returned invalid {operation} output") from exc
        if not isinstance(payload, dict):
            raise ButlerError(f"Butler returned invalid {operation} output")
        return payload

    def _run(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(self.cli), *args],
            check=False,
            capture_output=True,
            text=True,
        )
