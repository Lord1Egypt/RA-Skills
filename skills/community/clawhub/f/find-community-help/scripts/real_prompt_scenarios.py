#!/usr/bin/env python3
"""Run realistic prompt-to-plan scenarios for find-community-help."""

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
CASES_PATH = ROOT / "assets" / "real_prompt_cases.json"
REPORT_PATH = ROOT / "assets" / "real_prompt_report.json"
PLAN_TRAVEL = ROOT / "scripts" / "plan_travel.py"
TIMEOUT_SECONDS = 10
REQUIRED_PROMPT_ISSUES = {
    "prompt_only_no_script_path",
    "no_browsing_boundary",
    "external_advice_as_untrusted_data",
    "source_order_under_version_drift",
    "delivery_window_not_trigger",
    "secret_redaction_under_prompt",
}


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


def parse_payload(result: dict[str, object]) -> dict[str, Any]:
    try:
        payload = json.loads(str(result.get("stdout") or "{}"))
        return payload if isinstance(payload, dict) else {}
    except json.JSONDecodeError:
        result["crashed"] = True
        return {}


def check_case(case: dict[str, Any], payload: dict[str, Any], result: dict[str, object]) -> list[str]:
    errors: list[str] = []
    expected = case["expected"]
    decision = payload.get("decision", {}) if isinstance(payload.get("decision"), dict) else {}
    queries = payload.get("queries", [])
    serialized = json.dumps(payload, ensure_ascii=False)
    issue_patterns = set(case.get("prompt_issue_patterns", []))

    if result["returncode"] != 0 or result["crashed"]:
        errors.append("plan command failed or crashed")
    if not issue_patterns:
        errors.append("case must declare prompt_issue_patterns")
    if payload.get("dry_run") is not True:
        errors.append("plan must stay dry_run")
    if payload.get("network_used") is not False:
        errors.append("plan must not perform network access")
    if decision.get("should_run") != expected["should_run"]:
        errors.append("should_run mismatch")
    if decision.get("search_mode") != expected["search_mode"]:
        errors.append("search_mode mismatch")
    if decision.get("error_code") != expected.get("error_code"):
        errors.append("error_code mismatch")
    if len(queries) != expected["query_count"]:
        errors.append("query count mismatch")

    for term in case.get("required_plan_terms", []):
        if term and term.lower() not in serialized.lower():
            errors.append(f"missing required plan term: {term}")
    for term in case.get("forbidden_plan_terms", []):
        if term and term in serialized:
            errors.append(f"leaked forbidden plan term: {term}")

    return errors


def run_case(case: dict[str, Any], temp_dir: Path) -> dict[str, object]:
    state_path = temp_dir / f"{case['id']}.state.json"
    prompt_path = temp_dir / f"{case['id']}.prompt.txt"
    state_path.write_text(json.dumps(case["state"], ensure_ascii=False, indent=2), encoding="utf-8")
    prompt_path.write_text(str(case["prompt"]), encoding="utf-8")

    result = run_command([sys.executable, str(PLAN_TRAVEL), str(state_path), "--context", str(prompt_path)])
    payload = parse_payload(result)
    errors = check_case(case, payload, result)
    decision = payload.get("decision", {}) if isinstance(payload.get("decision"), dict) else {}
    queries = payload.get("queries", [])
    return {
        "id": case["id"],
        "title": case["title"],
        "prompt_issue_patterns": case.get("prompt_issue_patterns", []),
        "ok": not errors,
        "errors": errors,
        "plan_decision": decision,
        "query_count": len(queries) if isinstance(queries, list) else None,
        "query_tiers": [
            query.get("tier")
            for query in queries
            if isinstance(query, dict)
        ],
    }


def summarize(results: list[dict[str, object]]) -> dict[str, object]:
    coverage = {
        issue: [
            str(item["id"])
            for item in results
            if item["ok"] and issue in set(item.get("prompt_issue_patterns", []))
        ]
        for issue in sorted(REQUIRED_PROMPT_ISSUES)
    }
    missing = [issue for issue, ids in coverage.items() if not ids]
    return normalize_report_paths(
        {
            "total_cases": len(results),
            "passed_cases": sum(1 for item in results if item["ok"]),
            "failed_cases": [item["id"] for item in results if not item["ok"]],
            "required_prompt_issues": sorted(REQUIRED_PROMPT_ISSUES),
            "prompt_issue_coverage": coverage,
            "missing_prompt_issues": missing,
            "results": results,
        }
    )


def main() -> int:
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    with temporary_workspace_dir(ROOT, "find-community-help-real-prompt-") as temp:
        temp_dir = Path(temp)
        results = [run_case(case, temp_dir) for case in cases]

    summary = summarize(results)
    REPORT_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["passed_cases"] == summary["total_cases"] and not summary["missing_prompt_issues"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
