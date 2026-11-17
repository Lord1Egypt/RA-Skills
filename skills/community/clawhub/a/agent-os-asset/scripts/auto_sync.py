#!/usr/bin/env python3
"""LaunchAgent-friendly automatic Agent Asset maintenance runner / 面向 LaunchAgent 的自动 Agent Asset 维护 runner。

The runner intentionally owns scheduling, locking, debouncing, notifications, and
conditional indexing.  Project adapters remain the sole owners of extraction and
manifest mutation, invoked through ``--sync --execute``. Automatic promotion to
final knowledge requires a separate, explicit ``--auto-keep`` opt-in.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import plistlib
import stat
import subprocess
import sys
import tempfile
import time
from typing import Any, Iterator

from asset_pipeline import DEFAULT_INDEX_REGISTRY, index_scope_error


SCRIPT_PATH = Path(__file__).resolve()
SKILL_ROOT = SCRIPT_PATH.parents[1]
SECOND_BRAIN_ROUTINE = SKILL_ROOT / "skills" / "second-brain" / "scripts" / "routine_update.py"
DEFAULT_MIXED_FOLDER_ADAPTER = SKILL_ROOT / "scripts" / "mixed_folder_adapter.py"
STATE_NAME = "agent-asset-sync-state.json"
LOCK_NAME = "agent-asset-sync.lock"
DEFAULT_DEBOUNCE_SECONDS = 90
DEFAULT_HEARTBEAT_SECONDS = 2 * 60 * 60
DEFAULT_INTERVAL_SECONDS = 60 * 60


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def workspace(root: Path) -> Path:
    path = root.resolve() / ".cleanup-extracted"
    if path.is_symlink():
        raise ValueError("run-state directory cannot be a symlink / 运行状态目录不能是符号链接")
    path.resolve().relative_to(path)
    return path


def validate_workspace(root: Path, scope: str) -> str:
    root = root.resolve()
    scoped = (root / scope).resolve()
    scoped.relative_to(root)
    state = workspace(root)
    for name in (STATE_NAME, LOCK_NAME, "asset-manifest.jsonl", "asset-decisions.json",
                 "second-brain-asset-index", "agent-asset-sync-launchd.stdout.log",
                 "second-brain-routine.log", "second-brain-routine.lock",
                 "agent-asset-sync-launchd.stderr.log"):
        path = state / name
        path.resolve().relative_to(state)
        if path.is_symlink():
            raise ValueError("run-state paths cannot be symlinks / 运行状态路径不能是符号链接")
    (root / "Archived" / scoped.relative_to(root)).resolve().relative_to(root)
    return scoped.relative_to(root).as_posix()


def state_path(root: Path) -> Path:
    path = workspace(root) / STATE_NAME
    path.resolve().relative_to(workspace(root))
    if path.is_symlink():
        raise ValueError("sync state cannot be a symlink / 同步状态不能是符号链接")
    return path


def lock_path(root: Path) -> Path:
    path = workspace(root) / LOCK_NAME
    path.resolve().relative_to(workspace(root))
    if path.is_symlink():
        raise ValueError("sync lock cannot be a symlink / 同步锁不能是符号链接")
    return path


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
        temp_path = Path(handle.name)
    os.replace(temp_path, path)


def load_state(root: Path) -> dict[str, Any]:
    path = state_path(root)
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


@contextmanager
def sync_lock(root: Path) -> Iterator[bool]:
    """Use advisory flock so a WatchPaths burst cannot overlap a heartbeat run."""
    path = lock_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600)
    info = os.fstat(descriptor)
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        os.close(descriptor)
        raise ValueError("sync lock must be a private regular file, not a hardlink / 同步锁必须是独立的普通文件，不能是硬链接")
    with os.fdopen(descriptor, "r+", encoding="utf-8") as handle:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            yield False
            return
        handle.seek(0)
        handle.truncate()
        handle.write(f"pid={os.getpid()} started_at={utc_now()}\n")
        handle.flush()
        try:
            yield True
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def command_json(stdout: str) -> dict[str, Any]:
    """Adapters print one JSON object; keep a defensive fallback for wrapper noise."""
    try:
        payload = json.loads(stdout)
        return payload if isinstance(payload, dict) else {}
    except json.JSONDecodeError:
        start = stdout.rfind("\n{")
        if start >= 0:
            try:
                payload = json.loads(stdout[start + 1 :])
                return payload if isinstance(payload, dict) else {}
            except json.JSONDecodeError:
                pass
    return {}


def notify(title: str, message: str) -> None:
    """Best-effort local notification; messages contain counts/status, never bodies."""
    if sys.platform != "darwin":
        return
    script = f"display notification {json.dumps(message, ensure_ascii=False)} with title {json.dumps(title, ensure_ascii=False)}"
    subprocess.run(["osascript", "-e", script], check=False, capture_output=True, text=True)


def iso_age_seconds(value: str) -> float | None:
    if not value:
        return None
    try:
        timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return max(0.0, (datetime.now(timezone.utc) - timestamp).total_seconds())


def status_for_state(root: Path, heartbeat_seconds: int = DEFAULT_HEARTBEAT_SECONDS) -> dict[str, Any]:
    state = load_state(root)
    if not state:
        return {"status": "baseline_missing", "state_path": str(state_path(root))}
    last_sync = state.get("last_sync", {}) if isinstance(state.get("last_sync"), dict) else {}
    pending = int(last_sync.get("pending_review", 0) or 0)
    failed = int(last_sync.get("failed", 0) or 0)
    success_age = iso_age_seconds(str(state.get("last_success_at", "")))
    heartbeat_age = iso_age_seconds(str(state.get("last_heartbeat_at", "")))
    problems: list[str] = []
    if failed:
        problems.append("failed")
    if pending and success_age is not None and success_age > 15 * 60:
        problems.append("pending_over_15m")
    if heartbeat_age is None or heartbeat_age > heartbeat_seconds:
        problems.append("heartbeat_overdue")
    return {
        "status": "ok" if not problems else "attention",
        "problems": problems,
        "last_success_at": state.get("last_success_at", ""),
        "last_heartbeat_at": state.get("last_heartbeat_at", ""),
        "pending_review": pending,
        "failed": failed,
        "index_ready": bool(last_sync.get("index_ready")),
        "last_indexed_at": state.get("last_indexed_at", ""),
        "state_path": str(state_path(root)),
    }


def scoped_label(root: Path, scope: str) -> str:
    digest = hashlib.sha256(f"{root}\0{scope}".encode("utf-8")).hexdigest()[:16]
    return f"dev.agentos.asset-sync.{digest}"


def launch_agent_path(root: Path, scope: str) -> Path:
    return Path.home() / "Library" / "LaunchAgents" / f"{scoped_label(root, scope)}.plist"


def launch_agent_payload(root: Path, scope: str, cleanup_tool: Path, debounce_seconds: int,
                         *, auto_keep: bool = False) -> dict[str, Any]:
    scope = validate_workspace(root, scope)
    log_root = workspace(root)
    payload = {
        "Label": scoped_label(root, scope),
        "ProgramArguments": [
            sys.executable,
            str(SCRIPT_PATH),
            "--run",
            "--root",
            str(root),
            "--scope",
            scope,
            "--cleanup-tool",
            str(cleanup_tool),
            "--debounce-seconds",
            str(debounce_seconds),
        ],
        "WatchPaths": [str(root / scope), str(root / "Archived" / scope)],
        "StartInterval": DEFAULT_INTERVAL_SECONDS,
        "ProcessType": "Background",
        "StandardOutPath": str(log_root / "agent-asset-sync-launchd.stdout.log"),
        "StandardErrorPath": str(log_root / "agent-asset-sync-launchd.stderr.log"),
    }
    if auto_keep:
        payload["ProgramArguments"].append("--auto-keep")
    return payload


def install_launch_agent(root: Path, scope: str, cleanup_tool: Path, debounce_seconds: int,
                         *, auto_keep: bool = False) -> dict[str, Any]:
    scope = validate_workspace(root, scope)
    path = launch_agent_path(root, scope)
    path.parent.mkdir(parents=True, exist_ok=True)
    workspace(root).mkdir(parents=True, exist_ok=True)
    payload = launch_agent_payload(root, scope, cleanup_tool, debounce_seconds, auto_keep=auto_keep)
    with tempfile.NamedTemporaryFile("wb", dir=path.parent, delete=False) as handle:
        plistlib.dump(payload, handle)
        temp_path = Path(handle.name)
    os.replace(temp_path, path)
    uid = os.getuid()
    subprocess.run(["launchctl", "bootout", f"gui/{uid}", str(path)], check=False, capture_output=True, text=True)
    result = subprocess.run(
        ["launchctl", "bootstrap", f"gui/{uid}", str(path)], check=False, capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "launchctl bootstrap failed")
    return {"status": "installed", "label": payload["Label"], "plist": str(path)}


def uninstall_launch_agent(root: Path, scope: str) -> dict[str, Any]:
    path = launch_agent_path(root, scope)
    uid = os.getuid()
    result = subprocess.run(["launchctl", "bootout", f"gui/{uid}", str(path)], check=False, capture_output=True, text=True)
    path.unlink(missing_ok=True)
    return {"status": "uninstalled", "plist": str(path), "launchctl_returncode": result.returncode}


def adapter_command(root: Path, scope: str, cleanup_tool: Path, *, auto_keep: bool = False) -> list[str]:
    command = [sys.executable, str(cleanup_tool), "--sync", "--execute"]
    if auto_keep:
        command.append("--auto-keep")
    if scope and scope != ".":
        command.extend(["--scope", scope])
    return command


def index_command(root: Path) -> list[str]:
    return [
        sys.executable,
        str(SECOND_BRAIN_ROUTINE),
        "--vault",
        str(root),
        "--out",
        str(workspace(root) / "second-brain-asset-index"),
        "--source-mode",
        "asset-manifest",
        "--json",
        "--log", str(workspace(root) / "second-brain-routine.log"),
        "--lock", str(workspace(root) / "second-brain-routine.lock"),
        "--asset-index-registry", str(DEFAULT_INDEX_REGISTRY),
    ]


def run_automatic_sync(
    root: Path,
    scope: str,
    cleanup_tool: Path,
    debounce_seconds: int = DEFAULT_DEBOUNCE_SECONDS,
    heartbeat_seconds: int = DEFAULT_HEARTBEAT_SECONDS,
    *,
    auto_keep: bool = False,
) -> dict[str, Any]:
    root = root.resolve()
    scope = validate_workspace(root, scope)
    cleanup_tool = cleanup_tool.resolve()
    if not cleanup_tool.exists():
        raise FileNotFoundError(f"cleanup adapter not found: {cleanup_tool}")
    with sync_lock(root) as acquired:
        if not acquired:
            return {"status": "locked", "state_path": str(state_path(root))}
        state = load_state(root)
        state["last_started_at"] = utc_now()
        atomic_json(state_path(root), state)
        if debounce_seconds:
            time.sleep(debounce_seconds)
        command = adapter_command(root, scope, cleanup_tool, auto_keep=auto_keep)
        result = subprocess.run(command, cwd=root, check=False, text=True, capture_output=True)
        payload = command_json(result.stdout)
        state = load_state(root)
        state["last_runner_at"] = utc_now()
        state["last_command"] = command
        state["last_command_returncode"] = result.returncode
        if result.returncode != 0 or not payload:
            error = result.stderr.strip() or result.stdout.strip() or "sync adapter failed without JSON output"
            state["last_failure_at"] = utc_now()
            state["last_runner_error"] = error
            atomic_json(state_path(root), state)
            notify(
                "Agent Asset: Sync failed / 同步失败",
                f"Sync failed; see / 同步失败；查看 {workspace(root) / 'agent-asset-sync-launchd.stderr.log'}",
            )
            return {"status": "failed", "error": error, "adapter": payload}
        state["last_sync"] = payload
        state["last_heartbeat_at"] = utc_now()
        if int(payload.get("failed", 0) or 0):
            state["last_failure_at"] = utc_now()
            atomic_json(state_path(root), state)
            notify(
                "Agent Asset: Sync failed / 同步失败",
                f"{payload.get('failed')} assets failed; log: {payload.get('log_path', 'state file')} / {payload.get('failed')} 个资产失败；日志：{payload.get('log_path', 'state file')}",
            )
            return {"status": "failed", "adapter": payload}
        state["last_success_at"] = utc_now()
        changes = sum(int(payload.get(key, 0) or 0) for key in ("added", "modified", "removed", "moved"))
        index_result: dict[str, Any] | None = None
        if auto_keep and payload.get("index_ready") is True:
            audit_command = [sys.executable, str(cleanup_tool), "--audit-agent-assets"]
            if scope != ".":
                audit_command.extend(["--scope", scope])
            audit_result = subprocess.run(audit_command, cwd=root, check=False, text=True, capture_output=True)
            audit = command_json(audit_result.stdout)
            summary = audit.get("summary", {})
            blockers = ("candidate", "review", "missing_source", "missing_semantic", "final_pii", "delete_failed")
            ready = (audit_result.returncode == 0 and isinstance(summary, dict)
                     and summary.get("ready_for_scope_index") is True
                     and all(summary.get(key, 0) == 0 for key in blockers))
            scope_error = index_scope_error(root, scope)
            if not ready or scope_error:
                state["last_index_blocked_at"] = utc_now()
                state["last_index_blocked_reason"] = scope_error or "fresh scope audit is not index-ready / 最新范围审计尚未允许索引"
                atomic_json(state_path(root), state)
                notify("Agent Asset sync needs review / Agent Asset 同步需要审阅", "New content has not passed scope review; retaining the prior index / 新内容尚未通过范围审核，保留原索引。")
                return {"status": "attention", "adapter": payload, "index": None,
                        "reason": state["last_index_blocked_reason"]}
            result = subprocess.run(index_command(root), cwd=root, check=False, text=True, capture_output=True)
            index_result = command_json(result.stdout)
            if result.returncode != 0 or not index_result:
                error = result.stderr.strip() or result.stdout.strip() or "SecondBrain indexing failed"
                state["last_failure_at"] = utc_now()
                state["last_runner_error"] = error
                atomic_json(state_path(root), state)
                notify(
                    "Agent Asset index failed / Agent Asset 索引失败",
                    f"Sync completed but indexing failed; see {workspace(root) / 'agent-asset-sync-launchd.stderr.log'} / 同步已完成，但索引失败；查看 {workspace(root) / 'agent-asset-sync-launchd.stderr.log'}",
                )
                return {"status": "failed", "adapter": payload, "index": index_result, "error": error}
            state["last_indexed_at"] = utc_now()
            state["last_index_summary"] = index_result.get("summary", {})
        atomic_json(state_path(root), state)
        if changes:
            message = (
                f"Added / 新增: {payload.get('added', 0)}; modified / 修改: {payload.get('modified', 0)}; "
                f"removed / 删除: {payload.get('removed', 0)}; moved / 移动: {payload.get('moved', 0)}"
            )
            if index_result:
                indexed = index_result.get("summary", {}).get("indexed_documents", 0)
                message += f"; indexed {indexed} documents / 索引 {indexed} 条"
            notify("Agent Asset sync completed / Agent Asset 同步完成", message)
        health = status_for_state(root, heartbeat_seconds)
        if health["status"] == "attention":
            notify("Agent Asset sync needs attention / Agent Asset 同步需要关注", ", ".join(health["problems"]))
        return {"status": "ok", "adapter": payload, "index": index_result, "health": health}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--scope", default=".")
    parser.add_argument("--cleanup-tool", type=Path)
    parser.add_argument("--auto-keep", action="store_true", help="Explicitly allow non-PII changes in the reviewed scope to become final and index after a fresh audit / 显式允许已审阅范围内的非个人隐私变更成为最终资产，并在重新审计后索引。")
    parser.add_argument("--run", action="store_true", help="Run one debounced automatic sync / 运行一次带 debounce 的自动同步。")
    parser.add_argument("--install", action="store_true", help="Install the per-directory macOS LaunchAgent / 安装目录级 macOS LaunchAgent。")
    parser.add_argument("--uninstall", action="store_true", help="Unload and remove the per-directory macOS LaunchAgent / 卸载并删除目录级 macOS LaunchAgent。")
    parser.add_argument("--status", action="store_true", help="Show state, pending changes, failures, and heartbeat status / 显示 state、pending changes、failures 与 heartbeat status。")
    parser.add_argument("--debounce-seconds", type=int, default=DEFAULT_DEBOUNCE_SECONDS)
    parser.add_argument("--heartbeat-seconds", type=int, default=DEFAULT_HEARTBEAT_SECONDS)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    args.root = args.root.expanduser().resolve()
    try:
        args.scope = validate_workspace(args.root, args.scope)
    except (ValueError, OSError, RuntimeError) as exc:
        parser.error(f"scope or state path escapes workspace / 范围或状态路径越出工作区: {exc}")
    args.cleanup_tool = (args.cleanup_tool or DEFAULT_MIXED_FOLDER_ADAPTER).expanduser().resolve()
    return args


def self_test() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        tool = root / "tools" / "cleanup_convert.py"
        tool.parent.mkdir(parents=True)
        tool.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
        payload = launch_agent_payload(root, ".", tool, 0)
        assert payload["StartInterval"] == DEFAULT_INTERVAL_SECONDS
        assert str(root / "Archived") in payload["WatchPaths"]
        assert "--run" in payload["ProgramArguments"]
        atomic_json(state_path(root), {"last_success_at": utc_now(), "last_heartbeat_at": utc_now(), "last_sync": {"pending_review": 0, "failed": 0}})
        assert status_for_state(root)["status"] == "ok"


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.self_test:
        self_test()
        print("auto_sync self-test passed / auto_sync 自检通过")
        return 0
    actions = sum(bool(value) for value in (args.run, args.install, args.uninstall, args.status))
    if actions != 1:
        raise SystemExit("select exactly one of --run, --install, --uninstall, or --status / 必须且只能选择 --run、--install、--uninstall 或 --status 之一")
    if args.install:
        result = install_launch_agent(args.root, args.scope, args.cleanup_tool, args.debounce_seconds, auto_keep=args.auto_keep)
    elif args.uninstall:
        result = uninstall_launch_agent(args.root, args.scope)
    elif args.status:
        result = status_for_state(args.root, args.heartbeat_seconds)
    else:
        result = run_automatic_sync(
            args.root,
            args.scope,
            args.cleanup_tool,
            args.debounce_seconds,
            args.heartbeat_seconds,
            auto_keep=args.auto_keep,
        )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") in {"ok", "installed", "uninstalled", "baseline_missing", "attention", "locked"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
