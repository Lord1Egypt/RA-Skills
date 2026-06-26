#!/usr/bin/env python3
"""Autoloop controller — wraps improvement-orchestrator in a persistent loop.

Supports three modes:
  single-run  — one iteration then exit
  continuous  — loop with cooldown until termination condition
  scheduled   — exit after each run (cron triggers next)

Termination conditions (OR logic):
  1. max_iterations reached
  2. cost_cap exceeded
  3. score plateau detected
  4. oscillation detected
  5. consecutive errors exceeded (circuit breaker)
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import traceback
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Shared-lib import (same pattern as orchestrate.py)
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from lib.common import read_json, utc_now_iso, write_json

# Sibling modules
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from convergence import compute_weighted_score, detect_oscillation, detect_plateau
# cost_tracker available for future use

# ---------------------------------------------------------------------------
# Orchestrator path
# ---------------------------------------------------------------------------

ORCHESTRATOR_SCRIPT = _REPO_ROOT / "skills" / "improvement-orchestrator" / "scripts" / "orchestrate.py"

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

SCHEMA_VERSION = "1.0"


@dataclass
class AutoloopState:
    """Serializable state for cross-session persistence."""

    schema_version: str = SCHEMA_VERSION
    target: str = ""
    started_at: str = ""
    iterations_completed: int = 0
    max_iterations: int = 5
    total_cost_usd: float = 0.0
    max_cost_usd: float = 50.0
    current_scores: dict[str, float] = field(default_factory=dict)
    score_history: list[dict[str, Any]] = field(default_factory=list)
    plateau_counter: int = 0
    plateau_window: int = 3
    status: str = "running"
    last_failure_trace: str | None = None
    consecutive_errors: int = 0
    max_consecutive_errors: int = 3
    cooldown_minutes: int = 30
    next_run_at: str | None = None

    # -- persistence --------------------------------------------------------

    @classmethod
    def load(cls, path: Path) -> "AutoloopState":
        """Load from JSON or create a fresh instance if file is missing."""
        if path.exists():
            data = read_json(path)
            known_fields = {f.name for f in cls.__dataclass_fields__.values()}
            filtered = {k: v for k, v in data.items() if k in known_fields}
            return cls(**filtered)
        return cls(started_at=utc_now_iso())

    def save(self, path: Path) -> None:
        write_json(path, asdict(self))


# ---------------------------------------------------------------------------
# Termination logic
# ---------------------------------------------------------------------------


def should_stop(state: AutoloopState) -> tuple[bool, str]:
    """Check all termination conditions. Returns (should_stop, reason)."""
    if state.iterations_completed >= state.max_iterations:
        return True, f"max_iterations reached ({state.iterations_completed}/{state.max_iterations})"

    if state.total_cost_usd >= state.max_cost_usd:
        return True, f"cost_cap exceeded (${state.total_cost_usd:.2f} >= ${state.max_cost_usd:.2f})"

    if detect_plateau(state.score_history, window=state.plateau_window):
        return True, f"plateau detected (no improvement in last {state.plateau_window} iterations)"

    if detect_oscillation(state.score_history, window=4):
        return True, "oscillation detected (keep-reject alternating pattern)"

    if state.consecutive_errors >= state.max_consecutive_errors:
        return True, f"consecutive_errors exceeded ({state.consecutive_errors}/{state.max_consecutive_errors})"

    return False, ""


# ---------------------------------------------------------------------------
# Single iteration
# ---------------------------------------------------------------------------


def run_single_iteration(
    state: AutoloopState,
    target: str,
    state_root: str,
    dry_run: bool = False,
) -> tuple[AutoloopState, dict[str, Any]]:
    """Run one improvement-orchestrator pipeline iteration.

    Returns updated state and the pipeline result dict.
    """
    iteration = state.iterations_completed + 1
    iter_start = time.monotonic()
    started_at = utc_now_iso()

    result: dict[str, Any]

    if dry_run:
        # Simulate a successful keep with dummy scores
        result = {
            "target": target,
            "attempts": 1,
            "max_retries": 3,
            "final_decision": "keep",
            "final_candidate_id": f"dry-run-{iteration}",
            "final_artifact_path": None,
        }
        duration = 0.1
        cost = 0.0
    else:
        # Subprocess isolation — do not import orchestrate directly
        cmd = [
            sys.executable,
            str(ORCHESTRATOR_SCRIPT),
            "--target", str(target),
            "--state-root", str(state_root),
            "--auto",
        ]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        except subprocess.TimeoutExpired:
            state.last_failure_trace = "Orchestrator subprocess timed out after 3600s"
            state.status = "error"
            state.consecutive_errors += 1
            result = {
                "target": target,
                "attempts": 0,
                "max_retries": 0,
                "final_decision": "error",
                "final_candidate_id": None,
                "final_artifact_path": None,
                "error": state.last_failure_trace,
            }
            return state, result

        duration = time.monotonic() - iter_start

        if proc.returncode != 0:
            state.last_failure_trace = proc.stderr.strip() or proc.stdout.strip()
            state.status = "error"
            state.consecutive_errors += 1
            result = {
                "target": target,
                "attempts": 0,
                "max_retries": 0,
                "final_decision": "error",
                "final_candidate_id": None,
                "final_artifact_path": None,
                "error": state.last_failure_trace,
            }
            return state, result

        # Parse the pipeline result — orchestrate.py prints summary to stdout
        # Try to find JSON output; fall back to parsing text
        result = _parse_orchestrator_output(proc.stdout, target)
        cost = _estimate_cost(duration)

    decision = result.get("final_decision", "reject")

    # Compute weighted score from learner output if available
    scores = _load_latest_scores(state_root)
    weighted = compute_weighted_score(scores) if scores else 0.0

    # Update score history
    history_entry = {
        "iteration": iteration,
        "weighted_score": weighted,
        "decision": decision,
        "scores": scores,
        "timestamp": utc_now_iso(),
    }
    state.score_history.append(history_entry)
    state.current_scores = scores

    # Update plateau counter
    if len(state.score_history) >= 2:
        prev_best = max(h["weighted_score"] for h in state.score_history[:-1])
        if weighted > prev_best:
            state.plateau_counter = 0
        else:
            state.plateau_counter += 1
    else:
        state.plateau_counter = 0

    # Update cost
    cost_val = cost if not dry_run else 0.0
    state.total_cost_usd += cost_val
    state.iterations_completed = iteration
    state.last_failure_trace = None
    state.consecutive_errors = 0

    # Append to iteration log
    log_entry = {
        "iteration": iteration,
        "started_at": started_at,
        "finished_at": utc_now_iso(),
        "decision": decision,
        "weighted_score": weighted,
        "cost_usd": round(cost_val, 4),
        "duration_seconds": round(duration, 1),
        "candidate_id": result.get("final_candidate_id"),
        "artifact_path": result.get("final_artifact_path"),
    }
    _append_iteration_log(state_root, log_entry)

    return state, result


def _parse_orchestrator_output(stdout: str, target: str) -> dict[str, Any]:
    """Best-effort parse of orchestrate.py stdout."""
    # Try to extract structured data from the summary lines
    lines = stdout.strip().split("\n")
    result: dict[str, Any] = {"target": target}

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("Final Decision:"):
            result["final_decision"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("Candidate:"):
            val = stripped.split(":", 1)[1].strip()
            result["final_candidate_id"] = val if val != "N/A" else None
        elif stripped.startswith("Artifact:"):
            val = stripped.split(":", 1)[1].strip()
            result["final_artifact_path"] = val if val != "N/A" else None
        elif stripped.startswith("Attempts:"):
            parts = stripped.split(":", 1)[1].strip().split("/")
            if len(parts) == 2:
                result["attempts"] = int(parts[0])
                result["max_retries"] = int(parts[1])

    result.setdefault("final_decision", "reject")
    result.setdefault("final_candidate_id", None)
    result.setdefault("final_artifact_path", None)
    result.setdefault("attempts", 0)
    result.setdefault("max_retries", 3)
    return result


def _estimate_cost(duration_seconds: float) -> float:
    """Rough cost estimate based on duration. Placeholder heuristic."""
    # ~$0.10 per minute of LLM time as rough estimate
    return round(duration_seconds / 60.0 * 0.10, 4)


def _load_latest_scores(state_root: str) -> dict[str, float]:
    """Try to load latest learner scores from the state directory."""
    state_dir = Path(state_root)
    # Look for the most recent learner output
    learner_dir = state_dir / "learner"
    if not learner_dir.exists():
        return {}
    candidates = sorted(learner_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not candidates:
        return {}
    try:
        data = read_json(candidates[0])
        # Extract dimension scores from learner output (final_scores or legacy dimensions)
        dimensions = data.get("final_scores", data.get("dimensions", {}))
        return {k: v.get("score", 0.0) if isinstance(v, dict) else float(v) for k, v in dimensions.items()}
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        return {}


def _append_iteration_log(state_root: str, entry: dict) -> None:
    """Append one JSON line to iteration_log.jsonl."""
    log_path = Path(state_root) / "iteration_log.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Autoloop controller — persistent improvement loop",
    )
    parser.add_argument("--target", required=True, help="Target skill/file path")
    parser.add_argument("--state-root", required=True, help="State directory root")
    parser.add_argument("--max-iterations", type=int, default=5, help="Max iterations (default: 5)")
    parser.add_argument("--max-cost", type=float, default=50.0, help="Cost cap in USD (default: 50.0)")
    parser.add_argument("--plateau-window", type=int, default=3, help="Plateau detection window (default: 3)")
    parser.add_argument("--cooldown-minutes", type=int, default=30, help="Cooldown between iterations in minutes (default: 30)")
    parser.add_argument(
        "--mode",
        choices=["single-run", "continuous", "scheduled"],
        default="single-run",
        help="Run mode (default: single-run)",
    )
    parser.add_argument("--max-consecutive-errors", type=int, default=3, help="Stop after N consecutive errors (default: 3)")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without calling orchestrator")
    return parser.parse_args(argv)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    target = str(Path(args.target).expanduser().resolve())
    state_root = str(Path(args.state_root).expanduser().resolve())
    state_path = Path(state_root) / "autoloop_state.json"

    # Ensure state directory exists
    Path(state_root).mkdir(parents=True, exist_ok=True)

    # Load or create state
    state = AutoloopState.load(state_path)
    state.target = target
    state.max_iterations = args.max_iterations
    state.max_cost_usd = args.max_cost
    state.plateau_window = args.plateau_window
    state.cooldown_minutes = args.cooldown_minutes
    state.max_consecutive_errors = args.max_consecutive_errors

    if not state.started_at:
        state.started_at = utc_now_iso()

    state.status = "running"
    state.save(state_path)

    print(f"Autoloop starting: target={target}, mode={args.mode}, max_iter={args.max_iterations}, max_cost=${args.max_cost}")

    try:
        while True:
            # Check termination conditions
            stop, reason = should_stop(state)
            if stop:
                status_map = {
                    "max_iterations": "stopped_max_iter",
                    "cost_cap": "stopped_cost",
                    "plateau": "stopped_plateau",
                    "oscillation": "stopped_oscillation",
                    "consecutive_errors": "stopped_errors",
                }
                for key, status_val in status_map.items():
                    if key in reason:
                        state.status = status_val
                        break
                else:
                    state.status = "completed"
                state.save(state_path)
                print(f"\nStopped: {reason}")
                break

            # Run one iteration
            print(f"\n--- Iteration {state.iterations_completed + 1}/{state.max_iterations} ---")
            state, result = run_single_iteration(state, target, state_root, dry_run=args.dry_run)
            state.save(state_path)

            decision = result.get("final_decision", "unknown")
            print(f"  Decision: {decision}")
            if state.score_history:
                latest = state.score_history[-1]
                print(f"  Weighted score: {latest['weighted_score']:.4f}")
            print(f"  Cumulative cost: ${state.total_cost_usd:.4f}")

            if state.status == "error":
                print(f"  Error: {state.last_failure_trace}")
                break

            # Mode-specific behavior
            if args.mode == "single-run":
                # Check if we should do another iteration
                stop, reason = should_stop(state)
                if stop:
                    state.status = "completed" if "max_iterations" in reason else state.status
                    for key, status_val in {
                        "max_iterations": "stopped_max_iter",
                        "cost_cap": "stopped_cost",
                        "plateau": "stopped_plateau",
                        "oscillation": "stopped_oscillation",
                    "consecutive_errors": "stopped_errors",
                    }.items():
                        if key in reason:
                            state.status = status_val
                            break
                    state.save(state_path)
                    print(f"\nStopped: {reason}")
                    break
                # Continue to next iteration in single-run mode
                continue

            elif args.mode == "continuous":
                # Sleep between iterations
                stop, reason = should_stop(state)
                if stop:
                    for key, status_val in {
                        "max_iterations": "stopped_max_iter",
                        "cost_cap": "stopped_cost",
                        "plateau": "stopped_plateau",
                        "oscillation": "stopped_oscillation",
                    "consecutive_errors": "stopped_errors",
                    }.items():
                        if key in reason:
                            state.status = status_val
                            break
                    state.save(state_path)
                    print(f"\nStopped: {reason}")
                    break
                cooldown_sec = state.cooldown_minutes * 60
                next_run = datetime.now(timezone.utc).replace(microsecond=0)
                from datetime import timedelta
                next_run = next_run + timedelta(seconds=cooldown_sec)
                state.next_run_at = next_run.isoformat().replace("+00:00", "Z")
                state.save(state_path)
                print(f"  Cooling down {state.cooldown_minutes}m (next: {state.next_run_at})")
                time.sleep(cooldown_sec)

            elif args.mode == "scheduled":
                # Exit after one iteration; cron triggers next
                state.status = "running"
                state.save(state_path)
                print("  Scheduled mode: exiting after single iteration")
                break

    except KeyboardInterrupt:
        state.status = "completed"
        state.save(state_path)
        print("\nInterrupted by user")
    except Exception:
        state.last_failure_trace = traceback.format_exc()
        state.status = "error"
        state.save(state_path)
        print(f"\nError: {state.last_failure_trace}", file=sys.stderr)
        return 1

    # Final summary
    print(f"\n=== Autoloop Summary ===")
    print(f"  Iterations: {state.iterations_completed}/{state.max_iterations}")
    print(f"  Total cost: ${state.total_cost_usd:.4f}")
    print(f"  Status: {state.status}")
    if state.score_history:
        best = max(state.score_history, key=lambda h: h["weighted_score"])
        print(f"  Best score: {best['weighted_score']:.4f} (iteration {best['iteration']})")
    print(f"  State saved: {state_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
