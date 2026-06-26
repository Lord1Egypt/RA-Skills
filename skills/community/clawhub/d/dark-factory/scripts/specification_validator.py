#!/usr/bin/env python3
"""
Dark Factory — Specification Validator
Validates a specification JSON for clarity, completeness, and testability
before passing it to the behavioral test engine or orchestrator.

Usage:
  python specification_validator.py <specification.json>
"""
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

REQUIRED_TOP_LEVEL = ["specification_id", "title", "description", "behavioral_scenarios", "success_criteria"]
REQUIRED_SCENARIO_FIELDS = ["scenario", "input", "expected_output"]


def log(msg: str, level: str = "INFO"):
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    prefix = {"OK": "✓ ", "WARN": "⚠ ", "ERR": "✗ ", "INFO": "  "}.get(level, "  ")
    print(f"[{ts}] {prefix}{msg}")


def validate(spec_path: str) -> tuple[bool, list, list]:
    """
    Validate a specification file.
    Returns (passed: bool, errors: list, warnings: list)
    """
    errors = []
    warnings = []

    # Load file
    path = Path(spec_path)
    if not path.exists():
        return False, [f"File not found: {spec_path}"], []

    try:
        spec = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"], []

    # Check required top-level fields
    for field in REQUIRED_TOP_LEVEL:
        if field not in spec:
            errors.append(f"Missing required field: '{field}'")
        elif not spec[field] and spec[field] != 0:
            warnings.append(f"Field '{field}' is empty")

    # Validate specification_id format
    if "specification_id" in spec:
        sid = spec["specification_id"]
        if not isinstance(sid, str) or not sid.startswith("spec-"):
            warnings.append(f"specification_id should follow format 'spec-XXXXXXXX', got: '{sid}'")

    # Validate behavioral_scenarios
    scenarios = spec.get("behavioral_scenarios", [])
    if not isinstance(scenarios, list):
        errors.append("'behavioral_scenarios' must be a list")
    elif len(scenarios) == 0:
        errors.append("'behavioral_scenarios' must contain at least one scenario")
    else:
        for i, scenario in enumerate(scenarios):
            if not isinstance(scenario, dict):
                errors.append(f"Scenario {i+1} must be an object")
                continue
            for field in REQUIRED_SCENARIO_FIELDS:
                if field not in scenario:
                    errors.append(f"Scenario {i+1} missing required field: '{field}'")
                elif field == "scenario" and not scenario[field].strip():
                    warnings.append(f"Scenario {i+1} has empty 'scenario' description")

    # Validate success_criteria
    criteria = spec.get("success_criteria", {})
    if not isinstance(criteria, dict):
        errors.append("'success_criteria' must be an object")
    else:
        if "test_pass_rate" not in criteria:
            warnings.append("'success_criteria' should include 'test_pass_rate' (recommended: 0.95)")
        elif not (0.0 <= float(criteria.get("test_pass_rate", 0)) <= 1.0):
            errors.append("'success_criteria.test_pass_rate' must be between 0.0 and 1.0")

    # Optional field checks
    if "dependencies" in spec and not isinstance(spec["dependencies"], list):
        warnings.append("'dependencies' should be a list of skill/system names")

    if "security_requirements" not in spec:
        warnings.append("No 'security_requirements' defined — consider specifying data sensitivity level")

    passed = len(errors) == 0
    return passed, errors, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: python specification_validator.py <specification.json>")
        sys.exit(1)

    spec_path = sys.argv[1]
    log("=" * 60)
    log(f"SPECIFICATION VALIDATOR")
    log(f"File: {spec_path}")
    log("=" * 60)

    passed, errors, warnings = validate(spec_path)

    if warnings:
        log(f"{len(warnings)} warning(s):", "INFO")
        for w in warnings:
            log(w, "WARN")

    if errors:
        log(f"{len(errors)} error(s):", "INFO")
        for e in errors:
            log(e, "ERR")

    log("=" * 60)
    if passed:
        log(f"VALIDATION PASSED — {len(warnings)} warning(s), 0 errors", "OK")
    else:
        log(f"VALIDATION FAILED — {len(errors)} error(s), {len(warnings)} warning(s)", "ERR")
    log("=" * 60)

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
