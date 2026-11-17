#!/usr/bin/env python3

import argparse
import re
import sys
from collections import Counter

from pm_common import (
    HEADING_DEF_RE,
    REQ_STATUS_VALUES,
    VERIFICATION_ACTIVITIES,
    VERIFICATION_METHODS,
    VERIFICATION_SCOPES,
    contains_placeholder,
    parse_requirement_id,
    parse_requirement_record,
    requirement_block_text,
    requirement_definitions,
)


PROCESS_RE = re.compile(r"^[A-Z]{2,6}\d{1,2}$")

V11_FIELDS = {
    "status",
    "upstream",
    "allocated_to",
    "verification_method",
    "verification_scope",
    "verification_activity",
    "verification_process",
    "implementation_milestone",
    "verification_milestone",
    "owner",
    "priority",
    "change_id",
    "rationale",
    "acceptance_criteria",
}

REMOVED_SOURCE_FIELDS = {
    "source_type",
    "source_document",
    "source_locator",
}


def legacy_requirement_block(item):
    lines = item["lines"]
    start = item["line"] - 1

    if not HEADING_DEF_RE.match(lines[start]):
        return lines[start]

    block = [lines[start]]

    for line in lines[start + 1:]:
        if re.match(r"^\s*#{2,6}\s+", line):
            break
        block.append(line)

    return "\n".join(block)


def normative_wording(text):
    return bool(
        re.search(
            # English is canonical for generated content. The French forms
            # preserve compatibility with legacy requirement statements.
            r"\b(shall|must|will|should|doit|doivent|devra|devront)\b",
            text or "",
            re.IGNORECASE,
        )
    )


def add_issue(errors, warnings, message, strict=True):
    if strict:
        errors.append(message)
    else:
        warnings.append(message)


def lint_upstream(record, errors):
    rid = record["id"]
    upstream = record.get("upstream")

    # ROOT and DERIVED are the only two special text values.
    if isinstance(upstream, str):
        if upstream in ("ROOT", "DERIVED"):
            return

        errors.append(
            f"{rid}: invalid Upstream: {upstream}"
        )
        return

    # Otherwise Upstream must be a list of one or more
    # revisioned V1.1 references.
    if not isinstance(upstream, list) or not upstream:
        errors.append(
            f"{rid}: Upstream missing or invalid"
        )
        return

    for reference in upstream:
        identity = parse_requirement_id(reference)

        if (
            identity is None
            or identity.get("scheme") != "V1.1"
            or not identity.get("revisioned")
        ):
            errors.append(
                f"{rid}: invalid Upstream reference: "
                f"{reference}"
            )



def lint_legacy(item, args, errors, warnings):
    rid = item["id"]
    block = legacy_requirement_block(item)

    if contains_placeholder(block):
        add_issue(
            errors,
            warnings,
            f"{rid}: placeholder detected",
            args.strict,
        )

    if not normative_wording(block):
        add_issue(
            errors,
            warnings,
            f"{rid}: normative shall wording not detected",
            args.strict,
        )

    if HEADING_DEF_RE.match(item["text"]):
        if not re.search(
            r"verification\s+method\s*:",
            block,
            re.IGNORECASE,
        ):
            add_issue(
                errors,
                warnings,
                f"{rid}: Verification Method missing",
                args.strict,
            )




def lint_v11(item, args, errors, warnings):
    record = parse_requirement_record(item)
    rid = record["id"]
    meta = record.get("attributes", {})
    status = (record.get("status") or "").upper()

    # The parser preserves the existing metadata representation, while lint
    # rejects ambiguity before duplicate fields can change lifecycle meaning.
    seen_fields = set()
    for line in requirement_block_text(item).splitlines()[1:]:
        if re.match(r"^\s*(?:Text\s*:|\[END_REQ\])\s*$", line, re.IGNORECASE):
            break
        match = re.match(r"^\s*([A-Za-z][A-Za-z0-9_]*)\s*:", line)
        if match:
            field = match.group(1).lower()
            if field in seen_fields:
                errors.append(f"{rid}: duplicate attribute: {field}")
            seen_fields.add(field)

    if not record.get("terminated"):
        errors.append(
            f"{rid}: [END_REQ] missing"
        )

    if not status:
        errors.append(
            f"{rid}: Status missing"
        )
    elif status not in REQ_STATUS_VALUES:
        errors.append(
            f"{rid}: invalid Status: {status}"
        )

    if contains_placeholder(
        record.get("requirement_text") or ""
    ):
        errors.append(
            f"{rid}: placeholder detected in Text"
        )

    # The Source_* attributes were removed from the V1.1 model.
    for key in sorted(REMOVED_SOURCE_FIELDS):
        if key in meta:
            errors.append(
                f"{rid}: obsolete attribute not allowed: {key}"
            )

    unknown = (
        set(meta)
        - V11_FIELDS
        - REMOVED_SOURCE_FIELDS
    )

    for key in sorted(unknown):
        add_issue(
            errors,
            warnings,
            f"{rid}: unknown attribute: {key}",
            args.strict,
        )

    lint_upstream(record, errors)

    if (
        record.get("upstream") == "DERIVED"
        and not record.get("rationale")
    ):
        errors.append(
            f"{rid}: Rationale is mandatory for DERIVED requirements"
        )

    # The text remains mandatory even for a cancelled requirement,
    # in order to preserve the technical history.
    text = record.get("requirement_text")

    if not text:
        errors.append(
            f"{rid}: Text missing or empty"
        )
    elif not normative_wording(text):
        add_issue(
            errors,
            warnings,
            f"{rid}: normative shall wording not detected",
            args.strict,
        )

    if not record.get("acceptance_criteria"):
        errors.append(
            f"{rid}: Acceptance_Criteria missing"
        )

    # A CANCELLED requirement remains historical but no longer has
    # an active allocation or planning obligation.
    active = status != "CANCELLED"

    allocated = (
        record.get("allocated_to") or ""
    ).upper()

    if active and not allocated:
        errors.append(
            f"{rid}: Allocated_To missing"
        )
    elif allocated and allocated != "NONE":
        if not PROCESS_RE.fullmatch(allocated):
            errors.append(
                f"{rid}: invalid Allocated_To: {allocated}"
            )

    method = (
        record.get("verification_method") or ""
    ).upper()

    scope = (
        record.get("verification_scope") or ""
    ).upper()

    activity = (
        record.get("verification_activity") or ""
    ).upper()

    process = (
        record.get("verification_process") or ""
    ).upper()

    if active:
        if not method:
            errors.append(
                f"{rid}: Verification_Method missing"
            )
        elif method not in VERIFICATION_METHODS:
            errors.append(
                f"{rid}: invalid Verification_Method: {method}"
            )

        if not scope:
            errors.append(
                f"{rid}: Verification_Scope missing"
            )
        elif scope not in VERIFICATION_SCOPES:
            errors.append(
                f"{rid}: invalid Verification_Scope: {scope}"
            )

        if not activity:
            errors.append(
                f"{rid}: Verification_Activity missing"
            )
        elif activity not in VERIFICATION_ACTIVITIES:
            errors.append(
                f"{rid}: invalid Verification_Activity: {activity}"
            )

        if not process:
            errors.append(
                f"{rid}: Verification_Process missing"
            )
        elif not PROCESS_RE.fullmatch(process):
            errors.append(
                f"{rid}: invalid Verification_Process: {process}"
            )

        if not record.get("implementation_milestone"):
            errors.append(
                f"{rid}: Implementation_Milestone missing"
            )

    # R2 and later correspond to a controlled change.
    revision = record.get("revision_number")

    if revision and revision >= 2:
        if not record.get("change_id"):
            errors.append(
                f"{rid}: Change_ID is mandatory from revision R2 onward"
            )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project")
    parser.add_argument(
        "--strict",
        action="store_true",
    )
    args = parser.parse_args()

    definitions = requirement_definitions(
        args.project
    )

    if not definitions:
        print("Requirements checked: 0")

        if args.strict:
            print("ERROR: no requirement detected")
            print("RESULT: 1 error(s), 0 warning(s)")
            return 1

        print("RESULT: 0 error(s), 0 warning(s)")
        return 0

    errors = []
    warnings = []

    ids = [item["id"] for item in definitions]

    for rid, count in Counter(ids).items():
        if count > 1:
            errors.append(
                f"{rid}: duplicate definition ({count})"
            )

    for item in definitions:
        if item.get("scheme") == "V1.1":
            lint_v11(
                item,
                args,
                errors,
                warnings,
            )
        else:
            lint_legacy(
                item,
                args,
                errors,
                warnings,
            )

    print(
        f"Requirements checked: "
        f"{len(definitions)}"
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
