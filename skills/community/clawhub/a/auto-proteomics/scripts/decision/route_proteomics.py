#!/usr/bin/env python3
"""Minimal routing engine for Auto-Proteomics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
RULES_PATH = ROOT / "references" / "WORKFLOW_INDEX.yaml"


def load_rules() -> dict[str, Any]:
    with RULES_PATH.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Auto-Proteomics workflow router")
    parser.add_argument("--goal")
    parser.add_argument("--data-type")
    parser.add_argument("--acquisition-mode")
    parser.add_argument("--target-output")
    parser.add_argument("--input-stage")
    parser.add_argument("--pretty", action="store_true")
    return parser.parse_args()


def value_matches(expected: Any, actual: Any) -> bool:
    if isinstance(expected, list):
        return actual in expected
    return actual == expected


def rule_matches(rule: dict[str, Any], payload: dict[str, Any]) -> bool:
    for field, expected in rule.get("when", {}).items():
        actual = payload.get(field)
        if actual is None or not value_matches(expected, actual):
            return False
    return True


def missing_fields(payload: dict[str, Any], required_fields: list[str]) -> list[str]:
    return [field for field in required_fields if not payload.get(field)]


def public_workflows(rules: dict[str, Any]) -> set[str]:
    public_promise = rules.get("public_promise", {})
    return set(public_promise.get("shipped_workflows", []))


def out_of_scope_result(
    payload: dict[str, Any],
    *,
    why: str,
    missing: list[str] | None = None,
    matched_rule: str | None = None,
    internal_route: str | None = None,
    workflow_status: str | None = None,
    route_mode: str | None = None,
    next_step: str | None = None,
    confidence: str = "low",
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "status": "needs-clarification-or-out-of-scope",
        "recommended": None,
        "public_supported": False,
        "why": why,
        "avoid": ["Do not present scaffold or prototype workflows as published public recommendations."],
        "next": next_step,
        "confidence": confidence,
        "input": payload,
    }
    if missing:
        result["missing_fields"] = missing
    if matched_rule:
        result["matched_rule"] = matched_rule
    if internal_route:
        result["internal_route"] = internal_route
    if workflow_status:
        result["workflow_status"] = workflow_status
    if route_mode:
        result["route_mode"] = route_mode
    return result


def main() -> int:
    args = parse_args()
    payload = {
        "goal": args.goal,
        "data_type": args.data_type,
        "acquisition_mode": args.acquisition_mode,
        "target_output": args.target_output,
        "input_stage": args.input_stage,
    }
    payload = {k: v for k, v in payload.items() if v}
    rules = load_rules()
    required_fields = rules.get("fallback", {}).get("missing_info_priority", [])
    missing = missing_fields(payload, required_fields)
    matches = [rule for rule in rules.get("routing_rules", []) if rule_matches(rule, payload)]
    published = public_workflows(rules)

    if missing:
        result = out_of_scope_result(
            payload,
            why="Input is incomplete for public v0.x routing; provide the smallest missing field set.",
            missing=missing,
        )
    elif matches:
        rule = matches[0]
        recommendations = rule.get("recommend", [])
        recommended = recommendations[0] if recommendations else None
        if rule.get("status") == "shipped" and recommended in published:
            result = {
                "status": "public-match",
                "recommended": recommended,
                "public_supported": True,
                "workflow_status": rule.get("status", "shipped"),
                "why": rule["why"],
                "avoid": rule.get("avoid", []),
                "next": rule.get("next", {}).get("primary"),
                "confidence": rule.get("confidence", "medium"),
                "input": payload,
            }
        else:
            matched = (
                recommended
                or rule.get("prototype_candidate")
                or rule.get("scaffold_candidate")
                or rule.get("id")
            )
            result = out_of_scope_result(
                payload,
                why=(
                    f"Matched '{matched}', but it is outside the current public v0.x scope; "
                    "only 'dda-lfq-processed' is publicly runnable."
                ),
                matched_rule=rule.get("id"),
                internal_route=matched,
                workflow_status=rule.get("status"),
                route_mode=rule.get("route_mode") or rule.get("visibility") or "non-public",
                next_step=rule.get("next", {}).get("primary"),
                confidence=rule.get("confidence", "medium"),
            )
    else:
        result = out_of_scope_result(
            payload,
            why=(
                "No current public v0.x workflow fits this request; clarify the task or keep it "
                "outside the published scope for now."
            ),
        )

    if args.pretty:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
