#!/usr/bin/env python3
"""Wait for Codex Desktop to stop, then run and verify a target repair.

This wrapper is deliberately separate from ``repair.py``.  The repair logic
stays deterministic and backup-first; this module owns the process lifecycle
and refuses to write when Codex reappears or the rollout changes while waiting.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable, Sequence, TextIO

import repair


class DesktopRestartedError(RuntimeError):
    """Codex Desktop appeared again before it was safe to write."""


class DesktopNotDetectedError(RuntimeError):
    """The automatic mode could not confirm that Codex was running first."""


class DesktopWaitTimeoutError(TimeoutError):
    """Codex Desktop did not stay stopped within the configured timeout."""


class RolloutChangedError(RuntimeError):
    """The target rollout changed while waiting, so the diagnosis is stale."""


class RepairApplyError(RuntimeError):
    """The underlying repair command did not produce a verified result."""


@dataclass(frozen=True)
class ProcessInfo:
    pid: int
    command: str


STATUS_LABELS = {
    "diagnosed": ("Diagnosed", "已诊断"),
    "waiting": ("Waiting", "等待中"),
    "stopped": ("Stopped", "已停止"),
    "applying": ("Applying", "修复中"),
    "verified": ("Verified", "已验证"),
    "failed": ("Failed", "失败"),
}

STATUS_ACTIONS = {
    "verified": "Reopen Codex / 可以重新打开 Codex",
    "failed": "Keep Codex closed / 保持 Codex 关闭",
}

DEFAULT_WAIT_REMINDER_SECONDS = (60.0, 180.0, 240.0)


def _is_desktop_command(command: str) -> bool:
    normalized = command.strip().lower()
    if not normalized:
        return False
    # macOS may leave orphaned Chromium crashpad handlers alive after the
    # desktop app exits. They do not hold the Codex session open and must not
    # block the safe, process-free window.
    if "browser_crashpad_handler" in normalized:
        return False
    basename = Path(normalized).name
    if basename in {"chatgpt.exe", "codex.exe"}:
        return True
    return any(
        suffix in normalized
        for suffix in (
            "/chatgpt.app/contents/macos/chatgpt",
            "/codex.app/contents/macos/codex",
            "/chatgpt helper.app/contents/macos/chatgpt helper",
            "/chatgpt.app/contents/resources/codex",
            "/codex.app/contents/resources/codex",
            "/chatgpt.app/contents/frameworks/codex framework.framework/",
            "/codex.app/contents/frameworks/codex framework.framework/",
        )
    )


def parse_process_table(text: str) -> list[ProcessInfo]:
    """Parse ``ps -axo pid=,comm=`` output without matching the shell command."""
    processes: list[ProcessInfo] = []
    for line in text.splitlines():
        parts = line.strip().split(maxsplit=1)
        if len(parts) != 2:
            continue
        try:
            pid = int(parts[0])
        except ValueError:
            continue
        command = parts[1].strip()
        if _is_desktop_command(command):
            processes.append(ProcessInfo(pid, command))
    return processes


def list_codex_desktop_processes() -> list[ProcessInfo]:
    """Return visible Codex Desktop/main-helper processes.

    Process inspection is a safety boundary.  If the operating-system query
    fails, the exception is propagated and the caller must not apply a repair.
    """
    if os.name == "nt":
        completed = subprocess.run(
            ["tasklist", "/fo", "csv", "/nh"],
            check=True,
            capture_output=True,
            text=True,
        )
        processes: list[ProcessInfo] = []
        for row in csv.reader(completed.stdout.splitlines()):
            if len(row) < 2 or not _is_desktop_command(row[0]):
                continue
            try:
                processes.append(ProcessInfo(int(row[1]), row[0]))
            except ValueError:
                continue
        return processes

    completed = subprocess.run(
        ["ps", "-axo", "pid=,comm="],
        check=True,
        capture_output=True,
        text=True,
    )
    return parse_process_table(completed.stdout)


def _notify(notify: Callable[[str, str], None] | None, status: str, message: str) -> None:
    if notify is not None:
        notify(status, message)


def wait_for_desktop_exit(
    process_reader: Callable[[], Sequence[ProcessInfo]],
    *,
    timeout: float = 300.0,
    stable_seconds: float = 5.0,
    poll_seconds: float = 1.0,
    reminder_seconds: Sequence[float] | None = None,
    allow_already_stopped: bool = False,
    sleep: Callable[[float], None] = time.sleep,
    monotonic: Callable[[], float] = time.monotonic,
    notify: Callable[[str, str], None] | None = None,
) -> None:
    """Wait for a stable process-free window, failing closed on a restart.

    ``allow_already_stopped`` is used only by the explicit repair-job launcher.
    It makes the workflow safe when the user quits Codex before the worker's
    first process sample; the worker still requires a stable process-free
    window before writing anything.
    """
    if timeout <= 0 or stable_seconds < 0 or poll_seconds <= 0:
        raise ValueError("timeout and poll_seconds must be positive; stable_seconds cannot be negative")

    configured_reminders = DEFAULT_WAIT_REMINDER_SECONDS if reminder_seconds is None else reminder_seconds
    try:
        reminder_points = sorted(
            {
                float(point)
                for point in configured_reminders
                if 0 < float(point) < timeout
            }
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("reminder_seconds must contain positive numbers") from exc

    started_at = monotonic()
    absent_since: float | None = None
    first_sample = True
    initial_notice_sent = False
    next_reminder = 0

    def announce_waiting(prefix_zh: str, prefix_en: str) -> None:
        nonlocal initial_notice_sent, next_reminder
        elapsed = max(0.0, monotonic() - started_at)
        if not initial_notice_sent:
            _notify(
                notify,
                "waiting",
                f"{prefix_zh} 最长等待 {timeout:g} 秒，已等待约 {elapsed:g} 秒。请使用 Command+Q 完全退出 Codex。 / "
                f"{prefix_en} Maximum wait: {timeout:g}s; waited about {elapsed:g}s. Please fully quit Codex with Command+Q.",
            )
            initial_notice_sent = True
        while next_reminder < len(reminder_points) and elapsed >= reminder_points[next_reminder]:
            point = reminder_points[next_reminder]
            remaining = max(0.0, timeout - point)
            _notify(
                notify,
                "waiting",
                f"等待提醒：已等待约 {point:g} 秒，距离超时约 {remaining:g} 秒。请确认已使用 Command+Q 完全退出 Codex。 / "
                f"Wait reminder: about {point:g}s elapsed, about {remaining:g}s until timeout. Confirm that Codex was fully quit with Command+Q.",
            )
            next_reminder += 1

    while True:
        processes = list(process_reader())
        now = monotonic()
        if processes:
            if absent_since is not None:
                raise DesktopRestartedError(
                    "Codex Desktop reappeared during the shutdown stability window; no files were changed."
                )
            announce_waiting(
                "Codex 仍在运行，正在等待完全退出。",
                "Codex is still running; waiting for full exit.",
            )
        else:
            if first_sample:
                if not allow_already_stopped:
                    raise DesktopNotDetectedError(
                        "Could not confirm that Codex Desktop was running. "
                        "Start automatic mode while Codex is open, or use the manual repair command."
                    )
                absent_since = now
                announce_waiting(
                    "未检测到 Codex，正在确认它已经完全退出。",
                    "Codex is not detected; confirming full exit.",
                )
            if absent_since is None:
                absent_since = now
                announce_waiting(
                    "已检测不到 Codex，正在确认安全窗口。",
                    "Codex is absent; confirming a safe window.",
                )
            elif now - absent_since >= stable_seconds:
                _notify(
                    notify,
                    "stopped",
                    f"Codex 已完全退出，安全检查已通过（{stable_seconds:g} 秒）。 / Codex fully exited; safety check passed ({stable_seconds:g}s).",
                )
                return
        first_sample = False

        if now - started_at >= timeout:
            raise DesktopWaitTimeoutError(
                f"等待 Codex 完全退出已达到 {timeout:g} 秒，但进程仍未稳定停止；未修改文件。 / "
                f"Codex Desktop did not stay stopped within {timeout:g}s; no files were changed."
            )
        sleep(poll_seconds)


class StatusReporter:
    """Write human-readable progress and an atomically replaced JSON status file."""

    def __init__(self, session_id: str, path: Path | None = None, stream: TextIO | None = None):
        self.session_id = session_id
        self.path = path
        self.stream = stream if stream is not None else sys.stdout

    def update(self, status: str, message: str, **fields: object) -> dict[str, object]:
        status_en, status_zh = STATUS_LABELS.get(status, (status, status))
        payload: dict[str, object] = {
            "session_id": self.session_id,
            "status": status,
            "status_label": f"{status_en} / {status_zh}",
            "message": message,
            "can_reopen": status == "verified",
            "next_action": STATUS_ACTIONS.get(
                status,
                "Keep Codex closed and wait / 保持 Codex 关闭并等待",
            ),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        payload.update(fields)
        if self.path is not None:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            handle_path: str | None = None
            try:
                with tempfile.NamedTemporaryFile(
                    "w",
                    encoding="utf-8",
                    dir=self.path.parent,
                    prefix=f".{self.path.name}.",
                    suffix=".tmp",
                    delete=False,
                ) as handle:
                    json.dump(payload, handle, ensure_ascii=False, indent=2)
                    handle.write("\n")
                    handle_path = handle.name
                os.replace(handle_path, self.path)
            finally:
                if handle_path is not None and Path(handle_path).exists():
                    Path(handle_path).unlink()
        print(f"[{status_en} / {status_zh}] {message}", file=self.stream, flush=True)
        return payload


def rollout_fingerprint(path: Path) -> dict[str, object]:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    stat = path.stat()
    return {"size": stat.st_size, "mtime_ns": stat.st_mtime_ns, "sha256": digest}


def default_status_path(session_id: str) -> Path:
    """Return the predictable status path shown to beginner users."""
    return Path(tempfile.gettempdir()) / f"codex-session-repair-{session_id}.json"


def _backup_paths(rollout: Path) -> set[Path]:
    return set(rollout.parent.glob(f"{rollout.name}.bak-session-repair-*"))


def _build_repair_argv(
    session_id: str,
    codex_home: Path,
    remove_reasoning: str,
    provider: str | None,
    fix_provider: bool,
    model: str | None,
    fix_model: bool,
    fix_model_turn: bool,
    disable_remote_compaction: bool,
) -> list[str]:
    argv = [
        "--session-id",
        session_id,
        "--codex-home",
        str(codex_home),
        "--remove-reasoning",
        remove_reasoning,
        "--apply",
    ]
    if provider:
        argv.extend(["--provider", provider])
    if fix_provider:
        argv.append("--fix-provider")
    if model:
        argv.extend(["--model", model])
    if fix_model:
        argv.append("--fix-model")
    if fix_model_turn:
        argv.append("--fix-model-turn")
    if disable_remote_compaction:
        argv.append("--disable-remote-compaction")
    return argv


def _verify_post_report(
    report: dict[str, object],
    remove_reasoning: str,
    fix_model: bool = False,
    model: str | None = None,
) -> None:
    if report["json_parse_errors"]:
        raise RepairApplyError("post-repair verification found malformed JSONL")
    if remove_reasoning == "all" and report["reasoning_item_count"] != 0:
        raise RepairApplyError(
            f"post-repair verification found {report['reasoning_item_count']} local reasoning records"
        )
    if remove_reasoning == "stale" and report["stale_ids_present_as_reasoning"]:
        raise RepairApplyError("post-repair verification found stale IDs still present as local reasoning")
    if fix_model:
        if not model:
            raise RepairApplyError("model repair verification requires a target model")
        root_thread = report.get("root_thread")
        if not isinstance(root_thread, dict) or root_thread.get("model") != model:
            raise RepairApplyError("post-repair verification found the target DB model was not updated")
        structured_models = report.get("structured_model_values") or []
        if any(value != model for value in structured_models):
            raise RepairApplyError("post-repair verification found an old structured rollout model")


def run_wait_and_repair(
    *,
    session_id: str,
    codex_home: Path,
    remove_reasoning: str = "all",
    provider: str | None = None,
    fix_provider: bool = False,
    model: str | None = None,
    fix_model: bool = False,
    fix_model_turn: bool = False,
    disable_remote_compaction: bool = False,
    process_reader: Callable[[], Sequence[ProcessInfo]] = list_codex_desktop_processes,
    status_file: Path | None = None,
    timeout: float = 300.0,
    stable_seconds: float = 5.0,
    poll_seconds: float = 1.0,
    reminder_seconds: Sequence[float] | None = None,
    allow_already_stopped: bool = False,
    sleep: Callable[[float], None] = time.sleep,
    monotonic: Callable[[], float] = time.monotonic,
    apply_runner: Callable[[list[str]], int] = repair.main,
    stream: TextIO | None = None,
) -> dict[str, object]:
    """Diagnose, wait safely, apply via ``repair.py``, and verify the result."""
    reporter = StatusReporter(session_id, status_file or default_status_path(session_id), stream)
    try:
        report = repair.inspect_session(codex_home, session_id)
        if report["json_parse_errors"]:
            raise ValueError("refusing to wait/apply: JSONL has parse errors")
        rollout = Path(report["rollout_path"])
        before_fingerprint = rollout_fingerprint(rollout)
        before_backups = _backup_paths(rollout)
        reporter.update(
            "diagnosed",
            f"已完成只读诊断。修复任务已启动，最多等待 {timeout:g} 秒。请完全退出 Codex（macOS 使用 Command+Q）；修复尚未开始。 / "
            f"Read-only diagnosis complete. Repair job started; the worker may wait up to {timeout:g}s. Fully quit Codex (use Command+Q on macOS); repair has not started yet.",
            line_count=report["line_count"],
            reasoning_item_count=report["reasoning_item_count"],
            wait_timeout_seconds=timeout,
            wait_phase="waiting_for_desktop_exit",
            conversation_notice=f"修复任务已启动，最多等待 {timeout:g} 秒；请完全退出 Codex。 / Repair started; maximum wait is {timeout:g}s; fully quit Codex.",
        )

        wait_for_desktop_exit(
            process_reader,
            timeout=timeout,
            stable_seconds=stable_seconds,
            poll_seconds=poll_seconds,
            reminder_seconds=reminder_seconds,
            allow_already_stopped=allow_already_stopped,
            sleep=sleep,
            monotonic=monotonic,
            notify=lambda status, message: reporter.update(
                status,
                message,
                wait_timeout_seconds=timeout,
                wait_phase="waiting_for_desktop_exit",
            ),
        )
        if list(process_reader()):
            raise DesktopRestartedError("Codex Desktop reappeared before apply; no files were changed.")

        after_wait_fingerprint = rollout_fingerprint(rollout)
        if after_wait_fingerprint != before_fingerprint:
            raise RolloutChangedError(
                "The target rollout changed while waiting; diagnosis is stale and no files were changed."
            )

        reporter.update(
            "applying",
            "Codex 已完全退出，正在备份并修复目标会话。请保持 Codex 关闭。 / Codex fully exited; backing up and repairing the target session. Keep Codex closed.",
            wait_timeout_seconds=timeout,
            wait_phase="applying",
        )
        argv = _build_repair_argv(
            session_id,
            codex_home,
            remove_reasoning,
            provider,
            fix_provider,
            model,
            fix_model,
            fix_model_turn,
            disable_remote_compaction,
        )
        exit_code = apply_runner(argv)
        if exit_code != 0:
            raise RepairApplyError(f"repair.py exited with status {exit_code}")

        new_backups = _backup_paths(rollout) - before_backups
        if not new_backups:
            raise RepairApplyError("repair.py returned success but did not create a session backup")
        post_report = repair.inspect_session(codex_home, session_id)
        _verify_post_report(post_report, remove_reasoning, fix_model, model)
        backup = str(sorted(new_backups)[-1])
        reporter.update(
            "verified",
            "修复完成并验证通过，现在可以重新打开 Codex。 / Repair complete and verified; you can reopen Codex now.",
            backup=backup,
            line_count=post_report["line_count"],
            reasoning_item_count=post_report["reasoning_item_count"],
            historical_remote_stale_ids=post_report["stale_remote_item_ids"],
            wait_timeout_seconds=timeout,
            wait_phase="verified",
        )
        return {"status": "verified", "backup": backup, "post_report": post_report}
    except Exception as exc:
        failure_fields: dict[str, object] = {
            "error_type": type(exc).__name__,
            "wait_timeout_seconds": timeout,
        }
        if isinstance(exc, DesktopWaitTimeoutError):
            failure_fields.update(
                {
                    "wait_timed_out": True,
                    "conversation_notice": f"等待超时：Codex 完全退出超过 {timeout:g} 秒，未修改文件。请检查是否只关闭了窗口；如需重试，请使用 Command+Q 完全退出。 / "
                    f"Codex did not fully exit within {timeout:g}s; no files were changed. Check whether only the window was closed; use Command+Q before retrying.",
                }
            )
        reporter.update(
            "failed",
            f"修复未完成，请保持 Codex 关闭，暂时不要重新打开。 / Repair did not complete; keep Codex closed and do not reopen it yet. 原因 / Reason: {exc}",
            **failure_fields,
        )
        raise


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session-id", required=True, help="Target Codex session UUID")
    parser.add_argument("--codex-home", required=True, help="Codex home directory")
    parser.add_argument(
        "--remove-reasoning",
        choices=("none", "stale", "all"),
        default="all",
        help="Remove exact stale reasoning IDs, or all internal reasoning records",
    )
    parser.add_argument("--provider", help="Current provider when --fix-provider is used")
    parser.add_argument("--fix-provider", action="store_true")
    parser.add_argument("--model", help="Target model when --fix-model is used")
    parser.add_argument("--fix-model", action="store_true")
    parser.add_argument("--fix-model-turn", action="store_true")
    parser.add_argument("--disable-remote-compaction", action="store_true")
    parser.add_argument("--status-file", type=Path, help="Atomically updated JSON status file")
    parser.add_argument(
        "--allow-already-stopped",
        action="store_true",
        help="Allow the explicit repair job to start after Codex was already closed",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=300.0,
        help="Maximum Codex shutdown wait in seconds; emits bilingual reminders at about 60/180/240s by default",
    )
    parser.add_argument("--stable-seconds", type=float, default=5.0)
    parser.add_argument("--poll-seconds", type=float, default=1.0)
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        run_wait_and_repair(
            session_id=args.session_id,
            codex_home=Path(args.codex_home).expanduser().resolve(),
            remove_reasoning=args.remove_reasoning,
            provider=args.provider,
            fix_provider=args.fix_provider,
            model=args.model,
            fix_model=args.fix_model,
            fix_model_turn=args.fix_model_turn,
            disable_remote_compaction=args.disable_remote_compaction,
            status_file=args.status_file.expanduser().resolve() if args.status_file else None,
            timeout=args.timeout,
            stable_seconds=args.stable_seconds,
            poll_seconds=args.poll_seconds,
            allow_already_stopped=args.allow_already_stopped,
        )
        return 0
    except (OSError, ValueError, RuntimeError, TimeoutError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
