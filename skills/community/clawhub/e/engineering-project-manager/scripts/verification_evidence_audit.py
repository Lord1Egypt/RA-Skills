#!/usr/bin/env python3
"""Audit Project Manager verification evidence management and release coverage."""

import argparse
import json
from pathlib import Path

from pm_common import git_capture
from verification_evidence import (
    MODEL_VERSION,
    coverage,
    load_registry,
    locations,
    validate_registry,
)


def audit(project, strict=False):
    project = Path(project)
    marker = locations(project)["marker"]
    if not marker.exists():
        loc = locations(project)
        previously_enabled = git_capture(
            project, "log", "-1", "--format=%H", "--",
            marker.relative_to(project).as_posix(),
        )
        if (loc["registry"].exists()
                or any(loc["records"].glob("EV-*.md"))
                or previously_enabled):
            return [
                "Verification evidence enablement marker is missing from an enabled project; "
                "restore it before auditing or releasing"
            ], []
        return [], [] if strict else [
            "Verification Evidence Management is not enabled; legacy project skipped"
        ]
    try:
        model = json.loads(marker.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Cannot read verification-evidence marker: {exc}"], []
    errors, warnings = [], []
    if (
        model.get("model") != "PROJECT_MANAGER_VERIFICATION_EVIDENCE_MANAGEMENT"
        or model.get("model_version") != MODEL_VERSION
        or model.get("enabled") is not True
    ):
        errors.append("Invalid Verification Evidence Management enablement marker")
    try:
        registry = load_registry(project)
        registry_errors, registry_warnings = validate_registry(project, registry)
        errors.extend(registry_errors)
        warnings.extend(registry_warnings)
    except Exception as exc:
        return [f"Evidence registry audit failed: {exc}"], warnings

    covered, uncovered = coverage(project, registry)
    for requirement_id in uncovered:
        errors.append(f"Requirement has no compatible PASS evidence: {requirement_id}")
    if strict:
        errors.extend(f"Strict evidence warning: {warning}" for warning in warnings)
        warnings = []
    return errors, warnings


def main(argv=None):
    parser = argparse.ArgumentParser(description="Audit Project Manager verification evidence")
    parser.add_argument("project")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)
    errors, warnings = audit(Path(args.project).resolve(), args.strict)
    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"VERIFICATION EVIDENCE AUDIT: FAIL ({len(errors)} error(s), {len(warnings)} warning(s))")
        return 1
    print(f"VERIFICATION EVIDENCE AUDIT: PASS ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
