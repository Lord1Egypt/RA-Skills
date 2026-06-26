#!/usr/bin/env python3
"""
Update dream cron messages with today's date.
Reads job IDs dynamically from openclaw cron list.
Finds openclaw executable dynamically.

SAFETY: Cron editing is DISABLED by default.
Use --confirm flag to enable: python update-cron-date.py --confirm
"""

import subprocess
import os
import json
import shutil
import sys
import argparse
from datetime import datetime


def find_openclaw():
    """Find openclaw executable dynamically. Returns (bin, script_path)."""
    # Try environment variables first
    if os.environ.get("OPENCLAW_PATH"):
        return os.environ["OPENCLAW_PATH"], None
    if os.environ.get("OPENCLAW_SCRIPT") and os.path.exists(os.environ.get("OPENCLAW_SCRIPT", "")):
        return os.environ.get("OPENCLAW_BIN", "node"), os.environ["OPENCLAW_SCRIPT"]

    # Try common locations (no npm required)
    common_paths = [
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "npm", "node_modules", "openclaw", "dist", "index.js"),
        os.path.join(os.environ.get("APPDATA", ""), "npm", "node_modules", "openclaw", "dist", "index.js"),
    ]
    for p in common_paths:
        if os.path.exists(p):
            return "node", p

    # Try shutil.which
    path = shutil.which("openclaw")
    if path:
        return "openclaw", None

    # Last resort: return defaults and let subprocess resolve via PATH
    return os.environ.get("OPENCLAW_BIN", "node"), os.environ.get("OPENCLAW_SCRIPT", "")


def run_openclaw(args, openclaw_bin, openclaw_script):
    """Run openclaw CLI and return JSON output."""
    if openclaw_script:
        cmd = [openclaw_bin, openclaw_script] + args
    else:
        cmd = [openclaw_bin] + args
    cmd = [c for c in cmd if c]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    except Exception:
        result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        try:
            result = subprocess.run([openclaw_bin] + args, capture_output=True, text=True, encoding="utf-8", errors="replace")
        except Exception:
            result = subprocess.run([openclaw_bin] + args, capture_output=True, text=True)
    return result.stdout or "", result.returncode


def get_dream_job_ids(openclaw_bin, openclaw_script):
    """Get dream job IDs from openclaw cron list dynamically."""
    output, code = run_openclaw(["cron", "list", "--json"], openclaw_bin, openclaw_script)
    if code != 0:
        output, code = run_openclaw(["cron", "list"], openclaw_bin, openclaw_script)

    try:
        data = json.loads(output)
        jobs = data.get("jobs", data) if isinstance(data, dict) else data
        if isinstance(jobs, list):
            return {j["name"]: j["id"] for j in jobs if "dream" in j.get("name", "").lower()}
    except (json.JSONDecodeError, KeyError):
        pass

    # Fallback IDs from env or known defaults
    return {
        "dream-morning": os.environ.get("DREAM_MORNING_JOB_ID", ""),
        "dream-night": os.environ.get("DREAM_NIGHT_JOB_ID", ""),
    }


def get_log_dir():
    """Get workspace/memory dir dynamically."""
    return os.environ.get(
        "OPENCLAW_WORKSPACE",
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "workspace", "memory")
    )


def build_message(today_str, workspace):
    """Build the dream cron message for today."""
    today = datetime.strptime(today_str, "%Y-%m-%d")
    log_file = today.strftime("%Y/%m/%Y-%m-%d.md")

    return f"""Execute the dream distillation skill. Today is {today_str}.

PHASE 1 - Read today's daily log:
Read {workspace}/logs/{log_file} (create logs/ dir structure if missing).

PHASE 2 - Distill into topic memories:
Read existing MEMORY.md and topic files in {workspace}/topics/.
For each significant insight from today's log:
- If it belongs to an existing topic, update that topic file
- If new, create a new topic file with proper frontmatter (type, name, description, created, updated)

PHASE 3 - Update MEMORY.md index:
MEMORY.md is an INDEX ONLY. Format: - [Title](topics/file.md) — one-line hook
Keep it under 200 lines.

PHASE 4 - Write dream report:
Write to {workspace}/dreams/{today_str}.md with:
- What happened today (factual summary)
- Key insights distilled
- What was learned / corrected / decided
- Tomorrow's focus

Write in Chinese. Be specific, not generic. Do NOT fabricate if log is sparse."""


def main():
    parser = argparse.ArgumentParser(
        description="Update dream cron messages with today's date. "
                    "SAFETY: Cron editing is disabled by default — use --confirm to enable."
    )
    parser.add_argument(
        "--confirm", action="store_true",
        help="CONFIRM cron job modification. Without this flag, only prints what would be updated (dry-run)."
    )
    args = parser.parse_args()

    # Find openclaw at runtime (not at import time)
    openclaw_bin, openclaw_script = find_openclaw()

    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    workspace = get_log_dir()
    message = build_message(today_str, workspace)
    job_ids = get_dream_job_ids(openclaw_bin, openclaw_script)

    print(f"[Dream Cron Date Updater] Today: {today_str}")
    print(f"[Dream Cron Date Updater] Workspace: {workspace}")
    print(f"[Dream Cron Date Updater] OpenClaw: {openclaw_bin} {' ' + openclaw_script if openclaw_script else ''}")
    print()

    if not job_ids.get("dream-morning") and not job_ids.get("dream-night"):
        print("[WARN] Could not find dream job IDs.")
        print("  Set DREAM_MORNING_JOB_ID / DREAM_NIGHT_JOB_ID env vars, or check 'openclaw cron list'.")

    for name, job_id in job_ids.items():
        if not job_id:
            print(f"[SKIP] No job ID for {name}")
            continue
        print(f"[DRY-RUN] {name} ({job_id})")
        print(f"  Message would be updated to: {message[:100]}...")

        if args.confirm:
            print(f"[APPLYING] Editing {name} cron job...")
            edit_cmd = ([openclaw_bin, openclaw_script, "cron", "edit", job_id, "--message", message] if openclaw_script
                        else [openclaw_bin, "cron", "edit", job_id, "--message", message])
            try:
                result = subprocess.run(edit_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
            except Exception:
                result = subprocess.run(edit_cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"[OK] {name} cron updated")
            else:
                print(f"[FAIL] {name}: {(result.stderr or '')[:200]}")
        else:
            print(f"[SAFE] Skipped (use --confirm to actually edit)")

    print()
    if not args.confirm:
        print("DRY-RUN complete. Use --confirm to apply changes.")


if __name__ == "__main__":
    main()
