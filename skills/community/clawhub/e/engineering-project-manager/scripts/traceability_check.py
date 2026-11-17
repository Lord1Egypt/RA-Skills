#!/usr/bin/env python3

import argparse
import sys
from collections import defaultdict
from pathlib import Path

from pm_common import (
    REQ_ID_RE,
    parse_requirement_id,
    parse_requirement_record,
    read_text,
    requirement_definitions,
)


def add_issue(errors, warnings, message, strict):
    if strict:
        errors.append(message)
    else:
        warnings.append(message)


def status_of(record):
    return (record.get("status") or "").upper()


def latest_record(records):
    return max(
        records,
        key=lambda item: item.get("revision_number") or 0,
    )


def build_v11_model(definitions):
    records = [
        parse_requirement_record(item)
        for item in definitions
        if item.get("scheme") == "V1.1"
    ]

    by_full = {
        record["id"]: record
        for record in records
    }

    by_base = defaultdict(list)

    for record in records:
        by_base[record["base_id"]].append(record)

    current_by_base = {
        base_id: latest_record(items)
        for base_id, items in by_base.items()
    }

    active = [
        record
        for record in current_by_base.values()
        if status_of(record) != "CANCELLED"
    ]

    return (
        records,
        by_full,
        by_base,
        current_by_base,
        active,
    )


def check_v11_upstream(
    active,
    by_full,
    by_base,
    errors,
):
    checked_links = 0

    for child in active:
        upstream = child.get("upstream")

        if isinstance(upstream, str):
            if upstream in ("ROOT", "DERIVED"):
                continue

        if not isinstance(upstream, list):
            continue

        for reference in upstream:
            checked_links += 1

            identity = parse_requirement_id(reference)

            if (
                identity is None
                or identity.get("scheme") != "V1.1"
            ):
                continue

            exact = by_full.get(reference)
            base_id = identity["base_id"]

            if exact is None:
                candidates = by_base.get(base_id, [])

                if candidates:
                    latest = latest_record(candidates)

                    errors.append(
                        f"{child['id']}: Upstream reference "
                        f"has no exact definition: {reference}; "
                        f"latest available revision: "
                        f"{latest['id']}"
                    )
                else:
                    errors.append(
                        f"{child['id']}: Upstream reference "
                        f"has no definition: {reference}"
                    )

                continue

            if status_of(exact) == "CANCELLED":
                errors.append(
                    f"{child['id']}: Upstream reference "
                    f"points to a CANCELLED requirement: "
                    f"{reference}"
                )

            candidates = by_base.get(base_id, [])

            if not candidates:
                continue

            latest = latest_record(candidates)

            if (
                latest.get("revision_number", 0)
                > identity.get("revision_number", 0)
            ):
                errors.append(
                    f"{child['id']}: stale Upstream reference: "
                    f"{reference}; current revision: "
                    f"{latest['id']}"
                )

    return checked_links


def check_v11_coverage(
    active,
    errors,
    warnings,
    strict,
):
    children_by_upstream = defaultdict(list)

    for child in active:
        upstream = child.get("upstream")

        if not isinstance(upstream, list):
            continue

        for reference in upstream:
            children_by_upstream[reference].append(child)

    for parent in active:
        allocated = (
            parent.get("allocated_to") or ""
        ).upper()

        if not allocated:
            continue

        children = children_by_upstream.get(
            parent["id"],
            [],
        )

        if allocated == "NONE":
            if children:
                child_ids = ", ".join(
                    child["id"]
                    for child in children
                )

                errors.append(
                    f"{parent['id']}: Allocated_To is NONE "
                    f"but downstream coverage exists: "
                    f"{child_ids}"
                )

            continue

        if not children:
            add_issue(
                errors,
                warnings,
                f"{parent['id']}: no downstream requirement "
                f"for Allocated_To {allocated}",
                strict,
            )
            continue

        valid_children = []

        for child in children:
            actual_process = (
                child.get("process") or ""
            ).upper()

            if actual_process == allocated:
                valid_children.append(child)
                continue

            errors.append(
                f"{parent['id']}: ALLOCATION VIOLATION: "
                f"expected process {allocated}, "
                f"but covered by {child['id']} "
                f"({actual_process})"
            )

        if not valid_children:
            errors.append(
                f"{parent['id']}: no valid downstream "
                f"coverage by process {allocated}"
            )


def check_v11_cycles(active, errors):
    """Reject circular derivation among exact active requirement revisions."""
    graph = {
        record["id"]: record["upstream"]
        if isinstance(record.get("upstream"), list) else []
        for record in active
    }
    visited = set()
    for identifier in graph:
        if identifier in visited:
            continue
        path = [identifier]
        positions = {identifier: 0}
        stack = [(identifier, iter(graph[identifier]))]
        while stack:
            node, neighbors = stack[-1]
            upstream = next(neighbors, None)
            if upstream is None:
                visited.add(node)
                stack.pop()
                positions.pop(node)
                path.pop()
            elif upstream in positions:
                cycle = path[positions[upstream]:] + [upstream]
                errors.append("Circular Upstream traceability: " + " -> ".join(cycle))
            elif upstream in graph and upstream not in visited:
                positions[upstream] = len(path)
                path.append(upstream)
                stack.append((upstream, iter(graph[upstream])))


def check_legacy(
    project,
    definitions,
    errors,
    warnings,
    strict,
):
    legacy = [
        item
        for item in definitions
        if item.get("scheme") != "V1.1"
    ]

    if not legacy:
        return 0

    trace = (
        project
        / "01-requirements"
        / "TRACEABILITY.md"
    )

    if not trace.exists():
        errors.append(
            "TRACEABILITY.md is missing for legacy requirements."
        )
        return 0

    trace_text = read_text(trace)

    defined = {
        item["id"]
        for item in legacy
    }

    referenced = set()

    for rid in REQ_ID_RE.findall(trace_text):
        identity = parse_requirement_id(rid)

        if (
            identity
            and identity.get("scheme") == "LEGACY"
        ):
            referenced.add(rid)

    dangling = referenced - defined

    for rid in sorted(dangling):
        errors.append(
            f"{rid}: reference has no definition"
        )

    missing = defined - referenced

    for rid in sorted(missing):
        add_issue(
            errors,
            warnings,
            f"{rid}: missing from TRACEABILITY.md",
            strict,
        )

    return len(referenced)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project")
    parser.add_argument(
        "--strict",
        action="store_true",
    )

    args = parser.parse_args()
    project = Path(args.project)

    definitions = requirement_definitions(project)

    errors = []
    warnings = []

    if not definitions:
        if args.strict:
            errors.append(
                "No requirements available for traceability."
            )
        else:
            print(
                "SKIP: no requirements available "
                "for traceability."
            )
            return 0

    (
        v11_records,
        by_full,
        by_base,
        current_by_base,
        active,
    ) = build_v11_model(definitions)

    v11_links = check_v11_upstream(
        active,
        by_full,
        by_base,
        errors,
    )
    check_v11_cycles(active, errors)

    check_v11_coverage(
        active,
        errors,
        warnings,
        args.strict,
    )

    legacy_refs = check_legacy(
        project,
        definitions,
        errors,
        warnings,
        args.strict,
    )

    print(
        f"Defined requirements: {len(definitions)}"
    )
    print(
        f"V1.1 requirements: {len(v11_records)}"
    )
    print(
        f"V1.1 current requirements: "
        f"{len(current_by_base)}"
    )
    print(
        f"V1.1 active requirements: {len(active)}"
    )
    print(
        f"Requirements referenced in traceability: "
        f"{v11_links + legacy_refs}"
    )

    for warning in warnings:
        print("WARNING:", warning)

    for error in errors:
        print("ERROR:", error)

    print(
        f"RESULT: {len(errors)} error(s), "
        f"{len(warnings)} warning(s)"
    )

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
