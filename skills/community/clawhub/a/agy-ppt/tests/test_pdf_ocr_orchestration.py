"""Focused deterministic tests for Phase 15.2-D mixed-PDF execution."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
import hashlib
import sys
import unittest

sys.path.insert(0, "skills/agy-ppt/scripts")
sys.path.insert(0, "skills/agy-ppt/tests")

from helpers.fake_ocr_provider import FakeOCRProvider
from helpers.fake_pdf_rasterizer import FakePDFRasterizer
from ocr_providers import (
    OCRProvider,
    OCRProviderCapabilities,
    OCRProviderMetadata,
    OCRProvenance,
    OCRPage,
    OCRRequest,
    OCREvidence,
)
from ocr_providers.errors import OCRError
from pdf_ocr import (
    MixedPDFExecutionResult,
    OCRPageExecution,
    PDFOCRError,
    PDFPageIdentity,
    PDFPageInput,
    PDFSourceIdentity,
    PageRoute,
    TextPageExecution,
    execute_mixed_pdf,
    plan_pdf_pages,
)


RAW = b"%PDF-1.7\nphase15.2-d-fixture"
SOURCE = PDFSourceIdentity("pdf-source", hashlib.sha256(RAW).hexdigest())


def plan(*texts: str):
    return plan_pdf_pages(
        PDFPageInput(SOURCE, PDFPageIdentity(index, len(texts)), text)
        for index, text in enumerate(texts, 1)
    )


def run(mixed, *, rasterizer=None, providers=None, **kwargs):
    rasterizer = rasterizer or FakePDFRasterizer()
    providers = providers or {"tesseract": FakeOCRProvider(provider_id="tesseract", text="ocr")}
    return execute_mixed_pdf(mixed, RAW, rasterizer, providers, **kwargs)


class PageFailRasterizer(FakePDFRasterizer):
    def __init__(self, page: int):
        super().__init__()
        self.fail_page = page

    def rasterize(self, request):
        if request.page.page == self.fail_page:
            self._calls.append(request)
            raise PDFOCRError("page failure", "OCR_RASTERIZATION_FAILED")
        return super().rasterize(request)


class BadEvidenceProvider(OCRProvider):
    provider_id = "bad"
    provider_version = "1.0"
    capabilities = OCRProviderCapabilities(True, True, "local", False)

    def recognize(self, request: OCRRequest) -> OCREvidence:
        return OCREvidence(
            "1.0", request.source_id, request.source_digest,
            (OCRPage({"kind": "page", "page": 99, "total_pages": 99}, "bad", ()),),
            self.capabilities, OCRProviderMetadata(self.provider_id, self.provider_version),
            OCRProvenance(self.provider_id, self.provider_id, "local", False),
        )


class OrchestrationTests(unittest.TestCase):
    def test_all_searchable_preserves_text_and_does_not_render_or_ocr(self):
        rasterizer = FakePDFRasterizer()
        provider = FakeOCRProvider(provider_id="tesseract")
        result = run(plan(" page 1 ", "page 2", "\tpage 3\n"), rasterizer=rasterizer, providers={"tesseract": provider})
        self.assertEqual([page.route for page in result.pages], [PageRoute.TEXT] * 3)
        self.assertEqual([page.raw_text for page in result.pages], [" page 1 ", "page 2", "\tpage 3\n"])
        self.assertEqual(rasterizer.calls, ())
        self.assertEqual(provider.calls, [])

    def test_all_scanned_renders_and_ocr_once_per_page(self):
        rasterizer = FakePDFRasterizer()
        provider = FakeOCRProvider(provider_id="tesseract", text="raw OCR")
        result = run(plan("", "\n", "   "), rasterizer=rasterizer, providers={"tesseract": provider})
        self.assertEqual([page.route for page in result.pages], [PageRoute.OCR] * 3)
        self.assertEqual(len(rasterizer.calls), 3)
        self.assertEqual(len(provider.calls), 3)
        self.assertEqual([page.raw_text for page in result.pages], ["raw OCR"] * 3)
        self.assertTrue(all(page.raster_provenance.raster_digest != SOURCE.source_digest for page in result.pages))
        self.assertTrue(all(request.source_digest == SOURCE.source_digest for request in provider.calls))

    def test_mixed_pages_are_source_ordered_and_routes_are_independent(self):
        rasterizer = FakePDFRasterizer()
        provider = FakeOCRProvider(provider_id="tesseract", text="OCR page")
        result = run(plan("searchable", "", "text", "\u2003"), rasterizer=rasterizer, providers={"tesseract": provider})
        self.assertEqual([page.page.page for page in result.pages], [1, 2, 3, 4])
        self.assertEqual([page.route for page in result.pages], [PageRoute.TEXT, PageRoute.OCR, PageRoute.TEXT, PageRoute.OCR])
        self.assertEqual([request.page.page for request in rasterizer.calls], [2, 4])
        self.assertEqual([request.locator["page"] for request in provider.calls], [2, 4])
        self.assertEqual(result.pages[0].raw_text, "searchable")
        self.assertEqual(result.pages[2].raw_text, "text")

    def test_source_identity_is_original_pdf_digest_not_raster_digest(self):
        provider = FakeOCRProvider(provider_id="tesseract")
        result = run(plan(""), providers={"tesseract": provider})
        page = result.pages[0]
        self.assertIsInstance(page, OCRPageExecution)
        self.assertEqual(page.source.source_digest, hashlib.sha256(RAW).hexdigest())
        self.assertEqual(page.evidence.source_digest, page.source.source_digest)
        self.assertNotEqual(page.raster_provenance.raster_digest, page.source.source_digest)

    def test_first_middle_and_final_failures_fail_closed_and_stop(self):
        for failed_page in (1, 2, 3):
            with self.subTest(failed_page=failed_page):
                rasterizer = PageFailRasterizer(failed_page)
                provider = FakeOCRProvider(provider_id="tesseract")
                with self.assertRaises(PDFOCRError) as caught:
                    run(plan("", "", ""), rasterizer=rasterizer, providers={"tesseract": provider})
                self.assertEqual(caught.exception.error_code, "OCR_RASTERIZATION_FAILED")
                self.assertNotIsInstance(caught.exception, MixedPDFExecutionResult)
                self.assertEqual([request.page.page for request in rasterizer.calls], list(range(1, failed_page + 1)))
                self.assertEqual([request.locator["page"] for request in provider.calls], list(range(1, failed_page)))

    def test_renderer_failure_never_calls_provider_or_fallback(self):
        primary = FakeOCRProvider(provider_id="primary")
        fallback = FakeOCRProvider(provider_id="tesseract")
        rasterizer = FakePDFRasterizer(fail_code="OCR_PDF_RESOURCE_LIMIT_EXCEEDED")
        with self.assertRaises(PDFOCRError) as caught:
            run(plan(""), rasterizer=rasterizer, providers={"primary": primary, "tesseract": fallback}, explicit="primary", allow_fallback=True)
        self.assertEqual(caught.exception.error_code, "OCR_PDF_RESOURCE_LIMIT_EXCEEDED")
        self.assertEqual(primary.calls, [])
        self.assertEqual(fallback.calls, [])

    def test_provider_fallback_reuses_frozen_per_invocation_semantics(self):
        primary = FakeOCRProvider(provider_id="primary", fail_code="OCR_PROVIDER_UNAVAILABLE")
        fallback = FakeOCRProvider(provider_id="tesseract", text="fallback")
        result = run(plan(""), providers={"primary": primary, "tesseract": fallback}, explicit="primary", allow_fallback=True)
        self.assertEqual(result.pages[0].raw_text, "fallback")
        self.assertEqual(len(primary.calls), 1)
        self.assertEqual(len(fallback.calls), 1)
        self.assertTrue(result.pages[0].evidence.provenance.fallback_used)

    def test_terminal_provider_failure_and_disabled_fallback_are_not_broadened(self):
        for code, allow in (("OCR_PROVIDER_OUTPUT_INVALID", False), ("OCR_PROVIDER_CONTRACT_INVALID", True)):
            with self.subTest(code=code, allow=allow):
                primary = FakeOCRProvider(provider_id="primary", fail_code=code)
                fallback = FakeOCRProvider(provider_id="tesseract")
                with self.assertRaises(OCRError) as caught:
                    run(plan(""), providers={"primary": primary, "tesseract": fallback}, explicit="primary", allow_fallback=allow)
                self.assertEqual(caught.exception.error_code, code if allow else "OCR_FALLBACK_NOT_ALLOWED")
                self.assertEqual(fallback.calls, [])

    def test_evidence_identity_violation_fails_without_repair(self):
        with self.assertRaises(OCRError) as caught:
            run(plan(""), providers={"bad": BadEvidenceProvider()}, explicit="bad")
        self.assertEqual(caught.exception.error_code, "OCR_PROVIDER_CONTRACT_INVALID")

    def test_result_serialization_is_deterministic_and_models_are_frozen(self):
        first = run(plan("text", ""), providers={"tesseract": FakeOCRProvider(provider_id="tesseract")})
        second = run(plan("text", ""), providers={"tesseract": FakeOCRProvider(provider_id="tesseract")})
        self.assertEqual(first.to_json(), second.to_json())
        self.assertIsInstance(first.pages, tuple)
        with self.assertRaises(FrozenInstanceError):
            first.pages = ()  # type: ignore[misc]
        self.assertIsInstance(first.pages[0], TextPageExecution)

    def test_invalid_raw_source_digest_fails_before_page_execution(self):
        bad_source = PDFSourceIdentity("pdf-source", "0" * 64)
        bad_plan = plan_pdf_pages((PDFPageInput(bad_source, PDFPageIdentity(1, 1), ""),))
        rasterizer = FakePDFRasterizer()
        with self.assertRaises(PDFOCRError) as caught:
            execute_mixed_pdf(bad_plan, RAW, rasterizer, {"tesseract": FakeOCRProvider(provider_id="tesseract")})
        self.assertEqual(caught.exception.error_code, "OCR_PDF_INPUT_INVALID")
        self.assertEqual(rasterizer.calls, ())


if __name__ == "__main__":
    unittest.main()
