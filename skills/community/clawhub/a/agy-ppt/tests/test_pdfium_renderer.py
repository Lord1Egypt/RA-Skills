"""Phase 15.2-C isolated PDFium renderer tests."""

from __future__ import annotations

from io import BytesIO
import hashlib
import json
import os
from pathlib import Path
import sys
import unittest

from PIL import Image
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, DictionaryObject, FloatObject, NameObject, NumberObject

sys.path.insert(0, "skills/agy-ppt/scripts")
sys.path.insert(0, "skills/agy-ppt/tests")

from pdf_ocr import (
    PDFAdmissionResult,
    PDFOCRError,
    PDFPageIdentity,
    PDFSourceIdentity,
    RasterConfiguration,
    RasterRequest,
    ResourceLimits,
    WorkerIsolationPolicy,
)
from pdf_ocr.pdfium_geometry import build_geometry, outward_pixels
from pdf_ocr.pdfium_identity import (
    ENGINE_BUILD,
    ENGINE_ORIGIN,
    ENGINE_VERSION,
    RENDERER_VERSION,
    approved_build_identity,
    load_approved_artifact,
)
from pdf_ocr.pdfium_rasterizer import PDFiumRasterizer
from pdf_ocr.pdfium_worker import _resource_preflight


REPO_ROOT = Path(__file__).resolve().parents[3]
TESTS_ROOT = str(Path(__file__).resolve().parent)
WORKER_DEPENDENCY_PATH = next(
    (entry for entry in sys.path if entry and (Path(entry) / "pypdfium2").is_dir()),
    None,
)


def worker_paths(*paths: str) -> str | None:
    values = [*paths]
    if WORKER_DEPENDENCY_PATH:
        values.append(WORKER_DEPENDENCY_PATH)
    return os.pathsep.join(values) or None


def pdf_bytes(
    *,
    width: object = 60,
    height: object = 120,
    crop: tuple[object, object, object, object] | None = None,
    inherited_crop: bool = False,
    rotation: int = 0,
    annotation: bool = False,
    password: str | None = None,
) -> bytes:
    writer = PdfWriter()
    page = writer.add_blank_page(width=float(width), height=float(height))
    page.mediabox = ArrayObject([FloatObject(str(value)) for value in (0, 0, width, height)])
    if crop is not None:
        target = ArrayObject([FloatObject(str(value)) for value in crop])
        if inherited_crop:
            writer._pages.get_object()[NameObject("/CropBox")] = target
            page.pop(NameObject("/CropBox"), None)
        else:
            page[NameObject("/CropBox")] = target
    if rotation:
        page[NameObject("/Rotate")] = NumberObject(rotation)
    if annotation:
        page[NameObject("/Annots")] = ArrayObject(
            [
                DictionaryObject(
                    {
                        NameObject("/Type"): NameObject("/Annot"),
                        NameObject("/Subtype"): NameObject("/Square"),
                        NameObject("/Rect"): ArrayObject([FloatObject(5), FloatObject(5), FloatObject(55), FloatObject(55)]),
                        NameObject("/C"): ArrayObject([FloatObject(1), FloatObject(0), FloatObject(0)]),
                        NameObject("/F"): NumberObject(4),
                    }
                )
            ]
        )
    if password is not None:
        writer.encrypt(password)
    output = BytesIO()
    writer.write(output)
    return output.getvalue()


def request(raw_pdf: bytes, *, limits: ResourceLimits | None = None) -> RasterRequest:
    total_pages = 1
    return RasterRequest(
        raw_pdf_bytes=raw_pdf,
        source=PDFSourceIdentity("pdfium-test", hashlib.sha256(raw_pdf).hexdigest()),
        page=PDFPageIdentity(1, total_pages),
        configuration=RasterConfiguration(),
        resource_limits=limits or ResourceLimits(),
        isolation_policy=WorkerIsolationPolicy(),
        admission=PDFAdmissionResult(True, "pdf"),
    )


class DependencyIdentityTests(unittest.TestCase):
    def test_requirements_are_exact_and_wheel_only(self) -> None:
        requirements = (REPO_ROOT / "skills/agy-ppt/requirements.txt").read_text(encoding="utf-8").splitlines()
        self.assertIn("--only-binary=:all:", requirements)
        self.assertIn("pypdfium2==5.13.0", requirements)
        self.assertFalse(any(line.startswith(("PyMuPDF", "pymupdf")) for line in requirements))

    def test_manifest_has_exact_approved_engine_and_six_hashes(self) -> None:
        manifest = json.loads(
            (REPO_ROOT / "skills/agy-ppt/governance/pdfium-renderer-artifacts.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["package"], {"name": "pypdfium2", "version": "5.13.0"})
        self.assertEqual(manifest["engine"]["version"], "153.0.7999.0")
        self.assertEqual(manifest["engine"]["build"], 7999)
        self.assertEqual(manifest["engine"]["origin"], "pdfium-binaries")
        self.assertEqual(manifest["engine"]["flags"], [])
        self.assertFalse(manifest["engine"]["v8"])
        self.assertFalse(manifest["engine"]["xfa"])
        expected_hashes = {
            "linux_x86_64": "81df25c1ab4c13ff773102d3cbea1967511d079123b067fc077bd0c4d57d91d8",
            "linux_arm64": "9ee8c2bb2e68b396ab4a763215ac100dacb6b96d0da5bebeb239a021aecc3a7e",
            "macos_x86_64": "2abedfb5c70992b19c780ed58d7f7b929e8ce8ee52c9140158f44317c90ec6c7",
            "macos_arm64": "da5c7b74eebf40b5c1fbe1de01aa1edc8827a79fb1efd999616bc20dcaf77ba4",
            "windows_x86_64": "47dcca2a8d507b5fd24f94c3c9d48fb379430f097bc20f01beff6c963ffbcedb",
            "windows_arm64": "554a0b23376460af1410e3c915906895e2dac67a086b9e6ccde0643a795d3b0d",
        }
        self.assertEqual({item["platform"]: item["sha256"] for item in manifest["artifacts"]}, expected_hashes)
        lock = (REPO_ROOT / "skills/agy-ppt/governance/pdfium-renderer-requirements.lock").read_text()
        self.assertIn("--only-binary=:all:", lock)
        self.assertIn("--require-hashes", lock)
        self.assertEqual(lock.count("--hash=sha256:"), 6)
        for item in manifest["artifacts"]:
            self.assertIn(item["sha256"], lock)

    def test_runtime_identity_and_build_identity_are_approved(self) -> None:
        from pypdfium2.version import PDFIUM_INFO, PYPDFIUM_INFO

        artifact = load_approved_artifact()
        self.assertEqual(str(PYPDFIUM_INFO), RENDERER_VERSION)
        self.assertEqual(str(PDFIUM_INFO), ENGINE_VERSION)
        self.assertEqual(PDFIUM_INFO.build, ENGINE_BUILD)
        self.assertEqual(PDFIUM_INFO.origin, ENGINE_ORIGIN)
        self.assertEqual(tuple(PDFIUM_INFO.flags), ())
        identity = approved_build_identity(artifact)
        self.assertIn(artifact["filename"], identity)
        self.assertIn(artifact["sha256"], identity)
        self.assertTrue(identity.endswith("|pdfium-build:7999|origin:pdfium-binaries|flags:none"))

    def test_license_bundle_and_sbom_exist(self) -> None:
        license_root = REPO_ROOT / "third_party/pypdfium2-5.13.0"
        expected = {
            "abseil.txt", "agg23.txt", "fast_float.txt", "freetype.txt", "icu.txt", "lcms.txt",
            "libjpeg_turbo.ijg", "libjpeg_turbo.md", "libopenjpeg.txt", "libpng.txt", "libtiff.txt",
            "llvm-libc.txt", "pdfium-binaries.txt", "simdutf.txt", "zlib.txt",
        }
        self.assertEqual({path.name for path in (license_root / "BUILD_LICENSES/common").iterdir()}, expected)
        self.assertTrue((license_root / "BUILD_LICENSES/pdfium-macos.txt").is_file())
        self.assertTrue((license_root / "BUILD_LICENSES/pdfium-linux-windows.txt").is_file())
        sbom = json.loads((REPO_ROOT / "skills/agy-ppt/governance/pdfium-renderer-sbom.json").read_text())
        self.assertEqual([item["name"] for item in sbom["components"]], ["pypdfium2", "PDFium"])


class ExactGeometryTests(unittest.TestCase):
    def test_sixty_points_is_exactly_250_pixels(self) -> None:
        self.assertEqual(outward_pixels(60), 250)
        self.assertEqual(outward_pixels(60.0), 250)

    def test_fractional_extent_rounds_outward(self) -> None:
        self.assertEqual(outward_pixels("60.001"), 251)
        self.assertEqual(outward_pixels("0.24"), 1)

    def test_rotation_swaps_pixel_axes(self) -> None:
        normal = build_geometry((0, 0, 60, 120), None, 0)
        rotated = build_geometry((0, 0, 60, 120), None, 90)
        self.assertEqual((normal.width, normal.height), (250, 500))
        self.assertEqual((rotated.width, rotated.height), (500, 250))

    def test_valid_crop_and_invalid_crop_fallback(self) -> None:
        crop = build_geometry((0, 0, 60, 120), (10, 20, 50, 100), 0)
        fallback = build_geometry((0, 0, 60, 120), (0, 0, 70, 120), 0)
        self.assertEqual((crop.selected_box, crop.width, crop.height), ("CropBox", 167, 334))
        self.assertEqual((fallback.selected_box, fallback.width, fallback.height), ("MediaBox", 250, 500))

    def test_invalid_media_and_rotation_fail_closed(self) -> None:
        for media, rotation in (((0, 0, 0, 10), 0), ((0, 0, 10, 10), 45)):
            with self.assertRaises(PDFOCRError) as caught:
                build_geometry(media, None, rotation)
            self.assertEqual(caught.exception.error_code, "OCR_PDF_INPUT_INVALID")

    def test_pixel_limit_boundary_preflight(self) -> None:
        exact = build_geometry((0, 0, 1200, 1200), None, 0)
        self.assertEqual(exact.width * exact.height, 25_000_000)
        _resource_preflight(exact, ResourceLimits())
        over = build_geometry((0, 0, "1200.24", 1200), None, 0)
        with self.assertRaises(PDFOCRError) as caught:
            _resource_preflight(over, ResourceLimits())
        self.assertEqual(caught.exception.error_code, "OCR_PDF_RESOURCE_LIMIT_EXCEEDED")

    def test_packed_bgr_stride_footprint_is_preflighted(self) -> None:
        geometry = build_geometry((0, 0, 60, 120), None, 0)
        self.assertEqual((geometry.width, geometry.height), (250, 500))
        with self.assertRaises(PDFOCRError) as caught:
            _resource_preflight(geometry, ResourceLimits(worker_memory_limit_bytes=374_999))
        self.assertEqual(caught.exception.error_code, "OCR_PDF_RESOURCE_LIMIT_EXCEEDED")


class RealRendererTests(unittest.TestCase):
    def setUp(self) -> None:
        self.renderer = PDFiumRasterizer(_worker_pythonpath=worker_paths())

    def test_rgb_no_alpha_png_and_repeatable_digest(self) -> None:
        raw = pdf_bytes()
        first = self.renderer.rasterize(request(raw))
        second = self.renderer.rasterize(request(raw))
        self.assertEqual(first.raster_bytes, second.raster_bytes)
        self.assertEqual(first.provenance.raster_digest, hashlib.sha256(first.raster_bytes).hexdigest())
        image = Image.open(BytesIO(first.raster_bytes))
        self.assertEqual(image.format, "PNG")
        self.assertEqual(image.mode, "RGB")
        self.assertEqual(image.size, (250, 500))

    def test_explicit_crop_and_inherited_crop(self) -> None:
        for inherited in (False, True):
            with self.subTest(inherited=inherited):
                result = self.renderer.rasterize(request(pdf_bytes(crop=(10, 20, 50, 100), inherited_crop=inherited)))
                self.assertEqual(result.provenance.selected_box, "CropBox")
                self.assertEqual(result.provenance.box_coordinates, (10.0, 20.0, 50.0, 100.0))
                self.assertEqual((result.provenance.width, result.provenance.height), (167, 334))

    def test_invalid_crop_falls_back_to_media(self) -> None:
        result = self.renderer.rasterize(request(pdf_bytes(crop=(0, 0, 70, 120))))
        self.assertEqual(result.provenance.selected_box, "MediaBox")
        self.assertEqual((result.provenance.width, result.provenance.height), (250, 500))

    def test_intrinsic_rotation_is_recorded_without_extra_rotation(self) -> None:
        result = self.renderer.rasterize(request(pdf_bytes(rotation=90)))
        self.assertEqual(result.provenance.effective_rotation, 90)
        self.assertEqual((result.provenance.width, result.provenance.height), (500, 250))

    def test_annotations_and_forms_are_not_rendered(self) -> None:
        result = self.renderer.rasterize(request(pdf_bytes(annotation=True)))
        image = Image.open(BytesIO(result.raster_bytes))
        self.assertEqual(image.getextrema(), ((255, 255), (255, 255), (255, 255)))
        self.assertFalse(result.provenance.render_annotations)

    def test_invalid_and_password_required_admission(self) -> None:
        invalid = b"not a PDF"
        with self.assertRaises(PDFOCRError) as caught:
            self.renderer.rasterize(request(invalid))
        self.assertEqual(caught.exception.error_code, "OCR_PDF_INPUT_INVALID")
        encrypted = pdf_bytes(password="secret")
        with self.assertRaises(PDFOCRError) as caught:
            self.renderer.rasterize(request(encrypted))
        self.assertEqual(caught.exception.error_code, "OCR_PDF_PASSWORD_REQUIRED")

    def test_dimension_and_output_limits_map_to_resource_error(self) -> None:
        with self.assertRaises(PDFOCRError) as caught:
            self.renderer.rasterize(request(pdf_bytes(width=2500, height=10)))
        self.assertEqual(caught.exception.error_code, "OCR_PDF_RESOURCE_LIMIT_EXCEEDED")
        with self.assertRaises(PDFOCRError) as caught:
            self.renderer.rasterize(
                request(pdf_bytes(), limits=ResourceLimits(max_raster_output_bytes_per_page=100))
            )
        self.assertEqual(caught.exception.error_code, "OCR_PDF_RESOURCE_LIMIT_EXCEEDED")

    def test_provenance_is_stable_complete_and_path_free(self) -> None:
        provenance = self.renderer.rasterize(request(pdf_bytes(crop=(10, 20, 50, 100)))).provenance
        payload = provenance.to_dict()
        self.assertEqual(payload["renderer_id"], "pypdfium2")
        self.assertEqual(payload["renderer_version"], "5.13.0")
        self.assertEqual(payload["renderer_engine_version"], "153.0.7999.0")
        self.assertNotIn("/", provenance.approved_build_identity)
        serialized = provenance.to_json().lower()
        for forbidden in ("timestamp", "tmp/", "users/", "environment", "cache/"):
            self.assertNotIn(forbidden, serialized)


class WorkerBoundaryTests(unittest.TestCase):
    def test_controlled_worker_failure_preserves_renderer_error_taxonomy(self) -> None:
        renderer = PDFiumRasterizer(
            _worker_module="helpers.pdfium_worker_error",
            _worker_pythonpath=worker_paths(TESTS_ROOT),
        )
        with self.assertRaises(PDFOCRError) as caught:
            renderer.rasterize(request(pdf_bytes()))
        self.assertEqual(caught.exception.error_code, "OCR_PDF_INPUT_INVALID")
        self.assertFalse(caught.exception.provider_fallback_eligible)

    def test_worker_timeout_maps_to_resource_limit(self) -> None:
        renderer = PDFiumRasterizer(
            _worker_module="helpers.pdfium_worker_timeout",
            _worker_pythonpath=worker_paths(TESTS_ROOT),
            _watchdog_grace_seconds=0.05,
        )
        limits = ResourceLimits(document_open_timeout_seconds=0.05, renderer_timeout_seconds_per_page=0.05)
        with self.assertRaises(PDFOCRError) as caught:
            renderer.rasterize(request(pdf_bytes(), limits=limits))
        self.assertEqual(caught.exception.error_code, "OCR_PDF_RESOURCE_LIMIT_EXCEEDED")
        self.assertFalse(caught.exception.provider_fallback_eligible)

    def test_abnormal_native_worker_exit_is_rasterization_failure(self) -> None:
        renderer = PDFiumRasterizer(
            _worker_module="helpers.pdfium_worker_exit",
            _worker_pythonpath=worker_paths(TESTS_ROOT),
        )
        with self.assertRaises(PDFOCRError) as caught:
            renderer.rasterize(request(pdf_bytes()))
        self.assertEqual(caught.exception.error_code, "OCR_RASTERIZATION_FAILED")

    def test_oversized_ipc_payload_is_resource_failure(self) -> None:
        renderer = PDFiumRasterizer(
            _worker_module="helpers.pdfium_worker_oversized",
            _worker_pythonpath=worker_paths(TESTS_ROOT),
        )
        limits = ResourceLimits(max_raster_output_bytes_per_page=100)
        with self.assertRaises(PDFOCRError) as caught:
            renderer.rasterize(request(pdf_bytes(), limits=limits))
        self.assertEqual(caught.exception.error_code, "OCR_PDF_RESOURCE_LIMIT_EXCEEDED")


if __name__ == "__main__":
    unittest.main()
