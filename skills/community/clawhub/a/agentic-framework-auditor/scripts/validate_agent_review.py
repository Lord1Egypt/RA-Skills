from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ALLOWED_ASSESSMENTS = {"confirm", "possible_false_positive", "possible_false_negative", "needs_human_review"}
ALLOWED_CONFIDENCE = {"low", "medium", "high"}
TOP_LEVEL_KEYS = {"audit_id", "reviewer_id", "deterministic_findings_remain_authoritative", "observations"}
OBSERVATION_KEYS = {"finding_id", "assessment", "confidence", "evidence", "operator_action"}
TOKEN_LIKE_RE = re.compile(r"(?i)(sk-[a-z0-9_-]{12,}|xox[baprs]-[a-z0-9-]{10,}|ghp_[a-z0-9]{20,}|AKIA[0-9A-Z]{16})")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return value


def nonempty_text(value: object, *, max_length: int = 2000) -> bool:
    return isinstance(value, str) and bool(value.strip()) and len(value) <= max_length


def validate_response(audit_payload: dict[str, Any], response: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    gate = audit_payload.get("agent_review") or {}
    if gate.get("status") != "ready" or not gate.get("enabled"):
        errors.append("The deterministic audit does not have a ready agent-review gate.")

    expected_audit_id = gate.get("audit_id") or audit_payload.get("audit_id")
    if response.get("audit_id") != expected_audit_id:
        errors.append("Response audit_id does not match the deterministic audit.")
    if response.get("reviewer_id") != gate.get("reviewer_id"):
        errors.append("Response reviewer_id does not match the accountable reviewer identity.")
    if response.get("deterministic_findings_remain_authoritative") is not True:
        errors.append("Response must affirm that deterministic findings remain authoritative.")

    unknown_top = set(response) - TOP_LEVEL_KEYS
    if unknown_top:
        errors.append(f"Unknown top-level response fields: {sorted(unknown_top)}")

    observations = response.get("observations")
    if not isinstance(observations, list):
        errors.append("observations must be a JSON array.")
        observations = []

    selected_ids = {str(value) for value in gate.get("selected_finding_ids") or []}
    if len(observations) > len(selected_ids):
        errors.append("Response contains more observations than selected deterministic findings.")

    seen_ids: set[str] = set()
    normalized: list[dict[str, str]] = []
    for index, observation in enumerate(observations):
        label = f"observations[{index}]"
        if not isinstance(observation, dict):
            errors.append(f"{label} must be an object.")
            continue
        unknown = set(observation) - OBSERVATION_KEYS
        if unknown:
            errors.append(f"{label} has unknown fields: {sorted(unknown)}")
        finding_id = str(observation.get("finding_id") or "")
        if finding_id not in selected_ids:
            errors.append(f"{label}.finding_id is not in the bounded review packet: {finding_id!r}")
        if finding_id in seen_ids:
            errors.append(f"{label}.finding_id is duplicated: {finding_id!r}")
        seen_ids.add(finding_id)

        assessment = str(observation.get("assessment") or "")
        confidence = str(observation.get("confidence") or "")
        if assessment not in ALLOWED_ASSESSMENTS:
            errors.append(f"{label}.assessment is invalid: {assessment!r}")
        if confidence not in ALLOWED_CONFIDENCE:
            errors.append(f"{label}.confidence is invalid: {confidence!r}")
        evidence = observation.get("evidence")
        action = observation.get("operator_action")
        if not nonempty_text(evidence):
            errors.append(f"{label}.evidence must be non-empty and at most 2000 characters.")
        if not nonempty_text(action):
            errors.append(f"{label}.operator_action must be non-empty and at most 2000 characters.")
        if TOKEN_LIKE_RE.search(str(evidence)) or TOKEN_LIKE_RE.search(str(action)):
            errors.append(f"{label} appears to contain a secret-like token.")
        normalized.append({
            "finding_id": finding_id,
            "assessment": assessment,
            "confidence": confidence,
            "evidence": str(evidence or "").strip(),
            "operator_action": str(action or "").strip(),
        })

    canonical = json.dumps(response, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return {
        "schema_version": 1,
        "valid": not errors,
        "audit_id": expected_audit_id,
        "reviewer_id": gate.get("reviewer_id"),
        "response_sha256": hashlib.sha256(canonical).hexdigest(),
        "errors": errors,
        "observations": normalized if not errors else [],
        "deterministic_findings_modified": False,
    }


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description="Validate a bounded same-agent review response without changing deterministic findings.")
    value.add_argument("--findings", required=True, help="Deterministic <prefix>_findings.json file.")
    value.add_argument("--response", required=True, help="Agent-produced JSON response matching the packet contract.")
    value.add_argument("--output", help="Validation output path. Defaults beside the response file.")
    return value


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    findings_path = Path(args.findings).expanduser().resolve()
    response_path = Path(args.response).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve() if args.output else response_path.with_suffix(".validated.json")
    try:
        result = validate_response(load_json(findings_path), load_json(response_path))
    except Exception as exc:
        result = {
            "schema_version": 1,
            "valid": False,
            "errors": [f"validation_input_error: {exc}"],
            "observations": [],
            "deterministic_findings_modified": False,
        }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Agent review response: {'valid' if result.get('valid') else 'invalid'}")
    print(f"validation: {output_path}")
    for error in result.get("errors") or []:
        print(f"  - {error}")
    return 0 if result.get("valid") else 1


if __name__ == "__main__":
    raise SystemExit(main())
