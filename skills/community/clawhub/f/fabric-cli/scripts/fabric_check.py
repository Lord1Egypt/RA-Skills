#!/usr/bin/env python3
"""Read-only diagnostics for the Fabric.so CLI.

The script checks whether the Fabric.so CLI executable named `fabric` is on PATH,
optionally runs read-only account/workspace checks, and emits concise structured
output for agents. It never installs software, authenticates, logs out, changes
workspace, writes to Fabric, or deletes anything.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from typing import Iterable, Sequence

SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*[^\s,;]+"),
    re.compile(r"(?i)bearer\s+[a-z0-9._~+/=-]{12,}"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"\b[a-f0-9]{32,}\b", re.IGNORECASE),
]


@dataclass
class CommandResult:
    name: str
    command: list[str]
    ok: bool
    returncode: int | None
    duration_ms: int
    stdout_preview: str = ""
    stderr_preview: str = ""
    error: str = ""


@dataclass
class DiagnosticReport:
    status: str
    installed: bool
    fabric_path: str | None
    fab_path: str | None
    summary: list[str] = field(default_factory=list)
    checks: list[CommandResult] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)


def redact(text: str) -> str:
    value = text or ""
    for pattern in SECRET_PATTERNS:
        value = pattern.sub("[REDACTED_SECRET]", value)
    return value


def preview(text: str, limit: int) -> str:
    cleaned = redact(text).replace("\r", "")
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[:limit] + f"\n...[truncated {len(cleaned) - limit} chars]"


def run_command(name: str, command: Sequence[str], timeout: float, max_output: int) -> CommandResult:
    started = time.monotonic()
    try:
        proc = subprocess.run(list(command), text=True, capture_output=True, timeout=timeout, check=False)
        elapsed = int((time.monotonic() - started) * 1000)
        return CommandResult(
            name=name,
            command=list(command),
            ok=proc.returncode == 0,
            returncode=proc.returncode,
            duration_ms=elapsed,
            stdout_preview=preview(proc.stdout, max_output),
            stderr_preview=preview(proc.stderr, max_output),
        )
    except subprocess.TimeoutExpired as exc:
        elapsed = int((time.monotonic() - started) * 1000)
        return CommandResult(
            name=name,
            command=list(command),
            ok=False,
            returncode=None,
            duration_ms=elapsed,
            stdout_preview=preview(exc.stdout or "", max_output) if isinstance(exc.stdout, str) else "",
            stderr_preview=preview(exc.stderr or "", max_output) if isinstance(exc.stderr, str) else "",
            error=f"Timed out after {timeout:g}s",
        )
    except OSError as exc:
        elapsed = int((time.monotonic() - started) * 1000)
        return CommandResult(name=name, command=list(command), ok=False, returncode=None, duration_ms=elapsed, error=str(exc))


def build_report(deep: bool, timeout: float, max_output: int) -> DiagnosticReport:
    fabric_path = shutil.which("fabric")
    fab_path = shutil.which("fab")
    report = DiagnosticReport(status="unknown", installed=bool(fabric_path), fabric_path=fabric_path, fab_path=fab_path)

    if not fabric_path:
        report.status = "not_installed"
        report.summary.append("No `fabric` executable was found on PATH.")
        if fab_path:
            report.summary.append("A `fab` executable was found. That is commonly Microsoft Fabric CLI, not Fabric.so CLI.")
            report.recommendations.append("Use the Fabric.so CLI executable named `fabric`; do not substitute `fab`.")
        report.recommendations.append("Install only with user approval: curl -fsSL https://fabric.so/cli/install.sh | sh")
        report.recommendations.append("After installation, restart the shell or update PATH, then rerun this checker.")
        return report

    report.summary.append(f"Found Fabric.so CLI candidate at: {fabric_path}")
    if fab_path:
        report.summary.append(f"Also found `fab` at: {fab_path}. Keep Fabric.so `fabric` distinct from Microsoft Fabric `fab`.")

    local_commands = [
        ("version", ["fabric", "--version"]),
        ("top_level_help", ["fabric", "--help"]),
    ]
    for name, cmd in local_commands:
        report.checks.append(run_command(name, cmd, timeout, max_output))

    if any(not c.ok for c in report.checks):
        report.status = "local_error"
        report.summary.append("The `fabric` executable exists but one or more local checks failed.")
        report.recommendations.append("Run `fabric --help` manually and check aliases, permissions, and whether this is the Fabric.so binary.")
        return report

    if not deep:
        report.status = "installed_local_ok"
        report.summary.append("Local CLI checks passed. Run with --deep for read-only account and workspace checks.")
        report.recommendations.append("For live Fabric workflows, verify auth/workspace with `python3 scripts/fabric_check.py --deep --json`.")
        return report

    remote_commands = [
        ("workspace_current_json", ["fabric", "--json", "workspace", "current"]),
        ("workspace_list_json", ["fabric", "--json", "workspace", "list"]),
        ("task_list_json", ["fabric", "--json", "task", "list"]),
        ("subscription_json", ["fabric", "--json", "subscription"]),
    ]
    start = len(report.checks)
    for name, cmd in remote_commands:
        report.checks.append(run_command(name, cmd, timeout, max_output))

    if any(not c.ok for c in report.checks[start:]):
        report.status = "needs_auth_or_workspace"
        report.summary.append("Local CLI checks passed, but at least one read-only account/workspace check failed.")
        report.recommendations.append("Use `fabric login` in an interactive terminal, or `fabric auth` with a securely supplied API key for headless setup.")
        report.recommendations.append("Run `fabric workspace current` and `fabric workspace list` after authentication.")
        report.recommendations.append("If JSON output failed, retry the same command without `--json` for diagnostics.")
    else:
        report.status = "ok"
        report.summary.append("Local and read-only account/workspace checks passed.")

    return report


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read-only diagnostic checks for the Fabric.so CLI executable named fabric.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--deep", action="store_true", help="Run read-only account/workspace checks that contact Fabric.")
    parser.add_argument("--json", action="store_true", help="Emit a JSON diagnostic report.")
    parser.add_argument("--timeout", type=float, default=15.0, help="Timeout per command in seconds.")
    parser.add_argument("--max-output", type=int, default=2000, help="Maximum stdout/stderr preview characters per command.")
    parser.add_argument("--strict", action="store_true", help="Return non-zero for any non-ok status.")
    return parser.parse_args(list(argv))


def print_text(report: DiagnosticReport) -> None:
    print(f"Fabric CLI diagnostic status: {report.status}")
    print(f"Installed: {report.installed}")
    if report.fabric_path:
        print(f"fabric path: {report.fabric_path}")
    if report.fab_path:
        print(f"fab path: {report.fab_path}")
    print("\nSummary:")
    for item in report.summary:
        print(f"- {item}")
    if report.recommendations:
        print("\nRecommendations:")
        for item in report.recommendations:
            print(f"- {item}")


def main(argv: Iterable[str] = sys.argv[1:]) -> int:
    args = parse_args(argv)
    report = build_report(args.deep, args.timeout, args.max_output)
    if args.json:
        print(json.dumps(asdict(report), indent=2, sort_keys=True))
    else:
        print_text(report)
    if args.strict and report.status != "ok":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
