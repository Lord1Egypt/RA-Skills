#!/usr/bin/env python3
"""Validate routing audit JSON/JSONL records and core safety invariants."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Iterable


ROUTES = {"local_faq", "cloud_llm", "tool_call", "abstain"}
SENSITIVE_KEYS = {
    "authorization_token",
    "api_key",
    "access_token",
    "refresh_token",
    "secret",
    "password",
    "credential",
    "credentials",
}


def load_records(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    stripped = text.lstrip()
    if not stripped:
        return []
    if stripped.startswith("["):
        value = json.loads(text)
        if not isinstance(value, list):
            raise ValueError("JSON root must be a list or use JSONL")
        return [record for record in value if isinstance(record, dict)]
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"line {line_number}: expected a JSON object")
        records.append(value)
    return records


def walk_keys(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key).lower()
            yield from walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_keys(child)


def validate_record(record: dict[str, Any], index: int) -> list[str]:
    errors: list[str] = []
    prefix = f"record {index}"

    request_id = record.get("request_id")
    if not isinstance(request_id, str) or not request_id.strip():
        errors.append(f"{prefix}: missing request_id")

    found_sensitive = sorted(set(walk_keys(record)) & SENSITIVE_KEYS)
    if found_sensitive:
        errors.append(f"{prefix}: sensitive keys present: {', '.join(found_sensitive)}")

    route = record.get("route")
    if not isinstance(route, dict):
        errors.append(f"{prefix}: route must be an object")
        return errors

    route_name = route.get("route")
    if route_name not in ROUTES:
        errors.append(f"{prefix}: invalid route {route_name!r}")

    confidence = route.get("confidence")
    if not isinstance(confidence, (int, float)) or not 0.0 <= confidence <= 1.0:
        errors.append(f"{prefix}: confidence must be in [0, 1]")

    probabilities = route.get("probabilities")
    if isinstance(probabilities, dict) and probabilities:
        values = list(probabilities.values())
        if not all(isinstance(value, (int, float)) and 0.0 <= value <= 1.0 for value in values):
            errors.append(f"{prefix}: route probabilities must be in [0, 1]")
        elif not math.isclose(sum(values), 1.0, abs_tol=1e-5):
            errors.append(f"{prefix}: route probabilities sum to {sum(values):.6f}, not 1")

    ood = record.get("ood")
    if isinstance(ood, dict):
        distance = ood.get("distance")
        threshold = ood.get("threshold")
        is_ood = ood.get("is_ood")
        if isinstance(distance, (int, float)) and isinstance(threshold, (int, float)):
            expected = distance >= threshold
            if is_ood is not expected:
                errors.append(
                    f"{prefix}: OOD flag {is_ood!r} inconsistent with "
                    f"distance={distance} and threshold={threshold}"
                )

    result = record.get("result")
    if not isinstance(result, dict):
        errors.append(f"{prefix}: result must be an object")
        return errors

    final_decision = result.get("final_decision")
    gate = record.get("gate")
    gate_status = gate.get("status") if isinstance(gate, dict) else None
    result_gate_status = result.get("gate_decision")

    if final_decision == "tool_execute":
        if gate_status != "allow" or result_gate_status != "allow":
            errors.append(f"{prefix}: tool_execute without matching gate allow")
        if not isinstance(gate, dict) or not gate.get("policy_version"):
            errors.append(f"{prefix}: tool_execute without gate policy_version")
        if not record.get("requested_action") or not record.get("resource"):
            errors.append(f"{prefix}: tool_execute missing requested_action or resource")

    escalated = result.get("escalated")
    is_ood = ood.get("is_ood") if isinstance(ood, dict) else False
    should_escalate = route_name == "cloud_llm" or is_ood is True
    if isinstance(escalated, bool) and should_escalate and not escalated:
        errors.append(f"{prefix}: cloud route or OOD flag was not escalated")

    context = record.get("context_snapshot")
    if not isinstance(context, dict):
        errors.append(f"{prefix}: missing context_snapshot")
    else:
        for field in ("policy_version", "available_tools_version", "observed_at"):
            if not context.get(field):
                errors.append(f"{prefix}: context_snapshot missing {field}")

    versions = result.get("versions")
    if not isinstance(versions, dict) or not versions.get("router") or not versions.get("policy"):
        errors.append(f"{prefix}: result missing router or policy version")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="JSON or JSONL audit file")
    args = parser.parse_args()

    try:
        records = load_records(args.path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "parse_error": str(exc)}, ensure_ascii=False))
        return 2

    violations: list[str] = []
    for index, record in enumerate(records, start=1):
        violations.extend(validate_record(record, index))

    summary = {
        "path": str(args.path),
        "records": len(records),
        "valid": not violations,
        "violations": len(violations),
        "details": violations[:100],
        "details_truncated": len(violations) > 100,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())
