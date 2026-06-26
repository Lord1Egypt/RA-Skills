#!/usr/bin/env python3
"""Deterministic OpenClaw cron health report.

Usage:
  python3 openclaw_cron_health_check.py /absolute/path/to/config.json

The script is stdlib-only, runs constrained local diagnostic probes, avoids
shell execution, does not intentionally mutate scheduler state, and prints one
report to stdout.
"""

from __future__ import annotations

import datetime as dt
import glob
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

STATUS_ORDER = {"OK": 0, "INFO": 1, "WARNING": 2, "CRITICAL": 3}
ERROR_RE = re.compile(
    r"error|fatal|exception|panic|segfault|killed|ENOENT|EACCES|EPERM|exit code [1-9]|traceback|permission denied|no such file",
    re.IGNORECASE,
)
SAFE_EXACT_ARGV = {
    ("openclaw", "cron", "list", "--json"),
    ("crontab", "-l"),
    ("systemctl", "--failed", "--no-pager", "--plain"),
    ("systemctl", "list-timers", "--all", "--no-pager", "--plain"),
}
SERVICE_NAME_RE = re.compile(r"^[A-Za-z0-9_.@:+-]+$")
BLOCKED_BINS = {
    "bash",
    "curl",
    "dash",
    "fish",
    "ftp",
    "nc",
    "netcat",
    "rsync",
    "scp",
    "sh",
    "ssh",
    "su",
    "sudo",
    "telnet",
    "wget",
    "zsh",
}


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def load_config(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def max_line(cfg: dict[str, Any]) -> int:
    try:
        return int(cfg.get("runtime", {}).get("max_line_chars", 240))
    except Exception:
        return 240


def shorten(text: Any, limit: int = 240) -> str:
    value = "" if text is None else str(text).replace("\n", " ").strip()
    if len(value) <= limit:
        return value
    return value[: max(0, limit - 3)] + "..."


def redact(text: Any, patterns: list[str], limit: int = 240) -> str:
    value = "" if text is None else str(text)
    for pattern in patterns:
        value = re.sub(pattern, "<redacted>", value)
    return shorten(value, limit)


def command_label(command: Any) -> str:
    if isinstance(command, dict):
        argv = command.get("argv")
        if isinstance(argv, list):
            return " ".join(str(part) for part in argv)
    return str(command)


def command_argv(command: Any) -> tuple[list[str], str | None]:
    """Return a shell-free argv vector and optional cwd.

    New configs should use {"argv": [...], "cwd": "..."} objects. A simple
    legacy string is accepted only as whitespace-separated arguments with no
    shell syntax support.
    """
    cwd: str | None = None
    if isinstance(command, dict):
        argv = command.get("argv")
        cwd_value = command.get("cwd")
        if cwd_value:
            if not isinstance(cwd_value, str) or not cwd_value.startswith("/") or not os.path.isdir(cwd_value):
                raise ValueError("cwd must be an existing absolute directory")
            cwd = cwd_value
        if not isinstance(argv, list) or not argv or not all(isinstance(part, str) and part for part in argv):
            raise ValueError("command object must contain non-empty string argv")
        return argv, cwd
    if isinstance(command, str):
        if any(ch in command for ch in "|;&`(){}<>$\\\n\r"):
            raise ValueError("command string contains shell syntax; use an argv object")
        parts = command.split()
        if not parts:
            raise ValueError("empty command")
        return parts, None
    raise ValueError("command must be an argv object or simple legacy string")


def is_safe_builtin_argv(argv: list[str]) -> bool:
    parts = tuple(argv)
    if parts in SAFE_EXACT_ARGV:
        return True
    return (
        len(argv) == 3
        and argv[0] == "systemctl"
        and argv[1] == "is-active"
        and bool(SERVICE_NAME_RE.fullmatch(argv[2]))
    )


def validate_runnable_command(command: Any, cfg: dict[str, Any]) -> tuple[list[str], str | None]:
    argv, cwd = command_argv(command)
    base = os.path.basename(argv[0])
    if base in BLOCKED_BINS:
        raise ValueError(f"blocked command: {base}")
    if argv[0].startswith("/"):
        raise ValueError("absolute command paths are not supported by the portable checker")
    if not is_safe_builtin_argv(argv):
        raise ValueError(f"argv is not in the non-mutating diagnostic allowlist: {command_label(command)}")
    return argv, cwd


def run(command: Any, cfg: dict[str, Any], timeout: int = 20) -> tuple[int, str, str]:
    try:
        argv, cwd = validate_runnable_command(command, cfg)
        proc = subprocess.run(
            argv,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            cwd=cwd,
        )
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except subprocess.TimeoutExpired as exc:
        return 124, exc.stdout or "", f"timeout after {timeout}s"
    except Exception as exc:
        return 1, "", str(exc)


def worst(*statuses: str) -> str:
    return max(statuses, key=lambda s: STATUS_ORDER.get(s, 0)) if statuses else "INFO"


def is_placeholder(value: Any) -> bool:
    if isinstance(value, str):
        return not value or (value.startswith("<") and value.endswith(">"))
    if isinstance(value, dict) and "argv" in value:
        argv = value.get("argv")
        return not argv or any(is_placeholder(part) for part in argv)
    return False


def command_status(command: Any) -> tuple[str, str]:
    """Best-effort command existence check without executing the command.

    Returns OK, WARNING, or CRITICAL. WARNING means the command is not
    statically provable, not necessarily broken.
    """
    if is_placeholder(command):
        return "INFO", "placeholder not configured"
    if isinstance(command, str) and any(ch in command for ch in "|;&`(){}<>$\\\n\r"):
        return "WARNING", "shell syntax is not executed; require log or metadata proof"
    try:
        argv, cwd = command_argv(command)
    except Exception as exc:
        return "WARNING", str(exc)
    base = os.path.basename(argv[0])
    if base in BLOCKED_BINS:
        return "WARNING", f"blocked command: {base}"
    if cwd and not os.path.isdir(cwd):
        return "CRITICAL", f"working directory missing: {cwd}"
    if not is_safe_builtin_argv(argv):
        return "WARNING", "argv not in non-mutating diagnostic allowlist"
    if argv[0].startswith("/"):
        return "WARNING", "absolute command paths are not supported by the portable checker"
    return ("OK", "binary exists") if shutil.which(argv[0]) else ("CRITICAL", f"binary missing: {argv[0]}")


def get_any(data: dict[str, Any], keys: list[str]) -> Any:
    for key in keys:
        cur: Any = data
        ok = True
        for part in key.split("."):
            if isinstance(cur, dict) and part in cur:
                cur = cur[part]
            else:
                ok = False
                break
        if ok and cur not in (None, ""):
            return cur
    return None


def load_openclaw_jobs(cfg: dict[str, Any]) -> tuple[list[dict[str, Any]], str]:
    oc = cfg.get("openclaw", {})
    jobs: Any = []
    source = "none"
    list_command = oc.get("list_command")
    if list_command and not is_placeholder(list_command):
        status, _ = command_status(list_command)
        if status in {"OK", "WARNING"}:
            code, out, _ = run(list_command, cfg)
            if code == 0 and out:
                try:
                    data = json.loads(out)
                    jobs = data.get("jobs", data.get("items", data)) if isinstance(data, dict) else data
                    source = "command"
                except Exception:
                    jobs = []
    if not jobs:
        jobs_file = oc.get("jobs_file")
        if jobs_file and not is_placeholder(jobs_file) and os.path.exists(jobs_file):
            with open(jobs_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            jobs = data.get("jobs", data.get("items", data)) if isinstance(data, dict) else data
            source = "jobs_file"
    if isinstance(jobs, dict):
        jobs = list(jobs.values())
    clean: list[dict[str, Any]] = []
    for job in jobs if isinstance(jobs, list) else []:
        if isinstance(job, dict):
            copied = dict(job)
            copied["_health_source"] = source
            clean.append(copied)
    return clean, source


def classify_openclaw_job(job: dict[str, Any], patterns: list[str], limit: int) -> tuple[str, str]:
    paused = bool(get_any(job, ["paused", "disabled"]) or get_any(job, ["enabled"]) is False)
    name = get_any(job, ["name", "title", "label", "id"]) or "unnamed"
    last_status = get_any(job, ["lastStatus", "last_status", "status", "lastRun.status", "lastRunStatus"]) or "unknown"
    last_run = get_any(job, ["lastRun", "last_run", "lastRunAt", "last_run_at", "lastCompletedAt"])
    next_run = get_any(job, ["nextRun", "next_run", "next", "nextRunAt", "next_run_at", "nextFireAt"])
    schedule = get_any(job, ["schedule", "cron", "expr", "spec"])
    delivery_error = get_any(job, ["lastDeliveryError", "last_delivery_error", "deliveryError", "delivery.error"])
    script = get_any(job, ["script", "scriptPath", "script_path", "runtime.script"])
    source = job.get("_health_source", "unknown")
    try:
        consecutive_errors = int(get_any(job, ["consecutiveErrors", "consecutive_errors", "errorCount"]) or 0)
    except Exception:
        consecutive_errors = 0

    status = "OK"
    reasons: list[str] = []
    if paused:
        status = "INFO"
        reasons.append("paused")
    if consecutive_errors >= 3:
        status = "CRITICAL"
        reasons.append(f"{consecutive_errors} consecutive errors")
    elif consecutive_errors > 0:
        status = worst(status, "WARNING")
        reasons.append(f"{consecutive_errors} consecutive errors")
    if str(last_status).lower() in {"error", "failed", "failure"}:
        status = worst(status, "WARNING")
        reasons.append(f"last status {last_status}")
    if delivery_error:
        status = worst(status, "WARNING")
        reasons.append("delivery error")
    if not paused and not next_run:
        if schedule:
            if status == "OK":
                status = "INFO"
            reasons.append(f"next run not exposed by {source}")
        else:
            status = worst(status, "WARNING")
            reasons.append("no visible next run or schedule")
    if script and str(script).startswith("/") and not os.path.exists(str(script)):
        status = "CRITICAL"
        reasons.append("script missing")
    if not reasons:
        reasons.append("metadata healthy")
    detail = f"{name} - last: {last_run or 'unknown'}, next: {next_run or 'unknown'}, schedule: {shorten(schedule, 80)}, status: {last_status}; {', '.join(reasons)}"
    if delivery_error:
        detail += f"; error: {redact(delivery_error, patterns, limit)}"
    return status, shorten(detail, limit)


def compile_ignore(cfg: dict[str, Any]) -> list[re.Pattern[str]]:
    return [re.compile(p) for p in cfg.get("system_crons", {}).get("ignore_lines_matching", [])]


def cron_command(line: str, system_file: bool) -> str:
    if not line:
        return ""
    if line.startswith("@"):
        parts = line.split(maxsplit=2 if system_file else 1)
        if system_file and len(parts) >= 3:
            return parts[2]
        return parts[1] if len(parts) >= 2 else ""
    parts = line.split()
    min_parts = 7 if system_file else 6
    if len(parts) < min_parts:
        return ""
    return " ".join(parts[6 if system_file else 5 :])


def parse_cron_sources(cfg: dict[str, Any]) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    sys_crons = cfg.get("system_crons", {})
    ignore = compile_ignore(cfg)
    for source in sys_crons.get("crontab_commands", []):
        if is_placeholder(source):
            continue
        code, out, _ = run(source, cfg)
        if code != 0:
            continue
        for line in out.splitlines():
            text = line.strip()
            if any(r.search(text) for r in ignore):
                continue
            if "=" in text and not text.lstrip().startswith(("@", "*", *tuple(str(i) for i in range(10)))):
                continue
            command = cron_command(text, system_file=False)
            if command:
                items.append({"source": command_label(source), "line": text, "command": command, "kind": "crontab"})
    for pattern in sys_crons.get("crontab_files", []):
        if is_placeholder(pattern):
            continue
        for path in glob.glob(pattern):
            if not os.path.isfile(path):
                continue
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    text = line.strip()
                    if any(r.search(text) for r in ignore):
                        continue
                    if "=" in text and not text.startswith(("@", "*")):
                        continue
                    command = cron_command(text, system_file=True)
                    if command:
                        items.append({"source": path, "line": text, "command": command, "kind": "crontab_file"})
    for item in sys_crons.get("run_parts_dirs", []):
        path = item.get("path") if isinstance(item, dict) else str(item)
        if is_placeholder(path) or not path:
            continue
        for child in sorted(Path(path).iterdir()) if os.path.isdir(path) else []:
            if child.is_file() and not child.name.startswith("."):
                items.append({"source": path, "line": str(child), "command": str(child), "kind": "run_parts"})
    return items


def infer_log_path(command: str) -> str | None:
    m = re.search(r">>?\s*([^\s]+)", command)
    if not m:
        return None
    path = m.group(1).strip().strip("'\"")
    return path if path.startswith("/") else None


def validate_log(log_file: str | None, freshness_minutes: int | None, patterns: list[str], limit: int) -> tuple[str, str]:
    if not log_file or is_placeholder(log_file):
        return "WARNING", "no runtime proof"
    if not os.path.exists(log_file):
        return "CRITICAL", "log missing"
    age_minutes = int((now_utc().timestamp() - os.path.getmtime(log_file)) / 60)
    status = "OK" if freshness_minutes is None or age_minutes <= freshness_minutes else "WARNING"
    lines = Path(log_file).read_text(encoding="utf-8", errors="replace").splitlines()[-50:]
    errors = [redact(line, patterns, limit) for line in lines if ERROR_RE.search(line)]
    if len(errors) > 5:
        status = "CRITICAL"
    elif errors:
        status = worst(status, "WARNING")
    last = redact(lines[-1], patterns, limit) if lines else "empty log"
    err = f"; error: {errors[-1]}" if errors else ""
    return status, f"log age {age_minutes}m; errors {len(errors)}; last: {last}{err}"


def validate_known_system_jobs(cfg: dict[str, Any], patterns: list[str], limit: int) -> list[tuple[str, str]]:
    results: list[tuple[str, str]] = []
    for job in cfg.get("known_system_jobs", []):
        name = job.get("name", "unnamed")
        cmd = job.get("command") or job.get("command_or_script") or job.get("script") or ""
        if is_placeholder(name) and is_placeholder(cmd):
            continue
        cmd_status, cmd_detail = command_status(cmd)
        status = "WARNING" if cmd_status == "INFO" else cmd_status
        details = [cmd_detail]
        log_file = job.get("log_file") or job.get("log")
        log_status, log_detail = validate_log(log_file, job.get("expected_log_freshness_minutes"), patterns, limit)
        status = worst(status, log_status)
        details.append(log_detail)
        validation = job.get("safe_validation_command")
        if validation and not is_placeholder(validation):
            code, out, err = run(validation, cfg, timeout=60)
            if code != 0:
                status = worst(status, "WARNING")
                details.append(f"validation failed: {redact(err or out, patterns, limit)}")
            else:
                details.append("validation passed")
        results.append((status, shorten(f"{name} - {' | '.join(details)}", limit)))
    return results


def system_health(cfg: dict[str, Any], patterns: list[str], limit: int) -> list[tuple[str, str]]:
    results: list[tuple[str, str]] = []
    cron_service = cfg.get("system", {}).get("cron_service")
    if cron_service and not is_placeholder(cron_service) and shutil.which("systemctl"):
        code, out, err = run({"argv": ["systemctl", "is-active", str(cron_service)]}, cfg)
        results.append(("OK" if out == "active" else "CRITICAL", f"{cron_service}: {redact(out or err, patterns, limit)}"))
    failed_cmd = cfg.get("system", {}).get("failed_units_command")
    if failed_cmd and not is_placeholder(failed_cmd):
        probe_status, _ = command_status(failed_cmd)
        if probe_status in {"OK", "WARNING"}:
            code, out, err = run(failed_cmd, cfg)
            clean = redact(out or err or "none", patterns, limit)
            no_failed = "0 loaded units listed" in (out or "") or "0 loaded units" in (out or "")
            status = "OK" if code == 0 and no_failed else "WARNING"
            results.append((status, f"systemd failed units: {clean or 'none'}"))
    return results


def validate_expected_project_jobs(projects: list[dict[str, Any]], jobs: list[dict[str, Any]], patterns: list[str], limit: int) -> list[tuple[str, str]]:
    results: list[tuple[str, str]] = []
    names = {str(get_any(job, ["name", "title", "label", "id"])) for job in jobs}
    for project in projects:
        name = project.get("name", "project")
        expected = [e for e in project.get("expected_openclaw_jobs", []) if not is_placeholder(e)]
        missing = [e for e in expected if e not in names]
        status = "WARNING" if missing else "OK"
        details = [f"missing expected jobs: {', '.join(missing)}" if missing else "expected jobs present"] if expected else ["no expected jobs configured"]
        command = project.get("validation_command", "")
        if command and not is_placeholder(command):
            code, out, err = run(command, cfg, timeout=60)
            if code != 0:
                status = worst(status, "WARNING")
                details.append(f"validation failed: {redact(err or out, patterns, limit)}")
            else:
                details.append("validation passed")
        elif not expected:
            status = "INFO"
        results.append((status, shorten(f"{name}: {' | '.join(details)}", limit)))
    return results


def registry_notes(cfg: dict[str, Any], jobs: list[dict[str, Any]], limit: int) -> list[tuple[str, str]]:
    reg = cfg.get("registry", {})
    if not reg.get("enabled"):
        return [("INFO", "registry reconciliation disabled")]
    notes: list[str] = []
    registry_file = reg.get("task_registry_file")
    if not registry_file or is_placeholder(registry_file) or not os.path.exists(registry_file):
        notes.append("registry file missing or not configured")
    else:
        text = Path(registry_file).read_text(encoding="utf-8", errors="replace")
        for job in jobs:
            name = str(get_any(job, ["name", "title", "id"]) or "")
            if name and name not in text:
                notes.append(f"missing registry entry: {name}")
    if not notes:
        notes.append("no registry notes")
    status = "WARNING" if any("missing" in n for n in notes) else "INFO"
    return [(status, shorten("; ".join(notes), limit))]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: openclaw_cron_health_check.py /absolute/path/to/config.json", file=sys.stderr)
        return 2
    cfg = load_config(sys.argv[1])
    limit = max_line(cfg)
    patterns = cfg.get("privacy", {}).get("redact_patterns", [])
    instance = cfg.get("instance", {}).get("name", "OpenClaw instance")
    generated = now_utc().strftime("%Y-%m-%d %H:%M UTC")

    sections: dict[str, list[tuple[str, str]]] = {"system": [], "openclaw": [], "system_crons": [], "known_jobs": [], "projects": [], "registry": []}
    sections["system"].extend(system_health(cfg, patterns, limit))

    jobs, source = load_openclaw_jobs(cfg)
    include_paused = cfg.get("openclaw", {}).get("include_paused", True)
    for job in jobs:
        if not include_paused and (job.get("paused") or job.get("disabled")):
            continue
        sections["openclaw"].append(classify_openclaw_job(job, patterns, limit))
    if not jobs:
        sections["openclaw"].append(("WARNING", "no OpenClaw jobs found from configured sources"))

    for entry in parse_cron_sources(cfg):
        cmd = entry["command"]
        cmd_status, cmd_detail = command_status(cmd)
        log_path = infer_log_path(cmd)
        log_status, log_detail = validate_log(log_path, None, patterns, limit) if log_path else ("WARNING", "no runtime proof")
        status = worst(cmd_status, log_status)
        if cmd_status == "INFO":
            status = worst("WARNING", log_status)
        sections["system_crons"].append((status, shorten(f"{entry['source']}: {cmd_detail} | {log_detail}", limit)))

    sections["known_jobs"].extend(validate_known_system_jobs(cfg, patterns, limit))
    projects = cfg.get("known_project_validations", [])
    sections["projects"].extend(validate_expected_project_jobs(projects, jobs, patterns, limit))
    sections["registry"].extend(registry_notes(cfg, jobs, limit))

    all_items = [item for values in sections.values() for item in values]
    total = len(all_items)
    healthy = sum(1 for status, _ in all_items if status in {"OK", "INFO"})
    issues = sum(1 for status, _ in all_items if status in {"WARNING", "CRITICAL"})
    worst_status = worst(*(s for s, _ in all_items)) if all_items else "INFO"

    print(f"OpenClaw Cron Health Report - {instance}")
    print(f"Generated: {generated}")
    print(f"Summary: {healthy}/{total} healthy or informational | {issues} attention points | overall {worst_status}")
    print("")
    labels = [
        ("System", "system"),
        ("OpenClaw Jobs", "openclaw"),
        ("System Crons", "system_crons"),
        ("Known System Jobs", "known_jobs"),
        ("Project Scheduler Checks", "projects"),
        ("Registry Notes", "registry"),
    ]
    for title, key in labels:
        print(title)
        values = sections[key] or [("INFO", "none configured")]
        for status, detail in values:
            print(f"- [{status}] {redact(detail, patterns, limit)}")
        print("")
    if issues:
        print("Conclusion: attention required before considering all scheduled automation healthy.")
    else:
        print("Conclusion: scheduled automation appears healthy from configured non-mutating diagnostic checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
