#!/usr/bin/env python3
"""
Dial-a-Cron — Preflight Runner
The entry point for any Dial-a-Cron wrapped cron job.

This script:
1. Loads job config from jobs/<job-id>.json
2. Checks state — skip if paused
3. Runs the diff engine — skip if no changes (when skipIfNoDiff: true)
4. Outputs a context block for injection into the LLM prompt
5. Sets environment variables for the cron to use

Usage (from OpenClaw cron prompt):
    Run this at the start: python preflight.py <job-id>
    If it exits non-zero, skip the main cron task.
    Use $DAC_CONTEXT in your prompt.
    When done, run: python preflight.py <job-id> --finish --status ok --output "..."
"""

import json
import os
import sys
import argparse
from pathlib import Path

# Allow import from same dir
sys.path.insert(0, str(Path(__file__).parent))

from state import CronState
from diff import DiffEngine
from router import DeliveryRouter, RoutingSpec, evaluate_severity

JOBS_DIR = os.environ.get("DAC_JOBS_DIR", str(Path(__file__).parent.parent / "jobs"))


def load_job_config(job_id: str) -> dict:
    """Load job config from jobs/<job-id>.json"""
    path = Path(JOBS_DIR) / f"{job_id}.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


def run_preflight(job_id: str) -> int:
    """Run preflight checks. Returns 0 (proceed) or non-zero (skip)."""
    state = CronState(job_id)
    config = load_job_config(job_id)

    # Check if paused
    if state.should_skip():
        print(f"DAC_SKIP=true", flush=True)
        return 1

    # Get heal level
    heal = state.get_heal_level()
    carry = state.get_carry()

    # Run diff engine if specs defined
    diff_specs = config.get("diffs", [])
    prev_hashes = carry.get("_dac_hashes", {})
    diff_result = None
    skip_if_no_diff = config.get("skipIfNoDiff", False)

    if diff_specs:
        engine = DiffEngine(job_id, prev_hashes)
        diff_result = engine.run(diff_specs)

        if skip_if_no_diff and not diff_result.has_changes:
            state.start()
            state.finish(status="noop", output="No changes detected — skipped")
            print(f"DAC_SKIP=true", flush=True)
            print(f"DAC_REASON=no_diff", flush=True)
            return 2

    # Start the run
    state.start()

    # Build context block for LLM prompt injection
    context_lines = [
        f"## Dial-a-Cron Context: {job_id}",
        f"- Run #{state.data['runCount']}",
        f"- Heal level: {heal}",
        f"- Consecutive errors: {state.get_consecutive_errors()}",
    ]

    if carry:
        relevant_carry = {k: v for k, v in carry.items() if not k.startswith("_")}
        if relevant_carry:
            context_lines.append(f"- Previous run data: {json.dumps(relevant_carry)}")

    if diff_result and diff_result.has_changes:
        context_lines.append("")
        context_lines.append(diff_result.to_prompt_block())

    if heal == "minimal":
        context_lines.append("\n⚠️  MINIMAL MODE: Skip optional steps. Focus on core task only.")
    elif heal == "pause":
        context_lines.append("\n🚨 CRITICAL: Next error will auto-pause this job. Fix the issue.")

    context = "\n".join(context_lines)

    # Output for shell consumption
    print(f"DAC_CONTEXT<<EOF", flush=True)
    print(context, flush=True)
    print(f"EOF", flush=True)
    print(f"DAC_JOB_ID={job_id}", flush=True)
    print(f"DAC_HEAL_LEVEL={heal}", flush=True)
    print(f"DAC_RUN_COUNT={state.data['runCount']}", flush=True)
    if diff_result:
        print(f"DAC_HAS_CHANGES={'true' if diff_result.has_changes else 'false'}", flush=True)
        print(f"DAC_NEW_HASH={diff_result.new_hash}", flush=True)

    return 0


def run_finish(job_id: str, status: str, output: str, tokens: int, carry_extra: dict = None):
    """Finish a cron run and route output."""
    state = CronState(job_id)
    config = load_job_config(job_id)

    # Merge carry
    prev_carry = state.get_carry()
    if carry_extra:
        prev_carry.update(carry_extra)

    # Update diff hashes in carry if available
    new_hash = os.environ.get("DAC_NEW_HASH")
    if new_hash:
        prev_carry["_dac_last_hash"] = new_hash

    state.finish(
        status=status,
        output=output,
        tokens=tokens,
        carry=prev_carry,
    )

    # Route output
    route_specs_raw = config.get("routes", [
        {"to": "log", "when": ["silent", "log", "info", "alert", "urgent"]}
    ])
    specs = [RoutingSpec(**s) for s in route_specs_raw]
    router = DeliveryRouter(specs, job_id=job_id)

    severity = evaluate_severity(output, errors=state.get_consecutive_errors())
    result = router.route(severity, output[:200], output)

    print(f"[dial-a-cron] {state.summary()}")
    print(f"[dial-a-cron] Routed → {result.routed_to}")

    # Exit non-zero if paused (auto-heal triggered)
    if state.data.get("paused"):
        sys.exit(2)


def main():
    parser = argparse.ArgumentParser(description="Dial-a-Cron Preflight")
    parser.add_argument("job_id", help="Job ID")
    parser.add_argument("--finish", action="store_true", help="Finish mode (post-run)")
    parser.add_argument("--status", choices=["ok", "error", "noop"], help="Run status")
    parser.add_argument("--output", default="", help="Run output/summary")
    parser.add_argument("--tokens", type=int, default=0, help="Tokens used")
    parser.add_argument("--carry", help="JSON carry data to merge")
    args = parser.parse_args()

    if args.finish:
        carry = json.loads(args.carry) if args.carry else None
        run_finish(args.job_id, args.status or "ok", args.output, args.tokens, carry)
    else:
        sys.exit(run_preflight(args.job_id))


if __name__ == "__main__":
    main()
