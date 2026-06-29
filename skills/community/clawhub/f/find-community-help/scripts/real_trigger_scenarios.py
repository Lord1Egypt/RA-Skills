#!/usr/bin/env python3
"""Run realistic trigger-to-plan scenarios for find-community-help."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _report_utils import normalize_report_paths, temporary_workspace_dir


ROOT = SCRIPT_DIR.parent
SCENARIOS_PATH = ROOT / "assets" / "real_trigger_scenarios.json"
REPORT_PATH = ROOT / "assets" / "real_trigger_report.json"
SHOULD_TRAVEL = ROOT / "scripts" / "should_travel.py"
PLAN_TRAVEL = ROOT / "scripts" / "plan_travel.py"
TIMEOUT_SECONDS = 10
REQUIRED_DESCRIPTION_CONDITIONS = {
    "blocked_agent_work",
    "active_task_stalled",
    "looping",
    "version_sensitive",
    "known_issue_or_library_risk",
    "user_asks_official_or_community_guidance",
    "dry_run_only",
    "no_browsing",
    "no_durable_memory",
}
DURABLE_MEMORY_TERMS = [
    "long-term memory",
    "long term memory",
    "durable memory",
    "permanent memory",
    "core instructions",
    "system prompt",
]


def run_command(args: list[str]) -> dict[str, object]:
    try:
        proc = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False,
            timeout=TIMEOUT_SECONDS,
        )
        output = (proc.stdout + proc.stderr).strip()
        return {
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "output": output,
            "crashed": "Traceback" in output,
        }
    except subprocess.TimeoutExpired:
        return {
            "returncode": 1,
            "stdout": "",
            "output": f"TIMEOUT after {TIMEOUT_SECONDS}s",
            "crashed": True,
        }


def parse_json_output(result: dict[str, object]) -> dict[str, Any]:
    try:
        payload = json.loads(str(result.get("stdout") or "{}"))
        return payload if isinstance(payload, dict) else {}
    except json.JSONDecodeError:
        result["crashed"] = True
        return {}


def check_common(
    scenario: dict[str, Any],
    trigger_payload: dict[str, Any],
    plan_payload: dict[str, Any],
    trigger_result: dict[str, object],
    plan_result: dict[str, object],
) -> tuple[bool, list[str]]:
    errors: list[str] = []
    expected = scenario["expected"]
    decision = plan_payload.get("decision", {}) if isinstance(plan_payload.get("decision"), dict) else {}
    queries = plan_payload.get("queries", [])
    adoption_gates = plan_payload.get("adoption_gates", [])
    serialized_plan = json.dumps(plan_payload, ensure_ascii=False)
    description_conditions = set(scenario.get("description_conditions", []))

    if trigger_result["returncode"] != 0 or trigger_result["crashed"]:
        errors.append("trigger command failed or crashed")
    if plan_result["returncode"] != 0 or plan_result["crashed"]:
        errors.append("plan command failed or crashed")
    if not description_conditions:
        errors.append("scenario must declare description_conditions")
    if plan_payload.get("dry_run") is not True:
        errors.append("plan must stay dry_run")
    if plan_payload.get("network_used") is not False:
        errors.append("plan must not perform network access")
    for source, payload in (("trigger", trigger_payload), ("plan", decision)):
        if payload.get("should_run") != expected["should_run"]:
            errors.append(f"{source} should_run mismatch")
        if payload.get("search_mode") != expected["search_mode"]:
            errors.append(f"{source} search_mode mismatch")
        if payload.get("error_code") != expected.get("error_code"):
            errors.append(f"{source} error_code mismatch")
    if len(queries) != expected["query_count"]:
        errors.append("query count mismatch")
    if expected["should_run"]:
        if not isinstance(adoption_gates, list) or not adoption_gates:
            errors.append("positive plan must include adoption gates")
        if "explicit user authorization" not in serialized_plan:
            errors.append("positive plan must keep execution behind explicit user authorization")
        if "security scan" not in serialized_plan:
            errors.append("positive plan must mention platform safety or scan checks")

    query_tiers = [query.get("tier") for query in queries if isinstance(query, dict)]
    if expected["should_run"] and query_tiers:
        if query_tiers[0] != "primary":
            errors.append(f"first query tier must be primary: {query_tiers}")
        if len(query_tiers) > 1 and not any(tier != "primary" for tier in query_tiers):
            errors.append(f"query plan needs a non-primary cross-check tier: {query_tiers}")
    for term in scenario.get("forbidden_plan_terms", []):
        if term and term in serialized_plan:
            errors.append(f"leaked forbidden plan term: {term}")
    for term in DURABLE_MEMORY_TERMS:
        if term in serialized_plan.lower():
            errors.append(f"plan contains durable-memory instruction: {term}")

    return not errors, errors


def run_scenario(scenario: dict[str, Any], temp_dir: Path) -> dict[str, object]:
    state_path = temp_dir / f"{scenario['id']}.state.json"
    context_path = temp_dir / f"{scenario['id']}.context.txt"
    state_path.write_text(json.dumps(scenario["state"], ensure_ascii=False, indent=2), encoding="utf-8")
    context_path.write_text(str(scenario["thread_context"]), encoding="utf-8")

    trigger_result = run_command([sys.executable, str(SHOULD_TRAVEL), str(state_path)])
    plan_result = run_command([sys.executable, str(PLAN_TRAVEL), str(state_path), "--context", str(context_path)])
    trigger_payload = parse_json_output(trigger_result)
    plan_payload = parse_json_output(plan_result)
    common_ok, errors = check_common(scenario, trigger_payload, plan_payload, trigger_result, plan_result)

    return {
        "id": scenario["id"],
        "title": scenario["title"],
        "description_conditions": scenario.get("description_conditions", []),
        "ok": common_ok,
        "errors": errors,
        "trigger_payload": trigger_payload,
        "plan_decision": plan_payload.get("decision", {}),
        "query_tiers": [
            query.get("tier")
            for query in plan_payload.get("queries", [])
            if isinstance(query, dict)
        ],
        "query_count": len(plan_payload.get("queries", [])) if isinstance(plan_payload.get("queries", []), list) else None,
    }


def summarize(results: list[dict[str, object]]) -> dict[str, object]:
    coverage = {
        condition: [
            str(item["id"])
            for item in results
            if item["ok"] and condition in set(item.get("description_conditions", []))
        ]
        for condition in sorted(REQUIRED_DESCRIPTION_CONDITIONS)
    }
    missing = [condition for condition, ids in coverage.items() if not ids]
    return normalize_report_paths(
        {
            "total_cases": len(results),
            "passed_cases": sum(1 for item in results if item["ok"]),
            "failed_cases": [item["id"] for item in results if not item["ok"]],
            "required_description_conditions": sorted(REQUIRED_DESCRIPTION_CONDITIONS),
            "description_condition_coverage": coverage,
            "missing_description_conditions": missing,
            "results": results,
        }
    )


def main() -> int:
    scenarios = json.loads(SCENARIOS_PATH.read_text(encoding="utf-8"))
    with temporary_workspace_dir(ROOT, "find-community-help-real-trigger-") as temp:
        temp_dir = Path(temp)
        results = [run_scenario(scenario, temp_dir) for scenario in scenarios]

    summary = summarize(results)
    REPORT_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["passed_cases"] == summary["total_cases"] and not summary["missing_description_conditions"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
