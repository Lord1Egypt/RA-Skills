"""Disk-backed OCR job store and progress reporter."""

from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ocr_runtime import ProgressReporter

JOBS_ROOT = Path.home() / ".semantic-ocr" / "jobs"

PIPELINE_STEPS: list[tuple[str, str]] = [
    ("preflight", "Preflight checks"),
    ("render_pages", "Converting document to images"),
    ("ocr_pages", "Extracting page content via VLM"),
    ("build_html", "Generating HTML comparison report"),
    ("build_docx", "Generating DOCX document"),
    ("build_excel", "Generating Excel workbook"),
    ("finalize", "Finalizing outputs"),
]

TERMINAL_STATUSES = {"completed", "failed", "cancelled"}


def utc_now() -> str:
    """Return a compact UTC timestamp suitable for JSON payloads."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def create_job_id() -> str:
    """Create a stable, human-readable OCR job id."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    suffix = uuid.uuid4().hex[:6]
    return f"ocr_{timestamp}_{suffix}"


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    tmp_path.replace(path)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _build_steps() -> list[dict[str, str]]:
    return [{"id": step_id, "label": label, "status": "pending"} for step_id, label in PIPELINE_STEPS]


def _is_pid_alive(pid: int | None) -> bool:
    if not pid:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


class JobStore:
    """Owns the on-disk state for a single OCR background job."""

    def __init__(self, job_dir: str | Path):
        self.job_dir = Path(job_dir).expanduser().resolve()
        self.manifest_path = self.job_dir / "manifest.json"
        self.progress_path = self.job_dir / "progress.json"
        self.events_path = self.job_dir / "events.jsonl"
        self.log_path = self.job_dir / "worker.log"
        self.pid_path = self.job_dir / "worker.pid"
        self.cancel_path = self.job_dir / "cancel.flag"

    @classmethod
    def jobs_root(cls) -> Path:
        JOBS_ROOT.mkdir(parents=True, exist_ok=True)
        return JOBS_ROOT

    @property
    def job_id(self) -> str:
        return self.job_dir.name

    def exists(self) -> bool:
        return self.manifest_path.exists() and self.progress_path.exists()

    def create(self, input_path: str | Path, *, params: dict[str, Any]) -> None:
        input_file = Path(input_path).expanduser().resolve()
        created_at = utc_now()

        manifest = {
            "job_id": self.job_id,
            "version": 1,
            "created_at": created_at,
            "input_path": str(input_file),
            "input_name": input_file.name,
            "params": params,
        }
        progress = {
            "job_id": self.job_id,
            "version": 1,
            "status": "queued",
            "message": "Queued for OCR processing.",
            "error": None,
            "created_at": created_at,
            "started_at": None,
            "finished_at": None,
            "updated_at": created_at,
            "current_step": None,
            "step_label": None,
            "steps": _build_steps(),
            "total_pages": None,
            "processed_pages": 0,
            "failed_pages": 0,
            "completed_pages": [],
            "failed_page_numbers": [],
            "artifacts": {},
            "worker_pid": None,
        }

        self.job_dir.mkdir(parents=True, exist_ok=True)
        _atomic_write_json(self.manifest_path, manifest)
        _atomic_write_json(self.progress_path, progress)
        self.append_event("job_created", input_path=str(input_file))

    def load_manifest(self) -> dict[str, Any]:
        data = _load_json(self.manifest_path)
        if not data:
            raise FileNotFoundError(f"Job manifest not found: {self.manifest_path}")
        return data

    def load_progress(self) -> dict[str, Any]:
        data = _load_json(self.progress_path)
        if not data:
            raise FileNotFoundError(f"Job progress not found: {self.progress_path}")
        return data

    def save_progress(self, progress: dict[str, Any]) -> dict[str, Any]:
        progress["updated_at"] = utc_now()
        _atomic_write_json(self.progress_path, progress)
        return progress

    def append_event(self, event_type: str, **payload: Any) -> None:
        record = {"ts": utc_now(), "type": event_type, **payload}
        self.events_path.parent.mkdir(parents=True, exist_ok=True)
        with self.events_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    def snapshot(self, *, refresh_liveness: bool = False) -> dict[str, Any]:
        if refresh_liveness:
            self.refresh_liveness()
        manifest = self.load_manifest()
        progress = self.load_progress()
        artifacts = {
            name: path
            for name, path in progress.get("artifacts", {}).items()
            if Path(path).exists()
        }
        return {
            **progress,
            "input_path": manifest.get("input_path"),
            "input_name": manifest.get("input_name"),
            "params": manifest.get("params", {}),
            "job_dir": str(self.job_dir),
            "artifacts": artifacts,
            "artifacts_ready": sorted(artifacts.keys()),
        }

    def set_worker_pid(self, pid: int) -> None:
        progress = self.load_progress()
        progress["worker_pid"] = pid
        self.pid_path.write_text(f"{pid}\n", encoding="utf-8")
        self.save_progress(progress)

    def mark_started(self, *, pid: int | None = None) -> None:
        progress = self.load_progress()
        progress["status"] = "running"
        progress["message"] = "OCR worker is running."
        progress["error"] = None
        progress["finished_at"] = None
        if progress.get("started_at") is None:
            progress["started_at"] = utc_now()
        if pid is not None:
            progress["worker_pid"] = pid
            self.pid_path.write_text(f"{pid}\n", encoding="utf-8")
        self.save_progress(progress)
        self.append_event("job_started", pid=progress.get("worker_pid"))

    def set_step(self, step_id: str, status: str) -> None:
        progress = self.load_progress()
        for step in progress.get("steps", []):
            if step["id"] == step_id:
                step["status"] = status
                progress["current_step"] = step_id
                progress["step_label"] = step["label"]
                break
        self.save_progress(progress)
        self.append_event("step_updated", step_id=step_id, status=status)

    def record_pages_discovered(self, total_pages: int) -> None:
        progress = self.load_progress()
        progress["total_pages"] = total_pages
        self.save_progress(progress)
        self.append_event("pages_discovered", total_pages=total_pages)

    def _update_page_sets(
        self,
        *,
        completed_page: int | None = None,
        failed_page: int | None = None,
    ) -> dict[str, Any]:
        progress = self.load_progress()
        completed = set(progress.get("completed_pages", []))
        failed = set(progress.get("failed_page_numbers", []))

        if completed_page is not None:
            completed.add(completed_page)
            failed.discard(completed_page)
        if failed_page is not None:
            failed.add(failed_page)
            completed.discard(failed_page)

        progress["completed_pages"] = sorted(completed)
        progress["failed_page_numbers"] = sorted(failed)
        progress["processed_pages"] = len(progress["completed_pages"])
        progress["failed_pages"] = len(progress["failed_page_numbers"])
        return self.save_progress(progress)

    def record_page_done(self, page_num: int, *, skipped: bool = False) -> None:
        self._update_page_sets(completed_page=page_num)
        self.append_event("page_done", page=page_num, skipped=skipped)

    def record_page_failed(self, page_num: int, error: str) -> None:
        self._update_page_sets(failed_page=page_num)
        self.append_event("page_failed", page=page_num, error=error)

    def record_artifact(self, name: str, path: str | Path) -> None:
        artifact_path = str(Path(path).resolve())
        progress = self.load_progress()
        progress.setdefault("artifacts", {})[name] = artifact_path
        self.save_progress(progress)
        self.append_event("artifact_ready", name=name, path=artifact_path)

    def log_message(self, message: str, *, warning: bool = False) -> None:
        progress = self.load_progress()
        progress["message"] = message
        self.save_progress(progress)
        self.append_event("warning" if warning else "log", message=message)

    def mark_completed(self, message: str = "OCR job completed.") -> None:
        progress = self.load_progress()
        progress["status"] = "completed"
        progress["message"] = message
        progress["error"] = None
        progress["finished_at"] = utc_now()
        progress["current_step"] = None
        progress["step_label"] = None
        for step in progress.get("steps", []):
            if step["status"] == "running":
                step["status"] = "completed"
        self.save_progress(progress)
        self.append_event("job_completed")

    def mark_failed(self, error: str) -> None:
        progress = self.load_progress()
        progress["status"] = "failed"
        progress["message"] = "OCR job failed."
        progress["error"] = error
        progress["finished_at"] = utc_now()
        self.save_progress(progress)
        self.append_event("job_failed", error=error)

    def mark_cancel_requested(self) -> None:
        self.cancel_path.touch()
        progress = self.load_progress()
        if progress.get("status") not in TERMINAL_STATUSES:
            progress["status"] = "cancelling"
            progress["message"] = "Cancellation requested."
            self.save_progress(progress)
        self.append_event("cancel_requested")

    def clear_cancel_requested(self) -> None:
        if self.cancel_path.exists():
            self.cancel_path.unlink()

    def is_cancel_requested(self) -> bool:
        return self.cancel_path.exists()

    def mark_cancelled(self) -> None:
        progress = self.load_progress()
        progress["status"] = "cancelled"
        progress["message"] = "OCR job cancelled."
        progress["finished_at"] = utc_now()
        progress["current_step"] = None
        progress["step_label"] = None
        self.save_progress(progress)
        self.append_event("job_cancelled")

    def prepare_for_resume(self) -> None:
        progress = self.load_progress()
        if progress.get("status") == "running":
            raise RuntimeError("Cannot resume a running OCR job.")
        progress["status"] = "queued"
        progress["message"] = "Resume requested."
        progress["error"] = None
        progress["finished_at"] = None
        progress["current_step"] = None
        progress["step_label"] = None
        for step in progress.get("steps", []):
            if step["status"] in {"running", "failed"}:
                step["status"] = "pending"
        self.save_progress(progress)
        self.append_event("resume_requested")

    def refresh_liveness(self) -> None:
        progress = self.load_progress()
        status = progress.get("status")
        if status in TERMINAL_STATUSES:
            return
        pid = progress.get("worker_pid")
        if pid and not _is_pid_alive(pid):
            progress["status"] = "failed"
            progress["message"] = "OCR worker is no longer running."
            progress["error"] = "Background OCR worker exited unexpectedly."
            progress["finished_at"] = utc_now()
            self.save_progress(progress)
            self.append_event("job_failed", error=progress["error"])

    def tail_log(self, lines: int = 100) -> list[str]:
        if not self.log_path.exists():
            return []
        content = self.log_path.read_text(encoding="utf-8", errors="replace").splitlines()
        if lines <= 0:
            return content
        return content[-lines:]


class DiskProgressReporter(ProgressReporter):
    """Writes OCR progress updates into a JobStore."""

    def __init__(self, store: JobStore):
        self.store = store

    def job_started(self) -> None:
        self.store.log_message("OCR pipeline started.")

    def step_started(self, step_id: str, label: str) -> None:
        self.store.set_step(step_id, "running")
        self.store.log_message(label)

    def step_completed(self, step_id: str) -> None:
        self.store.set_step(step_id, "completed")

    def pages_discovered(self, total_pages: int) -> None:
        self.store.record_pages_discovered(total_pages)

    def page_done(self, page_num: int, total_pages: int, *, skipped: bool = False) -> None:
        self.store.record_pages_discovered(total_pages)
        self.store.record_page_done(page_num, skipped=skipped)

    def page_failed(self, page_num: int, total_pages: int, error: str) -> None:
        self.store.record_pages_discovered(total_pages)
        self.store.record_page_failed(page_num, error)

    def artifact_ready(self, name: str, path: str | Path) -> None:
        self.store.record_artifact(name, path)

    def warning(self, message: str) -> None:
        self.store.log_message(message, warning=True)

    def log(self, message: str) -> None:
        self.store.log_message(message)

    def is_cancelled(self) -> bool:
        return self.store.is_cancel_requested()


def list_jobs(*, state: str | None = None) -> list[dict[str, Any]]:
    jobs_root = JobStore.jobs_root()
    rows: list[dict[str, Any]] = []
    for job_dir in sorted((p for p in jobs_root.iterdir() if p.is_dir()), reverse=True):
        store = JobStore(job_dir)
        if not store.exists():
            continue
        snapshot = store.snapshot(refresh_liveness=True)
        if state and snapshot.get("status") != state:
            continue
        rows.append(snapshot)
    return rows
