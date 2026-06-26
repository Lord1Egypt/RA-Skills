#!/usr/bin/env python3
"""
Unified Orchestrator v2 — Signal Router
Paradigm Shift 1: Specification Drift Detection
Paradigm Shift 5: Verifiable Improvement Chains

Responsibilities:
  - Compute drift_score between specification intent and observed outcomes
  - Detect semantic drift across multiple cycles
  - Build and verify cryptographic improvement chains
  - Route pipeline signals (trigger re-specification, meta-learning, etc.)

Usage:
  python signal_router.py drift --spec spec.json --analysis analysis.json
  python signal_router.py chain-append --chain improvement_chain.json --report improvement_report.json
  python signal_router.py verify --chain improvement_chain.json
  python signal_router.py route --state pipeline_state.json
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


def sha256_dict(data: dict) -> str:
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


# ── Paradigm Shift 1: Drift Detection ────────────────────────────────────────

def compute_drift_score(specification: dict, analysis: dict, outcome: Optional[dict] = None) -> dict:
    """
    Compute a drift score (0.0–1.0) measuring how far execution has wandered
    from the original specification intent.

    0.0 = perfect alignment (no drift)
    1.0 = complete misalignment (total drift)
    """
    drift_components = []
    drift_details = []

    success_criteria = specification.get("success_criteria", {})
    alignment = analysis.get("alignment", {})
    alignment_score = alignment.get("alignment_score", 1.0)
    performance_score = analysis.get("performance_score", 1.0)

    # Component 1: Alignment drift (how far from alignment_values thresholds)
    # alignment_score of 1.0 = no drift; 0.0 = maximum drift
    alignment_drift = round(1.0 - alignment_score, 4)
    drift_components.append(alignment_drift * 0.40)
    drift_details.append({
        "component": "alignment_drift",
        "weight": 0.40,
        "value": alignment_drift,
        "description": f"Alignment score is {alignment_score:.2f} (drift = {alignment_drift:.2f})"
    })

    # Component 2: Success criteria drift (spec said X, we got Y)
    criteria_drift = 0.0
    criteria_checks = []
    metrics = analysis.get("metrics_analyzed", [])
    obs_metrics = {}

    # Try to get actual metric values from the analysis
    if outcome:
        perf = outcome.get("performance_metrics", {})
        obs_metrics = {
            "pass_rate": perf.get("overall_pass_rate", perf.get("pass_rate")),
            "duration_ms": perf.get("total_duration_ms", perf.get("duration_ms")),
        }

    for criterion, target in success_criteria.items():
        if isinstance(target, (int, float)):
            actual = obs_metrics.get(criterion)
            if actual is not None:
                if target > 0:
                    gap = max(0.0, (target - actual) / target)
                else:
                    gap = 0.0
                criteria_checks.append({
                    "criterion": criterion,
                    "target": target,
                    "actual": actual,
                    "gap": round(gap, 4)
                })
                criteria_drift += gap

    if criteria_checks:
        criteria_drift = round(criteria_drift / len(criteria_checks), 4)
    drift_components.append(criteria_drift * 0.35)
    drift_details.append({
        "component": "criteria_drift",
        "weight": 0.35,
        "value": criteria_drift,
        "criteria_checks": criteria_checks,
        "description": f"Average gap from success criteria: {criteria_drift:.2f}"
    })

    # Component 3: Performance regression drift
    # If performance is declining across cycles, that signals drift from intent
    regression = analysis.get("regression", {})
    regression_drift = 0.0
    if regression.get("detected"):
        delta = abs(regression.get("delta", 0.0))
        regression_drift = min(1.0, delta * 3)  # Scale: 0.33 delta → 1.0 drift
    drift_components.append(regression_drift * 0.25)
    drift_details.append({
        "component": "regression_drift",
        "weight": 0.25,
        "value": regression_drift,
        "regression_detected": regression.get("detected", False),
        "description": f"Regression drift: {'detected' if regression.get('detected') else 'none'} (value: {regression_drift:.2f})"
    })

    total_drift = round(sum(drift_components), 4)

    # Classify drift severity
    if total_drift < 0.05:
        severity = "none"
        action = "continue"
    elif total_drift < 0.15:
        severity = "minor"
        action = "monitor"
    elif total_drift < 0.30:
        severity = "moderate"
        action = "respecify"
    elif total_drift < 0.50:
        severity = "significant"
        action = "respecify_urgent"
    else:
        severity = "critical"
        action = "respecify_urgent"

    return {
        "drift_score": total_drift,
        "severity": severity,
        "action": action,
        "components": drift_details,
        "specification_id": specification.get("specification_id"),
        "analysis_id": analysis.get("analysis_id"),
        "computed_at": datetime.now(timezone.utc).isoformat()
    }


def detect_cumulative_drift(drift_history: list) -> dict:
    """Analyze drift trends across multiple cycles to detect systemic drift."""
    if len(drift_history) < 2:
        return {"trend": "insufficient_data", "cycles_analyzed": len(drift_history)}

    scores = [d.get("drift_score", 0) for d in drift_history]
    trend_delta = scores[-1] - scores[0]
    avg_score = round(sum(scores) / len(scores), 4)

    # Detect monotonic increase (consistently worsening drift)
    increasing = all(scores[i] <= scores[i+1] for i in range(len(scores)-1))
    decreasing = all(scores[i] >= scores[i+1] for i in range(len(scores)-1))

    if increasing and trend_delta > 0.10:
        trend = "worsening"
    elif decreasing and trend_delta < -0.05:
        trend = "improving"
    elif abs(trend_delta) < 0.05:
        trend = "stable"
    else:
        trend = "volatile"

    return {
        "trend": trend,
        "trend_delta": round(trend_delta, 4),
        "average_drift": avg_score,
        "min_drift": round(min(scores), 4),
        "max_drift": round(max(scores), 4),
        "cycles_analyzed": len(drift_history),
        "scores": scores
    }


# ── Paradigm Shift 5: Verifiable Improvement Chains ──────────────────────────

def chain_append(chain: list, report: dict) -> tuple:
    """
    Append a new report to the improvement chain.
    Each link contains: report_id, report_hash, prior_hash, timestamp.
    Returns (updated_chain, link).
    """
    prior_hash = chain[-1]["report_hash"] if chain else "genesis"

    # Build the link payload (exclude integrity field to avoid circular hash)
    link_payload = {
        "report_id": report.get("report_id"),
        "prior_hash": prior_hash,
        "cycle": report.get("cycle", 1),
        "performance_score": report.get("summary", {}).get("performance_score"),
        "alignment_score": report.get("summary", {}).get("alignment_score"),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    link_hash = sha256_dict(link_payload)

    link = {
        **link_payload,
        "report_hash": link_hash
    }
    updated_chain = chain + [link]
    return updated_chain, link


def verify_chain(chain: list) -> dict:
    """
    Verify the integrity of an improvement chain by re-computing all hashes
    and checking that each link's prior_hash matches the previous link's report_hash.
    """
    if not chain:
        return {"valid": True, "links": 0, "message": "Empty chain — nothing to verify"}

    errors = []
    for i, link in enumerate(chain):
        # Re-compute expected hash
        payload = {k: v for k, v in link.items() if k != "report_hash"}
        expected_hash = sha256_dict(payload)
        actual_hash = link.get("report_hash", "")

        if expected_hash != actual_hash:
            errors.append(f"Link {i+1} (report_id={link.get('report_id')}): hash mismatch — expected {expected_hash[:16]}..., got {actual_hash[:16]}...")

        # Check prior_hash linkage
        if i > 0:
            expected_prior = chain[i-1]["report_hash"]
            actual_prior = link.get("prior_hash", "")
            if expected_prior != actual_prior:
                errors.append(f"Link {i+1}: prior_hash mismatch — chain broken between link {i} and {i+1}")

    return {
        "valid": len(errors) == 0,
        "links": len(chain),
        "errors": errors,
        "message": "Chain verified: all hashes valid. No tampering detected." if not errors else f"Chain INVALID: {len(errors)} error(s) found.",
        "verified_at": datetime.now(timezone.utc).isoformat()
    }


# ── Pipeline Signal Routing ───────────────────────────────────────────────────

def route_signals(state: dict, config: dict) -> dict:
    """
    Analyze the current pipeline state and emit routing signals for the next stage.
    Returns a signals dict that pipeline.py uses to decide what to do next.
    """
    signals = {
        "trigger_respecify": False,
        "trigger_meta_learning": False,
        "trigger_transfer": False,
        "trigger_chain_append": True,
        "respecify_reason": None,
        "meta_learning_reason": None
    }

    drift_threshold = config.get("drift_threshold", 0.15)
    auto_revise_threshold = config.get("auto_revise_after_n_failures", 3)
    min_cycles_for_meta = config.get("min_cycles_for_meta_learning", 3)

    # Signal: trigger re-specification
    drift_result = state.get("drift_result", {})
    if drift_result.get("action") in ("respecify", "respecify_urgent"):
        signals["trigger_respecify"] = True
        signals["respecify_reason"] = f"Drift score {drift_result.get('drift_score', 0):.3f} exceeds threshold {drift_threshold}"

    consecutive_failures = state.get("consecutive_failures", 0)
    if consecutive_failures >= auto_revise_threshold:
        signals["trigger_respecify"] = True
        signals["respecify_reason"] = f"{consecutive_failures} consecutive failures on same goal"

    # Signal: trigger meta-learning
    cycle = state.get("cycle", 1)
    if cycle >= min_cycles_for_meta:
        signals["trigger_meta_learning"] = True
        signals["meta_learning_reason"] = f"Cycle {cycle} reached minimum threshold ({min_cycles_for_meta})"

    # Signal: trigger cross-goal transfer (only on first cycle of a new goal)
    if cycle == 1 and not state.get("transfer_applied"):
        signals["trigger_transfer"] = True

    return signals


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Unified Orchestrator Signal Router")
    subparsers = parser.add_subparsers(dest="command")

    # drift command
    drift_parser = subparsers.add_parser("drift", help="Compute drift score")
    drift_parser.add_argument("--spec", required=True, help="Path to specification.json")
    drift_parser.add_argument("--analysis", required=True, help="Path to analysis.json")
    drift_parser.add_argument("--outcome", help="Path to outcome_report.json (optional)")
    drift_parser.add_argument("--output", default="drift_result.json")

    # chain-append command
    append_parser = subparsers.add_parser("chain-append", help="Append report to improvement chain")
    append_parser.add_argument("--chain", required=True, help="Path to improvement_chain.json")
    append_parser.add_argument("--report", required=True, help="Path to improvement_report.json")
    append_parser.add_argument("--output", help="Output path (default: overwrites --chain)")

    # verify command
    verify_parser = subparsers.add_parser("verify", help="Verify improvement chain integrity")
    verify_parser.add_argument("--chain", required=True, help="Path to improvement_chain.json")

    # route command
    route_parser = subparsers.add_parser("route", help="Compute routing signals from pipeline state")
    route_parser.add_argument("--state", required=True, help="Path to pipeline_state.json")
    route_parser.add_argument("--config", help="Path to pipeline_config.json")
    route_parser.add_argument("--output", default="signals.json")

    args = parser.parse_args()

    if args.command == "drift":
        spec = json.loads(Path(args.spec).read_text())
        analysis = json.loads(Path(args.analysis).read_text())
        outcome = json.loads(Path(args.outcome).read_text()) if args.outcome and Path(args.outcome).exists() else None
        result = compute_drift_score(spec, analysis, outcome)
        Path(args.output).write_text(json.dumps(result, indent=2))
        log(f"Drift score: {result['drift_score']:.4f} ({result['severity']}) → action: {result['action']}", "OK")
        log(f"Output: {args.output}", "OK")

    elif args.command == "chain-append":
        chain_path = Path(args.chain)
        chain = json.loads(chain_path.read_text()) if chain_path.exists() else []
        report = json.loads(Path(args.report).read_text())
        updated_chain, link = chain_append(chain, report)
        out_path = Path(args.output) if args.output else chain_path
        out_path.write_text(json.dumps(updated_chain, indent=2))
        log(f"Chain now has {len(updated_chain)} link(s). New hash: {link['report_hash'][:16]}...", "OK")

    elif args.command == "verify":
        chain_path = Path(args.chain)
        if not chain_path.exists():
            log(f"Chain file not found: {chain_path}", "FAIL"); sys.exit(1)
        chain = json.loads(chain_path.read_text())
        result = verify_chain(chain)
        icon = "OK" if result["valid"] else "FAIL"
        log(result["message"], icon)
        if not result["valid"]:
            for err in result["errors"]:
                log(f"  {err}", "FAIL")
            sys.exit(1)

    elif args.command == "route":
        state = json.loads(Path(args.state).read_text())
        config = {}
        if args.config and Path(args.config).exists():
            config = json.loads(Path(args.config).read_text())
        signals = route_signals(state, config)
        Path(args.output).write_text(json.dumps(signals, indent=2))
        log(f"Signals: respecify={signals['trigger_respecify']}, meta_learning={signals['trigger_meta_learning']}, transfer={signals['trigger_transfer']}", "OK")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
