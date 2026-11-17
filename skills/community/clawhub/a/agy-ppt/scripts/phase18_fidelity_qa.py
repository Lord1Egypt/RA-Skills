#!/usr/bin/env python3
"""Phase 18.4 deterministic portability and visual-fidelity QA."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, replace
from enum import Enum
from pathlib import Path
from typing import Iterable

from phase18_contract import (
    DeliveryEditabilityContract,
    EditabilityClass,
    PlateProvenanceMode,
    PlateRequirement,
    ProductionStrategy,
    ReservedEditableZone,
)
from phase18_hybrid_pptx import ElementBox, HybridElement
from phase18_production_plan import ElementProductionPlan


ERROR_FIDELITY_QA_INVALID = "PHASE18_FIDELITY_QA_INVALID"


class FidelityQaError(Exception):
    def __init__(self, error_code: str, message: str) -> None:
        super().__init__(message)
        self.error_code = error_code


class QaDimension(str, Enum):
    CONTENT_INTEGRITY = "CONTENT_INTEGRITY"
    LAYOUT_INTEGRITY = "LAYOUT_INTEGRITY"
    VISUAL_FIDELITY = "VISUAL_FIDELITY"
    EDITABILITY = "EDITABILITY"


class FidelityIssue(str, Enum):
    CONTENT_CHANGED = "CONTENT_CHANGED"
    FONT_SUBSTITUTION = "FONT_SUBSTITUTION"
    MISSING_GLYPH = "MISSING_GLYPH"
    TEXT_REFLOW = "TEXT_REFLOW"
    TEXT_OVERFLOW = "TEXT_OVERFLOW"
    LINE_BREAK_DRIFT = "LINE_BREAK_DRIFT"
    OBJECT_SHIFT = "OBJECT_SHIFT"
    IMAGE_CROP_DRIFT = "IMAGE_CROP_DRIFT"
    Z_ORDER_CHANGE = "Z_ORDER_CHANGE"
    CHART_STYLE_DRIFT = "CHART_STYLE_DRIFT"
    COLOR_DRIFT = "COLOR_DRIFT"
    HIERARCHY_DEGRADATION = "HIERARCHY_DEGRADATION"
    EDITABILITY_LOST = "EDITABILITY_LOST"
    COMPOSITE_CONFLICT = "COMPOSITE_CONFLICT"


class QaSeverity(str, Enum):
    ACCEPTABLE = "ACCEPTABLE"
    WARNING = "WARNING"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    BLOCKING = "BLOCKING"


_SEVERITY_ORDER = {
    QaSeverity.ACCEPTABLE: 0,
    QaSeverity.WARNING: 1,
    QaSeverity.REVIEW_REQUIRED: 2,
    QaSeverity.BLOCKING: 3,
}


def _color(value: str) -> str:
    clean = value.upper() if isinstance(value, str) else ""
    if len(clean) != 6 or any(char not in "0123456789ABCDEF" for char in clean):
        raise FidelityQaError(ERROR_FIDELITY_QA_INVALID, "color must be six hex digits")
    return clean


def _crop(value: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    clean = tuple(float(item) for item in value)
    if len(clean) != 4 or any(not math.isfinite(item) or item < 0 or item > 1 for item in clean):
        raise FidelityQaError(ERROR_FIDELITY_QA_INVALID, "crop must contain four normalized values")
    return clean


@dataclass(frozen=True)
class ElementSnapshot:
    element_id: str
    content: str
    box: ElementBox
    font_name: str = "Arial"
    glyphs_present: bool = True
    line_count: int = 1
    overflow: bool = False
    crop: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)
    z_order: int = 0
    chart_style: str | None = None
    color: str = "000000"
    prominence: int = 1
    editable: bool = False
    evidence_bound: bool = False
    plate_mode: PlateProvenanceMode = PlateProvenanceMode.CLEAN_PLATE
    plate_contains_content: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.element_id, str) or not self.element_id.strip() or not isinstance(self.content, str):
            raise FidelityQaError(ERROR_FIDELITY_QA_INVALID, "snapshot identity and content are invalid")
        if not isinstance(self.box, ElementBox) or not isinstance(self.font_name, str) or not self.font_name:
            raise FidelityQaError(ERROR_FIDELITY_QA_INVALID, "snapshot geometry or font is invalid")
        if not isinstance(self.line_count, int) or isinstance(self.line_count, bool) or self.line_count < 1:
            raise FidelityQaError(ERROR_FIDELITY_QA_INVALID, "line count is invalid")
        if not isinstance(self.z_order, int) or isinstance(self.z_order, bool) or self.z_order < 0:
            raise FidelityQaError(ERROR_FIDELITY_QA_INVALID, "z-order is invalid")
        if not isinstance(self.prominence, int) or isinstance(self.prominence, bool) or self.prominence < 0:
            raise FidelityQaError(ERROR_FIDELITY_QA_INVALID, "prominence is invalid")
        for flag in (self.glyphs_present, self.overflow, self.editable, self.evidence_bound, self.plate_contains_content):
            if not isinstance(flag, bool):
                raise FidelityQaError(ERROR_FIDELITY_QA_INVALID, "snapshot flags must be boolean")
        if not isinstance(self.plate_mode, PlateProvenanceMode):
            raise FidelityQaError(ERROR_FIDELITY_QA_INVALID, "snapshot plate mode is invalid")
        object.__setattr__(self, "element_id", self.element_id.strip())
        object.__setattr__(self, "crop", _crop(self.crop))
        object.__setattr__(self, "color", _color(self.color))


@dataclass(frozen=True)
class FidelityFinding:
    issue: FidelityIssue
    dimension: QaDimension
    severity: QaSeverity
    element_id: str
    detail: str

    def internal_dict(self) -> dict[str, str]:
        return {
            "issue": self.issue.value,
            "dimension": self.dimension.value,
            "severity": self.severity.value,
            "element_id": self.element_id,
            "detail": self.detail,
        }


@dataclass(frozen=True)
class FidelityQaReport:
    status: QaSeverity
    findings: tuple[FidelityFinding, ...]
    approved_sample_compared: bool

    def canonical_json(self) -> str:
        payload = {
            "status": self.status.value,
            "approved_sample_compared": self.approved_sample_compared,
            "findings": [item.internal_dict() for item in self.findings],
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)

    def count(self, issue: FidelityIssue) -> int:
        return sum(item.issue is issue for item in self.findings)


def _distance(first: ElementBox, second: ElementBox) -> float:
    return max(abs(first.left - second.left), abs(first.top - second.top), abs(first.width - second.width), abs(first.height - second.height))


def compare_fidelity(
    approved: Iterable[ElementSnapshot],
    delivered: Iterable[ElementSnapshot],
    *,
    approved_sample: bool = True,
    layout_tolerance: float = 0.08,
    color_tolerance: int = 8,
) -> FidelityQaReport:
    reference = tuple(approved)
    result = tuple(delivered)
    if not reference or any(not isinstance(item, ElementSnapshot) for item in reference + result):
        raise FidelityQaError(ERROR_FIDELITY_QA_INVALID, "approved and delivered snapshots are required")
    if len({item.element_id for item in reference}) != len(reference) or len({item.element_id for item in result}) != len(result):
        raise FidelityQaError(ERROR_FIDELITY_QA_INVALID, "snapshot element ids must be unique")
    delivered_by_id = {item.element_id: item for item in result}
    findings: list[FidelityFinding] = []

    def add(issue, dimension, severity, element_id, detail):
        findings.append(FidelityFinding(issue, dimension, severity, element_id, detail))

    for expected in reference:
        actual = delivered_by_id.get(expected.element_id)
        if actual is None:
            detail = "evidence-bound element is missing" if expected.evidence_bound else "approved element is missing"
            add(FidelityIssue.CONTENT_CHANGED, QaDimension.CONTENT_INTEGRITY, QaSeverity.BLOCKING, expected.element_id, detail)
            continue
        if actual.content != expected.content:
            detail = "evidence-bound content changed" if expected.evidence_bound else "approved content changed"
            add(FidelityIssue.CONTENT_CHANGED, QaDimension.CONTENT_INTEGRITY, QaSeverity.BLOCKING, expected.element_id, detail)
        if not actual.glyphs_present:
            add(FidelityIssue.MISSING_GLYPH, QaDimension.CONTENT_INTEGRITY, QaSeverity.BLOCKING, expected.element_id, "one or more glyphs are missing")
        if actual.font_name != expected.font_name:
            add(FidelityIssue.FONT_SUBSTITUTION, QaDimension.VISUAL_FIDELITY, QaSeverity.WARNING, expected.element_id, f"{expected.font_name} -> {actual.font_name}")
        if actual.line_count != expected.line_count:
            difference = abs(actual.line_count - expected.line_count)
            severity = QaSeverity.ACCEPTABLE if difference == 1 and not actual.overflow else QaSeverity.REVIEW_REQUIRED
            add(FidelityIssue.LINE_BREAK_DRIFT, QaDimension.LAYOUT_INTEGRITY, severity, expected.element_id, f"{expected.line_count} -> {actual.line_count} lines")
            if difference > 1:
                add(FidelityIssue.TEXT_REFLOW, QaDimension.LAYOUT_INTEGRITY, QaSeverity.REVIEW_REQUIRED, expected.element_id, "text reflow exceeds the bounded tolerance")
        if actual.overflow:
            add(FidelityIssue.TEXT_OVERFLOW, QaDimension.LAYOUT_INTEGRITY, QaSeverity.REVIEW_REQUIRED, expected.element_id, "text exceeds its editability envelope")
        # Hybrid production shares the frozen assembly coordinate system:
        # 10 x 5.625 inches for 16:9.  Larger bounds previously let objects
        # pass QA while PowerPoint rendered them partly off-slide.
        if actual.box.left + actual.box.width > 10.001 or actual.box.top + actual.box.height > 5.626:
            add(FidelityIssue.TEXT_OVERFLOW, QaDimension.LAYOUT_INTEGRITY, QaSeverity.REVIEW_REQUIRED, expected.element_id, "object geometry extends outside slide bounds")
        distance = _distance(expected.box, actual.box)
        if distance > layout_tolerance:
            add(FidelityIssue.OBJECT_SHIFT, QaDimension.LAYOUT_INTEGRITY, QaSeverity.REVIEW_REQUIRED, expected.element_id, f"geometry drift {distance:.3f}in")
        if max(abs(left - right) for left, right in zip(expected.crop, actual.crop)) > 0.03:
            add(FidelityIssue.IMAGE_CROP_DRIFT, QaDimension.VISUAL_FIDELITY, QaSeverity.REVIEW_REQUIRED, expected.element_id, "crop differs materially")
        if expected.z_order != actual.z_order:
            add(FidelityIssue.Z_ORDER_CHANGE, QaDimension.LAYOUT_INTEGRITY, QaSeverity.REVIEW_REQUIRED, expected.element_id, "object stacking order changed")
        if expected.chart_style != actual.chart_style:
            add(FidelityIssue.CHART_STYLE_DRIFT, QaDimension.VISUAL_FIDELITY, QaSeverity.WARNING, expected.element_id, "chart styling differs")
        color_delta = max(abs(int(expected.color[index:index + 2], 16) - int(actual.color[index:index + 2], 16)) for index in (0, 2, 4))
        if color_delta > color_tolerance:
            add(FidelityIssue.COLOR_DRIFT, QaDimension.VISUAL_FIDELITY, QaSeverity.WARNING, expected.element_id, "key color differs beyond tolerance")
        if approved_sample and actual.prominence + 1 < expected.prominence:
            add(FidelityIssue.HIERARCHY_DEGRADATION, QaDimension.VISUAL_FIDELITY, QaSeverity.BLOCKING, expected.element_id, "approved visual hierarchy was materially weakened")
        if expected.editable and not actual.editable:
            add(FidelityIssue.EDITABILITY_LOST, QaDimension.EDITABILITY, QaSeverity.REVIEW_REQUIRED, expected.element_id, "planned editability was lost")

        # Composite conflict detection
        if (actual.plate_contains_content and actual.editable) or (actual.plate_mode is PlateProvenanceMode.FULL_COMPOSITE and actual.editable):
            add(
                FidelityIssue.COMPOSITE_CONFLICT,
                QaDimension.VISUAL_FIDELITY,
                QaSeverity.BLOCKING,
                expected.element_id,
                "composite conflict: editable native overlay placed over plate that already contains the content",
            )

    findings.sort(key=lambda item: (item.element_id, item.issue.value, item.detail))
    status = max((item.severity for item in findings), key=lambda item: _SEVERITY_ORDER[item], default=QaSeverity.ACCEPTABLE)
    return FidelityQaReport(status, tuple(findings), approved_sample)


def check_composite_conflicts(
    slide_id: str,
    plate_mode: PlateProvenanceMode,
    elements: Iterable[HybridElement],
    reserved_zones: Iterable[ReservedEditableZone] = (),
) -> tuple[FidelityFinding, ...]:
    """Deterministic QA gate checking for composite conflicts before hybrid presentation assembly."""
    findings: list[FidelityFinding] = []
    zones_by_id = {z.element_id: z for z in reserved_zones}
    for elem in elements:
        strategy = elem.plan.contract.strategy
        if strategy in {ProductionStrategy.NATIVE_TEXT, ProductionStrategy.NATIVE_IMAGE, ProductionStrategy.NATIVE_CHART}:
            if plate_mode is PlateProvenanceMode.FULL_COMPOSITE:
                findings.append(
                    FidelityFinding(
                        FidelityIssue.COMPOSITE_CONFLICT,
                        QaDimension.VISUAL_FIDELITY,
                        QaSeverity.BLOCKING,
                        elem.plan.element_id,
                        f"composite conflict: editable element '{elem.plan.element_id}' placed on FULL_COMPOSITE plate",
                    )
                )
            elif plate_mode is PlateProvenanceMode.PARTIAL_COMPOSITE:
                zone = zones_by_id.get(elem.plan.element_id)
                if zone is None or zone.plate_requirement is not PlateRequirement.CONTENT_FREE:
                    findings.append(
                        FidelityFinding(
                            FidelityIssue.COMPOSITE_CONFLICT,
                            QaDimension.VISUAL_FIDELITY,
                            QaSeverity.BLOCKING,
                            elem.plan.element_id,
                            f"composite conflict: editable element '{elem.plan.element_id}' lacks CONTENT_FREE reserved zone on PARTIAL_COMPOSITE plate",
                        )
                    )
    return tuple(findings)


@dataclass(frozen=True)
class FidelityRepairResult:
    plan: ElementProductionPlan
    repair_passes: int
    changed: bool


def safe_representation_fallback(
    plan: ElementProductionPlan,
    report: FidelityQaReport,
    *,
    repair_passes: int = 0,
) -> FidelityRepairResult:
    """Perform at most one representation-only fallback; semantic defects never auto-repair."""
    if not isinstance(plan, ElementProductionPlan) or not isinstance(report, FidelityQaReport):
        raise FidelityQaError(ERROR_FIDELITY_QA_INVALID, "plan and QA report are required")
    if repair_passes >= 1:
        return FidelityRepairResult(plan, repair_passes, False)
    relevant = [item for item in report.findings if item.element_id == plan.element_id]
    if not relevant:
        return FidelityRepairResult(plan, repair_passes, False)
    has_conflict = any(item.issue is FidelityIssue.COMPOSITE_CONFLICT for item in relevant)
    if any(item.dimension is QaDimension.CONTENT_INTEGRITY for item in relevant) and not has_conflict:
        return FidelityRepairResult(plan, repair_passes, False)
    if not any(item.severity in {QaSeverity.REVIEW_REQUIRED, QaSeverity.BLOCKING} for item in relevant):
        return FidelityRepairResult(plan, repair_passes, False)
    contract = DeliveryEditabilityContract(
        EditabilityClass.LOCKED_REQUIRED,
        ProductionStrategy.LOCKED_VISUAL,
        plan.contract.font_portability,
        delivery_profile=plan.contract.delivery_profile,
    )
    return FidelityRepairResult(replace(plan, contract=contract), 1, True)


def verify_pptx_package(
    pptx_path: str | Path,
    *,
    required_notes_by_slide: dict[int, str] | None = None,
) -> FidelityQaReport:
    """Deterministic validation of PPTX package integrity and required speaker notes."""
    import zipfile
    target = Path(pptx_path)
    findings: list[FidelityFinding] = []
    if not target.is_file():
        findings.append(FidelityFinding(FidelityIssue.CONTENT_CHANGED, QaDimension.CONTENT_INTEGRITY, QaSeverity.BLOCKING, "package", "PPTX package does not exist"))
        return FidelityQaReport(QaSeverity.BLOCKING, tuple(findings), False)
    if not zipfile.is_zipfile(target):
        findings.append(FidelityFinding(FidelityIssue.CONTENT_CHANGED, QaDimension.CONTENT_INTEGRITY, QaSeverity.BLOCKING, "package", "Broken PPTX package (not a zip file)"))
        return FidelityQaReport(QaSeverity.BLOCKING, tuple(findings), False)
    try:
        from pptx import Presentation
        deck = Presentation(str(target))
    except Exception as exc:
        findings.append(FidelityFinding(FidelityIssue.CONTENT_CHANGED, QaDimension.CONTENT_INTEGRITY, QaSeverity.BLOCKING, "package", f"Broken PPTX package: {exc}"))
        return FidelityQaReport(QaSeverity.BLOCKING, tuple(findings), False)

    if required_notes_by_slide:
        for slide_index, required_text in required_notes_by_slide.items():
            if slide_index < 0 or slide_index >= len(deck.slides):
                findings.append(FidelityFinding(FidelityIssue.CONTENT_CHANGED, QaDimension.CONTENT_INTEGRITY, QaSeverity.BLOCKING, f"slide_{slide_index + 1}", "slide index out of range"))
                continue
            slide = deck.slides[slide_index]
            notes = slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ""
            if required_text not in notes:
                findings.append(FidelityFinding(FidelityIssue.CONTENT_CHANGED, QaDimension.CONTENT_INTEGRITY, QaSeverity.BLOCKING, f"slide_{slide_index + 1}", "missing required speaker notes"))

    status = max((item.severity for item in findings), key=lambda item: _SEVERITY_ORDER[item], default=QaSeverity.ACCEPTABLE)
    return FidelityQaReport(status, tuple(findings), False)


__all__ = [
    "ERROR_FIDELITY_QA_INVALID", "ElementSnapshot", "FidelityFinding", "FidelityIssue",
    "FidelityQaError", "FidelityQaReport", "FidelityRepairResult", "QaDimension",
    "QaSeverity", "check_composite_conflicts", "compare_fidelity",
    "safe_representation_fallback", "verify_pptx_package",
]
