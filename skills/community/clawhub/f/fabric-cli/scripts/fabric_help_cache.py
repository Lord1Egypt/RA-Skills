#!/usr/bin/env python3
"""Capture read-only help output from the installed Fabric.so CLI.

Agents can run this before using commands whose options may have changed. The
script emits bounded, redacted JSON or Markdown. It never performs Fabric writes.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from typing import Iterable, Sequence

SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*[^\s,;]+"),
    re.compile(r"(?i)bearer\s+[a-z0-9._~+/=-]{12,}"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"),
]

DEFAULT_COMMANDS = ["search", "path", "create", "note", "link", "file", "save", "folder", "workspace", "ask", "task", "completion", "subscription"]


@dataclass
class HelpResult:
    command_name: str
    attempted_commands: list[list[str]]
    ok: bool
    returncode: int | None
    duration_ms: int
    output: str
    stderr: str


def redact(text: str) -> str:
    value = text or ""
    for pattern in SECRET_PATTERNS:
        value = pattern.sub("[REDACTED_SECRET]", value)
    return value


def truncate(text: str, limit: int) -> str:
    value = redact(text).replace("\r", "")
    if len(value) <= limit:
        return value
    return value[:limit] + f"\n...[truncated {len(value) - limit} chars]"


def run(cmd: Sequence[str], timeout: float) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(list(cmd), text=True, capture_output=True, timeout=timeout, check=False)
    except (subprocess.TimeoutExpired, OSError):
        return None


def capture_help(command_name: str, timeout: float, max_output: int) -> HelpResult:
    attempts: list[list[str]] = []
    started = time.monotonic()
    if command_name in {"", "root", "--help"}:
        candidates = [["fabric", "--help"]]
        label = "root"
    else:
        label = command_name
        candidates = [["fabric", "help", command_name], ["fabric", command_name, "--help"]]

    last_returncode: int | None = None
    last_stdout = ""
    last_stderr = ""
    for candidate in candidates:
        attempts.append(candidate)
        proc = run(candidate, timeout)
        if proc is None:
            last_returncode = None
            last_stderr = f"Command failed or timed out: {' '.join(candidate)}"
            continue
        last_returncode = proc.returncode
        last_stdout = proc.stdout
        last_stderr = proc.stderr
        if proc.returncode == 0 and (proc.stdout.strip() or proc.stderr.strip()):
            elapsed = int((time.monotonic() - started) * 1000)
            return HelpResult(label, attempts, True, proc.returncode, elapsed, truncate(proc.stdout or proc.stderr, max_output), truncate(proc.stderr, max_output))

    elapsed = int((time.monotonic() - started) * 1000)
    return HelpResult(label, attempts, False, last_returncode, elapsed, truncate(last_stdout, max_output), truncate(last_stderr, max_output))


def parse_commands(value: str | None) -> list[str]:
    if not value:
        return ["root", *DEFAULT_COMMANDS]
    result = [p.strip() for p in value.split(",") if p.strip()]
    return result or ["root", *DEFAULT_COMMANDS]


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture help output from the installed Fabric.so CLI.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--commands", help="Comma-separated command names, e.g. search,save,task. Omit for common commands.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    parser.add_argument("--timeout", type=float, default=10.0, help="Timeout per help command in seconds.")
    parser.add_argument("--max-output", type=int, default=6000, help="Maximum characters per captured help output.")
    parser.add_argument("--strict", action="store_true", help="Return non-zero if any requested help command fails.")
    return parser.parse_args(list(argv))


def main(argv: Iterable[str] = sys.argv[1:]) -> int:
    args = parse_args(argv)
    if not shutil.which("fabric"):
        payload = {"status": "not_installed", "message": "No `fabric` executable found on PATH."}
        print(json.dumps(payload, indent=2, sort_keys=True) if args.json else payload["message"])
        return 2 if args.strict else 0

    results = [capture_help(name, args.timeout, args.max_output) for name in parse_commands(args.commands)]
    if args.json:
        print(json.dumps({"status": "ok" if all(r.ok for r in results) else "partial", "results": [asdict(r) for r in results]}, indent=2, sort_keys=True))
    else:
        for result in results:
            print(f"## {result.command_name} ({'ok' if result.ok else 'failed'})\n")
            for cmd in result.attempted_commands:
                print(f"- `{' '.join(cmd)}`")
            if result.output:
                print("\n```text")
                print(result.output.rstrip())
                print("```\n")
    if args.strict and not all(r.ok for r in results):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
