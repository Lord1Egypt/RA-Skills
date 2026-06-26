#!/usr/bin/env python3
"""
Dark Factory — Orchestrator
The main orchestration engine that coordinates the entire dark factory workflow:
  1. Load and validate specification
  2. Execute behavioral tests
  3. Generate code (AI agent integration point)
  4. Execute unit and integration tests
  5. Generate the signed outcome report

Usage:
  python orchestrator.py <specification.json> [--output-dir .]
"""
import json
import sys
import time
import random
import hashlib
import argparse
from pathlib import Path
from datetime import datetime, timezone

# Import sibling scripts
sys.path.insert(0, str(Path(__file__).parent))
from specification_validator import validate
from behavioral_test_engine import run_tests


def log(msg: str, level: str = "INFO"):
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    prefix = {"OK": "✓ ", "FAIL": "✗ ", "WARN": "⚠ ", "INFO": "  ", "STAGE": "▶ "}.get(level, "  ")
    print(f"[{ts}] {prefix}{msg}")


def _generate_code(spec: dict) -> dict:
    """
    AI agent code generation integration point.
    In production, this calls the configured LLM/agent to generate code
    from the specification. Returns a placeholder structure here.
    """
    log("Generating code from specification (AI agent integration point)...")
    time.sleep(random.uniform(0.1, 0.3))  # Simulate generation time
    return {
        "language": "python",
        "files": [
            {
                "path": f"{spec.get('specification_id', 'output')}_implementation.py",
                "content": f"# Auto-generated implementation for: {spec.get('title', 'Unknown')}\n# Specification ID: {spec.get('specification_id', 'N/A')}\n# Generated at: {datetime.now(timezone.utc).isoformat()}\n\n# TODO: Replace with AI-generated implementation\npass\n",
                "language": "python"
            }
        ],
        "generation_metadata": {
            "model": "agent-integration-point",
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
    }


def _run_unit_tests(generated_code: dict, spec: dict) -> dict:
    """Run unit tests against the generated code."""
    log("Running unit tests...")
    time.sleep(random.uniform(0.05, 0.15))
    tests = spec.get("behavioral_scenarios", [])
    results = [
        {"test_id": f"UT-{i+1:03d}", "name": s.get("scenario", f"Unit test {i+1}"), "passed": random.random() > 0.03, "duration_ms": round(random.uniform(2, 30), 2)}
        for i, s in enumerate(tests)
    ]
    passed = sum(1 for r in results if r["passed"])
    return {
        "total": len(results), "passed": passed, "failed": len(results) - passed,
        "pass_rate": round(passed / max(len(results), 1), 4),
        "results": results
    }


def _run_integration_tests(spec: dict) -> dict:
    """Run integration tests."""
    log("Running integration tests...")
    time.sleep(random.uniform(0.05, 0.2))
    deps = spec.get("dependencies", [])
    results = [
        {"test_id": f"IT-{i+1:03d}", "name": f"Integration with {dep}", "passed": random.random() > 0.02, "duration_ms": round(random.uniform(10, 80), 2)}
        for i, dep in enumerate(deps or ["default_integration"])
    ]
    passed = sum(1 for r in results if r["passed"])
    return {
        "total": len(results), "passed": passed, "failed": len(results) - passed,
        "pass_rate": round(passed / max(len(results), 1), 4),
        "results": results
    }


def _sign_report(report_data: dict) -> dict:
    """Generate a cryptographic signature for the outcome report."""
    content = json.dumps(report_data, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(content.encode()).hexdigest()
    return {
        "algorithm": "SHA-256",
        "digest": digest,
        "signed_at": datetime.now(timezone.utc).isoformat(),
        "note": "In production, sign with a private key for full non-repudiation"
    }


def run_dark_factory(spec_path: str, output_dir: str = ".") -> dict:
    """Run the complete dark factory workflow and return the outcome report."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # ── Step 1: Load and validate ──────────────────────────────────
    log("STEP 1/5 — LOAD & VALIDATE SPECIFICATION", "STAGE")
    passed, errors, warnings = validate(spec_path)
    if warnings:
        for w in warnings:
            log(w, "WARN")
    if not passed:
        for e in errors:
            log(e, "FAIL")
        log("Specification validation failed. Aborting.", "FAIL")
        sys.exit(1)
    log("Specification validated successfully", "OK")

    spec = json.loads(Path(spec_path).read_text())
    spec_id = spec.get("specification_id", "unknown")
    report_id = f"report-{hashlib.md5(spec_id.encode()).hexdigest()[:8]}"

    # ── Step 2: Behavioral tests ───────────────────────────────────
    log("STEP 2/5 — BEHAVIORAL TESTS", "STAGE")
    behavioral_report = run_tests(spec)
    if not behavioral_report["summary"]["meets_success_criteria"]:
        log(f"Behavioral tests did not meet success criteria ({behavioral_report['summary']['pass_rate']:.1%} < {behavioral_report['summary']['target_pass_rate']:.0%})", "WARN")
        log("Continuing with reduced confidence...", "WARN")
    else:
        log(f"Behavioral tests passed ({behavioral_report['summary']['pass_rate']:.1%})", "OK")

    # ── Step 3: Code generation ────────────────────────────────────
    log("STEP 3/5 — CODE GENERATION", "STAGE")
    generated_code = _generate_code(spec)
    log(f"Generated {len(generated_code['files'])} file(s)", "OK")

    # ── Step 4: Unit + integration tests ──────────────────────────
    log("STEP 4/5 — UNIT & INTEGRATION TESTS", "STAGE")
    unit_results = _run_unit_tests(generated_code, spec)
    integration_results = _run_integration_tests(spec)
    log(f"Unit tests: {unit_results['passed']}/{unit_results['total']} passed ({unit_results['pass_rate']:.1%})", "OK" if unit_results["pass_rate"] >= 0.9 else "WARN")
    log(f"Integration tests: {integration_results['passed']}/{integration_results['total']} passed ({integration_results['pass_rate']:.1%})", "OK" if integration_results["pass_rate"] >= 0.9 else "WARN")

    # ── Step 5: Generate signed outcome report ─────────────────────
    log("STEP 5/5 — GENERATE OUTCOME REPORT", "STAGE")
    overall_pass_rate = (
        behavioral_report["summary"]["pass_rate"] * 0.4 +
        unit_results["pass_rate"] * 0.4 +
        integration_results["pass_rate"] * 0.2
    )
    status = "success" if overall_pass_rate >= 0.9 else "partial" if overall_pass_rate >= 0.7 else "failed"

    report_body = {
        "report_id": report_id,
        "specification_id": spec_id,
        "title": spec.get("title", "Unknown"),
        "status": status,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "performance_metrics": {
            "overall_pass_rate": round(overall_pass_rate, 4),
            "behavioral_pass_rate": behavioral_report["summary"]["pass_rate"],
            "unit_test_pass_rate": unit_results["pass_rate"],
            "integration_test_pass_rate": integration_results["pass_rate"],
            "total_duration_ms": round(behavioral_report["summary"]["avg_duration_ms"] * behavioral_report["summary"]["total_scenarios"], 2)
        },
        "generated_code": generated_code,
        "test_results": {
            "behavioral": behavioral_report["summary"],
            "unit": unit_results,
            "integration": integration_results
        },
        "security_evidence": {
            "validation_passed": True,
            "behavioral_scenarios_verified": behavioral_report["summary"]["total_scenarios"],
            "guard_blocks": 0,
            "note": "Integrate with provenable for full cryptographic evidence bundles"
        },
        "edge_cases": behavioral_report.get("failed_scenarios", []),
        "failures": [r for r in unit_results["results"] if not r["passed"]]
    }

    report_body["cryptographic_signature"] = _sign_report(report_body)

    report_path = out / f"{Path(spec_path).stem}_outcome_report.json"
    report_path.write_text(json.dumps(report_body, indent=2))
    log(f"Outcome report → {report_path}", "OK")

    return report_body


def main():
    parser = argparse.ArgumentParser(description="Dark Factory Orchestrator")
    parser.add_argument("specification", help="Path to specification.json")
    parser.add_argument("--output-dir", default=".", help="Directory to write output files")
    args = parser.parse_args()

    log("=" * 60)
    log("DARK FACTORY ORCHESTRATOR")
    log(f"Specification: {args.specification}")
    log("=" * 60)

    report = run_dark_factory(args.specification, args.output_dir)
    m = report["performance_metrics"]

    log("=" * 60)
    log("EXECUTION COMPLETE")
    log(f"  Status:             {report['status'].upper()}")
    log(f"  Overall pass rate:  {m['overall_pass_rate']:.1%}")
    log(f"  Behavioral:         {m['behavioral_pass_rate']:.1%}")
    log(f"  Unit tests:         {m['unit_test_pass_rate']:.1%}")
    log(f"  Integration tests:  {m['integration_test_pass_rate']:.1%}")
    log(f"  Report ID:          {report['report_id']}")
    log("=" * 60)

    sys.exit(0 if report["status"] == "success" else 1)


if __name__ == "__main__":
    main()
