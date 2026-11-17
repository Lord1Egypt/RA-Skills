"""Focused deterministic tests for Phase 15.2-A internal contracts."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
import hashlib
import json
import sys
import unittest

sys.path.insert(0, "skills/agy-ppt/scripts")
sys.path.insert(0, "skills/agy-ppt/tests")

from helpers.fake_pdf_rasterizer import FakePDFRasterizer
from pdf_ocr import (
    ERROR_CODES,
    PDFAdmissionResult,
    PDFOCRError,
    PDFOCRErrorCode,
    PDFPageIdentity,
    PDFSourceIdentity,
    PageClassification,
    RasterConfiguration,
    RasterProvenance,
    RasterRequest,
    RasterResult,
    ResourceLimits,
    WorkerIsolationPolicy,
)
from source_grounding import compute_source_digest


RAW_PDF = b"%PDF-1.7\nsynthetic contract fixture"
SOURCE_DIGEST = compute_source_digest(RAW_PDF)


def request(**overrides: object) -> RasterRequest:
    values: dict[str, object] = {
        "raw_pdf_bytes": RAW_PDF,
        "source": PDFSourceIdentity("source-1", SOURCE_DIGEST),
        "page": PDFPageIdentity(1, 3),
        "configuration": RasterConfiguration(),
        "resource_limits": ResourceLimits(),
        "isolation_policy": WorkerIsolationPolicy(),
        "admission": PDFAdmissionResult(True, "pdf"),
    }
    values.update(overrides)
    return RasterRequest(**values)  # type: ignore[arg-type]


class SourceAndPageIdentityTests(unittest.TestCase):
    def test_source_identity_preserves_original_pdf_digest(self) -> None:
        identity = PDFSourceIdentity("source-1", SOURCE_DIGEST)
        self.assertEqual(identity.source_digest, compute_source_digest(RAW_PDF))
        self.assertEqual(json.loads(identity.to_json()), identity.to_dict())

    def test_invalid_source_digest_is_rejected(self) -> None:
        for digest in ("A" * 64, "0" * 63, "not-a-digest"):
            with self.subTest(digest=digest), self.assertRaises(PDFOCRError) as caught:
                PDFSourceIdentity("source-1", digest)
            self.assertEqual(caught.exception.error_code, "OCR_PDF_INPUT_INVALID")

    def test_page_identity_is_one_based_and_deterministic(self) -> None:
        page = PDFPageIdentity(2, 3)
        self.assertEqual(page.to_dict(), {"kind": "page", "page": 2, "total_pages": 3})
        self.assertEqual(page.to_json(), '{"kind":"page","page":2,"total_pages":3}')

    def test_invalid_page_indices_use_pdf_page_error(self) -> None:
        for page, total in ((0, 1), (-1, 1), (True, 1), (2, 1), (1, False)):
            with self.subTest(page=page, total=total), self.assertRaises(PDFOCRError) as caught:
                PDFPageIdentity(page, total)  # type: ignore[arg-type]
            self.assertEqual(caught.exception.error_code, "OCR_PDF_PAGE_INVALID")


class ClassificationAndConfigurationTests(unittest.TestCase):
    def test_classification_has_only_committed_states(self) -> None:
        self.assertEqual([item.value for item in PageClassification], ["SEARCHABLE", "SCANNED"])
        self.assertEqual(PageClassification("SEARCHABLE"), PageClassification.SEARCHABLE)
        self.assertEqual(PageClassification("SCANNED"), PageClassification.SCANNED)

    def test_invalid_classification_is_rejected(self) -> None:
        for value in ("LOW_QUALITY", "NEEDS_OCR", "MAYBE_SCANNED", "searchable"):
            with self.assertRaises(ValueError):
                PageClassification(value)

    def test_raster_configuration_committed_defaults(self) -> None:
        config = RasterConfiguration()
        self.assertEqual(
            config.to_dict(),
            {
                "dpi": 300,
                "output_format": "PNG",
                "colorspace": "RGB",
                "alpha": False,
                "rotation_policy": "respect_effective_pdf_page_rotation",
                "box_policy": "valid_explicit_cropbox_else_mediabox",
                "semantic_preprocessing": "none",
                "render_annotations": False,
            },
        )
        self.assertEqual(config.to_json(), RasterConfiguration().to_json())

    def test_raster_configuration_rejects_changes_and_bool_aliases(self) -> None:
        invalid = ({"dpi": True}, {"dpi": 299}, {"output_format": "png"}, {"colorspace": "RGBA"},
                   {"alpha": 0}, {"render_annotations": True}, {"semantic_preprocessing": "deskew"})
        for values in invalid:
            with self.subTest(values=values), self.assertRaises(PDFOCRError):
                RasterConfiguration(**values)


class ResourceAndIsolationTests(unittest.TestCase):
    def test_resource_defaults_match_committed_ceilings(self) -> None:
        limits = ResourceLimits()
        self.assertEqual(limits.to_dict(), ResourceLimits.committed_ceilings())
        self.assertEqual(limits.max_raw_pdf_bytes, 100 * 1024 * 1024)
        self.assertEqual(limits.max_page_count, 500)
        self.assertEqual(limits.max_pixels_per_page, 25_000_000)
        self.assertEqual(limits.max_temporary_storage_bytes, 256 * 1024 * 1024)
        self.assertEqual(limits.worker_memory_limit_bytes, 512 * 1024 * 1024)
        self.assertFalse(limits.enforced)

    def test_smaller_positive_resource_limits_are_allowed(self) -> None:
        limits = ResourceLimits(max_page_count=1, renderer_timeout_seconds_per_page=0.5)
        self.assertEqual(limits.max_page_count, 1)

    def test_zero_negative_bool_and_above_ceiling_are_rejected(self) -> None:
        for values in ({"max_page_count": 0}, {"max_page_count": -1}, {"max_page_count": True},
                       {"max_page_count": 501}, {"renderer_timeout_seconds_per_page": 31.0},
                       {"renderer_timeout_seconds_per_page": False}):
            with self.subTest(values=values), self.assertRaises(PDFOCRError) as caught:
                ResourceLimits(**values)
            self.assertEqual(caught.exception.error_code, "OCR_PDF_RESOURCE_LIMIT_EXCEEDED")

    def test_resource_serialization_is_stable(self) -> None:
        self.assertEqual(ResourceLimits().to_json(), ResourceLimits().to_json())
        self.assertEqual(json.loads(ResourceLimits().to_json()), ResourceLimits().to_dict())

    def test_isolation_defaults_are_strict_and_serializable(self) -> None:
        policy = WorkerIsolationPolicy()
        self.assertTrue(policy.dedicated_worker)
        self.assertTrue(policy.restricted_before_open)
        self.assertFalse(policy.network_enabled)
        self.assertFalse(policy.credentials_available)
        self.assertTrue(policy.native_crash_isolated)
        self.assertTrue(policy.resource_limits_required)
        self.assertTrue(policy.temporary_storage_bounded)
        self.assertFalse(policy.enforced)
        self.assertEqual(json.loads(policy.to_json()), policy.to_dict())

    def test_isolation_policy_cannot_be_weakened(self) -> None:
        for values in ({"dedicated_worker": False}, {"network_enabled": True}, {"bounded_ipc": False},
                       {"resource_limits_required": False}, {"temporary_storage_bounded": False},
                       {"credentials_available": True}, {"cleanup_required": False}):
            with self.subTest(values=values), self.assertRaises(PDFOCRError):
                WorkerIsolationPolicy(**values)


class AdmissionAndProvenanceTests(unittest.TestCase):
    def test_admission_accepts_only_deterministic_pdf_result(self) -> None:
        admitted = PDFAdmissionResult(True, "pdf")
        self.assertEqual(admitted.detected_format, "pdf")
        self.assertEqual(json.loads(admitted.to_json()), admitted.to_dict())
        with self.assertRaises(PDFOCRError):
            PDFAdmissionResult(True, "epub")
        rejected = PDFAdmissionResult(False, None, "OCR_PDF_INPUT_INVALID")
        self.assertFalse(rejected.accepted)

    def test_request_rejects_non_pdf_or_unadmitted_input(self) -> None:
        with self.assertRaises(PDFOCRError):
            request(admission=PDFAdmissionResult(False, None, "OCR_PDF_INPUT_INVALID"))

    def test_request_enforces_raw_byte_limit(self) -> None:
        limits = ResourceLimits(max_raw_pdf_bytes=1)
        with self.assertRaises(PDFOCRError) as caught:
            request(resource_limits=limits)
        self.assertEqual(caught.exception.error_code, "OCR_PDF_RESOURCE_LIMIT_EXCEEDED")

    def test_request_rejects_digest_not_derived_from_original_pdf_bytes(self) -> None:
        different = PDFSourceIdentity("source-1", compute_source_digest(b"derived raster"))
        with self.assertRaises(PDFOCRError) as caught:
            request(source=different)
        self.assertEqual(caught.exception.error_code, "OCR_PDF_INPUT_INVALID")

    def test_provenance_is_complete_stable_and_path_free(self) -> None:
        result = FakePDFRasterizer().rasterize(request())
        payload = result.provenance.to_dict()
        self.assertEqual(payload["renderer_id"], "fake-pdf-rasterizer")
        self.assertEqual(payload["width"], 1200)
        self.assertEqual(payload["height"], 1600)
        self.assertFalse(payload["render_annotations"])
        self.assertEqual(result.provenance.to_json(), result.provenance.to_json())
        for forbidden in ("path", "timestamp", "cache", "credential", "environment"):
            self.assertNotIn(forbidden, " ".join(payload).lower())

    def test_provenance_rejects_private_path_and_invalid_geometry(self) -> None:
        result = FakePDFRasterizer().rasterize(request())
        values = result.provenance.to_dict()
        values["box_coordinates"] = tuple(values["box_coordinates"])
        for update in ({"renderer_version": "/private/lib.so"}, {"width": 0},
                       {"effective_rotation": 45}, {"selected_box": "BleedBox"},
                       {"box_coordinates": (1.0, 1.0, 0.0, 0.0)}):
            candidate = dict(values)
            candidate.update(update)
            with self.subTest(update=update), self.assertRaises(PDFOCRError):
                RasterProvenance(**candidate)

    def test_raster_digest_identifies_prepared_bytes_not_source(self) -> None:
        result = FakePDFRasterizer().rasterize(request())
        self.assertEqual(result.provenance.raster_digest, hashlib.sha256(result.raster_bytes).hexdigest())
        self.assertNotEqual(result.provenance.raster_digest, SOURCE_DIGEST)

    def test_result_rejects_mismatched_raster_digest(self) -> None:
        result = FakePDFRasterizer().rasterize(request())
        with self.assertRaises(PDFOCRError):
            RasterResult(b"different", result.provenance)


class FakeRasterizerAndErrorTests(unittest.TestCase):
    def test_fake_is_repeatable_and_records_immutable_calls(self) -> None:
        fake = FakePDFRasterizer()
        first = fake.rasterize(request())
        second = fake.rasterize(request())
        self.assertEqual(first, second)
        self.assertEqual(len(fake.calls), 2)
        self.assertIsInstance(fake.calls, tuple)

    def test_fake_changes_deterministically_with_page_identity(self) -> None:
        fake = FakePDFRasterizer()
        first = fake.rasterize(request(page=PDFPageIdentity(1, 3)))
        second = fake.rasterize(request(page=PDFPageIdentity(2, 3)))
        self.assertNotEqual(first.raster_bytes, second.raster_bytes)

    def test_fake_dimensions_change_output_deterministically(self) -> None:
        first = FakePDFRasterizer(width=1200, height=1600).rasterize(request())
        second = FakePDFRasterizer(width=1201, height=1600).rasterize(request())
        self.assertNotEqual(first.raster_bytes, second.raster_bytes)
        self.assertNotEqual(first.provenance.raster_digest, second.provenance.raster_digest)

    def test_fake_failure_injection_is_stable(self) -> None:
        fake = FakePDFRasterizer(fail_code=PDFOCRErrorCode.RASTERIZATION_FAILED)
        with self.assertRaises(PDFOCRError) as caught:
            fake.rasterize(request())
        self.assertEqual(caught.exception.error_code, "OCR_RASTERIZATION_FAILED")
        self.assertEqual(len(fake.calls), 1)

    def test_exact_committed_error_codes_and_no_provider_fallback(self) -> None:
        self.assertEqual(
            ERROR_CODES,
            frozenset(
                {
                    "OCR_PDF_PASSWORD_REQUIRED",
                    "OCR_PDF_INPUT_INVALID",
                    "OCR_PDF_PAGE_INVALID",
                    "OCR_PDF_RESOURCE_LIMIT_EXCEEDED",
                    "OCR_PDF_CLEANUP_FAILED",
                    "OCR_RASTERIZATION_FAILED",
                }
            ),
        )
        for code in PDFOCRErrorCode:
            error = PDFOCRError("failure", code)
            self.assertEqual(error.error_code, code.value)
            self.assertFalse(error.provider_fallback_eligible)
            self.assertEqual(PDFOCRError("different message", code).error_code, code.value)

    def test_models_are_frozen(self) -> None:
        models = (PDFPageIdentity(1, 1), PDFSourceIdentity("source", SOURCE_DIGEST), RasterConfiguration(),
                  ResourceLimits(), WorkerIsolationPolicy(), PDFAdmissionResult(True, "pdf"),
                  FakePDFRasterizer().rasterize(request()).provenance)
        for model in models:
            with self.subTest(model=type(model).__name__), self.assertRaises(FrozenInstanceError):
                model.extra = "mutation"  # type: ignore[attr-defined]

    def test_recorded_request_nested_models_are_immutable(self) -> None:
        fake = FakePDFRasterizer()
        fake.rasterize(request())
        with self.assertRaises(FrozenInstanceError):
            fake.calls[0].page.page = 2  # type: ignore[misc]


if __name__ == "__main__":
    unittest.main()
