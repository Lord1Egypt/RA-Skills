#!/usr/bin/env python3
"""Controlled problem resolution, verification and traced reopening."""

import argparse
from datetime import datetime
import json
import sys

from management_common import (
    RecordError, Store, add_record, artifact_errors, cell, get_record, link_errors,
    now, require_strings, require_text, seal_artifact, write_view,
)

REGISTRY = "07-quality/PROBLEMS.json"
VIEW = "07-quality/PROBLEMS.md"
STATES = {"NEW", "TRIAGED", "IN_PROGRESS", "RESOLVED", "VERIFIED", "CLOSED"}
SEVERITIES = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
DISPOSITIONS = {"FIXED", "DUPLICATE", "REJECTED"}


def store(project):
    return Store(project, REGISTRY, "problems", "PRB")


def event(actor, rationale, **fields):
    return {"actor": require_text(actor, "actor"), "rationale": require_text(rationale, "rationale"),
            "at": now(), **fields}


def evidence(project, paths):
    paths = require_strings(paths or [], "evidence paths")
    if not paths:
        raise RecordError("At least one evidence artifact is required")
    return [seal_artifact(project, path) for path in paths]


def event_errors(project, value, label, artifacts=False):
    errors = []
    if not isinstance(value, dict):
        return [f"{label} must be an object"]
    try:
        require_text(value.get("actor"), label + " actor")
        require_text(value.get("rationale"), label + " rationale")
        stamp = datetime.fromisoformat(require_text(value.get("at"), label + " timestamp"))
        if stamp.tzinfo is None:
            raise RecordError(label + " timestamp requires timezone")
    except (RecordError, ValueError) as exc:
        errors.append(str(exc))
    if artifacts:
        items = value.get("evidence")
        if not isinstance(items, list) or not items:
            errors.append(label + " requires sealed evidence")
        else:
            for item in items:
                errors.extend(label + ": " + error for error in artifact_errors(project, item))
    return errors


def validate_registry(project, data):
    errors = store(project).errors(data)
    if errors:
        return errors
    known = {record["id"]: record for record in data["records"]}
    duplicates = {}
    for record in data["records"]:
        identifier = record["id"]
        record_errors = []
        try:
            if record["status"] not in STATES:
                raise RecordError("Unknown problem status")
            require_text(record.get("description"), "problem description")
            if record.get("severity") not in SEVERITIES:
                raise RecordError("Invalid severity")
            if type(record.get("release_blocking")) is not bool:
                raise RecordError("release_blocking must be a boolean")
            for key in ("tasks", "requirements", "changes"):
                require_strings(record.get(key), key)
            for key in ("triage", "resolution", "verification", "closure"):
                if key not in record:
                    raise RecordError("Missing problem field: " + key)
            if record["status"] != "NEW" and record["triage"] is None:
                record_errors.append("Triaged problems require triage rationale")
            if record["status"] == "NEW" and any(record[field] is not None for field in ("triage", "resolution", "verification", "closure")):
                record_errors.append("NEW problem cannot have resolution metadata")
            resolved = record["status"] in {"RESOLVED", "VERIFIED", "CLOSED"}
            if resolved != (record["resolution"] is not None):
                record_errors.append("Resolution metadata does not match problem status")
            verified = record["status"] in {"VERIFIED", "CLOSED"}
            if verified != (record["verification"] is not None):
                record_errors.append("Verification metadata does not match problem status")
            if (record["status"] == "CLOSED") != (record["closure"] is not None):
                record_errors.append("Closure metadata does not match problem status")
            resolution = record["resolution"]
            if isinstance(resolution, dict):
                disposition = resolution.get("disposition")
                if disposition not in DISPOSITIONS:
                    record_errors.append("Invalid resolution disposition")
                duplicate = resolution.get("duplicate_of")
                if disposition == "DUPLICATE":
                    if duplicate == identifier or duplicate not in known:
                        record_errors.append("Duplicate disposition needs a distinct existing problem reference")
                    else:
                        duplicates[identifier] = duplicate
                elif duplicate is not None:
                    record_errors.append("Only DUPLICATE may reference duplicate_of")
        except (RecordError, KeyError, TypeError) as exc:
            record_errors.append(str(exc))
        record_errors.extend(link_errors(project, record))
        for field, artifacts in (("triage", False), ("resolution", True), ("verification", True),
                                  ("closure", False), ("last_update", False), ("last_transition", False)):
            if record.get(field) is not None:
                record_errors.extend(event_errors(project, record[field], field, artifacts))
        errors.extend(f"{identifier}: {error}" for error in record_errors)
    for identifier in duplicates:
        visited, current = set(), identifier
        while current in duplicates:
            if current in visited:
                errors.append(f"{identifier}: duplicate references form a cycle")
                break
            visited.add(current)
            current = duplicates[current]
    return errors


def checked(project, data):
    errors = validate_registry(project, data)
    if errors:
        raise RecordError("Invalid problem registry: " + "; ".join(errors))


def render(project, data):
    lines = ["# Problem Register", "", "Generated from PROBLEMS.json. Do not edit this view.", "",
             "| ID | Title | Owner | Severity | Status | Release blocking | Disposition | Duplicate of |",
             "|---|---|---|---|---|---|---|---|"]
    for record in data["records"]:
        resolution = record.get("resolution") or {}
        values = [record["id"], record["title"], record["owner"], record["severity"], record["status"],
                  record["release_blocking"], resolution.get("disposition", "—"), resolution.get("duplicate_of") or "—"]
        lines.append("| " + " | ".join(cell(value) for value in values) + " |")
    write_view(project, VIEW, "\n".join(lines) + "\n")


def audit(project, release=False):
    if not store(project).exists():
        return [], []
    try:
        data = store(project).read()
        errors = validate_registry(project, data)
    except (RecordError, OSError, ValueError) as exc:
        return [str(exc)], []
    warnings = []
    if errors:
        return errors, warnings
    known = {record["id"]: record for record in data["records"]}
    for record in data["records"]:
        if not record["release_blocking"]:
            continue
        target = record
        # Closing a duplicate resolves the duplicate report, not its underlying
        # defect. Preserve the original release obligation through that chain,
        # including when a formerly closed canonical problem is reopened.
        while (target["status"] == "CLOSED" and
               (target.get("resolution") or {}).get("disposition") == "DUPLICATE"):
            target = known[target["resolution"]["duplicate_of"]]
        if target["status"] != "CLOSED":
            if target["id"] == record["id"]:
                message = f"{record['id']}: release-blocking problem is {record['status']}"
            else:
                message = (f"{record['id']}: release-blocking duplicate still depends on "
                           f"{target['id']} in {target['status']}")
            (errors if release else warnings).append(message)
    return errors, warnings


def mutate(project, actor, action, operation):
    def guarded(data):
        checked(project, data)
        return operation(data)
    data = store(project).update(actor, action, guarded, validator=validate_registry)
    try:
        render(project, store(project).read())
    except (RecordError, OSError, ValueError) as exc:
        print("WARNING: problem registry update committed; Markdown view needs rebuilding with render "
              f"({type(exc).__name__})", file=sys.stderr)
    return data


def transition(project, data, identifier, target, actor, reason, *, disposition=None, duplicate_of=None, artifacts=None):
    record = get_record(data, identifier)
    current = record["status"]
    require_text(reason, "transition rationale")
    if target != "RESOLVED" and (disposition is not None or duplicate_of is not None):
        raise RecordError("Disposition options apply only to RESOLVED")
    if target not in {"RESOLVED", "VERIFIED"} and artifacts:
        raise RecordError("Evidence options apply only to RESOLVED or VERIFIED")
    if current == "NEW" and target == "TRIAGED":
        record["triage"] = event(actor, reason)
    elif current == "TRIAGED" and target == "IN_PROGRESS":
        pass
    elif current in {"RESOLVED", "VERIFIED", "CLOSED"} and target == "IN_PROGRESS":
        record.update(resolution=None, verification=None, closure=None)
    elif target == "RESOLVED" and current in {"TRIAGED", "IN_PROGRESS"}:
        if disposition not in DISPOSITIONS:
            raise RecordError("Resolution requires FIXED, DUPLICATE or REJECTED disposition")
        if current == "TRIAGED" and disposition == "FIXED":
            raise RecordError("A fix must pass through IN_PROGRESS")
        if disposition == "DUPLICATE":
            if duplicate_of == identifier:
                raise RecordError("A problem cannot duplicate itself")
            get_record(data, duplicate_of)
        elif duplicate_of is not None:
            raise RecordError("duplicate_of applies only to DUPLICATE")
        record["resolution"] = event(actor, reason, disposition=disposition, duplicate_of=duplicate_of,
                                      evidence=evidence(project, artifacts))
    elif current == "RESOLVED" and target == "VERIFIED":
        record["verification"] = event(actor, reason, evidence=evidence(project, artifacts))
    elif current == "VERIFIED" and target == "CLOSED":
        record["closure"] = event(actor, reason)
    else:
        raise RecordError(f"Invalid problem transition: {current} -> {target}")
    record["status"] = target
    record["last_transition"] = event(actor, reason)
    return identifier


def boolean(value):
    if value not in {"true", "false"}:
        raise argparse.ArgumentTypeError("Expected true or false")
    return value == "true"


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("init", "create", "update", "transition", "audit", "list", "render"):
        command = commands.add_parser(name)
        if name in {"init", "create", "update", "transition"}:
            command.add_argument("--actor", required=True)
        if name in {"update", "transition"}:
            command.add_argument("id")
            command.add_argument("--reason", required=True)
        if name in {"create", "update"}:
            command.add_argument("--title", required=name == "create")
            command.add_argument("--owner", required=name == "create")
            command.add_argument("--description", required=name == "create")
            command.add_argument("--severity", choices=sorted(SEVERITIES), required=name == "create")
            command.add_argument("--release-blocking", type=boolean, default=True if name == "create" else None)
            for field in ("task", "requirement", "change"):
                command.add_argument("--" + field, action="append")
                if name == "update":
                    command.add_argument("--clear-" + field + "s", action="store_true")
        if name == "transition":
            command.add_argument("--to", choices=sorted(STATES), required=True)
            command.add_argument("--disposition", choices=sorted(DISPOSITIONS))
            command.add_argument("--duplicate-of")
            command.add_argument("--evidence", action="append")
        if name == "audit":
            command.add_argument("--release", action="store_true")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        registry = store(args.project)
        if args.command == "init":
            registry.initialize(args.actor)
            data = registry.read()
            checked(args.project, data)
            render(args.project, data)
        elif args.command == "create":
            def create(data):
                record = add_record(data, "PRB", args.title, args.owner, "NEW",
                                    description=args.description, severity=args.severity, release_blocking=args.release_blocking,
                                    tasks=args.task or [], requirements=args.requirement or [], changes=args.change or [],
                                    triage=None, resolution=None, verification=None, closure=None)
                return record["id"]
            data = mutate(args.project, args.actor, "create problem", create)
            print(data["records"][-1]["id"])
        elif args.command == "update":
            def update(data):
                record = get_record(data, args.id)
                if record["status"] not in {"NEW", "TRIAGED", "IN_PROGRESS"}:
                    raise RecordError("Reopen the problem before changing its assessed content")
                changed = False
                for field in ("title", "owner", "description", "severity", "release_blocking"):
                    value = getattr(args, field)
                    if value is not None:
                        record[field] = value
                        changed = True
                for singular, plural in (("task", "tasks"), ("requirement", "requirements"), ("change", "changes")):
                    values, clear = getattr(args, singular), getattr(args, "clear_" + plural)
                    if values and clear:
                        raise RecordError(f"Cannot set and clear {plural} together")
                    if values is not None or clear:
                        record[plural] = values or []
                        changed = True
                if not changed:
                    raise RecordError("No problem update fields supplied")
                record["last_update"] = event(args.actor, args.reason)
                return args.id
            mutate(args.project, args.actor, "update problem", update)
        elif args.command == "transition":
            mutate(args.project, args.actor, "transition problem", lambda data: transition(
                args.project, data, args.id, args.to, args.actor, args.reason, disposition=args.disposition,
                duplicate_of=args.duplicate_of, artifacts=args.evidence))
        elif args.command == "audit":
            errors, warnings = audit(args.project, args.release)
            print(json.dumps({"errors": errors, "warnings": warnings}, indent=2))
            return 1 if errors else 0
        else:
            data = registry.read()
            checked(args.project, data)
            if args.command == "render":
                render(args.project, data)
            else:
                print(json.dumps(data["records"], indent=2, ensure_ascii=False))
        return 0
    except (RecordError, OSError, ValueError, TypeError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
