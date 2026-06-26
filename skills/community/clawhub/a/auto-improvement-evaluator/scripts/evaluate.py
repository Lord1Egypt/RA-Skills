#!/usr/bin/env python3
"""Improvement Evaluator: run task suites to measure Skill execution effectiveness.

Sits between the discriminator (scoring) and gate (quality gate) stages.
Runs real tasks with the Skill under test, compares candidate vs baseline pass rates.

Usage:
    python3 scripts/evaluate.py \
        --input ranking.json \
        --candidate-id c1 \
        --task-suite tasks.yaml \
        --state-root /tmp/state \
        [--pass-k 1] \
        [--baseline-cache-dir /tmp/cache] \
        [--output path.json] \
        [--eval-threshold 6.0] \
        [--mock]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import shutil
import sys
import time
from pathlib import Path
from typing import Any

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

_SCRIPTS_DIR = str(Path(__file__).resolve().parent)
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

from lib.common import (
    SCHEMA_VERSION,
    read_json,
    utc_now_iso,
    write_json,
)

from task_runner import TaskRunner, TaskResult

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BASELINE_CACHE_TTL_DAYS = 7
BASELINE_ABORT_THRESHOLD = 0.2  # abort if baseline < 20%
VALID_JUDGE_TYPES = {"contains", "pytest", "llm-rubric"}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run task suite to evaluate Skill execution effectiveness.",
    )
    parser.add_argument("--input", help="Path to ranking artifact JSON (from discriminator)")
    parser.add_argument("--candidate-id", help="ID of the candidate to evaluate")
    parser.add_argument("--standalone", action="store_true",
                        help="Run task suite directly without ranking artifact (standalone mode)")
    parser.add_argument("--task-suite", required=True, help="Path to task suite YAML")
    parser.add_argument("--state-root", required=True, help="State root directory")
    parser.add_argument("--pass-k", type=int, default=1, help="Number of attempts per task (pass@k)")
    parser.add_argument("--baseline-cache-dir", help="Directory for baseline result caching")
    parser.add_argument("--output", help="Output path for evaluation artifact JSON")
    parser.add_argument("--eval-threshold", type=float, default=6.0, help="Minimum discriminator score to evaluate")
    parser.add_argument("--mock", action="store_true", help="Use mock execution (no claude CLI needed)")
    parser.add_argument("--model", help="Model to use for claude -p (e.g. claude-sonnet-4-6, claude-haiku-4-5)")
    parser.add_argument("--skill-path", help="Path to SKILL.md or skill directory (standalone mode: prepend to prompts)")
    return parser.parse_args(argv)


# ---------------------------------------------------------------------------
# Preflight checks
# ---------------------------------------------------------------------------


def preflight_check(task_suite_path: Path, mock: bool = False) -> None:
    """Validate prerequisites before running evaluation."""
    # Check claude CLI availability (skip in mock mode)
    if not mock:
        if shutil.which("claude") is None:
            raise AssertionError(
                "claude CLI not found in PATH. Install it or use --mock for testing."
            )

    # Validate task suite file exists
    if not task_suite_path.exists():
        raise AssertionError(f"Task suite not found: {task_suite_path}")

    # Validate YAML schema
    suite = _load_yaml(task_suite_path)
    _validate_suite_schema(suite)


def _load_yaml(path: Path) -> dict:
    """Load and return YAML content."""
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _validate_suite_schema(suite: dict) -> None:
    """Validate task suite YAML schema."""
    assert "skill_id" in suite and suite["skill_id"], "skill_id is required and must be non-empty"
    assert "version" in suite and suite["version"] == "1.0", "version must be '1.0'"
    assert "tasks" in suite and isinstance(suite["tasks"], list), "tasks must be a list"
    assert len(suite["tasks"]) > 0, "tasks list must not be empty"

    seen_ids: set[str] = set()
    for i, task in enumerate(suite["tasks"]):
        assert "id" in task, f"task[{i}] missing 'id'"
        assert task["id"] not in seen_ids, f"duplicate task id: {task['id']}"
        seen_ids.add(task["id"])
        assert "prompt" in task and task["prompt"], f"task[{i}] missing or empty 'prompt'"
        assert "judge" in task, f"task[{i}] missing 'judge'"
        judge = task["judge"]
        assert "type" in judge, f"task[{i}] judge missing 'type'"
        assert judge["type"] in VALID_JUDGE_TYPES, (
            f"task[{i}] unknown judge type: {judge['type']}"
        )

        if judge["type"] == "contains":
            assert "expected" in judge and isinstance(judge["expected"], list), (
                f"task[{i}] contains judge needs 'expected' list"
            )
            assert len(judge["expected"]) > 0, f"task[{i}] 'expected' list must not be empty"
        elif judge["type"] == "pytest":
            assert "test_file" in judge, f"task[{i}] pytest judge needs 'test_file'"
            assert judge["test_file"].startswith("fixtures/"), (
                f"task[{i}] test_file must start with 'fixtures/'"
            )
        elif judge["type"] == "llm-rubric":
            assert "rubric" in judge and judge["rubric"], (
                f"task[{i}] llm-rubric judge needs non-empty 'rubric'"
            )


# ---------------------------------------------------------------------------
# Task suite loading
# ---------------------------------------------------------------------------


def load_task_suite(path: Path) -> dict:
    """Load and validate a task suite YAML file."""
    suite = _load_yaml(path)
    _validate_suite_schema(suite)
    return suite


# ---------------------------------------------------------------------------
# Candidate / baseline execution
# ---------------------------------------------------------------------------


def extract_candidate_skill(ranking_artifact: dict, candidate_id: str) -> dict:
    """Find the candidate by ID in the ranking artifact."""
    for candidate in ranking_artifact.get("scored_candidates", []):
        if candidate.get("id") == candidate_id:
            return candidate
    raise ValueError(f"Candidate '{candidate_id}' not found in ranking artifact")


def get_skill_content(candidate: dict, target: dict) -> str:
    """Extract the SKILL.md content for a candidate.

    Candidates may have their own 'skill_content' or 'content' field.
    If not, read the original SKILL.md from the target path.
    """
    # Check candidate for inline content
    for key in ("skill_content", "content", "body"):
        if key in candidate and candidate[key]:
            return candidate[key]

    # Fallback: read original SKILL.md from target
    target_path = Path(target.get("path", ""))
    skill_md = target_path / "SKILL.md" if target_path.is_dir() else target_path
    if skill_md.exists():
        return skill_md.read_text(encoding="utf-8")

    raise ValueError(f"Cannot find SKILL.md content for candidate or at {target_path}")


def get_baseline_skill_content(target: dict) -> str:
    """Read the original (baseline) SKILL.md from the target path."""
    target_path = Path(target.get("path", ""))
    skill_md = target_path / "SKILL.md" if target_path.is_dir() else target_path
    if skill_md.exists():
        return skill_md.read_text(encoding="utf-8")
    raise ValueError(f"Baseline SKILL.md not found at {target_path}")


def run_task_suite(
    runner: TaskRunner,
    skill_content: str,
    tasks: list[dict],
    pass_k: int = 1,
) -> list[dict]:
    """Run all tasks in a suite and return per-task results."""
    results = []
    for task in tasks:
        task_result = runner.run(skill_content, task, pass_k=pass_k)
        results.append({
            "task_id": task["id"],
            "passed": task_result.passed,
            "score": task_result.judge_output.get("score", 0.0),
            "details": task_result.judge_output.get("details", ""),
            "duration_ms": task_result.duration_ms,
            "error": task_result.error,
        })
    return results


def compute_pass_rate(results: list[dict]) -> float:
    """Compute pass rate from task results."""
    if not results:
        return 0.0
    passed = sum(1 for r in results if r["passed"])
    return round(passed / len(results), 4)


# ---------------------------------------------------------------------------
# Baseline caching
# ---------------------------------------------------------------------------


def _baseline_cache_key(skill_content: str, suite_path: str) -> str:
    """Generate a cache key from skill content and suite path."""
    h = hashlib.sha256()
    h.update(skill_content.encode("utf-8"))
    h.update(suite_path.encode("utf-8"))
    return h.hexdigest()[:16]


def load_baseline_cache(cache_dir: Path, cache_key: str) -> dict | None:
    """Load cached baseline results if fresh enough."""
    cache_file = cache_dir / f"baseline_{cache_key}.json"
    if not cache_file.exists():
        return None

    cached = read_json(cache_file)
    # Check TTL
    created_at = cached.get("created_at", "")
    if not created_at:
        return None

    from datetime import datetime, timezone
    try:
        created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        age_days = (datetime.now(timezone.utc) - created).days
        if age_days > BASELINE_CACHE_TTL_DAYS:
            return None
    except (ValueError, TypeError):
        return None

    return cached


def save_baseline_cache(cache_dir: Path, cache_key: str, data: dict) -> None:
    """Save baseline results to cache."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"baseline_{cache_key}.json"
    write_json(cache_file, data)


# ---------------------------------------------------------------------------
# Result computation
# ---------------------------------------------------------------------------


def compute_results(
    candidate_rate: float,
    baseline_rate: float,
) -> dict:
    """Compute delta and verdict.

    Verdict is "pass" if candidate pass_rate >= baseline pass_rate.
    """
    delta = round(candidate_rate - baseline_rate, 4)
    verdict = "pass" if delta >= 0 or candidate_rate >= baseline_rate else "fail"
    return {
        "execution_pass_rate": candidate_rate,
        "baseline_pass_rate": baseline_rate,
        "delta": delta,
        "verdict": verdict,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    state_root = Path(args.state_root).expanduser().resolve()
    state_root.mkdir(parents=True, exist_ok=True)
    task_suite_path = Path(args.task_suite).expanduser().resolve()

    # Preflight
    try:
        preflight_check(task_suite_path, mock=args.mock)
    except AssertionError as exc:
        logger.error("Preflight failed: %s", exc)
        return 1

    # --- Standalone mode: run task suite directly without ranking artifact ---
    if args.standalone:
        suite = load_task_suite(task_suite_path)
        tasks = suite["tasks"]
        runner = TaskRunner(mock=args.mock, model=getattr(args, 'model', None))
        run_id = f"standalone-{suite.get('skill_id', 'unknown')}"

        # Load skill content if --skill-path provided
        skill_content = ""
        if args.skill_path:
            sp = Path(args.skill_path).expanduser().resolve()
            skill_md = sp / "SKILL.md" if sp.is_dir() else sp
            if skill_md.exists():
                skill_content = skill_md.read_text(encoding="utf-8")
                logger.info("Loaded SKILL.md from %s (%d chars)", skill_md, len(skill_content))
            else:
                logger.warning("SKILL.md not found at %s, running without skill content", skill_md)

        logger.info("Running %d tasks in standalone mode...", len(tasks))
        results = run_task_suite(runner, skill_content, tasks, pass_k=args.pass_k)
        pass_rate = compute_pass_rate(results)

        output_path = _resolve_output(args.output, state_root, run_id)
        artifact = {
            "schema_version": SCHEMA_VERSION,
            "lane": "standalone",
            "run_id": run_id,
            "stage": "evaluated",
            "status": "success",
            "created_at": utc_now_iso(),
            "task_suite": str(task_suite_path),
            "skill_id": suite.get("skill_id", ""),
            "pass_k": args.pass_k,
            "evaluation": {
                "total_tasks": len(results),
                "passed": sum(1 for r in results if r["passed"]),
                "failed": sum(1 for r in results if not r["passed"]),
                "pass_rate": pass_rate,
                "verdict": "pass" if pass_rate >= 0.5 else "fail",
            },
            "task_results": results,
            "truth_anchor": str(output_path),
        }
        write_json(output_path, artifact)
        print(str(output_path))

        # Pretty print summary
        logger.info("=== Standalone Evaluation Results ===")
        logger.info("Skill: %s", suite.get("skill_id", "unknown"))
        logger.info("Tasks: %d passed / %d total (%.0f%%)",
                     artifact["evaluation"]["passed"], len(results), pass_rate * 100)
        for r in results:
            status = "PASS" if r["passed"] else "FAIL"
            logger.info("  [%s] %s", status, r.get("task_id", "?"))
        return 0

    # --- Pipeline mode: requires --input and --candidate-id ---
    if not args.input or not args.candidate_id:
        logger.error("--input and --candidate-id required in pipeline mode (use --standalone for direct evaluation)")
        return 1

    # Load inputs
    ranking_artifact = read_json(Path(args.input).expanduser().resolve())
    run_id = ranking_artifact["run_id"]
    target = ranking_artifact.get("target", {})

    # Find candidate
    try:
        candidate = extract_candidate_skill(ranking_artifact, args.candidate_id)
    except ValueError as exc:
        logger.error(str(exc))
        return 1

    # Check if candidate score meets threshold
    candidate_score = candidate.get("score", 0.0)
    if candidate_score < args.eval_threshold:
        logger.info(
            "Candidate score %.1f below threshold %.1f, skipping evaluation",
            candidate_score, args.eval_threshold,
        )
        output_path = _resolve_output(args.output, state_root, run_id)
        artifact = _build_artifact(
            run_id=run_id,
            target=target,
            candidate_id=args.candidate_id,
            verdict="skipped",
            reason=f"score {candidate_score} < threshold {args.eval_threshold}",
            output_path=output_path,
        )
        write_json(output_path, artifact)
        print(str(output_path))
        return 0

    # Load task suite
    suite = load_task_suite(task_suite_path)
    tasks = suite["tasks"]

    runner = TaskRunner(mock=args.mock, model=getattr(args, 'model', None))

    # --- Run candidate ---
    try:
        candidate_skill = get_skill_content(candidate, target)
    except ValueError as exc:
        logger.error("Cannot get candidate skill content: %s", exc)
        return 1

    logger.info("Running %d tasks for candidate '%s'...", len(tasks), args.candidate_id)
    candidate_results = run_task_suite(runner, candidate_skill, tasks, pass_k=args.pass_k)
    candidate_rate = compute_pass_rate(candidate_results)
    logger.info("Candidate pass rate: %.2f", candidate_rate)

    # --- Run baseline ---
    baseline_results: list[dict] | None = None
    baseline_rate = 0.0

    cache_dir = Path(args.baseline_cache_dir).expanduser().resolve() if args.baseline_cache_dir else None

    try:
        baseline_skill = get_baseline_skill_content(target)
    except ValueError:
        logger.warning("Baseline SKILL.md not found; using 0.0 as baseline")
        baseline_skill = None

    if baseline_skill:
        # Check cache
        cached = None
        cache_key = ""
        if cache_dir:
            cache_key = _baseline_cache_key(baseline_skill, str(task_suite_path))
            cached = load_baseline_cache(cache_dir, cache_key)

        if cached:
            baseline_rate = cached["pass_rate"]
            baseline_results = cached["results"]
            logger.info("Baseline loaded from cache: %.2f", baseline_rate)
        else:
            logger.info("Running %d tasks for baseline...", len(tasks))
            baseline_results = run_task_suite(runner, baseline_skill, tasks, pass_k=args.pass_k)
            baseline_rate = compute_pass_rate(baseline_results)
            logger.info("Baseline pass rate: %.2f", baseline_rate)

            # Save to cache
            if cache_dir and cache_key:
                save_baseline_cache(cache_dir, cache_key, {
                    "pass_rate": baseline_rate,
                    "results": baseline_results,
                    "created_at": utc_now_iso(),
                })

        # Abort if baseline is broken
        if baseline_rate < BASELINE_ABORT_THRESHOLD:
            logger.error(
                "Baseline pass rate %.2f < %.2f threshold. Task suite may be broken.",
                baseline_rate, BASELINE_ABORT_THRESHOLD,
            )
            output_path = _resolve_output(args.output, state_root, run_id)
            artifact = _build_artifact(
                run_id=run_id,
                target=target,
                candidate_id=args.candidate_id,
                verdict="error",
                reason=f"baseline pass rate {baseline_rate} < {BASELINE_ABORT_THRESHOLD}",
                output_path=output_path,
            )
            write_json(output_path, artifact)
            print(str(output_path))
            return 1

    # --- Compute results ---
    evaluation = compute_results(candidate_rate, baseline_rate)

    # --- Build output artifact ---
    output_path = _resolve_output(args.output, state_root, run_id)
    artifact = {
        "schema_version": SCHEMA_VERSION,
        "lane": ranking_artifact.get("lane", "generic-skill"),
        "run_id": run_id,
        "stage": "evaluated",
        "status": "success",
        "created_at": utc_now_iso(),
        "source_ranking_artifact": args.input,
        "candidate_id": args.candidate_id,
        "candidate_score": candidate_score,
        "task_suite": str(task_suite_path),
        "task_suite_skill_id": suite.get("skill_id", ""),
        "pass_k": args.pass_k,
        "evaluation": evaluation,
        "candidate_results": candidate_results,
        "baseline_results": baseline_results,
        "target": target,
        "next_step": "gate_decision",
        "next_owner": "gate",
        "truth_anchor": str(output_path),
    }
    write_json(output_path, artifact)
    print(str(output_path))
    return 0


def _resolve_output(output_arg: str | None, state_root: Path, run_id: str) -> Path:
    """Resolve the output file path."""
    if output_arg:
        return Path(output_arg).expanduser().resolve()
    evaluations_dir = state_root / "evaluations"
    evaluations_dir.mkdir(parents=True, exist_ok=True)
    return evaluations_dir / f"{run_id}.json"


def _build_artifact(
    *,
    run_id: str,
    target: dict,
    candidate_id: str,
    verdict: str,
    reason: str,
    output_path: Path,
) -> dict:
    """Build a minimal evaluation artifact for skip/error cases."""
    return {
        "schema_version": SCHEMA_VERSION,
        "lane": "generic-skill",
        "run_id": run_id,
        "stage": "evaluated",
        "status": verdict,
        "created_at": utc_now_iso(),
        "candidate_id": candidate_id,
        "evaluation": {
            "execution_pass_rate": 0.0,
            "baseline_pass_rate": 0.0,
            "delta": 0.0,
            "verdict": verdict,
            "reason": reason,
        },
        "target": target,
        "next_step": "gate_decision" if verdict == "skipped" else "abort",
        "next_owner": "gate" if verdict == "skipped" else "human",
        "truth_anchor": str(output_path),
    }


if __name__ == "__main__":
    sys.exit(main())
