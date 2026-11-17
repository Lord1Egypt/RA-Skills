"""Coverage checker: how much of the source does an IR actually use?

Guards against the weak-model failure of "read half the article and stop"
(plan decision D5). Coverage is computed structurally: each section of the
source (h2 outline by default) counts as covered when any anchor inside it
is referenced by the IR; tables are tracked individually because dropped
tables are the most common silent content loss.

The report is advisory data — thresholds and pass/fail policy belong to the
pipeline (P3), not here. `status` is a suggestion computed from default
thresholds so CLI users get a signal without extra wiring.
"""

from __future__ import annotations

from .evidence_ledger import evidence_by_id
from .source_doc import SourceDoc, parse_anchor

DEFAULT_SECTION_THRESHOLD = 0.6
DEFAULT_TABLE_THRESHOLD = 1.0


def _referenced_anchors(ir: dict) -> dict[str, set[str]]:
    refs: dict[str, set[str]] = {}

    def note(ref: dict | None) -> None:
        if not isinstance(ref, dict):
            return
        parsed = parse_anchor(ref.get("loc", ""))
        if parsed is None:
            return
        refs.setdefault(ref.get("source_id", ""), set()).add(f"{parsed[0]}_{parsed[1]}")

    for slide in ir.get("slides", []):
        for block in slide.get("blocks", []):
            note(block.get("source_ref"))
            for multi_ref in block.get("source_refs", []) or []:
                note(multi_ref)
            for item in block.get("items", []) or []:
                note(item.get("source_ref"))
                for multi_ref in item.get("source_refs", []) or []:
                    note(multi_ref)
    return refs


def _sections(doc: SourceDoc) -> list[tuple[str, set[str]]]:
    level = 2 if doc.headings(2) else (1 if len(doc.headings(1)) > 1 else None)
    if level is None:
        return [(doc.title() or "(whole document)",
                 {e.anchor for e in doc.elements})]
    sections: list[tuple[str, set[str]]] = []
    title, anchors = "(preamble)", set()
    for element in doc.elements:
        if element.etype == f"h{level}":
            if anchors:
                sections.append((title, anchors))
            title, anchors = element.text, {element.anchor}
        else:
            anchors.add(element.anchor)
    if anchors:
        sections.append((title, anchors))
    return sections


def coverage_report(ir: dict, docs: dict[str, SourceDoc], *,
                    section_threshold: float = DEFAULT_SECTION_THRESHOLD,
                    table_threshold: float = DEFAULT_TABLE_THRESHOLD) -> dict:
    referenced = _referenced_anchors(ir)
    per_source: list[dict] = []
    for source_id, doc in docs.items():
        used = referenced.get(source_id, set())
        sections = _sections(doc)
        covered = [t for t, anchors in sections if anchors & used]
        uncovered = [t for t, anchors in sections if not (anchors & used)]
        tables = [t.anchor for t in doc.tables()]
        tables_covered = [a for a in tables if a in used]
        per_source.append({
            "source_id": source_id,
            "sections_total": len(sections),
            "sections_covered": len(covered),
            "sections_uncovered": uncovered,
            "section_ratio": round(len(covered) / len(sections), 3) if sections else 1.0,
            "tables_total": len(tables),
            "tables_covered": len(tables_covered),
            "tables_uncovered": [a for a in tables if a not in used],
            "table_ratio": round(len(tables_covered) / len(tables), 3) if tables else 1.0,
        })

    worst_section = min((s["section_ratio"] for s in per_source), default=1.0)
    worst_table = min((s["table_ratio"] for s in per_source), default=1.0)
    status = "pass"
    if worst_section < section_threshold or worst_table < table_threshold:
        status = "warn"
    if worst_section < section_threshold / 2:
        status = "fail"
    return {
        "status": status,
        "section_threshold": section_threshold,
        "table_threshold": table_threshold,
        "sources": per_source,
    }


def _ratio(numerator: int | float, denominator: int | float) -> float:
    return round(numerator / denominator, 4) if denominator else 1.0


def evidence_coverage_report(content_bindings: dict, ledger: dict) -> dict:
    """Measure selected and deliberately omitted evidence independently."""
    units = evidence_by_id(ledger)
    selected: set[str] = set()
    omitted: set[str] = set()
    for slide in content_bindings.get("slides", []) if isinstance(content_bindings, dict) else []:
        if not isinstance(slide, dict):
            continue
        selected.update(
            evidence_id for evidence_id in slide.get("evidence_ids", [])
            if isinstance(evidence_id, str) and evidence_id in units
        )
        for omission in slide.get("omissions", []) or []:
            if not isinstance(omission, dict):
                continue
            evidence_id, reason = omission.get("evidence_id"), omission.get("reason")
            if (
                isinstance(evidence_id, str)
                and evidence_id in units
                and isinstance(reason, str)
                and reason.strip()
            ):
                omitted.add(evidence_id)

    handled = selected | omitted
    total_weight = sum(float(unit.get("salience", 0)) for unit in units.values())
    selected_weight = sum(
        float(units[evidence_id].get("salience", 0)) for evidence_id in selected
    )
    required = {
        evidence_id for evidence_id, unit in units.items() if unit.get("must_keep")
    }
    numeric = {
        evidence_id for evidence_id, unit in units.items()
        if unit.get("kind") == "metric" or unit.get("numbers")
    }
    exhibits = {
        evidence_id for evidence_id, unit in units.items()
        if unit.get("kind") == "exhibit"
    }
    return {
        "total_evidence": len(units),
        "selected_evidence": len(selected),
        "omitted_evidence": len(omitted),
        "weighted_ratio": _ratio(selected_weight, total_weight),
        "required_ratio": _ratio(len(required & handled), len(required)),
        "numeric_ratio": _ratio(len(numeric & selected), len(numeric)),
        "exhibit_ratio": _ratio(len(exhibits & handled), len(exhibits)),
        "selected_evidence_ids": sorted(selected),
        "omitted_evidence_ids": sorted(omitted),
        "uncovered_evidence_ids": sorted(set(units) - handled),
        "missing_required_evidence_ids": sorted(required - handled),
        "missing_numeric_evidence_ids": sorted(numeric - selected),
        "unhandled_exhibit_ids": sorted(exhibits - handled),
    }
