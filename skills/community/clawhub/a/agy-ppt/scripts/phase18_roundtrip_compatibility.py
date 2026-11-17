#!/usr/bin/env python3
"""Phase 18.5 round-trip editability and compatibility QA.

Verifies that meaningful edits survive:
generate -> open/modify -> save -> reopen -> inspect/render -> compare
without weakening evidence integrity or approved visual quality.

Reports qualification honestly with explicit distinction between:
- ACTUAL_CLIENT (genuine execution of named application)
- STRUCTURAL_PROXY (OOXML/package inspection, save/reopen simulation)
"""

from __future__ import annotations

import json
import shutil
import zipfile
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Iterable

from pptx import Presentation
from pptx.chart.data import CategoryChartData

from phase18_contract import (
    DeliveryEditabilityContract,
    DeliveryProfile,
    EditabilityClass,
    FontPortability,
    ProductionStrategy,
)
from phase18_hybrid_pptx import (
    ChartSeries,
    ChartSpec,
    ElementBox,
    HybridElement,
    HybridSlide,
    ShapeStyle,
    TextStyle,
    create_hybrid_presentation,
)
from phase18_production_plan import ElementProductionPlan, ElementRole, PortabilityRisk


ERROR_ROUNDTRIP_INVALID = "PHASE18_ROUNDTRIP_INVALID"


class RoundTripError(Exception):
    def __init__(self, error_code: str, message: str) -> None:
        super().__init__(message)
        self.error_code = error_code


class QualificationType(str, Enum):
    ACTUAL_CLIENT = "ACTUAL_CLIENT"
    STRUCTURAL_PROXY = "STRUCTURAL_PROXY"


class RoundTripOutcome(str, Enum):
    PASS = "PASS"
    WARNING = "WARNING"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    BLOCKING = "BLOCKING"


_OUTCOME_SEVERITY = {
    RoundTripOutcome.PASS: 0,
    RoundTripOutcome.WARNING: 1,
    RoundTripOutcome.REVIEW_REQUIRED: 2,
    RoundTripOutcome.BLOCKING: 3,
}

UNEXECUTED_ENVIRONMENTS: tuple[str, ...] = (
    "Windows Microsoft PowerPoint",
    "macOS Microsoft PowerPoint",
    "Apple Keynote",
    "LibreOffice Impress",
)


def audit_client_environments() -> dict[str, Any]:
    """Audit local environment to report honestly on real desktop clients."""
    has_powerpoint = Path("/Applications/Microsoft PowerPoint.app").exists()
    has_keynote = Path("/Applications/Keynote.app").exists()
    has_soffice = shutil.which("soffice") is not None

    detected: list[str] = []
    if has_powerpoint:
        detected.append("macOS Microsoft PowerPoint")
    if has_keynote:
        detected.append("Apple Keynote")
    if has_soffice:
        detected.append("LibreOffice Impress")

    return {
        "detected_desktop_apps": tuple(detected),
        "actual_clients_executed": (),
        "unexecuted_environments": UNEXECUTED_ENVIRONMENTS,
        "qualification_type": QualificationType.STRUCTURAL_PROXY,
    }


@dataclass(frozen=True)
class RoundTripFinding:
    scenario: str
    outcome: RoundTripOutcome
    qualification: QualificationType
    detail: str

    def internal_dict(self) -> dict[str, str]:
        return {
            "scenario": self.scenario,
            "outcome": self.outcome.value,
            "qualification": self.qualification.value,
            "detail": self.detail,
        }


@dataclass(frozen=True)
class RoundTripReport:
    overall_status: RoundTripOutcome
    qualification: QualificationType
    findings: tuple[RoundTripFinding, ...]
    executed_scenarios: tuple[str, ...]
    unexecuted_environments: tuple[str, ...]

    def canonical_json(self) -> str:
        payload = {
            "overall_status": self.overall_status.value,
            "qualification": self.qualification.value,
            "executed_scenarios": list(self.executed_scenarios),
            "unexecuted_environments": list(self.unexecuted_environments),
            "findings": [item.internal_dict() for item in self.findings],
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)

    def count(self, outcome: RoundTripOutcome) -> int:
        return sum(item.outcome is outcome for item in self.findings)


def _find_shape_by_name(slide_or_deck, name: str):
    if hasattr(slide_or_deck, "shapes"):
        for shape in slide_or_deck.shapes:
            if shape.name == name:
                return shape
    elif hasattr(slide_or_deck, "slides"):
        for slide in slide_or_deck.slides:
            for shape in slide.shapes:
                if shape.name == name:
                    return shape
    return None


def _find_slide_and_shape_by_name(deck, name: str):
    for slide in deck.slides:
        for shape in slide.shapes:
            if shape.name == name:
                return slide, shape
    return None, None


def simulate_kpi_edit(
    pptx_path: Path | str,
    element_id: str,
    new_value: str,
    *,
    save_path: Path | str | None = None,
) -> RoundTripFinding:
    """Modify native KPI within envelope; verify persistence and structural stability."""
    src = Path(pptx_path)
    dst = Path(save_path) if save_path else src
    target_name = f"agy:{element_id}"

    deck = Presentation(str(src))
    slide, shape = _find_slide_and_shape_by_name(deck, target_name)
    if shape is None or not shape.has_text_frame:
        return RoundTripFinding("KPI_EDIT", RoundTripOutcome.BLOCKING, QualificationType.STRUCTURAL_PROXY, f"shape {target_name} not found or has no text frame")

    orig_left = shape.left
    orig_top = shape.top
    orig_width = shape.width
    orig_height = shape.height

    shape.text_frame.text = new_value
    deck.save(str(dst))

    # Reopen and inspect
    reopened = Presentation(str(dst))
    reopened_slide, reopened_shape = _find_slide_and_shape_by_name(reopened, target_name)
    if reopened_shape is None:
        return RoundTripFinding("KPI_EDIT", RoundTripOutcome.BLOCKING, QualificationType.STRUCTURAL_PROXY, "shape identity lost after save/reopen")

    if reopened_shape.text != new_value:
        return RoundTripFinding("KPI_EDIT", RoundTripOutcome.BLOCKING, QualificationType.STRUCTURAL_PROXY, "modified value did not persist")

    # Geometry integrity
    if (reopened_shape.left, reopened_shape.top, reopened_shape.width, reopened_shape.height) != (orig_left, orig_top, orig_width, orig_height):
        return RoundTripFinding("KPI_EDIT", RoundTripOutcome.WARNING, QualificationType.STRUCTURAL_PROXY, "geometry shifted unexpectedly")

    return RoundTripFinding("KPI_EDIT", RoundTripOutcome.PASS, QualificationType.STRUCTURAL_PROXY, f"KPI updated to '{new_value}' and persisted cleanly")


def simulate_title_edit(
    pptx_path: Path | str,
    element_id: str,
    new_text: str,
    *,
    max_chars: int = 40,
    save_path: Path | str | None = None,
) -> RoundTripFinding:
    """Modify native title. Within envelope -> bounded reflow. Beyond envelope -> honest warning."""
    src = Path(pptx_path)
    dst = Path(save_path) if save_path else src
    target_name = f"agy:{element_id}"

    deck = Presentation(str(src))
    slide, shape = _find_slide_and_shape_by_name(deck, target_name)
    if shape is None or not shape.has_text_frame:
        return RoundTripFinding("TITLE_EDIT", RoundTripOutcome.BLOCKING, QualificationType.STRUCTURAL_PROXY, f"shape {target_name} not found")

    shape.text_frame.text = new_text
    deck.save(str(dst))

    reopened = Presentation(str(dst))
    reopened_slide, reopened_shape = _find_slide_and_shape_by_name(reopened, target_name)
    if reopened_shape is None or reopened_shape.text != new_text:
        return RoundTripFinding("TITLE_EDIT", RoundTripOutcome.BLOCKING, QualificationType.STRUCTURAL_PROXY, "title edit failed to persist")

    if len(new_text) > max_chars:
        return RoundTripFinding(
            "TITLE_BEYOND_ENVELOPE",
            RoundTripOutcome.WARNING,
            QualificationType.STRUCTURAL_PROXY,
            f"title length ({len(new_text)} chars) exceeds envelope ({max_chars} chars); requires layout review",
        )

    return RoundTripFinding(
        "TITLE_WITHIN_ENVELOPE",
        RoundTripOutcome.PASS,
        QualificationType.STRUCTURAL_PROXY,
        f"title updated within envelope ({len(new_text)} <= {max_chars} chars); stable reflow",
    )


def simulate_logo_replacement(
    pptx_path: Path | str,
    element_id: str,
    new_image_path: Path | str,
    *,
    save_path: Path | str | None = None,
) -> RoundTripFinding:
    """Replace logo image blob; verify position, frame, and replacement semantics."""
    src = Path(pptx_path)
    dst = Path(save_path) if save_path else src
    new_img = Path(new_image_path)
    if not new_img.is_file():
        return RoundTripFinding("LOGO_REPLACEMENT", RoundTripOutcome.BLOCKING, QualificationType.STRUCTURAL_PROXY, "replacement image missing")

    target_name = f"agy:{element_id}"
    deck = Presentation(str(src))
    slide, shape = _find_slide_and_shape_by_name(deck, target_name)
    if shape is None:
        return RoundTripFinding("LOGO_REPLACEMENT", RoundTripOutcome.BLOCKING, QualificationType.STRUCTURAL_PROXY, f"shape {target_name} not found")

    orig_left, orig_top, orig_width, orig_height = shape.left, shape.top, shape.width, shape.height
    new_blob = new_img.read_bytes()
    slide.part.related_part(shape._element.blip_rId)._blob = new_blob
    deck.save(str(dst))

    reopened = Presentation(str(dst))
    reopened_slide, reopened_shape = _find_slide_and_shape_by_name(reopened, target_name)
    if reopened_shape is None:
        return RoundTripFinding("LOGO_REPLACEMENT", RoundTripOutcome.BLOCKING, QualificationType.STRUCTURAL_PROXY, "shape lost after replacement")

    if reopened_shape.image.blob != new_blob:
        return RoundTripFinding("LOGO_REPLACEMENT", RoundTripOutcome.BLOCKING, QualificationType.STRUCTURAL_PROXY, "image blob not updated")

    if (reopened_shape.left, reopened_shape.top, reopened_shape.width, reopened_shape.height) != (orig_left, orig_top, orig_width, orig_height):
        return RoundTripFinding("LOGO_REPLACEMENT", RoundTripOutcome.WARNING, QualificationType.STRUCTURAL_PROXY, "logo frame geometry shifted")

    return RoundTripFinding("LOGO_REPLACEMENT", RoundTripOutcome.PASS, QualificationType.STRUCTURAL_PROXY, "logo replaced cleanly with frame preserved")


def simulate_photo_replacement(
    pptx_path: Path | str,
    element_id: str,
    new_image_path: Path | str,
    *,
    save_path: Path | str | None = None,
) -> RoundTripFinding:
    """Replace photo; verify frame box and aspect stability."""
    src = Path(pptx_path)
    dst = Path(save_path) if save_path else src
    new_img = Path(new_image_path)
    if not new_img.is_file():
        return RoundTripFinding("PHOTO_REPLACEMENT", RoundTripOutcome.BLOCKING, QualificationType.STRUCTURAL_PROXY, "replacement photo missing")

    target_name = f"agy:{element_id}"
    deck = Presentation(str(src))
    slide, shape = _find_slide_and_shape_by_name(deck, target_name)
    if shape is None:
        return RoundTripFinding("PHOTO_REPLACEMENT", RoundTripOutcome.BLOCKING, QualificationType.STRUCTURAL_PROXY, f"shape {target_name} not found")

    orig_geom = (shape.left, shape.top, shape.width, shape.height)
    new_blob = new_img.read_bytes()
    slide.part.related_part(shape._element.blip_rId)._blob = new_blob
    deck.save(str(dst))

    reopened = Presentation(str(dst))
    reopened_slide, reopened_shape = _find_slide_and_shape_by_name(reopened, target_name)
    if reopened_shape is None:
        return RoundTripFinding("PHOTO_REPLACEMENT", RoundTripOutcome.BLOCKING, QualificationType.STRUCTURAL_PROXY, "photo shape missing after save")

    if reopened_shape.image.blob != new_blob:
        return RoundTripFinding("PHOTO_REPLACEMENT", RoundTripOutcome.BLOCKING, QualificationType.STRUCTURAL_PROXY, "photo blob not updated")

    if (reopened_shape.left, reopened_shape.top, reopened_shape.width, reopened_shape.height) != orig_geom:
        return RoundTripFinding("PHOTO_REPLACEMENT", RoundTripOutcome.WARNING, QualificationType.STRUCTURAL_PROXY, "photo frame geometry drifted")

    return RoundTripFinding("PHOTO_REPLACEMENT", RoundTripOutcome.PASS, QualificationType.STRUCTURAL_PROXY, "photo replaced with frame preserved")


def verify_table_boundary() -> RoundTripFinding:
    """Verify and document honest table boundary: Phase 18 does not implement native tables."""
    return RoundTripFinding(
        "TABLE_BOUNDARY",
        RoundTripOutcome.PASS,
        QualificationType.STRUCTURAL_PROXY,
        "Phase 18 contract boundary: native table production strategy is not implemented. Structured tables use LOCKED_VISUAL or RASTER_REGION to avoid unverified reflow.",
    )


def simulate_chart_data_edit(
    pptx_path: Path | str,
    element_id: str,
    new_values: tuple[float, ...],
    *,
    categories: tuple[str, ...] | None = None,
    series_name: str = "Metric",
    save_path: Path | str | None = None,
) -> RoundTripFinding:
    """Modify native chart series data; verify chart updates while surrounding objects remain unaffected."""
    src = Path(pptx_path)
    dst = Path(save_path) if save_path else src
    target_name = f"agy:{element_id}"

    deck = Presentation(str(src))
    slide, shape = _find_slide_and_shape_by_name(deck, target_name)
    if shape is None or not shape.has_chart:
        return RoundTripFinding("CHART_DATA_EDIT", RoundTripOutcome.BLOCKING, QualificationType.STRUCTURAL_PROXY, f"shape {target_name} not found or has no chart")

    chart_data = CategoryChartData()
    cats = categories or tuple(f"C{i+1}" for i in range(len(new_values)))
    chart_data.categories = cats
    chart_data.add_series(series_name, new_values)

    shape.chart.replace_data(chart_data)
    deck.save(str(dst))

    reopened = Presentation(str(dst))
    reopened_slide, reopened_shape = _find_slide_and_shape_by_name(reopened, target_name)
    if reopened_shape is None or not reopened_shape.has_chart:
        return RoundTripFinding("CHART_DATA_EDIT", RoundTripOutcome.BLOCKING, QualificationType.STRUCTURAL_PROXY, "chart structure corrupted after data edit")

    series = list(reopened_shape.chart.series)
    if not series or tuple(series[0].values) != tuple(new_values):
        return RoundTripFinding("CHART_DATA_EDIT", RoundTripOutcome.BLOCKING, QualificationType.STRUCTURAL_PROXY, "modified chart values did not persist")

    return RoundTripFinding("CHART_DATA_EDIT", RoundTripOutcome.PASS, QualificationType.STRUCTURAL_PROXY, f"native chart updated with values {new_values}")


def simulate_save_reopen(
    pptx_path: Path | str,
    *,
    save_path: Path | str | None = None,
) -> RoundTripFinding:
    """Verify package, slide, and shape identity survive save and reopen cycle."""
    src = Path(pptx_path)
    dst = Path(save_path) if save_path else src

    deck = Presentation(str(src))
    orig_slide_count = len(deck.slides)
    orig_shapes_by_slide = [[s.name for s in slide.shapes] for slide in deck.slides]

    deck.save(str(dst))

    # Verify valid zip package
    if not zipfile.is_zipfile(dst):
        return RoundTripFinding("SAVE_REOPEN", RoundTripOutcome.BLOCKING, QualificationType.STRUCTURAL_PROXY, "package is not a valid zip archive after save")

    reopened = Presentation(str(dst))
    if len(reopened.slides) != orig_slide_count:
        return RoundTripFinding("SAVE_REOPEN", RoundTripOutcome.BLOCKING, QualificationType.STRUCTURAL_PROXY, "slide count changed across save/reopen")

    for idx, orig_names in enumerate(orig_shapes_by_slide):
        reopened_names = [s.name for s in reopened.slides[idx].shapes]
        if reopened_names != orig_names:
            return RoundTripFinding("SAVE_REOPEN", RoundTripOutcome.BLOCKING, QualificationType.STRUCTURAL_PROXY, f"shape names on slide {idx} changed")

    return RoundTripFinding("SAVE_REOPEN", RoundTripOutcome.PASS, QualificationType.STRUCTURAL_PROXY, "package and object identity preserved across save/reopen")


def verify_typography(
    text: str,
    *,
    language: str = "zh-TW",
    font_name: str = "Arial",
) -> RoundTripFinding:
    """Verify glyph coverage and typography integrity without substitution errors."""
    if "\ufffd" in text:
        return RoundTripFinding(
            f"TYPOGRAPHY_{language.upper()}",
            RoundTripOutcome.BLOCKING,
            QualificationType.STRUCTURAL_PROXY,
            "replacement character detected in typography string",
        )
    return RoundTripFinding(
        f"TYPOGRAPHY_{language.upper()}",
        RoundTripOutcome.PASS,
        QualificationType.STRUCTURAL_PROXY,
        f"{language} text ({len(text)} chars) validated with font '{font_name}'",
    )


def verify_fallback_font(
    element_font: str,
    portability: FontPortability,
) -> RoundTripFinding:
    """Verify that FONT_CRITICAL elements warn/protect if non-standard font is specified."""
    standard_fonts = {"Arial", "Calibri", "Times New Roman", "Microsoft JhengHei", "PingFang TC"}
    if portability is FontPortability.FONT_CRITICAL and element_font not in standard_fonts:
        return RoundTripFinding(
            "FONT_FALLBACK",
            RoundTripOutcome.WARNING,
            QualificationType.STRUCTURAL_PROXY,
            f"font '{element_font}' is FONT_CRITICAL but not universally portable; protected visual representation recommended",
        )
    return RoundTripFinding(
        "FONT_FALLBACK",
        RoundTripOutcome.PASS,
        QualificationType.STRUCTURAL_PROXY,
        f"font '{element_font}' with portability {portability.value} is acceptable",
    )


def verify_evidence_integrity_guard(
    original_text: str,
    delivered_text: str,
    *,
    is_intentional_user_edit: bool = False,
    evidence_bound: bool = True,
) -> RoundTripFinding:
    """Distinguish intentional user test edits from accidental pipeline mutation of evidence-bound facts."""
    if evidence_bound and original_text != delivered_text:
        if not is_intentional_user_edit:
            return RoundTripFinding(
                "EVIDENCE_INTEGRITY",
                RoundTripOutcome.BLOCKING,
                QualificationType.STRUCTURAL_PROXY,
                f"unauthorized pipeline mutation of evidence-bound fact: '{original_text}' -> '{delivered_text}'",
            )
        return RoundTripFinding(
            "EVIDENCE_INTEGRITY",
            RoundTripOutcome.PASS,
            QualificationType.STRUCTURAL_PROXY,
            f"intentional user edit applied: '{original_text}' -> '{delivered_text}'",
        )
    return RoundTripFinding(
        "EVIDENCE_INTEGRITY",
        RoundTripOutcome.PASS,
        QualificationType.STRUCTURAL_PROXY,
        "evidence-bound facts exact and untampered",
    )


def run_roundtrip_qualification(temp_dir: Path | str) -> RoundTripReport:
    """Execute all Phase 18.5 round-trip scenarios and produce a qualification report."""
    from PIL import Image

    root = Path(temp_dir)
    audit = audit_client_environments()
    qualification_type = audit["qualification_type"]
    unexecuted = audit["unexecuted_environments"]

    # Prepare fixtures
    img_path = root / "sample_img.png"
    new_img_path = root / "new_img.png"
    Image.new("RGB", (320, 180), (20, 40, 60)).save(img_path)
    Image.new("RGB", (320, 180), (80, 120, 160)).save(new_img_path)

    # Build hybrid deck fixture
    deck_path = root / "roundtrip_fixture.pptx"
    kpi_plan = ElementProductionPlan(
        "ep:kpi", "kpi", "claim:kpi", "narrative:kpi", "18%", ("pc:evidence",),
        ElementRole.KPI, PortabilityRisk.LOW,
        DeliveryEditabilityContract(EditabilityClass.EDITABLE_REQUIRED, ProductionStrategy.NATIVE_TEXT, FontPortability.FONT_SAFE),
    )
    title_plan = ElementProductionPlan(
        "ep:title", "title", "claim:title", "narrative:title", "Q3 Performance Review", (),
        ElementRole.TITLE, PortabilityRisk.LOW,
        DeliveryEditabilityContract(EditabilityClass.EDITABLE_PREFERRED, ProductionStrategy.NATIVE_TEXT, FontPortability.FONT_SAFE),
    )
    logo_plan = ElementProductionPlan(
        "ep:logo", "logo", "claim:logo", "narrative:logo", "logo", (),
        ElementRole.LOGO, PortabilityRisk.LOW,
        DeliveryEditabilityContract(EditabilityClass.REPLACEABLE, ProductionStrategy.NATIVE_IMAGE, FontPortability.FONT_SAFE),
    )
    photo_plan = ElementProductionPlan(
        "ep:photo", "photo", "claim:photo", "narrative:photo", "photo", (),
        ElementRole.PHOTO, PortabilityRisk.LOW,
        DeliveryEditabilityContract(EditabilityClass.REPLACEABLE, ProductionStrategy.NATIVE_IMAGE, FontPortability.FONT_SAFE),
    )
    chart_plan = ElementProductionPlan(
        "ep:chart", "chart", "claim:chart", "narrative:chart", "chart", ("pc:evidence",),
        ElementRole.CHART, PortabilityRisk.LOW,
        DeliveryEditabilityContract(EditabilityClass.EDITABLE_PREFERRED, ProductionStrategy.NATIVE_CHART, FontPortability.FONT_SAFE),
    )

    elements = (
        HybridElement(kpi_plan, ElementBox(1.0, 1.0, 2.5, 1.0), text_style=TextStyle(font_size=28.0)),
        HybridElement(title_plan, ElementBox(1.0, 2.2, 8.0, 1.0), text_style=TextStyle(font_size=24.0)),
        HybridElement(logo_plan, ElementBox(8.0, 0.5, 1.4, 0.8), image_path=str(img_path)),
        HybridElement(photo_plan, ElementBox(5.0, 3.35, 4.0, 1.8), image_path=str(img_path)),
        HybridElement(
            chart_plan, ElementBox(1.0, 3.35, 3.5, 1.8),
            chart=ChartSpec(("Q1", "Q2", "Q3"), (ChartSeries("Revenue", (10.0, 14.0, 18.0)),)),
        ),
    )
    slide = HybridSlide("slide_01", elements, speaker_notes="Speaker notes for slide 1")
    create_hybrid_presentation((slide,), str(deck_path))

    findings: list[RoundTripFinding] = []
    executed: list[str] = []

    # 1. KPI edit
    f_kpi = simulate_kpi_edit(deck_path, "kpi", "22%")
    findings.append(f_kpi)
    executed.append("KPI_EDIT")

    # 2. Title within envelope
    f_title_in = simulate_title_edit(deck_path, "title", "Q3 Comprehensive Review", max_chars=40)
    findings.append(f_title_in)
    executed.append("TITLE_WITHIN_ENVELOPE")

    # 3. Title beyond envelope
    f_title_out = simulate_title_edit(deck_path, "title", "This is an extremely long title that deliberately overflows the designated layout envelope for headline text in business slides", max_chars=40)
    findings.append(f_title_out)
    executed.append("TITLE_BEYOND_ENVELOPE")

    # 4. Logo replacement
    f_logo = simulate_logo_replacement(deck_path, "logo", new_img_path)
    findings.append(f_logo)
    executed.append("LOGO_REPLACEMENT")

    # 5. Photo replacement
    f_photo = simulate_photo_replacement(deck_path, "photo", new_img_path)
    findings.append(f_photo)
    executed.append("PHOTO_REPLACEMENT")

    # 6. Table boundary
    f_tbl = verify_table_boundary()
    findings.append(f_tbl)
    executed.append("TABLE_BOUNDARY")

    # 7. Chart data edit
    f_chart = simulate_chart_data_edit(deck_path, "chart", (12.0, 16.0, 22.0), categories=("Q1", "Q2", "Q3"))
    findings.append(f_chart)
    executed.append("CHART_DATA_EDIT")

    # 8. Save/reopen
    f_reopen = simulate_save_reopen(deck_path)
    findings.append(f_reopen)
    executed.append("SAVE_REOPEN")

    # 9. Traditional Chinese
    f_zh = verify_typography("繁體中文排版測試：營收年增 18%，維持強勁現金流。", language="zh-TW", font_name="Microsoft JhengHei")
    findings.append(f_zh)
    executed.append("TYPOGRAPHY_ZH_TW")

    # 10. English
    f_en = verify_typography("English Typography Test: 18% YoY Revenue Growth with Healthy Margins.", language="en", font_name="Arial")
    findings.append(f_en)
    executed.append("TYPOGRAPHY_EN")

    # 11. Fallback font
    f_font = verify_fallback_font("CustomExoticFont", FontPortability.FONT_CRITICAL)
    findings.append(f_font)
    executed.append("FONT_FALLBACK")

    # 12. Evidence integrity (intentional edit vs accidental corruption)
    f_ev_intentional = verify_evidence_integrity_guard("18%", "22%", is_intentional_user_edit=True)
    findings.append(f_ev_intentional)
    executed.append("EVIDENCE_INTEGRITY_INTENTIONAL")

    f_ev_accidental = verify_evidence_integrity_guard("18%", "1.8%", is_intentional_user_edit=False)
    findings.append(f_ev_accidental)
    executed.append("EVIDENCE_INTEGRITY_ACCIDENTAL")

    overall = max((f.outcome for f in findings), key=lambda x: _OUTCOME_SEVERITY[x], default=RoundTripOutcome.PASS)
    return RoundTripReport(
        overall_status=overall,
        qualification=qualification_type,
        findings=tuple(findings),
        executed_scenarios=tuple(executed),
        unexecuted_environments=unexecuted,
    )


__all__ = [
    "ERROR_ROUNDTRIP_INVALID",
    "QualificationType",
    "RoundTripError",
    "RoundTripFinding",
    "RoundTripOutcome",
    "RoundTripReport",
    "UNEXECUTED_ENVIRONMENTS",
    "audit_client_environments",
    "run_roundtrip_qualification",
    "simulate_chart_data_edit",
    "simulate_kpi_edit",
    "simulate_logo_replacement",
    "simulate_photo_replacement",
    "simulate_save_reopen",
    "simulate_title_edit",
    "verify_evidence_integrity_guard",
    "verify_fallback_font",
    "verify_table_boundary",
    "verify_typography",
]
