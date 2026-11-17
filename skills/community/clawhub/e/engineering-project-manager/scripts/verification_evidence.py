#!/usr/bin/env python3
"""Authoritative verification and test evidence registry for Project Manager."""

import argparse
import fcntl
import hashlib
import json
import re
import sys
from contextlib import contextmanager
from pathlib import Path

from pm_common import (
    VERIFICATION_ACTIVITIES,
    VERIFICATION_METHODS,
    VERIFICATION_SCOPES,
    VERSIONED_REQ_PATTERN,
    active_requirement_records,
    git_capture,
    parse_requirement_record,
    read_text,
    requirement_definitions,
    utc_timestamp,
    write_json_atomic,
    write_text_atomic,
)

MODEL_VERSION = "1.0"
EV_ID_RE = re.compile(r"^EV-(\d{3,})$")
RESULTS = {"PASS", "FAIL", "BLOCKED", "SKIPPED"}
STATUSES = {"PLANNED", "IN_PROGRESS", "PASS", "FAIL", "BLOCKED", "SKIPPED", "SUPERSEDED"}
MUTABLE_STATUSES = {"PLANNED", "IN_PROGRESS", "FAIL", "BLOCKED", "SKIPPED"}
ARTIFACT_TYPES = {"REPORT", "LOG", "DATA", "IMAGE", "VIDEO", "BUILD", "MEASUREMENT", "OTHER"}


class EvidenceError(RuntimeError):
    pass


def locations(project):
    root = Path(project) / "05-verification"
    return {
        "root": root,
        "marker": root / "EVIDENCE-MANAGEMENT.json",
        "registry": root / "EVIDENCE.json",
        "index": root / "EVIDENCE.md",
        "records": root / "evidence",
        "lock": root / ".evidence.lock",
    }


@contextmanager
def evidence_lock(project):
    loc = locations(project)
    loc["root"].mkdir(parents=True, exist_ok=True)
    with loc["lock"].open("a+", encoding="utf-8") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(stream, fcntl.LOCK_UN)


def empty_registry():
    return {
        "model": "PROJECT_MANAGER_VERIFICATION_EVIDENCE",
        "model_version": MODEL_VERSION,
        "registry_revision": 0,
        "next_number": 1,
        "evidence": [],
    }


def load_registry(project, required=True):
    path = locations(project)["registry"]
    if not path.exists():
        if required:
            raise EvidenceError("Verification evidence management is not initialized")
        return empty_registry()
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvidenceError(f"Cannot read evidence registry: {exc}") from exc


def save_registry(project, registry, expected_revision):
    current = load_registry(project)
    if current.get("registry_revision") != expected_revision:
        raise EvidenceError("Evidence registry was modified concurrently; retry the operation")
    registry["registry_revision"] = expected_revision + 1
    write_json_atomic(locations(project)["registry"], registry)
    render_all(project, registry)


def evidence_by_id(registry, evidence_id):
    for item in registry.get("evidence", []):
        if item.get("Evidence_ID") == evidence_id:
            return item
    raise EvidenceError(f"Unknown Evidence_ID: {evidence_id}")


def requirement_model(project):
    definitions = requirement_definitions(project)
    by_id = {}
    latest_v11 = {}
    for item in definitions:
        by_id[item["id"]] = item
        if item.get("scheme") == "V1.1":
            record = parse_requirement_record(item)
            by_id[item["id"]] = record
            current = latest_v11.get(record["base_id"])
            if current is None or record["revision_number"] > current["revision_number"]:
                latest_v11[record["base_id"]] = record
    return definitions, by_id, latest_v11


def find_requirement(project, requirement_id):
    _, by_id, _ = requirement_model(project)
    item = by_id.get(requirement_id)
    if item is None:
        raise EvidenceError(f"Requirement does not exist: {requirement_id}")
    if item.get("scheme") == "V1.1":
        if (item.get("status") or "").upper() == "CANCELLED":
            raise EvidenceError(f"Cannot register evidence against a CANCELLED requirement: {requirement_id}")
    return item


def validate_evidence_against_requirement(evidence, requirement):
    if requirement.get("scheme") != "V1.1":
        return []
    errors = []
    comparisons = (
        ("Verification_Method", "verification_method"),
        ("Verification_Scope", "verification_scope"),
        ("Verification_Activity", "verification_activity"),
        ("Verification_Process", "verification_process"),
    )
    for evidence_key, requirement_key in comparisons:
        expected = requirement.get(requirement_key)
        actual = evidence.get(evidence_key)
        if expected and actual != expected:
            errors.append(
                f"{evidence['Evidence_ID']}: {evidence_key} {actual} does not match "
                f"requirement strategy {expected}"
            )
    return errors


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_artifact(project, path_value, artifact_type="OTHER", checksum=None):
    raw = Path(path_value)
    if raw.is_absolute() or ".." in raw.parts:
        raise EvidenceError(f"Artifact must be a project-relative path without traversal: {path_value}")
    resolved = (Path(project) / raw).resolve()
    if not resolved.is_relative_to(Path(project).resolve()):
        raise EvidenceError(f"Artifact resolves outside the project: {path_value}")
    artifact_type = artifact_type.upper()
    if artifact_type not in ARTIFACT_TYPES:
        raise EvidenceError(f"Invalid artifact type: {artifact_type}")
    result = {
        "path": raw.as_posix(),
        "type": artifact_type,
        "recorded_at": utc_timestamp(),
    }
    absolute = Path(project) / raw
    if checksum:
        result["sha256"] = checksum
    elif absolute.is_file():
        result["sha256"] = sha256_file(absolute)
    return result


def event(evidence, actor, event_type, comment=None):
    evidence.setdefault("History", []).append({
        "timestamp": utc_timestamp(),
        "actor": actor,
        "event": event_type,
        "comment": comment,
    })


def validate_registry(project, registry=None):
    registry = registry or load_registry(project)
    errors, warnings = [], []
    if registry.get("model") != "PROJECT_MANAGER_VERIFICATION_EVIDENCE":
        errors.append("Invalid verification evidence registry model")
    if registry.get("model_version") != MODEL_VERSION:
        errors.append("Unsupported verification evidence model version")
    records = registry.get("evidence")
    if not isinstance(records, list):
        return ["evidence must be a list"], []
    ids = [item.get("Evidence_ID") for item in records]
    if len(ids) != len(set(ids)):
        errors.append("Evidence identifiers are not unique")
    max_used = max(
        (int(match.group(1)) for value in ids if isinstance(value, str) and (match := EV_ID_RE.fullmatch(value))),
        default=0,
    )
    if registry.get("next_number", 0) <= max_used:
        errors.append("next_number would reuse an Evidence_ID")

    _, by_id, _ = requirement_model(project)
    for item in records:
        evidence_id = item.get("Evidence_ID")
        if not isinstance(evidence_id, str) or not EV_ID_RE.fullmatch(evidence_id):
            errors.append(f"Invalid Evidence_ID: {evidence_id}")
            continue
        required = (
            "Requirement_ID", "Verification_Method", "Verification_Scope",
            "Verification_Activity", "Verification_Process", "Test_Case",
            "Status", "Created_At", "Created_By", "History",
        )
        for field in required:
            if field not in item or item[field] in (None, ""):
                errors.append(f"{evidence_id}: required field missing: {field}")
        if item.get("Status") not in STATUSES:
            errors.append(f"{evidence_id}: invalid Status: {item.get('Status')}")
        for field, values in (
            ("Verification_Method", VERIFICATION_METHODS),
            ("Verification_Scope", VERIFICATION_SCOPES),
            ("Verification_Activity", VERIFICATION_ACTIVITIES),
        ):
            if item.get(field) and item[field] not in values:
                errors.append(f"{evidence_id}: invalid {field}: {item[field]}")
        if item.get("Verification_Process") and not re.fullmatch(r"[A-Z]{2,6}\d{1,2}", item["Verification_Process"]):
            errors.append(f"{evidence_id}: invalid Verification_Process: {item['Verification_Process']}")

        test_case = item.get("Test_Case")
        if not isinstance(test_case, dict):
            errors.append(f"{evidence_id}: Test_Case must be an object")
            test_case = {}
        for field in ("Test_Case_ID", "Title", "Objective", "Expected_Result"):
            if not test_case.get(field):
                errors.append(f"{evidence_id}: Test_Case.{field} is required")

        requirement_id = item.get("Requirement_ID")
        requirement = by_id.get(requirement_id)
        if requirement is None:
            errors.append(f"{evidence_id}: requirement does not exist: {requirement_id}")
        else:
            if requirement.get("scheme") == "V1.1" and (requirement.get("status") or "").upper() == "CANCELLED":
                errors.append(f"{evidence_id}: requirement is CANCELLED: {requirement_id}")
            errors.extend(validate_evidence_against_requirement(item, requirement))

        execution = item.get("Execution")
        status = item.get("Status")
        if status in RESULTS or status == "SUPERSEDED":
            if not isinstance(execution, dict):
                errors.append(f"{evidence_id}: Execution is required for status {status}")
                execution = {}
            for field in ("Execution_ID", "Executed_At", "Executed_By", "Environment", "Git_Commit", "Result", "Result_Summary"):
                if not execution.get(field):
                    errors.append(f"{evidence_id}: Execution.{field} is required")
            if status in RESULTS and execution.get("Result") != status:
                errors.append(f"{evidence_id}: Status and Execution.Result disagree")
            if execution.get("Result") not in RESULTS:
                errors.append(f"{evidence_id}: invalid Execution.Result: {execution.get('Result')}")
            commit = execution.get("Git_Commit")
            if commit and git_capture(project, "cat-file", "-e", f"{commit}^{{commit}}") is None:
                errors.append(f"{evidence_id}: execution Git commit does not exist: {commit}")
        elif execution not in (None, {}):
            errors.append(f"{evidence_id}: Execution must be empty while status is {status}")

        baseline = item.get("Configuration_Baseline")
        if baseline:
            baseline_path = Path(project) / "08-configuration" / "baselines" / f"{baseline}.json"
            if not baseline_path.is_file():
                errors.append(f"{evidence_id}: configuration baseline does not exist: {baseline}")

        artifacts = item.get("Artifacts", [])
        if not isinstance(artifacts, list):
            errors.append(f"{evidence_id}: Artifacts must be a list")
            artifacts = []
        for number, artifact in enumerate(artifacts, 1):
            if not isinstance(artifact, dict):
                errors.append(f"{evidence_id}: artifact {number} must be an object")
                continue
            relative = artifact.get("path")
            artifact_type = artifact.get("type")
            if not isinstance(relative, str) or not relative.strip():
                errors.append(f"{evidence_id}: artifact {number} path is required")
                continue
            path_value = Path(relative)
            if path_value.is_absolute() or ".." in path_value.parts:
                errors.append(f"{evidence_id}: artifact path is unsafe: {relative}")
                continue
            if not (Path(project) / path_value).resolve().is_relative_to(Path(project).resolve()):
                errors.append(f"{evidence_id}: artifact resolves outside the project: {relative}")
                continue
            if artifact_type not in ARTIFACT_TYPES:
                errors.append(f"{evidence_id}: invalid artifact type: {artifact_type}")
            absolute = Path(project) / path_value
            checksum = artifact.get("sha256")
            if not absolute.is_file():
                message = f"{evidence_id}: artifact does not exist yet: {relative}"
                (errors if status in {"PASS", "SUPERSEDED"} else warnings).append(message)
            elif status in {"PASS", "SUPERSEDED"} and not checksum:
                errors.append(f"{evidence_id}: completed artifact requires SHA-256: {relative}")
            elif checksum and sha256_file(absolute) != checksum:
                errors.append(f"{evidence_id}: artifact SHA-256 mismatch: {relative}")

        history = item.get("History", [])
        if not isinstance(history, list) or not history:
            errors.append(f"{evidence_id}: History must contain a creation event")
            history = []
        if history and history[0].get("event") != "CREATED":
            errors.append(f"{evidence_id}: first history event must be CREATED")
        previous_time = ""
        for number, entry in enumerate(history, 1):
            for field in ("timestamp", "actor", "event"):
                if not entry.get(field):
                    errors.append(f"{evidence_id}: history event {number} missing {field}")
            timestamp = entry.get("timestamp", "")
            if timestamp < previous_time:
                errors.append(f"{evidence_id}: history timestamps are not ordered")
            previous_time = timestamp

        if item.get("Status") == "SUPERSEDED":
            replacement = item.get("Superseded_By")
            if replacement not in ids:
                errors.append(f"{evidence_id}: replacement evidence does not exist: {replacement}")
            else:
                # A valid chain may grow when its replacement is itself
                # superseded, but it must terminate in a distinct PASS record.
                seen = {evidence_id}
                while replacement in ids:
                    if replacement in seen:
                        errors.append(f"{evidence_id}: cyclic evidence supersession")
                        break
                    seen.add(replacement)
                    successor = evidence_by_id(registry, replacement)
                    if successor.get("Status") == "PASS":
                        break
                    if successor.get("Status") != "SUPERSEDED":
                        errors.append(f"{evidence_id}: replacement chain must end in PASS evidence")
                        break
                    replacement = successor.get("Superseded_By")
    return errors, warnings


def active_requirements_for_coverage(project):
    definitions, by_id, latest = requirement_model(project)
    requirements = []
    for item in definitions:
        if item.get("scheme") == "V1.1":
            record = by_id[item["id"]]
            if latest.get(record["base_id"]) is record and (record.get("status") or "").upper() != "CANCELLED":
                requirements.append(record)
        else:
            requirements.append(item)
    return sorted(requirements, key=lambda item: item["id"])


def requirement_is_covered(project, registry, requirement):
    for item in registry.get("evidence", []):
        if item.get("Requirement_ID") != requirement["id"]:
            continue
        if item.get("Status") != "PASS":
            continue
        if validate_evidence_against_requirement(item, requirement):
            continue
        return True
    return False


def coverage(project, registry=None):
    registry = registry or load_registry(project)
    covered, uncovered = [], []
    for requirement in active_requirements_for_coverage(project):
        if requirement_is_covered(project, registry, requirement):
            covered.append(requirement["id"])
        else:
            uncovered.append(requirement["id"])
    return covered, uncovered


def render_record(item):
    test_case = item.get("Test_Case", {})
    execution = item.get("Execution") or {}
    lines = [
        f"# {item['Evidence_ID']} - {test_case.get('Title', 'Evidence')}", "",
        f"- Status: {item.get('Status')}",
        f"- Requirement: {item.get('Requirement_ID')}",
        f"- Verification Strategy: {item.get('Verification_Method')} / {item.get('Verification_Scope')} / "
        f"{item.get('Verification_Activity')} / {item.get('Verification_Process')}",
        f"- Configuration Baseline: {item.get('Configuration_Baseline') or 'NOT_SET'}",
        "", "## Test Case", "",
        f"- ID: {test_case.get('Test_Case_ID')}",
        f"- Objective: {test_case.get('Objective')}",
        f"- Environment: {test_case.get('Environment') or 'NOT_SET'}",
        f"- Expected Result: {test_case.get('Expected_Result')}",
        "", "## Procedure", "",
    ]
    procedure = test_case.get("Procedure", [])
    lines.extend(f"{number}. {step}" for number, step in enumerate(procedure, 1))
    if not procedure:
        lines.append("1. Execute the prescribed verification.")
    lines.extend(["", "## Execution", ""])
    if execution:
        lines.extend([
            f"- ID: {execution.get('Execution_ID')}",
            f"- Executed At: {execution.get('Executed_At')}",
            f"- Executed By: {execution.get('Executed_By')}",
            f"- Environment: {execution.get('Environment')}",
            f"- Git Commit: {execution.get('Git_Commit')}",
            f"- Result: {execution.get('Result')}",
            f"- Summary: {execution.get('Result_Summary')}",
        ])
    else:
        lines.append("Not executed yet.")
    lines.extend(["", "## Artifacts", ""])
    artifacts = item.get("Artifacts", [])
    lines.extend(
        f"- `{artifact.get('path')}` ({artifact.get('type')}) `{artifact.get('sha256') or ''}`"
        for artifact in artifacts
    )
    if not artifacts:
        lines.append("- None")
    lines.extend(["", "## History", "", "| Timestamp | Actor | Event | Comment |", "|---|---|---|---|"])
    for entry in item.get("History", []):
        comment = str(entry.get("comment") or "").replace("|", "\\|")
        lines.append(
            f"| {entry.get('timestamp', '')} | {entry.get('actor', '')} | {entry.get('event', '')} | "
            f"{comment} |"
        )
    return "\n".join(lines) + "\n"


def render_all(project, registry=None):
    registry = registry or load_registry(project)
    loc = locations(project)
    loc["records"].mkdir(parents=True, exist_ok=True)
    lines = [
        "# Verification Evidence", "",
        f"Model version: {registry.get('model_version')}", "",
        "| Evidence ID | Requirement | Status | Method | Scope | Activity | Process |",
        "|---|---|---|---|---|---|---|",
    ]
    for item in registry.get("evidence", []):
        lines.append(
            f"| {item['Evidence_ID']} | {item['Requirement_ID']} | {item['Status']} | "
            f"{item['Verification_Method']} | {item['Verification_Scope']} | "
            f"{item['Verification_Activity']} | {item['Verification_Process']} |"
        )
        write_text_atomic(loc["records"] / f"{item['Evidence_ID']}.md", render_record(item))
    if not registry.get("evidence"):
        lines.append("| - | No evidence records | - | - | - | - | - |")
    write_text_atomic(loc["index"], "\n".join(lines) + "\n")


def registry_is_valid_or_raise(project, registry):
    errors, warnings = validate_registry(project, registry)
    for warning in warnings:
        print(f"WARN: {warning}")
    if errors:
        raise EvidenceError("Invalid evidence registry: " + "; ".join(errors))


def create_record(project, registry, args):
    requirement = find_requirement(project, args.requirement_id)
    defaults = {
        "Verification_Method": requirement.get("verification_method"),
        "Verification_Scope": requirement.get("verification_scope"),
        "Verification_Activity": requirement.get("verification_activity"),
        "Verification_Process": requirement.get("verification_process"),
    }
    values = {
        "Verification_Method": args.method or defaults["Verification_Method"],
        "Verification_Scope": args.scope or defaults["Verification_Scope"],
        "Verification_Activity": args.activity or defaults["Verification_Activity"],
        "Verification_Process": args.process or defaults["Verification_Process"],
    }
    for key, value in values.items():
        if not value:
            raise EvidenceError(f"{key} is required and cannot be inferred from {args.requirement_id}")
    number = registry["next_number"]
    evidence_id = f"EV-{number:03d}"
    registry["next_number"] = number + 1
    artifacts = [
        normalize_artifact(project, path, args.artifact_type)
        for path in (args.artifact or [])
    ]
    record = {
        "Evidence_ID": evidence_id,
        "Requirement_ID": args.requirement_id,
        **values,
        "Configuration_Baseline": args.baseline,
        "Test_Case": {
            "Test_Case_ID": args.test_case_id or f"TC-{number:03d}",
            "Title": args.title,
            "Objective": args.objective,
            "Environment": args.environment,
            "Procedure": args.procedure or [],
            "Expected_Result": args.expected_result,
        },
        "Execution": None,
        "Artifacts": artifacts,
        "Status": "PLANNED",
        "Created_At": utc_timestamp(),
        "Created_By": args.actor,
        "Superseded_By": None,
        "History": [],
    }
    event(record, args.actor, "CREATED", "Evidence record created")
    registry["evidence"].append(record)
    return record


def record_result(project, registry, evidence, args):
    if evidence.get("Status") not in MUTABLE_STATUSES:
        raise EvidenceError(f"Cannot record a result from status {evidence.get('Status')}")
    result = args.result
    number = int(EV_ID_RE.fullmatch(evidence["Evidence_ID"]).group(1))
    execution = evidence.get("Execution") or {}
    execution.update({
        "Execution_ID": execution.get("Execution_ID") or f"EX-{number:03d}",
        "Executed_At": utc_timestamp(),
        "Executed_By": args.actor,
        "Environment": args.environment or evidence.get("Test_Case", {}).get("Environment") or "NOT_SET",
        "Git_Commit": git_capture(project, "rev-parse", "HEAD") or "NOT_SET",
        "Result": result,
        "Result_Summary": args.summary,
    })
    evidence["Execution"] = execution
    evidence["Status"] = result
    evidence["Artifacts"].extend(
        normalize_artifact(project, path, args.artifact_type)
        for path in (args.artifact or [])
    )
    # Planned artifacts may not have existed at creation. Seal them when the
    # result is recorded so a later file edit cannot silently change its proof.
    for artifact in evidence["Artifacts"]:
        if not artifact.get("sha256"):
            artifact.update(normalize_artifact(
                project, artifact["path"], artifact.get("type", "OTHER")
            ))
    if args.baseline:
        evidence["Configuration_Baseline"] = args.baseline
    event(evidence, args.actor, f"RESULT_{result}", args.summary)


def build_parser():
    parser = argparse.ArgumentParser(description="Manage Project Manager verification evidence")
    parser.add_argument("--project", default=".")
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="Initialize authoritative evidence management")
    init.add_argument("--actor", required=True)
    create = commands.add_parser("create", help="Create a planned verification evidence record")
    create.add_argument("--requirement-id", required=True)
    create.add_argument("--title", required=True)
    create.add_argument("--objective", required=True)
    create.add_argument("--expected-result", required=True)
    create.add_argument("--actor", required=True)
    create.add_argument("--test-case-id")
    create.add_argument("--environment")
    create.add_argument("--procedure", action="append")
    create.add_argument("--method", choices=sorted(VERIFICATION_METHODS))
    create.add_argument("--scope", choices=sorted(VERIFICATION_SCOPES))
    create.add_argument("--activity", choices=sorted(VERIFICATION_ACTIVITIES))
    create.add_argument("--process")
    create.add_argument("--baseline")
    create.add_argument("--artifact", action="append")
    create.add_argument("--artifact-type", default="REPORT", choices=sorted(ARTIFACT_TYPES))
    commands.add_parser("list", help="List evidence records")
    show = commands.add_parser("show", help="Show one evidence record")
    show.add_argument("evidence_id")
    start = commands.add_parser("start", help="Mark evidence as IN_PROGRESS")
    start.add_argument("evidence_id")
    start.add_argument("--actor", required=True)
    result = commands.add_parser("record-result", help="Record PASS, FAIL, BLOCKED, or SKIPPED")
    result.add_argument("evidence_id")
    result.add_argument("--result", required=True, choices=sorted(RESULTS))
    result.add_argument("--actor", required=True)
    result.add_argument("--summary", required=True)
    result.add_argument("--environment")
    result.add_argument("--baseline")
    result.add_argument("--artifact", action="append")
    result.add_argument("--artifact-type", default="REPORT", choices=sorted(ARTIFACT_TYPES))
    supersede = commands.add_parser("supersede", help="Supersede evidence with a newer record")
    supersede.add_argument("evidence_id")
    supersede.add_argument("--by", required=True)
    supersede.add_argument("--actor", required=True)
    supersede.add_argument("--comment")
    commands.add_parser("validate", help="Validate the authoritative registry")
    coverage_cmd = commands.add_parser("coverage", help="Report requirements lacking PASS evidence")
    coverage_cmd.add_argument("--strict", action="store_true")
    commands.add_parser("assess", help="Non-destructively report existing task evidence and reports")
    commands.add_parser("render", help="Regenerate Markdown evidence views")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    project = Path(args.project).resolve()
    try:
        if args.command == "init":
            with evidence_lock(project):
                registry = load_registry(project, required=False)
                loc = locations(project)
                loc["records"].mkdir(parents=True, exist_ok=True)
                write_json_atomic(loc["marker"], {
                    "model": "PROJECT_MANAGER_VERIFICATION_EVIDENCE_MANAGEMENT",
                    "model_version": MODEL_VERSION,
                    "enabled": True,
                    "enabled_at": utc_timestamp(),
                    "enabled_by": args.actor,
                })
                if not loc["registry"].exists():
                    write_json_atomic(loc["registry"], registry)
                render_all(project, registry)
            print("Verification evidence management initialized")
            return 0

        registry = load_registry(project)
        if args.command == "list":
            for item in registry["evidence"]:
                print(f"{item['Evidence_ID']}\t{item['Status']}\t{item['Requirement_ID']}\t{item['Test_Case'].get('Title')}")
            return 0
        if args.command == "show":
            print(render_record(evidence_by_id(registry, args.evidence_id)), end="")
            return 0
        if args.command == "render":
            render_all(project, registry)
            print("Evidence Markdown views regenerated")
            return 0
        if args.command == "validate":
            errors, warnings = validate_registry(project, registry)
            for warning in warnings:
                print(f"WARN: {warning}")
            for error in errors:
                print(f"ERROR: {error}")
            print(f"EVIDENCE VALIDATION: {'FAIL' if errors else 'PASS'}")
            return 1 if errors else 0
        if args.command == "coverage":
            covered, uncovered = coverage(project, registry)
            print(f"Covered requirements: {len(covered)}")
            print(f"Uncovered requirements: {len(uncovered)}")
            for requirement_id in uncovered:
                print(f"UNCOVERED: {requirement_id}")
            print(f"EVIDENCE COVERAGE: {'FAIL' if uncovered and args.strict else 'PASS'}")
            return 1 if uncovered and args.strict else 0
        if args.command == "assess":
            report = assess_existing_evidence(project)
            print(json.dumps(report, indent=2, sort_keys=True))
            return 0

        with evidence_lock(project):
            registry = load_registry(project)
            revision = registry["registry_revision"]
            if args.command == "create":
                record = create_record(project, registry, args)
            else:
                evidence = evidence_by_id(registry, args.evidence_id)
                if args.command == "start":
                    if evidence["Status"] != "PLANNED":
                        raise EvidenceError(f"start requires PLANNED, got {evidence['Status']}")
                    evidence["Status"] = "IN_PROGRESS"
                    event(evidence, args.actor, "IN_PROGRESS")
                elif args.command == "record-result":
                    record_result(project, registry, evidence, args)
                elif args.command == "supersede":
                    if evidence["Status"] != "PASS":
                        raise EvidenceError("Only PASS evidence can be superseded")
                    if args.by == args.evidence_id:
                        raise EvidenceError("Evidence cannot supersede itself")
                    replacement = evidence_by_id(registry, args.by)
                    if replacement["Status"] != "PASS":
                        raise EvidenceError("Replacement evidence must be PASS")
                    evidence["Status"] = "SUPERSEDED"
                    evidence["Superseded_By"] = args.by
                    event(evidence, args.actor, "SUPERSEDED", args.comment or f"Superseded by {args.by}")
            errors, warnings = validate_registry(project, registry)
            for warning in warnings:
                print(f"WARN: {warning}")
            if errors:
                raise EvidenceError("Invalid evidence registry: " + "; ".join(errors))
            save_registry(project, registry, revision)
            if args.command == "create":
                print(record["Evidence_ID"])
        return 0
    except EvidenceError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


def assess_existing_evidence(project):
    report = {
        "task_evidence_references": [],
        "verification_reports": [],
        "evidence_registry_records": 0,
        "migration_note": "References are reported only; no record is created or modified.",
    }
    tasks_path = Path(project) / "00-project/management/TASKS.json"
    if tasks_path.is_file():
        try:
            tasks = json.loads(tasks_path.read_text(encoding="utf-8"))
            for task in tasks.get("tasks", []):
                for item in task.get("evidence", []):
                    report["task_evidence_references"].append({
                        "task": task.get("id"),
                        "reference": item,
                    })
        except (OSError, json.JSONDecodeError) as exc:
            report["task_evidence_error"] = str(exc)
    verification_root = Path(project) / "05-verification"
    if verification_root.is_dir():
        report["verification_reports"] = sorted(
            path.relative_to(project).as_posix()
            for path in verification_root.rglob("*VERIFICATION-REPORT.md")
        )
    registry_path = verification_root / "EVIDENCE.json"
    if registry_path.is_file():
        try:
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            report["evidence_registry_records"] = len(registry.get("evidence", []))
        except (OSError, json.JSONDecodeError) as exc:
            report["evidence_registry_error"] = str(exc)
    return report


if __name__ == "__main__":
    sys.exit(main())
