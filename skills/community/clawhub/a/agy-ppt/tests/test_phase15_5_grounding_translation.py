"""Deterministic tests for the additive Phase 15.5 grounding adapter."""
from __future__ import annotations

from dataclasses import FrozenInstanceError
import hashlib
import sys
import unittest

sys.path.insert(0, "skills/agy-ppt/scripts")
sys.path.insert(0, "skills/agy-ppt/tests")

from helpers.fake_ocr_provider import FakeOCRProvider
from image_ocr import ImagePreparationProvenance, ImageSourceIdentity, StandaloneImageOCRResult
from ocr_grounding import (
    GroundingTranslationError, translate_mixed_pdf, translate_pdf_ocr_page,
    translate_pdf_text_page, translate_standalone_image,
)
from ocr_providers import OCRRequest
from pdf_ocr import PDFPageIdentity, PDFSourceIdentity, OCRPageExecution, TextPageExecution, MixedPDFExecutionResult


PDF_RAW = b"%PDF-1.7 phase15.5"
PDF_DIGEST = hashlib.sha256(PDF_RAW).hexdigest()
PDF_SOURCE = PDFSourceIdentity("src_pdf", PDF_DIGEST)
IMAGE_RAW = b"standalone-image-bytes"
IMAGE_DIGEST = hashlib.sha256(IMAGE_RAW).hexdigest()


class _Provenance:
    def __init__(self, value: str):
        self.value = value

    def to_dict(self):
        return {"kind": self.value}


def pdf_evidence(page: PDFPageIdentity, text: str):
    provider = FakeOCRProvider(provider_id="tesseract", text=text)
    evidence = provider.recognize(OCRRequest(b"prepared-png", PDF_SOURCE.source_id, PDF_SOURCE.source_digest, page.to_dict()))
    provider.calls.clear()
    return evidence, provider


def mixed_result(texts: tuple[str, ...]):
    pages = []
    for number, text in enumerate(texts, 1):
        page = PDFPageIdentity(number, len(texts))
        if text:
            pages.append(TextPageExecution(PDF_SOURCE, page, text))
        else:
            evidence, _ = pdf_evidence(page, f"ocr-{number}")
            pages.append(OCRPageExecution(PDF_SOURCE, page, evidence, _Provenance(f"raster-{number}")))
    return MixedPDFExecutionResult(PDF_SOURCE, tuple(pages))


class TranslationTests(unittest.TestCase):
    def test_pdf_page_mapping_preserves_identity_and_mechanical_locator(self):
        page = PDFPageIdentity(2, 3)
        evidence, _ = pdf_evidence(page, "  raw\nOCR  ")
        translated = translate_pdf_ocr_page(PDF_SOURCE, page, evidence, _Provenance("raster"))
        self.assertEqual(translated.locator, {"kind": "page", "start": 2, "end": 2})
        self.assertEqual(translated.native_locator, page.to_dict())
        self.assertEqual(translated.text, "  raw\nOCR  ")
        self.assertEqual(translated.source_digest, PDF_DIGEST)
        self.assertIs(translated.ocr_evidence, evidence)

    def test_text_page_never_fabricates_ocr_evidence(self):
        translated = translate_pdf_text_page(PDF_SOURCE, PDFPageIdentity(1, 1), "\n exact Unicode — text \n")
        self.assertEqual(translated.route, "TEXT")
        self.assertIsNone(translated.ocr_evidence)
        self.assertEqual(translated.text, "\n exact Unicode — text \n")

    def test_mixed_pdf_is_source_ordered_and_keeps_one_source_identity(self):
        translated = translate_mixed_pdf(mixed_result(("search", "", "text", "")), PDF_RAW)
        self.assertEqual([page.locator for page in translated.pages], [
            {"kind": "page", "start": 1, "end": 1},
            {"kind": "page", "start": 2, "end": 2},
            {"kind": "page", "start": 3, "end": 3},
            {"kind": "page", "start": 4, "end": 4},
        ])
        self.assertEqual([page.route for page in translated.pages], ["TEXT", "OCR", "TEXT", "OCR"])
        self.assertEqual({page.source_digest for page in translated.pages}, {PDF_DIGEST})
        self.assertEqual(translated.pages[1].derived_provenance.to_dict(), {"kind": "raster-2"})

    def test_image_maps_to_existing_generic_locator_without_digest_substitution(self):
        provider = FakeOCRProvider(provider_id="tesseract", text="image OCR")
        evidence = provider.recognize(OCRRequest(b"prepared", "src_image", IMAGE_DIGEST, {"kind": "image", "ordinal": 1}))
        preparation = ImagePreparationProvenance(
            "Pillow", "10.0", "PNG", 4, 3, "RGBA", 6, True, False,
            "composite_on_white", "rgba_to_rgb", "PNG", "RGB", 3, 4,
            hashlib.sha256(b"prepared").hexdigest(),
        )
        result = StandaloneImageOCRResult(ImageSourceIdentity("src_image", IMAGE_DIGEST), preparation, evidence)
        translated = translate_standalone_image(result, IMAGE_RAW)
        self.assertEqual(translated.locator, {"kind": "generic", "label": "image:1-of-1"})
        self.assertEqual(translated.native_locator, {"kind": "image", "ordinal": 1})
        self.assertEqual(translated.source_digest, IMAGE_DIGEST)
        self.assertNotEqual(translated.source_digest, preparation.prepared_image_digest)
        self.assertIs(translated.derived_provenance, preparation)

    def test_source_and_evidence_mismatches_fail_closed(self):
        page = PDFPageIdentity(1, 1)
        evidence, _ = pdf_evidence(page, "text")
        wrong_source = PDFSourceIdentity("src_other", "1" * 64)
        with self.assertRaises(GroundingTranslationError) as caught:
            translate_pdf_ocr_page(wrong_source, page, evidence)
        self.assertEqual(caught.exception.error_code, "OCR_GROUNDING_SOURCE_MISMATCH")

    def test_derived_digest_cannot_be_substituted_for_source_identity(self):
        page = PDFPageIdentity(1, 1)
        evidence, _ = pdf_evidence(page, "text")
        raster_digest = hashlib.sha256(b"derived-raster").hexdigest()
        substituted = PDFSourceIdentity("src_pdf", raster_digest)
        with self.assertRaises(GroundingTranslationError) as caught:
            translate_pdf_ocr_page(substituted, page, evidence, _Provenance("raster"))
        self.assertEqual(caught.exception.error_code, "OCR_GROUNDING_SOURCE_MISMATCH")
        with self.assertRaises(GroundingTranslationError) as caught:
            translate_mixed_pdf(mixed_result(("",)), b"wrong")
        self.assertEqual(caught.exception.error_code, "OCR_GROUNDING_SOURCE_MISMATCH")

    def test_locator_and_page_mismatches_fail_closed(self):
        page = PDFPageIdentity(1, 2)
        other_page = PDFPageIdentity(2, 2)
        evidence, _ = pdf_evidence(other_page, "wrong page")
        with self.assertRaises(GroundingTranslationError) as caught:
            translate_pdf_ocr_page(PDF_SOURCE, page, evidence)
        self.assertEqual(caught.exception.error_code, "OCR_GROUNDING_LOCATOR_INVALID")

    def test_invalid_image_ordinal_is_rejected_without_execution(self):
        provider = FakeOCRProvider(provider_id="tesseract")
        evidence = provider.recognize(OCRRequest(b"prepared", "src_image", IMAGE_DIGEST, {"kind": "image", "ordinal": 1}))
        object.__setattr__(evidence, "pages", (evidence.pages[0].__class__({"kind": "image", "ordinal": 2}, "x", ()),))
        with self.assertRaises(Exception):
            StandaloneImageOCRResult(ImageSourceIdentity("src_image", IMAGE_DIGEST), _prep(), evidence)
        self.assertEqual(provider.calls[-1].image_bytes, b"prepared")

    def test_raw_text_and_serialization_are_deterministic_and_immutable(self):
        first = translate_mixed_pdf(mixed_result((" lead\n\n終 ", "")), PDF_RAW)
        second = translate_mixed_pdf(mixed_result((" lead\n\n終 ", "")), PDF_RAW)
        self.assertEqual(first.to_json(), second.to_json())
        self.assertEqual(first.pages[0].text, " lead\n\n終 ")
        with self.assertRaises(FrozenInstanceError):
            first.pages = ()  # type: ignore[misc]
        with self.assertRaises(TypeError):
            first.pages[0].locator["start"] = 9  # type: ignore[index]

    def test_translation_has_zero_provider_raster_or_decoder_side_effects(self):
        provider = FakeOCRProvider(provider_id="tesseract")
        page = PDFPageIdentity(1, 1)
        evidence = provider.recognize(OCRRequest(b"prepared", PDF_SOURCE.source_id, PDF_SOURCE.source_digest, page.to_dict()))
        provider.calls.clear()
        translate_pdf_ocr_page(PDF_SOURCE, page, evidence)
        self.assertEqual(provider.calls, [])


def _prep():
    return ImagePreparationProvenance(
        "Pillow", "10.0", "PNG", 1, 1, "RGB", None, False, False,
        "composite_on_white", "preserve_rgb", "PNG", "RGB", 1, 1,
        hashlib.sha256(b"prepared").hexdigest(),
    )


if __name__ == "__main__":
    unittest.main()
