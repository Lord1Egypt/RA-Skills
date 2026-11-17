#!/usr/bin/env python3
"""Controlled change-request workflow for Project Manager V1.1."""

import argparse
import fcntl
import json
import re
import sys
from contextlib import contextmanager
from pathlib import Path

from pm_common import (
    VERSIONED_REQ_PATTERN,
    active_requirement_records,
    parse_requirement_record,
    requirement_block_text,
    requirement_definitions,
    utc_timestamp,
    write_json_atomic,
    write_text_atomic,
)

MODEL_VERSION = "1.1"
CR_ID_RE = re.compile(r"^CR-(\d{3,})$")
STATUSES = {
    "DRAFT", "SUBMITTED", "UNDER_ANALYSIS", "ANALYZED",
    "IMPLEMENTING", "IMPLEMENTED", "VERIFIED", "CLOSED",
    "REJECTED", "DEFERRED", "CANCELLED",
}
ANALYSIS_RESULTS = {
    "IMPLEMENT", "REJECT", "DEFER", "MORE_INFORMATION_REQUIRED",
}
TERMINAL_STATUSES = {"CLOSED", "REJECTED", "CANCELLED"}
TRANSITIONS = {
    "DRAFT": {"SUBMITTED", "CANCELLED"},
    "SUBMITTED": {"UNDER_ANALYSIS", "CANCELLED"},
    "UNDER_ANALYSIS": {"ANALYZED", "CANCELLED"},
    "ANALYZED": {"IMPLEMENTING", "REJECTED", "DEFERRED", "UNDER_ANALYSIS", "CANCELLED"},
    "IMPLEMENTING": {"IMPLEMENTED", "CANCELLED"},
    "IMPLEMENTED": {"VERIFIED", "IMPLEMENTING", "CANCELLED"},
    "VERIFIED": {"CLOSED", "IMPLEMENTING", "CANCELLED"},
    "DEFERRED": {"UNDER_ANALYSIS", "CANCELLED"},
    "CLOSED": set(), "REJECTED": set(), "CANCELLED": set(),
}
RESULT_TRANSITION = {
    "IMPLEMENT": "IMPLEMENTING",
    "REJECT": "REJECTED",
    "DEFER": "DEFERRED",
    "MORE_INFORMATION_REQUIRED": "UNDER_ANALYSIS",
}


class ChangeError(RuntimeError):
    pass


def paths(project):
    root = Path(project) / "08-configuration"
    return root, root / "CHANGE-REQUESTS.json", root / "CHANGE-REQUESTS.md"


@contextmanager
def registry_lock(project):
    root, _, _ = paths(project)
    root.mkdir(parents=True, exist_ok=True)
    lock_path = root / ".change-requests.lock"
    with lock_path.open("a+", encoding="utf-8") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        yield
        fcntl.flock(stream, fcntl.LOCK_UN)


def empty_registry():
    return {
        "model": "PROJECT_MANAGER_CHANGE_MANAGEMENT",
        "model_version": MODEL_VERSION,
        "registry_revision": 0,
        "next_number": 1,
        "changes": [],
    }


def load_registry(project, required=True):
    _, path, _ = paths(project)
    if not path.exists():
        if required:
            raise ChangeError("Change management is not initialized")
        return empty_registry()
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ChangeError(f"Cannot read change registry: {exc}") from exc


def save_registry(project, registry, expected_revision):
    current = load_registry(project, required=False)
    if current.get("registry_revision", 0) != expected_revision:
        raise ChangeError("Change registry was modified concurrently; retry the operation")
    registry["registry_revision"] = expected_revision + 1
    _, path, _ = paths(project)
    write_json_atomic(path, registry)
    render_markdown(project, registry)


def get_change(registry, change_id):
    for change in registry.get("changes", []):
        if change.get("Change_ID") == change_id:
            return change
    raise ChangeError(f"Unknown Change Request: {change_id}")


def split_items(values):
    result = []
    for value in values or []:
        result.extend(item.strip() for item in value.split(",") if item.strip())
    return list(dict.fromkeys(result))


def event(change, actor, previous, new, assignee, role, comment=None):
    entry = {
        "timestamp": utc_timestamp(),
        "actor": actor,
        "previous_status": previous,
        "new_status": new,
        "assignee": assignee,
        "role": role,
        "analysis_result": change.get("Analysis_Result"),
    }
    if comment:
        entry["comment"] = comment
    change.setdefault("History", []).append(entry)


def render_change(change):
    lines = [
        f"# {change['Change_ID']} - {change['Title']}", "",
        f"- Status: {change['Status']}",
        f"- Requester: {change['Requester']}",
        f"- Current Assignee: {change['Current_Assignee']}",
        f"- Current Role: {change['Current_Role']}",
        f"- Priority: {change['Priority']}",
        f"- Analysis Result: {change.get('Analysis_Result') or 'NOT_SET'}",
        f"- Implementation Milestone: {change.get('Implementation_Milestone') or 'NOT_SET'}",
        "", "## Reason", "", change["Reason"], "",
        "## Changed Items", "",
    ]
    lines.extend(f"- {item}" for item in change.get("Changed_Items", []))
    if not change.get("Changed_Items"):
        lines.append("- None")
    lines.extend(["", "## Impacted Items", ""])
    impact = change.get("Impacted_Items", {})
    for label, key in (("Direct", "direct"), ("Transitive", "transitive"), ("Manual", "manual")):
        lines.append(f"### {label} Impact")
        lines.append("")
        items = impact.get(key, []) if isinstance(impact, dict) else []
        lines.extend(f"- {item}" for item in items)
        if not items:
            lines.append("- None")
        lines.append("")
    lines.extend(["## Impact Summary", "", change.get("Impact_Summary") or "Not analyzed.", "", "## Description", "", change.get("Text") or "", "", "## Workflow History", "", "| Timestamp | Actor | Previous | New | Assignee | Role | Analysis Result | Comment |", "|---|---|---|---|---|---|---|---|"])
    for item in change.get("History", []):
        cells = [item.get(key) or "" for key in ("timestamp", "actor", "previous_status", "new_status", "assignee", "role", "analysis_result", "comment")]
        lines.append("| " + " | ".join(str(cell).replace("|", "\\|") for cell in cells) + " |")
    return "\n".join(lines) + "\n"


def render_markdown(project, registry=None):
    registry = registry or load_registry(project)
    root, _, index = paths(project)
    change_dir = root / "changes"
    change_dir.mkdir(parents=True, exist_ok=True)
    lines = ["# Change Requests", "", f"Model version: {registry.get('model_version')}", "", "| Change ID | Title | Status | Analysis Result | Current Assignee | Current Role |", "|---|---|---|---|---|---|"]
    for change in registry.get("changes", []):
        lines.append(f"| {change['Change_ID']} | {change['Title']} | {change['Status']} | {change.get('Analysis_Result') or ''} | {change['Current_Assignee']} | {change['Current_Role']} |")
        write_text_atomic(change_dir / f"{change['Change_ID']}.md", render_change(change))
    if not registry.get("changes"):
        lines.append("| - | No Change Requests | - | - | - | - |")
    write_text_atomic(index, "\n".join(lines) + "\n")


def validate_registry(project, registry=None):
    registry = registry or load_registry(project)
    errors = []
    if registry.get("model_version") != MODEL_VERSION:
        errors.append("Unsupported change-management model version")
    changes = registry.get("changes")
    if not isinstance(changes, list):
        return ["changes must be a list"]
    ids = [change.get("Change_ID") for change in changes]
    if len(ids) != len(set(ids)):
        errors.append("Change Request identifiers are not unique")
    definitions = {item["id"]: parse_requirement_record(item) for item in requirement_definitions(project)}
    for change in changes:
        cid = change.get("Change_ID")
        if not isinstance(cid, str) or not CR_ID_RE.fullmatch(cid):
            errors.append(f"Invalid Change Request identifier: {cid}")
            continue
        for field in ("Status", "Title", "Requester", "Current_Assignee", "Current_Role", "Priority", "Reason", "Changed_Items", "Impacted_Items", "History"):
            if field not in change or change[field] in (None, ""):
                errors.append(f"{cid}: required field missing: {field}")
        status = change.get("Status")
        result = change.get("Analysis_Result")
        if status not in STATUSES:
            errors.append(f"{cid}: invalid status: {status}")
        if result is not None and result not in ANALYSIS_RESULTS:
            errors.append(f"{cid}: invalid Analysis_Result: {result}")
        history = change.get("History", [])
        if not isinstance(history, list) or not history:
            errors.append(f"{cid}: workflow history must contain a creation event")
            history = []
        previous_time = ""
        expected = None
        for number, item in enumerate(history, 1):
            for field in ("timestamp", "actor", "previous_status", "new_status", "assignee", "role"):
                if not item.get(field) and not (field == "previous_status" and number == 1):
                    errors.append(f"{cid}: history event {number} missing {field}")
            timestamp = item.get("timestamp", "")
            if timestamp < previous_time:
                errors.append(f"{cid}: event timestamps are not ordered")
            previous_time = timestamp
            if number > 1 and item.get("previous_status") != expected:
                errors.append(f"{cid}: discontinuous workflow history at event {number}")
            new = item.get("new_status")
            old = item.get("previous_status")
            event_result = item.get("analysis_result")
            if event_result is not None and event_result not in ANALYSIS_RESULTS:
                errors.append(f"{cid}: history event {number} has invalid analysis result")
            if number == 1 and (old is not None or new != "DRAFT"):
                errors.append(f"{cid}: first history event must create DRAFT from no status")
            if old and new not in TRANSITIONS.get(old, set()) and not (old == new and item.get("comment", "").startswith(("Assignment", "Analysis result", "Impact analysis", "Requirement revision"))):
                errors.append(f"{cid}: invalid historical transition {old} -> {new}")
            if old == "ANALYZED" and new != "CANCELLED":
                required = RESULT_TRANSITION.get(event_result)
                if new != required:
                    errors.append(f"{cid}: history event {number} is inconsistent with Analysis_Result")
            expected = new
        if history and expected != status:
            errors.append(f"{cid}: current status does not match workflow history")
        if history and (history[-1].get("assignee") != change.get("Current_Assignee") or history[-1].get("role") != change.get("Current_Role")):
            errors.append(f"{cid}: current assignment does not match latest history")
        if status in {"IMPLEMENTING", "IMPLEMENTED", "VERIFIED", "CLOSED"} and result != "IMPLEMENT":
            errors.append(f"{cid}: {status} requires Analysis_Result IMPLEMENT")
        if status == "REJECTED" and result != "REJECT":
            errors.append(f"{cid}: REJECTED requires Analysis_Result REJECT")
        if status == "DEFERRED" and result != "DEFER":
            errors.append(f"{cid}: DEFERRED requires Analysis_Result DEFER")
        changed_items = change.get("Changed_Items", [])
        if not isinstance(changed_items, list) or any(not isinstance(item, str) or not item.strip() for item in changed_items):
            errors.append(f"{cid}: Changed_Items must contain non-empty configuration references")
            changed_items = []
        if len(changed_items) != len(set(changed_items)):
            errors.append(f"{cid}: Changed_Items contains duplicates")
        for ref in changed_items:
            if re.fullmatch(VERSIONED_REQ_PATTERN, ref) and ref not in definitions:
                errors.append(f"{cid}: Changed_Items requirement does not exist: {ref}")
        impact = change.get("Impacted_Items", {})
        if not isinstance(impact, dict) or any(not isinstance(impact.get(key), list) for key in ("direct", "transitive", "manual")):
            errors.append(f"{cid}: Impacted_Items must contain direct, transitive, and manual lists")
            impact = {"direct": [], "transitive": [], "manual": []}
        flattened = impact.get("direct", []) + impact.get("transitive", []) + impact.get("manual", [])
        if len(flattened) != len(set(flattened)):
            errors.append(f"{cid}: Impacted_Items contains duplicate classifications")
        for ref in impact.get("direct", []) + impact.get("transitive", []):
            if re.fullmatch(VERSIONED_REQ_PATTERN, ref) and ref not in definitions:
                errors.append(f"{cid}: impacted requirement does not exist: {ref}")
    max_used = max((int(match.group(1)) for cid in ids if isinstance(cid, str) and (match := CR_ID_RE.fullmatch(cid))), default=0)
    if registry.get("next_number", 0) <= max_used:
        errors.append("next_number would reuse a Change Request identifier")
    return errors


def analyze_impact(project, change, manual_items=None):
    active = active_requirement_records(project)
    changed = set(change.get("Changed_Items", []))
    direct = set()
    transitive = set()
    frontier = set(changed)
    depth = 0
    while frontier:
        found = set()
        for record in active:
            upstream = record.get("upstream")
            if isinstance(upstream, list) and set(upstream) & frontier:
                found.add(record["id"])
        found -= direct | transitive | changed
        if depth == 0:
            direct |= found
        else:
            transitive |= found
        frontier = found
        depth += 1
    if manual_items is None:
        manual_items = change.get("Impacted_Items", {}).get("manual", [])
    manual = sorted(
        set(manual_items) - changed - direct - transitive
    )
    return {"direct": sorted(direct), "transitive": sorted(transitive), "manual": manual}


def transition(change, new_status, actor, assignee, role, comment=None):
    old = change["Status"]
    if new_status not in TRANSITIONS.get(old, set()):
        raise ChangeError(f"Invalid Change Request transition: {old} -> {new_status}")
    if old == "ANALYZED":
        expected = RESULT_TRANSITION.get(change.get("Analysis_Result"))
        if new_status != expected and new_status != "CANCELLED":
            raise ChangeError(f"Analysis_Result {change.get('Analysis_Result') or 'NOT_SET'} requires transition to {expected or 'no status'}")
    change["Status"] = new_status
    change["Current_Assignee"] = assignee
    change["Current_Role"] = role
    event(change, actor, old, new_status, assignee, role, comment)


def create_revision(project, change, requirement_id, actor):
    if change.get("Status") not in {"ANALYZED", "IMPLEMENTING"} or change.get("Analysis_Result") != "IMPLEMENT":
        raise ChangeError("Requirement revisions require an ANALYZED or IMPLEMENTING Change Request with Analysis_Result IMPLEMENT")
    definitions = requirement_definitions(project)
    source_item = next((item for item in definitions if item["id"] == requirement_id), None)
    if source_item is None or source_item.get("scheme") != "V1.1":
        raise ChangeError(f"Requirement revision does not exist: {requirement_id}")
    source = parse_requirement_record(source_item)
    if (source.get("status") or "").upper() != "RELEASED":
        raise ChangeError(
            "A new revision may only be created from a RELEASED requirement; "
            "edit DRAFT requirements in place"
        )
    latest = max((item["revision_number"] for item in definitions if item.get("base_id") == source["base_id"]), default=0)
    if source["revision_number"] != latest:
        raise ChangeError("A new revision can only be created from the latest revision")
    new_id = f"{source['base_id']}@R{latest + 1}"
    block = requirement_block_text(source_item)
    lines = block.splitlines()
    lines[0] = f"[{new_id}]"
    changed = False
    for index, line in enumerate(lines):
        if re.match(r"^Status\s*:", line, re.IGNORECASE):
            lines[index] = "Status: DRAFT"
        elif re.match(r"^Change_ID\s*:", line, re.IGNORECASE):
            lines[index] = f"Change_ID: {change['Change_ID']}"
            changed = True
        elif re.match(r"^Text\s*:\s*$", line, re.IGNORECASE) and not changed:
            lines.insert(index, f"Change_ID: {change['Change_ID']}")
            changed = True
            break
    if not changed:
        raise ChangeError("Requirement block has no Text marker")
    path = source_item["path"]
    original = path.read_text(encoding="utf-8")
    separator = "" if original.endswith("\n\n") else ("\n" if original.endswith("\n") else "\n\n")
    write_text_atomic(path, original + separator + "\n".join(lines) + "\n")
    if requirement_id not in change["Changed_Items"]:
        change["Changed_Items"].append(requirement_id)
    event(change, actor, change["Status"], change["Status"], change["Current_Assignee"], change["Current_Role"], f"Requirement revision created: {new_id}")
    return new_id


def add_common_assignment(parser):
    parser.add_argument("--assignee", required=True)
    parser.add_argument("--role", required=True)
    parser.add_argument("--actor", required=True)


def build_parser():
    parser = argparse.ArgumentParser(description="Manage controlled Project Manager V1.1 Change Requests")
    parser.add_argument("--project", default=".")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("init", help="Initialize or migrate change management")
    create = commands.add_parser("create", help="Create the next non-reusable Change Request identifier")
    for name in ("title", "requester", "priority", "reason", "assignee", "role", "actor"):
        create.add_argument(f"--{name}", required=True)
    create.add_argument("--changed-item", action="append", default=[])
    create.add_argument("--text", default="")
    create.add_argument("--milestone")
    commands.add_parser("list", help="List Change Requests")
    show = commands.add_parser("show", help="Show a Change Request")
    show.add_argument("change_id")
    assign = commands.add_parser("assign", help="Change the current assignee and role")
    assign.add_argument("change_id"); add_common_assignment(assign); assign.add_argument("--comment")
    move = commands.add_parser("transition", help="Perform a validated workflow transition")
    move.add_argument("change_id"); move.add_argument("status", choices=sorted(STATUSES)); add_common_assignment(move); move.add_argument("--comment")
    start = commands.add_parser("start-analysis", help="Transition SUBMITTED or DEFERRED to UNDER_ANALYSIS")
    start.add_argument("change_id"); add_common_assignment(start); start.add_argument("--comment")
    result = commands.add_parser("set-result", help="Set the independent analysis result while UNDER_ANALYSIS or ANALYZED")
    result.add_argument("change_id"); result.add_argument("result", choices=sorted(ANALYSIS_RESULTS)); result.add_argument("--actor", required=True); result.add_argument("--summary", required=True)
    impact = commands.add_parser("impact", help="Recursively analyze downstream requirement impact")
    impact.add_argument("change_id"); impact.add_argument("--actor", required=True); impact.add_argument("--summary")
    impact.add_argument("--manual-impact", action="append", default=[])
    impact.add_argument("--clear-manual-impact", action="store_true")
    revision = commands.add_parser("revise-requirement", help="Create the next DRAFT requirement revision under a Change Request")
    revision.add_argument("change_id"); revision.add_argument("requirement_id"); revision.add_argument("--actor", required=True)
    commands.add_parser("validate", help="Validate the authoritative registry and workflow history")
    commands.add_parser("render", help="Regenerate human-readable Markdown views")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    project = Path(args.project).resolve()
    try:
        if args.command == "init":
            with registry_lock(project):
                registry = load_registry(project, required=False)
                root, path, _ = paths(project)
                (root / "changes").mkdir(parents=True, exist_ok=True)
                if not path.exists():
                    write_json_atomic(path, registry)
                render_markdown(project, registry)
            print("Change management initialized")
            return 0
        if args.command in {"list", "show", "validate", "render"}:
            registry = load_registry(project)
            if args.command == "list":
                for change in registry["changes"]:
                    print(f"{change['Change_ID']}\t{change['Status']}\t{change['Title']}\t{change['Current_Assignee']}\t{change['Current_Role']}")
            elif args.command == "show":
                print(render_change(get_change(registry, args.change_id)), end="")
            elif args.command == "render":
                render_markdown(project, registry); print("Change Request Markdown views regenerated")
            else:
                errors = validate_registry(project, registry)
                for error in errors: print(f"ERROR: {error}")
                print(f"CHANGE VALIDATION: {'FAIL' if errors else 'PASS'}")
                return 1 if errors else 0
            return 0
        with registry_lock(project):
            registry = load_registry(project)
            revision = registry["registry_revision"]
            if args.command == "create":
                number = registry["next_number"]
                cid = f"CR-{number:03d}"
                registry["next_number"] = number + 1
                now = utc_timestamp()
                change = {"Change_ID": cid, "Status": "DRAFT", "Title": args.title, "Requester": args.requester, "Current_Assignee": args.assignee, "Current_Role": args.role, "Priority": args.priority, "Reason": args.reason, "Analysis_Result": None, "Implementation_Milestone": args.milestone, "Changed_Items": split_items(args.changed_item), "Impacted_Items": {"direct": [], "transitive": [], "manual": []}, "Impact_Summary": "", "Text": args.text, "Created_At": now, "History": []}
                event(change, args.actor, None, "DRAFT", args.assignee, args.role, "Change Request created")
                registry["changes"].append(change)
                print(cid)
            else:
                change = get_change(registry, args.change_id)
                if args.command == "assign":
                    old = change["Status"]; change["Current_Assignee"] = args.assignee; change["Current_Role"] = args.role
                    event(change, args.actor, old, old, args.assignee, args.role, f"Assignment changed{': ' + args.comment if args.comment else ''}")
                elif args.command in {"transition", "start-analysis"}:
                    status = args.status if args.command == "transition" else "UNDER_ANALYSIS"
                    transition(change, status, args.actor, args.assignee, args.role, args.comment)
                elif args.command == "set-result":
                    if change["Status"] not in {"UNDER_ANALYSIS", "ANALYZED"}:
                        raise ChangeError("Analysis_Result may only be set during or after analysis")
                    change["Analysis_Result"] = args.result
                    change["Impact_Summary"] = args.summary
                    event(change, args.actor, change["Status"], change["Status"], change["Current_Assignee"], change["Current_Role"], f"Analysis result set: {args.result}")
                elif args.command == "impact":
                    existing_manual = [] if args.clear_manual_impact else change.get("Impacted_Items", {}).get("manual", [])
                    manual = split_items([*existing_manual, *args.manual_impact])
                    change["Impacted_Items"] = analyze_impact(project, change, manual)
                    if args.summary: change["Impact_Summary"] = args.summary
                    event(change, args.actor, change["Status"], change["Status"], change["Current_Assignee"], change["Current_Role"], "Impact analysis updated")
                elif args.command == "revise-requirement":
                    new_id = create_revision(project, change, args.requirement_id, args.actor)
                    print(new_id)
            save_registry(project, registry, revision)
        return 0
    except ChangeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
