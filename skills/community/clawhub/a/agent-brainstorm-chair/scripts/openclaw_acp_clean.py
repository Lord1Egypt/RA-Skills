#!/usr/bin/env python3
"""Run `openclaw acp` while filtering non-JSON stdout noise.

Generic version — uses env var or PATH to discover openclaw binary.
"""

from __future__ import annotations

import argparse
from collections import deque
import json
import os
import shutil
import signal
import subprocess
import sys
import threading
from pathlib import Path
from typing import Iterable


def _resolve_openclaw_bin() -> Path:
    env = os.environ.get("OPENCLAW_BIN", "").strip()
    if env:
        return Path(env)
    found = shutil.which("openclaw")
    if found:
        return Path(found)
    for candidate in (
        Path("/opt/homebrew/bin/openclaw"),
        Path("/usr/local/bin/openclaw"),
        Path.home() / ".local/bin/openclaw",
    ):
        if candidate.exists():
            return candidate
    return Path("openclaw")


OPENCLAW_BIN = _resolve_openclaw_bin()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run `openclaw acp` while filtering non-JSON stdout noise.",
    )
    parser.add_argument("--session", dest="session")
    parser.add_argument("--session-label", dest="session_label")
    parser.add_argument("--url")
    parser.add_argument("--token")
    parser.add_argument("--token-file", dest="token_file")
    parser.add_argument("--password")
    parser.add_argument("--password-file", dest="password_file")
    parser.add_argument("--require-existing", action="store_true")
    parser.add_argument("--reset-session", action="store_true")
    parser.add_argument("--no-prefix-cwd", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    return parser


def iter_args(args: argparse.Namespace) -> Iterable[str]:
    if args.session:
        yield "--session"
        yield args.session
    if args.session_label:
        yield "--session-label"
        yield args.session_label
    if args.url:
        yield "--url"
        yield args.url
    if args.token:
        yield "--token"
        yield args.token
    if args.token_file:
        yield "--token-file"
        yield args.token_file
    if args.password:
        yield "--password"
        yield args.password
    if args.password_file:
        yield "--password-file"
        yield args.password_file
    if args.require_existing:
        yield "--require-existing"
    if args.reset_session:
        yield "--reset-session"
    if args.no_prefix_cwd:
        yield "--no-prefix-cwd"
    if args.verbose:
        yield "--verbose"


def looks_like_jsonrpc(line: str) -> bool:
    try:
        payload = json.loads(line)
    except json.JSONDecodeError:
        return False
    if not isinstance(payload, dict):
        return False
    if payload.get("jsonrpc") != "2.0":
        return False
    return any(key in payload for key in ("id", "method", "result", "error", "params"))


def stderr_write(text: str) -> None:
    try:
        sys.stderr.write(text)
        sys.stderr.flush()
    except BrokenPipeError:
        pass


def stdout_write(text: str) -> None:
    try:
        sys.stdout.write(text)
        sys.stdout.flush()
    except BrokenPipeError:
        pass


def main() -> int:
    args = build_parser().parse_args()
    openclaw_bin = str(OPENCLAW_BIN if OPENCLAW_BIN.exists() else "openclaw")
    cmd = ["script", "-q", "/dev/null", openclaw_bin, "acp", *iter_args(args)]

    env = os.environ.copy()
    env["PATH"] = f"{OPENCLAW_BIN.parent}:{env.get('PATH', '')}".rstrip(":")
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        env=env,
    )
    echoed_inputs: deque[str] = deque()
    echoed_inputs_lock = threading.Lock()

    def forward_signal(signum: int, _frame: object) -> None:
        try:
            proc.send_signal(signum)
        except Exception:
            pass

    signal.signal(signal.SIGINT, forward_signal)
    signal.signal(signal.SIGTERM, forward_signal)

    def should_suppress_echo(line: str) -> bool:
        normalized = line.rstrip("\r\n")
        if not normalized:
            return False
        with echoed_inputs_lock:
            if echoed_inputs and echoed_inputs[0] == normalized:
                echoed_inputs.popleft()
                return True
        return False

    def pump_stdin() -> None:
        assert proc.stdin is not None
        try:
            for line in sys.stdin:
                normalized = line.rstrip("\r\n")
                if normalized:
                    with echoed_inputs_lock:
                        echoed_inputs.append(normalized)
                proc.stdin.write(line)
                proc.stdin.flush()
        except BrokenPipeError:
            pass
        finally:
            try:
                proc.stdin.close()
            except Exception:
                pass

    def pump_stdout() -> None:
        assert proc.stdout is not None
        for line in proc.stdout:
            if should_suppress_echo(line):
                continue
            if looks_like_jsonrpc(line):
                stdout_write(line)
            else:
                stderr_write(line)

    def pump_stderr() -> None:
        assert proc.stderr is not None
        for line in proc.stderr:
            stderr_write(line)

    threads = [
        threading.Thread(target=pump_stdin, daemon=True),
        threading.Thread(target=pump_stdout, daemon=True),
        threading.Thread(target=pump_stderr, daemon=True),
    ]
    for thread in threads:
        thread.start()

    try:
        return proc.wait()
    finally:
        for thread in threads:
            thread.join(timeout=0.2)


if __name__ == "__main__":
    raise SystemExit(main())
