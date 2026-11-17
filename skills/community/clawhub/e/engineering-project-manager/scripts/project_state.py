#!/usr/bin/env python3

import argparse
import fcntl
import json
import os
from contextlib import contextmanager
from datetime import datetime, timezone

from pm_common import write_text_atomic

PRIO = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
VALID_STATUS = {
    "BACKLOG", "READY", "IN_PROGRESS", "BLOCKED", "REVIEW", "REWORK",
    "DONE", "CANCELLED",
}


def now():
    return datetime.now(timezone.utc).isoformat()


def paths(project):
    plan = os.path.join(project, "00-project/management")
    os.makedirs(plan, exist_ok=True)
    return (
        os.path.join(plan, "TASKS.json"),
        os.path.join(plan, "TASKS.md"),
    )


@contextmanager
def task_lock(project):
    plan = os.path.join(project, "00-project/management")
    os.makedirs(plan, exist_ok=True)
    with open(os.path.join(plan, ".tasks.lock"), "a+", encoding="utf-8") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(stream, fcntl.LOCK_UN)


def normalize_state(data):
    """Fill optional V1 task fields without changing canonical semantics."""

    if not isinstance(data, dict):
        return data
    data.setdefault("history", [])
    tasks = data.get("tasks")
    if not isinstance(tasks, list):
        return data
    for task in tasks:
        if not isinstance(task, dict):
            continue
        for field in (
            "depends_on", "requirements", "acceptance_criteria", "outputs", "evidence"
        ):
            task.setdefault(field, [])
        task.setdefault("workstream", "")
        task.setdefault("domain", "")
        task.setdefault("process", "")
        task.setdefault("blocker", None)
    return data


def validate_state(data):
    errors = []
    if not isinstance(data, dict):
        return ["task state must be a JSON object"]
    if data.get("schema_version") != 1:
        errors.append("unsupported task schema_version")
    tasks = data.get("tasks")
    history = data.get("history")
    if not isinstance(tasks, list):
        return errors + ["tasks must be a list"]
    if not isinstance(history, list):
        errors.append("history must be a list")

    identifiers = []
    for index, task in enumerate(tasks, 1):
        if not isinstance(task, dict):
            errors.append(f"task {index} must be an object")
            continue
        identifier = task.get("id")
        if not isinstance(identifier, str) or not identifier.strip():
            errors.append(f"task {index} has no valid id")
            continue
        identifiers.append(identifier)
        if not isinstance(task.get("title"), str) or not task["title"].strip():
            errors.append(f"{identifier}: title is required")
        if task.get("priority") not in PRIO:
            errors.append(f"{identifier}: invalid priority {task.get('priority')}")
        if task.get("status") not in VALID_STATUS:
            errors.append(f"{identifier}: invalid status {task.get('status')}")
        for field in (
            "depends_on", "requirements", "acceptance_criteria", "outputs", "evidence"
        ):
            if not isinstance(task.get(field), list):
                errors.append(f"{identifier}: {field} must be a list")
            elif any(not isinstance(value, str) or not value.strip() for value in task[field]):
                errors.append(f"{identifier}: {field} must contain non-empty strings")

    if len(identifiers) != len(set(identifiers)):
        errors.append("task identifiers must be unique")
    known = set(identifiers)
    graph = {}
    for task in tasks:
        if not isinstance(task, dict) or not isinstance(task.get("id"), str):
            continue
        dependencies = task.get("depends_on", [])
        if not isinstance(dependencies, list) or any(not isinstance(value, str) for value in dependencies):
            continue
        graph[task["id"]] = dependencies
        for dependency in dependencies:
            if dependency not in known:
                errors.append(f"{task['id']}: unknown dependency {dependency}")
            if dependency == task["id"]:
                errors.append(f"{task['id']}: self dependency is forbidden")

    visiting, visited = set(), set()

    def visit(identifier):
        if identifier in visiting:
            errors.append(f"dependency cycle includes {identifier}")
            return
        if identifier in visited:
            return
        visiting.add(identifier)
        for dependency in graph.get(identifier, []):
            if dependency in graph:
                visit(dependency)
        visiting.remove(identifier)
        visited.add(identifier)

    for identifier in graph:
        visit(identifier)
    return errors


def load(project):
    jf, _ = paths(project)
    if not os.path.exists(jf):
        raise SystemExit(f"TASKS.json missing: {jf}")

    try:
        with open(jf, encoding="utf-8") as f:
            data = normalize_state(json.load(f))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Cannot read TASKS.json: {exc}") from exc
    errors = validate_state(data)
    if errors:
        raise SystemExit("Invalid TASKS.json: " + "; ".join(errors))
    return data


def save(project, data):
    jf, mf = paths(project)
    data["updated_at"] = now()
    normalize_state(data)
    errors = validate_state(data)
    if errors:
        raise SystemExit("Refusing to write invalid TASKS.json: " + "; ".join(errors))
    write_text_atomic(
        jf,
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
    )
    render(mf, data)


def get_task(data, tid):
    for item in data["tasks"]:
        if item["id"] == tid:
            return item

    raise SystemExit(f"Unknown task: {tid}")


def add_history(data, tid, old, new, note=""):
    data["history"].append({
        "time": now(),
        "task": tid,
        "from": old,
        "to": new,
        "note": note,
    })


def deps_done(data, item):
    for dep in item.get("depends_on", []):
        if get_task(data, dep)["status"] != "DONE":
            return False
    return True

def render(path, data):
    counts = {}

    for item in data["tasks"]:
        status = item["status"]
        counts[status] = counts.get(status, 0) + 1

    lines = [
        "# Tasks",
        "",
        f"- Project: {data.get('project_title', '')}",
        f"- Updated: {data.get('updated_at', '')}",
        "",
        "## Summary",
        "",
    ]

    statuses = [
        "BACKLOG",
        "READY",
        "IN_PROGRESS",
        "BLOCKED",
        "REVIEW",
        "REWORK",
        "DONE",
        "CANCELLED",
    ]

    for status in statuses:
        lines.append(f"- {status}: {counts.get(status, 0)}")

    lines += [
        "",
        "## Tasks",
        "",
        "| ID | Priority | Status | Owner | Domain | Process | Title |",
        "|---|---|---|---|---|---|---|",
    ]

    ordered = sorted(
        data["tasks"],
        key=lambda x: (PRIO.get(x["priority"], 9), x["id"]),
    )

    for item in ordered:
        lines.append(
            f"| {item['id']} | {item['priority']} | "
            f"{item['status']} | {item.get('owner', '')} | "
            f"{item.get('domain', '')} | "
            f"{item.get('process', '')} | {item['title']} |"
        )

    write_text_atomic(path, "\n".join(lines) + "\n")

def cmd_init(args):
    jf, _ = paths(args.project)

    if os.path.exists(jf) and not args.force:
        raise SystemExit(
            "TASKS.json already exists. "
            "Use --force only deliberately."
        )

    data = {
        "schema_version": 1,
        "project_title": args.title,
        "project_slug": args.slug,
        "created_at": now(),
        "updated_at": now(),
        "tasks": [],
        "history": [],
    }

    save(args.project, data)


def cmd_add(args):
    data = load(args.project)

    if any(item["id"] == args.id for item in data["tasks"]):
        raise SystemExit(f"ID already in use: {args.id}")

    item = {
        "id": args.id,
        "title": args.title,
        "workstream": args.workstream or "",
        "domain": args.domain or "",
        "process": args.process or "",
        "owner": args.owner,
        "priority": args.priority,
        "status": "BACKLOG",
        "depends_on": args.depends or [],
        "requirements": args.requirement or [],
        "acceptance_criteria": args.acceptance or [],
        "outputs": args.output or [],
        "evidence": [],
        "blocker": None,
        "created_at": now(),
        "updated_at": now(),
    }

    data["tasks"].append(item)
    save(args.project, data)


def cmd_refresh(args):
    data = load(args.project)

    for item in data["tasks"]:
        if (
            item["status"] in ("BACKLOG", "REWORK")
            and deps_done(data, item)
        ):
            old = item["status"]
            item["status"] = "READY"
            item["updated_at"] = now()
            add_history(
                data,
                item["id"],
                old,
                "READY",
                "Dependencies satisfied",
            )

    save(args.project, data)


def cmd_ready(args):
    data = load(args.project)

    ready = [
        item for item in data["tasks"]
        if item["status"] == "READY"
    ]

    ready.sort(
        key=lambda x: (PRIO.get(x["priority"], 9), x["id"])
    )

    print(json.dumps(ready, indent=2, ensure_ascii=False))

def transition(args, allowed, new_status, note=""):
    data = load(args.project)
    item = get_task(data, args.id)

    if item["status"] not in allowed:
        raise SystemExit(
            f"Forbidden transition: "
            f"{item['status']} -> {new_status}"
        )

    old = item["status"]
    item["status"] = new_status
    item["updated_at"] = now()

    add_history(
        data,
        item["id"],
        old,
        new_status,
        note,
    )

    save(args.project, data)


def cmd_start(args):
    data = load(args.project)
    item = get_task(data, args.id)
    if item["status"] != "READY":
        raise SystemExit(f"Forbidden transition: {item['status']} -> IN_PROGRESS")
    if not deps_done(data, item):
        raise SystemExit("Dependencies not satisfied")
    if not item.get("acceptance_criteria"):
        raise SystemExit("Cannot start task without acceptance criteria")
    in_progress = sum(task["status"] == "IN_PROGRESS" for task in data["tasks"])
    if in_progress >= 3:
        raise SystemExit("WIP limit reached: 3 tasks are already IN_PROGRESS")
    old = item["status"]
    item["status"] = "IN_PROGRESS"
    item["updated_at"] = now()
    add_history(data, item["id"], old, "IN_PROGRESS", "Execution started")
    save(args.project, data)


def cmd_submit(args):
    data = load(args.project)
    item = get_task(data, args.id)

    if item["status"] != "IN_PROGRESS":
        raise SystemExit("submit requires IN_PROGRESS")

    if args.evidence:
        item["evidence"].extend(args.evidence)

    old = item["status"]
    item["status"] = "REVIEW"
    item["updated_at"] = now()

    add_history(
        data,
        item["id"],
        old,
        "REVIEW",
        "Submitted for review",
    )

    save(args.project, data)


def cmd_accept(args):
    data = load(args.project)
    item = get_task(data, args.id)

    if item["status"] != "REVIEW":
        raise SystemExit("accept requires REVIEW")

    if not item.get("evidence") and not args.allow_no_evidence:
        raise SystemExit(
            "No evidence recorded. "
            "Add --evidence during submit."
        )

    old = item["status"]
    item["status"] = "DONE"
    item["updated_at"] = now()
    item["accepted_by"] = args.reviewer
    item["accepted_at"] = now()

    add_history(
        data,
        item["id"],
        old,
        "DONE",
        args.note or "Acceptance passed",
    )

    save(args.project, data)


def cmd_rework(args):
    transition(
        args,
        ["REVIEW", "IN_PROGRESS"],
        "REWORK",
        args.reason,
    )


def cmd_cancel(args):
    transition(
        args,
        ["BACKLOG", "READY"],
        "CANCELLED",
        args.reason,
    )


def cmd_block(args):
    data = load(args.project)
    item = get_task(data, args.id)

    if item["status"] not in (
        "READY",
        "IN_PROGRESS",
        "REWORK",
    ):
        raise SystemExit(
            "block not allowed from this state"
        )

    old = item["status"]
    item["status"] = "BLOCKED"
    item["blocker"] = args.reason
    item["updated_at"] = now()

    add_history(
        data,
        item["id"],
        old,
        "BLOCKED",
        args.reason,
    )

    save(args.project, data)


def cmd_unblock(args):
    data = load(args.project)
    item = get_task(data, args.id)

    if item["status"] != "BLOCKED":
        raise SystemExit("Task is not BLOCKED")

    if not deps_done(data, item):
        raise SystemExit("Dependencies not satisfied")

    old = item["status"]
    item["status"] = "READY"
    item["blocker"] = None
    item["updated_at"] = now()

    add_history(
        data,
        item["id"],
        old,
        "READY",
        args.note or "Blocker resolved",
    )

    save(args.project, data)


def cmd_show(args):
    data = load(args.project)

    print(
        json.dumps(
            get_task(data, args.id),
            indent=2,
            ensure_ascii=False,
        )
    )


def cmd_summary(args):
    data = load(args.project)
    counts = {}

    for item in data["tasks"]:
        status = item["status"]
        counts[status] = counts.get(status, 0) + 1

    result = {
        "project": data.get("project_title"),
        "counts": counts,
        "ready": [
            item["id"] for item in data["tasks"]
            if item["status"] == "READY"
        ],
        "blocked": [
            item["id"] for item in data["tasks"]
            if item["status"] == "BLOCKED"
        ],
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))

parser = argparse.ArgumentParser()
sub = parser.add_subparsers(dest="cmd", required=True)

p = sub.add_parser("init")
p.add_argument("project")
p.add_argument("--title", required=True)
p.add_argument("--slug", required=True)
p.add_argument("--force", action="store_true")
p.set_defaults(fn=cmd_init)

p = sub.add_parser("add")
p.add_argument("project")
p.add_argument("--id", required=True)
p.add_argument("--title", required=True)
p.add_argument("--owner", default="main")
p.add_argument(
    "--priority",
    choices=list(PRIO.keys()),
    default="P2",
)
p.add_argument("--workstream")
p.add_argument("--domain")
p.add_argument("--process")
p.add_argument("--depends", action="append")
p.add_argument("--requirement", action="append")
p.add_argument("--acceptance", action="append")
p.add_argument("--output", action="append")
p.set_defaults(fn=cmd_add)

for name, fn in [
    ("refresh", cmd_refresh),
    ("ready", cmd_ready),
    ("summary", cmd_summary),
]:
    p = sub.add_parser(name)
    p.add_argument("project")
    p.set_defaults(fn=fn)

p = sub.add_parser("start")
p.add_argument("project")
p.add_argument("id")
p.set_defaults(fn=cmd_start)

p = sub.add_parser("submit")
p.add_argument("project")
p.add_argument("id")
p.add_argument("--evidence", action="append")
p.set_defaults(fn=cmd_submit)

p = sub.add_parser("accept")
p.add_argument("project")
p.add_argument("id")
p.add_argument("--reviewer", default="main")
p.add_argument("--note")
p.add_argument("--allow-no-evidence", action="store_true")
p.set_defaults(fn=cmd_accept)

p = sub.add_parser("rework")
p.add_argument("project")
p.add_argument("id")
p.add_argument("--reason", required=True)
p.set_defaults(fn=cmd_rework)

p = sub.add_parser("cancel")
p.add_argument("project")
p.add_argument("id")
p.add_argument("--reason", required=True)
p.set_defaults(fn=cmd_cancel)

p = sub.add_parser("block")
p.add_argument("project")
p.add_argument("id")
p.add_argument("--reason", required=True)
p.set_defaults(fn=cmd_block)

p = sub.add_parser("unblock")
p.add_argument("project")
p.add_argument("id")
p.add_argument("--note")
p.set_defaults(fn=cmd_unblock)

p = sub.add_parser("show")
p.add_argument("project")
p.add_argument("id")
p.set_defaults(fn=cmd_show)

def main(argv=None):
    args = parser.parse_args(argv)
    mutating = {
        "init", "add", "refresh", "start", "submit", "accept", "rework",
        "block", "unblock", "cancel",
    }
    if args.cmd in mutating:
        with task_lock(args.project):
            args.fn(args)
    else:
        args.fn(args)
    return 0


if __name__ == "__main__":
    main()
