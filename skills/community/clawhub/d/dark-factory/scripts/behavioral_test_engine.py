#!/usr/bin/env python3
"""
Dark Factory — Behavioral Test Engine
Executes behavioral scenarios from a specification against a mock environment.
Produces a detailed test report with pass rates and performance metrics.

Usage:
  python behavioral_test_engine.py <specification.json> [--output report.json]
"""
import json
import sys
import time
import random
import argparse
from pathlib import Path
from datetime import datetime, timezone


def log(msg: str, level: str = "INFO"):
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    prefix = {"OK": "✓ ", "FAIL": "✗ ", "WARN": "⚠ ", "INFO": "  ", "STAGE": "▶ "}.get(level, "  ")
    print(f"[{ts}] {prefix}{msg}")


def _mock_execute(scenario: dict) -> dict:
    """
    Mock execution of a behavioral scenario.
    In production, this is replaced by the AI agent executing the scenario.
    """
    start = time.time()
    # Simulate execution time (5–80ms)
    time.sleep(random.uniform(0.005, 0.08))
    duration_ms = round((time.time() - start) * 1000, 2)

    expected = scenario.get("expected_output", {})
    # Simulate a 96% pass rate for demo purposes
    passed = random.random() > 0.04

    return {
        "passed": passed,
        "actual_output": expected if passed else {"error": "mock_execution_divergence"},
        "duration_ms": duration_ms,
        "match_score": 1.0 if passed else round(random.uniform(0.3, 0.7), 3)
    }


def run_tests(spec: dict) -> dict:
    """Run all behavioral scenarios and return a full test report."""
    scenarios = spec.get("behavioral_scenarios", [])
    spec_id = spec.get("specification_id", "unknown")
    title = spec.get("title", "Unknown")
    target_pass_rate = spec.get("success_criteria", {}).get("test_pass_rate", 0.95)

    log(f"BEHAVIORAL TEST ENGINE", "STAGE")
    log(f"Specification: {title} ({spec_id})")
    log(f"Scenarios to run: {len(scenarios)}")
    log(f"Target pass rate: {target_pass_rate:.0%}")
    log("-" * 50)

    results = []
    for i, scenario in enumerate(scenarios):
        scenario_desc = scenario.get("scenario", f"Scenario {i+1}")
        log(f"Running [{i+1}/{len(scenarios)}]: {scenario_desc}")
        result = _mock_execute(scenario)
        status = "OK" if result["passed"] else "FAIL"
        log(f"  → {'PASS' if result['passed'] else 'FAIL'} ({result['duration_ms']}ms, match={result['match_score']})", status)
        results.append({
            "scenario_index": i + 1,
            "scenario": scenario_desc,
            "input": scenario.get("input", {}),
            "expected_output": scenario.get("expected_output", {}),
            "actual_output": result["actual_output"],
            "passed": result["passed"],
            "duration_ms": result["duration_ms"],
            "match_score": result["match_score"]
        })

    total = len(results)
    passed_count = sum(1 for r in results if r["passed"])
    failed_count = total - passed_count
    pass_rate = passed_count / total if total > 0 else 0.0
    avg_duration = sum(r["duration_ms"] for r in results) / total if total > 0 else 0.0
    meets_criteria = pass_rate >= target_pass_rate

    report = {
        "report_type": "behavioral_test_report",
        "specification_id": spec_id,
        "title": title,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total_scenarios": total,
            "passed": passed_count,
            "failed": failed_count,
            "pass_rate": round(pass_rate, 4),
            "target_pass_rate": target_pass_rate,
            "meets_success_criteria": meets_criteria,
            "avg_duration_ms": round(avg_duration, 2)
        },
        "scenario_results": results,
        "failed_scenarios": [r for r in results if not r["passed"]]
    }

    return report


def main():
    parser = argparse.ArgumentParser(description="Dark Factory Behavioral Test Engine")
    parser.add_argument("specification", help="Path to specification.json")
    parser.add_argument("--output", default=None, help="Output report path (default: <spec>_test_report.json)")
    args = parser.parse_args()

    spec_path = Path(args.specification)
    if not spec_path.exists():
        log(f"Specification file not found: {spec_path}", "FAIL")
        sys.exit(1)

    try:
        spec = json.loads(spec_path.read_text())
    except json.JSONDecodeError as e:
        log(f"Invalid JSON in specification: {e}", "FAIL")
        sys.exit(1)

    log("=" * 60)
    report = run_tests(spec)
    s = report["summary"]

    output_path = Path(args.output) if args.output else spec_path.parent / f"{spec_path.stem}_test_report.json"
    output_path.write_text(json.dumps(report, indent=2))

    log("=" * 60)
    log(f"TEST REPORT SUMMARY")
    log(f"  Total:      {s['total_scenarios']}")
    log(f"  Passed:     {s['passed']}")
    log(f"  Failed:     {s['failed']}")
    log(f"  Pass rate:  {s['pass_rate']:.1%} (target: {s['target_pass_rate']:.0%})")
    log(f"  Avg time:   {s['avg_duration_ms']}ms")
    log(f"  Criteria:   {'MET' if s['meets_success_criteria'] else 'NOT MET'}", "OK" if s["meets_success_criteria"] else "FAIL")
    log(f"  Report:     {output_path}", "OK")
    log("=" * 60)

    sys.exit(0 if s["meets_success_criteria"] else 1)


if __name__ == "__main__":
    main()
