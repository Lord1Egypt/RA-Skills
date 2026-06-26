#!/usr/bin/env python3
"""
Feedback Loop v2 — Observer
Normalizes any input into a standard observation.json.

Modes (auto-detected):
  standalone   — any JSON log, plain text, or prior observation.json
  enhanced     — + outcome_report.json from dark-factory
  full_triad   — + specification.json from intent-engineering

Usage:
  python observer.py --input log.json --goal "Process tickets in < 2 min"
  python observer.py --text "Script ran but missed 3 edge cases" --goal "Handle all inputs"
  python observer.py --observation prior_observation.json
  python observer.py --outcome outcome_report.json --spec specification.json
"""
import json
import re
import sys
import hashlib
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Optional


def log(msg: str, level: str = "INFO"):
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    icons = {"OK": "✓", "FAIL": "✗", "WARN": "⚠", "INFO": " ", "STAGE": "▶"}
    print(f"[{ts}] {icons.get(level, ' ')} {msg}")


def _obs_id() -> str:
    return f"obs-{hashlib.md5(str(datetime.now(timezone.utc).timestamp()).encode()).hexdigest()[:10]}"


# ── Metric extraction helpers ─────────────────────────────────────────────────

def _extract_metrics_json(data: dict) -> dict:
    m = {}
    for k in ("passed", "pass", "successes", "success_count"):
        if k in data and isinstance(data[k], (int, float)):
            m["passed"] = int(data[k]); break
    for k in ("failed", "fail", "failures", "failure_count"):
        if k in data and isinstance(data[k], (int, float)):
            m["failed"] = int(data[k]); break
    for k in ("pass_rate", "success_rate", "accuracy", "overall_pass_rate"):
        if k in data and isinstance(data[k], (int, float)):
            m["pass_rate"] = round(float(data[k]), 4); break
    for k in ("duration_ms", "duration", "elapsed_ms", "total_duration_ms", "execution_time"):
        if k in data and isinstance(data[k], (int, float)):
            m["duration_ms"] = float(data[k]); break
    for k in ("total", "total_count", "count", "total_scenarios"):
        if k in data and isinstance(data[k], (int, float)):
            m["total"] = int(data[k]); break
    # Derive pass_rate if missing
    if "pass_rate" not in m:
        if "passed" in m and "total" in m and m["total"] > 0:
            m["pass_rate"] = round(m["passed"] / m["total"], 4)
        elif "passed" in m and "failed" in m:
            t = m["passed"] + m["failed"]
            if t > 0:
                m["pass_rate"] = round(m["passed"] / t, 4)
                m.setdefault("total", t)
    return m


def _extract_failures_json(data: dict) -> list:
    out = []
    for key in ("failures", "errors", "failed_tests", "failed_scenarios", "edge_cases"):
        val = data.get(key)
        if isinstance(val, list):
            for item in val:
                if isinstance(item, dict):
                    out.append({
                        "description": (item.get("description") or item.get("scenario")
                                        or item.get("name") or item.get("test_id") or str(item)),
                        "input": item.get("input") or {},
                        "expected": item.get("expected_output") or item.get("expected") or {},
                        "actual": item.get("actual_output") or item.get("actual") or {},
                        "source": key
                    })
                elif isinstance(item, str):
                    out.append({"description": item, "input": {}, "expected": {}, "actual": {}, "source": key})
    return out


def _extract_metrics_text(text: str) -> dict:
    m = {}
    for pat in [r"(\d+(?:\.\d+)?)\s*%\s*pass", r"pass\s*rate[:\s]+(\d+(?:\.\d+)?)", r"(\d+(?:\.\d+)?)\s*%\s*success"]:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            v = float(match.group(1))
            m["pass_rate"] = round(v / 100 if v > 1 else v, 4); break
    match = re.search(r"(\d+)\s+passed", text, re.IGNORECASE)
    if match: m["passed"] = int(match.group(1))
    match = re.search(r"(\d+)\s+failed", text, re.IGNORECASE)
    if match: m["failed"] = int(match.group(1))
    for pat, mult in [(r"(\d+(?:\.\d+)?)\s*ms", 1), (r"(\d+(?:\.\d+)?)\s*second", 1000), (r"(\d+(?:\.\d+)?)\s*minute", 60000)]:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            m["duration_ms"] = float(match.group(1)) * mult; break
    return m


def _extract_failures_text(text: str) -> list:
    out = []
    for pat in [r"missed\s+(.+?)(?:\.|,|\n|$)", r"failed\s+to\s+(.+?)(?:\.|,|\n|$)",
                r"error[:\s]+(.+?)(?:\.|,|\n|$)", r"issue[:\s]+(.+?)(?:\.|,|\n|$)",
                r"bug[:\s]+(.+?)(?:\.|,|\n|$)", r"problem[:\s]+(.+?)(?:\.|,|\n|$)"]:
        for match in re.finditer(pat, text, re.IGNORECASE):
            desc = match.group(1).strip()
            if len(desc) > 3:
                out.append({"description": desc, "input": {}, "expected": {}, "actual": {}, "source": "text_extraction"})
    return out


# ── Mode-specific enrichment ──────────────────────────────────────────────────

def _enrich_from_outcome_report(obs: dict, outcome: dict) -> dict:
    """Enrich observation with dark-factory outcome_report.json fields."""
    perf = outcome.get("performance_metrics", {})
    if perf:
        obs["metrics"].update({k: v for k, v in perf.items() if k not in obs["metrics"]})
        if "overall_pass_rate" in perf and "pass_rate" not in obs["metrics"]:
            obs["metrics"]["pass_rate"] = perf["overall_pass_rate"]

    # Merge failures and edge cases
    obs["failures"] += _extract_failures_json(outcome)
    obs["edge_cases"] = outcome.get("edge_cases", [])

    # Carry over status and report metadata
    obs["outcome_status"] = outcome.get("status", "unknown")
    obs["outcome_report_id"] = outcome.get("report_id")
    obs["generated_code_files"] = len((outcome.get("generated_code") or {}).get("files", []))

    # Security evidence (if present — does not require provenable)
    sec = outcome.get("security_evidence", {})
    if sec:
        obs["security_evidence"] = sec

    obs["mode"] = "enhanced"
    return obs


def _enrich_from_specification(obs: dict, spec: dict) -> dict:
    """Enrich observation with intent-engineering specification.json fields."""
    obs["specification_id"] = spec.get("specification_id")
    obs["specification_title"] = spec.get("title")
    obs["specification_version"] = spec.get("version")

    # Use spec goal if no goal was provided
    if obs.get("goal") == "Not specified" and spec.get("description"):
        obs["goal"] = spec["description"]

    # Carry over success criteria for alignment checking
    obs["success_criteria"] = spec.get("success_criteria", {})

    # Carry over existing behavioral scenarios as baseline
    obs["baseline_scenarios"] = spec.get("behavioral_scenarios", [])
    obs["dependencies"] = spec.get("dependencies", [])

    obs["mode"] = "full_triad"
    return obs


# ── Main builder ──────────────────────────────────────────────────────────────

def build_observation(
    input_data: Any = None,
    text: str = None,
    prior_observation: dict = None,
    outcome_report: dict = None,
    specification: dict = None,
    goal: str = None,
    cycle: int = 1
) -> dict:
    """Build a normalized observation from any combination of inputs."""

    metrics = {}
    failures = []
    raw_input = {}
    source_type = "standalone"

    if prior_observation:
        source_type = "prior_observation"
        raw_input = prior_observation
        metrics = dict(prior_observation.get("metrics", {}))
        failures = list(prior_observation.get("failures", []))
        goal = goal or prior_observation.get("goal", "Not specified")
        cycle = prior_observation.get("cycle", 1) + 1

    elif input_data is not None:
        source_type = "json"
        raw_input = input_data if isinstance(input_data, dict) else {"raw": input_data}
        metrics = _extract_metrics_json(raw_input)
        failures = _extract_failures_json(raw_input)

    elif text:
        source_type = "text"
        raw_input = {"text": text}
        metrics = _extract_metrics_text(text)
        failures = _extract_failures_text(text)

    # Default mode is source_type; enrichment functions (_enrich_from_outcome_report,
    # _enrich_from_specification) will override obs["mode"] to "enhanced" or "full_triad"
    obs_mode = source_type

    # Compute health score
    health_score = None
    if "pass_rate" in metrics:
        health_score = round(metrics["pass_rate"], 4)
    elif "passed" in metrics and "total" in metrics and metrics["total"] > 0:
        health_score = round(metrics["passed"] / metrics["total"], 4)

    obs = {
        "observation_id": _obs_id(),
        "goal": goal or "Not specified",
        "cycle": cycle,
        "source_type": source_type,
        "mode": obs_mode,
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "metrics": metrics,
        "health_score": health_score,
        "failures": failures,
        "edge_cases": [f for f in failures if f.get("source") in ("edge_cases", "failed_scenarios")],
        "raw_input": raw_input,
        "regression_tests": []  # Populated by analyzer
    }

    # Enrich with dark-factory output if available
    if outcome_report:
        obs = _enrich_from_outcome_report(obs, outcome_report)

    # Enrich with intent-engineering spec if available
    if specification:
        obs = _enrich_from_specification(obs, specification)

    return obs


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Feedback Loop Observer — normalize any input into observation.json",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Modes (auto-detected from provided arguments):
  Standalone:   --input / --text / --observation
  Enhanced:     --outcome (dark-factory output)
  Full Triad:   --outcome + --spec (intent-engineering output)
        """
    )
    # Standalone inputs
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--input", help="Path to any JSON execution log")
    group.add_argument("--text", help="Plain text description of what happened")
    group.add_argument("--observation", help="Path to a prior observation.json (continue a cycle)")
    # Optional enrichment inputs
    parser.add_argument("--outcome", help="Path to dark-factory outcome_report.json (optional enrichment)")
    parser.add_argument("--spec", help="Path to intent-engineering specification.json (optional enrichment)")
    # Options
    parser.add_argument("--goal", help="The goal this observation is measured against")
    parser.add_argument("--cycle", type=int, default=1, help="Cycle number (default: 1)")
    parser.add_argument("--output", default="observation.json", help="Output path (default: observation.json)")
    args = parser.parse_args()

    log("OBSERVER", "STAGE")

    input_data = None
    prior_observation = None
    outcome_report = None
    specification = None
    text = args.text

    # Load standalone input
    if args.input:
        p = Path(args.input)
        if not p.exists():
            log(f"Input file not found: {p}", "FAIL"); sys.exit(1)
        try:
            input_data = json.loads(p.read_text())
            log(f"Loaded JSON input: {p}")
        except json.JSONDecodeError:
            text = p.read_text()
            log(f"Loaded text input: {p}")

    elif args.observation:
        p = Path(args.observation)
        if not p.exists():
            log(f"Observation file not found: {p}", "FAIL"); sys.exit(1)
        prior_observation = json.loads(p.read_text())
        log(f"Loaded prior observation: {p} (cycle {prior_observation.get('cycle', 1)})")

    # Load optional enrichment inputs
    if args.outcome:
        p = Path(args.outcome)
        if p.exists():
            outcome_report = json.loads(p.read_text())
            log(f"Loaded dark-factory outcome report: {p}")
        else:
            log(f"Outcome report not found: {p} — continuing in standalone mode", "WARN")

    if args.spec:
        p = Path(args.spec)
        if p.exists():
            specification = json.loads(p.read_text())
            log(f"Loaded intent-engineering specification: {p}")
        else:
            log(f"Specification not found: {p} — continuing without spec enrichment", "WARN")

    obs = build_observation(
        input_data=input_data,
        text=text,
        prior_observation=prior_observation,
        outcome_report=outcome_report,
        specification=specification,
        goal=args.goal,
        cycle=args.cycle
    )

    out_path = Path(args.output)
    out_path.write_text(json.dumps(obs, indent=2))

    log(f"Observation ID:  {obs['observation_id']}", "OK")
    log(f"Mode:            {obs['mode']}")
    log(f"Goal:            {obs['goal']}")
    log(f"Cycle:           {obs['cycle']}")
    log(f"Metrics:         {list(obs['metrics'].keys()) or 'none'}")
    log(f"Failures:        {len(obs['failures'])}")
    log(f"Health score:    {obs['health_score']}")
    log(f"Output:          {out_path}", "OK")


if __name__ == "__main__":
    main()
