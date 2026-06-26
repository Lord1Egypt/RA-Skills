#!/usr/bin/env python3
"""
Memory Lifecycle Health Check

Verifies the memory lifecycle system is working correctly.
Designed to be called from heartbeat or manually.

Usage:
    python3 health_check.py [--workspace PATH] [--agent AGENT_ID] [--fix]
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path


def check_file_exists(path, name):
    """Check if a structured file exists."""
    if path.exists():
        age_hours = (datetime.now().timestamp() - path.stat().st_mtime) / 3600
        size = path.stat().st_size
        return {"name": name, "status": "ok", "size": size, "age_hours": round(age_hours, 1)}
    return {"name": name, "status": "missing", "size": 0, "age_hours": None}


def check_recent_buffer(memory_path):
    """Check if MEMORY.md has a ## Recent section and if items are stale."""
    if not memory_path.exists():
        return {"status": "error", "message": "MEMORY.md not found"}

    content = memory_path.read_text()
    if "## Recent" not in content:
        return {"status": "warning", "message": "No ## Recent buffer in MEMORY.md"}

    # Check for stale items (older than 48h)
    lines = content.split("\n")
    in_recent = False
    stale_items = []
    for line in lines:
        if line.strip() == "## Recent":
            in_recent = True
            continue
        if in_recent and line.startswith("## "):
            break
        if in_recent and line.startswith("- **"):
            # Try to extract date
            try:
                date_str = line.split("**")[1].rstrip(":")
                item_date = datetime.strptime(date_str, "%Y-%m-%d")
                if datetime.now() - item_date > timedelta(hours=48):
                    stale_items.append(line.strip()[:80])
            except (IndexError, ValueError):
                pass

    if stale_items:
        return {"status": "warning", "message": f"{len(stale_items)} stale items in ## Recent (>48h)", "stale": stale_items}
    return {"status": "ok", "message": "## Recent buffer healthy"}


def check_memory_size(memory_path):
    """Check MEMORY.md size."""
    if not memory_path.exists():
        return {"status": "error", "words": 0}
    content = memory_path.read_text()
    words = len(content.split())
    if words > 5000:
        return {"status": "warning", "words": words, "message": f"MEMORY.md is {words} words — consider archiving completed items"}
    if words > 4000:
        return {"status": "info", "words": words, "message": f"MEMORY.md is {words} words — approaching recommended limit"}
    return {"status": "ok", "words": words}


def check_nightly_cron(agent_id):
    """Check if the nightly cron job ran successfully."""
    result = subprocess.run(
        f'openclaw cron list --json 2>/dev/null',
        shell=True, capture_output=True, text=True
    )
    try:
        data = json.loads(result.stdout)
        jobs = data.get("jobs", data) if isinstance(data, dict) else data
        if not isinstance(jobs, list):
            return {"status": "warning", "message": "Could not parse cron job list"}
        for job in jobs:
            if "Nightly" in job.get("name", "") and job.get("agentId") == agent_id:
                state = job.get("state", {})
                last_status = state.get("lastStatus", "unknown")
                last_run = state.get("lastRunAtMs")
                if last_run:
                    hours_ago = (datetime.now().timestamp() * 1000 - last_run) / 3600000
                    return {
                        "status": "ok" if last_status == "ok" else "error",
                        "last_status": last_status,
                        "hours_ago": round(hours_ago, 1),
                        "job_id": job.get("id"),
                    }
                return {"status": "info", "message": "Nightly job exists but hasn't run yet"}
    except (json.JSONDecodeError, KeyError, TypeError):
        pass
    return {"status": "warning", "message": "No nightly cron job found"}


def check_daily_file(memory_dir):
    """Check if today's daily file exists."""
    today = datetime.now().strftime("%Y-%m-%d")
    daily_path = memory_dir / f"{today}.md"
    if daily_path.exists():
        return {"status": "ok", "file": str(daily_path)}
    return {"status": "info", "message": f"No daily file for {today} yet (created on first activity)"}


def main():
    parser = argparse.ArgumentParser(description="Memory Lifecycle Health Check")
    parser.add_argument("--workspace", default=os.getcwd(), help="Workspace directory")
    parser.add_argument("--agent", default="main", help="Agent ID")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    memory_dir = workspace / "memory"

    results = {
        "timestamp": datetime.now().isoformat(),
        "agent": args.agent,
        "checks": {}
    }

    # Check structured files
    structured_files = ["people.md", "decisions.md", "lessons.md", "commitments.md"]
    file_checks = []
    for f in structured_files:
        file_checks.append(check_file_exists(memory_dir / f, f))
    results["checks"]["structured_files"] = file_checks

    # Check Recent buffer
    results["checks"]["recent_buffer"] = check_recent_buffer(workspace / "MEMORY.md")

    # Check MEMORY.md size
    results["checks"]["memory_size"] = check_memory_size(workspace / "MEMORY.md")

    # Check nightly cron
    results["checks"]["nightly_cron"] = check_nightly_cron(args.agent)

    # Check today's daily file
    results["checks"]["daily_file"] = check_daily_file(memory_dir)

    # Overall status
    all_statuses = []
    for check in results["checks"].values():
        if isinstance(check, list):
            all_statuses.extend(c.get("status", "ok") for c in check)
        else:
            all_statuses.append(check.get("status", "ok"))

    if "error" in all_statuses:
        results["overall"] = "error"
    elif "warning" in all_statuses:
        results["overall"] = "warning"
    else:
        results["overall"] = "healthy"

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"\n🧠 Memory Lifecycle Health Check")
        print(f"{'=' * 50}")
        print(f"Agent: {args.agent} | Status: {results['overall'].upper()}\n")

        print("📁 Structured Files:")
        for f in file_checks:
            icon = "✅" if f["status"] == "ok" else "❌"
            extra = f" ({f['size']} bytes, {f['age_hours']}h old)" if f["status"] == "ok" else ""
            print(f"  {icon} {f['name']}{extra}")

        print(f"\n📋 Recent Buffer: {results['checks']['recent_buffer']['status'].upper()}")
        print(f"  {results['checks']['recent_buffer'].get('message', '')}")

        mem = results["checks"]["memory_size"]
        print(f"\n📏 MEMORY.md: {mem['words']} words {'⚠️' if mem['status'] == 'warning' else '✅'}")
        if mem.get("message"):
            print(f"  {mem['message']}")

        nightly = results["checks"]["nightly_cron"]
        print(f"\n🌙 Nightly Cron: {nightly['status'].upper()}")
        if "hours_ago" in nightly:
            print(f"  Last run: {nightly['hours_ago']}h ago (status: {nightly.get('last_status', 'unknown')})")
        elif "message" in nightly:
            print(f"  {nightly['message']}")

        daily = results["checks"]["daily_file"]
        icon = "✅" if daily["status"] == "ok" else "ℹ️"
        print(f"\n📅 Daily File: {icon} {daily.get('file', daily.get('message', ''))}")
        print()


if __name__ == "__main__":
    main()
