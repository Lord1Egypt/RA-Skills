#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Rebuild the paper index offline from pinned sources and versioned rules."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
from functools import lru_cache
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCES = SKILL_ROOT / "references"
CATALOG_PATH = REFERENCES / "catalog-snapshot.json"
RULES_PATH = REFERENCES / "routing-rules.json"
ARCHIVE_PATH = REFERENCES / "archive-records.json"
AUDIT_PATH = REFERENCES / "legacy-routing-review.json"
SELECTION_METADATA_PATH = REFERENCES / "paper-selection-metadata.json"
RELATIONS_PATH = REFERENCES / "paper-repository-relations.json"
PAPERS_PATH = REFERENCES / "papers.jsonl"
STATE_PATH = REFERENCES / "source-state.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Rebuild or verify papers.jsonl from the pinned catalog snapshot, archive "
            "records, relation evidence, and routing rules. No network is used."
        )
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Verify only (default).")
    mode.add_argument("--write", action="store_true", help="Write deterministic outputs.")
    parser.add_argument(
        "--bootstrap-from-current",
        type=Path,
        help=(
            "Maintainer-only: extract archive records and legacy review sets from the "
            "specified existing papers.jsonl before rebuilding."
        ),
    )
    parser.add_argument("--pretty", action="store_true", help="Indent JSON status output.")
    return parser.parse_args()


def emit(payload: Any, pretty: bool) -> None:
    json.dump(
        payload,
        sys.stdout,
        ensure_ascii=True,
        indent=2 if pretty else None,
        sort_keys=True,
    )
    sys.stdout.write("\n")


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="wb", prefix=f".{path.name}.", suffix=".tmp", dir=path.parent, delete=False
    ) as handle:
        temporary = Path(handle.name)
        handle.write(content)
        handle.flush()
    try:
        temporary.replace(path)
    finally:
        if temporary.exists():
            temporary.unlink()


def source_text(record: dict[str, Any], field: str) -> str:
    value = record.get(field, "")
    if isinstance(value, list):
        return "\n".join(str(item) for item in value)
    return str(value or "")


@lru_cache(maxsize=None)
def phrase_pattern(phrase: str) -> re.Pattern[str]:
    escaped = re.escape(phrase)
    if phrase[:1].isalnum():
        escaped = r"(?<![A-Za-z0-9])" + escaped
    if phrase[-1:].isalnum():
        escaped += r"(?![A-Za-z0-9])"
    return re.compile(escaped, re.IGNORECASE)


def phrase_match(text: str, phrase: str) -> re.Match[str] | None:
    return phrase_pattern(phrase).search(text)


def route_group(
    record: dict[str, Any],
    rules: list[dict[str, Any]],
    field_order: list[str],
    confidence_by_field: dict[str, float],
    limit: int,
) -> tuple[list[str], dict[str, list[dict[str, Any]]]]:
    candidates: dict[str, tuple[tuple[float, int], dict[str, Any]]] = {}
    for rule in rules:
        for field_index, field in enumerate(field_order):
            text = source_text(record, field)
            for phrase in rule["patterns"]:
                match = phrase_match(text, phrase)
                if match is None:
                    continue
                confidence = float(confidence_by_field[field])
                evidence = {
                    "rule_id": rule["rule_id"],
                    "matched_field": field,
                    "matched_span": [match.start(), match.end()],
                    "matched_text": text[match.start() : match.end()],
                    "confidence": confidence,
                    "review_status": "evidence_confirmed_v1.1",
                }
                rank = (confidence, int(rule["priority"]) - field_index)
                prior = candidates.get(rule["label"])
                if prior is None or rank > prior[0]:
                    candidates[rule["label"]] = (rank, evidence)
                break
            if rule["label"] in candidates:
                break
    ordered = sorted(
        candidates,
        key=lambda label: (
            -candidates[label][0][0],
            -candidates[label][0][1],
            label,
        ),
    )[:limit]
    return ordered, {label: [candidates[label][1]] for label in ordered}


def extract_summary(abstract: str) -> tuple[str, dict[str, Any]]:
    normalized = abstract.strip()
    sentence_match = re.search(r"[.!?](?:[\"')\]]*)\s", normalized)
    end = sentence_match.end() - 1 if sentence_match else len(normalized)
    sentence = normalized[:end].strip()
    truncated = False
    source_end = len(sentence)
    if len(sentence) > 480:
        boundary = sentence.rfind(" ", 0, 480)
        if boundary < 1:
            boundary = 479
        sentence = sentence[:boundary].rstrip() + "…"
        source_end = boundary
        truncated = True
    return sentence, {
        "source_field": "abstract",
        "source_span": [0, source_end],
        "truncated": truncated,
        "input_sha256": sha256_bytes(normalized.encode("utf-8")),
        "policy": "first_sentence_word_boundary_max_480_characters",
    }


def relation_map() -> dict[str, list[dict[str, Any]]]:
    if not RELATIONS_PATH.is_file():
        return {}
    payload = load_json(RELATIONS_PATH)
    output: dict[str, list[dict[str, Any]]] = {}
    for relation in payload.get("relations", []):
        doi = relation.get("paper_doi")
        if not isinstance(doi, str) or relation.get("paper_scope") != "indexed":
            continue
        output.setdefault(doi.casefold(), []).append(
            {
                "url": relation["repository_url"],
                "relation_type": relation["relation_type"],
                "evidence": relation["evidence"],
            }
        )
    for values in output.values():
        values.sort(key=lambda item: (item["url"], item["relation_type"]))
    return output


def legacy_review_map(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    mapped: dict[str, dict[str, Any]] = {}
    for set_name, entries in payload.get("review_sets", {}).items():
        for entry in entries:
            identifier = str(entry.get("doi") or entry.get("paper_id"))
            mapped.setdefault(
                identifier.casefold(),
                {"status": "completed_v1.1", "review_sets": []},
            )["review_sets"].append(set_name)
    for value in mapped.values():
        value["review_sets"].sort()
    return mapped


def bootstrap(current_path: Path) -> None:
    records = load_jsonl(current_path)
    archive = [
        record
        for record in records
        if record.get("record_type") == "archive_only_provenance"
    ]
    canonical = [
        record for record in records if record.get("record_type") == "canonical_paper"
    ]
    catalog = load_json(CATALOG_PATH)
    catalog_by_doi = {
        str(record["doi"]).casefold(): record for record in catalog["records"]
    }
    optimal_positive = (
        "optimal transport",
        "wasserstein",
        "kantorovich",
        "gradient flow",
        "jko/evi",
        "jko scheme",
    )
    review_sets: dict[str, list[dict[str, Any]]] = {
        "legacy_optimal_transport_label": [],
        "legacy_optimal_transport_without_specific_indicator": [],
        "free_energy_disambiguation": [],
        "legacy_four_or_more_dimensions": [],
        "legacy_five_or_more_methods": [],
    }
    for record in canonical:
        identifier = {"doi": record["doi"], "title": record["title"]}
        text_record = catalog_by_doi.get(record["doi"].casefold(), {})
        full_text = " ".join(
            source_text(text_record, field) for field in ("title", "keywords", "abstract")
        ).casefold()
        if "optimal_transport_and_gradient_flows" in record.get("method_terms", []):
            review_sets["legacy_optimal_transport_label"].append(identifier)
            if not any(phrase in full_text for phrase in optimal_positive):
                review_sets[
                    "legacy_optimal_transport_without_specific_indicator"
                ].append(identifier)
        if re.search(r"free[- ]energy", full_text):
            review_sets["free_energy_disambiguation"].append(identifier)
        if len(record.get("phase_dimensions", [])) >= 4:
            review_sets["legacy_four_or_more_dimensions"].append(identifier)
        if len(record.get("method_terms", [])) >= 5:
            review_sets["legacy_five_or_more_methods"].append(identifier)
    for entries in review_sets.values():
        entries.sort(key=lambda item: item["doi"])
    audit = {
        "schema_version": "1.1.0",
        "status": "completed",
        "method": (
            "Every listed record is rerouted with versioned field/span evidence. "
            "Labels without retained evidence are removed."
        ),
        "review_sets": review_sets,
        "counts": {key: len(value) for key, value in review_sets.items()},
        "unique_title_counts": {
            key: len({entry["title"] for entry in value})
            for key, value in review_sets.items()
        },
    }
    atomic_write(ARCHIVE_PATH, canonical_bytes({"records": archive}))
    atomic_write(AUDIT_PATH, canonical_bytes(audit))
    atomic_write(
        SELECTION_METADATA_PATH,
        canonical_bytes(
            {
                "schema_version": "1.1.0",
                "records": [
                    {
                        "doi": record["doi"],
                        "works_url": record.get("works_url"),
                        "mapping_status": record.get("mapping_status"),
                        "content_status": record.get("content_status"),
                        "quality_flags": record.get("quality_flags", []),
                    }
                    for record in canonical
                ],
            }
        ),
    )


def build_records() -> list[dict[str, Any]]:
    catalog = load_json(CATALOG_PATH)
    rules = load_json(RULES_PATH)
    archive_payload = load_json(ARCHIVE_PATH)
    audit_payload = load_json(AUDIT_PATH)
    selection_payload = load_json(SELECTION_METADATA_PATH)
    state = load_json(STATE_PATH)
    excluded = {
        item["doi"].casefold()
        for item in state["paper_selection"]["catalog_records_not_in_papers_config"]
    }
    relations = relation_map()
    reviews = legacy_review_map(audit_payload)
    selection_by_doi = {
        record["doi"].casefold(): record for record in selection_payload["records"]
    }
    catalog_sha = sha256_file(CATALOG_PATH)
    rules_sha = sha256_file(RULES_PATH)
    generator_sha = sha256_file(Path(__file__))
    records: list[dict[str, Any]] = []
    for source in catalog["records"]:
        doi = str(source["doi"])
        if doi.casefold() in excluded:
            continue
        summary, summary_provenance = extract_summary(str(source.get("abstract") or ""))
        routing: dict[str, dict[str, list[dict[str, Any]]]] = {}
        labels: dict[str, list[str]] = {}
        for output_name, rule_name in (
            ("themes", "theme_rules"),
            ("method_terms", "method_rules"),
            ("phase_dimensions", "dimension_rules"),
        ):
            values, evidence = route_group(
                source,
                rules[rule_name],
                rules["field_order"],
                rules["confidence_by_field"],
                int(rules["limits"][output_name]),
            )
            labels[output_name] = values
            routing[output_name] = evidence
        record_hash = sha256_bytes(canonical_bytes(source))
        selection = selection_by_doi[doi.casefold()]
        record = {
            "record_type": "canonical_paper",
            "paper_id": doi,
            "doi": doi,
            "title": source["title"],
            "authors": source.get("authors", []),
            "date_published": source.get("date_published"),
            "primary_theme": labels["themes"][0] if labels["themes"] else "unclassified",
            "themes": labels["themes"],
            "summary": summary,
            "summary_type": "extractive_first_sentence_from_catalog_abstract",
            "summary_provenance": summary_provenance,
            "method_terms": labels["method_terms"],
            "phase_dimensions": labels["phase_dimensions"],
            "routing_evidence": routing,
            "routing_review": reviews.get(
                doi.casefold(),
                {"status": "evidence_confirmed_v1.1", "review_sets": []},
            ),
            "keywords": source.get("keywords", []),
            "related_repositories": relations.get(doi.casefold(), []),
            "canonical_url": source.get("canonical_url") or source.get("doi_url"),
            "works_url": selection.get("works_url") or source.get("local_record_url"),
            "catalog_sha256": catalog_sha,
            "source_hashes": {
                "catalog_record_sha256": record_hash,
                "catalog_snapshot_sha256": catalog_sha,
                "routing_rules_sha256": rules_sha,
                "generator_sha256": generator_sha,
            },
            "derivation_version": "paper-index-v1.1.0",
            "mapping_status": selection.get("mapping_status"),
            "content_status": selection.get("content_status"),
            "quality_flags": selection.get("quality_flags", []),
        }
        records.append(record)
    for source in archive_payload["records"]:
        record = dict(source)
        record["catalog_sha256"] = None
        record["derivation_version"] = "archive-index-v1.1.0"
        record["source_hashes"] = {
            "catalog_snapshot_sha256": catalog_sha,
            "routing_rules_sha256": rules_sha,
            "generator_sha256": generator_sha,
            "archive_sha256": record.get("archive_sha256"),
            "tex_sha256": record.get("tex_sha256"),
        }
        record["summary_provenance"] = {
            "source_field": "archive_source_condensation",
            "source_span": None,
            "truncated": False,
            "input_sha256": record.get("tex_sha256"),
            "policy": record.get("summary_type"),
        }
        record["routing_evidence"] = {
            "themes": {},
            "method_terms": {},
            "phase_dimensions": {},
        }
        record["routing_review"] = {
            "status": "archive_provenance_reviewed_v1.1",
            "review_sets": [],
        }
        records.append(record)
    if len(records) != 231:
        raise ValueError(f"expected 231 records, built {len(records)}")
    return records


def output_bytes(records: list[dict[str, Any]]) -> bytes:
    return b"".join(canonical_bytes(record) for record in records)


def main() -> int:
    args = parse_args()
    try:
        if args.bootstrap_from_current is not None:
            bootstrap(args.bootstrap_from_current)
        records = build_records()
        content = output_bytes(records)
        actual = PAPERS_PATH.read_bytes() if PAPERS_PATH.is_file() else b""
        matches = actual == content
        if args.write:
            atomic_write(PAPERS_PATH, content)
            state = load_json(STATE_PATH)
            state["hashes"]["catalog_snapshot_sha256"] = sha256_file(CATALOG_PATH)
            state["hashes"]["routing_rules_sha256"] = sha256_file(RULES_PATH)
            state["hashes"]["legacy_routing_review_sha256"] = sha256_file(AUDIT_PATH)
            state["hashes"]["archive_records_sha256"] = sha256_file(ARCHIVE_PATH)
            state["hashes"]["paper_selection_metadata_sha256"] = sha256_file(
                SELECTION_METADATA_PATH
            )
            state["hashes"]["derived_papers_jsonl_sha256"] = sha256_bytes(content)
            state["derivation"]["classification_policy"] = (
                "Versioned token-boundary rules retain only labels with a stored rule, "
                "field, matched span, confidence, and completed review status."
            )
            atomic_write(
                STATE_PATH,
                json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True).encode(
                    "utf-8"
                )
                + b"\n",
            )
            matches = True
        emit(
            {
                "ok": matches,
                "mode": "write" if args.write else "check",
                "records": len(records),
                "canonical_records": sum(
                    record["record_type"] == "canonical_paper" for record in records
                ),
                "archive_only_records": sum(
                    record["record_type"] == "archive_only_provenance"
                    for record in records
                ),
                "output_sha256": sha256_bytes(content),
                "matches_bundled_index": matches,
            },
            args.pretty,
        )
        return 0 if matches else 1
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"rebuild_indexes: {exc}", file=sys.stderr)
        emit({"ok": False, "error": str(exc)}, args.pretty)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
