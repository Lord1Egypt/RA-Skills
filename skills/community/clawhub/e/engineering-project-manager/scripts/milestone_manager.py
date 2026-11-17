#!/usr/bin/env python3
"""Controlled milestones with task dependencies and sealed acceptance evidence."""

from __future__ import annotations

import argparse
from datetime import date, datetime
import json
from pathlib import Path
import sys

from management_common import (RecordError, Store, add_record, artifact_errors, cell,
                               get_record, link_errors, now, require_date,
                               project_file, require_strings, require_text, seal_artifact, task_records, write_view)

REGISTRY = "00-project/management/MILESTONES.json"
VIEW = "00-project/management/MILESTONES.md"
SELF_ARTIFACTS = {REGISTRY, VIEW, "00-project/management/.milestones.lock"}
STATUSES = {"PLANNED", "ACTIVE", "BLOCKED", "ACHIEVED", "CANCELLED"}
EDITABLE = {"PLANNED", "ACTIVE", "BLOCKED"}
TRANSITIONS = {
    "PLANNED": {"ACTIVE", "BLOCKED", "CANCELLED"},
    "ACTIVE": {"BLOCKED", "ACHIEVED", "CANCELLED"},
    "BLOCKED": {"ACTIVE", "ACHIEVED", "CANCELLED"},
    "ACHIEVED": set(),
    "CANCELLED": set(),
}


def store(project) -> Store:
    return Store(project, REGISTRY, "milestones", "MS")


def task_statuses(project) -> dict[str, str]:
    try:
        return {identifier: record["status"] for identifier, record in task_records(project).items()}
    except (OSError, UnicodeError, ValueError, TypeError, KeyError) as exc:
        raise RecordError("linked task registry cannot be read") from exc


def seal_proof(project, relative):
    path = project_file(project, relative).resolve()
    root = Path(project).resolve()
    if path in {root / item for item in SELF_ARTIFACTS}:
        raise RecordError("milestone registry, view and lock cannot serve as their own acceptance proof")
    return seal_artifact(project, relative)


def review_errors(review, label: str, required_fields) -> list[str]:
    if not isinstance(review, dict):
        return [label + " must be an object"]
    errors = []
    for field in required_fields:
        try:
            require_text(review.get(field), label + " " + field)
        except RecordError as exc:
            errors.append(str(exc))
    if review.get("actor") == review.get("reviewer"):
        errors.append(label + " needs a distinct reviewer label; labels are not authentication")
    try:
        if datetime.fromisoformat(review.get("reviewed_at", "")).tzinfo is None:
            errors.append(label + " review timestamp requires a timezone")
    except (TypeError, ValueError):
        errors.append(label + " review timestamp is invalid")
    return errors


def history_errors(data) -> list[str]:
    errors, replay = [], {}
    for event in data["history"]:
        after = event["after"]
        previous = replay.get(event["record_id"])
        action = event["action"]
        label = event["record_id"]
        if previous is None:
            if action != "create" or after.get("status") != "PLANNED":
                errors.append(label + ": milestone history must begin with PLANNED creation")
        elif action == "update":
            if (not isinstance(previous.get("status"), str) or previous.get("status") not in EDITABLE or
                    after.get("status") != previous.get("status")):
                errors.append(label + ": invalid update in milestone history")
        elif action.startswith("transition:"):
            source, target = previous.get("status"), after.get("status")
            prior_cancel = previous.get("cancellation")
            new_cancel = after.get("cancellation")
            waiver_addition = (source == target == "CANCELLED" and isinstance(prior_cancel, dict) and
                              isinstance(new_cancel, dict) and prior_cancel.get("release_waiver") is None and
                              isinstance(new_cancel.get("release_waiver"), dict) and
                              {key: value for key, value in prior_cancel.items() if key != "release_waiver"} ==
                              {key: value for key, value in new_cancel.items() if key != "release_waiver"})
            if (not isinstance(source, str) or not isinstance(target, str) or
                    target not in TRANSITIONS.get(source, set()) and not waiver_addition or
                    action != "transition:" + str(target)):
                errors.append(label + ": invalid transition in milestone history")
        else:
            errors.append(label + ": unknown milestone history action")
        if previous and previous.get("release_required") is True and after.get("release_required") is not True:
            errors.append(label + ": release-required obligation was removed in history")
        replay[event["record_id"]] = after
    return errors


def validate_registry(project, data) -> list[str]:
    """Validate common ledger plus milestone semantics, links and current proof."""
    errors = store(project).errors(data)
    if errors or not isinstance(data, dict) or not isinstance(data.get("records"), list):
        return errors
    errors.extend(history_errors(data))
    records = [record for record in data["records"] if isinstance(record, dict)]
    by_id = {record["id"]: record for record in records if isinstance(record.get("id"), str)}
    graph = {}
    for record in records:
        identifier = record.get("id", "[invalid milestone]")
        label = identifier if isinstance(identifier, str) else "[invalid milestone]"
        status = record.get("status")
        if not isinstance(status, str) or status not in STATUSES:
            errors.append(label + ": invalid milestone status")
            status = "INVALID"
        for field in ("title", "owner"):
            try:
                require_text(record.get(field), label + " " + field)
            except RecordError as exc:
                errors.append(str(exc))
        try:
            require_date(record.get("due_date"), label + " due_date")
        except RecordError as exc:
            errors.append(str(exc))
        lists = {}
        for field in ("tasks", "depends_on", "acceptance_criteria"):
            try:
                lists[field] = require_strings(record.get(field), label + " " + field)
            except RecordError as exc:
                errors.append(str(exc))
                lists[field] = []
        if not lists["acceptance_criteria"]:
            errors.append(label + ": at least one acceptance criterion is required")
        if type(record.get("release_required")) is not bool:
            errors.append(label + ": release_required must be a boolean")
        errors.extend(link_errors(project, record))
        graph[label] = lists["depends_on"]
        for dependency in lists["depends_on"]:
            if dependency not in by_id:
                errors.append(label + ": unknown milestone dependency " + dependency)
            if dependency == label:
                errors.append(label + ": self dependency is forbidden")
        if status == "BLOCKED":
            try:
                require_text(record.get("blocker"), label + " blocker")
            except RecordError as exc:
                errors.append(str(exc))
        elif record.get("blocker") is not None:
            errors.append(label + ": only BLOCKED milestones may have a blocker")
        completion = record.get("completion")
        if status == "ACHIEVED":
            errors.extend(review_errors(completion, label + " completion", ("actor", "reviewer", "review_note", "reviewed_at")))
            if isinstance(completion, dict):
                criteria = completion.get("criteria")
                if not isinstance(criteria, list):
                    errors.append(label + ": completion criteria must be a list")
                else:
                    actual = []
                    for proof in criteria:
                        if not isinstance(proof, dict):
                            errors.append(label + ": criterion proof must be an object")
                            continue
                        actual.append(proof.get("criterion"))
                        artifacts = proof.get("artifacts")
                        if not isinstance(artifacts, list) or not artifacts:
                            errors.append(label + ": each completed criterion requires sealed artifacts")
                            continue
                        paths = []
                        for artifact in artifacts:
                            errors.extend(label + ": " + error for error in artifact_errors(project, artifact))
                            if isinstance(artifact, dict):
                                paths.append(artifact.get("path"))
                                if isinstance(artifact.get("path"), str) and artifact["path"] in SELF_ARTIFACTS:
                                    errors.append(label + ": milestone runtime files cannot be acceptance proof")
                        if any(not isinstance(path, str) for path in paths) or len(paths) != len(set(paths)):
                            errors.append(label + ": criterion artifact paths must be unique strings")
                    if actual != lists["acceptance_criteria"]:
                        errors.append(label + ": all criteria need exactly one ordered completion record")
            if lists["tasks"]:
                try:
                    tasks = task_statuses(project)
                    for task in lists["tasks"]:
                        if tasks.get(task) != "DONE":
                            errors.append(label + ": linked task is not DONE: " + task)
                except RecordError as exc:
                    errors.append(label + ": " + str(exc))
            for dependency in lists["depends_on"]:
                if by_id.get(dependency, {}).get("status") != "ACHIEVED":
                    errors.append(label + ": dependency is not ACHIEVED: " + dependency)
        elif completion is not None:
            errors.append(label + ": only ACHIEVED milestones may have completion proof")
        cancellation = record.get("cancellation")
        if status == "CANCELLED":
            if not isinstance(cancellation, dict):
                errors.append(label + ": cancellation must be an object")
            else:
                for field in ("actor", "rationale", "cancelled_at"):
                    try:
                        require_text(cancellation.get(field), label + " cancellation " + field)
                    except RecordError as exc:
                        errors.append(str(exc))
                try:
                    if datetime.fromisoformat(cancellation.get("cancelled_at", "")).tzinfo is None:
                        errors.append(label + ": cancellation timestamp requires a timezone")
                except (TypeError, ValueError):
                    errors.append(label + ": cancellation timestamp is invalid")
                waiver = cancellation.get("release_waiver")
                if waiver is not None:
                    errors.extend(review_errors(waiver, label + " release waiver", ("actor", "reviewer", "rationale", "reviewed_at")))
                    if record.get("release_required") is not True:
                        errors.append(label + ": only a release-required milestone needs a release waiver")
        elif cancellation is not None:
            errors.append(label + ": only CANCELLED milestones may have cancellation records")
    # Kahn's algorithm also handles long graphs without Python recursion limits.
    remaining = {key: {dependency for dependency in deps if dependency in graph} for key, deps in graph.items()}
    while remaining:
        roots = {key for key, deps in remaining.items() if not deps}
        if not roots:
            errors.append("milestone dependency graph contains a cycle")
            break
        remaining = {key: deps - roots for key, deps in remaining.items() if key not in roots}
    return errors


def render(project, data) -> None:
    lines = ["# Milestones", "", "Derived from MILESTONES.json. Rebuild this view; do not edit it as authoritative data.", "",
             "| ID | Milestone | Owner | Due | Status | Release required | Tasks | Dependencies |",
             "|---|---|---|---|---|---|---|---|"]
    for record in data["records"]:
        values = [record["id"], record["title"], record["owner"], record["due_date"], record["status"],
                  "YES" if record["release_required"] else "NO", ", ".join(record["tasks"]), ", ".join(record["depends_on"])]
        lines.append("| " + " | ".join(cell(value) for value in values) + " |")
    for record in data["records"]:
        lines.extend(["", "## " + cell(record["id"]) + " — " + cell(record["title"]), ""])
        lines.extend(str(index) + ". " + cell(criterion) for index, criterion in enumerate(record["acceptance_criteria"], 1))
        if record["blocker"]:
            lines.extend(["", "Blocker: " + cell(record["blocker"])])
        completion = record["completion"]
        if completion:
            lines.extend(["", "Review: " + cell(completion["review_note"]),
                          "", "Recorded actor / reviewer: " + cell(completion["actor"]) + " / " + cell(completion["reviewer"])])
            for proof in completion["criteria"]:
                for artifact in proof["artifacts"]:
                    lines.append("- Evidence: " + cell(artifact["path"]) + " (SHA-256: " + artifact["sha256"] + ")")
        cancellation = record["cancellation"]
        if cancellation:
            lines.extend(["", "Cancellation: " + cell(cancellation["rationale"])])
            waiver = cancellation["release_waiver"]
            if waiver:
                lines.extend(["", "Release waiver: " + cell(waiver["rationale"]) + "; reviewer: " + cell(waiver["reviewer"])])
            elif record["release_required"]:
                lines.extend(["", "Release remains blocked: explicit reviewed release waiver missing."])
    lines.extend(["", "Actor and reviewer labels record declared responsibility; they do not authenticate an approval.", ""])
    write_view(project, VIEW, "\n".join(lines))


def initialize(project, actor):
    registry = store(project)
    registry.initialize(actor)
    data = registry.read()
    errors = validate_registry(project, data)
    if errors:
        raise RecordError("; ".join(errors))
    render(project, data)
    return data


def validated_update(project, actor, action, operation):
    def checked(data):
        errors = validate_registry(project, data)
        if errors:
            raise RecordError("; ".join(errors))
        return operation(data)
    return store(project).update(actor, action, checked, validate_registry)


def create(project, *, actor, title, owner, due_date, acceptance_criteria,
           tasks=None, depends_on=None, release_required=False):
    def operation(data):
        record = add_record(data, "MS", require_text(title, "title"), require_text(owner, "owner"), "PLANNED",
                            due_date=require_date(due_date, "due_date"),
                            acceptance_criteria=require_strings(acceptance_criteria, "acceptance_criteria"),
                            tasks=require_strings(tasks if tasks is not None else [], "tasks"),
                            depends_on=require_strings(depends_on if depends_on is not None else [], "depends_on"),
                            release_required=release_required, blocker=None, completion=None, cancellation=None)
        return record["id"]
    data = validated_update(project, actor, "create", operation)
    render(project, data)
    return data


def update(project, identifier, *, actor, title=None, owner=None, due_date=None,
           acceptance_criteria=None, tasks=None, depends_on=None, release_required=None):
    def operation(data):
        record = get_record(data, identifier)
        if record["status"] not in EDITABLE:
            raise RecordError("achieved and cancelled milestones are immutable")
        changes = {"title": title, "owner": owner, "due_date": due_date,
                   "acceptance_criteria": acceptance_criteria, "tasks": tasks,
                   "depends_on": depends_on, "release_required": release_required}
        if not any(value is not None for value in changes.values()):
            raise RecordError("update requires at least one field")
        if record["release_required"] and release_required is False:
            raise RecordError("release_required cannot be removed; use explicit reviewed cancellation waiver")
        for key, value in changes.items():
            if value is not None:
                if key in ("title", "owner"):
                    value = require_text(value, key)
                elif key in ("acceptance_criteria", "tasks", "depends_on"):
                    value = require_strings(value, key)
                record[key] = value
        return record["id"]
    data = validated_update(project, actor, "update", operation)
    render(project, data)
    return data


def transition(project, identifier, status, *, actor, reason=None, reviewer=None,
               review_note=None, criterion_evidence=None, waiver_rationale=None, waiver_reviewer=None):
    """criterion_evidence is {one_based_index: [relative artifact paths]}."""
    if not isinstance(status, str) or status not in STATUSES:
        raise RecordError("invalid milestone target status")
    def operation(data):
        record = get_record(data, identifier)
        adding_waiver = (record["status"] == status == "CANCELLED" and waiver_rationale is not None and
                        record["cancellation"]["release_waiver"] is None)
        if status not in TRANSITIONS[record["status"]] and not adding_waiver:
            raise RecordError("milestone transition is not allowed")
        if status != "ACHIEVED" and any(value is not None for value in (reviewer, review_note, criterion_evidence)):
            raise RecordError("completion review and evidence apply only to ACHIEVED")
        if status != "CANCELLED" and any(value is not None for value in (waiver_rationale, waiver_reviewer)):
            raise RecordError("release waiver applies only to CANCELLED")
        if status not in {"BLOCKED", "CANCELLED"} and reason is not None:
            raise RecordError("reason applies only to blocking or cancellation; completion uses review_note")
        if status == "ACHIEVED":
            expected = set(range(1, len(record["acceptance_criteria"]) + 1))
            if (not isinstance(criterion_evidence, dict) or any(type(index) is not int for index in criterion_evidence)
                    or set(criterion_evidence) != expected):
                raise RecordError("supply evidence for each acceptance criterion exactly once")
            criteria = []
            for index, criterion in enumerate(record["acceptance_criteria"], 1):
                paths = require_strings(criterion_evidence[index], "criterion evidence paths")
                if not paths:
                    raise RecordError("each criterion requires at least one artifact")
                artifacts = [seal_proof(project, path) for path in paths]
                criteria.append({"criterion": criterion, "artifacts": artifacts})
            record["completion"] = {"actor": require_text(actor, "actor"), "reviewer": require_text(reviewer, "reviewer"),
                                    "review_note": require_text(review_note, "review_note"), "reviewed_at": now(), "criteria": criteria}
        if status == "CANCELLED":
            if not adding_waiver:
                record["cancellation"] = {"actor": require_text(actor, "actor"),
                                          "rationale": require_text(reason, "cancellation rationale"),
                                          "cancelled_at": now(), "release_waiver": None}
            elif reason is not None:
                raise RecordError("an existing cancellation rationale cannot be rewritten while adding its waiver")
            if waiver_rationale is not None or waiver_reviewer is not None:
                if not record["release_required"]:
                    raise RecordError("release waiver requires a release-required milestone")
                record["cancellation"]["release_waiver"] = {
                    "actor": require_text(actor, "waiver actor"), "reviewer": require_text(waiver_reviewer, "waiver reviewer"),
                    "rationale": require_text(waiver_rationale, "waiver rationale"), "reviewed_at": now()}
        record["blocker"] = require_text(reason, "blocker reason") if status == "BLOCKED" else None
        record["status"] = status
        return record["id"]
    data = validated_update(project, actor, "transition:" + str(status), operation)
    render(project, data)
    return data


def audit(project, release=False):
    registry = store(project)
    if not registry.exists():
        return [], []
    try:
        data = registry.read()
    except (RecordError, OSError, UnicodeError, ValueError) as exc:
        return ["Milestone registry: " + str(exc)], []
    errors = validate_registry(project, data)
    warnings = []
    today = date.today().isoformat()
    for record in data.get("records", []):
        if not isinstance(record, dict):
            continue
        identifier = str(record.get("id", "[invalid milestone]"))
        if record.get("status") in EDITABLE:
            try:
                if require_date(record.get("due_date"), "due_date") < today:
                    warnings.append(identifier + ": milestone is overdue")
            except RecordError:
                pass
        if release and record.get("release_required") is True and record.get("status") != "ACHIEVED":
            cancellation = record.get("cancellation")
            waived = (record.get("status") == "CANCELLED" and isinstance(cancellation, dict) and
                      isinstance(cancellation.get("release_waiver"), dict) and
                      not review_errors(cancellation["release_waiver"], "waiver", ("actor", "reviewer", "rationale", "reviewed_at")))
            if waived:
                warnings.append(identifier + ": release-required milestone was explicitly waived; it is not ACHIEVED")
            else:
                errors.append(identifier + ": release-required milestone is unmet and has no valid explicit waiver")
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    commands = parser.add_subparsers(dest="command", required=True)
    init_parser = commands.add_parser("init")
    init_parser.add_argument("--actor", required=True)
    for command in ("create", "update"):
        sub = commands.add_parser(command)
        sub.add_argument("--actor", required=True)
        if command == "update":
            sub.add_argument("id")
        sub.add_argument("--title", required=command == "create")
        sub.add_argument("--owner", required=command == "create")
        sub.add_argument("--due-date", required=command == "create")
        sub.add_argument("--criterion", action="append", required=command == "create")
        sub.add_argument("--task", action="append")
        sub.add_argument("--depends-on", action="append")
        sub.add_argument("--release-required", action="store_true", default=False if command == "create" else None)
        if command == "update":
            sub.add_argument("--clear-tasks", action="store_true")
            sub.add_argument("--clear-dependencies", action="store_true")
    change = commands.add_parser("transition")
    change.add_argument("id")
    change.add_argument("status", choices=sorted(STATUSES))
    change.add_argument("--actor", required=True)
    change.add_argument("--reason")
    change.add_argument("--reviewer")
    change.add_argument("--review-note")
    change.add_argument("--criterion-evidence", action="append", help="Repeat INDEX=relative/path, with 1-based criterion index")
    change.add_argument("--waiver-rationale")
    change.add_argument("--waiver-reviewer")
    check = commands.add_parser("audit")
    check.add_argument("--release", action="store_true")
    commands.add_parser("list")
    commands.add_parser("render")
    args = parser.parse_args()
    try:
        if args.command == "init":
            data = initialize(args.project, args.actor)
        elif args.command in {"create", "update"}:
            if getattr(args, "clear_tasks", False) and args.task or getattr(args, "clear_dependencies", False) and args.depends_on:
                raise RecordError("do not combine clear flags with replacement values")
            fields = dict(actor=args.actor, title=args.title, owner=args.owner, due_date=args.due_date,
                          acceptance_criteria=args.criterion, tasks=[] if getattr(args, "clear_tasks", False) else args.task,
                          depends_on=[] if getattr(args, "clear_dependencies", False) else args.depends_on,
                          release_required=args.release_required)
            data = create(args.project, **fields) if args.command == "create" else update(args.project, args.id, **fields)
        elif args.command == "transition":
            evidence = None
            if args.criterion_evidence is not None:
                evidence = {}
                for item in args.criterion_evidence:
                    index, separator, path = item.partition("=")
                    if not separator or not index.isdigit() or int(index) < 1 or not path:
                        raise RecordError("criterion evidence must use positive INDEX=relative/path")
                    evidence.setdefault(int(index), []).append(path)
            data = transition(args.project, args.id, args.status, actor=args.actor, reason=args.reason, reviewer=args.reviewer,
                              review_note=args.review_note, criterion_evidence=evidence,
                              waiver_rationale=args.waiver_rationale, waiver_reviewer=args.waiver_reviewer)
        elif args.command == "audit":
            errors, warnings = audit(args.project, args.release)
            print(json.dumps({"errors": errors, "warnings": warnings}, indent=2))
            return 1 if errors else 0
        else:
            data = store(args.project).read()
            errors = validate_registry(args.project, data)
            if errors:
                raise RecordError("; ".join(errors))
            if args.command == "render":
                render(args.project, data)
        print(json.dumps(data, indent=2))
        return 0
    except (RecordError, OSError, UnicodeError) as exc:
        print("MILESTONE ERROR: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
