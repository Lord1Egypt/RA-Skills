#!/usr/bin/env python3
"""Cleanup utility for legacy or orphaned Chronos cron jobs."""
import argparse
import json
import sqlite3
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.paths import OPENCLAW_BIN, TODO_DB
from core.openclaw_cron import build_cron_remove_command

CHRONOS_PREFIXES = ("task_reminder_", "reminder_immediate_")


def is_chronos_job(job: dict) -> bool:
    return str(job.get("name") or "").startswith(CHRONOS_PREFIXES)


def is_legacy_bad_job(job: dict) -> bool:
    if not is_chronos_job(job):
        return False
    delivery = job.get("delivery") or {}
    state = job.get("state") or {}
    missing_explicit_to = delivery.get("mode") == "announce" and not delivery.get("to")
    heartbeat_error = "@heartbeat" in str(state.get("lastError") or "")
    return missing_explicit_to or heartbeat_error


def load_existing_reminder_job_ids() -> set[str]:
    if not TODO_DB.exists():
        return set()

    conn = sqlite3.connect(str(TODO_DB))
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT reminder_job_id FROM periodic_occurrences WHERE reminder_job_id IS NOT NULL AND reminder_job_id != ''"
        )
        return {row[0] for row in cur.fetchall()}
    except sqlite3.Error:
        return set()
    finally:
        conn.close()


def is_orphaned_job(job: dict, known_job_ids: set[str]) -> bool:
    if not is_chronos_job(job):
        return False
    return str(job.get("name") or "") not in known_job_ids


def classify_jobs(jobs: list[dict], known_job_ids: set[str]) -> list[dict]:
    candidates = []
    for job in jobs:
        reasons = []
        if is_legacy_bad_job(job):
            reasons.append("legacy-bad-delivery")
        if is_orphaned_job(job, known_job_ids):
            reasons.append("orphaned-db-reference")
        if reasons:
            candidates.append(
                {
                    "id": job.get("id"),
                    "name": job.get("name"),
                    "enabled": job.get("enabled"),
                    "reasons": reasons,
                }
            )
    return candidates


def load_cron_jobs() -> list[dict]:
    result = subprocess.run(
        [OPENCLAW_BIN, "cron", "list", "--all", "--json"],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "failed to list cron jobs")
    payload = json.loads(result.stdout)
    return payload.get("jobs", [])


def remove_jobs(candidates: list[dict]) -> list[str]:
    removed = []
    for candidate in candidates:
        result = subprocess.run(
            build_cron_remove_command(candidate["id"]),
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        if result.returncode == 0:
            removed.append(candidate["id"])
        else:
            print(f"Failed to remove {candidate['name']} ({candidate['id']}): {result.stderr.strip()}")
    return removed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Cleanup legacy/orphaned Chronos cron jobs")
    parser.add_argument("--apply", action="store_true", help="Actually remove candidates (default: dry-run)")
    parser.add_argument("--json", action="store_true", help="Output JSON summary")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    jobs = load_cron_jobs()
    known_job_ids = load_existing_reminder_job_ids()
    candidates = classify_jobs(jobs, known_job_ids)

    summary = {
        "mode": "apply" if args.apply else "dry-run",
        "total_jobs": len(jobs),
        "candidate_count": len(candidates),
        "candidates": candidates,
    }

    if args.apply and candidates:
        summary["removed_ids"] = remove_jobs(candidates)

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"Chronos legacy cron cleanup ({summary['mode']})")
        print(f"total_jobs: {summary['total_jobs']}")
        print(f"candidate_count: {summary['candidate_count']}")
        for candidate in candidates:
            reasons = ",".join(candidate["reasons"])
            print(f"- {candidate['name']} [{candidate['id']}] enabled={candidate['enabled']} reasons={reasons}")
        if args.apply:
            print(f"removed: {len(summary.get('removed_ids', []))}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
