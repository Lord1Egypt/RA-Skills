"""Focused deterministic tests for Phase 15.2-B classification and planning."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
import sys
import unittest

sys.path.insert(0, "skills/agy-ppt/scripts")
sys.path.insert(0, "skills/agy-ppt/tests")

from helpers.fake_ocr_provider import FakeOCRProvider
from helpers.fake_pdf_rasterizer import FakePDFRasterizer
from pdf_ocr import (
    MixedPDFPlan,
    PDFOCRError,
    PDFPageIdentity,
    PDFPageInput,
    PDFPagePlan,
    PDFSourceIdentity,
    PageClassification,
    PageRoute,
    classify_page_text,
    plan_pdf_pages,
)
from source_grounding import compute_source_digest


SOURCE = PDFSourceIdentity("source-1", compute_source_digest(b"%PDF-1.7\nsource one"))


def page(number: int, total: int, text: str, source: PDFSourceIdentity = SOURCE) -> PDFPageInput:
    return PDFPageInput(source, PDFPageIdentity(number, total), text)


class MechanicalClassifierTests(unittest.TestCase):
    def test_non_whitespace_is_searchable_without_quality_rules(self) -> None:
        values = ("a", ".", "123", "?", "x", "少", "文字與假想的大圖片")
        for text in values:
            with self.subTest(text=text):
                self.assertIs(classify_page_text(text), PageClassification.SEARCHABLE)

    def test_empty_and_unicode_whitespace_are_scanned(self) -> None:
        values = ("", " ", "\t", "\n", " \t\r\n ", "\u00a0", "\u2003", "\u3000")
        for text in values:
            with self.subTest(text=repr(text)):
                self.assertIs(classify_page_text(text), PageClassification.SCANNED)

    def test_leading_trailing_and_embedded_whitespace_do_not_change_text(self) -> None:
        values = ("  text", "text  ", "\ntext\n", "a\tb", "a\n\nb", "\u2003文\u3000")
        for text in values:
            with self.subTest(text=repr(text)):
                result = plan_pdf_pages((page(1, 1, text),))
                self.assertEqual(result.pages[0].extracted_text, text)
                self.assertEqual(result.to_dict()["pages"][0]["extracted_text"], text)

    def test_non_string_text_fails_closed(self) -> None:
        for value in (None, b"text", 1, True):
            with self.subTest(value=value), self.assertRaises(PDFOCRError) as caught:
                classify_page_text(value)  # type: ignore[arg-type]
            self.assertEqual(caught.exception.error_code, "OCR_PDF_INPUT_INVALID")


class MixedPDFPlanningTests(unittest.TestCase):
    def test_all_searchable_routes_to_text(self) -> None:
        plan = plan_pdf_pages((page(1, 3, "a"), page(2, 3, "."), page(3, 3, "123")))
        self.assertEqual(tuple(item.route for item in plan.pages), (PageRoute.TEXT,) * 3)

    def test_all_scanned_routes_to_ocr(self) -> None:
        plan = plan_pdf_pages((page(1, 3, ""), page(2, 3, "\t"), page(3, 3, "\u2003")))
        self.assertEqual(tuple(item.route for item in plan.pages), (PageRoute.OCR,) * 3)

    def test_mixed_plan_preserves_source_order_and_mapping(self) -> None:
        plan = plan_pdf_pages(
            (page(1, 4, "text"), page(2, 4, ""), page(3, 4, "?"), page(4, 4, " \n "))
        )
        self.assertEqual(tuple(item.page.page for item in plan.pages), (1, 2, 3, 4))
        self.assertEqual(tuple(item.route for item in plan.pages),
                         (PageRoute.TEXT, PageRoute.OCR, PageRoute.TEXT, PageRoute.OCR))
        self.assertEqual(tuple(item.classification for item in plan.pages),
                         (PageClassification.SEARCHABLE, PageClassification.SCANNED,
                          PageClassification.SEARCHABLE, PageClassification.SCANNED))

    def test_repeated_calls_and_serialization_are_identical(self) -> None:
        inputs = (page(1, 2, "text"), page(2, 2, ""))
        first = plan_pdf_pages(inputs)
        second = plan_pdf_pages(inputs)
        self.assertEqual(first, second)
        self.assertEqual(first.to_json(), second.to_json())

    def test_caller_owned_sequence_is_defensively_copied(self) -> None:
        inputs = [page(1, 2, "text"), page(2, 2, "")]
        plan = plan_pdf_pages(inputs)
        inputs.reverse()
        self.assertEqual(tuple(item.page.page for item in plan.pages), (1, 2))
        with self.assertRaises(FrozenInstanceError):
            plan.pages[0].extracted_text = "changed"  # type: ignore[misc]


class StructuralValidationTests(unittest.TestCase):
    def assert_plan_error(self, inputs: tuple[PDFPageInput, ...], code: str) -> None:
        with self.assertRaises(PDFOCRError) as caught:
            plan_pdf_pages(inputs)
        self.assertEqual(caught.exception.error_code, code)

    def test_empty_plan_is_rejected(self) -> None:
        self.assert_plan_error((), "OCR_PDF_INPUT_INVALID")

    def test_duplicate_page_is_rejected(self) -> None:
        self.assert_plan_error((page(1, 2, "a"), page(1, 2, "")), "OCR_PDF_INPUT_INVALID")

    def test_missing_page_is_rejected(self) -> None:
        self.assert_plan_error((page(1, 3, "a"), page(3, 3, "")), "OCR_PDF_INPUT_INVALID")

    def test_unordered_complete_input_is_canonicalized_to_source_order(self) -> None:
        plan = plan_pdf_pages((page(2, 2, ""), page(1, 2, "a")))
        self.assertEqual(tuple(item.page.page for item in plan.pages), (1, 2))
        self.assertEqual(tuple(item.route for item in plan.pages), (PageRoute.TEXT, PageRoute.OCR))

    def test_inconsistent_total_pages_is_rejected(self) -> None:
        self.assert_plan_error((page(1, 2, "a"), page(2, 3, "")), "OCR_PDF_INPUT_INVALID")

    def test_mixed_source_identity_is_rejected(self) -> None:
        other_id = PDFSourceIdentity("source-2", SOURCE.source_digest)
        other_digest = PDFSourceIdentity("source-1", compute_source_digest(b"%PDF-1.7\nother"))
        for other in (other_id, other_digest):
            with self.subTest(other=other):
                self.assert_plan_error((page(1, 2, "a"), page(2, 2, "", other)),
                                       "OCR_PDF_INPUT_INVALID")

    def test_page_bounds_and_bool_validation_are_inherited(self) -> None:
        for number, total in ((0, 1), (-1, 1), (True, 1), (2, 1), (1, False)):
            with self.subTest(number=number, total=total), self.assertRaises(PDFOCRError) as caught:
                page(number, total, "")  # type: ignore[arg-type]
            self.assertEqual(caught.exception.error_code, "OCR_PDF_PAGE_INVALID")

    def test_invalid_classification_or_route_state_is_rejected(self) -> None:
        identity = PDFPageIdentity(1, 1)
        with self.assertRaises(PDFOCRError) as caught:
            PDFPagePlan(SOURCE, identity, "text", PageClassification.SEARCHABLE, PageRoute.OCR)
        self.assertEqual(caught.exception.error_code, "OCR_PDF_INPUT_INVALID")
        for enum_type, value in ((PageClassification, "LOW_QUALITY"), (PageRoute, "AUTO")):
            with self.subTest(enum_type=enum_type), self.assertRaises(ValueError):
                enum_type(value)

    def test_plan_and_nested_identities_are_immutable(self) -> None:
        plan = plan_pdf_pages((page(1, 1, "text"),))
        self.assertIsInstance(plan, MixedPDFPlan)
        with self.assertRaises(FrozenInstanceError):
            plan.pages = ()  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            plan.pages[0].page.page = 2  # type: ignore[misc]


class ScopeBoundaryTests(unittest.TestCase):
    def test_planning_does_not_call_rasterizer_or_ocr_provider(self) -> None:
        rasterizer = FakePDFRasterizer()
        provider = FakeOCRProvider()
        plan = plan_pdf_pages((page(1, 2, "text"), page(2, 2, "")))
        self.assertEqual(tuple(item.route for item in plan.pages), (PageRoute.TEXT, PageRoute.OCR))
        self.assertEqual(rasterizer.calls, ())
        self.assertEqual(provider.calls, [])


if __name__ == "__main__":
    unittest.main()
