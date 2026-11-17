"""Focused deterministic Phase 15.6 OCR pipeline qualification tests."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys
import unittest

sys.path.insert(0, "skills/agy-ppt/scripts")
sys.path.insert(0, "skills/agy-ppt/tests")

from image_ocr import ImageOCRError, ImagePreparationConfiguration, ImagePreparationRequest, ImageResourceLimits, ImageSourceIdentity, PillowImagePreparer
from helpers.fake_ocr_provider import FakeOCRProvider
from ocr_qualification import image_fixture, multipage_tiff_fixture, pdf_fixture, run_contract_qualification
from ocr_providers import OCRRequest, execute_with_fallback
from ocr_providers.errors import OCRError
from pdf_ocr import PDFAdmissionResult, PDFOCRError, PDFPageIdentity, PDFSourceIdentity, RasterConfiguration, RasterRequest, ResourceLimits, WorkerIsolationPolicy
from pdf_ocr.pdfium_rasterizer import PDFiumRasterizer
from source_grounding import compute_source_digest


BASELINE = "85d3ba4edaf121215dae3d4c86bb1c6a671bd53c"
TESTS_ROOT = str(Path(__file__).resolve().parent)
DEPENDENCY_PATH = next((item for item in sys.path if item and (Path(item) / "pypdfium2").is_dir()), None)


def worker_paths() -> str:
    values = [TESTS_ROOT]
    if DEPENDENCY_PATH:
        values.append(DEPENDENCY_PATH)
    return os.pathsep.join(values)


class QualificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.first = run_contract_qualification(baseline_sha=BASELINE)
        cls.second = run_contract_qualification(baseline_sha=BASELINE)
        cls.cases = {case.case_id: case.to_dict() for case in cls.first.cases}

    def test_runtime_identity_is_exact_and_non_v8_non_xfa(self):
        runtime = self.first.runtime
        self.assertEqual(runtime["pypdfium2_version"], "5.13.0")
        self.assertEqual(runtime["pdfium_version"], "153.0.7999.0")
        self.assertEqual(runtime["pdfium_build"], 7999)
        self.assertEqual(runtime["pdfium_origin"], "pdfium-binaries")
        self.assertEqual(runtime["pdfium_flags"], ())
        self.assertEqual(len(runtime["wheel_sha256"]), 64)

    def test_scanned_pdf_reaches_phase12_grounding_with_distinct_raster_identity(self):
        evidence = self.cases["pdf-scanned-e2e"]["evidence"]
        self.assertEqual(evidence["route"], "OCR")
        self.assertEqual(evidence["grounding"]["locators"], [{"kind": "page", "start": 1, "end": 1}])
        self.assertNotEqual(evidence["source_digest"], evidence["raster_digest"])

    def test_mixed_pdf_routes_only_scanned_pages_and_preserves_order(self):
        evidence = self.cases["pdf-mixed-e2e"]["evidence"]
        self.assertEqual(evidence["routes"], ["TEXT", "OCR", "TEXT", "OCR"])
        self.assertEqual(evidence["ocr_calls"], 2)
        self.assertEqual([item["start"] for item in evidence["grounding"]["locators"]], [1, 2, 3, 4])

    def test_png_jpeg_exif_and_tiff_reach_image_grounding(self):
        for name in ("image-png-e2e", "image-jpeg-e2e", "image-tiff-e2e"):
            with self.subTest(name=name):
                evidence = self.cases[name]["evidence"]
                self.assertEqual(evidence["grounding"]["locators"], [{"kind": "generic", "label": "image:1-of-1"}])
                self.assertNotEqual(evidence["source_digest"], evidence["prepared_digest"])
        jpeg = self.cases["image-jpeg-e2e"]["evidence"]
        self.assertTrue(jpeg["orientation_applied"])
        self.assertEqual(jpeg["prepared_dimensions"], [48, 96])

    def test_report_is_deterministic_immutable_and_platform_honest(self):
        self.assertEqual(self.first.to_json(), self.second.to_json())
        self.assertEqual(self.first.release_readiness, "RELEASE READY WITH DOCUMENTED PLATFORM LIMITATIONS")
        self.assertIn("Linux hard isolation requires deployment-environment validation", self.first.limitations)
        with self.assertRaises(TypeError):
            self.first.runtime["pdfium_build"] = 0  # type: ignore[index]

    def test_report_has_no_paths_credentials_timestamps_or_random_ids(self):
        serialized = self.first.to_json().lower()
        for forbidden in ("/users/", "/home/", "/tmp/", "password", "api_key", "timestamp", "environment dump", "uuid"):
            self.assertNotIn(forbidden, serialized)

    def test_project_owned_fixtures_are_repeatable(self):
        for value in (
            pdf_fixture(pages=4), image_fixture("PNG", mode="RGBA"),
            image_fixture("JPEG", exif_orientation=6), image_fixture("TIFF", mode="L"),
        ):
            self.assertEqual(hashlib.sha256(value).hexdigest(), compute_source_digest(value))

    def test_password_and_invalid_pdf_fail_with_stable_errors(self):
        rasterizer = PDFiumRasterizer(_worker_pythonpath=worker_paths())
        for raw, code in ((pdf_fixture(password="secret"), "OCR_PDF_PASSWORD_REQUIRED"), (b"not pdf", "OCR_PDF_INPUT_INVALID")):
            source = PDFSourceIdentity("src_failure_pdf", compute_source_digest(raw))
            request = RasterRequest(raw, source, PDFPageIdentity(1, 1), RasterConfiguration(), ResourceLimits(), WorkerIsolationPolicy(), PDFAdmissionResult(True, "pdf"))
            with self.subTest(code=code), self.assertRaises(PDFOCRError) as caught:
                rasterizer.rasterize(request)
            self.assertEqual(caught.exception.error_code, code)

    def test_multipage_tiff_and_resource_limit_fail_closed(self):
        preparer = PillowImagePreparer(_worker_pythonpath=worker_paths())
        raw = multipage_tiff_fixture()
        request = ImagePreparationRequest(raw, ImageSourceIdentity("src_multi", compute_source_digest(raw)), ImagePreparationConfiguration(), ImageResourceLimits())
        with self.assertRaises(ImageOCRError) as caught:
            preparer.prepare(request)
        self.assertEqual(caught.exception.error_code, "OCR_IMAGE_FORMAT_UNSUPPORTED")

        png = image_fixture("PNG")
        limited = ImagePreparationRequest(png, ImageSourceIdentity("src_limited", compute_source_digest(png)), ImagePreparationConfiguration(), ImageResourceLimits(max_width=10))
        with self.assertRaises(ImageOCRError) as caught:
            preparer.prepare(limited)
        self.assertEqual(caught.exception.error_code, "OCR_IMAGE_RESOURCE_LIMIT_EXCEEDED")

    def test_malformed_and_unsupported_images_fail_before_provider_execution(self):
        preparer = PillowImagePreparer(_worker_pythonpath=worker_paths())
        for raw, code in ((b"not an image", "OCR_IMAGE_INPUT_INVALID"), (image_fixture("PNG")[:20], "OCR_IMAGE_INPUT_INVALID")):
            source = ImageSourceIdentity("src_bad_image", compute_source_digest(raw))
            request = ImagePreparationRequest(raw, source, ImagePreparationConfiguration(), ImageResourceLimits())
            with self.subTest(code=code), self.assertRaises(ImageOCRError) as caught:
                preparer.prepare(request)
            self.assertEqual(caught.exception.error_code, code)

    def test_provider_failure_and_single_fallback_rules_remain_frozen(self):
        request = OCRRequest(b"prepared", "src_provider", "1" * 64, {"kind": "image", "ordinal": 1})
        primary = FakeOCRProvider(provider_id="primary", fail_code="OCR_PROVIDER_UNAVAILABLE")
        fallback = FakeOCRProvider(provider_id="tesseract", text="fallback")
        with self.assertRaises(OCRError) as caught:
            execute_with_fallback({"primary": primary, "tesseract": fallback}, request, explicit="primary", allow_fallback=False)
        self.assertEqual(caught.exception.error_code, "OCR_FALLBACK_NOT_ALLOWED")
        self.assertEqual(fallback.calls, [])

        result = execute_with_fallback({"primary": primary, "tesseract": fallback}, request, explicit="primary", allow_fallback=True)
        self.assertTrue(result.provenance.fallback_used)
        self.assertEqual(result.provenance.fallback_reason, "OCR_PROVIDER_UNAVAILABLE")
        self.assertEqual(len(fallback.calls), 1)

        terminal = FakeOCRProvider(provider_id="terminal", fail_code="OCR_PROVIDER_VERSION_UNSUPPORTED")
        untouched = FakeOCRProvider(provider_id="tesseract")
        with self.assertRaises(OCRError) as caught:
            execute_with_fallback({"terminal": terminal, "tesseract": untouched}, request, explicit="terminal", allow_fallback=True)
        self.assertEqual(caught.exception.error_code, "OCR_PROVIDER_VERSION_UNSUPPORTED")
        self.assertEqual(untouched.calls, [])

    def test_worker_timeout_and_abnormal_exit_are_stable(self):
        raw = image_fixture("PNG")
        source = ImageSourceIdentity("src_worker", compute_source_digest(raw))
        limits = ImageResourceLimits(preparation_timeout_seconds=0.05)
        request = ImagePreparationRequest(raw, source, ImagePreparationConfiguration(), limits)
        timeout = PillowImagePreparer(_worker_module="helpers.image_worker_timeout", _worker_pythonpath=worker_paths(), _watchdog_grace_seconds=0.05)
        with self.assertRaises(ImageOCRError) as caught:
            timeout.prepare(request)
        self.assertEqual(caught.exception.error_code, "OCR_IMAGE_RESOURCE_LIMIT_EXCEEDED")

        abnormal = PillowImagePreparer(_worker_module="helpers.image_worker_exit", _worker_pythonpath=worker_paths())
        with self.assertRaises(ImageOCRError) as caught:
            abnormal.prepare(ImagePreparationRequest(raw, source, ImagePreparationConfiguration(), ImageResourceLimits()))
        self.assertEqual(caught.exception.error_code, "OCR_IMAGE_DECODE_FAILED")

    def test_internal_report_shape_is_not_published_as_ocr_schema(self):
        value = json.loads(self.first.to_json())
        self.assertEqual(value["schema_version"], "phase15.6-internal/1")
        self.assertFalse((Path("skills/agy-ppt/schemas") / "ocr_qualification.schema.json").exists())


if __name__ == "__main__":
    unittest.main()
