#!/usr/bin/env python3
"""Controlled engineering risks with evidenced mitigation and explicit acceptance."""

import argparse
from datetime import datetime
import json
import sys

from management_common import (
    RecordError, Store, add_record, artifact_errors, cell, get_record, link_errors,
    now, require_date, require_strings, require_text, seal_artifact, write_view,
)

REGISTRY = "09-risks/RISKS.json"
VIEW = "09-risks/RISKS.md"
STATES = {"OPEN", "MITIGATING", "MITIGATED", "ACCEPTED", "CLOSED"}
HIGH_SCORE = 15


def store(project):
    return Store(project, REGISTRY, "risks", "RISK")


def rating(value, label):
    if type(value) is not int or not 1 <= value <= 5:
        raise RecordError(f"{label} must be an integer from 1 to 5")
    return value


def event(actor, rationale, **fields):
    return {"actor": require_text(actor, "actor"), "rationale": require_text(rationale, "rationale"),
            "at": now(), **fields}


def evidence(project, paths):
    paths = require_strings(paths or [], "evidence paths")
    if not paths:
        raise RecordError("At least one evidence artifact is required")
    return [seal_artifact(project, path) for path in paths]


def event_errors(project, value, label, *, artifacts=False, acceptance=False):
    errors = []
    if not isinstance(value, dict):
        return [f"{label} must be an object"]
    try:
        require_text(value.get("actor"), f"{label} actor")
        require_text(value.get("rationale"), f"{label} rationale")
        stamp = require_text(value.get("at"), f"{label} timestamp")
        if datetime.fromisoformat(stamp).tzinfo is None:
            raise RecordError(f"{label} timestamp requires timezone")
        if acceptance:
            date = require_date(value.get("review_date"), "acceptance review date")
            if date < stamp[:10]:
                errors.append(f"{label}: review date precedes acceptance")
    except (RecordError, ValueError) as exc:
        errors.append(str(exc))
    if artifacts:
        items = value.get("evidence")
        if not isinstance(items, list) or not items:
            errors.append(f"{label} requires sealed evidence")
        else:
            for item in items:
                errors.extend(f"{label}: {error}" for error in artifact_errors(project, item))
    return errors


def effective_score(record):
    """Unverified lower estimates do not reduce the initial exposure."""
    if record.get("mitigation_result") is not None:
        return record["residual_probability"] * record["residual_impact"]
    return record["probability"] * record["impact"]


def acceptance_current(record):
    value = record.get("acceptance")
    return record.get("status") == "ACCEPTED" and isinstance(value, dict) and value.get("review_date", "") >= now()[:10]


def validate_registry(project, data):
    errors = store(project).errors(data)
    if errors:
        return errors
    for record in data["records"]:
        identifier = record["id"]
        record_errors = []
        try:
            if record["status"] not in STATES:
                raise RecordError("Unknown risk status")
            require_text(record.get("description"), "risk description")
            rating(record.get("probability"), "probability")
            rating(record.get("impact"), "impact")
            if not isinstance(record.get("mitigation"), str):
                raise RecordError("mitigation must be a string")
            if record["mitigation"]:
                require_text(record["mitigation"], "mitigation plan")
            if record["status"] in {"MITIGATING", "MITIGATED"}:
                require_text(record["mitigation"], "mitigation plan")
            for key in ("tasks", "requirements", "changes"):
                require_strings(record.get(key), key)
            if record.get("review_due") is not None:
                require_date(record["review_due"], "review_due")
            for key in ("mitigation_result", "acceptance", "closure", "last_review"):
                if key not in record:
                    raise RecordError(f"Missing risk field: {key}")
            residual = record.get("residual_probability"), record.get("residual_impact")
            if any(value is not None for value in residual):
                rating(residual[0], "residual probability")
                rating(residual[1], "residual impact")
            if record["status"] in {"MITIGATED", "ACCEPTED", "CLOSED"}:
                rating(residual[0], "residual probability")
                rating(residual[1], "residual impact")
            if record["status"] in {"OPEN", "MITIGATING"} and (record["mitigation_result"] is not None or
                    record["acceptance"] is not None or record["closure"] is not None or any(v is not None for v in residual)):
                record_errors.append("Open or mitigating risks cannot retain disposition or residual evidence")
            if record["status"] == "MITIGATED" and record["mitigation_result"] is None:
                record_errors.append("MITIGATED requires mitigation evidence")
            if record["status"] == "ACCEPTED" and record["acceptance"] is None:
                record_errors.append("ACCEPTED requires explicit acceptance")
            if record["status"] != "ACCEPTED" and record["status"] != "CLOSED" and record["acceptance"] is not None:
                record_errors.append("Acceptance is incompatible with the risk status")
            if record["status"] == "CLOSED" and record["closure"] is None:
                record_errors.append("CLOSED requires closure proof")
            if record["status"] != "CLOSED" and record["closure"] is not None:
                record_errors.append("Closure proof is incompatible with the risk status")
            if record["mitigation_result"] is None and any(v is not None for v in residual) and residual != (record["probability"], record["impact"]):
                record_errors.append("A reduced residual estimate requires sealed mitigation evidence")
        except (RecordError, TypeError, KeyError) as exc:
            record_errors.append(str(exc))
        record_errors.extend(link_errors(project, record))
        for field, artifacts, accepted in (("mitigation_result", True, False), ("acceptance", False, True),
                                            ("closure", True, False), ("last_review", False, False),
                                            ("last_update", False, False), ("last_transition", False, False)):
            if record.get(field) is not None:
                record_errors.extend(event_errors(project, record[field], field, artifacts=artifacts, acceptance=accepted))
        errors.extend(f"{identifier}: {error}" for error in record_errors)
    return errors


def checked(project, data):
    errors = validate_registry(project, data)
    if errors:
        raise RecordError("Invalid risk registry: " + "; ".join(errors))


def render(project, data):
    lines = ["# Risk Register", "", "Generated from RISKS.json. Do not edit this view.", "",
             "Probability and impact each use 1–5. High exposure is score >= 15.", "",
             "| ID | Title | Owner | Status | Initial score | Effective score | Review due | Acceptance review |",
             "|---|---|---|---|---|---|---|---|"]
    for record in data["records"]:
        values = [record["id"], record["title"], record["owner"], record["status"],
                  record["probability"] * record["impact"], effective_score(record), record.get("review_due") or "—",
                  (record.get("acceptance") or {}).get("review_date", "—")]
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
    for record in data["records"]:
        if record["status"] == "CLOSED":
            continue
        if record.get("review_due") and record["review_due"] < now()[:10]:
            warnings.append(f"{record['id']}: risk review is overdue")
        if record["status"] == "ACCEPTED" and not acceptance_current(record):
            warnings.append(f"{record['id']}: residual-risk acceptance has expired")
        if effective_score(record) >= HIGH_SCORE and not acceptance_current(record):
            message = f"{record['id']}: high risk requires current explicit acceptance or evidenced closure/mitigation"
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
        print("WARNING: risk registry update committed; Markdown view needs rebuilding with render "
              f"({type(exc).__name__})", file=sys.stderr)
    return data


def transition(project, data, identifier, target, actor, reason, *, residual_probability=None,
               residual_impact=None, artifacts=None, review_date=None):
    record = get_record(data, identifier)
    current = record["status"]
    require_text(reason, "transition rationale")
    if target != "MITIGATED" and (residual_probability is not None or residual_impact is not None):
        raise RecordError("Residual ratings apply only to MITIGATED")
    if target not in {"MITIGATED", "CLOSED"} and artifacts:
        raise RecordError("Evidence options apply only to MITIGATED or CLOSED")
    if target != "ACCEPTED" and review_date is not None:
        raise RecordError("Acceptance review date applies only to ACCEPTED")
    if target == "OPEN" and current in {"MITIGATING", "MITIGATED", "ACCEPTED", "CLOSED"}:
        record.update(mitigation_result=None, acceptance=None, closure=None, residual_probability=None, residual_impact=None)
    elif target == "MITIGATING" and current == "OPEN":
        require_text(record["mitigation"], "mitigation plan")
    elif target == "MITIGATED" and current == "MITIGATING":
        record["residual_probability"] = rating(residual_probability, "residual probability")
        record["residual_impact"] = rating(residual_impact, "residual impact")
        record["mitigation_result"] = event(actor, reason, evidence=evidence(project, artifacts))
    elif target == "ACCEPTED" and current in {"OPEN", "MITIGATING", "MITIGATED", "ACCEPTED"}:
        date = require_date(review_date, "acceptance review date")
        if date < now()[:10]:
            raise RecordError("Acceptance review date cannot be in the past")
        if record["mitigation_result"] is None:
            record["residual_probability"], record["residual_impact"] = record["probability"], record["impact"]
        record["acceptance"] = event(actor, reason, review_date=date)
    elif target == "CLOSED" and current in {"MITIGATED", "ACCEPTED"}:
        record["closure"] = event(actor, reason, evidence=evidence(project, artifacts))
    else:
        raise RecordError(f"Invalid risk transition: {current} -> {target}")
    record["status"] = target
    record["last_transition"] = event(actor, reason)
    return identifier


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("init", "create", "update", "transition", "review", "audit", "list", "render"):
        command = commands.add_parser(name)
        if name in {"init", "create", "update", "transition", "review"}:
            command.add_argument("--actor", required=True)
        if name in {"update", "transition", "review"}:
            command.add_argument("id")
            command.add_argument("--reason", required=True)
        if name in {"create", "update"}:
            command.add_argument("--title", required=name == "create")
            command.add_argument("--owner", required=name == "create")
            command.add_argument("--description", required=name == "create")
            command.add_argument("--probability", type=int, required=name == "create")
            command.add_argument("--impact", type=int, required=name == "create")
            command.add_argument("--mitigation")
            command.add_argument("--review-due")
            for field in ("task", "requirement", "change"):
                command.add_argument("--" + field, action="append")
                if name == "update":
                    command.add_argument("--clear-" + field + "s", action="store_true")
        if name == "transition":
            command.add_argument("--to", choices=sorted(STATES), required=True)
            command.add_argument("--residual-probability", type=int)
            command.add_argument("--residual-impact", type=int)
            command.add_argument("--evidence", action="append")
            command.add_argument("--review-date")
        if name == "review":
            command.add_argument("--next-review-date", required=True)
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
                record = add_record(data, "RISK", args.title, args.owner, "OPEN",
                                    description=args.description, probability=args.probability, impact=args.impact,
                                    mitigation=args.mitigation or "", review_due=args.review_due,
                                    residual_probability=None, residual_impact=None, mitigation_result=None,
                                    acceptance=None, closure=None, last_review=None,
                                    tasks=args.task or [], requirements=args.requirement or [], changes=args.change or [])
                return record["id"]
            data = mutate(args.project, args.actor, "create risk", create)
            print(data["records"][-1]["id"])
        elif args.command == "update":
            def update(data):
                record = get_record(data, args.id)
                if record["status"] not in {"OPEN", "MITIGATING"}:
                    raise RecordError("Reopen the risk before changing its assessed content")
                changed = False
                for field in ("title", "owner", "description", "probability", "impact", "mitigation", "review_due"):
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
                    raise RecordError("No risk update fields supplied")
                record["last_update"] = event(args.actor, args.reason)
                return args.id
            mutate(args.project, args.actor, "update risk", update)
        elif args.command == "transition":
            mutate(args.project, args.actor, "transition risk", lambda data: transition(
                args.project, data, args.id, args.to, args.actor, args.reason,
                residual_probability=args.residual_probability, residual_impact=args.residual_impact,
                artifacts=args.evidence, review_date=args.review_date))
        elif args.command == "review":
            def review(data):
                record = get_record(data, args.id)
                if record["status"] == "CLOSED":
                    raise RecordError("Reopen a closed risk before scheduling another review")
                due = require_date(args.next_review_date, "next review date")
                if due < now()[:10]:
                    raise RecordError("Next review date cannot be in the past")
                record["review_due"] = due
                record["last_review"] = event(args.actor, args.reason)
                return args.id
            mutate(args.project, args.actor, "review risk (does not renew acceptance)", review)
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
