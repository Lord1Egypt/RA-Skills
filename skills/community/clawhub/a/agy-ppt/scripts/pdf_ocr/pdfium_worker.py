"""Restricted subprocess entry point for Phase 15.2 PDFium rasterization."""

from __future__ import annotations

from contextlib import contextmanager
from io import BytesIO
import hashlib
import os
import signal
import sys
from typing import Any, Iterator

from .errors import PDFOCRError, PDFOCRErrorCode
from .models import PDFPageIdentity, PDFSourceIdentity, RasterConfiguration, ResourceLimits
from .pdfium_geometry import EffectivePageGeometry, build_geometry
from .pdfium_identity import (
    ENGINE_BUILD,
    ENGINE_FLAGS,
    ENGINE_ORIGIN,
    ENGINE_VERSION,
    RENDERER_ID,
    RENDERER_VERSION,
    approved_build_identity,
    load_approved_artifact,
)
from .pdfium_ipc import IPCError, PROTOCOL_VERSION, read_frame, write_frame


_MAX_RAW_PDF_BYTES = 100 * 1024 * 1024


class _StageTimeout(RuntimeError):
    pass


def _apply_worker_restrictions() -> dict[str, Any]:
    """Apply controls before signaling readiness to receive PDF bytes."""

    result: dict[str, Any] = {
        "credentials": False,
        "network": False,
        "minimal_environment": True,
        "process_group": os.name == "posix",
        "resource_limits": False,
    }
    keep_tmp = os.environ.get("TMPDIR")
    os.environ.clear()
    if keep_tmp:
        os.environ["TMPDIR"] = keep_tmp

    def deny_dangerous_runtime(event: str, _args: tuple[object, ...]) -> None:
        if event.startswith("socket.") or event in {"os.system", "subprocess.Popen"}:
            raise PermissionError("network and child-process creation are disabled in the PDFium worker")

    sys.addaudithook(deny_dangerous_runtime)

    if os.name == "posix":
        import resource

        limits = (
            (resource.RLIMIT_CORE, 0),
            (resource.RLIMIT_NOFILE, 64),
            (resource.RLIMIT_FSIZE, 256 * 1024 * 1024),
            (resource.RLIMIT_CPU, 65),
        )
        if sys.platform.startswith("linux"):
            limits += ((resource.RLIMIT_AS, 512 * 1024 * 1024),)
        for limit, value in limits:
            soft, hard = resource.getrlimit(limit)
            effective = min(value, hard) if hard != resource.RLIM_INFINITY else value
            resource.setrlimit(limit, (effective, effective))
        result["resource_limits"] = True
    return result


@contextmanager
def _stage_timeout(seconds: float) -> Iterator[None]:
    if os.name != "posix" or not hasattr(signal, "setitimer"):
        yield
        return

    def expired(_signum: int, _frame: object) -> None:
        raise _StageTimeout("PDFium worker stage timed out")

    previous = signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)


def _resource_preflight(geometry: EffectivePageGeometry, limits: ResourceLimits) -> None:
    if geometry.width > limits.max_raster_width or geometry.height > limits.max_raster_height:
        raise PDFOCRError("raster dimensions exceed configured limits", PDFOCRErrorCode.RESOURCE_LIMIT_EXCEEDED)
    pixels = geometry.width * geometry.height
    if pixels > limits.max_pixels_per_page:
        raise PDFOCRError("raster pixel product exceeds configured limit", PDFOCRErrorCode.RESOURCE_LIMIT_EXCEEDED)
    # FPDFBitmap_BGR uses three packed bytes per pixel.  Keep stride explicit
    # so the allocation calculation stays coupled to the bitmap configuration.
    stride = geometry.width * 3
    raw_footprint = stride * geometry.height
    if raw_footprint > limits.worker_memory_limit_bytes:
        raise PDFOCRError("raw raster footprint exceeds worker memory limit", PDFOCRErrorCode.RESOURCE_LIMIT_EXCEEDED)


def _resolve_geometry(raw_pdf: bytes, page_index: int, dpi: int) -> tuple[EffectivePageGeometry, int]:
    from pypdf import PdfReader
    from pypdf.errors import PdfReadError

    try:
        reader = PdfReader(BytesIO(raw_pdf), strict=True)
        if reader.is_encrypted:
            raise PDFOCRError("PDF requires a password", PDFOCRErrorCode.PASSWORD_REQUIRED)
        total_pages = len(reader.pages)
        page = reader.pages[page_index]
        media = page["/MediaBox"]
        crop = page.get("/CropBox")
        rotation = page.get("/Rotate", 0)
        geometry = build_geometry(media, crop, rotation, dpi=dpi)
    except PDFOCRError:
        raise
    except (PdfReadError, IndexError, KeyError, TypeError, ValueError, RecursionError) as exc:
        raise PDFOCRError("PDF structure or effective page geometry is invalid", PDFOCRErrorCode.INPUT_INVALID) from exc
    return geometry, total_pages


def _validate_runtime_identity() -> dict[str, str]:
    from pypdfium2.version import PDFIUM_INFO, PYPDFIUM_INFO

    actual_flags = tuple(str(value) for value in PDFIUM_INFO.flags)
    if (
        str(PYPDFIUM_INFO) != RENDERER_VERSION
        or str(PDFIUM_INFO) != ENGINE_VERSION
        or PDFIUM_INFO.build != ENGINE_BUILD
        or PDFIUM_INFO.origin != ENGINE_ORIGIN
        or actual_flags != ENGINE_FLAGS
    ):
        raise PDFOCRError("runtime PDFium identity is not approved", PDFOCRErrorCode.RASTERIZATION_FAILED)
    artifact = load_approved_artifact()
    return {**artifact, "build_identity": approved_build_identity(artifact)}


def _render(raw_pdf: bytes, request: dict[str, Any]) -> tuple[dict[str, Any], bytes]:
    import pypdfium2 as pdfium
    import pypdfium2.raw as pdfium_c

    limits = ResourceLimits(**request["resource_limits"])
    configuration = RasterConfiguration(**request["configuration"])
    source = PDFSourceIdentity(**request["source"])
    page_identity = PDFPageIdentity(**request["page"])
    if len(raw_pdf) > limits.max_raw_pdf_bytes:
        raise PDFOCRError("raw PDF exceeds configured byte limit", PDFOCRErrorCode.RESOURCE_LIMIT_EXCEEDED)
    if hashlib.sha256(raw_pdf).hexdigest() != source.source_digest:
        raise PDFOCRError("source digest does not identify raw PDF bytes", PDFOCRErrorCode.INPUT_INVALID)

    artifact = _validate_runtime_identity()
    try:
        with _stage_timeout(limits.document_open_timeout_seconds):
            document = pdfium.PdfDocument(raw_pdf)
    except pdfium.PdfiumError as exc:
        if exc.err_code == pdfium_c.FPDF_ERR_PASSWORD:
            raise PDFOCRError("PDF requires a password", PDFOCRErrorCode.PASSWORD_REQUIRED) from exc
        raise PDFOCRError("input is not a valid readable PDF", PDFOCRErrorCode.INPUT_INVALID) from exc
    except _StageTimeout as exc:
        raise PDFOCRError("PDF document open timed out", PDFOCRErrorCode.RESOURCE_LIMIT_EXCEEDED) from exc

    primary_error: BaseException | None = None
    try:
        if len(document) < 1 or len(document) > limits.max_page_count:
            raise PDFOCRError("PDF page count exceeds configured bounds", PDFOCRErrorCode.RESOURCE_LIMIT_EXCEEDED)
        if len(document) != page_identity.total_pages:
            raise PDFOCRError("parser and renderer page counts differ", PDFOCRErrorCode.INPUT_INVALID)
        page_index = page_identity.page - 1
        try:
            with _stage_timeout(limits.document_open_timeout_seconds):
                geometry, parser_page_count = _resolve_geometry(raw_pdf, page_index, configuration.dpi)
        except _StageTimeout as exc:
            raise PDFOCRError("PDF structure parsing timed out", PDFOCRErrorCode.RESOURCE_LIMIT_EXCEEDED) from exc
        if parser_page_count != len(document):
            raise PDFOCRError("parser and renderer page counts differ", PDFOCRErrorCode.INPUT_INVALID)
        _resource_preflight(geometry, limits)

        page = document[page_index]
        bitmap = None
        try:
            x0, y0, x1, y1 = geometry.provenance_coordinates
            page.set_cropbox(x0, y0, x1, y1)
            bitmap = pdfium.PdfBitmap.new_native(
                geometry.width,
                geometry.height,
                format=pdfium_c.FPDFBitmap_BGR,
                rev_byteorder=False,
            )
            bitmap.fill_rect((255, 255, 255, 255), 0, 0, geometry.width, geometry.height)
            with _stage_timeout(limits.renderer_timeout_seconds_per_page):
                # Flags intentionally omit FPDF_ANNOT. Forms are never initialized
                # and FPDF_FFLDraw is never called (draw_annots/may_draw_forms false).
                pdfium_c.FPDF_RenderPageBitmap(bitmap, page, 0, 0, geometry.width, geometry.height, 0, 0)
                image = bitmap.to_pil().convert("RGB")
                output = BytesIO()
                image.save(output, format="PNG", optimize=False, compress_level=9)
                png_bytes = output.getvalue()
        except _StageTimeout as exc:
            raise PDFOCRError("PDF page rendering timed out", PDFOCRErrorCode.RESOURCE_LIMIT_EXCEEDED) from exc
        finally:
            if bitmap is not None:
                bitmap.close()
            page.close()

        if image.mode != "RGB" or image.size != (geometry.width, geometry.height):
            raise PDFOCRError("rendered raster dimensions or colorspace are invalid", PDFOCRErrorCode.RASTERIZATION_FAILED)
        if len(png_bytes) > limits.max_raster_output_bytes_per_page:
            raise PDFOCRError("encoded PNG exceeds configured output limit", PDFOCRErrorCode.RESOURCE_LIMIT_EXCEEDED)
        digest = hashlib.sha256(png_bytes).hexdigest()
        header = {
            "protocol_version": PROTOCOL_VERSION,
            "status": "ok",
            "payload_length": len(png_bytes),
            "renderer_id": RENDERER_ID,
            "renderer_version": RENDERER_VERSION,
            "renderer_engine_version": ENGINE_VERSION,
            "pdfium_build": ENGINE_BUILD,
            "engine_origin": ENGINE_ORIGIN,
            "engine_flags": list(ENGINE_FLAGS),
            "approved_build_identity": artifact["build_identity"],
            "selected_box": geometry.selected_box,
            "box_coordinates": list(geometry.provenance_coordinates),
            "effective_rotation": geometry.effective_rotation,
            "width": geometry.width,
            "height": geometry.height,
            "draw_annots": False,
            "may_draw_forms": False,
            "raster_digest": digest,
        }
        return header, png_bytes
    except BaseException as exc:
        primary_error = exc
        raise
    finally:
        try:
            document.close()
        except Exception as exc:
            if primary_error is None:
                raise PDFOCRError("PDFium document cleanup failed", PDFOCRErrorCode.CLEANUP_FAILED) from exc


def _error_header(error: PDFOCRError) -> dict[str, Any]:
    diagnostic = str(error).replace("\n", " ")[:512]
    return {
        "protocol_version": PROTOCOL_VERSION,
        "status": "error",
        "payload_length": 0,
        "error_code": error.error_code,
        "diagnostic": diagnostic,
    }


def main() -> int:
    try:
        isolation = _apply_worker_restrictions()
        write_frame(
            sys.stdout.buffer,
            {
                "protocol_version": PROTOCOL_VERSION,
                "status": "ready",
                "payload_length": 0,
                "isolation": isolation,
            },
        )
        request, raw_pdf = read_frame(sys.stdin.buffer, max_payload=_MAX_RAW_PDF_BYTES)
        header, png_bytes = _render(raw_pdf, request)
        write_frame(sys.stdout.buffer, header, png_bytes)
        return 0
    except PDFOCRError as exc:
        write_frame(sys.stdout.buffer, _error_header(exc))
        return 0
    except (IPCError, KeyError, TypeError, ValueError) as exc:
        error = PDFOCRError(str(exc), PDFOCRErrorCode.INPUT_INVALID)
        write_frame(sys.stdout.buffer, _error_header(error))
        return 0
    except BaseException:
        return 70


if __name__ == "__main__":
    raise SystemExit(main())
