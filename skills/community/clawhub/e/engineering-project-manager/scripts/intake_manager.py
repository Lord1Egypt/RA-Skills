#!/usr/bin/env python3
"""Version local external sources and their reviewed obligation inventory."""

import argparse
from collections import Counter
import json
from pathlib import Path
import sys

from management_common import (
    RecordError, Store, add_record, artifact_errors, cell, digest, get_record,
    now, require_text, seal_artifact, write_view,
)

REGISTRY = "01-requirements/intake/SOURCES.json"
VIEW = "01-requirements/intake/SOURCES.md"
STATUSES = {"DRAFT", "REVIEWED", "SUPERSEDED"}
CONFIDENTIALITY = {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"}


def store(project):
    return Store(project, REGISTRY, "sources", "SRC")


def review_payload(record):
    return {key: record.get(key) for key in (
        "id", "title", "owner", "created_at", "source_key", "version", "reference",
        "license", "confidentiality", "artifact", "obligations",
        "reviewed_by", "reviewed_at", "review_rationale", "no_obligations_rationale",
    )}


def obligation(record, key):
    for item in record.get("obligations", []):
        if item.get("key") == key:
            return item
    raise RecordError(f"{record.get('id')}: unknown obligation: {key}")


def validate_registry(project, data):
    errors = store(project).errors(data)
    if errors:
        return errors
    records = data.get("records", [])
    if not isinstance(records, list):
        return errors
    known = {r.get("id"): r for r in records if isinstance(r, dict)}
    identities = []
    for record in records:
        if not isinstance(record, dict):
            continue
        rid = record.get("id", "<source>")
        try:
            for field in ("source_key", "version", "reference", "license"):
                require_text(record.get(field), field)
            identities.append((record["source_key"], record["version"]))
            if record.get("status") not in STATUSES:
                raise RecordError("invalid source status")
            if record.get("confidentiality") not in CONFIDENTIALITY:
                raise RecordError("invalid source confidentiality")
            errors.extend(f"{rid}: {item}" for item in artifact_errors(project, record.get("artifact")))
            items = record.get("obligations")
            if not isinstance(items, list):
                raise RecordError("obligations must be a list")
            keys = []
            for item in items:
                if not isinstance(item, dict):
                    raise RecordError("each obligation must be an object")
                for field in ("key", "locator", "text"):
                    require_text(item.get(field), f"obligation {field}")
                keys.append(item["key"])
            if len(keys) != len(set(keys)):
                raise RecordError("obligation keys must be unique within a source version")
            if record["status"] in {"REVIEWED", "SUPERSEDED"}:
                if not items:
                    require_text(record.get("no_obligations_rationale"), "explicit zero-obligation rationale")
                for field in ("reviewed_by", "reviewed_at", "review_rationale"):
                    require_text(record.get(field), field)
                if record.get("review_sha256") != digest(review_payload(record)):
                    raise RecordError("reviewed source snapshot SHA-256 mismatch")
            elif record.get("review_sha256") is not None:
                raise RecordError("DRAFT source cannot carry a reviewed snapshot")
            if record["status"] != "SUPERSEDED" and record.get("superseded_by"):
                raise RecordError("only SUPERSEDED sources may name a replacement")
            if record["status"] == "SUPERSEDED":
                visited = {rid}
                replacement = record.get("superseded_by")
                while True:
                    if replacement in visited:
                        raise RecordError("cyclic source supersession")
                    if replacement not in known:
                        raise RecordError("replacement source does not exist")
                    visited.add(replacement)
                    successor = known[replacement]
                    if successor.get("source_key") != record["source_key"]:
                        raise RecordError("replacement must belong to the same source_key")
                    if successor.get("status") == "REVIEWED":
                        break
                    if successor.get("status") != "SUPERSEDED":
                        raise RecordError("supersession must terminate in a REVIEWED source")
                    replacement = successor.get("superseded_by")
        except (RecordError, ValueError, TypeError, KeyError) as exc:
            errors.append(f"{rid}: {exc}")
    if len(identities) != len(set(identities)):
        errors.append("Source key/version pairs must be unique")
    previous = {}
    for event in data.get("history", []):
        after = event.get("after", {})
        rid = after.get("id")
        before = previous.get(rid)
        if before:
            transition = (before.get("status"), after.get("status"))
            if transition not in {("DRAFT", "DRAFT"), ("DRAFT", "REVIEWED"), ("REVIEWED", "SUPERSEDED")}:
                errors.append(f"{rid}: invalid historical source transition: {transition}")
            if before.get("status") in {"REVIEWED", "SUPERSEDED"} and review_payload(before) != review_payload(after):
                errors.append(f"{rid}: historical reviewed source snapshot was rewritten")
        elif after.get("status") != "DRAFT":
            errors.append(f"{rid}: source history must start in DRAFT")
        previous[rid] = after
    return errors


def audit(project, release=False):
    try:
        if not store(project).exists():
            return [], []
        data = store(project).read()
        errors = validate_registry(project, data)
        if errors:
            return errors, []
        warnings = []
        drafts = [r["id"] for r in data["records"] if r["status"] == "DRAFT"]
        if drafts:
            (errors if release else warnings).append("Sources await review: " + ", ".join(drafts))
        active = Counter(r["source_key"] for r in data["records"] if r["status"] == "REVIEWED")
        for key, count in active.items():
            if count > 1:
                (errors if release else warnings).append(
                    f"Source {key} has multiple reviewed versions; complete supersession"
                )
        return errors, warnings
    except (RecordError, OSError, ValueError, TypeError, KeyError) as exc:
        return [f"Source intake registry invalid: {exc}"], []


def render(project, data):
    lines = ["# External Source Intake", "", "Generated view; SOURCES.json is authoritative.", "",
             "| ID | Source | Version | Status | Owner | Confidentiality | Obligations |",
             "|---|---|---|---|---|---|---|"]
    for r in data["records"]:
        lines.append("| " + " | ".join(cell(str(value)) for value in (
            r["id"], r["source_key"], r["version"], r["status"], r["owner"],
            r["confidentiality"], len(r["obligations"]),
        )) + " |")
    for r in data["records"]:
        lines.extend(["", f"## {cell(r['id'])}", "",
                      f"- Reference: {cell(r['reference'])}",
                      f"- Rights/license declaration: {cell(r['license'])}",
                      f"- Staged file: {cell(r['artifact']['path'])}",
                      f"- SHA-256: {r['artifact']['sha256']}",
                      f"- Reviewed by: {cell(r.get('reviewed_by') or 'Not reviewed')}",
                      f"- Review rationale: {cell(r.get('review_rationale') or 'Not reviewed')}",
                      f"- Zero-obligation rationale: {cell(r.get('no_obligations_rationale') or 'Not applicable')}",
                      f"- Superseded by: {cell(r.get('superseded_by') or 'None')}",
                      "", "| Obligation | Locator | Text |", "|---|---|---|"])
        for item in r["obligations"]:
            lines.append("| " + " | ".join(cell(item[key]) for key in ("key", "locator", "text")) + " |")
    write_view(project, VIEW, "\n".join(lines) + "\n")


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=".")
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    init.add_argument("--actor", required=True)
    create = commands.add_parser("create")
    for field in ("title", "owner", "source-key", "version", "file", "reference", "license", "actor"):
        create.add_argument("--" + field, required=True)
    create.add_argument("--confidentiality", choices=sorted(CONFIDENTIALITY), required=True)
    item = commands.add_parser("obligation", help="Add one obligation to a DRAFT source inventory")
    item.add_argument("id")
    for field in ("key", "locator", "text", "actor"):
        item.add_argument("--" + field, required=True)
    item.add_argument("--replace", action="store_true", help="Correct an existing DRAFT obligation, preserving history")
    review = commands.add_parser("review", help="Seal the source version and complete obligation inventory")
    review.add_argument("id")
    review.add_argument("--actor", required=True)
    review.add_argument("--rationale", required=True)
    review.add_argument("--no-obligations-rationale", help="Explicitly justify a source containing zero applicable obligations to assess")
    supersede = commands.add_parser("supersede")
    supersede.add_argument("id")
    supersede.add_argument("--by", required=True)
    supersede.add_argument("--actor", required=True)
    supersede.add_argument("--rationale", required=True)
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
            print("Source intake initialized")
            return 0
        if args.command == "audit":
            errors, warnings = audit(project, args.release)
            for item in warnings:
                print("WARN: " + item)
            for item in errors:
                print("ERROR: " + item)
            print("SOURCE INTAKE AUDIT: " + ("FAIL" if errors else "PASS"))
            return 1 if errors else 0
        if args.command in {"list", "report", "render"}:
            data = manager.read()
            if args.command == "render":
                render(project, data)
            else:
                print(json.dumps(data["records"], indent=2, ensure_ascii=False))
            return 0

        def mutate(data):
            if args.command == "create":
                artifact = seal_artifact(project, args.file)
                resolved = (project / artifact["path"]).resolve()
                managed = {REGISTRY, VIEW, "01-requirements/intake/COMPLIANCE.json", "01-requirements/intake/COMPLIANCE.md"}
                if resolved in {(project / path).resolve() for path in managed}:
                    raise RecordError("Stage an external source file; management registries cannot be their own source")
                path = resolved.relative_to(project)
                if path.suffix.lower() == ".md" and path.parts[0] == "01-requirements":
                    raise RecordError("Stage source Markdown outside 01-requirements to avoid importing it as canonical requirements")
                return add_record(
                    data, "SRC", args.title, args.owner, "DRAFT",
                    source_key=require_text(args.source_key, "source key"),
                    version=require_text(args.version, "version"),
                    reference=require_text(args.reference, "source reference"),
                    license=require_text(args.license, "rights/license declaration"),
                    confidentiality=args.confidentiality, artifact=artifact, obligations=[],
                    reviewed_by=None, reviewed_at=None, review_rationale=None,
                    review_sha256=None, superseded_by=None, no_obligations_rationale=None,
                )["id"]
            record = get_record(data, args.id)
            if args.command == "obligation":
                if record["status"] != "DRAFT":
                    raise RecordError("Only DRAFT source obligations may be edited; create a new source version")
                key = require_text(args.key, "obligation key")
                existing = next((item for item in record["obligations"] if item["key"] == key), None)
                if bool(existing) != args.replace:
                    raise RecordError("Use --replace only when correcting an existing DRAFT obligation")
                value = {"key": key, "locator": require_text(args.locator, "locator"),
                         "text": require_text(args.text, "obligation text")}
                if existing:
                    existing.update(value)
                else:
                    record["obligations"].append(value)
            elif args.command == "review":
                if record["status"] != "DRAFT":
                    raise RecordError("Only DRAFT sources can be reviewed")
                if not record["obligations"]:
                    record["no_obligations_rationale"] = require_text(
                        args.no_obligations_rationale, "explicit zero-obligation rationale"
                    )
                elif args.no_obligations_rationale:
                    raise RecordError("Zero-obligation rationale is only valid for an empty inventory")
                record.update(status="REVIEWED", reviewed_by=require_text(args.actor, "actor"),
                              reviewed_at=now(), review_rationale=require_text(args.rationale, "rationale"))
                record["review_sha256"] = digest(review_payload(record))
            elif args.command == "supersede":
                replacement = get_record(data, args.by)
                if record["id"] == replacement["id"]:
                    raise RecordError("A source cannot supersede itself")
                if record["status"] != "REVIEWED" or replacement["status"] != "REVIEWED":
                    raise RecordError("Supersession requires two REVIEWED source versions")
                if record["source_key"] != replacement["source_key"]:
                    raise RecordError("Replacement must belong to the same source_key")
                record.update(status="SUPERSEDED", superseded_by=args.by,
                              supersession_rationale=require_text(args.rationale, "rationale"))
            return record["id"]

        data = manager.update(args.actor, args.command, mutate, validator=validate_registry)
        render(project, data)
        print(data["records"][-1]["id"] if args.command == "create" else args.id)
        return 0
    except (RecordError, OSError, ValueError, TypeError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
