#!/usr/bin/env python3
"""根据通用 AI 应用与工作流业务蓝图生成初始回归测试用例。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("blueprint", type=Path)
    parser.add_argument("output", type=Path, help="输出 JSON；为避免误覆盖，文件必须不存在")
    return parser.parse_args()


def load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as stream:
        data = json.load(stream)
    if not isinstance(data, dict) or not isinstance(data.get("routes"), list):
        raise ValueError("蓝图必须是对象并包含 routes 数组")
    return data


def build_cases(blueprint: dict[str, Any]) -> list[dict[str, Any]]:
    forbidden = [str(value) for value in blueprint.get("forbidden_substrings", [])]
    max_latency = int(blueprint.get("default_max_latency_ms", 8000))
    max_chars = int(blueprint.get("default_max_answer_chars", 500))
    missing_route = str(blueprint.get("missing_input_route", "request-missing-field"))
    cases: list[dict[str, Any]] = []

    for route in blueprint["routes"]:
        if not isinstance(route, dict) or not route.get("id") or not route.get("sample_input"):
            raise ValueError("每条路由必须包含 id 和 sample_input")
        route_id = str(route["id"])
        kind = str(route.get("kind", "other"))
        expected = [str(value) for value in route.get("expected_substrings", [])]
        common = {
            "conversation": "clean",
            "workflow_mode": kind,
            "forbidden_substrings": forbidden,
            "max_latency_ms": max_latency,
            "max_answer_chars": max_chars,
        }
        cases.append({
            "case_id": f"{route_id}-success",
            "category": "core",
            "input": str(route["sample_input"]),
            "expected_route": str(route.get("success_expected_route", route_id)),
            "expected_substrings": expected,
            **common,
        })
        for field in route.get("required_fields", []):
            cases.append({
                "case_id": f"{route_id}-missing-{field}",
                "category": "missing-input",
                "input": f"执行 {route_id}，但未提供 {field}",
                "expected_route": missing_route,
                "expected_substrings": ["需要", str(field)],
                **common,
            })
        if kind == "knowledge":
            cases.append({
                "case_id": f"{route_id}-no-hit",
                "category": "knowledge-no-hit",
                "input": f"{route['sample_input']}（使用不存在的示例主题）",
                "expected_route": route_id,
                "expected_substrings": ["未找到"],
                **common,
            })
        if kind == "tool":
            for failure, expected_text in (("timeout", "稍后"), ("empty", "未返回"), ("business-error", "失败")):
                cases.append({
                    "case_id": f"{route_id}-{failure}",
                    "category": "tool-failure",
                    "input": str(route["sample_input"]),
                    "simulated_condition": failure,
                    "expected_route": route_id,
                    "expected_substrings": [expected_text],
                    **common,
                })
        side_effect = str(route.get("side_effect", "none"))
        confirmation_required = bool(route.get("confirmation_required", kind == "action-approval" and side_effect not in {"none", "read"}))
        if confirmation_required:
            cases.append({
                "case_id": f"{route_id}-requires-confirmation",
                "category": "safety",
                "input": str(route["sample_input"]),
                "expected_route": "request-confirmation",
                "expected_substrings": ["确认"],
                **common,
            })
        for mode_test in route.get("mode_tests", []):
            if not isinstance(mode_test, dict) or not mode_test.get("id"):
                raise ValueError(f"路由 {route_id} 的 mode_tests 每项必须包含 id")
            generated = {
                "case_id": f"{route_id}-{mode_test['id']}",
                "category": str(mode_test.get("category", kind)),
                "input": str(mode_test.get("input", route["sample_input"])),
                "expected_route": str(mode_test.get("expected_route", route_id)),
                "expected_substrings": [str(value) for value in mode_test.get("expected_substrings", [])],
                **common,
            }
            if mode_test.get("simulated_condition") is not None:
                generated["simulated_condition"] = str(mode_test["simulated_condition"])
            if mode_test.get("expected_behavior") is not None:
                generated["expected_behavior"] = str(mode_test["expected_behavior"])
            cases.append(generated)
    return cases


def main() -> int:
    args = parse_args()
    try:
        if args.output.exists():
            raise FileExistsError(f"拒绝覆盖已有文件：{args.output.resolve()}")
        cases = build_cases(load(args.blueprint))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(cases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}")
        return 1
    print(f"OK: {args.output.resolve()}")
    print(f"CASES: {len(cases)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
