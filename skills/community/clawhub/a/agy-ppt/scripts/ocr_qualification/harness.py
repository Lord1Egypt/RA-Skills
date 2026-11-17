"""Phase 15.6 end-to-end contract and opt-in live qualification."""
from __future__ import annotations

from dataclasses import asdict
import hashlib
import platform
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from PIL import __version__ as pillow_version
from pypdfium2.version import PDFIUM_INFO, PYPDFIUM_INFO

from image_ocr import PillowImagePreparer, execute_standalone_image_ocr
from ocr_grounding import translate_mixed_pdf, translate_standalone_image
from ocr_providers import (
    OCREvidence, OCRPage, OCRProvider, OCRProviderCapabilities, OCRProviderMetadata,
    OCRProvenance, OCRRequest, TesseractProvider,
)
from pdf_ocr import PDFPageIdentity, PDFPageInput, PDFSourceIdentity, execute_mixed_pdf, plan_pdf_pages
from pdf_ocr.pdfium_identity import ENGINE_BUILD, ENGINE_ORIGIN, ENGINE_VERSION, RENDERER_VERSION, load_approved_artifact
from pdf_ocr.pdfium_rasterizer import PDFiumRasterizer
from source_grounding import SourceInventory, compute_source_digest, validate_source_inventory

from .fixtures import image_fixture, pdf_fixture
from .models import QualificationCase, QualificationReport


class _ContractProvider(OCRProvider):
    provider_id = "phase15-qualification-fake"
    provider_version = "1.0"
    capabilities = OCRProviderCapabilities(True, True, "local", False)

    def __init__(self) -> None:
        self.calls: list[OCRRequest] = []

    def recognize(self, request: OCRRequest) -> OCREvidence:
        self.calls.append(request)
        locator = dict(request.locator)
        ordinal = locator.get("page", locator.get("ordinal"))
        raw_text = f"qualification OCR {locator['kind']} {ordinal}\n"
        evidence = OCREvidence(
            "1.0", request.source_id, request.source_digest,
            (OCRPage(locator, raw_text, ()),), self.capabilities,
            OCRProviderMetadata(self.provider_id, self.provider_version),
            OCRProvenance(self.provider_id, self.provider_id, "local", False, selection_origin="explicit"),
            language_config=request.language_config, execution_config=request.execution_config,
        )
        evidence.validate()
        return evidence


def _runtime() -> tuple[dict[str, Any], dict[str, Any], tuple[str, ...]]:
    artifact = load_approved_artifact()
    if str(PYPDFIUM_INFO) != RENDERER_VERSION or str(PDFIUM_INFO) != ENGINE_VERSION:
        raise RuntimeError("PDFium runtime identity is not approved")
    if PDFIUM_INFO.build != ENGINE_BUILD or PDFIUM_INFO.origin != ENGINE_ORIGIN or tuple(PDFIUM_INFO.flags):
        raise RuntimeError("PDFium build identity or flags are not approved")
    system = platform.system()
    machine = platform.machine().lower()
    if system == "Linux" and machine in {"x86_64", "amd64"}:
        platform_state = "PRODUCTION CANDIDATE / DEPLOYMENT ENVIRONMENT VALIDATION REQUIRED"
    elif system == "Darwin":
        platform_state = "DEVELOPMENT / API QUALIFIED"
    else:
        platform_state = "PACKAGE COMPATIBLE / PRODUCTION SECURITY NOT QUALIFIED"
    runtime = {
        "pdfium_build": ENGINE_BUILD,
        "pdfium_flags": [],
        "pdfium_origin": ENGINE_ORIGIN,
        "pdfium_version": str(PDFIUM_INFO),
        "pillow_version": pillow_version,
        "pypdfium2_version": str(PYPDFIUM_INFO),
        "wheel_filename": artifact["filename"],
        "wheel_sha256": artifact["sha256"],
    }
    platform_result = {"architecture": machine, "classification": platform_state, "system": system}
    limitation = "Linux hard isolation requires deployment-environment validation"
    return runtime, platform_result, (limitation,)


def _ground(translated, source_type: str) -> dict[str, Any]:
    pages = translated.pages if hasattr(translated, "pages") else (translated,)
    with TemporaryDirectory(prefix="agy-phase15-qualification-") as directory:
        inventory = SourceInventory.initialize(directory, "phase15_6")
        inventory.add_source(pages[0].source_id, source_type, source_digest=pages[0].source_digest)
        unit_ids = []
        for page in pages:
            unit = inventory.add_unit(page.source_id, page.route.lower(), dict(page.locator), "MEDIUM")
            unit_ids.append(unit["unit_id"])
        errors = validate_source_inventory(inventory.data)
    if errors:
        raise RuntimeError("Phase 12 grounding envelope rejected qualification data")
    return {"locators": [dict(page.locator) for page in pages], "unit_ids": unit_ids}


def run_contract_qualification(*, baseline_sha: str) -> QualificationReport:
    """Exercise frozen production paths with project-owned synthetic sources."""
    runtime, platform_result, limitations = _runtime()
    cases: list[QualificationCase] = []

    scanned_raw = pdf_fixture(crop=True, rotation=90)
    scanned_source = PDFSourceIdentity("src_qualification_pdf", compute_source_digest(scanned_raw))
    scanned_plan = plan_pdf_pages((PDFPageInput(scanned_source, PDFPageIdentity(1, 1), ""),))
    scanned_provider = _ContractProvider()
    scanned_result = execute_mixed_pdf(scanned_plan, scanned_raw, PDFiumRasterizer(), {scanned_provider.provider_id: scanned_provider}, explicit=scanned_provider.provider_id)
    scanned_translation = translate_mixed_pdf(scanned_result, scanned_raw)
    scanned_grounding = _ground(scanned_translation, "pdf")
    cases.append(QualificationCase("pdf-scanned-e2e", "PASS", {
        "grounding": scanned_grounding,
        "raster_digest": scanned_result.pages[0].raster_provenance.raster_digest,
        "route": scanned_result.pages[0].route.value,
        "source_digest": scanned_source.source_digest,
    }))

    mixed_raw = pdf_fixture(pages=4)
    mixed_source = PDFSourceIdentity("src_qualification_mixed", compute_source_digest(mixed_raw))
    extracted = ("searchable page 1\n", "", "searchable page 3\n", "")
    mixed_plan = plan_pdf_pages(PDFPageInput(mixed_source, PDFPageIdentity(index, 4), text) for index, text in enumerate(extracted, 1))
    mixed_provider = _ContractProvider()
    mixed_result = execute_mixed_pdf(mixed_plan, mixed_raw, PDFiumRasterizer(), {mixed_provider.provider_id: mixed_provider}, explicit=mixed_provider.provider_id)
    mixed_translation = translate_mixed_pdf(mixed_result, mixed_raw)
    cases.append(QualificationCase("pdf-mixed-e2e", "PASS", {
        "grounding": _ground(mixed_translation, "pdf"),
        "ocr_calls": len(mixed_provider.calls),
        "routes": [page.route.value for page in mixed_result.pages],
        "source_digest": mixed_source.source_digest,
    }))

    preparer = PillowImagePreparer()
    for format_name, mode, orientation in (("PNG", "RGBA", None), ("JPEG", "RGB", 6), ("TIFF", "L", None)):
        raw = image_fixture(format_name, mode=mode, exif_orientation=orientation)
        provider = _ContractProvider()
        source_id = f"src_qualification_{format_name.lower()}"
        result = execute_standalone_image_ocr(raw, source_id, preparer, {provider.provider_id: provider}, explicit=provider.provider_id)
        translated = translate_standalone_image(result, raw)
        cases.append(QualificationCase(f"image-{format_name.lower()}-e2e", "PASS", {
            "grounding": _ground(translated, format_name.lower()),
            "orientation_applied": result.preparation.orientation_transform_applied,
            "prepared_digest": result.preparation.prepared_image_digest,
            "prepared_dimensions": [result.preparation.prepared_width, result.preparation.prepared_height],
            "source_digest": result.source.source_digest,
            "source_format": result.preparation.source_format,
        }))

    cases.sort(key=lambda case: case.case_id)
    return QualificationReport(
        "phase15.6-internal/1", baseline_sha, runtime, platform_result,
        tuple(cases), "RELEASE READY WITH DOCUMENTED PLATFORM LIMITATIONS", limitations,
    )


def run_live_tesseract_qualification(tessdata_dir: str | Path, *, language: str = "eng", baseline_sha: str) -> dict[str, Any]:
    """Opt-in real Tesseract qualification; never downloads language data."""
    provider = TesseractProvider(tessdata_dir=tessdata_dir)
    raw = image_fixture("PNG")
    result = execute_standalone_image_ocr(
        raw, "src_live_tesseract", PillowImagePreparer(), {"tesseract": provider},
        explicit="tesseract", language_config={"languages": (language,)},
    )
    translated = translate_standalone_image(result, raw)
    grounding = _ground(translated, "png")
    return {
        "baseline_sha": baseline_sha,
        "engine_version": result.evidence.provider.engine_version,
        "execution_location": result.evidence.provenance.execution_location,
        "grounding": grounding,
        "language_config": dict(result.evidence.language_config),
        "model_manifest": [dict(item) for item in result.evidence.model_manifest],
        "provider_id": result.evidence.provider.provider_id,
        "provider_version": result.evidence.provider.provider_version,
        "raw_text_present": bool(result.raw_text),
        "source_digest": result.source.source_digest,
        "status": "PASS",
    }
