"""Deterministic source evidence units for Template-route content planning."""

from __future__ import annotations

import hashlib
import json

from .source_doc import SourceDoc, SourceElement, parse_anchor


EVIDENCE_KINDS = {
    "claim", "metric", "comparison", "trend", "process", "method", "risk", "exhibit",
}


def _source_digest(doc: SourceDoc) -> str:
    payload = json.dumps(
        doc.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


def _kind(element: SourceElement) -> str:
    if element.etype in {"table", "img"}:
        return "exhibit"
    if element.numbers():
        return "metric"
    return "claim"


def _number_record(value: str) -> dict:
    return {
        "value": value,
        "unit": "%" if value.endswith("%") else None,
        "period": None,
    }


def build_evidence_ledger(
    docs: dict[str, SourceDoc],
    source_hashes: dict[str, str] | None = None,
) -> dict:
    """Build stable evidence units without inventing facts or relationships."""
    sources: list[dict] = []
    units: list[dict] = []
    for source_id, doc in docs.items():
        digest = (source_hashes or {}).get(source_id) or _source_digest(doc)
        sources.append({"source_id": source_id, "sha256": digest})
        for element in doc.elements:
            if element.etype.startswith("h") or not element.full_text():
                continue
            kind = _kind(element)
            units.append({
                "evidence_id": f"{source_id}:{element.anchor}",
                "source_ref": {"source_id": source_id, "loc": element.anchor},
                "kind": kind,
                "text": element.full_text(),
                "entities": [],
                "numbers": [
                    _number_record(value) for value in sorted(element.numbers())
                ],
                "relations": [],
                "salience": (
                    3.0 if kind == "exhibit" else 2.0 if kind == "metric" else 1.0
                ),
                "must_keep": kind in {"metric", "exhibit"},
                "exhibit_id": (
                    f"{source_id}:{element.anchor}" if kind == "exhibit" else None
                ),
            })
    return {
        "schema_version": "1.0.0",
        "sources": sources,
        "evidence_units": units,
    }


def evidence_by_id(ledger: dict) -> dict[str, dict]:
    """Index well-formed evidence units; the validator reports duplicates."""
    return {
        unit["evidence_id"]: unit
        for unit in ledger.get("evidence_units", [])
        if isinstance(unit, dict) and isinstance(unit.get("evidence_id"), str)
    }


def _issue(code: str, **evidence) -> dict:
    return {"code": code, **evidence}


def validate_evidence_ledger(ledger: dict) -> list[dict]:
    """Return stable validation issues instead of raising on user data."""
    if not isinstance(ledger, dict):
        return [_issue("EVIDENCE_LEDGER_INVALID")]
    issues: list[dict] = []
    if ledger.get("schema_version") != "1.0.0":
        issues.append(_issue("EVIDENCE_LEDGER_VERSION_INVALID"))

    sources = ledger.get("sources")
    if not isinstance(sources, list):
        return [*issues, _issue("EVIDENCE_SOURCES_INVALID")]
    source_ids = {
        source.get("source_id")
        for source in sources
        if isinstance(source, dict) and isinstance(source.get("source_id"), str)
    }

    units = ledger.get("evidence_units")
    if not isinstance(units, list):
        return [*issues, _issue("EVIDENCE_UNITS_INVALID")]

    seen: set[str] = set()
    for index, unit in enumerate(units):
        if not isinstance(unit, dict):
            issues.append(_issue("EVIDENCE_UNIT_INVALID", index=index))
            continue
        evidence_id = unit.get("evidence_id")
        if not isinstance(evidence_id, str) or not evidence_id:
            issues.append(_issue("EVIDENCE_ID_INVALID", index=index))
        elif evidence_id in seen:
            issues.append(_issue("EVIDENCE_ID_DUPLICATE", evidence_id=evidence_id))
        else:
            seen.add(evidence_id)

        source_ref = unit.get("source_ref")
        source_id = source_ref.get("source_id") if isinstance(source_ref, dict) else None
        loc = source_ref.get("loc") if isinstance(source_ref, dict) else None
        if source_id not in source_ids:
            issues.append(_issue("EVIDENCE_SOURCE_UNKNOWN", evidence_id=evidence_id))
        if not isinstance(loc, str) or parse_anchor(loc) is None:
            issues.append(_issue("EVIDENCE_ANCHOR_INVALID", evidence_id=evidence_id))

        kind = unit.get("kind")
        if kind not in EVIDENCE_KINDS:
            issues.append(_issue("EVIDENCE_KIND_INVALID", evidence_id=evidence_id))
        salience = unit.get("salience")
        if (
            isinstance(salience, bool)
            or not isinstance(salience, (int, float))
            or salience <= 0
        ):
            issues.append(_issue("EVIDENCE_SALIENCE_INVALID", evidence_id=evidence_id))
        if kind == "exhibit" and not unit.get("exhibit_id"):
            issues.append(_issue("EXHIBIT_ID_REQUIRED", evidence_id=evidence_id))

    return issues
