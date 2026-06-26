#!/usr/bin/env python3
"""
Unified Orchestrator v2 — Pipeline
The main entry point. Runs the full unified pipeline across all three skills
and activates all five paradigm shifts.

Five Paradigm Shifts:
  1. Specification Drift Detection (signal_router.py)
  2. Capability Expansion via Meta-Learning (meta_learner.py)
  3. Autonomous Re-specification (capability_expander.py)
  4. Cross-Goal Skill Transfer (meta_learner.py)
  5. Verifiable Improvement Chains (signal_router.py)

Usage:
  python pipeline.py --goal "Process customer tickets with 98% accuracy"
  python pipeline.py --spec specification.json
  python pipeline.py --spec specification.json --outcome outcome_report.json
  python pipeline.py --state pipeline_state.json
  python pipeline.py --goal "..." --cycles 5 --output-dir ./run_001/
"""
import json
import sys
import time
import random
import hashlib
import argparse
from pathlib import Path
from datetime import datetime, timezone
from copy import deepcopy

# Import sibling scripts
sys.path.insert(0, str(Path(__file__).parent))
from signal_router import compute_drift_score, chain_append, verify_chain, route_signals
from meta_learner import (
    extract_learnings, update_learnings_log, generate_patches,
    update_goal_index, find_transfer_match
)
from capability_expander import generate_revised_specification, format_revision_rationale_md


def log(msg: str, level: str = "INFO"):
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    icons = {"OK": "✓", "FAIL": "✗", "WARN": "⚠", "INFO": " ", "STAGE": "▶"}
    print(f"[{ts}] {icons.get(level, ' ')} {msg}")


def sha256_dict(data: dict) -> str:
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


def _load_config(config_path: Path) -> dict:
    defaults = {
        "drift_threshold": 0.15,
        "auto_revise_after_n_failures": 3,
        "transfer_similarity_threshold": 0.60,
        "chain_enabled": True,
        "meta_learning_enabled": True,
        "min_cycles_for_meta_learning": 3,
        "no_auto_revise": False,
        "no_transfer": False
    }
    if config_path and config_path.exists():
        user_config = json.loads(config_path.read_text())
        defaults.update(user_config)
    return defaults


# ── Stage 1: Intent Engineering (Specification Generation) ───────────────────

def _generate_specification(goal: str, transfer_spec: dict = None) -> dict:
    """
    Generate a specification from a goal description.
    In production, this calls the intent-engineering skill.
    If a transfer_spec is provided, bootstraps from it.
    """
    log("Stage 1 — Generating specification from goal...", "STAGE")

    if transfer_spec:
        log("  Transfer: bootstrapping from prior goal specification", "INFO")
        spec = deepcopy(transfer_spec)
        spec["title"] = goal[:80]
        spec["goal"] = goal
        spec["specification_id"] = f"spec-{hashlib.sha256(goal.encode()).hexdigest()[:12]}"
        spec["version"] = "1.0-transferred"
        spec["created_at"] = datetime.now(timezone.utc).isoformat()
        spec["transfer_source"] = transfer_spec.get("specification_id")
        return spec

    # Standalone specification generation
    spec_id = f"spec-{hashlib.sha256(goal.encode()).hexdigest()[:12]}"
    return {
        "specification_id": spec_id,
        "title": goal[:80],
        "goal": goal,
        "version": "1.0",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "success_criteria": {
            "pass_rate": 0.95,
            "duration_ms": 2000,
            "alignment_score": 0.85
        },
        "behavioral_scenarios": [
            {
                "scenario": "Standard input processing",
                "input": "Typical input matching goal description",
                "expected_output": "Correct output within success criteria",
                "priority": "high"
            },
            {
                "scenario": "Edge case handling",
                "input": "Boundary or unusual input",
                "expected_output": "Graceful handling without failure",
                "priority": "medium"
            }
        ],
        "data_contracts": {
            "input_schema": {"type": "object", "description": f"Input for: {goal[:50]}"},
            "output_schema": {"type": "object", "description": "Output meeting success criteria"}
        },
        "constraints": ["Must meet all success criteria", "Must handle edge cases gracefully"],
        "generated_by": "unified-orchestrator-v2-standalone"
    }


# ── Stage 2: Dark Factory (Execution) ────────────────────────────────────────

def _execute_specification(spec: dict, outcome_report: dict = None) -> dict:
    """
    Execute the specification via dark-factory.
    If an outcome_report is provided, uses it directly.
    Otherwise, simulates execution.
    """
    log("Stage 2 — Executing specification...", "STAGE")

    if outcome_report:
        log("  Using provided dark-factory outcome report", "INFO")
        return outcome_report

    # Simulate execution (integration point for dark-factory)
    time.sleep(random.uniform(0.05, 0.15))
    scenarios = spec.get("behavioral_scenarios", [])
    pass_rate = round(random.uniform(0.72, 0.97), 4)
    passed = int(len(scenarios) * pass_rate)

    return {
        "outcome_id": f"outcome-{hashlib.sha256(spec.get('specification_id', '').encode()).hexdigest()[:12]}",
        "specification_id": spec.get("specification_id"),
        "status": "success" if pass_rate >= 0.90 else "partial",
        "performance_metrics": {
            "overall_pass_rate": pass_rate,
            "total_duration_ms": round(random.uniform(800, 2500), 1),
            "tests_run": len(scenarios),
            "tests_passed": passed,
            "tests_failed": len(scenarios) - passed
        },
        "behavioral_test_results": [
            {
                "scenario": s.get("scenario", f"Test {i+1}"),
                "passed": random.random() < pass_rate,
                "duration_ms": round(random.uniform(50, 400), 1)
            }
            for i, s in enumerate(scenarios)
        ],
        "edge_cases_detected": [
            {"case": "Null input handling", "severity": "medium"}
        ] if pass_rate < 0.90 else [],
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": "unified-orchestrator-v2-standalone"
    }


# ── Stage 3: Feedback Loop (Analysis) ────────────────────────────────────────

def _run_feedback_loop(spec: dict, outcome: dict, prior_observation: dict = None) -> dict:
    """
    Run the feedback loop analysis.
    Returns (observation, analysis, improvement_report).
    """
    log("Stage 3 — Running feedback loop analysis...", "STAGE")

    perf = outcome.get("performance_metrics", {})
    pass_rate = perf.get("overall_pass_rate", perf.get("pass_rate", 0.8))
    duration_ms = perf.get("total_duration_ms", perf.get("duration_ms", 1500))

    # Performance score
    perf_score = round(pass_rate * 0.7 + max(0, 1 - duration_ms / 5000) * 0.3, 4)

    # Regression detection
    prior_score = prior_observation.get("performance_score") if prior_observation else None
    regression = {
        "detected": prior_score is not None and perf_score < prior_score - 0.05,
        "prior_score": prior_score,
        "delta": round(perf_score - prior_score, 4) if prior_score is not None else None
    }

    # Suggestions
    suggestions = []
    if pass_rate < 0.95:
        suggestions.append({
            "id": "S001", "priority": "high", "category": "test_coverage",
            "description": f"Pass rate {pass_rate:.1%} below target 95%. Add edge case scenarios.",
            "effort_estimate": "medium", "expected_impact": "high"
        })
    if duration_ms > 2000:
        suggestions.append({
            "id": "S002", "priority": "medium", "category": "performance",
            "description": f"Duration {duration_ms:.0f}ms exceeds 2000ms target. Profile and optimize hot paths.",
            "effort_estimate": "high", "expected_impact": "medium"
        })
    if regression["detected"]:
        suggestions.append({
            "id": "S003", "priority": "critical", "category": "regression",
            "description": f"Performance regression detected: {prior_score:.3f} → {perf_score:.3f} (delta: {regression['delta']:.3f})",
            "effort_estimate": "medium", "expected_impact": "critical"
        })

    # Alignment check
    alignment_score = round(min(1.0, perf_score * 1.1 + 0.05), 4)
    alignment = {
        "alignment_score": alignment_score,
        "flags": [] if alignment_score >= 0.80 else ["alignment_below_threshold"]
    }

    # Regression tests from failures
    regression_tests = []
    for result in outcome.get("behavioral_test_results", []):
        if not result.get("passed"):
            regression_tests.append({
                "test_id": f"RT-{hashlib.sha256(result.get('scenario', '').encode()).hexdigest()[:8]}",
                "scenario": result.get("scenario"),
                "input": "Reproduce failing input",
                "expected_output": "Expected passing output",
                "generated_from": "failure"
            })
    for edge in outcome.get("edge_cases_detected", []):
        regression_tests.append({
            "test_id": f"RT-{hashlib.sha256(edge.get('case', '').encode()).hexdigest()[:8]}",
            "scenario": edge.get("case"),
            "input": "Edge case input",
            "expected_output": "Graceful handling",
            "generated_from": "edge_case"
        })

    analysis_id = f"analysis-{hashlib.sha256(spec.get('specification_id', '').encode()).hexdigest()[:12]}"
    analysis = {
        "analysis_id": analysis_id,
        "specification_id": spec.get("specification_id"),
        "performance_score": perf_score,
        "regression": regression,
        "suggestions": suggestions,
        "alignment": alignment,
        "regression_tests": regression_tests,
        "metrics_analyzed": ["pass_rate", "duration_ms"],
        "analyzed_at": datetime.now(timezone.utc).isoformat()
    }

    # Build observation
    observation = {
        "observation_id": f"obs-{hashlib.sha256(analysis_id.encode()).hexdigest()[:12]}",
        "source_type": "outcome_report" if outcome.get("outcome_id") else "json",
        "mode": "full_triad" if spec.get("specification_id") else "enhanced",
        "metrics": {"pass_rate": pass_rate, "duration_ms": duration_ms},
        "performance_score": perf_score,
        "failures": [r for r in outcome.get("behavioral_test_results", []) if not r.get("passed")],
        "edge_cases": outcome.get("edge_cases_detected", []),
        "observed_at": datetime.now(timezone.utc).isoformat()
    }

    # Build improvement report
    report_id = f"report-{hashlib.sha256(analysis_id.encode()).hexdigest()[:12]}"
    report_payload = {
        "report_id": report_id,
        "specification_id": spec.get("specification_id"),
        "analysis_id": analysis_id,
        "summary": {
            "performance_score": perf_score,
            "alignment_score": alignment_score,
            "suggestions_count": len(suggestions),
            "regression_tests_generated": len(regression_tests),
            "regression_detected": regression["detected"]
        },
        "suggestions": suggestions,
        "regression_tests": regression_tests,
        "generated_at": datetime.now(timezone.utc).isoformat()
    }
    report_payload["integrity"] = {
        "sha256": sha256_dict(report_payload),
        "signed_at": datetime.now(timezone.utc).isoformat()
    }

    return observation, analysis, report_payload


# ── Main Pipeline ─────────────────────────────────────────────────────────────

def run_pipeline(
    goal: str = None,
    spec_path: Path = None,
    outcome_path: Path = None,
    state_path: Path = None,
    output_dir: Path = Path("./pipeline_output"),
    config: dict = None,
    cycle_override: int = None
) -> dict:
    """Run one full pipeline cycle."""
    output_dir.mkdir(parents=True, exist_ok=True)
    config = config or {}

    # ── Load prior state ──────────────────────────────────────────────────────
    prior_state = {}
    if state_path and state_path.exists():
        prior_state = json.loads(state_path.read_text())
        log(f"Resuming from prior state (cycle {prior_state.get('cycle', 1)})", "INFO")

    cycle = cycle_override or (prior_state.get("cycle", 0) + 1)
    goal = goal or prior_state.get("goal", "")
    prior_observation = prior_state.get("observation")

    log(f"{'='*60}", "INFO")
    log(f"Unified Orchestrator v2 — Cycle {cycle}", "STAGE")
    log(f"Goal: {goal[:80]}", "INFO")
    log(f"{'='*60}", "INFO")

    # ── Paradigm Shift 4: Cross-Goal Transfer ────────────────────────────────
    transfer_spec = None
    transfer_applied = False
    if not config.get("no_transfer") and cycle == 1:
        index_path = output_dir / "goal_similarity_index.json"
        if index_path.exists():
            index = json.loads(index_path.read_text())
            transfer_result = find_transfer_match(
                goal, index,
                threshold=config.get("transfer_similarity_threshold", 0.60)
            )
            if transfer_result.get("match_found"):
                transfer_spec = transfer_result.get("best_specification")
                transfer_applied = True
                log(f"Paradigm Shift 4 — Transfer: matched '{transfer_result['matched_goal'][:60]}' (sim={transfer_result['similarity_score']:.2f})", "OK")

    # ── Stage 1: Specification ────────────────────────────────────────────────
    if spec_path and spec_path.exists():
        specification = json.loads(spec_path.read_text())
        log(f"Stage 1 — Loaded specification: {specification.get('specification_id')}", "OK")
    else:
        specification = _generate_specification(goal, transfer_spec)
        spec_out = output_dir / "specification.json"
        spec_out.write_text(json.dumps(specification, indent=2))
        log(f"Stage 1 — Specification generated: {specification.get('specification_id')}", "OK")

    # ── Paradigm Shift 3: Check for impossible criteria ───────────────────────
    auto_revised = False
    if not config.get("no_auto_revise"):
        history_path = output_dir / "cycles_history.json"
        history = json.loads(history_path.read_text()) if history_path.exists() else []
        if len(history) >= config.get("auto_revise_after_n_failures", 3):
            revision_result = generate_revised_specification(
                specification, history,
                threshold=config.get("auto_revise_after_n_failures", 3)
            )
            if revision_result["needs_revision"]:
                log(f"Paradigm Shift 3 — Auto-revising specification ({len(revision_result['impossible_criteria'])} impossible criteria)", "WARN")
                specification = revision_result["revised_specification"]
                (output_dir / "revised_specification.json").write_text(json.dumps(specification, indent=2))
                rationale_md = format_revision_rationale_md(revision_result["revision_rationale"])
                (output_dir / "revision_rationale.md").write_text(rationale_md)
                (output_dir / "revision_rationale.json").write_text(json.dumps(revision_result["revision_rationale"], indent=2))
                auto_revised = True

    # ── Stage 2: Execution ────────────────────────────────────────────────────
    outcome_report = None
    if outcome_path and outcome_path.exists():
        outcome_report = json.loads(outcome_path.read_text())
    outcome = _execute_specification(specification, outcome_report)
    (output_dir / "outcome_report.json").write_text(json.dumps(outcome, indent=2))
    log(f"Stage 2 — Execution complete: pass_rate={outcome.get('performance_metrics', {}).get('overall_pass_rate', '?')}", "OK")

    # ── Stage 3: Feedback Loop ────────────────────────────────────────────────
    observation, analysis, improvement_report = _run_feedback_loop(
        specification, outcome, prior_observation
    )
    (output_dir / "observation.json").write_text(json.dumps(observation, indent=2))
    (output_dir / "analysis.json").write_text(json.dumps(analysis, indent=2))
    (output_dir / "improvement_report.json").write_text(json.dumps(improvement_report, indent=2))
    log(f"Stage 3 — Analysis complete: perf={analysis['performance_score']:.3f}, align={analysis['alignment']['alignment_score']:.3f}, suggestions={len(analysis['suggestions'])}", "OK")

    # ── Paradigm Shift 1: Drift Detection ────────────────────────────────────
    drift_result = compute_drift_score(specification, analysis, outcome)
    (output_dir / "drift_result.json").write_text(json.dumps(drift_result, indent=2))
    drift_icon = "OK" if drift_result["severity"] == "none" else ("WARN" if drift_result["severity"] in ("minor", "moderate") else "FAIL")
    log(f"Paradigm Shift 1 — Drift: {drift_result['drift_score']:.4f} ({drift_result['severity']}) → {drift_result['action']}", drift_icon)

    # ── Paradigm Shift 5: Improvement Chain ──────────────────────────────────
    chain_path = output_dir / "improvement_chain.json"
    chain = json.loads(chain_path.read_text()) if chain_path.exists() else []
    improvement_report["cycle"] = cycle
    updated_chain, chain_link = chain_append(chain, improvement_report)
    chain_path.write_text(json.dumps(updated_chain, indent=2))
    log(f"Paradigm Shift 5 — Chain: {len(updated_chain)} link(s), hash={chain_link['report_hash'][:16]}...", "OK")

    # ── Build pipeline state ──────────────────────────────────────────────────
    consecutive_failures = prior_state.get("consecutive_failures", 0)
    if analysis["performance_score"] < 0.80:
        consecutive_failures += 1
    else:
        consecutive_failures = 0

    state = {
        "goal": goal,
        "cycle": cycle,
        "specification": specification,
        "outcome": outcome,
        "observation": observation,
        "analysis": analysis,
        "improvement_report": improvement_report,
        "drift_result": drift_result,
        "chain_link": chain_link,
        "consecutive_failures": consecutive_failures,
        "auto_revised": auto_revised,
        "transfer_applied": transfer_applied,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }

    # ── Paradigm Shift 2: Meta-Learning ──────────────────────────────────────
    if config.get("meta_learning_enabled", True):
        learnings_log_path = output_dir / "learnings_log.json"
        existing_learnings = json.loads(learnings_log_path.read_text()) if learnings_log_path.exists() else []
        new_learning = extract_learnings(state)
        all_learnings = update_learnings_log(learnings_log_path, new_learning)

        patches = generate_patches(all_learnings, min_cycles=config.get("min_cycles_for_meta_learning", 3))
        if patches["ready"]:
            (output_dir / "meta_patches.json").write_text(json.dumps(patches, indent=2))
            log(f"Paradigm Shift 2 — Meta patches: {len(patches['specification_patches'])} spec, {len(patches['rule_patches'])} rule", "OK")
        else:
            log(f"Paradigm Shift 2 — Meta-learning: {patches['reason']}", "INFO")

        # Update goal similarity index
        index_path = output_dir / "goal_similarity_index.json"
        update_goal_index(index_path, state)

    # ── Update cycles history ─────────────────────────────────────────────────
    history_path = output_dir / "cycles_history.json"
    history = json.loads(history_path.read_text()) if history_path.exists() else []
    perf = outcome.get("performance_metrics", {})
    history.append({
        "cycle": cycle,
        "metrics": {
            "pass_rate": perf.get("overall_pass_rate", perf.get("pass_rate")),
            "duration_ms": perf.get("total_duration_ms", perf.get("duration_ms")),
            "alignment_score": analysis["alignment"]["alignment_score"]
        },
        "performance_score": analysis["performance_score"],
        "drift_score": drift_result["drift_score"],
        "auto_revised": auto_revised
    })
    history_path.write_text(json.dumps(history, indent=2))

    # ── Save pipeline state ───────────────────────────────────────────────────
    state_out = output_dir / "pipeline_state.json"
    state_out.write_text(json.dumps(state, indent=2))

    # ── Build full pipeline run report ────────────────────────────────────────
    run_report = {
        "pipeline_run_id": f"run-{hashlib.sha256(f'{goal}{cycle}'.encode()).hexdigest()[:12]}",
        "goal": goal,
        "cycle": cycle,
        "paradigm_shifts": {
            "drift_detection": drift_result,
            "meta_learning_applied": patches["ready"] if config.get("meta_learning_enabled", True) else False,
            "auto_revised": auto_revised,
            "transfer_applied": transfer_applied,
            "chain_link": chain_link
        },
        "summary": {
            "performance_score": analysis["performance_score"],
            "alignment_score": analysis["alignment"]["alignment_score"],
            "drift_score": drift_result["drift_score"],
            "drift_severity": drift_result["severity"],
            "suggestions_count": len(analysis["suggestions"]),
            "regression_tests_generated": len(analysis["regression_tests"]),
            "chain_length": len(updated_chain)
        },
        "next_action": drift_result["action"],
        "outputs": {
            "specification": str(output_dir / "specification.json"),
            "outcome_report": str(output_dir / "outcome_report.json"),
            "observation": str(output_dir / "observation.json"),
            "analysis": str(output_dir / "analysis.json"),
            "improvement_report": str(output_dir / "improvement_report.json"),
            "improvement_chain": str(chain_path),
            "pipeline_state": str(state_out)
        },
        "generated_at": datetime.now(timezone.utc).isoformat()
    }
    run_report["integrity"] = {
        "sha256": sha256_dict({k: v for k, v in run_report.items() if k != "integrity"}),
        "signed_at": datetime.now(timezone.utc).isoformat()
    }
    (output_dir / "pipeline_run_report.json").write_text(json.dumps(run_report, indent=2))

    log(f"{'='*60}", "INFO")
    log(f"Pipeline cycle {cycle} complete.", "OK")
    log(f"  Performance: {analysis['performance_score']:.3f} | Alignment: {analysis['alignment']['alignment_score']:.3f} | Drift: {drift_result['drift_score']:.4f} ({drift_result['severity']})", "OK")
    log(f"  Suggestions: {len(analysis['suggestions'])} | Regression tests: {len(analysis['regression_tests'])} | Chain: {len(updated_chain)} links", "OK")
    log(f"  Outputs in: {output_dir}", "OK")
    log(f"{'='*60}", "INFO")

    return run_report


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Unified Orchestrator v2 Pipeline")
    parser.add_argument("--goal", help="Plain language goal description")
    parser.add_argument("--spec", help="Path to specification.json")
    parser.add_argument("--outcome", help="Path to dark-factory outcome_report.json")
    parser.add_argument("--state", help="Path to prior pipeline_state.json (continue a cycle)")
    parser.add_argument("--output-dir", default="./pipeline_output", help="Output directory")
    parser.add_argument("--cycles", type=int, default=1, help="Number of cycles to run")
    parser.add_argument("--config", help="Path to pipeline_config.json")
    parser.add_argument("--no-auto-revise", action="store_true", help="Disable autonomous re-specification")
    parser.add_argument("--no-transfer", action="store_true", help="Disable cross-goal skill transfer")
    parser.add_argument("--verify-chain", action="store_true", help="Verify improvement chain after run")

    args = parser.parse_args()

    if not args.goal and not args.spec and not args.state:
        parser.error("Provide at least one of: --goal, --spec, or --state")

    output_dir = Path(args.output_dir)
    config_path = Path(args.config) if args.config else None
    config = _load_config(config_path)
    config["no_auto_revise"] = args.no_auto_revise
    config["no_transfer"] = args.no_transfer

    spec_path = Path(args.spec) if args.spec else None
    outcome_path = Path(args.outcome) if args.outcome else None
    state_path = Path(args.state) if args.state else None

    # Load goal from state if not provided
    goal = args.goal
    if not goal and state_path and state_path.exists():
        state_data = json.loads(state_path.read_text())
        goal = state_data.get("goal", "")

    final_report = None
    for i in range(args.cycles):
        if i > 0:
            # For subsequent cycles, use the state from the previous cycle
            state_path = output_dir / "pipeline_state.json"
            spec_path = None  # Regenerate from state
            outcome_path = None

        final_report = run_pipeline(
            goal=goal,
            spec_path=spec_path,
            outcome_path=outcome_path,
            state_path=state_path,
            output_dir=output_dir,
            config=config,
            cycle_override=None
        )

    # Optionally verify chain after all cycles
    if args.verify_chain:
        chain_path = output_dir / "improvement_chain.json"
        if chain_path.exists():
            chain = json.loads(chain_path.read_text())
            result = verify_chain(chain)
            icon = "OK" if result["valid"] else "FAIL"
            log(f"Chain verification: {result['message']}", icon)

    return final_report


if __name__ == "__main__":
    main()
