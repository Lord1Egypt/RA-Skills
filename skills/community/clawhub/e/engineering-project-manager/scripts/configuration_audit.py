#!/usr/bin/env python3
"""Audit controlled changes and immutable configuration baselines."""

import argparse
import json
import re
import sys
from pathlib import Path

from baseline_manager import (
    BASELINE_ID_RE,
    TRANSITIONS as BASELINE_TRANSITIONS,
    load_baseline,
    load_registry as load_baseline_registry,
    validate_baseline,
)
from change_manager import (
    analyze_impact,
    load_registry as load_change_registry,
    validate_registry,
)
from pm_common import (
    active_requirement_records,
    git_capture,
    parse_requirement_record,
    read_text,
    requirement_definitions,
)


def current_baseline(project):
    path = Path(project) / "00-project" / "STATUS.md"
    if not path.exists(): return None
    # Horizontal whitespace only: ``\s`` also consumes newlines and could
    # incorrectly treat the following STATUS field as the selected baseline.
    match = re.search(
        r"^- Current Baseline:[ \t]*(.*?)[ \t]*$",
        read_text(path),
        re.MULTILINE,
    )
    if not match: return None
    value = match.group(1).strip()
    return None if not value or value.upper() in {"NONE", "NOT_SET", "N/A"} else value


def release_candidate_delta(project, baseline):
    """Return non-metadata paths changed after the candidate content commit."""

    commit = baseline.get("Git_Commit")
    head = git_capture(project, "rev-parse", "HEAD")
    if not commit or not head:
        return ["Git candidate commit or HEAD is unavailable"]
    if git_capture(project, "merge-base", "--is-ancestor", commit, head) is None:
        return [f"candidate commit {commit} is not an ancestor of HEAD"]
    changed = git_capture(project, "diff", "--name-only", f"{commit}..{head}")
    if changed is None:
        return [f"cannot compare candidate commit {commit} with HEAD"]
    allowed = {
        "00-project/STATUS.md",
        "08-configuration/BASELINE-REGISTRY.json",
        "08-configuration/BASELINES.md",
        "05-verification/EVIDENCE-MANAGEMENT.json",
        "05-verification/EVIDENCE.json",
        "05-verification/EVIDENCE.md",
    }

    def controlled_metadata(path):
        return path in allowed or bool(
            re.fullmatch(
                r"08-configuration/baselines/BL-\d+\.(?:json|md)", path
            )
            or re.fullmatch(
                r"05-verification/evidence/EV-\d+\.md", path
            )
        )

    return sorted(
        path for path in changed.splitlines()
        if path and not controlled_metadata(path)
    )


def audit(project, strict=False, release_candidate=None):
    project = Path(project)
    marker = project / "08-configuration" / "CONFIGURATION-MANAGEMENT.json"
    if not marker.exists():
        configuration = marker.parent
        previously_enabled = git_capture(
            project, "log", "-1", "--format=%H", "--",
            marker.relative_to(project).as_posix(),
        )
        if ((configuration / "CHANGE-REQUESTS.json").exists()
                or (configuration / "BASELINE-REGISTRY.json").exists()
                or any((configuration / "baselines").glob("BL-*.json"))
                or previously_enabled):
            return [
                "Configuration-management enablement marker is missing from an enabled project; "
                "restore it before auditing or releasing"
            ], []
        return [], [] if strict else ["Configuration Management V1.1 is not enabled; legacy project skipped"]
    errors, warnings = [], []
    try:
        model = json.loads(marker.read_text(encoding="utf-8"))
        if model.get("enabled") is not True or model.get("model_version") != "1.1": errors.append("Invalid Configuration Management V1.1 enablement marker")
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Cannot read configuration-management marker: {exc}"], []
    try:
        changes = load_change_registry(project)
        errors.extend(validate_registry(project, changes))
    except Exception as exc:
        changes = {"changes": []}; errors.append(f"Change registry audit failed: {exc}")
    change_by_id = {item.get("Change_ID"): item for item in changes.get("changes", [])}
    definitions = [parse_requirement_record(item) for item in requirement_definitions(project) if item.get("scheme") == "V1.1"]
    for requirement in definitions:
        if requirement["revision_number"] < 2: continue
        cid = requirement.get("change_id")
        if not cid or cid not in change_by_id:
            errors.append(f"{requirement['id']}: controlled revision references missing Change Request: {cid or 'NOT_SET'}")
            continue
        change = change_by_id[cid]
        previous = f"{requirement['base_id']}@R{requirement['revision_number'] - 1}"
        if previous not in change.get("Changed_Items", []) and requirement["id"] not in change.get("Changed_Items", []): errors.append(f"{requirement['id']}: Change Request {cid} does not identify the revised requirement")
    for change in changes.get("changes", []):
        expected = analyze_impact(project, change)
        stored = change.get("Impacted_Items", {})
        for key in ("direct", "transitive"):
            if sorted(stored.get(key, [])) != expected[key]: errors.append(f"{change['Change_ID']}: stored {key} impact is inconsistent with active requirement graph")
    try:
        registry = load_baseline_registry(project)
        if registry.get("model") != "PROJECT_MANAGER_BASELINE_MANAGEMENT" or registry.get("model_version") != "1.1":
            errors.append("Invalid baseline-management registry model or version")
        ids = registry.get("baselines", [])
        if not isinstance(ids, list):
            raise ValueError("baseline registry baselines must be a list")
        if len(ids) != len(set(ids)): errors.append("Baseline identifiers are not unique")
        max_used = max((int(match.group(1)) for bid in ids if (match := BASELINE_ID_RE.fullmatch(bid))), default=0)
        if registry.get("next_number", 0) <= max_used: errors.append("next_number would reuse a baseline identifier")
        baselines = {}
        for bid in ids:
            baseline = load_baseline(project, bid); baselines[bid] = baseline
            if baseline.get("Baseline_ID") != bid:
                errors.append(f"{bid}: baseline record identity does not match registry entry")
            related = baseline.get("Related_Change_Requests", [])
            if not isinstance(related, list):
                errors.append(f"{bid}: Related_Change_Requests must be a list")
            else:
                for cid in related:
                    if cid not in change_by_id:
                        errors.append(f"{bid}: related Change Request does not exist: {cid}")
            baseline_errors, baseline_warnings = validate_baseline(project, baseline); errors.extend(baseline_errors); warnings.extend(baseline_warnings)
            expected_status = None
            for number, item in enumerate(baseline.get("History", []), 1):
                old, new = item.get("previous_status"), item.get("new_status")
                if number > 1 and old != expected_status: errors.append(f"{bid}: discontinuous lifecycle history at event {number}")
                if old and new not in BASELINE_TRANSITIONS.get(old, set()) and not (old == new == "DRAFT" and item.get("comment") == "DRAFT snapshot refreshed"): errors.append(f"{bid}: invalid historical transition {old} -> {new}")
                expected_status = new
            if expected_status != baseline.get("Status"): errors.append(f"{bid}: status does not match lifecycle history")
            if baseline.get("Status") == "SUPERSEDED":
                replacement = baseline.get("Superseded_By")
                if replacement not in ids: errors.append(f"{bid}: replacement baseline does not exist: {replacement}")
        for bid, baseline in baselines.items():
            if baseline.get("Status") != "SUPERSEDED":
                continue
            seen = {bid}
            replacement = baseline.get("Superseded_By")
            while replacement in baselines:
                if replacement in seen:
                    errors.append(f"{bid}: cyclic baseline supersession")
                    break
                seen.add(replacement)
                successor = baselines[replacement]
                if successor.get("Status") in {"FROZEN", "RELEASED"}:
                    break
                if successor.get("Status") != "SUPERSEDED":
                    errors.append(f"{bid}: replacement chain must end in FROZEN or RELEASED baseline")
                    break
                replacement = successor.get("Superseded_By")
        selected = current_baseline(project)
        candidates = [bid for bid, value in baselines.items() if value.get("Status") in {"FROZEN", "RELEASED"}]
        if selected:
            if selected not in baselines: errors.append(f"STATUS.md Current Baseline does not exist: {selected}")
            elif baselines[selected].get("Status") not in {"FROZEN", "RELEASED"}: errors.append(f"STATUS.md Current Baseline is not FROZEN or RELEASED: {selected}")
            else:
                unexpected = release_candidate_delta(project, baselines[selected])
                if unexpected:
                    errors.append(
                        f"Current baseline {selected} differs from HEAD outside "
                        "controlled baseline metadata: " + ", ".join(unexpected)
                    )
        elif candidates:
            errors.append("STATUS.md Current Baseline is missing while a release candidate exists")
        if release_candidate is not None:
            candidate_id = selected if release_candidate == "CURRENT" else release_candidate
            if not candidate_id:
                errors.append("A FROZEN current baseline is required for release")
            elif selected != candidate_id:
                errors.append(
                    f"Release candidate {candidate_id} is not selected as Current Baseline"
                )
            elif candidate_id not in baselines:
                errors.append(f"Release candidate does not exist: {candidate_id}")
            elif baselines[candidate_id].get("Status") != "FROZEN":
                errors.append(f"Release candidate is not FROZEN: {candidate_id}")
            else:
                unexpected = release_candidate_delta(project, baselines[candidate_id])
                if unexpected:
                    errors.append(
                        "Engineering content changed after the baseline candidate commit: "
                        + ", ".join(unexpected)
                    )
    except Exception as exc:
        errors.append(f"Baseline registry audit failed: {exc}")
    if strict:
        errors.extend(f"Strict audit warning: {warning}" for warning in warnings)
        warnings = []
    return errors, warnings


def main(argv=None):
    parser = argparse.ArgumentParser(description="Audit Project Manager V1.1 change and baseline configuration control")
    parser.add_argument("project"); parser.add_argument("--strict", action="store_true")
    parser.add_argument("--release-candidate", nargs="?", const="CURRENT")
    args = parser.parse_args(argv)
    errors, warnings = audit(
        Path(args.project).resolve(), args.strict, args.release_candidate
    )
    for warning in warnings: print(f"WARN: {warning}")
    for error in errors: print(f"ERROR: {error}")
    if errors: print(f"CONFIGURATION AUDIT: FAIL ({len(errors)} error(s), {len(warnings)} warning(s))"); return 1
    print(f"CONFIGURATION AUDIT: PASS ({len(warnings)} warning(s))"); return 0


if __name__ == "__main__": sys.exit(main())
