#!/usr/bin/env python3
"""
Feedback Loop v2 — Orchestrator
Runs all three stages (observe → analyze → improve) and produces a signed
improvement_report.json. Works standalone or with intent-engineering / dark-factory.

Usage:
  # Standalone
  python orchestrator.py --input log.json --goal "Process tickets in < 2 min"
  python orchestrator.py --text "Script ran but missed 3 edge cases" --goal "Handle all inputs"
  python orchestrator.py --observation prior_observation.json

  # Dark Factory enhanced
  python orchestrator.py --outcome outcome_report.json --goal "Achieve 98% pass rate"

  # Full Triad (intent-engineering + dark-factory)
  python orchestrator.py --outcome outcome_report.json --spec specification.json

  # Run from pre-built observation or analysis
  python orchestrator.py --observation observation.json
  python orchestrator.py --analysis analysis.json

  # Options
  python orchestrator.py --input log.json --goal "..." --output-dir ./reports/
"""
import json
import sys
import hashlib
import argparse
from pathlib import Path
from datetime import datetime, timezone

# Import sibling scripts
sys.path.insert(0, str(Path(__file__).parent))
from observer import build_observation
from analyzer import analyze


def log(msg: str, level: str = "INFO"):
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    icons = {"OK": "✓", "FAIL": "✗", "WARN": "⚠", "INFO": " ", "STAGE": "▶"}
    print(f"[{ts}] {icons.get(level, ' ')} {msg}")


def sha256(data: dict) -> str:
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


def build_improvement_report(observation: dict, analysis: dict, mode: str) -> dict:
    """Assemble the final signed improvement report."""
    suggestions = analysis.get("suggestions", [])
    regression_tests = analysis.get("regression_tests", [])
    alignment = analysis.get("alignment", {})

    # Determine overall health
    score = analysis.get("performance_score", 0)
    if score >= 0.95:
        health = "excellent"
    elif score >= 0.85:
        health = "good"
    elif score >= 0.70:
        health = "fair"
    else:
        health = "poor"

    # Build next steps
    next_steps = []
    critical = [s for s in suggestions if s["priority"] == "critical"]
    high = [s for s in suggestions if s["priority"] == "high"]

    if analysis.get("regression", {}).get("detected"):
        next_steps.append("URGENT: Performance regression detected — investigate and revert or fix before next cycle")
    if critical:
        next_steps.append(f"Address {len(critical)} critical improvement(s) immediately")
    if high:
        next_steps.append(f"Schedule work for {len(high)} high-priority improvement(s)")
    if regression_tests:
        next_steps.append(f"Add {len(regression_tests)} auto-generated regression test(s) to your test suite")
    if not alignment.get("aligned", True):
        next_steps.append(f"Resolve {len(alignment.get('violations', []))} alignment violation(s)")
    if not next_steps:
        next_steps.append("Continue monitoring — performance is healthy")
    next_steps.append("Run next cycle with updated_observation.json to continue the improvement loop")

    report = {
        "report_id": f"report-{hashlib.md5(analysis.get('analysis_id', '').encode()).hexdigest()[:10]}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "cycle": observation.get("cycle", 1),
        "goal": observation.get("goal", "Not specified"),
        "observation_id": observation.get("observation_id"),
        "analysis_id": analysis.get("analysis_id"),
        "summary": {
            "health": health,
            "performance_score": analysis.get("performance_score"),
            "alignment_score": alignment.get("alignment_score"),
            "regression_detected": analysis.get("regression", {}).get("detected", False),
            "total_suggestions": len(suggestions),
            "critical_suggestions": len(critical),
            "regression_tests_generated": len(regression_tests),
            "failures_analyzed": analysis.get("failures_analyzed", 0),
        },
        "metrics": observation.get("metrics", {}),
        "suggestions": suggestions,
        "regression_tests": regression_tests,
        "alignment": alignment,
        "next_steps": next_steps,
        "mode_details": {
            "standalone": "Ran with standalone inputs only",
            "enhanced": "Enriched with dark-factory outcome_report.json",
            "full_triad": "Enriched with dark-factory outcome_report.json + intent-engineering specification.json",
            "prior_observation": "Continued from a prior observation cycle"
        }.get(mode, mode)
    }

    # Sign the report
    report["integrity"] = {
        "sha256": sha256({k: v for k, v in report.items() if k != "integrity"}),
        "signed_at": datetime.now(timezone.utc).isoformat()
    }

    return report


def build_updated_observation(observation: dict, analysis: dict) -> dict:
    """Build an updated observation for the next cycle."""
    updated = dict(observation)
    updated["cycle"] = observation.get("cycle", 1) + 1
    updated["prior_performance_score"] = analysis.get("performance_score")
    updated["prior_alignment_score"] = analysis.get("alignment", {}).get("alignment_score")

    # Accumulate regression tests
    existing_tests = observation.get("regression_tests", [])
    new_tests = analysis.get("regression_tests", [])
    existing_ids = {t["test_id"] for t in existing_tests}
    for t in new_tests:
        if t["test_id"] not in existing_ids:
            existing_tests.append(t)
    updated["regression_tests"] = existing_tests

    # Clear per-cycle fields
    updated["failures"] = []
    updated["edge_cases"] = []
    updated["raw_input"] = {}
    updated["observed_at"] = datetime.now(timezone.utc).isoformat()

    return updated


def build_updated_specification(specification: dict, analysis: dict) -> dict:
    """Build an updated specification for intent-engineering (full triad mode only)."""
    updated = dict(specification)
    updated["version"] = _bump_version(specification.get("version", "1.0.0"))
    updated["updated_at"] = datetime.now(timezone.utc).isoformat()

    # Add new regression tests as behavioral scenarios
    existing_scenarios = updated.get("behavioral_scenarios", [])
    existing_ids = {s.get("scenario_id") for s in existing_scenarios}
    for test in analysis.get("regression_tests", []):
        if test["test_id"] not in existing_ids:
            existing_scenarios.append({
                "scenario_id": test["test_id"],
                "description": test["description"],
                "input": test["input"],
                "expected_output": test["expected_output"],
                "source": "feedback_loop_regression"
            })
    updated["behavioral_scenarios"] = existing_scenarios

    # Record improvement cycle
    cycles = updated.get("improvement_cycles", [])
    cycles.append({
        "cycle": analysis.get("observation_id", "unknown"),
        "performance_score": analysis.get("performance_score"),
        "alignment_score": analysis.get("alignment", {}).get("alignment_score"),
        "suggestions_applied": len(analysis.get("suggestions", [])),
        "regression_tests_added": len(analysis.get("regression_tests", [])),
        "timestamp": datetime.now(timezone.utc).isoformat()
    })
    updated["improvement_cycles"] = cycles

    return updated


def _bump_version(version: str) -> str:
    """Bump the patch version number."""
    try:
        parts = version.split(".")
        parts[-1] = str(int(parts[-1]) + 1)
        return ".".join(parts)
    except Exception:
        return version


# ── Main orchestration ────────────────────────────────────────────────────────

def run(
    input_path=None, text=None, observation_path=None, analysis_path=None,
    outcome_path=None, spec_path=None, goal=None, cycle=1, output_dir="."
) -> dict:
    """Run the full feedback loop pipeline."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # ── Stage 1: Observe ──────────────────────────────────────────────────────
    if analysis_path:
        log("Skipping observe/analyze — loading pre-built analysis", "INFO")
        analysis = json.loads(Path(analysis_path).read_text())
        observation = {"observation_id": analysis.get("observation_id"), "mode": analysis.get("mode", "standalone"),
                       "goal": goal or "Not specified", "cycle": cycle, "metrics": {}, "failures": [],
                       "edge_cases": [], "regression_tests": []}
        mode = analysis.get("mode", "standalone")
    else:
        log("Stage 1: OBSERVE", "STAGE")

        input_data = None
        prior_observation = None
        outcome_report = None
        specification = None
        input_text = text

        if observation_path:
            p = Path(observation_path)
            if p.exists():
                prior_observation = json.loads(p.read_text())
                log(f"Loaded prior observation: {p} (cycle {prior_observation.get('cycle', 1)})")
            else:
                log(f"Observation file not found: {p}", "FAIL"); sys.exit(1)

        elif input_path:
            p = Path(input_path)
            if not p.exists():
                log(f"Input file not found: {p}", "FAIL"); sys.exit(1)
            try:
                input_data = json.loads(p.read_text())
                log(f"Loaded JSON input: {p}")
            except json.JSONDecodeError:
                input_text = p.read_text()
                log(f"Loaded text input: {p}")

        if outcome_path:
            p = Path(outcome_path)
            if p.exists():
                outcome_report = json.loads(p.read_text())
                log(f"Loaded dark-factory outcome report: {p}")
            else:
                log(f"Outcome report not found: {p} — continuing in standalone mode", "WARN")

        if spec_path:
            p = Path(spec_path)
            if p.exists():
                specification = json.loads(p.read_text())
                log(f"Loaded intent-engineering specification: {p}")
            else:
                log(f"Specification not found: {p} — continuing without spec enrichment", "WARN")

        observation = build_observation(
            input_data=input_data,
            text=input_text,
            prior_observation=prior_observation,
            outcome_report=outcome_report,
            specification=specification,
            goal=goal,
            cycle=cycle
        )
        mode = observation.get("mode", "standalone")
        obs_file = out / "observation.json"
        obs_file.write_text(json.dumps(observation, indent=2))
        log(f"Observation saved: {obs_file}", "OK")

        # ── Stage 2: Analyze ──────────────────────────────────────────────────
        log("Stage 2: ANALYZE", "STAGE")

        # Load config from references/ if available
        skill_dir = Path(__file__).parent.parent
        weights = None
        alignment_values = None
        suggestion_rules = None
        for filename, varname in [("scoring_weights.json", "weights"), ("alignment_values.json", "alignment_values")]:
            ref_path = skill_dir / "references" / filename
            if ref_path.exists():
                try:
                    loaded = json.loads(ref_path.read_text())
                    if varname == "weights":
                        weights = loaded
                    else:
                        alignment_values = loaded
                    log(f"Loaded {filename} from references/")
                except Exception:
                    pass

        analysis = analyze(observation, weights, alignment_values, suggestion_rules)
        analysis_file = out / "analysis.json"
        analysis_file.write_text(json.dumps(analysis, indent=2))
        log(f"Analysis saved: {analysis_file}", "OK")

    # ── Stage 3: Improve ──────────────────────────────────────────────────────
    log("Stage 3: IMPROVE", "STAGE")

    report = build_improvement_report(observation, analysis, mode)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    report_file = out / f"improvement_report_{ts}.json"
    report_file.write_text(json.dumps(report, indent=2))
    log(f"Improvement report saved: {report_file}", "OK")

    updated_obs = build_updated_observation(observation, analysis)
    updated_obs_file = out / "updated_observation.json"
    updated_obs_file.write_text(json.dumps(updated_obs, indent=2))
    log(f"Updated observation saved: {updated_obs_file}", "OK")

    # Full triad: also update the specification
    if mode == "full_triad" and spec_path and Path(spec_path).exists():
        specification = json.loads(Path(spec_path).read_text())
        updated_spec = build_updated_specification(specification, analysis)
        updated_spec_file = out / "updated_specification.json"
        updated_spec_file.write_text(json.dumps(updated_spec, indent=2))
        log(f"Updated specification saved: {updated_spec_file}", "OK")
        # Also embed reference in the report for test assertions
        report["updated_specification"] = {"file": str(updated_spec_file), "version": updated_spec.get("version")}
        # Re-sign after adding updated_specification
        report["integrity"] = {
            "sha256": sha256({k: v for k, v in report.items() if k != "integrity"}),
            "signed_at": datetime.now(timezone.utc).isoformat()
        }
        # Overwrite the report file with the updated version
        report_file.write_text(json.dumps(report, indent=2))

    return report


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Feedback Loop Orchestrator — run the full feedback loop pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Modes (auto-detected):
  Standalone:   --input / --text / --observation
  Enhanced:     --outcome  (dark-factory output)
  Full Triad:   --outcome + --spec  (intent-engineering output)
  Pre-built:    --analysis  (skip observe/analyze stages)
        """
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--input", help="Path to any JSON execution log")
    group.add_argument("--text", help="Plain text description of what happened")
    group.add_argument("--observation", help="Path to a prior observation.json (continue a cycle)")
    group.add_argument("--analysis", help="Path to a pre-built analysis.json (skip observe/analyze)")
    parser.add_argument("--outcome", help="Path to dark-factory outcome_report.json (optional)")
    parser.add_argument("--spec", help="Path to intent-engineering specification.json (optional)")
    parser.add_argument("--goal", help="The goal this run is measured against")
    parser.add_argument("--cycle", type=int, default=1, help="Cycle number (default: 1)")
    parser.add_argument("--output-dir", default=".", help="Output directory (default: current dir)")
    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("  FEEDBACK LOOP v2")
    print("=" * 60)

    report = run(
        input_path=args.input,
        text=args.text,
        observation_path=args.observation,
        analysis_path=args.analysis,
        outcome_path=args.outcome,
        spec_path=args.spec,
        goal=args.goal,
        cycle=args.cycle,
        output_dir=args.output_dir
    )

    summary = report.get("summary", {})
    print("\n" + "=" * 60)
    print("  RESULTS")
    print("=" * 60)
    print(f"  Report ID:          {report['report_id']}")
    print(f"  Mode:               {report['mode']}")
    print(f"  Cycle:              {report['cycle']}")
    print(f"  Health:             {summary.get('health', 'unknown').upper()}")
    print(f"  Performance score:  {summary.get('performance_score', 'N/A')}")
    print(f"  Alignment score:    {summary.get('alignment_score', 'N/A')}")
    print(f"  Regression:         {'YES ⚠' if summary.get('regression_detected') else 'No'}")
    print(f"  Suggestions:        {summary.get('total_suggestions', 0)} ({summary.get('critical_suggestions', 0)} critical)")
    print(f"  Regression tests:   {summary.get('regression_tests_generated', 0)} generated")
    print(f"  Integrity SHA-256:  {report.get('integrity', {}).get('sha256', 'N/A')[:16]}...")
    print("=" * 60)

    if report.get("next_steps"):
        print("\n  NEXT STEPS:")
        for i, step in enumerate(report["next_steps"], 1):
            print(f"  {i}. {step}")
    print()


if __name__ == "__main__":
    main()
