#!/usr/bin/env python3
"""Check an agent-produced configuration offline; this does not invoke an agent."""

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "scripts"))
import pace_chart as pace

SUITE = json.loads((ROOT / "cases.json").read_text(encoding="utf-8"))


def evaluate(case_id: str, config: dict) -> dict:
    case = next(case for case in SUITE["cases"] if case["id"] == case_id)
    errors = []
    result = {"case": case_id, "passed": False, "errors": errors}
    try:
        plan = pace.build_plan(ROOT / "course.gpx", config)
    except (pace.InputError, OSError) as error:
        errors.append(str(error))
        return result
    expected_parameters = {**SUITE["default_parameters"], **case.get("expected_parameters", {})}
    actual_parameters = {"water_mode": "distance", **plan["parameters"]}
    for key, expected in expected_parameters.items():
        actual = actual_parameters[key]
        if actual != expected:
            errors.append(f"parameters.{key}: expected {expected!r}, got {actual!r}")
    expected_targets = case.get("targets_seconds", SUITE["targets_seconds"])
    if plan["targets_seconds"] != expected_targets:
        errors.append(f"targets_seconds: expected {expected_targets}, got {plan['targets_seconds']}")
    for key, expected in case.get("required_config", {}).items():
        if key not in config or config[key] != expected:
            errors.append(f"configuration.{key}: expected explicit {expected!r}")
    for key in case.get("forbidden_config", []):
        if key in config:
            errors.append(f"configuration.{key}: must be removed for this request")
    if [cp["id"] for cp in plan["checkpoints"]] != ["start", "wpt:1", "finish"]:
        errors.append("checkpoint selection must preserve the embedded CP1 and both endpoints")
    rests = case.get("rests_seconds", {})
    cutoffs = case.get("cutoffs_seconds", {})
    actual_ids = {cp["id"] for cp in plan["checkpoints"]}
    if (set(rests) | set(cutoffs)) - actual_ids:
        errors.append("requested station rests or cutoffs are missing")
    for cp in plan["checkpoints"]:
        for field, expected in (
            ("rest_seconds", rests.get(cp["id"], 0)),
            ("cutoff_seconds", cutoffs.get(cp["id"])),
        ):
            if cp[field] != expected:
                errors.append(f'checkpoint.{cp["id"]}.{field}: expected {expected!r}, got {cp[field]!r}')
    result["summary"] = pace.plan_summary(plan)
    result["passed"] = not errors
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    cases = SUITE["cases"] + SUITE["manual_review_cases"]
    parser.add_argument("--case", required=True, choices=[case["id"] for case in cases])
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--config", type=Path, help="Actual configuration written by the agent")
    action.add_argument("--prompt", action="store_true", help="Show a prompt without its expected results")
    parser.add_argument("--language", choices=("zh", "en"), default="zh")
    parser.add_argument("--variant", type=int, default=1, help="1-based prompt variant")
    args = parser.parse_args(argv)
    case = next(case for case in cases if case["id"] == args.case)
    if args.prompt:
        prompts = [case[f"prompt_{args.language}"], *case[f"variants_{args.language}"]]
        if not 1 <= args.variant <= len(prompts):
            parser.error(f"--variant must be between 1 and {len(prompts)} for this case and language")
        result = {"case": args.case, "language": args.language, "variant": args.variant,
                  "prompt": prompts[args.variant - 1]}
        if "selected_config" in case:
            result["selected_config"] = case["selected_config"]
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    if case in SUITE["manual_review_cases"]:
        parser.error("manual-review cases cannot be checked with --config")
    try:
        result = evaluate(args.case, json.loads(args.config.read_text(encoding="utf-8")))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
