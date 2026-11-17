#!/usr/bin/env python3
"""Phase 16.5 final traceability, staleness, Notes, and support QA."""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from phase16_claims import ClaimContractError, ContentOrigin, resolve_binding
from phase16_editorial import EditorialReport
from phase16_slide_evidence import SlideEvidencePlan
from source_grounding import SourceInventory


ERROR_FINAL_TRACEABILITY_INVALID = "PHASE16_FINAL_TRACEABILITY_INVALID"
ERROR_FINAL_TRACEABILITY_INCOMPLETE = "PHASE16_FINAL_TRACEABILITY_INCOMPLETE"
ERROR_STALE_EVIDENCE = "PHASE16_STALE_EVIDENCE"


class FinalTraceabilityError(Exception):
    def __init__(self, error_code: str, message: str) -> None:
        super().__init__(message)
        self.error_code = error_code


@dataclass(frozen=True)
class FinalSlideRecord:
    plan: SlideEvidencePlan
    rendered_text: str
    speaker_notes: str = ""
    unsupported_source_claims: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.plan, SlideEvidencePlan) or not isinstance(self.rendered_text, str):
            raise FinalTraceabilityError(ERROR_FINAL_TRACEABILITY_INVALID, "final slide record is invalid")
        object.__setattr__(self, "unsupported_source_claims", tuple(self.unsupported_source_claims))


@dataclass(frozen=True)
class DependencyImpact:
    source_ids: tuple[str, ...]
    claim_ids: tuple[str, ...]
    slide_ids: tuple[str, ...]


@dataclass(frozen=True)
class FinalTraceabilityReport:
    slide_count: int
    grounded_claims: int
    user_provided_claims: int
    agy_synthesis_claims: int
    unsupported_claims: tuple[str, ...]
    stale_claim_ids: tuple[str, ...]
    stale_slide_ids: tuple[str, ...]
    evidence_bindings: int
    editorial_warnings: tuple[str, ...]

    @property
    def evidence_complete(self) -> bool:
        return not self.unsupported_claims and not self.stale_claim_ids

    def require_complete(self) -> None:
        if self.stale_claim_ids:
            raise FinalTraceabilityError(ERROR_STALE_EVIDENCE, "stale evidence requires revalidation")
        if self.unsupported_claims:
            raise FinalTraceabilityError(ERROR_FINAL_TRACEABILITY_INCOMPLETE, "unsupported source-derived claims remain")

    def to_dict(self) -> dict[str, Any]:
        return {
            "agy_synthesis_claims": self.agy_synthesis_claims,
            "editorial_warnings": list(self.editorial_warnings),
            "evidence_bindings": self.evidence_bindings,
            "evidence_complete": self.evidence_complete,
            "grounded_claims": self.grounded_claims,
            "slide_count": self.slide_count,
            "stale_claim_ids": list(self.stale_claim_ids),
            "stale_slide_ids": list(self.stale_slide_ids),
            "unsupported_claims": list(self.unsupported_claims),
            "user_provided_claims": self.user_provided_claims,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def dependency_impact(
    slides: Iterable[FinalSlideRecord], current_source_digests: Mapping[str, str]
) -> DependencyImpact:
    changed_sources: set[str] = set()
    claim_ids: set[str] = set()
    slide_ids: set[str] = set()
    for slide in slides:
        for material in slide.plan.claims:
            for binding in material.claim.evidence:
                current = current_source_digests.get(binding.source_id)
                if current is not None and current != binding.source_digest:
                    changed_sources.add(binding.source_id)
                    claim_ids.add(material.claim.claim_id)
                    slide_ids.add(slide.plan.slide_id)
    return DependencyImpact(tuple(sorted(changed_sources)), tuple(sorted(claim_ids)), tuple(sorted(slide_ids)))


def build_traceability_report(
    inventory: SourceInventory,
    slides: Iterable[FinalSlideRecord],
    *,
    current_source_digests: Mapping[str, str] | None = None,
    editorial_report: EditorialReport | None = None,
) -> FinalTraceabilityReport:
    clean = tuple(slides)
    if not clean:
        raise FinalTraceabilityError(ERROR_FINAL_TRACEABILITY_INVALID, "final traceability requires slides")
    origins = {origin: 0 for origin in ContentOrigin}
    evidence_count = 0
    unsupported: list[str] = []
    for slide in clean:
        slide.plan.validate_rendered_text(slide.rendered_text)
        unsupported.extend(item for item in slide.unsupported_source_claims if isinstance(item, str) and item.strip())
        for material in slide.plan.claims:
            claim = material.claim
            origins[claim.origin] += 1
            for binding in claim.evidence:
                try:
                    resolve_binding(inventory, binding)
                except ClaimContractError as exc:
                    raise FinalTraceabilityError(ERROR_FINAL_TRACEABILITY_INVALID, str(exc)) from exc
                evidence_count += 1
    impact = dependency_impact(clean, current_source_digests or {})
    warnings = tuple(warning.code for warning in editorial_report.warnings) if editorial_report else ()
    return FinalTraceabilityReport(
        len(clean),
        origins[ContentOrigin.SOURCE_GROUNDED],
        origins[ContentOrigin.USER_PROVIDED],
        origins[ContentOrigin.AGY_SYNTHESIS],
        tuple(sorted(unsupported)),
        impact.claim_ids,
        impact.slide_ids,
        evidence_count,
        warnings,
    )


def _source_label(inventory: SourceInventory, source_id: str) -> str:
    source = next(item for item in inventory.data["sources"] if item["source_id"] == source_id)
    label = source.get("label")
    return label.strip() if isinstance(label, str) and label.strip() else "Project source"


def _locator_label(locator: Mapping[str, Any]) -> str:
    if locator.get("kind") == "page":
        start, end = locator.get("start"), locator.get("end")
        return f"page {start}" if end in (None, start) else f"pages {start}–{end}"
    if locator.get("kind") == "line_range":
        return f"lines {locator.get('start')}–{locator.get('end') or locator.get('start')}"
    return str(locator.get("label") or locator.get("kind") or "source location")


def compose_traceable_notes(record: FinalSlideRecord, inventory: SourceInventory) -> str:
    """Keep presenter notes first and append human-readable provenance."""
    lines: list[str] = []
    seen: set[str] = set()
    for material in record.plan.claims:
        claim = material.claim
        if claim.origin is ContentOrigin.SOURCE_GROUNDED:
            for binding in claim.evidence:
                resolve_binding(inventory, binding)
                line = f"- {_source_label(inventory, binding.source_id)} — {_locator_label(binding.locator)}: {claim.text}"
                if line not in seen:
                    seen.add(line)
                    lines.append(line)
        elif claim.origin is ContentOrigin.USER_PROVIDED:
            lines.append(f"- User-provided: {claim.text}")
        else:
            lines.append(f"- AGY synthesis: {claim.text}")
    if not lines:
        return record.speaker_notes
    prefix = record.speaker_notes.rstrip()
    trace = "Traceability\n" + "\n".join(lines)
    return f"{prefix}\n\n---\n{trace}" if prefix else trace


def notes_map(records: Iterable[FinalSlideRecord], inventory: SourceInventory) -> dict[int, str]:
    result: dict[int, str] = {}
    for record in records:
        try:
            number = int(record.plan.slide_id.split("_", 1)[1])
        except (IndexError, ValueError) as exc:
            raise FinalTraceabilityError(ERROR_FINAL_TRACEABILITY_INVALID, "slide id cannot map to Notes") from exc
        result[number] = compose_traceable_notes(record, inventory)
    return result


def save_internal_report(workspace_root: str | Path, report: FinalTraceabilityReport) -> Path:
    root = Path(workspace_root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    path = root / "phase16_traceability.json"
    fd, temp_name = tempfile.mkstemp(prefix=".phase16_traceability.", suffix=".tmp", dir=root)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(report.to_dict(), ensure_ascii=False, sort_keys=True, indent=2) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)
    return path


__all__ = [
    "DependencyImpact", "ERROR_FINAL_TRACEABILITY_INCOMPLETE", "ERROR_FINAL_TRACEABILITY_INVALID",
    "ERROR_STALE_EVIDENCE", "FinalSlideRecord", "FinalTraceabilityError", "FinalTraceabilityReport",
    "build_traceability_report", "compose_traceable_notes", "dependency_impact", "notes_map",
    "save_internal_report",
]
