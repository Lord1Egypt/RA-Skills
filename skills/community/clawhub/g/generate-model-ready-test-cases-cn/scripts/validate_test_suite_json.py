#!/usr/bin/env python3
"""
Validate model-ready test suite JSON files produced with this skill.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ALLOWED_TARGET_TYPES = {"web", "api", "workflow", "mobile", "desktop"}
ALLOWED_PRIORITIES = {"P0", "P1", "P2", "P3"}
ALLOWED_ACTIONS = {
    "navigate",
    "click",
    "fill",
    "select",
    "keypress",
    "hover",
    "wait",
    "assert",
    "request",
    "extract",
    "upload",
    "download",
}
ALLOWED_ASSERTIONS = {
    "element_visible",
    "element_text",
    "element_value",
    "page_contains",
    "url_matches",
    "response_status",
    "json_path_equals",
    "json_path_exists",
    "variable_stored",
    "download_created",
}
TARGET_REQUIRED_ACTIONS = {"navigate", "click", "fill", "select", "hover", "upload"}


def fail(errors: list[str]) -> int:
    for error in errors:
        print(f"[ERROR] {error}")
    return 1


def require_type(value, expected_type, path: str, errors: list[str]) -> bool:
    if not isinstance(value, expected_type):
        expected_name = (
            expected_type.__name__
            if isinstance(expected_type, type)
            else "/".join(item.__name__ for item in expected_type)
        )
        errors.append(f"{path} must be {expected_name}")
        return False
    return True


def validate_expected(items: object, path: str, errors: list[str]) -> None:
    if not require_type(items, list, path, errors):
        return
    if not items:
        errors.append(f"{path} must not be empty")
        return
    for index, item in enumerate(items):
        item_path = f"{path}[{index}]"
        if not require_type(item, dict, item_path, errors):
            continue
        assertion_type = item.get("type")
        if not isinstance(assertion_type, str) or not assertion_type:
            errors.append(f"{item_path}.type must be a non-empty string")
        elif assertion_type not in ALLOWED_ASSERTIONS:
            errors.append(
                f"{item_path}.type must be one of {sorted(ALLOWED_ASSERTIONS)}"
            )


def validate_step(step: object, path: str, errors: list[str]) -> str | None:
    if not require_type(step, dict, path, errors):
        return None

    step_id = step.get("step_id")
    if not isinstance(step_id, str) or not step_id.strip():
        errors.append(f"{path}.step_id must be a non-empty string")
        step_id = None

    action = step.get("action")
    if not isinstance(action, str) or not action.strip():
        errors.append(f"{path}.action must be a non-empty string")
    elif action not in ALLOWED_ACTIONS:
        errors.append(f"{path}.action must be one of {sorted(ALLOWED_ACTIONS)}")

    target = step.get("target")
    input_data = step.get("input")
    expected = step.get("expected")

    if action in TARGET_REQUIRED_ACTIONS:
        if not require_type(target, dict, f"{path}.target", errors):
            return step_id

    if action == "navigate":
        if not isinstance(target, dict) or not isinstance(target.get("url"), str):
            errors.append(f"{path}.target.url is required for navigate")
    elif action == "fill":
        if not isinstance(input_data, dict) or "value" not in input_data:
            errors.append(f"{path}.input.value is required for fill")
    elif action == "select":
        if not isinstance(input_data, dict) or "value" not in input_data:
            errors.append(f"{path}.input.value is required for select")
    elif action == "keypress":
        if not isinstance(input_data, dict) or "key" not in input_data:
            errors.append(f"{path}.input.key is required for keypress")
    elif action == "request":
        if not require_type(input_data, dict, f"{path}.input", errors):
            return step_id
        if "method" not in input_data:
            errors.append(f"{path}.input.method is required for request")
        has_url = False
        if isinstance(target, dict) and isinstance(target.get("url"), str):
            has_url = True
        if isinstance(input_data.get("url"), str):
            has_url = True
        if not has_url:
            errors.append(f"{path} must provide target.url or input.url for request")
    elif action == "extract":
        if not isinstance(input_data, dict) or "variable" not in input_data:
            errors.append(f"{path}.input.variable is required for extract")

    validate_expected(expected, f"{path}.expected", errors)
    return step_id


def validate_case(case: object, path: str, errors: list[str]) -> str | None:
    if not require_type(case, dict, path, errors):
        return None

    case_id = case.get("case_id")
    if not isinstance(case_id, str) or not case_id.strip():
        errors.append(f"{path}.case_id must be a non-empty string")
        case_id = None

    for field in ("title", "objective"):
        value = case.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{path}.{field} must be a non-empty string")

    priority = case.get("priority")
    if priority not in ALLOWED_PRIORITIES:
        errors.append(f"{path}.priority must be one of {sorted(ALLOWED_PRIORITIES)}")

    for field in ("tags", "preconditions", "cleanup"):
        if not require_type(case.get(field), list, f"{path}.{field}", errors):
            continue

    if not require_type(case.get("test_data"), dict, f"{path}.test_data", errors):
        return case_id

    enabled = case.get("enabled")
    if not isinstance(enabled, bool):
        errors.append(f"{path}.enabled must be a boolean")

    steps = case.get("steps")
    if not require_type(steps, list, f"{path}.steps", errors):
        return case_id
    if not steps:
        errors.append(f"{path}.steps must not be empty")
        return case_id

    seen_step_ids: set[str] = set()
    for index, step in enumerate(steps):
        step_id = validate_step(step, f"{path}.steps[{index}]", errors)
        if step_id:
            if step_id in seen_step_ids:
                errors.append(f"{path}.steps has duplicated step_id: {step_id}")
            seen_step_ids.add(step_id)

    return case_id


def validate_suite(data: object) -> tuple[list[str], int]:
    errors: list[str] = []

    if not require_type(data, dict, "root", errors):
        return errors, 0

    for field in ("suite_id", "suite_title"):
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field} must be a non-empty string")

    target = data.get("target")
    if require_type(target, dict, "target", errors):
        target_type = target.get("type")
        if target_type not in ALLOWED_TARGET_TYPES:
            errors.append(f"target.type must be one of {sorted(ALLOWED_TARGET_TYPES)}")

    if not require_type(data.get("assumptions"), list, "assumptions", errors):
        return errors, 0
    if not require_type(data.get("defaults"), dict, "defaults", errors):
        return errors, 0

    cases = data.get("cases")
    if not require_type(cases, list, "cases", errors):
        return errors, 0
    if not cases:
        errors.append("cases must not be empty")
        return errors, 0

    seen_case_ids: set[str] = set()
    for index, case in enumerate(cases):
        case_id = validate_case(case, f"cases[{index}]", errors)
        if case_id:
            if case_id in seen_case_ids:
                errors.append(f"cases has duplicated case_id: {case_id}")
            seen_case_ids.add(case_id)

    return errors, len(cases)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a model-ready automation test suite JSON file."
    )
    parser.add_argument("json_file", help="Path to the JSON file to validate")
    args = parser.parse_args()

    path = Path(args.json_file).resolve()
    if not path.is_file():
        print(f"[ERROR] File not found: {path}")
        return 1

    try:
        # Accept both plain UTF-8 and UTF-8 with BOM, which is common on Windows.
        raw = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        print("[ERROR] File must be UTF-8 or UTF-8 with BOM encoded")
        return 1

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"[ERROR] Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}")
        return 1

    errors, case_count = validate_suite(data)
    if errors:
        return fail(errors)

    print(f"[OK] Validation passed: {path}")
    print(f"[OK] Cases: {case_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
