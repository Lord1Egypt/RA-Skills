"""Run Codex jobs and reconcile scheduler state."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

from .backends import backend_for
from .errors import SchedulerError
from .schedules import count_missed, latest_due, occurrence_key
from .storage import Store
from .util import (
    atomic_write_json,
    atomic_write_text,
    iso,
    now_local,
    parse_iso,
    process_alive,
    process_start_token,
    read_json,
    terminate_process_tree,
)
from .workspaces import prepare_workspace

FAILURE_STATUSES = {"failed", "timed_out", "abandoned"}
TERMINAL_STATUSES = {
    "succeeded",
    "failed",
    "timed_out",
    "cancelled",
    "abandoned",
    "skipped_overlap",
}
DETERMINISTIC_ERRORS = (
    "strict config",
    "configuration error",
    "config.toml",
    "unknown field",
    "unknown configuration field",
    "unexpected argument",
    "invalid value",
    "invalid profile",
    "unknown profile",
    "profile not found",
    "failed to load profile",
    "not logged in",
    "authentication",
    "unauthorized",
    "permission denied",
    "no such file or directory",
)


def _codex_arguments(
    job: dict[str, Any],
    *,
    cwd: Path,
    final_path: Path,
    session_id: str | None,
) -> list[str]:
    arguments = [*job["codex"]["command"], "exec"]
    outer = ["-C", str(cwd)]
    profile = job["codex"].get("profile")
    if profile:
        outer.extend(["-p", str(profile)])
    common = ["--strict-config", "--json", "-o", str(final_path)]
    for override in job["codex"].get("config", []):
        common.extend(["-c", str(override)])
    if not job["workspace"].get("is_git", True):
        common.append("--skip-git-repo-check")
    if session_id:
        return [*arguments, *outer, "resume", *common, session_id, "-"]
    return [*arguments, *outer, *common, "-"]


def _events(path: Path) -> dict[str, Any]:
    state: dict[str, Any] = {
        "thread_id": None,
        "turn_started": False,
        "turn_completed": False,
        "turn_failed": False,
        "last_error": None,
    }
    if not path.is_file():
        return state
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            continue
        event_type = event.get("type")
        if event_type == "thread.started":
            state["thread_id"] = event.get("thread_id")
        elif event_type == "turn.started":
            state["turn_started"] = True
        elif event_type == "turn.completed":
            state["turn_completed"] = True
        elif event_type in {"turn.failed", "error"}:
            state["turn_failed"] = True
            state["last_error"] = event.get("message") or event.get("error")
    return state


def _deterministic_failure(stderr_path: Path, event_state: dict[str, Any]) -> bool:
    detail = stderr_path.read_text(encoding="utf-8", errors="replace").lower()
    if event_state.get("last_error"):
        detail += f"\n{event_state['last_error']}".lower()
    return any(pattern in detail for pattern in DETERMINISTIC_ERRORS)


def _copy_attempt_artifacts(attempt_dir: Path, run_dir: Path) -> None:
    mapping = {
        "codex.jsonl": "codex.jsonl",
        "stderr.log": "stderr.log",
        "final.txt": "final.txt",
    }
    for source_name, target_name in mapping.items():
        source = attempt_dir / source_name
        target = run_dir / target_name
        if source.exists():
            shutil.copy2(source, target)
        else:
            target.unlink(missing_ok=True)


def _mark_cancel_requested(run_dir: Path) -> bool:
    return (run_dir / "cancel.requested").exists()


def execute_run(
    store: Store,
    run: dict[str, Any],
    run_dir: Path,
    job_snapshot: dict[str, Any],
    *,
    resume_session: str | None,
    preferred_cwd: Path | None = None,
) -> dict[str, Any]:
    prompt = (run_dir / "prompt.txt").read_text(encoding="utf-8")
    run["runner_pid"] = os.getpid()
    run["runner_start_token"] = process_start_token(os.getpid())
    store.save_run(run)
    if _mark_cancel_requested(run_dir):
        run["status"] = "cancelled"
        run["finished_at"] = iso()
        run["error"] = "run was stopped before workspace preparation"
        store.save_run(run)
        return run
    if preferred_cwd is not None:
        cwd = preferred_cwd
        workspace_record = {
            "mode": job_snapshot["workspace"]["mode"],
            "cwd": str(cwd),
            "reused_from_retry": True,
        }
    else:
        cwd, workspace_record = prepare_workspace(
            job_snapshot,
            run["id"],
            state_root=store.root,
        )
    atomic_write_json(run_dir / "workspace.json", workspace_record)
    if _mark_cancel_requested(run_dir):
        run["status"] = "cancelled"
        run["finished_at"] = iso()
        run["error"] = "run was stopped during workspace preparation"
        store.save_run(run)
        return run
    run["status"] = "running"
    run["started_at"] = iso()
    store.save_run(run)

    timeout = job_snapshot.get("timeout_seconds")
    terminal_status = "failed"
    error: str | None = None
    session_id = resume_session
    for attempt in range(1, 4):
        run["attempts"] = attempt
        attempt_dir = run_dir / "attempts" / str(attempt)
        attempt_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        final_path = attempt_dir / "final.txt"
        stdout_path = attempt_dir / "codex.jsonl"
        stderr_path = attempt_dir / "stderr.log"
        command = _codex_arguments(
            job_snapshot,
            cwd=cwd,
            final_path=final_path,
            session_id=session_id,
        )
        atomic_write_json(
            attempt_dir / "command.json",
            {"arguments": command, "cwd": str(cwd)},
        )
        environment = dict(job_snapshot["environment"])
        try:
            with (
                stdout_path.open("w", encoding="utf-8") as stdout_handle,
                stderr_path.open("w", encoding="utf-8") as stderr_handle,
            ):
                process = subprocess.Popen(
                    command,
                    cwd=cwd,
                    env=environment,
                    stdin=subprocess.PIPE,
                    stdout=stdout_handle,
                    stderr=stderr_handle,
                    text=True,
                    start_new_session=os.name != "nt",
                    creationflags=(
                        subprocess.CREATE_NEW_PROCESS_GROUP
                        if os.name == "nt"
                        else 0
                    ),
                )
                run["codex_pid"] = process.pid
                store.save_run(run)
                try:
                    process.communicate(prompt, timeout=timeout)
                except subprocess.TimeoutExpired:
                    terminate_process_tree(process.pid)
                    process.wait(timeout=15)
                    terminal_status = "timed_out"
                    error = f"Codex exceeded timeout of {timeout} seconds"
                run["exit_code"] = process.returncode
        except OSError as exc:
            atomic_write_text(stderr_path, f"{type(exc).__name__}: {exc}\n")
            run["exit_code"] = None
            error = f"could not launch Codex: {exc}"
        run["codex_pid"] = None
        event_state = _events(stdout_path)
        if event_state["thread_id"]:
            session_id = str(event_state["thread_id"])
            run["session_id"] = session_id
        _copy_attempt_artifacts(attempt_dir, run_dir)
        store.save_run(run)

        if _mark_cancel_requested(run_dir):
            terminal_status = "cancelled"
            error = "run was stopped"
            break
        if terminal_status == "timed_out":
            break
        if run["exit_code"] == 0 and event_state["turn_completed"]:
            terminal_status = "succeeded"
            error = None
            break
        if event_state["turn_started"]:
            error = str(event_state.get("last_error") or "Codex turn failed")
            break
        if _deterministic_failure(stderr_path, event_state):
            error = str(
                event_state.get("last_error")
                or stderr_path.read_text(encoding="utf-8", errors="replace").strip()
                or "Codex rejected the local configuration"
            )
            break
        error = str(
            event_state.get("last_error")
            or stderr_path.read_text(encoding="utf-8", errors="replace").strip()
            or f"Codex exited before turn.started (exit {run['exit_code']})"
        )
        if attempt < 3:
            time.sleep(5 if attempt == 1 else 30)

    run["status"] = terminal_status
    run["error"] = error
    run["finished_at"] = iso()
    store.save_run(run)
    return run


def _abandon_owner(
    store: Store,
    job_id: str,
    owner: dict[str, Any] | None,
) -> None:
    if not owner:
        return
    run_id = owner.get("run_id")
    if run_id:
        path = store.run_dir(job_id, run_id) / "run.json"
        if path.is_file():
            run = read_json(path)
            if run.get("status") in {"starting", "running"}:
                run["status"] = "abandoned"
                run["finished_at"] = iso()
                run["error"] = "runner process disappeared"
                store.save_run(run)
                _finish_job_state(
                    store,
                    job_id,
                    run,
                    scheduled=run.get("trigger") == "scheduled",
                )
    if run_id:
        store.release_active(job_id, str(run_id))


def reconcile_stale_runs(store: Store, job_id: str) -> list[str]:
    """Mark runs whose recorded runner process has disappeared."""
    stale: list[dict[str, Any]] = []
    with store.short_lock(job_id):
        for listed in store.list_runs(job_id):
            if listed.get("status") not in {"starting", "running"}:
                continue
            pid = listed.get("runner_pid")
            if not pid:
                age = now_local() - parse_iso(listed["created_at"]).astimezone()
                if age.total_seconds() <= 30:
                    continue
            elif process_alive(pid, listed.get("runner_start_token")):
                continue
            path = store.run_dir(job_id, listed["id"]) / "run.json"
            current = read_json(path)
            if current.get("status") not in {"starting", "running"}:
                continue
            current["status"] = "abandoned"
            current["finished_at"] = iso()
            current["codex_pid"] = None
            current["error"] = "runner process disappeared"
            store.save_run(current)
            stale.append(current)
    for run in stale:
        store.release_active(job_id, run["id"])
        _finish_job_state(
            store,
            job_id,
            run,
            scheduled=run.get("trigger") == "scheduled",
        )
    return [run["id"] for run in stale]


def _finish_job_state(
    store: Store,
    job_id: str,
    run: dict[str, Any],
    *,
    scheduled: bool,
) -> dict[str, Any]:
    with store.short_lock(job_id):
        job = store.load_job(job_id)
        stats = job["stats"]
        stats["last_run_id"] = run["id"]
        stats["last_result"] = run["status"]
        if run["status"] == "succeeded":
            stats["consecutive_failures"] = 0
        elif run["status"] in FAILURE_STATUSES:
            stats["consecutive_failures"] = int(
                stats.get("consecutive_failures", 0)
            ) + 1

        terminal = False
        if job["schedule"]["kind"] == "at" and scheduled:
            if run["status"] in FAILURE_STATUSES:
                job["status"] = "failed"
            elif run["status"] == "cancelled":
                job["status"] = "cancelled"
            else:
                job["status"] = "completed"
            terminal = True
        count = job["limits"].get("count")
        if scheduled and count and stats["scheduled_started"] >= int(count):
            job["status"] = "completed"
            terminal = True
        if (
            job["schedule"]["kind"] != "at"
            and stats["consecutive_failures"] >= 3
            and job["status"] == "active"
        ):
            job["status"] = "paused"
            terminal = True
        job["updated_at"] = iso()
        store.save_job(job)
        for candidate in store.retention_candidates(job):
            store.prune_run(candidate)
    if terminal:
        backend_for(job["backend"], state_root=store.root).unregister(job)
    return job


def _run_with_overlap(
    store: Store,
    job: dict[str, Any],
    run: dict[str, Any],
    run_dir: Path,
    *,
    scheduled: bool,
    resume_session: str | None,
    preferred_cwd: Path | None = None,
) -> dict[str, Any]:
    acquired = True
    if job["overlap_policy"] == "skip":
        acquired, previous = store.acquire_active(
            job["id"],
            run_id=run["id"],
            pid=os.getpid(),
            start_token=process_start_token(os.getpid()),
        )
        if acquired:
            _abandon_owner(store, job["id"], previous)
    if not acquired:
        run["status"] = "skipped_overlap"
        run["finished_at"] = iso()
        run["error"] = "another run of this job is active"
        store.save_run(run)
        _finish_job_state(
            store,
            job["id"],
            run,
            scheduled=scheduled,
        )
        return run
    try:
        if scheduled:
            with store.short_lock(job["id"]):
                current = store.load_job(job["id"])
                if current["status"] != "active":
                    run["status"] = "cancelled"
                    run["finished_at"] = iso()
                    run["error"] = "job became inactive before the run started"
                    store.save_run(run)
                    return run
                count = current["limits"].get("count")
                if count and int(
                    current["stats"].get("scheduled_started", 0)
                ) >= int(count):
                    run["status"] = "cancelled"
                    run["finished_at"] = iso()
                    run["error"] = "schedule count was reached before the run started"
                    store.save_run(run)
                    return run
                current["stats"]["scheduled_started"] = (
                    int(current["stats"].get("scheduled_started", 0)) + 1
                )
                current["updated_at"] = iso()
                store.save_job(current)
        try:
            completed = execute_run(
                store,
                run,
                run_dir,
                job,
                resume_session=resume_session,
                preferred_cwd=preferred_cwd,
            )
        except Exception as exc:
            completed = read_json(run_dir / "run.json")
            completed["status"] = "failed"
            completed["finished_at"] = iso()
            completed["codex_pid"] = None
            completed["error"] = f"{type(exc).__name__}: {exc}"
            store.save_run(completed)
        if (
            run["trigger"] != "retry"
            and job["session_mode"] == "resume_fixed"
            and completed.get("session_id")
        ):
            with store.short_lock(job["id"]):
                current = store.load_job(job["id"])
                same_generation = int(
                    current.get("session_generation", 1)
                ) == int(job.get("session_generation", 1))
                if (
                    current.get("session_mode") == "resume_fixed"
                    and same_generation
                    and not current.get("fixed_session_id")
                ):
                    current["fixed_session_id"] = completed["session_id"]
                    current["updated_at"] = iso()
                    store.save_job(current)
        _finish_job_state(
            store,
            job["id"],
            completed,
            scheduled=scheduled,
        )
        return completed
    finally:
        if job["overlap_policy"] == "skip":
            store.release_active(job["id"], run["id"])


def trigger_job(store: Store, reference: str) -> dict[str, Any] | None:
    job = store.resolve_job(reference)
    reconcile_stale_runs(store, job["id"])
    job = store.load_job(job["id"])
    if job["status"] != "active":
        return None
    now = now_local()
    due = latest_due(job["schedule"], now)
    if due is None:
        return None
    deadline = job["limits"].get("until")
    if deadline and due > parse_iso(deadline).astimezone(due.tzinfo):
        job["status"] = "completed"
        job["updated_at"] = iso()
        store.save_job(job)
        backend_for(job["backend"], state_root=store.root).unregister(job)
        return None
    count = job["limits"].get("count")
    if count and int(job["stats"].get("scheduled_started", 0)) >= int(count):
        job["status"] = "completed"
        job["updated_at"] = iso()
        store.save_job(job)
        backend_for(job["backend"], state_root=store.root).unregister(job)
        return None
    key = occurrence_key(job["schedule"], due)
    if not store.claim_occurrence(
        job["id"],
        key,
        {"claimed_at": iso(), "scheduled_for": iso(due)},
    ):
        return None
    previous = job["stats"].get("last_scheduled_for")
    missed = count_missed(
        job["schedule"],
        parse_iso(previous).astimezone(due.tzinfo) if previous else None,
        due,
    )
    with store.short_lock(job["id"]):
        current = store.load_job(job["id"])
        current["stats"]["last_scheduled_for"] = iso(due)
        current["updated_at"] = iso()
        store.save_job(current)
    run, run_dir = store.new_run(
        job,
        trigger="scheduled",
        scheduled_for=iso(due),
        occurrence_key=key,
    )
    run["coalesced_occurrences"] = missed
    store.save_run(run)
    session_id = (
        job.get("fixed_session_id")
        if job["session_mode"] == "resume_fixed"
        else None
    )
    return _run_with_overlap(
        store,
        job,
        run,
        run_dir,
        scheduled=True,
        resume_session=session_id,
    )


def spawn_trigger(store: Store, reference: str) -> dict[str, Any]:
    """Detach the long-running trigger so native scheduler units stay short."""
    job = store.resolve_job(reference)
    command = [
        job["python_command"],
        job["runner_entrypoint"],
        "--state-dir",
        str(store.root),
        "_execute-trigger",
        job["id"],
    ]
    kwargs: dict[str, Any] = {
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
        "cwd": str(Path(job["runner_entrypoint"]).parent),
        "close_fds": True,
    }
    if os.name == "nt":
        kwargs["creationflags"] = (
            subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
        )
    else:
        kwargs["start_new_session"] = True
    try:
        process = subprocess.Popen(command, **kwargs)
    except OSError as exc:
        raise SchedulerError(f"could not detach scheduled runner: {exc}") from exc
    return {"spawned_pid": process.pid, "job_id": job["id"]}


def run_now(store: Store, reference: str) -> dict[str, Any]:
    job = store.resolve_job(reference)
    reconcile_stale_runs(store, job["id"])
    run, run_dir = store.new_run(
        job,
        trigger="run_now",
        scheduled_for=None,
        occurrence_key=None,
    )
    session_id = (
        job.get("fixed_session_id")
        if job["session_mode"] == "resume_fixed"
        else None
    )
    return _run_with_overlap(
        store,
        job,
        run,
        run_dir,
        scheduled=False,
        resume_session=session_id,
    )


def retry_run(store: Store, reference: str) -> dict[str, Any]:
    original, original_dir = store.resolve_run(reference)
    if original.get("tombstone"):
        raise SchedulerError("a pruned run cannot be retried")
    if original["status"] not in TERMINAL_STATUSES:
        raise SchedulerError("only a terminal run can be retried")
    snapshot = read_json(original_dir / "job_snapshot.json")
    current_job = store.load_job(original["job_id"])
    prompt = (original_dir / "prompt.txt").read_text(encoding="utf-8")
    session_id = original.get("session_id")
    if snapshot["session_mode"] == "resume_fixed" and not session_id:
        raise SchedulerError(
            "fixed session is missing; reset the job session before running again"
        )
    preferred_cwd = None
    workspace_path = original_dir / "workspace.json"
    if session_id and workspace_path.is_file():
        workspace = read_json(workspace_path)
        candidate = Path(workspace["cwd"])
        if candidate.is_dir():
            preferred_cwd = candidate
        elif snapshot["session_mode"] == "resume_fixed":
            raise SchedulerError("the fixed-session workspace no longer exists")
        else:
            session_id = None
    run, run_dir = store.new_run(
        current_job,
        trigger="retry",
        scheduled_for=None,
        occurrence_key=None,
        retry_of=original["id"],
        job_snapshot=snapshot,
        prompt=prompt,
    )
    return _run_with_overlap(
        store,
        snapshot,
        run,
        run_dir,
        scheduled=False,
        resume_session=session_id,
        preferred_cwd=preferred_cwd,
    )


def stop_run(store: Store, reference: str) -> dict[str, Any]:
    run, run_dir = store.resolve_run(reference)
    if run.get("status") not in {"starting", "running"}:
        raise SchedulerError(f"run is not active: {run['status']}")
    atomic_write_text(run_dir / "cancel.requested", f"{iso()}\n")
    codex_pid = run.get("codex_pid")
    if codex_pid and process_alive(codex_pid):
        terminate_process_tree(codex_pid)
    runner_pid = run.get("runner_pid")
    if runner_pid and runner_pid != os.getpid() and process_alive(
        runner_pid,
        run.get("runner_start_token"),
    ):
        deadline = time.monotonic() + 10
        while process_alive(runner_pid) and time.monotonic() < deadline:
            time.sleep(0.1)
        if process_alive(runner_pid, run.get("runner_start_token")):
            terminate_process_tree(runner_pid, grace_seconds=2)
    latest = read_json(run_dir / "run.json")
    if latest.get("status") in {"starting", "running"}:
        latest["status"] = "cancelled"
        latest["finished_at"] = iso()
        latest["error"] = "run was stopped"
        latest["codex_pid"] = None
        store.save_run(latest)
        store.release_active(latest["job_id"], latest["id"])
        _finish_job_state(
            store,
            latest["job_id"],
            latest,
            scheduled=latest.get("trigger") == "scheduled",
        )
    return read_json(run_dir / "run.json")
