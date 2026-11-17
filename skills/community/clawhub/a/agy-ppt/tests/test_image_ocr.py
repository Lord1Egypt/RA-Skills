"""Focused deterministic tests for Phase 15.3 standalone image OCR."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from io import BytesIO
import hashlib
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch

from PIL import Image

sys.path.insert(0, "skills/agy-ppt/scripts")
sys.path.insert(0, "skills/agy-ppt/tests")

from helpers.fake_ocr_provider import FakeOCRProvider
from image_ocr import (
    ERROR_CODES,
    ImageOCRError,
    ImagePreparationConfiguration,
    ImagePreparationProvenance,
    ImagePreparationRequest,
    ImagePreparer,
    ImageResourceLimits,
    ImageSourceIdentity,
    PillowImagePreparer,
    PreparedImage,
    StandaloneImageOCRResult,
    execute_standalone_image_ocr,
)
from image_ocr.worker import _prepare
from ocr_providers import OCRPage, OCRProvider, OCRProviderCapabilities, OCRProviderMetadata, OCRProvenance, OCRRequest, OCREvidence
from ocr_providers.errors import OCRError


TESTS_ROOT = str(Path(__file__).resolve().parent)


def image_bytes(format_name: str = "PNG", mode: str = "RGB", size: tuple[int, int] = (4, 3), *, color=None, exif_orientation: int | None = None, icc: bool = False) -> bytes:
    if color is None:
        color = {"RGB": (20, 40, 60), "RGBA": (20, 40, 60, 128), "L": 80, "LA": (80, 128), "CMYK": (10, 20, 30, 40), "P": 0, "1": 1}[mode]
    image = Image.new(mode, size, color)
    if mode == "P":
        image.putpalette([255, 0, 0, 0, 255, 0] + [0, 0, 0] * 254)
    exif = None
    if exif_orientation is not None:
        exif = Image.Exif()
        exif[274] = exif_orientation
    output = BytesIO()
    kwargs = {}
    if exif is not None:
        kwargs["exif"] = exif
    if icc:
        kwargs["icc_profile"] = b"synthetic-icc-profile"
    image.save(output, format=format_name, **kwargs)
    image.close()
    return output.getvalue()


def multipage_tiff() -> bytes:
    first = Image.new("RGB", (2, 2), "red")
    second = Image.new("RGB", (2, 2), "blue")
    output = BytesIO()
    first.save(output, format="TIFF", save_all=True, append_images=[second])
    first.close()
    second.close()
    return output.getvalue()


def source(raw: bytes) -> ImageSourceIdentity:
    return ImageSourceIdentity("image-source", hashlib.sha256(raw).hexdigest())


def request(raw: bytes, limits: ImageResourceLimits | None = None) -> ImagePreparationRequest:
    return ImagePreparationRequest(raw, source(raw), ImagePreparationConfiguration(), limits or ImageResourceLimits())


def worker_paths() -> str:
    return TESTS_ROOT


class FakePreparer(ImagePreparer):
    def __init__(self, *, failure: ImageOCRError | None = None):
        self.calls: list[ImagePreparationRequest] = []
        self.failure = failure
        png = image_bytes(color=(200, 210, 220))
        self.result = PreparedImage(png, ImagePreparationProvenance(
            "Pillow", Image.__version__, "PNG", 4, 3, "RGB", None, False, False,
            "composite_on_white", "preserve_rgb", "PNG", "RGB", 4, 3,
            hashlib.sha256(png).hexdigest(),
        ))

    def prepare(self, preparation_request: ImagePreparationRequest) -> PreparedImage:
        self.calls.append(preparation_request)
        if self.failure:
            raise self.failure
        return self.result


class BadEvidenceProvider(OCRProvider):
    provider_id = "bad"
    provider_version = "1.0"
    capabilities = OCRProviderCapabilities(True, True, "local", False)

    def recognize(self, request: OCRRequest) -> OCREvidence:
        return OCREvidence(
            "1.0", request.source_id, request.source_digest,
            (OCRPage({"kind": "image", "ordinal": 2}, "bad", ()),),
            self.capabilities, OCRProviderMetadata(self.provider_id, self.provider_version),
            OCRProvenance(self.provider_id, self.provider_id, "local", False),
        )


class ContractTests(unittest.TestCase):
    def test_exact_error_family_is_non_fallback(self):
        self.assertEqual(ERROR_CODES, {
            "OCR_IMAGE_FORMAT_UNSUPPORTED", "OCR_IMAGE_INPUT_INVALID", "OCR_IMAGE_RESOURCE_LIMIT_EXCEEDED",
            "OCR_IMAGE_DECODE_FAILED", "OCR_IMAGE_CLEANUP_FAILED",
        })
        self.assertFalse(ImageOCRError("x", "OCR_IMAGE_INPUT_INVALID").provider_fallback_eligible)

    def test_source_identity_uses_original_bytes(self):
        raw = image_bytes("JPEG")
        self.assertEqual(ImageSourceIdentity.from_bytes("s", raw).source_digest, hashlib.sha256(raw).hexdigest())

    def test_limits_reject_bool_nonpositive_and_above_ceiling(self):
        for kwargs in ({"max_width": True}, {"max_pixels": 0}, {"max_height": 10_001}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ImageOCRError) as caught:
                ImageResourceLimits(**kwargs)
            self.assertEqual(caught.exception.error_code, "OCR_IMAGE_RESOURCE_LIMIT_EXCEEDED")

    def test_configuration_is_fixed(self):
        with self.assertRaises(ImageOCRError):
            ImagePreparationConfiguration(target_mode="RGBA")

    def test_models_are_immutable_and_serialization_is_stable(self):
        fake = FakePreparer()
        with self.assertRaises(FrozenInstanceError):
            fake.result.provenance.target_mode = "L"  # type: ignore[misc]
        self.assertEqual(fake.result.provenance.to_json(), fake.result.provenance.to_json())


class RealPreparationTests(unittest.TestCase):
    def setUp(self):
        self.preparer = PillowImagePreparer(_worker_pythonpath=worker_paths())

    def prepare(self, raw: bytes, limits: ImageResourceLimits | None = None) -> PreparedImage:
        return self.preparer.prepare(request(raw, limits))

    def test_valid_png_jpeg_and_single_frame_tiff(self):
        for format_name in ("PNG", "JPEG", "TIFF"):
            with self.subTest(format_name=format_name):
                result = self.prepare(image_bytes(format_name))
                self.assertEqual(result.provenance.source_format, format_name)
                with Image.open(BytesIO(result.png_bytes)) as prepared:
                    self.assertEqual((prepared.format, prepared.mode, prepared.size), ("PNG", "RGB", (4, 3)))

    def test_content_is_authoritative_and_unsupported_format_fails(self):
        png_named_jpeg = image_bytes("PNG")
        provider = FakeOCRProvider(provider_id="tesseract")
        transaction = execute_standalone_image_ocr(
            png_named_jpeg,
            "misleading-name.jpg",
            self.preparer,
            {"tesseract": provider},
        )
        self.assertEqual(transaction.preparation.source_format, "PNG")
        self.assertEqual(provider.calls[0].image_bytes, self.prepare(png_named_jpeg).png_bytes)
        with self.assertRaises(ImageOCRError) as caught:
            self.prepare(image_bytes("GIF"))
        self.assertEqual(caught.exception.error_code, "OCR_IMAGE_FORMAT_UNSUPPORTED")

    def test_multipage_tiff_is_rejected(self):
        with self.assertRaises(ImageOCRError) as caught:
            self.prepare(multipage_tiff())
        self.assertEqual(caught.exception.error_code, "OCR_IMAGE_FORMAT_UNSUPPORTED")

    def test_invalid_and_truncated_input_fail_closed(self):
        png = image_bytes("PNG")
        for raw in (b"not-an-image", png[: len(png) // 2], image_bytes("JPEG")[:20]):
            with self.subTest(length=len(raw)):
                with self.assertRaises(ImageOCRError) as caught:
                    self.prepare(raw)
                self.assertEqual(caught.exception.error_code, "OCR_IMAGE_INPUT_INVALID")

    def test_grayscale_and_bilevel_convert_to_rgb(self):
        for mode in ("L", "1"):
            result = self.prepare(image_bytes("PNG", mode))
            with Image.open(BytesIO(result.png_bytes)) as prepared:
                self.assertEqual(prepared.mode, "RGB")
                r, g, b = prepared.getpixel((0, 0))
                self.assertEqual(r, g)
                self.assertEqual(g, b)

    def test_rgba_and_la_composite_on_white(self):
        for mode in ("RGBA", "LA"):
            result = self.prepare(image_bytes("PNG", mode))
            with Image.open(BytesIO(result.png_bytes)) as prepared:
                self.assertEqual(prepared.mode, "RGB")
                self.assertNotEqual(prepared.getpixel((0, 0)), (20, 40, 60))
            self.assertEqual(result.provenance.color_conversion_policy, "alpha_composite_on_white")

    def test_fully_transparent_and_opaque_alpha_edges(self):
        transparent = self.prepare(image_bytes("PNG", "RGBA", color=(1, 2, 3, 0)))
        opaque = self.prepare(image_bytes("PNG", "RGBA", color=(1, 2, 3, 255)))
        with Image.open(BytesIO(transparent.png_bytes)) as first, Image.open(BytesIO(opaque.png_bytes)) as second:
            self.assertEqual(first.getpixel((0, 0)), (255, 255, 255))
            self.assertEqual(second.getpixel((0, 0)), (1, 2, 3))

    def test_palette_with_and_without_transparency(self):
        raw = image_bytes("PNG", "P")
        self.assertEqual(self.prepare(raw).provenance.color_conversion_policy, "palette_to_rgb")
        image = Image.open(BytesIO(raw))
        output = BytesIO()
        image.save(output, format="PNG", transparency=0)
        image.close()
        result = self.prepare(output.getvalue())
        self.assertEqual(result.provenance.color_conversion_policy, "alpha_composite_on_white")

    def test_cmyk_jpeg_converts_to_rgb(self):
        result = self.prepare(image_bytes("JPEG", "CMYK"))
        self.assertEqual(result.provenance.original_mode, "CMYK")
        self.assertEqual(result.provenance.color_conversion_policy, "cmyk_ycck_to_rgb")
        with Image.open(BytesIO(result.png_bytes)) as prepared:
            self.assertEqual(prepared.mode, "RGB")

    def test_exif_rotate_and_mirror_are_applied(self):
        rotated = self.prepare(image_bytes("JPEG", "RGB", (4, 2), exif_orientation=6))
        mirror_source = Image.new("RGB", (2, 1))
        mirror_source.putdata([(255, 0, 0), (0, 0, 255)])
        mirror_exif = Image.Exif()
        mirror_exif[274] = 2
        mirror_output = BytesIO()
        mirror_source.save(mirror_output, format="TIFF", exif=mirror_exif)
        mirror_source.close()
        mirrored = self.prepare(mirror_output.getvalue())
        self.assertEqual((rotated.provenance.prepared_width, rotated.provenance.prepared_height), (2, 4))
        self.assertEqual((mirrored.provenance.prepared_width, mirrored.provenance.prepared_height), (2, 1))
        self.assertTrue(rotated.provenance.orientation_transform_applied)
        self.assertTrue(mirrored.provenance.orientation_transform_applied)
        with Image.open(BytesIO(mirrored.png_bytes)) as prepared:
            self.assertEqual([prepared.getpixel((x, 0)) for x in range(2)], [(0, 0, 255), (255, 0, 0)])

    def test_normal_and_absent_orientation_do_not_claim_transform(self):
        for orientation in (None, 1):
            result = self.prepare(image_bytes("JPEG", exif_orientation=orientation))
            self.assertFalse(result.provenance.orientation_transform_applied)

    def test_invalid_exif_orientation_is_invalid_input(self):
        with self.assertRaises(ImageOCRError) as caught:
            self.prepare(image_bytes("JPEG", exif_orientation=9))
        self.assertEqual(caught.exception.error_code, "OCR_IMAGE_INPUT_INVALID")

    def test_unapproved_color_mode_is_unsupported(self):
        image = Image.new("I", (2, 2), 1024)
        output = BytesIO()
        image.save(output, format="TIFF")
        image.close()
        with self.assertRaises(ImageOCRError) as caught:
            self.prepare(output.getvalue())
        self.assertEqual(caught.exception.error_code, "OCR_IMAGE_FORMAT_UNSUPPORTED")

    def test_icc_presence_is_recorded_but_profile_is_dropped(self):
        result = self.prepare(image_bytes("PNG", icc=True))
        self.assertTrue(result.provenance.icc_profile_present)
        with Image.open(BytesIO(result.png_bytes)) as prepared:
            self.assertNotIn("icc_profile", prepared.info)

    def test_prepared_digest_and_repeatability(self):
        raw = image_bytes("PNG", "RGBA")
        first = self.prepare(raw)
        second = self.prepare(raw)
        self.assertEqual(first.png_bytes, second.png_bytes)
        self.assertEqual(first.provenance.to_json(), second.provenance.to_json())
        self.assertEqual(first.provenance.prepared_image_digest, hashlib.sha256(first.png_bytes).hexdigest())
        self.assertNotEqual(first.provenance.prepared_image_digest, hashlib.sha256(raw).hexdigest())

    def test_resource_limits_cover_raw_dimensions_pixels_footprint_and_output(self):
        cases = (
            (image_bytes(), ImageResourceLimits(max_raw_image_bytes=10)),
            (image_bytes(size=(5, 3)), ImageResourceLimits(max_width=4)),
            (image_bytes(size=(4, 3)), ImageResourceLimits(max_pixels=11)),
            (image_bytes(size=(4, 3)), ImageResourceLimits(max_decoded_packed_bytes=47)),
            (image_bytes(), ImageResourceLimits(max_prepared_png_bytes=20)),
        )
        for raw, limits in cases:
            with self.subTest(limits=limits), self.assertRaises(ImageOCRError) as caught:
                self.prepare(raw, limits)
            self.assertEqual(caught.exception.error_code, "OCR_IMAGE_RESOURCE_LIMIT_EXCEEDED")

    def test_decompression_bomb_warning_maps_to_resource_error(self):
        old = Image.MAX_IMAGE_PIXELS
        try:
            Image.MAX_IMAGE_PIXELS = 10
            worker_request = {"source": source(image_bytes()).to_dict(), "configuration": ImagePreparationConfiguration().to_dict(), "resource_limits": ImageResourceLimits().to_dict()}
            with self.assertRaises(ImageOCRError) as caught:
                _prepare(image_bytes(), worker_request)
            self.assertEqual(caught.exception.error_code, "OCR_IMAGE_RESOURCE_LIMIT_EXCEEDED")
        finally:
            Image.MAX_IMAGE_PIXELS = old

    def test_provenance_has_no_host_or_temp_paths(self):
        serialized = self.prepare(image_bytes()).provenance.to_json().lower()
        for forbidden in ("/users/", "/home/", "/tmp/", "timestamp", "environment", "cache/"):
            self.assertNotIn(forbidden, serialized)

    def test_cleanup_only_failure_uses_cleanup_error(self):
        raw = image_bytes()
        fake = Mock()
        fake.format = "PNG"
        fake.n_frames = 1
        fake.size = (4, 3)
        fake.mode = "RGB"
        fake.info = {}
        fake.getexif.return_value = {}
        fake.copy.return_value = fake
        fake.save.side_effect = lambda stream, **_kwargs: stream.write(b"prepared")
        fake.close.side_effect = OSError("cleanup")
        worker_request = {"source": source(raw).to_dict(), "configuration": ImagePreparationConfiguration().to_dict(), "resource_limits": ImageResourceLimits().to_dict()}
        with patch("PIL.Image.open", return_value=fake), patch("PIL.ImageOps.exif_transpose", return_value=fake):
            with self.assertRaises(ImageOCRError) as caught:
                _prepare(raw, worker_request)
        self.assertEqual(caught.exception.error_code, "OCR_IMAGE_CLEANUP_FAILED")


class WorkerBoundaryTests(unittest.TestCase):
    def configured(self, module: str, grace: float = 5.0) -> PillowImagePreparer:
        return PillowImagePreparer(_worker_module=module, _worker_pythonpath=worker_paths(), _watchdog_grace_seconds=grace)

    def test_controlled_error_preserves_image_taxonomy(self):
        with self.assertRaises(ImageOCRError) as caught:
            self.configured("helpers.image_worker_error").prepare(request(image_bytes()))
        self.assertEqual(caught.exception.error_code, "OCR_IMAGE_INPUT_INVALID")

    def test_timeout_maps_to_resource_limit(self):
        limits = ImageResourceLimits(preparation_timeout_seconds=0.05)
        with self.assertRaises(ImageOCRError) as caught:
            self.configured("helpers.image_worker_timeout", 0.05).prepare(request(image_bytes(), limits))
        self.assertEqual(caught.exception.error_code, "OCR_IMAGE_RESOURCE_LIMIT_EXCEEDED")

    def test_abnormal_worker_exit_maps_to_decode_failure(self):
        with self.assertRaises(ImageOCRError) as caught:
            self.configured("helpers.image_worker_exit").prepare(request(image_bytes()))
        self.assertEqual(caught.exception.error_code, "OCR_IMAGE_DECODE_FAILED")

    def test_oversized_ipc_maps_to_resource_limit(self):
        limits = ImageResourceLimits(max_prepared_png_bytes=100)
        with self.assertRaises(ImageOCRError) as caught:
            self.configured("helpers.image_worker_oversized").prepare(request(image_bytes(), limits))
        self.assertEqual(caught.exception.error_code, "OCR_IMAGE_RESOURCE_LIMIT_EXCEEDED")


class OrchestrationTests(unittest.TestCase):
    def execute(self, preparer: ImagePreparer, providers=None, **kwargs) -> StandaloneImageOCRResult:
        return execute_standalone_image_ocr(image_bytes(), "source", preparer, providers or {"tesseract": FakeOCRProvider(provider_id="tesseract")}, **kwargs)

    def test_valid_image_invokes_preparer_and_provider_once(self):
        preparer = FakePreparer()
        provider = FakeOCRProvider(provider_id="tesseract", text=" raw OCR\n")
        result = self.execute(preparer, {"tesseract": provider})
        self.assertEqual(len(preparer.calls), 1)
        self.assertEqual(len(provider.calls), 1)
        self.assertEqual(provider.calls[0].image_bytes, preparer.result.png_bytes)
        self.assertEqual(result.raw_text, " raw OCR\n")
        self.assertEqual(dict(provider.calls[0].locator), {"kind": "image", "ordinal": 1})

    def test_source_and_prepared_identities_remain_distinct(self):
        preparer = FakePreparer()
        provider = FakeOCRProvider(provider_id="tesseract")
        raw = image_bytes()
        result = execute_standalone_image_ocr(raw, "source", preparer, {"tesseract": provider})
        self.assertEqual(result.source.source_digest, hashlib.sha256(raw).hexdigest())
        self.assertEqual(result.evidence.source_digest, result.source.source_digest)
        self.assertEqual(result.preparation.prepared_image_digest, hashlib.sha256(preparer.result.png_bytes).hexdigest())
        self.assertNotEqual(result.source.source_digest, result.preparation.prepared_image_digest)

    def test_preparation_failure_never_calls_provider_or_fallback(self):
        preparer = FakePreparer(failure=ImageOCRError("limit", "OCR_IMAGE_RESOURCE_LIMIT_EXCEEDED"))
        primary = FakeOCRProvider(provider_id="primary")
        fallback = FakeOCRProvider(provider_id="tesseract")
        with self.assertRaises(ImageOCRError):
            self.execute(preparer, {"primary": primary, "tesseract": fallback}, explicit="primary", allow_fallback=True)
        self.assertEqual(primary.calls, [])
        self.assertEqual(fallback.calls, [])

    def test_frozen_provider_fallback_is_reused(self):
        primary = FakeOCRProvider(provider_id="primary", fail_code="OCR_PROVIDER_UNAVAILABLE")
        fallback = FakeOCRProvider(provider_id="tesseract", text="fallback")
        result = self.execute(FakePreparer(), {"primary": primary, "tesseract": fallback}, explicit="primary", allow_fallback=True)
        self.assertEqual(result.raw_text, "fallback")
        self.assertEqual((len(primary.calls), len(fallback.calls)), (1, 1))
        self.assertTrue(result.evidence.provenance.fallback_used)

    def test_disabled_and_terminal_failures_do_not_broaden_fallback(self):
        for code, allow, expected in (("OCR_PROVIDER_FAILED", False, "OCR_FALLBACK_NOT_ALLOWED"), ("OCR_PROVIDER_CONTRACT_INVALID", True, "OCR_PROVIDER_CONTRACT_INVALID")):
            primary = FakeOCRProvider(provider_id="primary", fail_code=code)
            fallback = FakeOCRProvider(provider_id="tesseract")
            with self.subTest(code=code), self.assertRaises(OCRError) as caught:
                self.execute(FakePreparer(), {"primary": primary, "tesseract": fallback}, explicit="primary", allow_fallback=allow)
            self.assertEqual(caught.exception.error_code, expected)
            self.assertEqual(fallback.calls, [])

    def test_fallback_failure_is_preserved(self):
        primary = FakeOCRProvider(provider_id="primary", fail_code="OCR_PROVIDER_FAILED")
        fallback = FakeOCRProvider(provider_id="tesseract", fail_code="OCR_EXTRACTION_FAILED")
        with self.assertRaises(OCRError) as caught:
            self.execute(FakePreparer(), {"primary": primary, "tesseract": fallback}, explicit="primary", allow_fallback=True)
        self.assertEqual(caught.exception.error_code, "OCR_EXTRACTION_FAILED")

    def test_invalid_evidence_fails_without_repair(self):
        with self.assertRaises(OCRError) as caught:
            self.execute(FakePreparer(), {"bad": BadEvidenceProvider()}, explicit="bad")
        self.assertEqual(caught.exception.error_code, "OCR_PROVIDER_CONTRACT_INVALID")

    def test_repeated_execution_serializes_identically(self):
        first = self.execute(FakePreparer(), {"tesseract": FakeOCRProvider(provider_id="tesseract")})
        second = self.execute(FakePreparer(), {"tesseract": FakeOCRProvider(provider_id="tesseract")})
        self.assertEqual(first.to_json(), second.to_json())


if __name__ == "__main__":
    unittest.main()
