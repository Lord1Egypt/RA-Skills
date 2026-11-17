#!/usr/bin/env python3
"""Configuration baseline lifecycle for Project Manager V1.1."""

import argparse
import fcntl
import json
import re
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path

from pm_common import (
    active_requirement_records,
    canonical_sha256,
    git_capture,
    parse_requirement_id,
    parse_requirement_record,
    read_text,
    requirement_definitions,
    utc_timestamp,
    write_json_atomic,
    write_text_atomic,
)

MODEL_VERSION = "1.1"
BASELINE_ID_RE = re.compile(r"^BL-(\d{3,})$")
STATUSES = {"DRAFT", "FROZEN", "RELEASED", "SUPERSEDED", "CANCELLED"}
TRANSITIONS = {
    "DRAFT": {"FROZEN", "CANCELLED"},
    "FROZEN": {"RELEASED"},
    "RELEASED": {"SUPERSEDED"},
    "SUPERSEDED": set(), "CANCELLED": set(),
}
BLOCKING_CR_STATUSES = {"SUBMITTED", "UNDER_ANALYSIS", "IMPLEMENTING", "IMPLEMENTED"}


class BaselineError(RuntimeError):
    pass


def locations(project):
    root = Path(project) / "08-configuration"
    return root, root / "CONFIGURATION-MANAGEMENT.json", root / "BASELINE-REGISTRY.json", root / "BASELINES.md", root / "baselines"


@contextmanager
def baseline_lock(project):
    root, _, _, _, _ = locations(project)
    root.mkdir(parents=True, exist_ok=True)
    with (root / ".baselines.lock").open("a+", encoding="utf-8") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        yield
        fcntl.flock(stream, fcntl.LOCK_UN)


def empty_registry():
    return {"model": "PROJECT_MANAGER_BASELINE_MANAGEMENT", "model_version": MODEL_VERSION, "registry_revision": 0, "next_number": 1, "baselines": []}


def load_registry(project, required=True):
    _, _, path, _, _ = locations(project)
    if not path.exists():
        if required: raise BaselineError("Baseline management is not initialized")
        return empty_registry()
    try: return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc: raise BaselineError(f"Cannot read baseline registry: {exc}") from exc


def record_path(project, baseline_id):
    return locations(project)[4] / f"{baseline_id}.json"


def load_baseline(project, baseline_id):
    path = record_path(project, baseline_id)
    if not path.exists(): raise BaselineError(f"Unknown baseline: {baseline_id}")
    try: return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc: raise BaselineError(f"Cannot read {baseline_id}: {exc}") from exc


def configuration_items(project):
    path = Path(project) / "08-configuration" / "CONFIGURATION-ITEMS.md"
    if not path.exists(): return []
    result = []
    for line in read_text(path).splitlines():
        if not line.strip().startswith("|"): continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or not re.fullmatch(r"CI-\d+", cells[0]): continue
        result.append({"id": cells[0], "item": cells[1] if len(cells) > 1 else "", "version": cells[2] if len(cells) > 2 else "", "location": cells[3] if len(cells) > 3 else ""})
    return result


def make_snapshot(project):
    head = git_capture(project, "rev-parse", "HEAD")
    if not head: raise BaselineError("Project is not in a readable Git repository")
    requirements = [{"id": record["id"], "status": record.get("status")} for record in active_requirement_records(project)]
    return {"Git_Commit": head, "Requirements_Snapshot": requirements, "Configuration_Items": configuration_items(project)}


def immutable_payload(baseline):
    return {key: baseline.get(key) for key in ("Baseline_ID", "Purpose", "Created_At", "Created_By", "Git_Commit", "Requirements_Snapshot", "Configuration_Items", "Related_Change_Requests", "Open_Deviations", "Open_Problems_Accepted")}


def blocking_changes(project, baseline):
    path = Path(project) / "08-configuration" / "CHANGE-REQUESTS.json"
    if not path.exists(): return [], []
    data = json.loads(path.read_text(encoding="utf-8"))
    def stable_identity(identifier):
        identity = parse_requirement_id(identifier) if isinstance(identifier, str) else None
        return identity["base_id"] if identity else identifier

    # A controlled change usually names R1 while its new baseline contains R2.
    # Gate the stable item across revisions without changing exact traceability
    # or the immutable snapshot. Non-requirement CI IDs retain exact matching.
    content = {stable_identity(item["id"]) for item in baseline.get("Requirements_Snapshot", [])} | {item.get("id") for item in baseline.get("Configuration_Items", [])}
    blocking, deferred = [], []
    for change in data.get("changes", []):
        affected = set(change.get("Changed_Items", []))
        impact = change.get("Impacted_Items", {})
        affected.update(impact.get("direct", [])); affected.update(impact.get("transitive", [])); affected.update(impact.get("manual", []))
        if not {stable_identity(item) for item in affected} & content: continue
        status = change.get("Status")
        if status in BLOCKING_CR_STATUSES or (status == "ANALYZED" and change.get("Analysis_Result") == "IMPLEMENT"):
            blocking.append(change["Change_ID"])
        elif status == "DEFERRED": deferred.append(change["Change_ID"])
    return sorted(blocking), sorted(deferred)


def validate_baseline(project, baseline):
    errors, warnings = [], []
    bid = baseline.get("Baseline_ID")
    if not isinstance(bid, str) or not BASELINE_ID_RE.fullmatch(bid): errors.append(f"Invalid baseline identifier: {bid}")
    if baseline.get("Status") not in STATUSES: errors.append(f"{bid}: invalid status: {baseline.get('Status')}")
    for field in ("Purpose", "Created_At", "Created_By", "Git_Commit", "Requirements_Snapshot", "Configuration_Items", "Related_Change_Requests", "Open_Deviations", "Open_Problems_Accepted", "History"):
        if field not in baseline: errors.append(f"{bid}: required field missing: {field}")
    commit = baseline.get("Git_Commit")
    if commit and git_capture(project, "cat-file", "-e", f"{commit}^{{commit}}") is None: errors.append(f"{bid}: Git commit does not exist: {commit}")
    active = {record["id"]: record for record in active_requirement_records(project)}
    historical = {
        item["id"]: parse_requirement_record(item)
        for item in requirement_definitions(project)
        if item.get("scheme") == "V1.1"
    }
    seen = set()
    for item in baseline.get("Requirements_Snapshot", []):
        rid = item.get("id") if isinstance(item, dict) else None
        if rid in seen: errors.append(f"{bid}: duplicate requirement snapshot entry: {rid}")
        seen.add(rid)
        if baseline.get("Status") == "DRAFT":
            if rid not in active:
                errors.append(f"{bid}: stale, cancelled, or missing active requirement: {rid}")
            elif item.get("status") != active[rid].get("status"):
                errors.append(f"{bid}: DRAFT requirement status is stale: {rid}")
        else:
            # Historical baselines intentionally retain exact superseded
            # revisions. Their payload and Git commit are the authority; a
            # newer active revision must not invalidate the old baseline.
            if rid not in historical:
                errors.append(f"{bid}: historical requirement is missing: {rid}")
            if item.get("status") != "RELEASED":
                errors.append(f"{bid}: frozen requirement was not RELEASED: {rid}")
    if baseline.get("Status") in {"FROZEN", "RELEASED", "SUPERSEDED"}:
        expected = canonical_sha256(immutable_payload(baseline))
        if baseline.get("Snapshot_Integrity_SHA256") != expected: errors.append(f"{bid}: immutable snapshot integrity hash mismatch")
    blocking, deferred = blocking_changes(project, baseline)
    if blocking: errors.append(f"{bid}: blocking Change Requests affect baseline content: {', '.join(blocking)}")
    if deferred: warnings.append(f"{bid}: deferred Change Requests affect baseline content: {', '.join(deferred)}")
    return errors, warnings


def render_baseline(baseline):
    lines = [f"# {baseline['Baseline_ID']} - Configuration Baseline", "", f"- Status: {baseline['Status']}", f"- Purpose: {baseline['Purpose']}", f"- Created At: {baseline['Created_At']}", f"- Created By: {baseline['Created_By']}", f"- Git Commit: {baseline['Git_Commit']}", f"- Snapshot Integrity SHA-256: {baseline.get('Snapshot_Integrity_SHA256') or 'NOT_FROZEN'}", "", "## Requirements Snapshot", ""]
    lines.extend(f"- {item['id']} ({item.get('status')})" for item in baseline.get("Requirements_Snapshot", []))
    if not baseline.get("Requirements_Snapshot"): lines.append("- None")
    lines.extend(["", "## Configuration Items", ""])
    lines.extend(f"- {item.get('id')}: {item.get('item')} | {item.get('version')} | {item.get('location')}" for item in baseline.get("Configuration_Items", []))
    if not baseline.get("Configuration_Items"): lines.append("- None")
    for title, key in (("Related Change Requests", "Related_Change_Requests"), ("Open Deviations", "Open_Deviations"), ("Open Problems Accepted", "Open_Problems_Accepted")):
        lines.extend(["", f"## {title}", ""]); values = baseline.get(key, []); lines.extend(f"- {value}" for value in values); lines.extend([] if values else ["- None"])
    lines.extend(["", "## Lifecycle History", "", "| Timestamp | Actor | Previous | New | Comment |", "|---|---|---|---|---|"])
    for item in baseline.get("History", []):
        comment = str(item.get("comment") or "").replace("|", "\\|")
        lines.append(f"| {item.get('timestamp', '')} | {item.get('actor', '')} | {item.get('previous_status') or ''} | {item.get('new_status', '')} | {comment} |")
    return "\n".join(lines) + "\n"


def render_all(project, registry=None):
    registry = registry or load_registry(project)
    _, _, _, index, directory = locations(project); directory.mkdir(parents=True, exist_ok=True)
    lines = ["# Baselines", "", f"Model version: {registry.get('model_version')}", "", "| Baseline ID | Status | Purpose | Git Commit | Integrity Hash |", "|---|---|---|---|---|"]
    for bid in registry.get("baselines", []):
        baseline = load_baseline(project, bid); lines.append(f"| {bid} | {baseline['Status']} | {baseline['Purpose']} | {baseline['Git_Commit']} | {baseline.get('Snapshot_Integrity_SHA256') or ''} |"); write_text_atomic(directory / f"{bid}.md", render_baseline(baseline))
    if not registry.get("baselines"): lines.append("| - | No baselines | - | - | - |")
    write_text_atomic(index, "\n".join(lines) + "\n")


def save(project, registry, baseline, expected_revision):
    current = load_registry(project)
    if current.get("registry_revision") != expected_revision: raise BaselineError("Baseline registry was modified concurrently; retry the operation")
    registry["registry_revision"] = expected_revision + 1
    write_json_atomic(record_path(project, baseline["Baseline_ID"]), baseline)
    write_json_atomic(locations(project)[2], registry)
    render_all(project, registry)


def event(baseline, actor, previous, new, comment=None):
    baseline.setdefault("History", []).append({"timestamp": utc_timestamp(), "actor": actor, "previous_status": previous, "new_status": new, "comment": comment})


def select_current_baseline(project, baseline_id):
    """Select a release candidate without rewriting unrelated STATUS content."""

    path = Path(project) / "00-project" / "STATUS.md"
    if not path.exists():
        raise BaselineError("Cannot select baseline: 00-project/STATUS.md is missing")
    text = read_text(path)
    pattern = re.compile(r"^- Current Baseline:[ \t]*.*$", re.MULTILINE)
    replacement = f"- Current Baseline: {baseline_id}"
    if pattern.search(text):
        updated = pattern.sub(replacement, text, count=1)
    else:
        updated = text.rstrip() + "\n\n" + replacement + "\n"
    write_text_atomic(path, updated)


def run_release_gate(project, baseline_id):
    release_check = Path(__file__).resolve().parent / "release_check.py"
    result = subprocess.run(
        [sys.executable, str(release_check), str(project), "--baseline", baseline_id],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.stdout:
        print(result.stdout, end="")
    if result.returncode != 0:
        raise BaselineError(f"Release gate failed for {baseline_id}")


def build_parser():
    parser = argparse.ArgumentParser(description="Manage immutable Project Manager V1.1 configuration baselines")
    parser.add_argument("--project", default="."); commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="Initialize or migrate baseline management"); init.add_argument("--actor", required=True)
    create = commands.add_parser("create", help="Create a DRAFT baseline from current active revisions"); create.add_argument("--purpose", required=True); create.add_argument("--actor", required=True); create.add_argument("--related-cr", action="append", default=[]); create.add_argument("--deviation", action="append", default=[]); create.add_argument("--accepted-problem", action="append", default=[])
    commands.add_parser("list", help="List baselines")
    for command, help_text in (("show", "Show a baseline"), ("validate", "Validate a baseline"), ("refresh", "Refresh a DRAFT snapshot"), ("freeze", "Freeze an immutable release-candidate snapshot"), ("release", "Transition FROZEN to RELEASED"), ("cancel", "Cancel a DRAFT baseline")):
        sub = commands.add_parser(command, help=help_text); sub.add_argument("baseline_id");
        if command in {"refresh", "freeze", "release", "cancel"}: sub.add_argument("--actor", required=True); sub.add_argument("--comment")
    supersede = commands.add_parser("supersede", help="Supersede a RELEASED baseline with another baseline"); supersede.add_argument("baseline_id"); supersede.add_argument("--by", required=True); supersede.add_argument("--actor", required=True); supersede.add_argument("--comment")
    commands.add_parser("render", help="Regenerate Markdown views")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv); project = Path(args.project).resolve()
    try:
        if args.command == "init":
            with baseline_lock(project):
                root, marker, registry_path, _, directory = locations(project); directory.mkdir(parents=True, exist_ok=True)
                if not registry_path.exists(): write_json_atomic(registry_path, empty_registry())
                write_json_atomic(marker, {"model": "PROJECT_MANAGER_CONFIGURATION_MANAGEMENT", "model_version": MODEL_VERSION, "enabled": True, "enabled_at": utc_timestamp(), "enabled_by": args.actor})
                render_all(project)
            print("Baseline management initialized"); return 0
        if args.command in {"list", "show", "validate", "render"}:
            registry = load_registry(project)
            if args.command == "list":
                for bid in registry["baselines"]:
                    baseline = load_baseline(project, bid); print(f"{bid}\t{baseline['Status']}\t{baseline['Purpose']}\t{baseline['Git_Commit']}")
            elif args.command == "show": print(render_baseline(load_baseline(project, args.baseline_id)), end="")
            elif args.command == "render": render_all(project, registry); print("Baseline Markdown views regenerated")
            else:
                errors, warnings = validate_baseline(project, load_baseline(project, args.baseline_id)); [print(f"WARN: {item}") for item in warnings]; [print(f"ERROR: {item}") for item in errors]; print(f"BASELINE VALIDATION: {'FAIL' if errors else 'PASS'}"); return 1 if errors else 0
            return 0
        with baseline_lock(project):
            registry = load_registry(project); revision = registry["registry_revision"]
            select_after_save = None
            if args.command == "create":
                number = registry["next_number"]; bid = f"BL-{number:03d}"; registry["next_number"] = number + 1; snapshot = make_snapshot(project)
                baseline = {"Baseline_ID": bid, "Status": "DRAFT", "Purpose": args.purpose, "Created_At": utc_timestamp(), "Created_By": args.actor, **snapshot, "Related_Change_Requests": list(dict.fromkeys(args.related_cr)), "Open_Deviations": args.deviation, "Open_Problems_Accepted": args.accepted_problem, "Snapshot_Integrity_SHA256": None, "Superseded_By": None, "History": []}
                event(baseline, args.actor, None, "DRAFT", "Baseline created"); registry["baselines"].append(bid); print(bid)
            else:
                baseline = load_baseline(project, args.baseline_id); old = baseline["Status"]
                if args.command == "refresh":
                    if old != "DRAFT": raise BaselineError("Only a DRAFT baseline may be refreshed")
                    baseline.update(make_snapshot(project)); event(baseline, args.actor, old, old, "DRAFT snapshot refreshed")
                elif args.command == "freeze":
                    if old != "DRAFT": raise BaselineError(f"Invalid baseline transition: {old} -> FROZEN")
                    dirty = git_capture(project, "status", "--porcelain")
                    if dirty: raise BaselineError("Cannot freeze baseline with a dirty Git worktree")
                    # Bind the immutable candidate to the exact clean commit
                    # being frozen, not the earlier commit at DRAFT creation.
                    baseline.update(make_snapshot(project))
                    errors, warnings = validate_baseline(project, baseline)
                    if errors: raise BaselineError("Cannot freeze invalid baseline: " + "; ".join(errors))
                    unreleased = [
                        item.get("id", "<unknown>")
                        for item in baseline.get("Requirements_Snapshot", [])
                        if item.get("status") != "RELEASED"
                    ]
                    if unreleased:
                        raise BaselineError(
                            "Cannot freeze baseline with non-RELEASED requirements: "
                            + ", ".join(unreleased)
                        )
                    if warnings and not baseline.get("Open_Deviations"): raise BaselineError("Deferred Change Requests require an accepted deviation")
                    baseline["Status"] = "FROZEN"; baseline["Snapshot_Integrity_SHA256"] = canonical_sha256(immutable_payload(baseline)); event(baseline, args.actor, old, "FROZEN", args.comment)
                    select_after_save = baseline["Baseline_ID"]
                elif args.command == "release":
                    if old != "FROZEN": raise BaselineError(f"Invalid baseline transition: {old} -> RELEASED")
                    errors, _ = validate_baseline(project, baseline)
                    if errors: raise BaselineError("Cannot release invalid baseline: " + "; ".join(errors))
                    run_release_gate(project, baseline["Baseline_ID"])
                    gate_commit = git_capture(project, "rev-parse", "HEAD")
                    comment = args.comment or f"Release gate passed at {gate_commit}"
                    baseline["Status"] = "RELEASED"; event(baseline, args.actor, old, "RELEASED", comment)
                elif args.command == "cancel":
                    if old != "DRAFT": raise BaselineError("Only a DRAFT baseline may be cancelled")
                    baseline["Status"] = "CANCELLED"; event(baseline, args.actor, old, "CANCELLED", args.comment)
                elif args.command == "supersede":
                    if old != "RELEASED": raise BaselineError("Only a RELEASED baseline may be superseded")
                    if args.by == baseline["Baseline_ID"]: raise BaselineError("A baseline cannot supersede itself")
                    replacement = load_baseline(project, args.by)
                    if replacement["Status"] not in {"FROZEN", "RELEASED"}: raise BaselineError("Replacement baseline must be FROZEN or RELEASED")
                    baseline["Status"] = "SUPERSEDED"; baseline["Superseded_By"] = args.by; event(baseline, args.actor, old, "SUPERSEDED", args.comment)
            save(project, registry, baseline, revision)
            if select_after_save:
                select_current_baseline(project, select_after_save)
        return 0
    except (BaselineError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr); return 2


if __name__ == "__main__": sys.exit(main())
