#!/usr/bin/env python3
"""
setup_cron.py
Adds Finance UX Observer jobs to the user's system crontab.

Run once after installing the skill:
    python3 ~/.openclaw/skills/finance-ux-observer/scripts/setup_cron.py

Options:
    --remove    Remove all Finance UX Observer cron entries
    --status    Show current status without making changes
"""

import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path.home() / ".openclaw" / "skills" / "finance-ux-observer"
LOG_DIR = SKILL_DIR / "logs"
MARKER = "# finance-ux-observer"

ENTRIES = [
    (
        "*/30 * * * *",
        f"python3 {SKILL_DIR}/scripts/observe_finance_usage.py",
        "30-min observation pass",
    ),
    (
        "55 23 * * *",
        f"TZ=America/Los_Angeles python3 {SKILL_DIR}/scripts/daily_synthesize.py"
        f" >> {LOG_DIR}/synthesize.log 2>&1",
        "end-of-day synthesis",
    ),
    (
        "0 6 * * *",
        f"TZ=America/Los_Angeles python3 {SKILL_DIR}/scripts/redact_reports.py --validate-only"
        f" >> {LOG_DIR}/redaction_check.log 2>&1",
        "redaction integrity check",
    ),
]


def get_crontab() -> str:
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    # crontab -l exits 1 with "no crontab" when empty — treat as empty string
    if result.returncode != 0 and "no crontab" in result.stderr.lower():
        return ""
    return result.stdout


def set_crontab(content: str) -> None:
    proc = subprocess.run(["crontab", "-"], input=content, text=True, capture_output=True)
    if proc.returncode != 0:
        print(f"Error writing crontab: {proc.stderr}", file=sys.stderr)
        sys.exit(1)


def cmd_install() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    (SKILL_DIR / "data" / "observations").mkdir(parents=True, exist_ok=True)
    (SKILL_DIR / "reports").mkdir(parents=True, exist_ok=True)

    current = get_crontab()
    lines = current.splitlines(keepends=True)

    added = 0
    new_lines = list(lines)
    # Ensure trailing newline before appending
    if new_lines and not new_lines[-1].endswith("\n"):
        new_lines[-1] += "\n"

    for schedule, command, label in ENTRIES:
        cron_line = f"{schedule} {command} {MARKER}\n"
        if command in current:
            print(f"  ✓  Already registered: {label}")
        else:
            new_lines.append(cron_line)
            print(f"  ➕ Added: {label}")
            added += 1

    if added:
        set_crontab("".join(new_lines))
        print(f"\n✅ {added} cron job(s) registered.")
    else:
        print("\n✅ All jobs already registered — nothing changed.")


def cmd_remove() -> None:
    current = get_crontab()
    filtered = [l for l in current.splitlines(keepends=True) if MARKER not in l]
    removed = len(current.splitlines()) - len(filtered)
    if removed:
        set_crontab("".join(filtered))
        print(f"✅ Removed {removed} Finance UX Observer cron entry/entries.")
    else:
        print("No Finance UX Observer cron entries found.")


def cmd_status() -> None:
    current = get_crontab()
    our_lines = [l.strip() for l in current.splitlines() if MARKER in l]
    if not our_lines:
        print("❌ No Finance UX Observer cron jobs registered.")
        print("   Run: python3 setup_cron.py")
    else:
        print(f"✅ {len(our_lines)} cron job(s) registered:\n")
        for line in our_lines:
            print(f"  {line}")


def main() -> None:
    flag = sys.argv[1] if len(sys.argv) > 1 else "--install"
    dispatch = {
        "--install": cmd_install,
        "--remove":  cmd_remove,
        "--status":  cmd_status,
    }
    handler = dispatch.get(flag)
    if handler is None:
        print(f"Unknown option: {flag}. Valid: {list(dispatch)}", file=sys.stderr)
        sys.exit(1)
    handler()


if __name__ == "__main__":
    main()
