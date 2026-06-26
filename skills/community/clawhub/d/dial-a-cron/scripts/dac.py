#!/usr/bin/env python3
"""
Dial-a-Cron — Main CLI
Unified interface for managing smart cron state, diffs, and routing.

Usage:
    python dac.py status                     # Show all job statuses
    python dac.py status <job-id>            # Show one job
    python dac.py preflight <job-id>         # Pre-run check (outputs DAC_CONTEXT)
    python dac.py finish <job-id> --status ok --output "..."  # Post-run
    python dac.py resume <job-id>            # Resume paused job
    python dac.py init <job-id>              # Create blank job config
    python dac.py budget                     # Monthly token budget report
    python dac.py test-diff <job-id>         # Test diff engine for a job
"""

import json
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone

# Ensure scripts dir is in path
sys.path.insert(0, str(Path(__file__).parent))

from state import CronState, list_all_jobs
from diff import DiffEngine
from preflight import run_preflight, run_finish

JOBS_DIR = os.environ.get("DAC_JOBS_DIR", str(Path(__file__).parent.parent / "jobs"))
STATE_DIR = os.environ.get("DAC_STATE_DIR", str(Path(__file__).parent.parent / "state"))


def cmd_status(args):
    """Show job statuses."""
    if args.job_id:
        s = CronState(args.job_id)
        s.show()
    else:
        jobs = list_all_jobs()
        if not jobs:
            print("No jobs tracked. Use 'dac init <job-id>' to create one.")
            return
        print(f"{'Job ID':<30} {'Status':<8} {'Errors':<7} {'Heal':<8} {'Tokens/Mo':<12} {'Last Run':<20}")
        print("-" * 95)
        for j in jobs:
            d = j.data
            last_run = d.get("lastRunAt", "never")
            if last_run and last_run != "never":
                last_run = last_run[:19]
            paused = " [PAUSED]" if d.get("paused") else ""
            print(f"{j.job_id:<30} {d.get('lastStatus', '?'):<8} {d.get('consecutiveErrors', 0):<7} "
                  f"{j.get_heal_level():<8} {d.get('monthlyTokens', 0):>9,}   {last_run}{paused}")


def cmd_preflight(args):
    """Run preflight for a job."""
    sys.exit(run_preflight(args.job_id))


def cmd_finish(args):
    """Finish a job run."""
    carry = json.loads(args.carry) if args.carry else None
    run_finish(args.job_id, args.status or "ok", args.output, args.tokens, carry)


def cmd_resume(args):
    """Resume a paused job."""
    s = CronState(args.job_id)
    if not s.data.get("paused"):
        print(f"Job '{args.job_id}' is not paused.")
        return
    s.resume()


def cmd_init(args):
    """Create a blank job config."""
    Path(JOBS_DIR).mkdir(parents=True, exist_ok=True)
    job_path = Path(JOBS_DIR) / f"{args.job_id}.json"
    if job_path.exists():
        print(f"Job config already exists: {job_path}")
        return
    config = {
        "jobId": args.job_id,
        "description": "",
        "skipIfNoDiff": False,
        "diffs": [],
        "routes": [
            {"to": "log", "channel": "log", "when": ["silent", "log", "info"]},
            {"to": "bobby", "channel": "telegram", "when": ["alert", "urgent"]}
        ],
        "budget": {
            "maxTokensPerRun": 50000,
            "maxTokensPerMonth": 500000,
            "onBudgetExceeded": "downgrade",
            "downgradeModel": "grok-mini"
        }
    }
    with open(job_path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"Created: {job_path}")
    print("Edit the file to add diffs, routes, and budget settings.")


def cmd_budget(args):
    """Monthly token budget report."""
    jobs = list_all_jobs()
    if not jobs:
        print("No jobs tracked.")
        return
    current_month = datetime.now(timezone.utc).strftime("%Y-%m")
    total = 0
    print(f"\nToken Budget Report — {current_month}\n")
    print(f"{'Job ID':<30} {'Tokens/Mo':<12} {'Total':<12} {'Runs':<8}")
    print("-" * 65)
    for j in jobs:
        d = j.data
        monthly = d.get("monthlyTokens", 0)
        total_all = d.get("totalTokens", 0)
        runs = d.get("runCount", 0)
        total += monthly
        print(f"{j.job_id:<30} {monthly:>9,}   {total_all:>9,}   {runs:>5}")
    print("-" * 65)
    print(f"{'TOTAL':<30} {total:>9,}")
    print()


def cmd_test_diff(args):
    """Test diff engine for a job."""
    config_path = Path(JOBS_DIR) / f"{args.job_id}.json"
    if not config_path.exists():
        print(f"No job config: {config_path}")
        return
    with open(config_path) as f:
        config = json.load(f)
    diff_specs = config.get("diffs", [])
    if not diff_specs:
        print("No diffs configured for this job.")
        return
    state = CronState(args.job_id)
    prev_hashes = state.get_carry().get("_dac_hashes", {})
    engine = DiffEngine(args.job_id, prev_hashes)
    result = engine.run(diff_specs)
    print(f"Has changes: {result.has_changes}")
    print(f"New hash: {result.new_hash}")
    print()
    print(result.to_prompt_block())


def main():
    parser = argparse.ArgumentParser(
        description="Dial-a-Cron — Intelligent Cron Orchestration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command")

    # status
    p = sub.add_parser("status", help="Show job statuses")
    p.add_argument("job_id", nargs="?", help="Specific job ID")

    # preflight
    p = sub.add_parser("preflight", help="Run preflight checks")
    p.add_argument("job_id", help="Job ID")

    # finish
    p = sub.add_parser("finish", help="Finish a job run")
    p.add_argument("job_id", help="Job ID")
    p.add_argument("--status", choices=["ok", "error", "noop"])
    p.add_argument("--output", default="")
    p.add_argument("--tokens", type=int, default=0)
    p.add_argument("--carry", help="JSON carry data")

    # resume
    p = sub.add_parser("resume", help="Resume a paused job")
    p.add_argument("job_id", help="Job ID")

    # init
    p = sub.add_parser("init", help="Create blank job config")
    p.add_argument("job_id", help="Job ID")

    # budget
    sub.add_parser("budget", help="Monthly token budget report")

    # test-diff
    p = sub.add_parser("test-diff", help="Test diff engine for a job")
    p.add_argument("job_id", help="Job ID")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    {
        "status": cmd_status,
        "preflight": cmd_preflight,
        "finish": cmd_finish,
        "resume": cmd_resume,
        "init": cmd_init,
        "budget": cmd_budget,
        "test-diff": cmd_test_diff,
    }[args.command](args)


if __name__ == "__main__":
    main()
