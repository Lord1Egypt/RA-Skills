#!/usr/bin/env python3
"""
cron_sentinel.py - Bulletproof scheduling that tells you when a job SILENTLY fails.

The dangerous failure isn't the job that errors loudly - it's the one that never
runs at all (machine asleep, cron misconfigured, command renamed) and produces no
error for anyone to notice. Cron Sentinel wraps your scheduled command so every
run is recorded, retries transient failures, and a separate `check` catches both
crashed AND missing (overdue) jobs.

  wrap     - run a command, retry on failure, record the outcome to a state file
  check    - report jobs that failed or are overdue; exit 1 if anything's wrong
  status   - list every tracked job, its last run, and when it's next expected
  crontab  - print a ready-to-paste crontab line that wraps a command

Usage:
  python cron_sentinel.py wrap --name backup --expect-every 1d --retries 2 -- /path/backup.sh
  python cron_sentinel.py check
  python cron_sentinel.py status
  python cron_sentinel.py crontab --name backup --schedule "0 3 * * *" --expect-every 1d -- /path/backup.sh

State lives in ~/.cron-sentinel/state.json (override with --state or $CRON_SENTINEL_STATE).
All timestamps are stored in UTC so it stays correct across timezones and DST.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

DEFAULT_STATE = os.environ.get("CRON_SENTINEL_STATE", "~/.cron-sentinel/state.json")
DUR_RE = re.compile(r"(\d+)\s*([smhdw])", re.I)
UNIT_SEC = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}


# --------------------------------------------------------------------------- #
# Duration parsing / formatting
# --------------------------------------------------------------------------- #

def parse_duration(text: str | None) -> int | None:
    """'1d', '12h', '90m', '1w2d' -> seconds. None stays None."""
    if not text:
        return None
    total, found = 0, False
    for num, unit in DUR_RE.findall(text):
        total += int(num) * UNIT_SEC[unit.lower()]
        found = True
    return total if found else None


def human_secs(s: float | None) -> str:
    if s is None:
        return "unknown"
    s = int(s)
    if s < 60:
        return f"{s}s"
    if s < 3600:
        return f"{s // 60}m"
    if s < 86400:
        return f"{s // 3600}h {s % 3600 // 60}m"
    return f"{s // 86400}d {s % 86400 // 3600}h"


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat()


def from_iso(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


# --------------------------------------------------------------------------- #
# State
# --------------------------------------------------------------------------- #

def state_path(explicit: str | None) -> Path:
    return Path(os.path.expanduser(explicit or DEFAULT_STATE))


def load_state(path: Path) -> dict:
    if path.is_file():
        try:
            return json.loads(path.read_text())
        except json.JSONDecodeError:
            pass
    return {"jobs": {}}


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2))
    tmp.replace(path)  # atomic on POSIX


# --------------------------------------------------------------------------- #
# wrap: run, retry, record
# --------------------------------------------------------------------------- #

def cmd_wrap(args) -> int:
    if not args.command:
        print("No command given. Put it after `--`, e.g. wrap --name x -- echo hi", file=sys.stderr)
        return 2
    sp = state_path(args.state)
    state = load_state(sp)
    job = state["jobs"].get(args.name, {})

    expect = parse_duration(args.expect_every)
    if expect is None and job.get("expect_every_sec"):
        expect = job["expect_every_sec"]

    start = now_utc()
    attempts = args.retries + 1
    exit_code, tail = 1, ""
    for attempt in range(1, attempts + 1):
        try:
            proc = subprocess.run(
                args.command,
                capture_output=True,
                text=True,
                timeout=args.timeout or None,
            )
            exit_code = proc.returncode
            out = (proc.stdout or "") + (proc.stderr or "")
            tail = "\n".join(out.splitlines()[-15:])[-2000:]
            # pass through so wrapping stays transparent in logs/pipelines
            if proc.stdout:
                sys.stdout.write(proc.stdout)
            if proc.stderr:
                sys.stderr.write(proc.stderr)
        except subprocess.TimeoutExpired:
            exit_code, tail = 124, f"Timed out after {args.timeout}s"
            sys.stderr.write(tail + "\n")
        except FileNotFoundError as e:
            exit_code, tail = 127, f"Command not found: {e}"
            sys.stderr.write(tail + "\n")

        if exit_code == 0:
            break
        if attempt < attempts:
            backoff = min(2 ** attempt, 30)
            sys.stderr.write(f"[cron-sentinel] attempt {attempt} failed (exit {exit_code}); "
                             f"retrying in {backoff}s\n")
            time.sleep(backoff)

    end = now_utc()
    prev_fail = job.get("consecutive_failures", 0)
    state["jobs"][args.name] = {
        "expect_every_sec": expect,
        "last_start": iso(start),
        "last_end": iso(end),
        "last_exit": exit_code,
        "last_duration_sec": round((end - start).total_seconds(), 2),
        "last_output_tail": tail,
        "consecutive_failures": 0 if exit_code == 0 else prev_fail + 1,
        "last_success": iso(end) if exit_code == 0 else job.get("last_success"),
        "runs": job.get("runs", 0) + 1,
    }
    save_state(sp, state)
    return exit_code


# --------------------------------------------------------------------------- #
# check: failed or overdue
# --------------------------------------------------------------------------- #

def evaluate(state: dict, grace: float) -> list[dict]:
    """Return a problem record per unhealthy job."""
    problems = []
    now = now_utc()
    for name, j in state.get("jobs", {}).items():
        # crashed: last run exited non-zero
        if j.get("last_exit", 0) != 0:
            problems.append({
                "name": name, "kind": "failed",
                "detail": f"last run exited {j['last_exit']} "
                          f"({j.get('consecutive_failures', 1)}x in a row)",
                "tail": j.get("last_output_tail", ""),
            })
            continue
        # silent / overdue: expected to run by now but hasn't
        expect = j.get("expect_every_sec")
        last = from_iso(j.get("last_start"))
        if expect and last:
            deadline = last + timedelta(seconds=expect * (1 + grace))
            if now > deadline:
                overdue = (now - last).total_seconds()
                problems.append({
                    "name": name, "kind": "overdue",
                    "detail": f"expected every {human_secs(expect)}, but last ran "
                              f"{human_secs(overdue)} ago - it may have silently stopped",
                    "tail": "",
                })
    return problems


def cmd_check(args) -> int:
    state = load_state(state_path(args.state))
    if not state.get("jobs"):
        print("No jobs are being tracked yet. Wrap a command with `wrap` first.")
        return 0
    problems = evaluate(state, args.grace)
    if args.json:
        print(json.dumps(problems, indent=2))
        return 1 if problems else 0
    if not problems:
        print(f"🟢 All {len(state['jobs'])} tracked jobs are healthy.")
        return 0
    print(f"🔴 {len(problems)} job(s) need attention:\n")
    for p in problems:
        icon = "💥" if p["kind"] == "failed" else "🔇"
        print(f"{icon} {p['name']}: {p['detail']}")
        if p["tail"]:
            tail = p["tail"].splitlines()
            print("   last output:")
            for line in tail[-4:]:
                print(f"     | {line}")
    return 1


# --------------------------------------------------------------------------- #
# status
# --------------------------------------------------------------------------- #

def cmd_status(args) -> int:
    state = load_state(state_path(args.state))
    jobs = state.get("jobs", {})
    if not jobs:
        print("No jobs tracked yet.")
        return 0
    now = now_utc()
    print(f"{'JOB':<20} {'LAST RUN':<14} {'STATUS':<10} {'NEXT EXPECTED':<16}")
    print("-" * 62)
    for name, j in sorted(jobs.items()):
        last = from_iso(j.get("last_start"))
        ago = human_secs((now - last).total_seconds()) + " ago" if last else "never"
        status = "ok" if j.get("last_exit", 0) == 0 else f"FAIL({j['last_exit']})"
        expect = j.get("expect_every_sec")
        if expect and last:
            due = last + timedelta(seconds=expect)
            nxt = "overdue" if now > due + timedelta(seconds=expect * args.grace) else human_secs((due - now).total_seconds())
        else:
            nxt = "n/a"
        print(f"{name:<20} {ago:<14} {status:<10} {nxt:<16}")
    return 0


# --------------------------------------------------------------------------- #
# crontab: emit a ready-to-paste line
# --------------------------------------------------------------------------- #

def cmd_crontab(args) -> int:
    if not args.command:
        print("Provide the command after `--`.", file=sys.stderr)
        return 2
    script = os.path.abspath(__file__)
    py = sys.executable or "python3"
    inner = " ".join(_shquote(c) for c in args.command)
    expect = f" --expect-every {args.expect_every}" if args.expect_every else ""
    retries = f" --retries {args.retries}" if args.retries else ""
    line = (f'{args.schedule} {py} {script} wrap --name {args.name}{expect}{retries} '
            f'-- {inner}')
    print("# Paste into your crontab (crontab -e). Then have Sentinel watch them:")
    print(line)
    print(f"# And a watchdog that alerts on failures/silence every 30 min:")
    print(f'*/30 * * * * {py} {script} check || true  # pipe to your notifier')
    return 0


def _shquote(s: str) -> str:
    return s if re.fullmatch(r"[A-Za-z0-9_./:=-]+", s) else "'" + s.replace("'", "'\\''") + "'"


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main(argv=None):
    ap = argparse.ArgumentParser(description="Bulletproof scheduling with silent-failure detection.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def st(p):
        p.add_argument("--state", help="State file (default ~/.cron-sentinel/state.json).")

    pw = sub.add_parser("wrap", help="Run a command, retry on failure, record the outcome.")
    st(pw)
    pw.add_argument("--name", required=True)
    pw.add_argument("--expect-every", help="Cadence for overdue detection, e.g. 1d, 12h, 1w.")
    pw.add_argument("--retries", type=int, default=0)
    pw.add_argument("--timeout", type=int, default=0, help="Per-attempt timeout seconds (0 = none).")
    pw.add_argument("command", nargs=argparse.REMAINDER, help="Command after `--`.")

    pc = sub.add_parser("check", help="Report failed or overdue jobs (exit 1 if any).")
    st(pc)
    pc.add_argument("--grace", type=float, default=0.5, help="Overdue grace as fraction of interval (default 0.5).")
    pc.add_argument("--json", action="store_true")

    pstat = sub.add_parser("status", help="List all tracked jobs.")
    st(pstat)
    pstat.add_argument("--grace", type=float, default=0.5)

    pcron = sub.add_parser("crontab", help="Print a ready-to-paste wrapped crontab line.")
    pcron.add_argument("--name", required=True)
    pcron.add_argument("--schedule", required=True, help='Cron expression, e.g. "0 3 * * *".')
    pcron.add_argument("--expect-every")
    pcron.add_argument("--retries", type=int, default=0)
    pcron.add_argument("command", nargs=argparse.REMAINDER)

    args = ap.parse_args(argv)
    # strip a leading "--" left in REMAINDER
    if getattr(args, "command", None) and args.command and args.command[0] == "--":
        args.command = args.command[1:]

    return {
        "wrap": cmd_wrap,
        "check": cmd_check,
        "status": cmd_status,
        "crontab": cmd_crontab,
    }[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main() or 0)
