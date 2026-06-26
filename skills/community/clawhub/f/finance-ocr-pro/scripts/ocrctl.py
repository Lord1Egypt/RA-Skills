"""CLI controller for durable OCR background jobs."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from ocr_jobs import JobStore, create_job_id, list_jobs

_SCRIPT_DIR = Path(__file__).resolve().parent


def _worker_popen_kwargs(*, log_file, env: dict[str, str]) -> dict[str, Any]:
    """Return cross-platform subprocess options for detached OCR workers."""
    kwargs: dict[str, Any] = {
        "cwd": str(_SCRIPT_DIR.parent),
        "stdin": subprocess.DEVNULL,
        "stdout": log_file,
        "stderr": subprocess.STDOUT,
        "env": env,
    }
    if os.name == "nt":
        creationflags = 0
        creationflags |= getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        creationflags |= getattr(subprocess, "CREATE_NO_WINDOW", 0)
        kwargs["creationflags"] = creationflags
    else:
        kwargs["start_new_session"] = True
    return kwargs


def _emit(payload: dict[str, Any], *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return

    if payload.get("ok") is False:
        print(f"Error: {payload.get('error', 'Unknown error')}")
        return

    for key, value in payload.items():
        print(f"{key}: {value}")


def _load_store(job_id: str) -> JobStore:
    store = JobStore(JobStore.jobs_root() / job_id)
    if not store.exists():
        raise FileNotFoundError(f"OCR job not found: {job_id}")
    return store


def _status_payload(store: JobStore) -> dict[str, Any]:
    snapshot = store.snapshot(refresh_liveness=True)
    total_pages = snapshot.get("total_pages") or 0
    processed_pages = snapshot.get("processed_pages") or 0
    percent = round((processed_pages / total_pages) * 100, 1) if total_pages else None
    return {
        "ok": True,
        "job_id": snapshot["job_id"],
        "status": snapshot["status"],
        "message": snapshot.get("message"),
        "error": snapshot.get("error"),
        "input_path": snapshot.get("input_path"),
        "input_name": snapshot.get("input_name"),
        "job_dir": snapshot.get("job_dir"),
        "current_step": snapshot.get("current_step"),
        "step_label": snapshot.get("step_label"),
        "total_pages": snapshot.get("total_pages"),
        "processed_pages": snapshot.get("processed_pages"),
        "failed_pages": snapshot.get("failed_pages"),
        "percent": percent,
        "created_at": snapshot.get("created_at"),
        "started_at": snapshot.get("started_at"),
        "finished_at": snapshot.get("finished_at"),
        "updated_at": snapshot.get("updated_at"),
        "artifacts_ready": snapshot.get("artifacts_ready", []),
    }


def cmd_start(args: argparse.Namespace) -> dict[str, Any]:
    input_path = Path(args.input_path).expanduser().resolve()
    if not input_path.is_file():
        return {"ok": False, "error": f"Input file not found: {input_path}"}

    job_id = create_job_id()
    store = JobStore(JobStore.jobs_root() / job_id)
    store.create(
        input_path,
        params={
            "threads": args.threads,
        },
    )

    cmd = [sys.executable, str(_SCRIPT_DIR / "ocr_worker.py"), "--job-dir", str(store.job_dir)]
    env = {**os.environ, "PYTHONUNBUFFERED": "1"}
    with store.log_path.open("a", encoding="utf-8") as log_file:
        proc = subprocess.Popen(cmd, **_worker_popen_kwargs(log_file=log_file, env=env))
    store.set_worker_pid(proc.pid)

    return {
        "ok": True,
        "job_id": job_id,
        "status": "queued",
        "input_path": str(input_path),
        "job_dir": str(store.job_dir),
        "worker_pid": proc.pid,
        "message": "OCR job accepted and worker started.",
    }


def cmd_status(args: argparse.Namespace) -> dict[str, Any]:
    store = _load_store(args.job_id)
    return _status_payload(store)


def cmd_list(args: argparse.Namespace) -> dict[str, Any]:
    jobs = list_jobs(state=args.state)
    rows = [
        {
            "job_id": job["job_id"],
            "status": job["status"],
            "input_name": job.get("input_name"),
            "current_step": job.get("current_step"),
            "processed_pages": job.get("processed_pages"),
            "total_pages": job.get("total_pages"),
            "updated_at": job.get("updated_at"),
        }
        for job in jobs
    ]
    return {"ok": True, "jobs": rows}


def cmd_tail(args: argparse.Namespace) -> dict[str, Any]:
    store = _load_store(args.job_id)
    return {
        "ok": True,
        "job_id": args.job_id,
        "lines": store.tail_log(lines=args.lines),
    }


def cmd_artifacts(args: argparse.Namespace) -> dict[str, Any]:
    store = _load_store(args.job_id)
    snapshot = store.snapshot(refresh_liveness=True)
    return {
        "ok": True,
        "job_id": args.job_id,
        "status": snapshot.get("status"),
        "artifacts": snapshot.get("artifacts", {}),
    }


def cmd_cancel(args: argparse.Namespace) -> dict[str, Any]:
    store = _load_store(args.job_id)
    snapshot = store.snapshot(refresh_liveness=True)
    if snapshot.get("status") in {"completed", "failed", "cancelled"}:
        return {
            "ok": True,
            "job_id": args.job_id,
            "status": snapshot.get("status"),
            "message": "OCR job is already finished.",
        }

    store.mark_cancel_requested()
    return {
        "ok": True,
        "job_id": args.job_id,
        "status": "cancelling",
        "message": "Cancellation requested.",
    }


def cmd_resume(args: argparse.Namespace) -> dict[str, Any]:
    store = _load_store(args.job_id)
    snapshot = store.snapshot(refresh_liveness=True)
    if snapshot.get("status") == "running":
        return {"ok": False, "error": "OCR job is already running."}
    if snapshot.get("status") == "completed":
        return {"ok": False, "error": "OCR job is already completed."}

    store.clear_cancel_requested()
    store.prepare_for_resume()

    cmd = [sys.executable, str(_SCRIPT_DIR / "ocr_worker.py"), "--job-dir", str(store.job_dir)]
    env = {**os.environ, "PYTHONUNBUFFERED": "1"}
    with store.log_path.open("a", encoding="utf-8") as log_file:
        proc = subprocess.Popen(cmd, **_worker_popen_kwargs(log_file=log_file, env=env))
    store.set_worker_pid(proc.pid)

    return {
        "ok": True,
        "job_id": args.job_id,
        "status": "queued",
        "worker_pid": proc.pid,
        "message": "OCR job resumed.",
    }


def cmd_doctor(args: argparse.Namespace) -> dict[str, Any]:
    from ocr_setup import find_soffice_binary

    jobs_root = JobStore.jobs_root()
    soffice_path = find_soffice_binary()
    return {
        "ok": True,
        "jobs_root": str(jobs_root),
        "python": sys.executable,
        "soffice_found": soffice_path is not None,
        "soffice_path": str(soffice_path) if soffice_path is not None else None,
        "env_file": str((_SCRIPT_DIR.parent / ".env").resolve()),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Control durable background OCR jobs.")
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    start = subparsers.add_parser("start", help="Start a new OCR background job.")
    start.add_argument("input_path", help="Path to the document or image to OCR.")
    start.add_argument("-t", "--threads", type=int, default=1, help="Number of OCR threads (default: 1; raise only if the API plan supports parallel OCR requests).")
    start.add_argument("--json", dest="subcommand_json", action="store_true", help=argparse.SUPPRESS)
    start.set_defaults(handler=cmd_start)

    status = subparsers.add_parser("status", help="Get the current status of a job.")
    status.add_argument("job_id", help="OCR job id.")
    status.add_argument("--json", dest="subcommand_json", action="store_true", help=argparse.SUPPRESS)
    status.set_defaults(handler=cmd_status)

    ls = subparsers.add_parser("list", help="List OCR jobs.")
    ls.add_argument("--state", default=None, help="Optional status filter.")
    ls.add_argument("--json", dest="subcommand_json", action="store_true", help=argparse.SUPPRESS)
    ls.set_defaults(handler=cmd_list)

    tail = subparsers.add_parser("tail", help="Read recent worker log lines.")
    tail.add_argument("job_id", help="OCR job id.")
    tail.add_argument("--lines", type=int, default=100, help="Number of lines to read.")
    tail.add_argument("--json", dest="subcommand_json", action="store_true", help=argparse.SUPPRESS)
    tail.set_defaults(handler=cmd_tail)

    artifacts = subparsers.add_parser("artifacts", help="List generated files for a job.")
    artifacts.add_argument("job_id", help="OCR job id.")
    artifacts.add_argument("--json", dest="subcommand_json", action="store_true", help=argparse.SUPPRESS)
    artifacts.set_defaults(handler=cmd_artifacts)

    cancel = subparsers.add_parser("cancel", help="Request cancellation for a running job.")
    cancel.add_argument("job_id", help="OCR job id.")
    cancel.add_argument("--json", dest="subcommand_json", action="store_true", help=argparse.SUPPRESS)
    cancel.set_defaults(handler=cmd_cancel)

    resume = subparsers.add_parser("resume", help="Resume a failed or cancelled job.")
    resume.add_argument("job_id", help="OCR job id.")
    resume.add_argument("--json", dest="subcommand_json", action="store_true", help=argparse.SUPPRESS)
    resume.set_defaults(handler=cmd_resume)

    doctor = subparsers.add_parser("doctor", help="Show local OCR control diagnostics.")
    doctor.add_argument("--json", dest="subcommand_json", action="store_true", help=argparse.SUPPRESS)
    doctor.set_defaults(handler=cmd_doctor)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        payload = args.handler(args)
    except Exception as exc:
        payload = {"ok": False, "error": str(exc)}

    _emit(
        payload,
        as_json=bool(getattr(args, "json", False) or getattr(args, "subcommand_json", False)),
    )
    if not payload.get("ok", False):
        sys.exit(1)


if __name__ == "__main__":
    main()
