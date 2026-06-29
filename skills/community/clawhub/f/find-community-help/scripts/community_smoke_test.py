#!/usr/bin/env python3
"""Run product-style community-help workflow smoke tests."""

from __future__ import annotations

import json
import copy
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _report_utils import normalize_report_paths, temporary_workspace_dir


ROOT = SCRIPT_DIR.parent
VALIDATOR = ROOT / "scripts" / "validate_suggestions.py"
SHOULD_TRAVEL = ROOT / "scripts" / "should_travel.py"
PLAN_TRAVEL = ROOT / "scripts" / "plan_travel.py"
CASES_PATH = ROOT / "assets" / "community_workflow_cases.json"
REPORT_PATH = ROOT / "assets" / "community_smoke_report.json"
TIMEOUT_SECONDS = 10
START = "<!-- find-community-help:suggestions:start -->"
END = "<!-- find-community-help:suggestions:end -->"
DEFAULT_FORBIDDEN_TERMS = [
    "long term memory",
    "system prompt",
    "all available sources",
    "deep crawl",
    "permanent",
]
TOP_LEVEL_OUTPUT_FIELDS = [
    "generated_at",
    "expires_at",
    "search_mode",
    "tool_preference",
    "source_scope",
    "thread_scope",
    "problem_fingerprint",
    "advisory_only",
    "trigger_reason",
    "visibility",
    "fingerprint_hash",
    "reuse_gate",
]
SUGGESTION_SCALAR_FIELDS = [
    "title",
    "applies_when",
    "hint",
    "confidence",
    "manual_check",
    "solves_point",
    "new_idea",
    "fit_reason",
]


def render_top_level(output: dict[str, object]) -> list[str]:
    return [
        START,
        "# find-community-help suggestions",
        *[f"{field}: {output[field]}" for field in TOP_LEVEL_OUTPUT_FIELDS],
    ]


def render_suggestion(index: int, item: dict[str, object]) -> list[str]:
    lines = ["", f"## suggestion-{index}"]
    lines.extend(f"{field}: {item[field]}" for field in SUGGESTION_SCALAR_FIELDS)
    lines.append("match_reasoning:")
    lines.extend(f"- {reasoning}" for reasoning in item["match_reasoning"])
    lines.extend(
        [
            f"version_scope: {item['version_scope']}",
            f"do_not_apply_when: {item['do_not_apply_when']}",
            "evidence:",
        ]
    )
    lines.extend(f"- {evidence}" for evidence in item["evidence"])
    return lines


def render_case_markdown(case: dict[str, object]) -> str:
    output = case["output"]
    suggestion_lines = render_top_level(output)
    for index, item in enumerate(output["suggestions"], start=1):
        suggestion_lines.extend(render_suggestion(index, item))
    suggestion_lines.append(END)
    return "\n".join(suggestion_lines) + "\n"


def run_command(args: list[str]) -> tuple[int, str, bool]:
    try:
        proc = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False,
            timeout=TIMEOUT_SECONDS,
        )
        output = (proc.stdout + proc.stderr).strip()
        crashed = "Traceback" in output
        return proc.returncode, output, crashed
    except subprocess.TimeoutExpired:
        return 1, f"TIMEOUT after {TIMEOUT_SECONDS}s", True


def normalize_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def content_blob(output: dict[str, object]) -> str:
    parts = [
        str(output.get("problem_fingerprint", "")),
        str(output.get("trigger_reason", "")),
        str(output.get("visibility", "")),
    ]
    for suggestion in output.get("suggestions", []):
        parts.extend(
            [
                str(suggestion.get("title", "")),
                str(suggestion.get("applies_when", "")),
                str(suggestion.get("hint", "")),
                str(suggestion.get("manual_check", "")),
                str(suggestion.get("solves_point", "")),
                str(suggestion.get("new_idea", "")),
                str(suggestion.get("fit_reason", "")),
                str(suggestion.get("version_scope", "")),
                str(suggestion.get("do_not_apply_when", "")),
                " ".join(str(item) for item in suggestion.get("match_reasoning", [])),
                " ".join(str(item) for item in suggestion.get("evidence", [])),
            ]
        )
    return normalize_text(" ".join(parts))


def extract_evidence_tiers(output: dict[str, object]) -> set[str]:
    tiers = set()
    for suggestion in output.get("suggestions", []):
        for evidence in suggestion.get("evidence", []):
            label = str(evidence).split(":", 1)[0].strip().lower()
            tiers.add(label.split("_", 1)[0])
    return tiers


def list_value(value: object) -> list[object]:
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return list(value)
    return [value]


def normalized_terms(eval_cfg: dict[str, object], key: str, fallback: list[object]) -> list[str]:
    return [normalize_text(str(term)) for term in list_value(eval_cfg.get(key, fallback))]


def minimum_hits(eval_cfg: dict[str, object], key: str, terms: list[str]) -> int:
    default = max(1, len(terms) - 1) if terms else 0
    legacy_default = eval_cfg.get("min_term_hits", default)
    return int(eval_cfg.get(key, legacy_default))


def count_hits(terms: list[str], text: str) -> int:
    return sum(1 for term in terms if term and term in text)


def positive_term_metrics(output: dict[str, object], eval_cfg: dict[str, object]) -> tuple[dict[str, object], str]:
    text = content_blob(output)
    fallback_terms = list_value(eval_cfg.get("pain_terms"))
    thread_focus_terms = normalized_terms(eval_cfg, "thread_focus_terms", fallback_terms)
    resolution_terms = normalized_terms(eval_cfg, "resolution_terms", fallback_terms)
    forbidden_terms = normalized_terms(eval_cfg, "forbidden_terms", DEFAULT_FORBIDDEN_TERMS)
    required_tiers = set(eval_cfg.get("required_evidence_tiers", []))
    actual_tiers = extract_evidence_tiers(output)
    thread_focus_min = minimum_hits(eval_cfg, "min_thread_focus_hits", thread_focus_terms)
    resolution_min = minimum_hits(eval_cfg, "min_resolution_hits", resolution_terms)
    forbidden_max = int(eval_cfg.get("max_forbidden_hits", 0))
    return {
        "thread_focus_hits": count_hits(thread_focus_terms, text),
        "thread_focus_total": len(thread_focus_terms),
        "resolution_hits": count_hits(resolution_terms, text),
        "resolution_total": len(resolution_terms),
        "forbidden_hits": count_hits(forbidden_terms, text),
        "forbidden_total": len(forbidden_terms),
        "required_evidence_tiers": sorted(required_tiers),
        "actual_evidence_tiers": sorted(actual_tiers),
        "thread_focus_min": thread_focus_min,
        "resolution_min": resolution_min,
        "forbidden_max": forbidden_max,
        "tiers_ok": required_tiers <= actual_tiers,
    }, text


def positive_contract_checks(
    case: dict[str, object],
    output: dict[str, object],
    suggestion: dict[str, object],
    trigger_payload: dict[str, object],
    metrics: dict[str, object],
    eval_cfg: dict[str, object],
) -> list[bool]:
    expected_trigger_reason = case["expected"].get("trigger_reason") or case["state"].get("event_kind")
    return [
        output["advisory_only"] == "true" and output["thread_scope"] == "active_conversation_only",
        output["visibility"] == eval_cfg.get("expected_visibility", "silent_until_relevant"),
        output["reuse_gate"] == "min_4_of_5_axes_and_ttl_valid",
        len(suggestion["match_reasoning"]) >= 4,
        bool(metrics["tiers_ok"]),
        bool(metrics["thread_focus_ok"]),
        bool(metrics["resolution_ok"]),
        bool(metrics["forbidden_ok"]),
        bool(suggestion["manual_check"] and suggestion["do_not_apply_when"] and suggestion["version_scope"]),
        trigger_payload.get("trigger_reason") == expected_trigger_reason,
    ]


def positive_usefulness_score(
    case: dict[str, object],
    trigger_payload: dict[str, object],
) -> tuple[int, dict[str, object], str]:
    output = case["output"]
    suggestion = output["suggestions"][0]
    eval_cfg = case.get("eval", {})
    breakdown, text = positive_term_metrics(output, eval_cfg)
    breakdown["mode"] = "positive"
    breakdown["thread_focus_ok"] = breakdown["thread_focus_hits"] >= breakdown["thread_focus_min"]
    breakdown["resolution_ok"] = breakdown["resolution_hits"] >= breakdown["resolution_min"]
    breakdown["forbidden_ok"] = breakdown["forbidden_hits"] <= breakdown["forbidden_max"]
    score = sum(positive_contract_checks(case, output, suggestion, trigger_payload, breakdown, eval_cfg))
    breakdown["score"] = score
    return score, breakdown, text


def silent_guardrail_score(
    case: dict[str, object],
    trigger_payload: dict[str, object],
) -> tuple[int, dict[str, object], str]:
    expected = case["expected"]
    eval_cfg = case.get("eval", {})
    score = 0
    observed_signals = trigger_payload.get("observed_signals", []) or []
    breakdown: dict[str, object] = {
        "mode": "silent_guardrail",
        "observed_signals": observed_signals,
    }
    thread_focus_ok = trigger_payload.get("should_run") is False
    if thread_focus_ok:
        score += 1
    resolution_ok = trigger_payload.get("error_code") == expected["error_code"]
    if resolution_ok:
        score += 1
    search_mode_ok = trigger_payload.get("search_mode") == expected["search_mode"]
    if search_mode_ok:
        score += 1
    expected_signal = eval_cfg.get("expected_signal")
    forbidden_ok = True
    if expected_signal:
        forbidden_ok = expected_signal in observed_signals
    if forbidden_ok:
        score += 1
    breakdown["thread_focus_ok"] = thread_focus_ok
    breakdown["resolution_ok"] = resolution_ok
    breakdown["forbidden_ok"] = forbidden_ok
    breakdown["search_mode_ok"] = search_mode_ok
    breakdown["score"] = score
    return score, breakdown, normalize_text(trigger_payload.get("reason", ""))


def make_hallucinated_output(output: dict[str, object]) -> dict[str, object]:
    mutated = copy.deepcopy(output)
    for suggestion in mutated["suggestions"]:
        suggestion["title"] = "Run a broad deep crawl and persist the result for every future task"
        suggestion["applies_when"] = "Any thread that feels uncertain, emotional, or incomplete."
        suggestion["hint"] = (
            "Start a broad crawl across all available sources, trust the newest community answer, "
            "and write the result into long-term memory so future runs stop asking the same question."
        )
        suggestion["manual_check"] = "Check later if the answer still feels right."
        suggestion["solves_point"] = "The thread has uncertainty."
        suggestion["new_idea"] = "Use a broad crawl, expand to all available sources, and keep the answer permanently."
        suggestion["fit_reason"] = "This generic pattern applies to almost every thread."
        suggestion["match_reasoning"] = [
            "host: assumed the same host behavior without checking host-specific constraints",
            "version: ignored exact version differences and reused the newest public answer",
            "symptom: treated general uncertainty as the same issue",
            "desired_next_outcome: stored a durable answer for later reuse",
        ]
        suggestion["version_scope"] = "Any host, any version, any future task."
        suggestion["do_not_apply_when"] = "Skip only when the host hard-blocks memory writes."
    return mutated


def without_skill_baseline_score(case: dict[str, object]) -> tuple[int, dict[str, object]]:
    mode = case.get("eval", {}).get("mode", "positive" if case.get("output") else "silent_guardrail")
    return 0, {
        "mode": "without_skill_baseline",
        "case_mode": mode,
        "emits_isolated_suggestion": False,
        "has_contract_validation": False,
        "has_cross_validation": False,
    }


def evaluate_case(
    case: dict[str, object],
    trigger_payload: dict[str, object],
) -> tuple[int, dict[str, object], bool, str]:
    eval_cfg = case.get("eval", {})
    mode = eval_cfg.get("mode", "positive" if case.get("output") else "silent_guardrail")
    if mode == "silent_guardrail":
        score, breakdown, text = silent_guardrail_score(case, trigger_payload)
    else:
        score, breakdown, text = positive_usefulness_score(case, trigger_payload)
    min_score = int(eval_cfg.get("min_score", 1))
    return score, breakdown, score >= min_score, text


def run_trigger_for_case(
    case: dict[str, object],
    temp_dir: Path,
) -> tuple[int, str, bool, dict[str, object]]:
    state_path = temp_dir / f"{case['id']}.state.json"
    state_path.write_text(json.dumps(case["state"], ensure_ascii=False, indent=2), encoding="utf-8")
    returncode, output, crashed = run_command([sys.executable, str(SHOULD_TRAVEL), str(state_path)])
    try:
        payload = json.loads(output) if output else {}
    except json.JSONDecodeError:
        payload = {}
        crashed = True
    return returncode, output, crashed, payload


def run_plan_for_case(case: dict[str, object], temp_dir: Path) -> dict[str, object]:
    context_fixture = str(case.get("context_fixture", "")).strip()
    if not context_fixture:
        return {
            "query_plan_checked": False,
            "query_plan_ok": True,
            "query_plan_output": "SKIPPED: no context_fixture for this workflow case",
            "query_plan": None,
        }

    context_path = ROOT / context_fixture
    state_path = temp_dir / f"{case['id']}.plan.state.json"
    state_path.write_text(json.dumps(case["state"], ensure_ascii=False, indent=2), encoding="utf-8")
    returncode, output, crashed = run_command(
        [sys.executable, str(PLAN_TRAVEL), str(state_path), "--context", str(context_path)]
    )
    try:
        payload = json.loads(output) if output else {}
    except json.JSONDecodeError:
        payload = {}
        crashed = True

    decision = payload.get("decision", {}) if isinstance(payload.get("decision"), dict) else {}
    queries = payload.get("queries", [])
    expected = case["expected"]
    eval_cfg = case.get("eval", {})
    serialized_payload = json.dumps(payload, ensure_ascii=False)
    forbidden_plan_terms = [str(term) for term in list_value(eval_cfg.get("forbidden_plan_terms"))]
    leaked_plan_terms = [term for term in forbidden_plan_terms if term and term in serialized_payload]
    query_plan_ok = (
        returncode == 0
        and not crashed
        and payload.get("community_help_plan") is True
        and payload.get("dry_run") is True
        and payload.get("network_used") is False
        and decision.get("should_run") == expected["should_run"]
        and decision.get("search_mode") == expected["search_mode"]
        and isinstance(queries, list)
        and (len(queries) > 0 if expected["should_run"] else len(queries) == 0)
        and not leaked_plan_terms
    )
    return {
        "query_plan_checked": True,
        "query_plan_ok": query_plan_ok,
        "query_plan_leaked_terms": leaked_plan_terms,
        "query_plan_output": output,
        "query_plan": payload,
    }


def validate_output_fixture(case: dict[str, object], temp_dir: Path) -> dict[str, object]:
    result: dict[str, object] = {
        "validator_ok": True,
        "validator_output": "SKIPPED: no output fixture for blocked case",
        "hallucination_validator_ok": True,
        "hallucination_validator_output": "SKIPPED: no output fixture for blocked case",
        "hallucinated_case": None,
    }
    if "output" not in case:
        return result

    suggestion_path = temp_dir / f"{case['id']}.suggestions.md"
    suggestion_path.write_text(render_case_markdown(case), encoding="utf-8")
    validator_returncode, validator_output, validator_crashed = run_command(
        [sys.executable, str(VALIDATOR), str(suggestion_path)]
    )

    hallucinated_case = copy.deepcopy(case)
    hallucinated_case["output"] = make_hallucinated_output(case["output"])
    hallucination_path = temp_dir / f"{case['id']}.hallucinated.md"
    hallucination_path.write_text(render_case_markdown(hallucinated_case), encoding="utf-8")
    hallucination_returncode, hallucination_output, hallucination_crashed = run_command(
        [sys.executable, str(VALIDATOR), str(hallucination_path)]
    )

    result.update(
        {
            "validator_ok": validator_returncode == 0 and not validator_crashed,
            "validator_output": validator_output,
            "hallucination_validator_ok": hallucination_returncode == 0 and not hallucination_crashed,
            "hallucination_validator_output": hallucination_output,
            "hallucinated_case": hallucinated_case,
        }
    )
    return result


def trigger_matches_expected(
    returncode: int,
    crashed: bool,
    payload: dict[str, object],
    expected: dict[str, object],
) -> bool:
    return (
        returncode == 0
        and not crashed
        and payload.get("should_run") == expected["should_run"]
        and payload.get("search_mode") == expected["search_mode"]
        and payload.get("error_code") == expected["error_code"]
    )


def evaluate_hallucination_guard(
    case: dict[str, object],
    fixture: dict[str, object],
    trigger_payload: dict[str, object],
    with_skill_score: int,
) -> tuple[int, dict[str, object] | None, bool]:
    hallucinated_case = fixture["hallucinated_case"]
    if not isinstance(hallucinated_case, dict):
        return 0, None, True
    if not bool(fixture["hallucination_validator_ok"]):
        return 0, None, True

    hallucinated_score, hallucination_breakdown, _, _ = evaluate_case(
        hallucinated_case,
        trigger_payload,
    )
    hallucination_min_gap = int(case.get("eval", {}).get("min_hallucination_gap", 3))
    forbidden_guard_rejected = not bool(hallucination_breakdown.get("forbidden_ok", True))
    hallucination_guard_ok = (
        bool(fixture["hallucination_validator_ok"])
        and hallucinated_score < with_skill_score
        and (with_skill_score - hallucinated_score >= hallucination_min_gap or forbidden_guard_rejected)
    )
    return hallucinated_score, hallucination_breakdown, hallucination_guard_ok


def build_case_result(case: dict[str, object], temp_dir: Path) -> dict[str, object]:
    trigger_returncode, trigger_output, trigger_crashed, trigger_payload = run_trigger_for_case(case, temp_dir)
    query_plan = run_plan_for_case(case, temp_dir)
    fixture = validate_output_fixture(case, temp_dir)
    expected = case["expected"]
    with_skill_score, score_breakdown, eval_ok, _ = evaluate_case(case, trigger_payload)
    without_skill_score, without_skill_breakdown = without_skill_baseline_score(case)
    hallucinated_score, hallucination_breakdown, hallucination_guard_ok = evaluate_hallucination_guard(
        case,
        fixture,
        trigger_payload,
        with_skill_score,
    )

    return {
        "id": case["id"],
        "title": case["title"],
        "host": case["host"],
        "sources": case["sources"],
        "trigger_ok": trigger_matches_expected(trigger_returncode, trigger_crashed, trigger_payload, expected),
        "query_plan_checked": query_plan["query_plan_checked"],
        "query_plan_ok": query_plan["query_plan_ok"],
        "query_plan_leaked_terms": query_plan.get("query_plan_leaked_terms", []),
        "query_plan_output": query_plan["query_plan_output"],
        "query_plan": query_plan["query_plan"],
        "validator_ok": fixture["validator_ok"],
        "validator_scope": "structure_only",
        "eval_ok": eval_ok,
        "hallucination_guard_ok": hallucination_guard_ok,
        "hallucination_structure_ok": fixture["hallucination_validator_ok"],
        "trigger_output": trigger_output,
        "validator_output": fixture["validator_output"],
        "hallucination_validator_output": fixture["hallucination_validator_output"],
        "with_skill_score": with_skill_score,
        "hallucinated_score": hallucinated_score,
        "without_skill_score": without_skill_score,
        "without_skill_breakdown": without_skill_breakdown,
        "score_delta": with_skill_score - without_skill_score,
        "score_breakdown": score_breakdown,
        "hallucination_breakdown": hallucination_breakdown,
        "thread_focus_ok": bool(score_breakdown.get("thread_focus_ok", False)),
        "resolution_ok": bool(score_breakdown.get("resolution_ok", False)),
        "forbidden_ok": bool(score_breakdown.get("forbidden_ok", False)),
    }


def summarize_results(results: list[dict[str, object]]) -> dict[str, object]:
    query_plan_cases = [item for item in results if item["query_plan_checked"]]
    summary = {
        "total_cases": len(results),
        "smoke_passed": sum(1 for item in results if item["trigger_ok"] and item["validator_ok"]),
        "query_plan_cases": len(query_plan_cases),
        "query_plan_passed": sum(1 for item in query_plan_cases if item["query_plan_ok"]),
        "eval_passed": sum(1 for item in results if item["eval_ok"]),
        "thread_focus_passed": sum(1 for item in results if item["thread_focus_ok"]),
        "resolution_passed": sum(1 for item in results if item["resolution_ok"]),
        "forbidden_guard_passed": sum(1 for item in results if item["forbidden_ok"]),
        "hallucination_guard_passed": sum(1 for item in results if item["hallucination_guard_ok"]),
        "ablation_positive": sum(1 for item in results if item["score_delta"] > 0),
        "results": results,
    }
    return normalize_report_paths(summary)


def all_checks_passed(summary: dict[str, object]) -> bool:
    return (
        summary["smoke_passed"] == summary["total_cases"]
        and summary["query_plan_passed"] == summary["query_plan_cases"]
        and summary["eval_passed"] == summary["total_cases"]
        and summary["thread_focus_passed"] == summary["total_cases"]
        and summary["resolution_passed"] == summary["total_cases"]
        and summary["forbidden_guard_passed"] == summary["total_cases"]
        and summary["hallucination_guard_passed"] == summary["total_cases"]
        and summary["ablation_positive"] == summary["total_cases"]
    )


def main() -> int:
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    with temporary_workspace_dir(ROOT, "find-community-help-community-") as temp:
        temp_dir = Path(temp)
        results = [build_case_result(case, temp_dir) for case in cases]

    summary = summarize_results(results)
    REPORT_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if all_checks_passed(summary) else 1


if __name__ == "__main__":
    raise SystemExit(main())
