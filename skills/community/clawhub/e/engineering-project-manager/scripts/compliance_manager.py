#!/usr/bin/env python3
"""Assess external obligations and report evidence coverage, not conformity."""

import argparse
import json
from pathlib import Path
import sys

import intake_manager
from management_common import (
    RecordError, Store, add_record, cell, get_record, link_errors, now,
    require_strings, require_text, write_view,
)
from pm_common import active_requirement_records

REGISTRY = "01-requirements/intake/COMPLIANCE.json"
VIEW = "01-requirements/intake/COMPLIANCE.md"
STATUSES = {"UNASSESSED", "IN_SCOPE", "EXCLUDED"}
IMMUTABLE_FIELDS = ("id", "source_id", "obligation_key", "source_review_sha256", "locator", "source_text")


def store(project):
    return Store(project, REGISTRY, "compliance", "CMP")


def sources(project):
    manager = intake_manager.store(project)
    if not manager.exists():
        return {"records": []}
    data = manager.read()
    errors = intake_manager.validate_registry(project, data)
    if errors:
        raise RecordError("Invalid source intake: " + "; ".join(errors))
    return data


def proof_model(project):
    # Existing V1 evidence remains authoritative. Import lazily so help/init
    # and an empty legacy project do not require the evidence runtime.
    import verification_evidence as evidence
    try:
        data = evidence.load_registry(project)
        errors, _ = evidence.validate_registry(project, data)
    except (evidence.EvidenceError, ValueError, TypeError, KeyError, AttributeError) as exc:
        raise RecordError(f"Cannot use verification evidence: {exc}") from exc
    if errors:
        raise RecordError("Invalid verification evidence registry: " + "; ".join(errors))
    return {item["Evidence_ID"]: item for item in data["evidence"]}


def validate_registry(project, data):
    errors = store(project).errors(data)
    if errors:
        return errors
    if not data["records"]:
        return []
    try:
        by_source = {r["id"]: r for r in sources(project)["records"]}
        proof_ids = [eid for r in data["records"] for eid in require_strings(r.get("evidence", []), "evidence")]
        proofs = proof_model(project) if proof_ids else {}
    except (RecordError, OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        return [str(exc)]
    identities = []
    for record in data["records"]:
        rid = record["id"]
        try:
            source_id = require_text(record.get("source_id"), "source ID")
            key = require_text(record.get("obligation_key"), "obligation key")
            identities.append((source_id, key))
            source = by_source.get(source_id)
            if source is None or source["status"] not in {"REVIEWED", "SUPERSEDED"}:
                raise RecordError("Compliance requires an existing reviewed source version")
            item = intake_manager.obligation(source, key)
            if record.get("source_review_sha256") != source["review_sha256"]:
                raise RecordError("Source reviewed snapshot link is stale or altered")
            if record.get("locator") != item["locator"] or record.get("source_text") != item["text"]:
                raise RecordError("Source obligation locator/text differs from the reviewed inventory")
            status = record.get("status")
            if status not in STATUSES:
                raise RecordError("Invalid applicability status")
            requirements = require_strings(record.get("requirements"), "requirements")
            evidence_ids = require_strings(record.get("evidence"), "evidence")
            errors.extend(f"{rid}: {message}" for message in link_errors(project, record))
            if status == "IN_SCOPE" and not requirements:
                raise RecordError("IN_SCOPE applicability requires exact requirement revision links")
            if status != "IN_SCOPE" and (requirements or evidence_ids):
                raise RecordError("Only IN_SCOPE rows may carry requirement/evidence links")
            if status in {"IN_SCOPE", "EXCLUDED"}:
                for field in ("assessed_by", "assessed_at", "rationale"):
                    require_text(record.get(field), field)
            for eid in evidence_ids:
                if eid not in proofs:
                    raise RecordError(f"Unknown verification evidence: {eid}")
                if proofs[eid].get("Requirement_ID") not in requirements:
                    raise RecordError(f"Evidence {eid} does not reference a mapped requirement revision")
        except (RecordError, ValueError, TypeError, KeyError, AttributeError) as exc:
            errors.append(f"{rid}: {exc}")
    if len(identities) != len(set(identities)):
        errors.append("Only one compliance row is allowed for each exact source version/obligation")
    previous = {}
    for event in data["history"]:
        after = event["after"]
        rid = after["id"]
        before = previous.get(rid)
        if before:
            if any(before.get(key) != after.get(key) for key in IMMUTABLE_FIELDS):
                errors.append(f"{rid}: historical source obligation link was rewritten")
            if after.get("status") not in STATUSES:
                errors.append(f"{rid}: invalid historical applicability status")
        elif after.get("status") != "UNASSESSED":
            errors.append(f"{rid}: applicability history must start UNASSESSED")
        previous[rid] = after
    return errors


def coverage_report(project, data=None):
    """Inventory only: COVERED means linked compatible PASS evidence exists."""
    source_data = sources(project)
    data = data if data is not None else (store(project).read() if store(project).exists() else {"records": []})
    if store(project).exists():
        errors = validate_registry(project, data)
        if errors:
            raise RecordError("Invalid compliance registry: " + "; ".join(errors))
    rows = {(r["source_id"], r["obligation_key"]): r for r in data["records"]}
    active = {r["id"]: r for r in active_requirement_records(project)}
    evidence_ids = [eid for r in data["records"] for eid in r.get("evidence", [])]
    proofs = proof_model(project) if evidence_ids else {}
    result = []
    for source in source_data["records"]:
        if source["status"] != "REVIEWED":
            continue
        for item in source["obligations"]:
            row = rows.get((source["id"], item["key"]))
            entry = {"source_id": source["id"], "obligation_key": item["key"],
                     "locator": item["locator"], "compliance_id": row["id"] if row else None,
                     "applicability": row["status"] if row else "UNASSESSED",
                     "coverage": "UNRESOLVED", "findings": []}
            if row is None or row["status"] == "UNASSESSED":
                entry["findings"].append("Obligation applicability has not been assessed")
            elif row["status"] == "EXCLUDED":
                entry["coverage"] = "EXCLUDED"
            else:
                from verification_evidence import validate_evidence_against_requirement
                for requirement_id in row["requirements"]:
                    requirement = active.get(requirement_id)
                    if requirement is None:
                        entry["findings"].append(f"Stale or cancelled requirement revision: {requirement_id}")
                        continue
                    matching = [proofs[eid] for eid in row["evidence"]
                                if eid in proofs and proofs[eid].get("Requirement_ID") == requirement_id]
                    if not any(proof.get("Status") == "PASS"
                               and not validate_evidence_against_requirement(proof, requirement)
                               for proof in matching):
                        entry["findings"].append(f"No linked compatible PASS evidence for {requirement_id}")
                if not entry["findings"]:
                    entry["coverage"] = "COVERED"
            result.append(entry)
    return {"notice": "Evidence coverage and applicability only; not conformity, certification, or legal compliance.",
            "obligations": result}


def audit(project, release=False):
    try:
        if not store(project).exists() and not intake_manager.store(project).exists():
            return [], []
        data = store(project).read() if store(project).exists() else {"records": []}
        errors = validate_registry(project, data) if store(project).exists() else []
        if errors:
            return errors, []
        report = coverage_report(project, data)
        warnings = []
        for entry in report["obligations"]:
            for message in entry["findings"]:
                # Stale engineering links are invalid at every stage. Planned
                # coverage/applicability is visible during development and gates release.
                target = errors if release or message.startswith("Stale ") else warnings
                target.append(f"{entry['source_id']}/{entry['obligation_key']}: {message}")
        return errors, warnings
    except (RecordError, OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        return [f"Compliance registry invalid: {exc}"], []


def render(project, data):
    lines = ["# Source Obligation Compliance Matrix", "",
             "Generated view; COMPLIANCE.json is authoritative. Coverage is not conformity.", "",
             "| ID | Source | Obligation | Applicability | Requirements | Evidence |",
             "|---|---|---|---|---|---|"]
    for r in data["records"]:
        lines.append("| " + " | ".join(cell(r.get(key, "")) for key in (
            "id", "source_id", "obligation_key", "status", "requirements", "evidence"
        )) + " |")
    for r in data["records"]:
        lines.extend(["", f"## {cell(r['id'])}", "",
                      f"- Locator: {cell(r['locator'])}",
                      f"- Source text: {cell(r['source_text'])}",
                      f"- Assessed by: {cell(r.get('assessed_by') or 'Unassessed')}",
                      f"- Assessment rationale: {cell(r.get('rationale') or 'Unassessed')}"])
    write_view(project, VIEW, "\n".join(lines) + "\n")


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=".")
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    init.add_argument("--actor", required=True)
    create = commands.add_parser("create")
    for field in ("source", "obligation", "owner", "actor"):
        create.add_argument("--" + field, required=True)
    create.add_argument("--title")
    for name in ("map", "exclude", "reopen"):
        p = commands.add_parser(name)
        p.add_argument("id")
        p.add_argument("--actor", required=True)
        p.add_argument("--rationale", required=True)
        if name == "map":
            p.add_argument("--requirement", action="append", required=True)
            p.add_argument("--evidence", action="append", default=[])
    for name in ("list", "report", "audit"):
        p = commands.add_parser(name)
        if name == "audit":
            p.add_argument("--release", action="store_true")
    commands.add_parser("render")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    project = Path(args.project).resolve()
    try:
        manager = store(project)
        if args.command == "init":
            manager.initialize(args.actor)
            render(project, manager.read())
            print("Compliance matrix initialized")
            return 0
        if args.command == "audit":
            errors, warnings = audit(project, args.release)
            for item in warnings:
                print("WARN: " + item)
            for item in errors:
                print("ERROR: " + item)
            print("COMPLIANCE AUDIT: " + ("FAIL" if errors else "PASS"))
            return 1 if errors else 0
        if args.command == "report":
            errors, warnings = audit(project)
            if errors:
                raise RecordError("; ".join(errors))
            report = coverage_report(project)
            report["warnings"] = warnings
            print(json.dumps(report, indent=2, ensure_ascii=False))
            return 0
        if args.command in {"list", "render"}:
            data = manager.read()
            if args.command == "render":
                render(project, data)
            else:
                print(json.dumps(data["records"], indent=2, ensure_ascii=False))
            return 0

        def mutate(data):
            source_data = sources(project)
            if args.command == "create":
                source = get_record(source_data, args.source)
                if source["status"] != "REVIEWED":
                    raise RecordError("Create compliance rows only for a current REVIEWED source")
                item = intake_manager.obligation(source, args.obligation)
                return add_record(
                    data, "CMP", args.title or f"{source['source_key']}: {item['key']}", args.owner, "UNASSESSED",
                    source_id=source["id"], obligation_key=item["key"], locator=item["locator"],
                    source_text=item["text"], source_review_sha256=source["review_sha256"],
                    requirements=[], evidence=[], assessed_by=None, assessed_at=None, rationale=None,
                )["id"]
            record = get_record(data, args.id)
            source = get_record(source_data, record["source_id"])
            if source["status"] != "REVIEWED":
                raise RecordError("Historical source compliance is immutable; assess the replacement source")
            record.update(assessed_by=require_text(args.actor, "actor"), assessed_at=now(),
                          rationale=require_text(args.rationale, "rationale"))
            if args.command == "map":
                requirements = require_strings(args.requirement, "requirements")
                active = {r["id"] for r in active_requirement_records(project)}
                if any(rid not in active for rid in requirements):
                    raise RecordError("Map only exact current, non-cancelled requirement revisions")
                record.update(status="IN_SCOPE", requirements=requirements,
                              evidence=require_strings(args.evidence, "evidence"))
            else:
                record.update(status="EXCLUDED" if args.command == "exclude" else "UNASSESSED",
                              requirements=[], evidence=[])
            return record["id"]

        data = manager.update(args.actor, args.command, mutate, validator=validate_registry)
        render(project, data)
        print(data["records"][-1]["id"] if args.command == "create" else args.id)
        return 0
    except (RecordError, OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
