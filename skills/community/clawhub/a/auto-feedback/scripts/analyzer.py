#!/usr/bin/env python3
"""
Feedback Loop v2 — Analyzer
Scores performance, detects regressions, generates improvement suggestions,
auto-creates regression tests, and checks goal alignment.

Works on any observation.json regardless of mode (standalone / enhanced / full_triad).

Usage:
  python analyzer.py --observation observation.json
  python analyzer.py --observation observation.json --output analysis.json
  python analyzer.py --observation observation.json --weights custom_weights.json
"""
import json
import sys
import hashlib
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional


def log(msg: str, level: str = "INFO"):
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    icons = {"OK": "✓", "FAIL": "✗", "WARN": "⚠", "INFO": " ", "STAGE": "▶"}
    print(f"[{ts}] {icons.get(level, ' ')} {msg}")


# ── Default scoring weights ───────────────────────────────────────────────────
# Override by passing --weights path/to/scoring_weights.json

DEFAULT_WEIGHTS = {
    "pass_rate": 0.50,
    "duration_ms": 0.20,   # lower is better; normalized against 5000ms baseline
    "failure_count": 0.20, # lower is better; normalized against 10 baseline
    "coverage": 0.10       # higher is better; 0-1 range
}

DEFAULT_ALIGNMENT_VALUES = {
    "principles": [
        "reliability",
        "performance",
        "correctness",
        "maintainability"
    ],
    "thresholds": {
        "min_pass_rate": 0.90,
        "max_duration_ms": 5000,
        "max_failures": 5
    }
}

DEFAULT_SUGGESTION_RULES = [
    {"condition": "pass_rate < 0.80", "priority": "critical", "suggestion": "Pass rate is critically low — review all failing scenarios immediately and add targeted fixes."},
    {"condition": "pass_rate < 0.90", "priority": "high", "suggestion": "Pass rate is below the 90% threshold — investigate and resolve failing test cases."},
    {"condition": "pass_rate < 0.95", "priority": "medium", "suggestion": "Pass rate is below 95% — review edge cases and add regression tests for known failures."},
    {"condition": "duration_ms > 10000", "priority": "high", "suggestion": "Execution time exceeds 10 seconds — profile the slowest operations and optimize."},
    {"condition": "duration_ms > 5000", "priority": "medium", "suggestion": "Execution time exceeds 5 seconds — consider caching or parallelization."},
    {"condition": "failure_count > 10", "priority": "high", "suggestion": "More than 10 failures detected — triage by severity and address critical failures first."},
    {"condition": "failure_count > 5", "priority": "medium", "suggestion": "More than 5 failures detected — review each failure and add regression tests."},
    {"condition": "regression_detected", "priority": "critical", "suggestion": "Performance regression detected vs. previous cycle — revert recent changes or add targeted fixes."},
]


# ── Performance scoring ───────────────────────────────────────────────────────

def compute_performance_score(metrics: dict, weights: dict) -> float:
    """Compute a 0.0-1.0 performance score from available metrics."""
    score_components = []
    total_weight = 0.0

    # Pass rate component (higher is better)
    if "pass_rate" in metrics:
        score_components.append(metrics["pass_rate"] * weights.get("pass_rate", 0.50))
        total_weight += weights.get("pass_rate", 0.50)

    # Duration component (lower is better; normalized against 5000ms baseline)
    if "duration_ms" in metrics:
        baseline = 5000.0
        duration_score = max(0.0, 1.0 - (metrics["duration_ms"] / baseline))
        score_components.append(duration_score * weights.get("duration_ms", 0.20))
        total_weight += weights.get("duration_ms", 0.20)

    # Failure count component (lower is better; normalized against 10 baseline)
    if "failed" in metrics:
        baseline = 10.0
        failure_score = max(0.0, 1.0 - (metrics["failed"] / baseline))
        score_components.append(failure_score * weights.get("failure_count", 0.20))
        total_weight += weights.get("failure_count", 0.20)

    if not score_components:
        return 0.5  # No metrics available — neutral score

    # Normalize by actual weight used
    raw_score = sum(score_components)
    if total_weight > 0:
        return round(raw_score / total_weight, 4)
    return round(raw_score, 4)


# ── Regression detection ──────────────────────────────────────────────────────

def detect_regression(current_score: float, prior_score: Optional[float]) -> dict:
    """Compare current score against prior cycle to detect regressions."""
    if prior_score is None:
        return {"detected": False, "delta": None, "prior_score": None}

    delta = round(current_score - prior_score, 4)
    detected = delta < -0.05  # More than 5% drop = regression

    return {
        "detected": detected,
        "delta": delta,
        "prior_score": prior_score,
        "current_score": current_score,
        "severity": "critical" if delta < -0.15 else "high" if delta < -0.05 else "none"
    }


# ── Improvement suggestions ───────────────────────────────────────────────────

def generate_suggestions(metrics: dict, failures: list, regression: dict, rules: list) -> list:
    """Generate prioritized improvement suggestions from metrics and failures."""
    suggestions = []
    seen = set()

    failure_count = len(failures)
    pass_rate = metrics.get("pass_rate", 1.0)
    duration_ms = metrics.get("duration_ms", 0)
    regression_detected = regression.get("detected", False)

    context = {
        "pass_rate": pass_rate,
        "duration_ms": duration_ms,
        "failure_count": failure_count,
        "regression_detected": regression_detected
    }

    for rule in rules:
        condition = rule["condition"]
        try:
            if eval(condition, {}, context):
                key = rule["suggestion"][:60]
                if key not in seen:
                    suggestions.append({
                        "priority": rule["priority"],
                        "suggestion": rule["suggestion"],
                        "condition_triggered": condition
                    })
                    seen.add(key)
        except Exception:
            pass

    # Add failure-specific suggestions
    for failure in failures[:5]:  # Top 5 failures
        desc = failure.get("description", "")
        if desc and desc[:40] not in seen:
            suggestions.append({
                "priority": "medium",
                "suggestion": f"Address failure: {desc}",
                "condition_triggered": "failure_present",
                "failure_detail": failure
            })
            seen.add(desc[:40])

    # Sort by priority
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    suggestions.sort(key=lambda s: priority_order.get(s["priority"], 4))

    return suggestions


# ── Regression test generation ────────────────────────────────────────────────

def generate_regression_tests(failures: list, edge_cases: list) -> list:
    """Auto-generate regression tests from failures and edge cases."""
    tests = []
    seen = set()

    all_cases = failures + [e for e in edge_cases if e not in failures]

    for case in all_cases:
        desc = case.get("description", "")
        if not desc or desc in seen:
            continue
        seen.add(desc)

        test = {
            "test_id": f"regression-{hashlib.md5(desc.encode()).hexdigest()[:8]}",
            "description": f"Regression test: {desc}",
            "input": case.get("input", {}),
            "expected_output": case.get("expected", {}),
            "actual_output_observed": case.get("actual", {}),
            "source": case.get("source", "failure"),
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
        tests.append(test)

    return tests


# ── Alignment check ───────────────────────────────────────────────────────────

def check_alignment(obs: dict, alignment_values: dict) -> dict:
    """Check observation against alignment values and success criteria."""
    thresholds = alignment_values.get("thresholds", {})
    principles = alignment_values.get("principles", [])
    metrics = obs.get("metrics", {})
    violations = []
    checks = []

    # Check pass rate threshold
    min_pass_rate = thresholds.get("min_pass_rate", 0.90)
    if "pass_rate" in metrics:
        ok = metrics["pass_rate"] >= min_pass_rate
        checks.append({"check": "pass_rate", "value": metrics["pass_rate"], "threshold": min_pass_rate, "passed": ok})
        if not ok:
            violations.append(f"Pass rate {metrics['pass_rate']:.1%} is below minimum {min_pass_rate:.1%}")

    # Check duration threshold
    max_duration = thresholds.get("max_duration_ms", 5000)
    if "duration_ms" in metrics:
        ok = metrics["duration_ms"] <= max_duration
        checks.append({"check": "duration_ms", "value": metrics["duration_ms"], "threshold": max_duration, "passed": ok})
        if not ok:
            violations.append(f"Duration {metrics['duration_ms']:.0f}ms exceeds maximum {max_duration}ms")

    # Check failure count threshold
    max_failures = thresholds.get("max_failures", 5)
    failure_count = len(obs.get("failures", []))
    ok = failure_count <= max_failures
    checks.append({"check": "failure_count", "value": failure_count, "threshold": max_failures, "passed": ok})
    if not ok:
        violations.append(f"Failure count {failure_count} exceeds maximum {max_failures}")

    # Check against success criteria (full triad mode)
    success_criteria = obs.get("success_criteria", {})
    if success_criteria:
        for criterion, target in success_criteria.items():
            if criterion in metrics:
                ok = metrics[criterion] >= target if isinstance(target, (int, float)) else True
                checks.append({"check": f"spec:{criterion}", "value": metrics[criterion], "threshold": target, "passed": ok})
                if not ok:
                    violations.append(f"Spec criterion '{criterion}': {metrics[criterion]} < {target}")

    # Compute alignment score
    if checks:
        passed = sum(1 for c in checks if c["passed"])
        alignment_score = round(passed / len(checks), 4)
    else:
        alignment_score = 1.0  # No checks = assume aligned

    return {
        "alignment_score": alignment_score,
        "principles": principles,
        "checks": checks,
        "violations": violations,
        "aligned": len(violations) == 0
    }


# ── Main analysis ─────────────────────────────────────────────────────────────

def analyze(observation: dict, weights: dict = None, alignment_values: dict = None, suggestion_rules: list = None) -> dict:
    """Run the full analysis on an observation."""
    weights = weights or DEFAULT_WEIGHTS
    alignment_values = alignment_values or DEFAULT_ALIGNMENT_VALUES
    suggestion_rules = suggestion_rules or DEFAULT_SUGGESTION_RULES

    metrics = observation.get("metrics", {})
    failures = observation.get("failures", [])
    edge_cases = observation.get("edge_cases", [])
    prior_score = observation.get("prior_performance_score")
    mode = observation.get("mode", "standalone")

    # Step 1: Score performance
    performance_score = compute_performance_score(metrics, weights)
    log(f"Performance score: {performance_score:.4f}")

    # Step 2: Detect regression
    regression = detect_regression(performance_score, prior_score)
    if regression["detected"]:
        log(f"Regression detected! Delta: {regression['delta']:.4f}", "WARN")

    # Step 3: Generate suggestions
    suggestions = generate_suggestions(metrics, failures, regression, suggestion_rules)
    log(f"Suggestions: {len(suggestions)} ({sum(1 for s in suggestions if s['priority'] == 'critical')} critical)")

    # Step 4: Auto-generate regression tests
    regression_tests = generate_regression_tests(failures, edge_cases)
    log(f"Regression tests generated: {len(regression_tests)}")

    # Step 5: Check alignment
    alignment = check_alignment(observation, alignment_values)
    log(f"Alignment score: {alignment['alignment_score']:.4f} ({'aligned' if alignment['aligned'] else 'violations found'})")

    analysis = {
        "analysis_id": f"analysis-{hashlib.md5(observation.get('observation_id', '').encode()).hexdigest()[:10]}",
        "observation_id": observation.get("observation_id"),
        "mode": mode,
        "analyzed_at": datetime.now(timezone.utc).isoformat(),
        "performance_score": performance_score,
        "prior_performance_score": prior_score,
        "regression": regression,
        "suggestions": suggestions,
        "suggestion_summary": {
            "critical": sum(1 for s in suggestions if s["priority"] == "critical"),
            "high": sum(1 for s in suggestions if s["priority"] == "high"),
            "medium": sum(1 for s in suggestions if s["priority"] == "medium"),
            "low": sum(1 for s in suggestions if s["priority"] == "low"),
        },
        "regression_tests": regression_tests,
        "alignment": alignment,
        "metrics_analyzed": list(metrics.keys()),
        "failures_analyzed": len(failures),
    }

    return analysis


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Feedback Loop Analyzer — analyze any observation.json")
    parser.add_argument("--observation", required=True, help="Path to observation.json")
    parser.add_argument("--weights", help="Path to custom scoring_weights.json (optional)")
    parser.add_argument("--alignment", help="Path to custom alignment_values.json (optional)")
    parser.add_argument("--rules", help="Path to custom suggestion_rules.json (optional)")
    parser.add_argument("--output", default="analysis.json", help="Output path (default: analysis.json)")
    args = parser.parse_args()

    log("ANALYZER", "STAGE")

    obs_path = Path(args.observation)
    if not obs_path.exists():
        log(f"Observation file not found: {obs_path}", "FAIL"); sys.exit(1)

    observation = json.loads(obs_path.read_text())
    log(f"Loaded observation: {observation.get('observation_id')} (mode: {observation.get('mode', 'standalone')})")

    # Load optional config overrides
    weights = DEFAULT_WEIGHTS
    if args.weights and Path(args.weights).exists():
        weights = json.loads(Path(args.weights).read_text())
        log(f"Loaded custom weights: {args.weights}")

    alignment_values = DEFAULT_ALIGNMENT_VALUES
    if args.alignment and Path(args.alignment).exists():
        alignment_values = json.loads(Path(args.alignment).read_text())
        log(f"Loaded custom alignment values: {args.alignment}")

    suggestion_rules = DEFAULT_SUGGESTION_RULES
    if args.rules and Path(args.rules).exists():
        suggestion_rules = json.loads(Path(args.rules).read_text())
        log(f"Loaded custom suggestion rules: {args.rules}")

    # Also try loading from references/ directory (relative to this script)
    skill_dir = Path(__file__).parent.parent
    for attr, filename, default in [
        ("weights", "scoring_weights.json", weights),
        ("alignment_values", "alignment_values.json", alignment_values),
    ]:
        ref_path = skill_dir / "references" / filename
        if ref_path.exists() and not getattr(args, attr.split("_")[0], None):
            try:
                loaded = json.loads(ref_path.read_text())
                if attr == "weights":
                    weights = loaded
                else:
                    alignment_values = loaded
                log(f"Loaded {filename} from references/")
            except Exception:
                pass

    analysis = analyze(observation, weights, alignment_values, suggestion_rules)

    out_path = Path(args.output)
    out_path.write_text(json.dumps(analysis, indent=2))

    log(f"Analysis ID:     {analysis['analysis_id']}", "OK")
    log(f"Performance:     {analysis['performance_score']:.4f}")
    log(f"Alignment:       {analysis['alignment']['alignment_score']:.4f}")
    log(f"Regression:      {'YES' if analysis['regression']['detected'] else 'no'}")
    log(f"Suggestions:     {len(analysis['suggestions'])} total")
    log(f"Regression tests:{len(analysis['regression_tests'])} generated")
    log(f"Output:          {out_path}", "OK")


if __name__ == "__main__":
    main()
