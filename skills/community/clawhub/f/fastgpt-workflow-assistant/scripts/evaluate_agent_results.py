#!/usr/bin/env python3
"""使用与接口回归执行器一致的契约评估 Agent 测试结果。"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from regression_assertions import evaluate_assertions


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cases", type=Path, help="测试用例 JSON 数组")
    parser.add_argument("results", type=Path, help="测试结果 JSON 数组")
    parser.add_argument("--json", action="store_true", dest="json_output")
    return parser.parse_args()


def load_array(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig") as stream:
        value = json.load(stream)
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise ValueError(f"{path}: 顶层必须是对象数组")
    return value


def diagnostic(code: str, case_id: str, message: str) -> dict[str, str]:
    return {"code": code, "severity": "error", "case_id": case_id, "message": message}


def flatten_cases(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """同时支持扁平用例和接口执行器使用的conversation/turns用例。"""
    flattened: list[dict[str, Any]] = []
    for case in cases:
        turns = case.get("turns")
        if not isinstance(turns, list):
            flattened.append(case)
            continue
        conversation_id = str(case.get("case_id", ""))
        base = {key: value for key, value in case.items() if key != "turns"}
        for index, turn in enumerate(turns, 1):
            if not isinstance(turn, dict):
                raise ValueError(f"{conversation_id or '<missing>'}: turns[{index}]必须是对象")
            item = {**base, **turn}
            item["conversation_id"] = conversation_id
            item["case_id"] = str(
                turn.get("result_id")
                or (conversation_id if len(turns) == 1 else f"{conversation_id}-{index}")
            )
            flattened.append(item)
    return flattened


def evaluate(cases: list[dict[str, Any]], results: list[dict[str, Any]]) -> dict[str, Any]:
    diagnostics: list[dict[str, str]] = []
    flattened_cases = flatten_cases(cases)
    result_by_id: dict[str, dict[str, Any]] = {}
    for item in results:
        result_id = str(item.get("case_id", ""))
        if result_id in result_by_id:
            diagnostics.append(diagnostic("EV004", result_id or "<missing>", "测试结果 case_id 重复"))
        result_by_id[result_id] = item
    case_reports: list[dict[str, Any]] = []
    seen_case_ids: set[str] = set()

    for case in flattened_cases:
        case_id = str(case.get("case_id", ""))
        failures: list[str] = []
        if not case_id:
            diagnostics.append(diagnostic("EV001", "<missing>", "测试用例缺少 case_id"))
            continue
        if case_id in seen_case_ids:
            diagnostics.append(diagnostic("EV003", case_id, "测试用例 case_id 重复"))
            case_reports.append({"case_id": case_id, "status": "fail", "failures": ["duplicate_case_id"]})
            continue
        seen_case_ids.add(case_id)
        result = result_by_id.get(case_id)
        if result is None:
            diagnostics.append(diagnostic("EV002", case_id, "缺少测试结果"))
            case_reports.append({"case_id": case_id, "status": "fail", "failures": ["missing_result"]})
            continue

        route = str(result.get("route", ""))
        check = evaluate_assertions(case, result, route)
        if check["route_mismatch"]:
            diagnostics.append(diagnostic("EV010", case_id, f"路由不符：期望 {case.get('expected_route')!r}，实际 {route!r}"))
            failures.append("route")
        for expected in check["missing"]:
            diagnostics.append(diagnostic("EV011", case_id, f"答案缺少期望子串：{expected!r}"))
            failures.append(f"missing:{expected}")
        for forbidden in check["forbidden"]:
            diagnostics.append(diagnostic("EV012", case_id, f"答案包含禁止子串：{forbidden!r}"))
            failures.append(f"forbidden:{forbidden}")
        if check["latency_missing"] or check["latency_exceeded"]:
            diagnostics.append(diagnostic("EV013", case_id, f"延迟超限或缺失：{check['latency_ms']!r}，上限 {case.get('max_latency_ms')!r}"))
            failures.append("latency")
        if check["answer_too_long"]:
            diagnostics.append(diagnostic("EV014", case_id, f"答案过长：{check['answer_chars']} > {case.get('max_answer_chars')}"))
            failures.append("length")
        if check["answer_too_short"]:
            diagnostics.append(diagnostic("EV015", case_id, f"答案过短：{check['answer_chars']} < {case.get('min_answer_chars')}"))
            failures.append("answer_too_short")
        if check["ipv4_count_exceeded"]:
            diagnostics.append(diagnostic("EV022", case_id, f"答案包含不同IPv4数量过多：{check['distinct_ipv4_count']} > {case.get('max_distinct_ipv4')}"))
            failures.append("distinct_ipv4_count")
        if check["mac_count_exceeded"]:
            diagnostics.append(diagnostic("EV023", case_id, f"答案包含不同MAC数量过多：{check['distinct_mac_count']} > {case.get('max_distinct_mac')}"))
            failures.append("distinct_mac_count")
        for group in check["missing_any_groups"]:
            diagnostics.append(diagnostic("EV016", case_id, f"答案未命中任一允许表达：{group!r}"))
            failures.append(f"missing_any:{group}")
        for node in check["missing_nodes"]:
            diagnostics.append(diagnostic("EV017", case_id, f"必需节点未执行：{node!r}"))
            failures.append(f"missing_node:{node}")
        for node in check["forbidden_nodes"]:
            diagnostics.append(diagnostic("EV018", case_id, f"禁止节点被执行：{node!r}"))
            failures.append(f"forbidden_node:{node}")
        for text in check["runtime_failure_matches"]:
            diagnostics.append(diagnostic("EV019", case_id, f"答案命中运行失败文本：{text!r}"))
            failures.append(f"runtime_failure:{text}")
        covered_runtime_flags = {
            "answer_too_short", "required_node_missing", "forbidden_node_executed",
            "runtime_failure_text", "latency_missing",
        }
        for flag in check["runtime_anomaly_flags"]:
            if flag not in covered_runtime_flags:
                diagnostics.append(diagnostic("EV021", case_id, f"检测到运行异常：{flag}"))
                failures.append(f"runtime:{flag}")
        case_reports.append({
            "case_id": case_id,
            "status": "fail" if failures else "pass",
            "failures": failures,
            "assertion_failed": check["assertion_failed"],
            "runtime_anomaly": check["runtime_anomaly"],
            "expected_behavior": check.get("expected_behavior", "normal"),
            "latency_exceeded": check["latency_exceeded"],
            "text_match_mode": check["text_match_mode"],
        })

    defined_ids = {str(case.get("case_id")) for case in flattened_cases}
    for extra_id in sorted(set(result_by_id) - defined_ids):
        diagnostics.append({"code": "EV020", "severity": "warning", "case_id": extra_id, "message": "结果中存在未定义用例"})

    status_counts = Counter(item["status"] for item in case_reports)
    return {
        "schema_version": "2.0",
        "summary": {
            "cases": len(flattened_cases),
            "results": len(results),
            "status_counts": dict(status_counts),
            "assertion_failures": sum(bool(item.get("assertion_failed")) for item in case_reports),
            "runtime_anomalies": sum(bool(item.get("runtime_anomaly")) for item in case_reports),
            "latency_exceeded": sum(bool(item.get("latency_exceeded")) for item in case_reports),
        },
        "cases": case_reports,
        "diagnostics": diagnostics,
    }


def main() -> int:
    args = parse_args()
    try:
        report = evaluate(load_array(args.cases), load_array(args.results))
    except Exception as exc:
        report = {"schema_version": "1.0", "summary": {"status_counts": {"fail": 1}}, "cases": [], "diagnostics": [diagnostic("EV000", "<file>", f"{type(exc).__name__}: {exc}")]}
    if args.json_output:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
        for item in report["diagnostics"]:
            print(f"[{item['severity'].upper()}][{item['code']}][{item['case_id']}] {item['message']}")
    return 1 if any(item["severity"] == "error" for item in report["diagnostics"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
