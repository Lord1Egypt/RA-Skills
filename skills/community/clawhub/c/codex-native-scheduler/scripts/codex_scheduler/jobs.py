"""Job creation, update, and native registration."""

from __future__ import annotations

import copy
import shutil
import sys
import uuid
from pathlib import Path
from typing import Any

from .backends import backend_for
from .errors import SchedulerError
from .storage import Store
from .util import (
    SCHEMA_VERSION,
    captured_environment,
    entrypoint_path,
    iso,
    make_id,
    now_local,
    parse_iso,
    resolve_codex_command,
    resolve_executable,
)
from .workspaces import ensure_direct_workspace, worktree_settings


def selected_backend(config: dict[str, Any], override: str | None) -> str:
    requested = override or str(config.get("backend", "auto"))
    backend = backend_for(requested, state_root=Path("."))
    return backend.name


def _configured_codex_command(
    defaults: dict[str, Any],
    requested: str | None,
) -> list[str]:
    if requested:
        return resolve_codex_command(requested)
    configured = defaults.get("codex_command")
    if isinstance(configured, list) and configured:
        paths = [str(resolve_executable(str(value))) for value in configured]
        return paths
    if isinstance(configured, str):
        return resolve_codex_command(configured)
    return resolve_codex_command()


def _configured_python(defaults: dict[str, Any]) -> str:
    configured = defaults.get("python_command")
    return str(resolve_executable(str(configured or sys.executable)))


def configured_commands(
    config: dict[str, Any],
    codex_path: str | None = None,
) -> tuple[str, list[str]]:
    defaults = dict(config.get("defaults", {}))
    return (
        _configured_python(defaults),
        _configured_codex_command(defaults, codex_path),
    )


def create_job(
    store: Store,
    *,
    prompt: str,
    name: str | None,
    cwd: Path,
    schedule: dict[str, Any],
    backend_name: str | None,
    session_mode: str,
    session_id: str | None,
    workspace_mode: str,
    base_policy: str,
    base_ref: str | None,
    allow_dirty: bool,
    overlap_policy: str,
    profile: str | None,
    codex_config: list[str],
    codex_path: str | None,
    env_names: list[str],
    env_assignments: list[str],
    timeout_seconds: int | None,
    count: int | None,
    until: str | None,
    retention: dict[str, Any],
) -> dict[str, Any]:
    config = store.load_config()
    defaults = dict(config.get("defaults", {}))
    store.ensure_unique_name(name)
    cwd = cwd.expanduser().resolve()
    if not cwd.is_dir():
        raise SchedulerError(f"working directory does not exist: {cwd}")
    if session_id is not None:
        try:
            session_id = str(uuid.UUID(session_id.strip()))
        except ValueError as exc:
            raise SchedulerError(
                "--session-id must be a Codex session UUID"
            ) from exc
    if session_mode == "resume_fixed" and overlap_policy == "parallel":
        raise SchedulerError("resume_fixed requires --overlap skip")
    if session_id is not None and session_mode != "resume_fixed":
        raise SchedulerError("--session-id requires --session-mode resume_fixed")
    if session_id is not None and workspace_mode != "direct":
        raise SchedulerError("--session-id requires --workspace direct")
    if session_id is not None and (profile is not None or codex_config):
        raise SchedulerError(
            "--session-id cannot be combined with --profile or "
            "-c/--codex-config"
        )
    if workspace_mode == "direct" and (
        base_ref is not None or base_policy != "latest"
    ):
        raise SchedulerError("--base-policy and --base-ref require worktree mode")
    if workspace_mode == "worktree" and allow_dirty:
        raise SchedulerError("--allow-dirty applies only to direct workspace mode")
    if workspace_mode == "direct":
        is_git = ensure_direct_workspace(cwd, allow_dirty=allow_dirty)
        workspace = {
            "mode": "direct",
            "allow_dirty": allow_dirty,
            "is_git": is_git,
        }
    else:
        workspace = worktree_settings(
            cwd,
            base_policy=base_policy,
            base_ref=base_ref,
        )
    environment, missing = captured_environment(env_names, env_assignments)
    actual_backend = selected_backend(config, backend_name)
    python_command, codex_command = configured_commands(config, codex_path)
    job_id = make_id("job-")
    now = iso()
    deadline_value = parse_iso(until) if until else None
    if deadline_value and deadline_value.astimezone() <= now_local():
        raise SchedulerError("--until must be in the future")
    deadline = (
        deadline_value.isoformat(timespec="seconds")
        if deadline_value
        else None
    )
    if count is not None and count < 1:
        raise SchedulerError("--count must be at least 1")
    if schedule["kind"] == "at" and (count is not None or deadline is not None):
        raise SchedulerError("--count and --until apply only to recurring jobs")
    job = {
        "schema_version": SCHEMA_VERSION,
        "id": job_id,
        "name": name,
        "revision": 1,
        "status": "active",
        "created_at": now,
        "updated_at": now,
        "backend": actual_backend,
        "schedule": schedule,
        "limits": {"count": count, "until": deadline},
        "stats": {
            "scheduled_started": 0,
            "consecutive_failures": 0,
            "last_scheduled_for": None,
            "last_run_id": None,
            "last_result": None,
        },
        "cwd": str(cwd),
        "workspace": workspace,
        "session_mode": session_mode,
        "session_generation": 1,
        "fixed_session_id": session_id,
        "session_seeded": session_id is not None,
        "overlap_policy": overlap_policy,
        "codex": {
            "command": codex_command,
            "profile": (
                None
                if session_id is not None
                else profile if profile is not None else defaults.get("profile")
            ),
            "config": list(codex_config),
            "strict_config": True,
        },
        "environment": environment,
        "environment_missing": missing,
        "timeout_seconds": (
            timeout_seconds
            if timeout_seconds is not None
            else defaults.get("timeout_seconds")
        ),
        "retention": retention,
        "python_command": python_command,
        "runner_entrypoint": str(entrypoint_path().resolve()),
    }
    store.create_job(job, prompt)
    backend = backend_for(actual_backend, state_root=store.root)
    try:
        backend.register(job)
    except Exception:
        shutil.rmtree(store.job_dir(job_id), ignore_errors=True)
        raise
    return job


def update_job(
    store: Store,
    job: dict[str, Any],
    *,
    changes: dict[str, Any],
    prompt: str | None,
    reset_session: bool,
) -> dict[str, Any]:
    previous = copy.deepcopy(job)
    previous_prompt = store.prompt(job["id"])
    seeded_session_continues = (
        bool(job.get("session_seeded"))
        and not reset_session
        and changes.get("session_mode", job["session_mode"]) == "resume_fixed"
    )
    if seeded_session_continues and "codex" in changes:
        raise SchedulerError(
            "profile and Codex overrides cannot be changed while continuing "
            "a session created with --session-id; use --reset-session first"
        )
    if "name" in changes:
        store.ensure_unique_name(changes["name"], excluding=job["id"])
    cwd_or_workspace_changed = bool(
        {"cwd", "workspace"} & changes.keys()
    )
    if (
        job["session_mode"] == "resume_fixed"
        and cwd_or_workspace_changed
        and not reset_session
    ):
        raise SchedulerError(
            "changing cwd or workspace mode for resume_fixed requires "
            "--reset-session"
        )
    for key, value in changes.items():
        job[key] = value
    session_mode_changed = bool(
        changes.get("session_mode")
        and changes["session_mode"] != previous["session_mode"]
    )
    if session_mode_changed:
        job["fixed_session_id"] = None
    if job["session_mode"] == "resume_fixed" and job["overlap_policy"] == "parallel":
        raise SchedulerError("resume_fixed requires overlap_policy=skip")
    if job["schedule"]["kind"] == "at" and any(
        job["limits"].get(key) is not None for key in ("count", "until")
    ):
        raise SchedulerError("one-shot jobs cannot have --count or --until")
    if reset_session or session_mode_changed:
        job["fixed_session_id"] = None
        job["session_seeded"] = False
        job["session_generation"] = int(
            previous.get("session_generation", 1)
        ) + 1
    if reset_session:
        workspace = job.get("workspace", {})
        if workspace.get("mode") == "worktree":
            workspace["generation"] = int(workspace.get("generation", 1)) + 1
    job["revision"] = int(job["revision"]) + 1
    job["updated_at"] = iso()
    if prompt is not None:
        store.save_prompt(job["id"], prompt)
    store.save_job(job, save_revision=True)
    backend = backend_for(job["backend"], state_root=store.root)
    try:
        if job["status"] == "active":
            backend.register(job)
    except Exception:
        store.save_prompt(job["id"], previous_prompt)
        store.save_job(previous)
        if previous["status"] == "active":
            backend_for(previous["backend"], state_root=store.root).register(previous)
        raise
    return job


def unregister_job(store: Store, job: dict[str, Any]) -> None:
    backend_for(job["backend"], state_root=store.root).unregister(job)


def set_job_status(
    store: Store,
    job: dict[str, Any],
    status: str,
    *,
    unregister: bool,
) -> dict[str, Any]:
    if unregister:
        unregister_job(store, job)
    job["status"] = status
    job["updated_at"] = iso()
    store.save_job(job)
    return job


def resume_job(store: Store, job: dict[str, Any]) -> dict[str, Any]:
    if job["schedule"]["kind"] == "at":
        raise SchedulerError("one-shot jobs cannot be resumed")
    if job["status"] != "paused":
        raise SchedulerError(
            f"only a paused recurring job can be resumed: {job['status']}"
        )
    previous = job["status"]
    job["status"] = "active"
    job["updated_at"] = iso()
    store.save_job(job)
    try:
        backend_for(job["backend"], state_root=store.root).register(job)
    except Exception:
        job["status"] = previous
        store.save_job(job)
        raise
    return job


def active_runs(store: Store, job_id: str) -> list[dict[str, Any]]:
    return [
        run
        for run in store.list_runs(job_id)
        if run.get("status") in {"starting", "running"}
    ]
