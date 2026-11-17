"""Command-line interface for Codex Native Scheduler."""

from __future__ import annotations

import argparse
import copy
import json
import shutil
import sys
from pathlib import Path
from typing import Any

from .backends import backend_for
from .errors import SchedulerError
from .jobs import (
    active_runs,
    configured_commands,
    create_job,
    resume_job,
    set_job_status,
    unregister_job,
    update_job,
)
from .runner import (
    reconcile_stale_runs,
    retry_run,
    run_now,
    spawn_trigger,
    stop_run,
    trigger_job,
)
from .schedules import make_schedule, next_due
from .storage import Store
from .util import (
    iso,
    now_local,
    parse_duration,
    parse_iso,
    process_alive,
    run_checked,
)
from .workspaces import (
    ensure_direct_workspace,
    remove_safe_worktrees,
    worktree_settings,
)

BACKEND_CHOICES = ["auto", "launchd", "systemd", "task-scheduler"]


def _json(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def _prompt_from_args(
    args: argparse.Namespace,
    *,
    required: bool,
) -> str | None:
    sources = [
        args.prompt is not None,
        args.prompt_file is not None,
        bool(getattr(args, "stdin", False)),
    ]
    if sum(sources) > 1:
        raise SchedulerError(
            "choose exactly one prompt source: --prompt, --prompt-file, or --stdin"
        )
    if args.prompt is not None:
        value = args.prompt
    elif args.prompt_file is not None:
        try:
            value = Path(args.prompt_file).expanduser().read_text(encoding="utf-8")
        except OSError as exc:
            raise SchedulerError(f"cannot read prompt file: {exc}") from exc
    elif getattr(args, "stdin", False) or (required and not sys.stdin.isatty()):
        value = sys.stdin.read()
    elif required:
        raise SchedulerError(
            "provide a prompt with --prompt, --prompt-file, or --stdin"
        )
    else:
        return None
    if not value.strip():
        raise SchedulerError("prompt cannot be empty")
    return value


def _schedule_from_args(
    args: argparse.Namespace,
    *,
    required: bool,
) -> dict[str, Any] | None:
    values = [args.at, args.every, args.daily_at, args.weekly_at]
    if not any(value is not None for value in values):
        if required:
            raise SchedulerError("a schedule is required")
        return None
    return make_schedule(
        at=args.at,
        every=args.every,
        daily_at=args.daily_at,
        weekly_at=args.weekly_at,
        now=now_local(),
    )


def _retention(args: argparse.Namespace) -> dict[str, Any]:
    if getattr(args, "retention_forever", False):
        if (
            getattr(args, "retention_days", None) is not None
            or getattr(args, "retain_runs", None) is not None
        ):
            raise SchedulerError(
                "--retention-forever cannot be combined with bounded retention"
            )
        return {"mode": "forever"}
    days = getattr(args, "retention_days", None)
    runs = getattr(args, "retain_runs", None)
    if days is None and runs is None:
        return {"mode": "forever"}
    if days is not None and days < 1:
        raise SchedulerError("--retention-days must be at least 1")
    if runs is not None and runs < 0:
        raise SchedulerError("--retain-runs cannot be negative")
    return {"mode": "bounded", "days": days, "retain_runs": runs}


def _redact_job(job: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(job)
    if "environment" in result:
        result["environment"] = {
            key: "<redacted>" for key in result["environment"]
        }
    return result


def _add_schedule_arguments(parser: argparse.ArgumentParser) -> None:
    group = parser.add_argument_group("schedule")
    group.add_argument("--at", help="one future ISO timestamp or duration")
    group.add_argument("--every", help="anchored interval such as 30m or 2h")
    group.add_argument("--daily-at", help="local wall-clock time, HH:MM")
    group.add_argument("--weekly-at", help="local weekday and time, e.g. mon@09:30")


def _add_prompt_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--stdin", action="store_true")


def _add_retention_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--retention-forever", action="store_true")
    parser.add_argument("--retention-days", type=int)
    parser.add_argument("--retain-runs", type=int)


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        prog="codex-schedule",
        description="Schedule Codex CLI jobs through the native OS scheduler.",
    )
    root.add_argument(
        "--state-dir",
        type=Path,
        help="override the private scheduler state directory",
    )
    sub = root.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="initialize the private state directory")

    create = sub.add_parser("create", help="create and register a job")
    create.add_argument("--name")
    create.add_argument("--cwd", type=Path, default=Path.cwd())
    create.add_argument("--backend", choices=BACKEND_CHOICES)
    create.add_argument(
        "--session-mode",
        choices=["new_each_run", "resume_fixed"],
        default="new_each_run",
    )
    create.add_argument(
        "--session-id",
        help="existing Codex session to use with resume_fixed in direct mode",
    )
    create.add_argument(
        "--workspace",
        choices=["direct", "worktree"],
        default="direct",
    )
    create.add_argument(
        "--base-policy",
        choices=["snapshot", "latest"],
        default="latest",
    )
    create.add_argument("--base-ref")
    create.add_argument("--allow-dirty", action="store_true")
    create.add_argument(
        "--overlap",
        choices=["skip", "parallel"],
        default="skip",
    )
    create.add_argument("--profile")
    create.add_argument(
        "-c",
        "--codex-config",
        action="append",
        default=[],
        metavar="KEY=VALUE",
    )
    create.add_argument("--codex-path")
    create.add_argument("--capture-env", action="append", default=[])
    create.add_argument("--env", action="append", default=[], metavar="KEY=VALUE")
    create.add_argument("--timeout", help="run timeout such as 2h")
    create.add_argument("--count", type=int)
    create.add_argument("--until", help="recurring schedule deadline (ISO 8601)")
    _add_schedule_arguments(create)
    _add_prompt_arguments(create)
    _add_retention_arguments(create)

    sub.add_parser("list", help="list jobs")

    show = sub.add_parser("show", help="show one job")
    show.add_argument("job")

    status = sub.add_parser("status", help="show scheduler and native state")
    status.add_argument("job")

    runs = sub.add_parser("runs", help="list runs for one job")
    runs.add_argument("job")

    run_show = sub.add_parser("run-show", help="show one run")
    run_show.add_argument("run")

    run_command = sub.add_parser("run-now", help="start a manual run now")
    run_command.add_argument("job")

    retry = sub.add_parser("retry", help="retry a terminal run")
    retry.add_argument("run")

    stop = sub.add_parser("stop", help="stop an active run")
    stop.add_argument("run")

    pause = sub.add_parser("pause", help="pause future scheduled runs")
    pause.add_argument("job")

    resume = sub.add_parser("resume", help="resume future scheduled runs")
    resume.add_argument("job")

    cancel = sub.add_parser("cancel", help="cancel a pending one-shot job")
    cancel.add_argument("job")

    update = sub.add_parser("update", help="update a job in place")
    update.add_argument("job")
    update.add_argument("--name")
    update.add_argument("--cwd", type=Path)
    update.add_argument("--workspace", choices=["direct", "worktree"])
    update.add_argument("--base-policy", choices=["snapshot", "latest"])
    update.add_argument("--base-ref")
    dirty = update.add_mutually_exclusive_group()
    dirty.add_argument(
        "--allow-dirty",
        action="store_const",
        const=True,
        dest="allow_dirty",
        default=None,
    )
    dirty.add_argument(
        "--require-clean",
        action="store_const",
        const=False,
        dest="allow_dirty",
    )
    update.add_argument("--session-mode", choices=["new_each_run", "resume_fixed"])
    update.add_argument("--overlap", choices=["skip", "parallel"])
    update.add_argument("--profile")
    update.add_argument(
        "-c",
        "--codex-config",
        action="append",
        default=None,
        metavar="KEY=VALUE",
    )
    update.add_argument("--timeout")
    update.add_argument("--no-timeout", action="store_true")
    update.add_argument("--count", type=int)
    update.add_argument("--until")
    update.add_argument("--reset-session", action="store_true")
    _add_schedule_arguments(update)
    _add_prompt_arguments(update)
    _add_retention_arguments(update)

    prune = sub.add_parser("prune", help="apply job retention")
    prune.add_argument("job", nargs="?")
    prune.add_argument("--dry-run", action="store_true")

    delete = sub.add_parser("delete", help="permanently delete a job and its runs")
    delete.add_argument("job")
    delete.add_argument("--stop", action="store_true")
    delete.add_argument("--yes", action="store_true")

    sub.add_parser(
        "decommission",
        help="unregister all jobs while preserving state",
    )

    purge = sub.add_parser("purge", help="permanently remove decommissioned state")
    purge.add_argument("--yes", action="store_true")

    doctor = sub.add_parser("doctor", help="diagnose runtime and backend access")
    doctor.add_argument("--backend", choices=BACKEND_CHOICES)

    trigger = sub.add_parser("_trigger", help=argparse.SUPPRESS)
    trigger.add_argument("job")
    execute_trigger = sub.add_parser("_execute-trigger", help=argparse.SUPPRESS)
    execute_trigger.add_argument("job")
    return root


def _handle_create(store: Store, args: argparse.Namespace) -> dict[str, Any]:
    schedule = _schedule_from_args(args, required=True)
    assert schedule is not None
    prompt = _prompt_from_args(args, required=True)
    assert prompt is not None
    timeout = parse_duration(args.timeout) if args.timeout else None
    return create_job(
        store,
        prompt=prompt,
        name=args.name,
        cwd=args.cwd,
        schedule=schedule,
        backend_name=args.backend,
        session_mode=args.session_mode,
        session_id=args.session_id,
        workspace_mode=args.workspace,
        base_policy=args.base_policy,
        base_ref=args.base_ref,
        allow_dirty=args.allow_dirty,
        overlap_policy=args.overlap,
        profile=args.profile,
        codex_config=args.codex_config,
        codex_path=args.codex_path,
        env_names=args.capture_env,
        env_assignments=args.env,
        timeout_seconds=timeout,
        count=args.count,
        until=args.until,
        retention=_retention(args),
    )


def _handle_update(
    store: Store,
    args: argparse.Namespace,
) -> dict[str, Any]:
    job = store.resolve_job(args.job)
    changes: dict[str, Any] = {}
    for key in ("name", "session_mode"):
        value = getattr(args, key)
        if value is not None:
            changes[key] = value
    if args.overlap is not None:
        changes["overlap_policy"] = args.overlap
    schedule = _schedule_from_args(args, required=False)
    if schedule is not None:
        changes["schedule"] = schedule
    if args.profile is not None or args.codex_config is not None:
        codex = copy.deepcopy(job["codex"])
        if args.profile is not None:
            codex["profile"] = args.profile
        if args.codex_config is not None:
            codex["config"] = args.codex_config
        changes["codex"] = codex
    if args.no_timeout:
        changes["timeout_seconds"] = None
    elif args.timeout:
        changes["timeout_seconds"] = parse_duration(args.timeout)
    if args.count is not None or args.until is not None:
        limits = copy.deepcopy(job["limits"])
        if args.count is not None:
            if args.count < 1:
                raise SchedulerError("--count must be at least 1")
            limits["count"] = args.count
        if args.until is not None:
            deadline = parse_iso(args.until)
            if deadline.astimezone() <= now_local():
                raise SchedulerError("--until must be in the future")
            limits["until"] = iso(deadline)
        changes["limits"] = limits
    if (
        args.retention_forever
        or args.retention_days is not None
        or args.retain_runs is not None
    ):
        changes["retention"] = _retention(args)
    if (
        args.cwd is not None
        or args.workspace is not None
        or args.allow_dirty is not None
    ):
        cwd = (args.cwd or Path(job["cwd"])).expanduser().resolve()
        mode = args.workspace or job["workspace"]["mode"]
        if mode == "worktree" and args.allow_dirty is not None:
            raise SchedulerError(
                "--allow-dirty and --require-clean apply only to direct mode"
            )
        if mode == "direct":
            allow_dirty = (
                args.allow_dirty
                if args.allow_dirty is not None
                else bool(job["workspace"].get("allow_dirty"))
            )
            is_git = ensure_direct_workspace(cwd, allow_dirty=allow_dirty)
            workspace = {
                "mode": "direct",
                "allow_dirty": allow_dirty,
                "is_git": is_git,
            }
        else:
            workspace = worktree_settings(
                cwd,
                base_policy=args.base_policy
                or job["workspace"].get("base_policy", "latest"),
                base_ref=args.base_ref,
            )
        changes["cwd"] = str(cwd)
        changes["workspace"] = workspace
    elif args.base_policy is not None or args.base_ref is not None:
        if job["workspace"]["mode"] != "worktree":
            raise SchedulerError("--base-policy and --base-ref require worktree mode")
        workspace = worktree_settings(
            Path(job["cwd"]),
            base_policy=args.base_policy or job["workspace"]["base_policy"],
            base_ref=args.base_ref or job["workspace"].get("base_ref"),
        )
        changes["workspace"] = workspace
    prompt = _prompt_from_args(args, required=False)
    if not changes and prompt is None and not args.reset_session:
        raise SchedulerError("no update was requested")
    return update_job(
        store,
        job,
        changes=changes,
        prompt=prompt,
        reset_session=args.reset_session,
    )


def _doctor(store: Store, requested: str | None) -> dict[str, Any]:
    config = store.load_config()
    selected = requested or str(config.get("backend", "auto"))
    backend = backend_for(selected, state_root=store.root)
    jobs = store.list_jobs()
    stale = []
    for job in jobs:
        for run in store.list_runs(job["id"]):
            if run.get("status") not in {"starting", "running"}:
                continue
            if not process_alive(
                run.get("runner_pid"),
                run.get("runner_start_token"),
            ):
                stale.append({"job_id": job["id"], "run_id": run["id"]})
    runtime: dict[str, Any]
    try:
        python_command, codex_command = configured_commands(config)
        python_result = run_checked([python_command, "--version"], timeout=15)
        codex_result = run_checked([*codex_command, "--version"], timeout=15)
        login_result = run_checked(
            [*codex_command, "login", "status"],
            timeout=30,
        )
        runtime = {
            "python_command": python_command,
            "python_version": (
                python_result.stdout.strip() or python_result.stderr.strip()
            ),
            "codex_command": codex_command,
            "codex_version": (
                codex_result.stdout.strip() or codex_result.stderr.strip()
            ),
            "codex_available": codex_result.returncode == 0,
            "login_ok": login_result.returncode == 0,
            "login_detail": (
                login_result.stdout.strip() or login_result.stderr.strip()
            ),
        }
    except SchedulerError as exc:
        runtime = {"codex_available": False, "error": str(exc)}
    return {
        "state_dir": str(store.root),
        "config": str(store.config_path),
        "backend": backend.doctor(),
        "runtime": runtime,
        "stale_active_runs": stale,
        "jobs": len(jobs),
    }


def _prune(store: Store, reference: str | None, dry_run: bool) -> dict[str, Any]:
    jobs = (
        [store.resolve_job(reference)]
        if reference
        else store.list_jobs()
    )
    candidates = []
    for job in jobs:
        with store.short_lock(job["id"]):
            current = store.load_job(job["id"])
            for run in store.retention_candidates(current):
                candidates.append(
                    {"job_id": current["id"], "run_id": run["id"]}
                )
                if not dry_run:
                    store.prune_run(run)
    return {"dry_run": dry_run, "runs": candidates}


def dispatch(args: argparse.Namespace) -> Any:
    store = Store(args.state_dir)
    command = args.command
    if command == "init":
        store.initialize()
        return {"state_dir": str(store.root), "config": str(store.config_path)}
    if command == "create":
        return _redact_job(_handle_create(store, args))
    if command == "list":
        return [_redact_job(job) for job in store.list_jobs()]
    if command == "show":
        return _redact_job(store.resolve_job(args.job))
    if command == "status":
        job = store.resolve_job(args.job)
        reconcile_stale_runs(store, job["id"])
        job = store.load_job(job["id"])
        native = backend_for(job["backend"], state_root=store.root).status(job)
        due = (
            next_due(job["schedule"], now_local())
            if job["status"] == "active"
            else None
        )
        return {
            "job": _redact_job(job),
            "next_due": iso(due) if due else None,
            "native": native,
        }
    if command == "runs":
        job = store.resolve_job(args.job)
        reconcile_stale_runs(store, job["id"])
        return store.list_runs(job["id"])
    if command == "run-show":
        run, path = store.resolve_run(args.run)
        reconcile_stale_runs(store, run["job_id"])
        run = store.resolve_run(run["id"])[0]
        return {"run": run, "directory": str(path)}
    if command == "run-now":
        return run_now(store, args.job)
    if command == "retry":
        return retry_run(store, args.run)
    if command == "stop":
        return stop_run(store, args.run)
    if command == "pause":
        job = store.resolve_job(args.job)
        if job["schedule"]["kind"] == "at":
            raise SchedulerError(
                "one-shot jobs cannot be paused; use cancel before they start"
            )
        if job["status"] != "active":
            raise SchedulerError(
                f"only an active recurring job can be paused: {job['status']}"
            )
        return _redact_job(
            set_job_status(store, job, "paused", unregister=True)
        )
    if command == "resume":
        return _redact_job(resume_job(store, store.resolve_job(args.job)))
    if command == "cancel":
        job = store.resolve_job(args.job)
        with store.short_lock(job["id"]):
            job = store.load_job(job["id"])
            if job["schedule"]["kind"] != "at" or job["status"] != "active":
                raise SchedulerError(
                    "only an active pending one-shot can be cancelled"
                )
            if int(job["stats"].get("scheduled_started", 0)):
                raise SchedulerError("one-shot has already started")
            job["status"] = "cancelled"
            job["updated_at"] = iso()
            store.save_job(job)
        unregister_job(store, job)
        return _redact_job(job)
    if command == "update":
        return _redact_job(_handle_update(store, args))
    if command == "prune":
        return _prune(store, args.job, args.dry_run)
    if command == "delete":
        job = store.resolve_job(args.job)
        if not args.yes:
            raise SchedulerError("delete is permanent; repeat with --yes")
        reconcile_stale_runs(store, job["id"])
        active = active_runs(store, job["id"])
        if active and not args.stop:
            raise SchedulerError("job has active runs; pass --stop to stop them")
        unregister_job(store, job)
        for run in active:
            stop_run(store, run["id"])
        remove_safe_worktrees(job, state_root=store.root)
        shutil.rmtree(store.job_dir(job["id"]))
        return {"deleted": job["id"]}
    if command == "decommission":
        changed = []
        for job in store.list_jobs():
            unregister_job(store, job)
            job["status"] = "decommissioned"
            job["updated_at"] = iso()
            store.save_job(job)
            changed.append(job["id"])
        return {"decommissioned": changed, "state_preserved": str(store.root)}
    if command == "purge":
        if not args.yes:
            raise SchedulerError("purge is permanent; repeat with --yes")
        non_decommissioned = [
            job["id"]
            for job in store.list_jobs()
            if job["status"] != "decommissioned"
        ]
        if non_decommissioned:
            raise SchedulerError(
                "decommission all jobs before purge: "
                + ", ".join(non_decommissioned)
            )
        active = [
            run["id"]
            for job in store.list_jobs()
            for run in active_runs(store, job["id"])
        ]
        if active:
            raise SchedulerError(
                "stop active runs before purge: " + ", ".join(active)
            )
        for job in store.list_jobs():
            remove_safe_worktrees(job, state_root=store.root)
        root = store.root
        if root.name != "codex-native-scheduler":
            raise SchedulerError(
                "refusing to purge a nonstandard state directory"
            )
        shutil.rmtree(root)
        return {"purged": str(root)}
    if command == "doctor":
        return _doctor(store, args.backend)
    if command == "_trigger":
        job = store.resolve_job(args.job)
        if job["backend"] == "task-scheduler":
            return trigger_job(store, job["id"])
        return spawn_trigger(store, args.job)
    if command == "_execute-trigger":
        return trigger_job(store, args.job)
    raise SchedulerError(f"unknown command: {command}")


def main(argv: list[str] | None = None) -> int:
    try:
        args = parser().parse_args(argv)
        result = dispatch(args)
        if result is not None and not args.command.startswith("_"):
            _json(result)
        return 0
    except SchedulerError as exc:
        print(f"codex-schedule: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("codex-schedule: interrupted", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
