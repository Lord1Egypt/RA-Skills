#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill Iteration Automation Script

Reads skill_improvement_feedback from .skill-iterations/, runs benchmarks
before and after applying improvements, and provides go/no-go recommendations.

This script automates the self-improvement loop defined in
research-retrospective-protocol.md.

Usage:
    # List pending improvements
    python scripts/iterate_skill.py --list

    # Run full iteration cycle for a specific feedback file
    python scripts/iterate_skill.py --apply 2026-06-28T103000-add-source-gate.json \
      --behavior-command 'python /path/to/judge.py --phase {phase} --skill {skill_dir} --output {output}'

    # Run with specific eval IDs only
    python scripts/iterate_skill.py --apply <file> --eval-ids 1,9,13 \
      --behavior-command 'python /path/to/judge.py --phase {phase} --skill {skill_dir} --output {output}'

    # Run with custom max iterations
    python scripts/iterate_skill.py --apply <file> --max-iterations 3 \
      --behavior-command 'python /path/to/judge.py --phase {phase} --skill {skill_dir} --output {output}'

Exit codes:
    0 = improvement recommended (benchmark improved or stable)
    1 = improvement not recommended (benchmark degraded)
    2 = error or no pending improvements
"""

import argparse
import json
import shlex
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path


# ── Constants ────────────────────────────────────────────────────────────────

SKILL_DIR = Path(__file__).parent.parent
ITERATIONS_DIR = SKILL_DIR / ".skill-iterations"
BENCHMARK_SCRIPT = SKILL_DIR.parent / "skill-forge" / "scripts" / "run_skill_benchmarks.py"
BENCHMARK_OUTPUT = SKILL_DIR / "evals" / "benchmark-results.json"
BENCHMARK_REPORT = SKILL_DIR / "evals" / "benchmark-report.md"
EVALS_FILE = SKILL_DIR / "evals" / "evals.json"

# Maximum iterations before forcing stop (safety guard)
DEFAULT_MAX_ITERATIONS = 3

# Iteration history file for tracking
ITERATION_HISTORY = ITERATIONS_DIR / "_history.json"


# ── Helpers ──────────────────────────────────────────────────────────────────


def load_feedback(filepath: str) -> dict:
    """Load a skill_improvement_feedback JSON file."""
    path = Path(filepath)
    if not path.is_absolute():
        path = ITERATIONS_DIR / filepath
    if not path.exists():
        print(f"Error: feedback file not found: {path}", file=sys.stderr)
        sys.exit(2)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def list_pending() -> list[dict]:
    """List all pending improvement feedback files."""
    if not ITERATIONS_DIR.exists():
        return []
    files = sorted(ITERATIONS_DIR.glob("*.json"))
    files = [f for f in files if f.name != "_history.json"]
    results = []
    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            results.append({
                "file": f.name,
                "top_fix": data.get("top_fix", "(unknown)"),
                "fix_type": data.get("fix_type", "(unknown)"),
                "rerun_evals": data.get("rerun_evals", False),
            })
        except (json.JSONDecodeError, KeyError):
            results.append({
                "file": f.name,
                "top_fix": "(parse error)",
                "fix_type": "(unknown)",
                "rerun_evals": False,
            })
    return results


def load_history() -> list[dict]:
    """Load iteration history for max_iterations tracking."""
    if ITERATION_HISTORY.exists():
        with open(ITERATION_HISTORY, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_history(history: list[dict]):
    """Save iteration history."""
    ITERATIONS_DIR.mkdir(parents=True, exist_ok=True)
    with open(ITERATION_HISTORY, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def count_iterations_for_fix(history: list[dict], top_fix: str) -> int:
    """Count how many iterations have been attempted for the same fix."""
    return sum(1 for h in history if h.get("top_fix") == top_fix)


def load_declared_eval_ids() -> list[int]:
    """Load the complete declared eval ID set for full-corpus evidence."""
    try:
        payload = json.loads(EVALS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise ValueError(f"unable to load declared eval IDs: {exc}") from exc
    raw_items = payload.get("evals") if isinstance(payload, dict) else None
    if not isinstance(raw_items, list):
        raise ValueError("evals/evals.json does not contain an evals list")
    ids = [item.get("id") for item in raw_items if isinstance(item, dict)]
    if (
        not ids
        or any(not isinstance(eval_id, int) for eval_id in ids)
        or len(ids) != len(set(ids))
    ):
        raise ValueError("declared eval IDs are empty, invalid, or duplicated")
    return ids


def run_behavior_command(
    command_template: str,
    phase: str,
    expected_eval_ids: list[int],
) -> dict:
    """Run an explicit behavioral evaluator and validate its result envelope.

    The command is argv-parsed (never run through a shell) and must write:
    ``{"executed": true, "items": [{"id": 1, "passed": true}, ...]}``.
    ``{phase}``, ``{skill_dir}``, ``{eval_ids}``, and ``{output}`` placeholders
    are supported. Evidence IDs must exactly match the requested eval set.
    """
    if "{output}" not in command_template:
        return {
            "pass_count": 0,
            "total_count": 0,
            "error": "--behavior-command must include the {output} placeholder",
        }
    try:
        command = shlex.split(command_template)
    except ValueError as exc:
        return {
            "pass_count": 0,
            "total_count": 0,
            "error": f"invalid --behavior-command: {exc}",
        }
    if not command:
        return {
            "pass_count": 0,
            "total_count": 0,
            "error": "--behavior-command is empty",
        }

    with tempfile.TemporaryDirectory(prefix="deep-research-behavior-") as temp_dir:
        output_path = Path(temp_dir) / f"{phase}-results.json"
        substitutions = {
            "{phase}": phase,
            "{skill_dir}": str(SKILL_DIR),
            "{eval_ids}": ",".join(str(eval_id) for eval_id in expected_eval_ids),
            "{output}": str(output_path),
        }
        argv = []
        for argument in command:
            for placeholder, value in substitutions.items():
                argument = argument.replace(placeholder, value)
            argv.append(argument)

        print(f"  Running behavioral evaluator ({phase}): {' '.join(argv)}")
        try:
            result = subprocess.run(
                argv,
                capture_output=True,
                text=True,
                timeout=300,
                cwd=str(SKILL_DIR.parent),
            )
        except subprocess.TimeoutExpired:
            return {
                "pass_count": 0,
                "total_count": 0,
                "error": f"behavioral evaluator timed out during {phase}",
            }
        except FileNotFoundError:
            return {
                "pass_count": 0,
                "total_count": 0,
                "error": f"behavioral evaluator command not found during {phase}",
            }
        if result.returncode != 0:
            return {
                "pass_count": 0,
                "total_count": 0,
                "error": (
                    f"behavioral evaluator exited {result.returncode} "
                    f"during {phase}"
                ),
            }
        if not output_path.exists():
            return {
                "pass_count": 0,
                "total_count": 0,
                "error": f"behavioral evaluator produced no {phase} results",
            }
        try:
            payload = json.loads(output_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            return {
                "pass_count": 0,
                "total_count": 0,
                "error": f"invalid behavioral results during {phase}: {exc}",
            }

    if not isinstance(payload, dict) or payload.get("executed") is not True:
        return {
            "pass_count": 0,
            "total_count": 0,
            "error": f"behavioral evaluator did not confirm execution during {phase}",
        }
    raw_items = payload.get("items")
    if not isinstance(raw_items, list):
        return {
            "pass_count": 0,
            "total_count": 0,
            "error": f"behavioral evaluator items are missing during {phase}",
        }
    if not raw_items or any(
        not isinstance(item, dict)
        for item in raw_items
    ):
        return {
            "pass_count": 0,
            "total_count": 0,
            "error": f"behavioral evaluator returned malformed items during {phase}",
        }
    items = [item for item in raw_items if not item.get("skipped", False)]
    if not items or any(
        not isinstance(item.get("id"), int)
        or not isinstance(item.get("passed"), bool)
        for item in items
    ):
        return {
            "pass_count": 0,
            "total_count": 0,
            "error": f"behavioral evaluator returned no valid assertions during {phase}",
        }
    actual_ids = [item["id"] for item in items]
    expected_ids = list(expected_eval_ids)
    duplicate_ids = sorted(
        {eval_id for eval_id in actual_ids if actual_ids.count(eval_id) > 1}
    )
    missing_ids = sorted(set(expected_ids) - set(actual_ids))
    unexpected_ids = sorted(set(actual_ids) - set(expected_ids))
    if duplicate_ids or missing_ids or unexpected_ids:
        return {
            "pass_count": 0,
            "total_count": 0,
            "error": (
                f"behavioral evaluator coverage mismatch during {phase}: "
                f"missing={missing_ids}, unexpected={unexpected_ids}, "
                f"duplicates={duplicate_ids}"
            ),
        }
    details = [
        {
            "id": item["id"],
            "passed": item["passed"],
            "category": item.get("category", ""),
        }
        for item in items
    ]
    return {
        "pass_count": sum(1 for item in details if item["passed"]),
        "total_count": len(details),
        "details": details,
        "evidence_source": "behavior-command",
    }


def run_benchmarks(
    eval_ids: list[int] | None = None,
    *,
    behavior_command: str | None = None,
    phase: str = "benchmark",
) -> dict:
    """Run skill benchmarks and return results.

    Only executable behavioral results may enter the iteration delta. Structural
    eval validity (``evals.items[].passed``) is deliberately excluded because it
    does not prove that the skill satisfied an expectation.
    """
    cmd = [
        sys.executable,
        str(BENCHMARK_SCRIPT),
        str(SKILL_DIR),
        "--pretty",
        "--output",
        str(BENCHMARK_OUTPUT),
        "--markdown-output",
        str(BENCHMARK_REPORT),
    ]

    # Note: run_skill_benchmarks.py may not support --eval-ids natively.
    # If eval_ids is provided, we note it for manual filtering.
    if eval_ids:
        print(
            f"  Note: --eval-ids {eval_ids} specified. "
            "Behavioral evidence must cover this exact ID set."
        )

    # A failed benchmark must never fall back to a result from an earlier run.
    for generated_path in (BENCHMARK_OUTPUT, BENCHMARK_REPORT):
        try:
            generated_path.unlink()
        except FileNotFoundError:
            pass

    print(f"  Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
            cwd=str(SKILL_DIR.parent),
        )
        if result.returncode != 0:
            print(f"  Benchmark exited with code {result.returncode}", file=sys.stderr)
            return {
                "pass_count": 0,
                "total_count": 0,
                "error": f"benchmark exited {result.returncode}",
            }
    except subprocess.TimeoutExpired:
        print("  Benchmark timed out after 300s", file=sys.stderr)
        return {"pass_count": 0, "total_count": 0, "error": "timeout"}
    except FileNotFoundError:
        print(f"  Benchmark script not found: {BENCHMARK_SCRIPT}", file=sys.stderr)
        return {"pass_count": 0, "total_count": 0, "error": "script not found"}

    if not BENCHMARK_OUTPUT.exists():
        return {"pass_count": 0, "total_count": 0, "error": "no results file"}

    try:
        with open(BENCHMARK_OUTPUT, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        return {
            "pass_count": 0,
            "total_count": 0,
            "error": f"invalid results file: {exc}",
        }

    if data.get("overall_passed") is not True:
        return {
            "pass_count": 0,
            "total_count": 0,
            "error": "benchmark overall gate failed",
        }

    if behavior_command:
        try:
            expected_eval_ids = eval_ids or load_declared_eval_ids()
        except ValueError as exc:
            return {
                "pass_count": 0,
                "total_count": 0,
                "error": str(exc),
            }
        return run_behavior_command(
            behavior_command,
            phase,
            expected_eval_ids,
        )

    blind = data.get("blind_audit", {})
    if not isinstance(blind, dict) or blind.get("executed") is not True:
        return {
            "pass_count": 0,
            "total_count": 0,
            "error": "behavioral results unavailable; manual or blind evaluation required",
        }

    items = [
        item
        for item in blind.get("items", [])
        if isinstance(item, dict) and not item.get("skipped", False)
    ]
    if not items:
        return {
            "pass_count": 0,
            "total_count": 0,
            "error": "behavioral results unavailable; no executable assertions",
        }

    details = [
        {
            "id": item.get("id"),
            "passed": item.get("passed") is True,
            "category": item.get("category", ""),
        }
        for item in items
    ]
    return {
        "pass_count": sum(1 for item in details if item["passed"]),
        "total_count": len(details),
        "details": details,
    }


def filter_results_by_eval_ids(results: dict, eval_ids: list[int]) -> dict:
    """Filter benchmark results to only show specified eval IDs."""
    if not eval_ids or "details" not in results:
        return results
    raw_details = results["details"]
    actual_ids = [
        detail.get("id")
        for detail in raw_details
        if isinstance(detail, dict)
    ]
    duplicate_ids = sorted(
        {
            eval_id
            for eval_id in actual_ids
            if isinstance(eval_id, int) and actual_ids.count(eval_id) > 1
        }
    )
    missing_ids = sorted(set(eval_ids) - set(actual_ids))
    if duplicate_ids or missing_ids:
        return {
            "pass_count": 0,
            "total_count": 0,
            "error": (
                "requested behavioral eval coverage is incomplete: "
                f"missing={missing_ids}, duplicates={duplicate_ids}"
            ),
        }
    details = [d for d in raw_details if d.get("id") in eval_ids]
    if not details:
        return {
            "pass_count": 0,
            "total_count": 0,
            "error": "requested behavioral eval coverage is empty",
        }
    passed = sum(1 for d in details if d.get("passed") is True)
    return {
        "pass_count": passed,
        "total_count": len(details),
        "details": details,
        "filtered": True,
    }


# ── Commands ─────────────────────────────────────────────────────────────────


def cmd_list():
    """List pending improvement feedback files."""
    pending = list_pending()
    if not pending:
        print("No pending improvements in .skill-iterations/")
        print(f"(directory: {ITERATIONS_DIR})")
        return 0

    print(f"Pending improvements ({len(pending)}):\n")
    for item in pending:
        print(f"  {item['file']}")
        print(f"    Fix: {item['top_fix']}")
        print(f"    Type: {item['fix_type']}")
        print(f"    Rerun evals: {item['rerun_evals']}")
        print()
    return 0


def cmd_apply(
    filepath: str,
    eval_ids: list[int] | None,
    max_iterations: int,
    behavior_command: str | None = None,
):
    """Run the full iteration cycle for a feedback file."""
    feedback = load_feedback(filepath)
    top_fix = feedback.get("top_fix", "(unknown)")
    fix_type = feedback.get("fix_type", "(unknown)")
    suggestion = feedback.get("suggestion", "")
    expected_dim = feedback.get("expected_dimension_improvement", "")
    feedback_eval_ids = feedback.get("rerun_eval_ids", [])

    # Merge eval IDs from CLI and feedback
    all_eval_ids = eval_ids or feedback_eval_ids or None

    # Max iterations safety check
    history = load_history()
    iteration_count = count_iterations_for_fix(history, top_fix)
    if iteration_count >= max_iterations:
        print(f"⚠️  Max iterations ({max_iterations}) reached for this fix.")
        print(f"    Previous attempts: {iteration_count}")
        print(f"    Fix: {top_fix}")
        print(f"\n    This fix has been attempted {iteration_count} times without success.")
        print(f"    Consider a different approach or accept the current state.")
        return 1

    if iteration_count > 0:
        print(f"ℹ️  This is attempt {iteration_count + 1}/{max_iterations} for this fix.")

    print("=" * 60)
    print("Skill Improvement Iteration")
    print("=" * 60)
    print(f"\n  Top fix: {top_fix}")
    print(f"  Type: {fix_type}")
    print(f"  Suggestion: {suggestion}")
    print(f"  Expected improvement: {expected_dim}")
    if all_eval_ids:
        print(f"  Eval IDs to check: {all_eval_ids}")
    print()

    # Step 1: Run baseline benchmark
    print("─" * 60)
    print("Step 1: Running baseline benchmark (before improvement)...")
    print("─" * 60)
    baseline = run_benchmarks(
        all_eval_ids,
        behavior_command=behavior_command,
        phase="baseline",
    )
    if all_eval_ids:
        baseline = filter_results_by_eval_ids(baseline, all_eval_ids)
    print(f"  Baseline: {baseline['pass_count']}/{baseline['total_count']} passed")
    if baseline.get("error"):
        print(f"  ❌ Error: {baseline['error']}")
        print("  Iteration aborted: a behavioral baseline is required before applying changes.")
        return 2
    print()

    # Step 2: Prompt user to apply the improvement
    print("─" * 60)
    print("Step 2: Apply the improvement")
    print("─" * 60)
    print(f"\n  Please apply the following change to the skill files:")
    print(f"  {suggestion}")
    print(f"\n  Press Enter when done (or 'skip' to abort)...")
    try:
        user_input = input().strip()
    except EOFError:
        user_input = "skip"

    if user_input.lower() == "skip":
        print("\n  Aborted by user.")
        return 2

    # Step 3: Run post-improvement benchmark
    print("\n" + "─" * 60)
    print("Step 3: Running post-improvement benchmark...")
    print("─" * 60)
    post = run_benchmarks(
        all_eval_ids,
        behavior_command=behavior_command,
        phase="post",
    )
    if all_eval_ids:
        post = filter_results_by_eval_ids(post, all_eval_ids)
    print(f"  Post: {post['pass_count']}/{post['total_count']} passed")
    if post.get("error"):
        print(f"  ❌ Error: {post['error']}")
        print("  Comparison aborted: post-change behavioral evidence is unavailable.")
        return 2
    print()

    # Step 4: Compare and recommend
    print("─" * 60)
    print("Step 4: Comparison")
    print("─" * 60)
    baseline_pass = baseline.get("pass_count", 0)
    post_pass = post.get("pass_count", 0)
    delta = post_pass - baseline_pass

    if delta > 0:
        verdict = "✅ GO — improvement detected"
        recommendation = "Apply and update VERSION."
    elif delta == 0:
        verdict = "🟡 HOLD — no change detected"
        recommendation = (
            "Check if the improvement targets a dimension not covered by benchmarks. "
            "Consider adding a new eval case if needed."
        )
    else:
        verdict = "🔴 NO-GO — regression detected"
        recommendation = "Roll back the change and record the failure."

    print(f"\n  Baseline: {baseline_pass}/{baseline.get('total_count', 0)}")
    print(f"  Post:     {post_pass}/{post.get('total_count', 0)}")
    print(f"  Delta:    {'+' if delta >= 0 else ''}{delta}")
    print(f"\n  Verdict: {verdict}")
    print(f"  Recommendation: {recommendation}")

    # Step 5: Record in history
    history_entry = {
        "timestamp": datetime.now().isoformat(),
        "top_fix": top_fix,
        "fix_type": fix_type,
        "suggestion": suggestion,
        "baseline_pass": baseline_pass,
        "baseline_total": baseline.get("total_count", 0),
        "post_pass": post_pass,
        "post_total": post.get("total_count", 0),
        "delta": delta,
        "verdict": verdict,
        "iteration_number": iteration_count + 1,
    }
    history.append(history_entry)
    save_history(history)
    print(f"\n  Recorded to: {ITERATION_HISTORY}")

    # Show per-eval comparison if details available
    if "details" in baseline and "details" in post:
        print("\n  Per-eval comparison:")
        baseline_map = {d["id"]: d.get("passed") for d in baseline["details"]}
        post_map = {d["id"]: d.get("passed") for d in post["details"]}
        all_ids = sorted(set(baseline_map.keys()) | set(post_map.keys()))
        for eid in all_ids:
            b_pass = baseline_map.get(eid)
            p_pass = post_map.get(eid)
            b = "PASS" if b_pass else ("FAIL" if b_pass is False else "?")
            p = "PASS" if p_pass else ("FAIL" if p_pass is False else "?")
            marker = ""
            if b == "PASS" and p == "FAIL":
                marker = " ⚠️ REGRESSION"
            elif b == "FAIL" and p == "PASS":
                marker = " ✅ FIXED"
            print(f"    Eval {eid}: {b} → {p}{marker}")

    print()
    return 0 if delta >= 0 else 1


# ── Main ─────────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Automate the skill self-improvement loop for deep-research-forge."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--list",
        action="store_true",
        help="List pending improvement feedback files",
    )
    group.add_argument(
        "--apply",
        metavar="FILE",
        help="Apply and benchmark a specific feedback file",
    )
    parser.add_argument(
        "--eval-ids",
        type=str,
        default=None,
        help="Comma-separated eval IDs to focus on (e.g., 1,9,13)",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=DEFAULT_MAX_ITERATIONS,
        help=f"Maximum iterations for the same fix (default: {DEFAULT_MAX_ITERATIONS})",
    )
    parser.add_argument(
        "--behavior-command",
        default=None,
        help=(
            "Explicit evaluator command for LLM behavior evidence. It must include "
            "{output}; optional placeholders: {phase}, {skill_dir}, {eval_ids}. "
            "The command must write one unique result for every requested eval ID: "
            "{\"executed\":true,\"items\":[{\"id\":1,\"passed\":true}]}."
        ),
    )
    args = parser.parse_args()

    if args.list:
        return cmd_list()

    if args.apply:
        eval_ids = None
        if args.eval_ids:
            try:
                eval_ids = [int(x.strip()) for x in args.eval_ids.split(",")]
            except ValueError:
                print("Error: --eval-ids must be comma-separated integers", file=sys.stderr)
                return 2
        return cmd_apply(
            args.apply,
            eval_ids,
            args.max_iterations,
            behavior_command=args.behavior_command,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
