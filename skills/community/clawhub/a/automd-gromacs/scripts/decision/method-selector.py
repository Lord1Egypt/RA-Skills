#!/usr/bin/env python3
"""Minimal public decision engine for AutoMD-GROMACS method routing.

This script reads structured inputs plus the packaged rule file and returns a
stable, low-token recommendation contract for OpenClaw agents.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
RULES_PATH = ROOT / "references" / "METHOD_SELECTION_INDEX.yaml"

REQUIRED_FIELDS = ("goal", "system_type", "target_observable")
ASK_HINTS = {
    "goal": "What is the scientific goal?",
    "target_observable": "What output do you actually want: PMF, binding free energy, structure ensemble, field response, transport property, or reaction profile?",
    "cv_known_or_reaction_coordinate_known": "Do you already know a credible CV or reaction coordinate?",
    "budget_level": "What is the compute budget: low, medium, or high?",
}


def load_rules() -> dict[str, Any]:
    with RULES_PATH.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def normalize_value(value: Any) -> Any:
    if isinstance(value, str):
        return value.strip()
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AutoMD-GROMACS method selector")
    parser.add_argument("--input", help="JSON file with structured method-selection input")
    parser.add_argument("--goal")
    parser.add_argument("--system-type")
    parser.add_argument("--target-observable")
    parser.add_argument("--budget-level")
    parser.add_argument("--timescale-gap")
    parser.add_argument("--expertise-level")
    parser.add_argument("--cv-known")
    parser.add_argument("--reaction-coordinate-known")
    parser.add_argument("--software-constraints")
    parser.add_argument("--priority")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    return parser.parse_args()


def load_input(args: argparse.Namespace) -> dict[str, Any]:
    data: dict[str, Any] = {}
    if args.input:
        with open(args.input, "r", encoding="utf-8") as fh:
            data.update(json.load(fh))

    cli_map = {
        "goal": args.goal,
        "system_type": args.system_type,
        "target_observable": args.target_observable,
        "budget_level": args.budget_level,
        "timescale_gap": args.timescale_gap,
        "expertise_level": args.expertise_level,
        "cv_known": args.cv_known,
        "reaction_coordinate_known": args.reaction_coordinate_known,
        "software_constraints": args.software_constraints,
        "priority": args.priority,
    }
    for key, value in cli_map.items():
        if value is not None:
            data[key] = value

    return {key: normalize_value(value) for key, value in data.items() if value not in (None, "")}


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


def rule_specificity(rule: dict[str, Any]) -> tuple[int, int, int]:
    when = rule.get("when", {})
    exact = sum(1 for value in when.values() if not isinstance(value, list))
    observable_priority = 1 if "target_observable" in when else 0
    return (len(when), observable_priority, exact)


def get_missing_fields(payload: dict[str, Any], rules: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    for field in rules.get("fallback", {}).get("missing_info_priority", []):
        if field == "cv_known_or_reaction_coordinate_known":
            if not payload.get("cv_known") and not payload.get("reaction_coordinate_known"):
                missing.append(field)
            continue
        if not payload.get(field):
            missing.append(field)
    return missing


def recommend_from_rule(rule: dict[str, Any]) -> dict[str, Any]:
    recommended = rule.get("recommend", [])
    primary = recommended[0] if recommended else "unknown"
    next_map = rule.get("next", {})
    next_step = next_map.get("primary") or next_map.get("alternative") or next_map.get("prep") or "unknown"
    return {
        "recommended": primary,
        "alternatives": recommended[1:],
        "why": rule.get("why", "No reason available."),
        "avoid": rule.get("avoid", []),
        "next": next_step,
        "confidence": rule.get("confidence", "medium"),
        "rule_id": rule.get("id", "unknown"),
    }


def fallback_response(payload: dict[str, Any], rules: dict[str, Any]) -> dict[str, Any]:
    script_map = rules.get("script_map", {})
    candidates = [
        {
            "target": "replica-exchange",
            "next": script_map.get("replica-exchange"),
            "why": "Safe default for broad exploration when CV information is still weak.",
        },
        {
            "target": "trajectory-analysis",
            "next": script_map.get("trajectory-analysis"),
            "why": "Use analysis-first when the user may already have enough data to interpret before launching new sampling.",
        },
    ]
    missing = get_missing_fields(payload, rules)
    return {
        "recommended": candidates[0]["target"],
        "alternatives": [candidate["target"] for candidate in candidates[1:]],
        "why": "Insufficient information for a high-confidence single route.",
        "avoid": ["Do not commit to a fragile or highly specific method yet."],
        "next": candidates[0]["next"],
        "confidence": "low",
        "rule_id": "fallback",
        "candidates": candidates,
        "ask": [ASK_HINTS[field] for field in missing if field in ASK_HINTS][:2],
    }


def format_text(result: dict[str, Any]) -> str:
    avoid = ", ".join(result.get("avoid", [])) if result.get("avoid") else "None"
    lines = [
        f"Recommended: {result['recommended']}",
        f"Why: {result['why']}",
        f"Avoid: {avoid}",
        f"Next: {result['next']}",
    ]
    if result.get("ask"):
        lines.append("Ask: " + " | ".join(result["ask"]))
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    payload = load_input(args)
    rules = load_rules()

    matches = [rule for rule in rules.get("routing_rules", []) if rule_matches(rule, payload)]
    if matches:
        matches.sort(key=rule_specificity, reverse=True)
        result = recommend_from_rule(matches[0])
    else:
        result = fallback_response(payload, rules)

    result["input"] = payload
    result["contract"] = format_text(result)

    if args.pretty:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
