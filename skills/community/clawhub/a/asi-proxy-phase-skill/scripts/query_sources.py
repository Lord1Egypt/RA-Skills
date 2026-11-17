#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Search the pinned paper and repository indexes without network access."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable


SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCES = SKILL_ROOT / "references"
PAPERS_PATH = REFERENCES / "papers.jsonl"
REPOSITORIES_PATH = REFERENCES / "repositories.json"
TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:[._:/-][A-Za-z0-9]+)*")
DIMENSIONS = (
    "provenance_integrity",
    "trust_quorum",
    "temporal_integrity",
    "structural_reachability",
    "causal_formation",
    "dimensional_consistency",
    "exact_self_maintenance",
    "finite_horizon_resource_persistence",
    "target_bound_generative_catalysis",
    "verification_capacity",
    "effective_independence",
    "coordination_protocol_integrity",
    "perturbation_robustness",
)
ROLES = (
    "core_intervention",
    "supporting_infrastructure",
    "evaluation_experiment",
    "research_source",
    "historical_exploratory",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Search the bundled evidence-scoped source indexes. The command is "
            "offline, read-only, and emits structured ASCII-safe JSON."
        )
    )
    parser.add_argument(
        "--kind",
        choices=("paper", "repo", "all"),
        default="all",
        help="Source type (default: all).",
    )
    parser.add_argument("--query", default="", help="DOI, repository name, or terms.")
    parser.add_argument(
        "--match",
        choices=("auto", "all", "any"),
        default="auto",
        help=(
            "Term policy. auto tries all terms and explicitly falls back to any only "
            "when all returns no result (default: auto)."
        ),
    )
    parser.add_argument(
        "--dimension",
        choices=DIMENSIONS,
        help="Require an exact phase-dimension identifier.",
    )
    parser.add_argument(
        "--role",
        choices=ROLES,
        help="Require an exact repository role; paper records are excluded.",
    )
    parser.add_argument(
        "--eligible-only",
        action="store_true",
        help="Exclude context-only repositories; paper records are unaffected.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum results from 1 to 100 (default: 10).",
    )
    parser.add_argument("--pretty", action="store_true", help="Indent JSON output.")
    parser.add_argument(
        "--full",
        action="store_true",
        help="Include the complete source record.",
    )
    return parser.parse_args()


def emit(payload: Any, *, pretty: bool = False) -> None:
    json.dump(
        payload,
        sys.stdout,
        ensure_ascii=True,
        indent=2 if pretty else None,
        sort_keys=True,
    )
    sys.stdout.write("\n")


def fail(message: str, pretty: bool) -> None:
    print(f"query_sources: {message}", file=sys.stderr)
    emit({"ok": False, "error": message}, pretty=pretty)
    raise SystemExit(2)


def load_papers() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(
        PAPERS_PATH.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"papers.jsonl:{line_number}: expected object")
        records.append(value)
    return records


def load_repositories() -> list[dict[str, Any]]:
    payload = json.loads(REPOSITORIES_PATH.read_text(encoding="utf-8"))
    records = payload.get("repositories") if isinstance(payload, dict) else payload
    if not isinstance(records, list) or not all(
        isinstance(record, dict) for record in records
    ):
        raise ValueError("repositories.json: expected repositories array")
    return records


def tokens(value: str) -> list[str]:
    return [token.casefold() for token in TOKEN_RE.findall(value)]


def flattened(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(flattened(item) for item in value)
    if isinstance(value, dict):
        return " ".join(
            f"{key} {flattened(item)}" for key, item in value.items()
        )
    return "" if value is None else str(value)


def searchable_fields(kind: str, record: dict[str, Any]) -> list[tuple[str, str, float]]:
    if kind == "paper":
        return [
            ("doi", str(record.get("doi") or ""), 100.0),
            ("paper_id", str(record.get("paper_id") or ""), 80.0),
            ("title", str(record.get("title") or ""), 14.0),
            ("keywords", flattened(record.get("keywords", [])), 8.0),
            ("summary", str(record.get("summary") or ""), 6.0),
            ("themes", flattened(record.get("themes", [])), 5.0),
            ("method_terms", flattened(record.get("method_terms", [])), 5.0),
            (
                "phase_dimensions",
                flattened(record.get("phase_dimensions", [])),
                5.0,
            ),
        ]
    return [
        ("name", str(record.get("name") or ""), 100.0),
        ("url", str(record.get("url") or ""), 60.0),
        ("summary", str(record.get("summary") or ""), 14.0),
        ("interfaces", flattened(record.get("interfaces", [])), 8.0),
        ("role", str(record.get("role") or ""), 7.0),
        ("dimensions", flattened(record.get("dimensions", [])), 6.0),
        ("dependencies", flattened(record.get("dependencies", {})), 4.0),
        ("related_papers", flattened(record.get("related_papers", [])), 4.0),
    ]


def score(
    kind: str, record: dict[str, Any], query: str, mode: str
) -> tuple[float, list[str]] | None:
    query_tokens = tokens(query)
    if not query_tokens:
        return 1.0, []
    normalized_query = query.strip().casefold()
    exact_identifiers = (
        [str(record.get("doi") or ""), str(record.get("paper_id") or "")]
        if kind == "paper"
        else [str(record.get("name") or ""), str(record.get("url") or "")]
    )
    exact = any(normalized_query == value.casefold() for value in exact_identifiers if value)
    field_data: list[tuple[str, set[str], str, float]] = []
    for name, text, weight in searchable_fields(kind, record):
        field_data.append((name, set(tokens(text)), text.casefold(), weight))
    matched_terms = [
        term
        for term in query_tokens
        if any(term in field_tokens for _, field_tokens, _, _ in field_data)
    ]
    if mode == "all" and len(matched_terms) != len(query_tokens):
        return None
    if mode == "any" and not matched_terms:
        return None
    value = 1000.0 if exact else 0.0
    matched_fields: set[str] = set()
    for name, field_tokens, field_text, weight in field_data:
        hits = sum(term in field_tokens for term in query_tokens)
        if hits:
            value += hits * weight
            matched_fields.add(name)
        if normalized_query and normalized_query in field_text:
            value += weight * 2
            matched_fields.add(name)
    return value, sorted(matched_fields)


def dimensions(record: dict[str, Any]) -> list[str]:
    values = record.get("phase_dimensions", record.get("dimensions", []))
    return [value for value in values if isinstance(value, str)]


def compact_routing_evidence(record: dict[str, Any]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    groups = record.get("routing_evidence", {})
    for group in ("phase_dimensions", "method_terms", "themes"):
        values = groups.get(group, {}) if isinstance(groups, dict) else {}
        for label, entries in values.items():
            if not isinstance(entries, list) or not entries:
                continue
            evidence = entries[0]
            output.append(
                {
                    "group": group,
                    "label": label,
                    "rule_id": evidence.get("rule_id"),
                    "matched_field": evidence.get("matched_field"),
                    "matched_span": evidence.get("matched_span"),
                    "matched_text": evidence.get("matched_text"),
                    "confidence": evidence.get("confidence"),
                }
            )
    return output[:8]


def compact_result(
    kind: str,
    record: dict[str, Any],
    score_value: float,
    matched_fields: list[str],
    full: bool,
) -> dict[str, Any]:
    if kind == "paper":
        identifier = str(record.get("doi") or record.get("paper_id") or "")
        result = {
            "source_type": "paper",
            "id": identifier,
            "title": record.get("title"),
            "url": record.get("canonical_url"),
            "summary": record.get("summary"),
            "phase_dimensions": dimensions(record),
            "score": round(score_value, 3),
            "matched_fields": matched_fields,
            "metadata": {
                "record_type": record.get("record_type"),
                "catalog_sha256": record.get("catalog_sha256"),
                "date_published": record.get("date_published"),
                "themes": record.get("themes", []),
                "methods": record.get("method_terms", []),
                "routing_evidence": compact_routing_evidence(record),
                "routing_review": record.get("routing_review", {}),
                "related_repositories": record.get("related_repositories", []),
            },
        }
    else:
        result = {
            "source_type": "repo",
            "id": record.get("name"),
            "title": record.get("name"),
            "url": record.get("url"),
            "summary": record.get("summary"),
            "phase_dimensions": dimensions(record),
            "score": round(score_value, 3),
            "matched_fields": matched_fields,
            "metadata": {
                "head_sha": record.get("head_sha"),
                "head_commit_date": record.get("head_commit_date"),
                "role": record.get("role"),
                "interfaces": record.get("interfaces", []),
                "maturity": record.get("maturity"),
                "evidence_state": record.get("evidence_state"),
                "license": record.get("license"),
                "selection_eligibility": record.get("selection_eligibility"),
                "dependencies": record.get("dependencies"),
                "related_papers": record.get("related_papers", []),
                "dimension_evidence": record.get("dimension_evidence", {}),
            },
        }
    if full:
        result["record"] = record
    return result


def filtered_records(
    args: argparse.Namespace,
) -> Iterable[tuple[str, dict[str, Any]]]:
    if args.kind in {"paper", "all"} and args.role is None:
        for record in load_papers():
            if args.dimension and args.dimension not in dimensions(record):
                continue
            yield "paper", record
    if args.kind in {"repo", "all"}:
        for record in load_repositories():
            if args.dimension and args.dimension not in dimensions(record):
                continue
            if args.role and record.get("role") != args.role:
                continue
            if args.eligible_only and record.get("selection_eligibility") == "context_only":
                continue
            yield "repo", record


def execute_search(
    records: list[tuple[str, dict[str, Any]]],
    query: str,
    mode: str,
    full: bool,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for kind, record in records:
        scored = score(kind, record, query, mode)
        if scored is None:
            continue
        score_value, matched_fields = scored
        results.append(
            compact_result(kind, record, score_value, matched_fields, full)
        )
    results.sort(key=lambda item: (-item["score"], str(item["id"]).casefold()))
    return results


def main() -> int:
    args = parse_args()
    if not 1 <= args.limit <= 100:
        fail("--limit must be between 1 and 100", args.pretty)
    if args.role and args.kind == "paper":
        fail("--role cannot be combined with --kind paper", args.pretty)
    try:
        records = list(filtered_records(args))
        effective_match = "all" if args.match == "auto" else args.match
        results = execute_search(records, args.query, effective_match, args.full)
        fallback = False
        if args.match == "auto" and args.query.strip() and not results:
            effective_match = "any"
            fallback = True
            results = execute_search(records, args.query, effective_match, args.full)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"query_sources: {exc}", file=sys.stderr)
        emit({"ok": False, "error": str(exc)}, pretty=args.pretty)
        return 1
    emit(
        {
            "ok": True,
            "request": {
                "kind": args.kind,
                "query": args.query,
                "match": args.match,
                "effective_match": effective_match,
                "auto_fallback_to_any": fallback,
                "dimension": args.dimension,
                "role": args.role,
                "eligible_only": args.eligible_only,
                "limit": args.limit,
                "full": args.full,
            },
            "examined": len(records),
            "matched": len(results),
            "returned": min(len(results), args.limit),
            "results": results[: args.limit],
        },
        pretty=args.pretty,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
