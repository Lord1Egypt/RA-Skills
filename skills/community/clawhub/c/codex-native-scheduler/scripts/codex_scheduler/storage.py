"""Private, atomic file-backed scheduler state."""

from __future__ import annotations

import contextlib
import datetime as dt
import json
import os
import shutil
import time
from collections.abc import Iterator
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.11+ is required.
    tomllib = None  # type: ignore[assignment]

from .errors import SchedulerError
from .util import (
    SCHEMA_VERSION,
    atomic_write_json,
    atomic_write_text,
    is_job_id,
    iso,
    make_id,
    now_utc,
    process_alive,
    process_start_token,
    read_json,
    secure_directory,
    state_root_from_environment,
)

DEFAULT_CONFIG = """\
schema_version = 1
backend = "auto"

[defaults]
# profile = "automation"
# timeout_seconds = 3600
# codex_command = ["/absolute/path/to/codex"]
# python_command = "/absolute/path/to/python3"
"""


class Store:
    """Own scheduler configuration, jobs, runs, claims, and short locks."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = (root or state_root_from_environment()).expanduser().resolve()
        self.jobs_root = self.root / "jobs"
        self.config_path = self.root / "config.toml"

    def initialize(self) -> None:
        secure_directory(self.root)
        secure_directory(self.jobs_root)
        if not self.config_path.exists():
            atomic_write_text(self.config_path, DEFAULT_CONFIG)

    def load_config(self) -> dict[str, Any]:
        self.initialize()
        try:
            with self.config_path.open("rb") as handle:
                data = tomllib.load(handle)
        except (OSError, ValueError) as exc:
            raise SchedulerError(f"cannot read scheduler config: {exc}") from exc
        if int(data.get("schema_version", 0)) != SCHEMA_VERSION:
            raise SchedulerError(
                f"unsupported config schema_version: {data.get('schema_version')!r}"
            )
        return data

    def job_dir(self, job_id: str) -> Path:
        if not is_job_id(job_id):
            raise SchedulerError(f"invalid job id: {job_id}")
        return self.jobs_root / job_id

    def create_job(self, job: dict[str, Any], prompt: str) -> Path:
        self.initialize()
        job_dir = self.job_dir(job["id"])
        if job_dir.exists():
            raise SchedulerError(f"job already exists: {job['id']}")
        secure_directory(job_dir)
        secure_directory(job_dir / "runs")
        secure_directory(job_dir / "claims")
        secure_directory(job_dir / "backend")
        secure_directory(job_dir / "revisions")
        atomic_write_text(job_dir / "prompt.txt", prompt)
        atomic_write_json(job_dir / "job.json", job)
        atomic_write_json(job_dir / "revisions" / "1.json", job)
        return job_dir

    def save_job(self, job: dict[str, Any], *, save_revision: bool = False) -> None:
        job_dir = self.job_dir(job["id"])
        if not job_dir.is_dir():
            raise SchedulerError(f"job directory does not exist: {job['id']}")
        atomic_write_json(job_dir / "job.json", job)
        if save_revision:
            atomic_write_json(
                job_dir / "revisions" / f"{job['revision']}.json",
                job,
            )

    def load_job(self, job_id: str) -> dict[str, Any]:
        job = read_json(self.job_dir(job_id) / "job.json")
        if job.get("id") != job_id:
            raise SchedulerError(f"job id does not match its directory: {job_id}")
        return job

    def list_jobs(self) -> list[dict[str, Any]]:
        self.initialize()
        jobs: list[dict[str, Any]] = []
        for path in sorted(self.jobs_root.iterdir(), reverse=True):
            if not is_job_id(path.name):
                continue
            metadata = path / "job.json"
            if not metadata.is_file():
                continue
            try:
                job = self.load_job(path.name)
            except SchedulerError:
                continue
            jobs.append(job)
        return jobs

    def resolve_job(self, reference: str) -> dict[str, Any]:
        if is_job_id(reference) and self.job_dir(reference).is_dir():
            return self.load_job(reference)
        matches = [
            job
            for job in self.list_jobs()
            if job.get("name") == reference or job["id"].startswith(reference)
        ]
        if not matches:
            raise SchedulerError(f"job not found: {reference}")
        unique = {job["id"]: job for job in matches}
        if len(unique) > 1:
            raise SchedulerError(
                f"job reference is ambiguous: {reference} "
                f"({', '.join(sorted(unique))})"
            )
        return next(iter(unique.values()))

    def ensure_unique_name(
        self,
        name: str | None,
        *,
        excluding: str | None = None,
    ) -> None:
        if not name:
            return
        for job in self.list_jobs():
            if job["id"] != excluding and job.get("name") == name:
                raise SchedulerError(f"job name already exists: {name}")

    def prompt(self, job_id: str) -> str:
        try:
            return (self.job_dir(job_id) / "prompt.txt").read_text(encoding="utf-8")
        except OSError as exc:
            raise SchedulerError(f"cannot read prompt for {job_id}: {exc}") from exc

    def save_prompt(self, job_id: str, prompt: str) -> None:
        atomic_write_text(self.job_dir(job_id) / "prompt.txt", prompt)

    def new_run(
        self,
        job: dict[str, Any],
        *,
        trigger: str,
        scheduled_for: str | None,
        occurrence_key: str | None,
        retry_of: str | None = None,
        status: str = "starting",
        job_snapshot: dict[str, Any] | None = None,
        prompt: str | None = None,
    ) -> tuple[dict[str, Any], Path]:
        run_id = make_id("run-")
        run_dir = self.job_dir(job["id"]) / "runs" / run_id
        secure_directory(run_dir)
        secure_directory(run_dir / "attempts")
        snapshot = job_snapshot or job
        run = {
            "schema_version": SCHEMA_VERSION,
            "id": run_id,
            "job_id": job["id"],
            "job_revision": snapshot["revision"],
            "trigger": trigger,
            "scheduled_for": scheduled_for,
            "occurrence_key": occurrence_key,
            "retry_of": retry_of,
            "status": status,
            "created_at": now_utc().isoformat(timespec="microseconds"),
            "started_at": None,
            "finished_at": None,
            "attempts": 0,
            "session_id": None,
            "runner_pid": None,
            "runner_start_token": None,
            "codex_pid": None,
            "exit_code": None,
            "error": None,
        }
        atomic_write_json(run_dir / "run.json", run)
        atomic_write_json(run_dir / "job_snapshot.json", snapshot)
        atomic_write_text(
            run_dir / "prompt.txt",
            self.prompt(job["id"]) if prompt is None else prompt,
        )
        return run, run_dir

    def save_run(self, run: dict[str, Any]) -> None:
        atomic_write_json(self.run_dir(run["job_id"], run["id"]) / "run.json", run)

    def run_dir(self, job_id: str, run_id: str) -> Path:
        return self.job_dir(job_id) / "runs" / run_id

    def resolve_run(self, reference: str) -> tuple[dict[str, Any], Path]:
        matches: list[tuple[dict[str, Any], Path]] = []
        for job in self.list_jobs():
            runs_dir = self.job_dir(job["id"]) / "runs"
            if not runs_dir.is_dir():
                continue
            for path in runs_dir.iterdir():
                if not path.is_dir() or not (path / "run.json").is_file():
                    continue
                if path.name == reference or path.name.startswith(reference):
                    matches.append((read_json(path / "run.json"), path))
        if not matches:
            raise SchedulerError(f"run not found: {reference}")
        if len(matches) > 1:
            raise SchedulerError(f"run reference is ambiguous: {reference}")
        return matches[0]

    def list_runs(self, job_id: str) -> list[dict[str, Any]]:
        runs_dir = self.job_dir(job_id) / "runs"
        if not runs_dir.is_dir():
            return []
        result = []
        for path in sorted(runs_dir.iterdir(), reverse=True):
            metadata = path / "run.json"
            if metadata.is_file():
                result.append(read_json(metadata))
        return sorted(
            result,
            key=lambda run: (run.get("created_at") or "", run["id"]),
            reverse=True,
        )

    def claim_occurrence(
        self, job_id: str, key: str, payload: dict[str, Any]
    ) -> bool:
        claims = self.job_dir(job_id) / "claims"
        secure_directory(claims)
        safe_key = key.replace(":", "").replace("+", "p").replace("/", "_")
        claim = claims / f"{safe_key}.json"
        try:
            descriptor = os.open(
                claim,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                0o600,
            )
        except FileExistsError:
            return False
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        return True

    def active_owner(self, job_id: str) -> dict[str, Any] | None:
        path = self.job_dir(job_id) / ".active" / "owner.json"
        if not path.is_file():
            return None
        try:
            return read_json(path)
        except SchedulerError:
            return None

    def acquire_active(
        self,
        job_id: str,
        *,
        run_id: str,
        pid: int,
        start_token: str | None,
    ) -> tuple[bool, dict[str, Any] | None]:
        lock = self.job_dir(job_id) / ".active"
        owner = {
            "run_id": run_id,
            "pid": pid,
            "start_token": start_token,
            "acquired_at": iso(),
        }
        with self.short_lock(job_id, "active-state"):
            previous = self.active_owner(job_id)
            if previous and process_alive(
                previous.get("pid"),
                previous.get("start_token"),
            ):
                return False, previous
            if lock.exists():
                shutil.rmtree(lock)
            try:
                lock.mkdir(mode=0o700)
            except FileExistsError:
                return False, self.active_owner(job_id)
            atomic_write_json(lock / "owner.json", owner)
            return True, previous

    def release_active(self, job_id: str, run_id: str) -> None:
        lock = self.job_dir(job_id) / ".active"
        owner = self.active_owner(job_id)
        if owner and owner.get("run_id") != run_id:
            return
        shutil.rmtree(lock, ignore_errors=True)

    @contextlib.contextmanager
    def short_lock(
        self, job_id: str, name: str = "state", *, wait_seconds: float = 5
    ) -> Iterator[None]:
        lock = self.job_dir(job_id) / f".{name}.lock"
        deadline = time.monotonic() + wait_seconds
        while True:
            try:
                lock.mkdir(mode=0o700)
                break
            except FileExistsError:
                owner_path = lock / "owner.json"
                if owner_path.is_file():
                    try:
                        owner = read_json(owner_path)
                    except SchedulerError:
                        owner = {}
                    if not process_alive(
                        owner.get("pid"),
                        owner.get("start_token"),
                    ):
                        shutil.rmtree(lock, ignore_errors=True)
                        continue
                else:
                    try:
                        old = time.time() - lock.stat().st_mtime > 10
                    except OSError:
                        old = False
                    if old:
                        shutil.rmtree(lock, ignore_errors=True)
                        continue
                if time.monotonic() >= deadline:
                    raise SchedulerError(f"timed out acquiring job {name} lock")
                time.sleep(0.05)
        atomic_write_json(
            lock / "owner.json",
            {
                "pid": os.getpid(),
                "start_token": process_start_token(os.getpid()),
                "acquired_at": iso(),
            },
        )
        try:
            yield
        finally:
            shutil.rmtree(lock, ignore_errors=True)

    def prune_run(self, run: dict[str, Any]) -> None:
        run_dir = self.run_dir(run["job_id"], run["id"])
        tombstone = {
            "schema_version": SCHEMA_VERSION,
            "id": run["id"],
            "job_id": run["job_id"],
            "job_revision": run["job_revision"],
            "status": run["status"],
            "trigger": run["trigger"],
            "scheduled_for": run.get("scheduled_for"),
            "created_at": run.get("created_at"),
            "started_at": run.get("started_at"),
            "finished_at": run.get("finished_at"),
            "retry_of": run.get("retry_of"),
            "pruned_at": iso(),
            "tombstone": True,
        }
        for path in run_dir.iterdir():
            if path.name == "run.json":
                continue
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
        atomic_write_json(run_dir / "run.json", tombstone)

    def retention_candidates(
        self,
        job: dict[str, Any],
        *,
        now: dt.datetime | None = None,
    ) -> list[dict[str, Any]]:
        retention = job.get("retention", {"mode": "forever"})
        if retention.get("mode") == "forever":
            return []
        runs = [
            run
            for run in self.list_runs(job["id"])
            if not run.get("tombstone") and run["status"] not in {"running", "starting"}
        ]
        current = now or now_utc()
        retain_runs = retention.get("retain_runs")
        retention_days = retention.get("days")
        kept_by_count = {
            run["id"] for run in runs[: int(retain_runs or 0)]
        }
        candidates = []
        for run in runs:
            if run["id"] in kept_by_count:
                continue
            if retention_days is not None:
                finished = run.get("finished_at") or run.get("created_at")
                if parse_datetime(finished) > current - dt.timedelta(
                    days=int(retention_days)
                ):
                    continue
            candidates.append(run)
        return candidates


def parse_datetime(value: str) -> dt.datetime:
    parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.UTC)
    return parsed.astimezone(dt.UTC)
