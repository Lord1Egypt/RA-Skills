#!/usr/bin/env python3
"""Start a detached, beginner-friendly Codex session repair job.

This is the user-facing entry point. It opens a visible Terminal window on
macOS, runs the process-aware worker there, and leaves the final status visible
until the user presses Enter; the dedicated Terminal window is then closed.
The worker accepts both "Codex is still open" and "the user already quit
Codex" because starting this command is itself the explicit repair approval.
"""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterable

import wait_and_repair


def default_status_path(session_id: str) -> Path:
    return wait_and_repair.default_status_path(session_id)


def build_worker_argv(
    *,
    skill_dir: Path,
    session_id: str,
    codex_home: Path,
    remove_reasoning: str,
    status_file: Path,
    timeout: float,
    stable_seconds: float,
    poll_seconds: float,
    provider: str | None = None,
    fix_provider: bool = False,
    model: str | None = None,
    fix_model: bool = False,
    fix_model_turn: bool = False,
    disable_remote_compaction: bool = False,
) -> list[str]:
    argv = [
        sys.executable,
        str(skill_dir / "wait_and_repair.py"),
        "--session-id",
        session_id,
        "--codex-home",
        str(codex_home),
        "--remove-reasoning",
        remove_reasoning,
        "--allow-already-stopped",
        "--status-file",
        str(status_file),
        "--timeout",
        str(timeout),
        "--stable-seconds",
        str(stable_seconds),
        "--poll-seconds",
        str(poll_seconds),
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


def _argument_value(argv: list[str], option: str, default: str) -> str:
    try:
        index = argv.index(option)
    except ValueError:
        return default
    if index + 1 >= len(argv):
        return default
    return str(argv[index + 1])


def build_conversation_notice(timeout: float) -> str:
    return f"修复任务已启动，最多等待 {timeout:g} 秒；请完全退出 Codex。 / Repair started; maximum wait is {timeout:g}s; fully quit Codex."


def _shell_literal(text: str) -> str:
    return "'" + text.replace("'", "'\"'\"'") + "'"


def _shell_print(text: str) -> str:
    return f"printf '%s\\n' {_shell_literal(text)}"


def terminal_tab_title(session_id: str) -> str:
    return f"Codex session repair {session_id}"


def build_terminal_title_command(session_id: str) -> str:
    title = _shell_literal(terminal_tab_title(session_id))
    return f"printf '\\033]0;%s\\007' {title}"


def build_terminal_close_applescript(session_id: str) -> str:
    marker = json.dumps(terminal_tab_title(session_id), ensure_ascii=False)
    return "\n".join(
        [
            'tell application "Terminal"',
            "repeat with targetWindow in windows",
            f"if (name of targetWindow) contains {marker} then",
            "if (count of tabs of targetWindow) is 1 then",
            "close targetWindow",
            "return",
            "end if",
            "end if",
            "end repeat",
            "end tell",
        ]
    )


def build_terminal_close_command(session_id: str) -> str:
    applescript = build_terminal_close_applescript(session_id)
    return f"/usr/bin/osascript -e {shlex.quote(applescript)} >/dev/null 2>&1"


def build_terminal_runner_script(argv: list[str], *, session_id: str, timeout: float) -> str:
    command = " ".join(shlex.quote(str(part)) for part in argv)
    lines = [
        "#!/bin/zsh",
        "set +e",
        "trap 'rm -f -- \"$0\"' EXIT",
        "clear",
        _shell_print(""),
        _shell_print("============================================================"),
        _shell_print("Codex 会话修复 / Codex session repair"),
        _shell_print("============================================================"),
        _shell_print(f"会话 / Session: {session_id}"),
        _shell_print(f"等待上限 / Wait limit: {timeout:g} 秒 / {timeout:g} seconds"),
        _shell_print("操作 / Action: 请使用 Command+Q 完全退出 Codex"),
        _shell_print("提示 / Note: 状态会双语显示；完成前不要重新打开 Codex。"),
        _shell_print("------------------------------------------------------------"),
        _shell_print(""),
        command,
        "rc=$?",
        _shell_print(""),
        "if [ \"$rc\" -eq 0 ]; then",
        _shell_print("Verified / 已验证：修复完成，现在可以重新打开 Codex。"),
        "else",
        _shell_print("Failed / 失败：修复未完成，请保持 Codex 关闭。"),
        "fi",
        _shell_print(""),
        _shell_print("按回车关闭此窗口 / Press Enter to close"),
        "read -r",
        "exit \"$rc\"",
    ]
    return "\n".join(lines) + "\n"


def build_terminal_command(
    argv: list[str], *, workdir: Path, runner_path: Path | None = None
) -> str:
    session_id = _argument_value(argv, "--session-id", "unknown")
    close_command = build_terminal_close_command(session_id)
    if runner_path is not None:
        return (
            f"{build_terminal_title_command(session_id)}; "
            f"cd {shlex.quote(str(workdir))} && /bin/zsh {shlex.quote(str(runner_path))}; "
            f"rc=$?; {close_command}; exit \"$rc\""
        )

    command = " ".join(shlex.quote(str(part)) for part in argv)
    timeout = _argument_value(argv, "--timeout", "300")
    wait_message = shlex.quote(
        f"Wait limit / 等待上限: up to {timeout} seconds / 最多 {timeout} 秒；请完全退出 Codex。"
    )
    return (
        f"{build_terminal_title_command(session_id)}; "
        f"cd {shlex.quote(str(workdir))} && "
        "echo 'Codex session repair started / Codex 会话修复已启动；请保持此窗口打开。' && "
        f"echo {wait_message} && "
        f"{command}; rc=$?; echo; "
        "if [ \"$rc\" -eq 0 ]; then "
        "echo 'verified / 已验证：Repair complete; you can reopen Codex now / 修复完成，现在可以重新打开 Codex。'; "
        "else "
        "echo 'failed / 失败：Repair did not complete; keep Codex closed / 修复未完成，请不要重新打开 Codex。'; "
        f"fi; echo; echo '按回车关闭此窗口'; read -r; {close_command}; exit \"$rc\""
    )


def build_terminal_applescript(command: str, *, session_id: str | None = None) -> str:
    if session_id:
        command = f"{build_terminal_title_command(session_id)}; {command}"
    lines = [
        'tell application "Terminal"',
        "activate",
        f"set repairTab to «event coredosc» {json.dumps(command, ensure_ascii=False)}",
    ]
    if session_id:
        lines.extend(
            [
                "tell repairTab",
                f"set custom title to {json.dumps(terminal_tab_title(session_id), ensure_ascii=False)}",
                "set title displays custom title to true",
                "end tell",
            ]
        )
    lines.extend(
        [
            "tell front window",
            "set number of columns to 120",
            "set number of rows to 36",
            "end tell",
            "end tell",
        ]
    )
    return "\n".join(lines)


def write_terminal_runner(script: str, session_id: str) -> Path:
    handle = tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        prefix=f"codex-session-repair-{session_id}-",
        suffix=".zsh",
        delete=False,
    )
    try:
        handle.write(script)
        handle.flush()
    finally:
        handle.close()
    path = Path(handle.name)
    path.chmod(0o700)
    return path


def open_terminal(command: str, *, session_id: str | None = None) -> None:
    """Open macOS Terminal and run the worker command in a visible window."""
    if sys.platform != "darwin":
        raise RuntimeError("--open-terminal is currently supported on macOS only")
    applescript = build_terminal_applescript(command, session_id=session_id)
    subprocess.run(["osascript", "-e", applescript], check=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--codex-home", required=True)
    parser.add_argument("--remove-reasoning", choices=("none", "stale", "all"), default="none")
    parser.add_argument("--provider")
    parser.add_argument("--fix-provider", action="store_true")
    parser.add_argument("--model")
    parser.add_argument("--fix-model", action="store_true")
    parser.add_argument("--fix-model-turn", action="store_true")
    parser.add_argument("--disable-remote-compaction", action="store_true")
    parser.add_argument("--status-file", type=Path)
    parser.add_argument(
        "--timeout",
        type=float,
        default=300.0,
        help="Maximum Codex shutdown wait in seconds; Terminal reminds at about 60/180/240s by default",
    )
    parser.add_argument("--stable-seconds", type=float, default=5.0)
    parser.add_argument("--poll-seconds", type=float, default=1.0)
    terminal = parser.add_mutually_exclusive_group()
    terminal.add_argument("--open-terminal", dest="open_terminal", action="store_true")
    terminal.add_argument("--no-open-terminal", dest="open_terminal", action="store_false")
    parser.set_defaults(open_terminal=(sys.platform == "darwin"))
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    skill_dir = Path(__file__).resolve().parent
    status_file = (args.status_file or default_status_path(args.session_id)).expanduser().resolve()
    worker_argv = build_worker_argv(
        skill_dir=skill_dir,
        session_id=args.session_id,
        codex_home=Path(args.codex_home).expanduser().resolve(),
        remove_reasoning=args.remove_reasoning,
        status_file=status_file,
        timeout=args.timeout,
        stable_seconds=args.stable_seconds,
        poll_seconds=args.poll_seconds,
        provider=args.provider,
        fix_provider=args.fix_provider,
        model=args.model,
        fix_model=args.fix_model,
        fix_model_turn=args.fix_model_turn,
        disable_remote_compaction=args.disable_remote_compaction,
    )
    if args.open_terminal:
        runner_path = write_terminal_runner(
            build_terminal_runner_script(
                worker_argv,
                session_id=args.session_id,
                timeout=args.timeout,
            ),
            args.session_id,
        )
        try:
            open_terminal(
                build_terminal_command(worker_argv, workdir=skill_dir, runner_path=runner_path),
                session_id=args.session_id,
            )
        except Exception:
            runner_path.unlink(missing_ok=True)
            raise
        print(build_conversation_notice(args.timeout))
        print(f"已打开终端状态窗口：{status_file}；最长等待 {args.timeout:g} 秒 / wait limit {args.timeout:g}s")
        return 0
    return subprocess.run(worker_argv, cwd=skill_dir).returncode


if __name__ == "__main__":
    raise SystemExit(main())
