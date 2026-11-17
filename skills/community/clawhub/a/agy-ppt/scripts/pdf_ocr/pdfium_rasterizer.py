"""Parent-side isolated PDFium implementation of the PDFRasterizer boundary."""

from __future__ import annotations

import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time

from .errors import PDFOCRError, PDFOCRErrorCode
from .models import RasterProvenance
from .pdfium_identity import (
    ENGINE_VERSION,
    RENDERER_ID,
    RENDERER_VERSION,
    approved_build_identity,
    load_approved_artifact,
)
from .pdfium_ipc import IPCError, PROTOCOL_VERSION, canonical_header, read_frame_deadline, write_deadline
from .rasterizer import PDFRasterizer, RasterRequest, RasterResult


class PDFiumRasterizer(PDFRasterizer):
    """Rasterize one PDF page in a killable, restricted subprocess."""

    def __init__(
        self,
        *,
        _worker_module: str = "pdf_ocr.pdfium_worker",
        _worker_pythonpath: str | None = None,
        _watchdog_grace_seconds: float = 5.0,
    ) -> None:
        self._worker_module = _worker_module
        self._worker_pythonpath = _worker_pythonpath
        self._watchdog_grace_seconds = _watchdog_grace_seconds

    @staticmethod
    def _terminate_group(process: subprocess.Popen[bytes]) -> None:
        if process.poll() is not None:
            return
        try:
            if os.name == "posix":
                os.killpg(process.pid, signal.SIGKILL)
            else:
                process.kill()
        finally:
            process.wait(timeout=5)

    def _environment(self, temporary_directory: str) -> dict[str, str]:
        scripts_root = str(Path(__file__).resolve().parents[1])
        pythonpath = scripts_root
        if self._worker_pythonpath:
            pythonpath += os.pathsep + self._worker_pythonpath
        return {
            "PYTHONIOENCODING": "utf-8",
            "PYTHONNOUSERSITE": "1",
            "PYTHONPATH": pythonpath,
            "TMPDIR": temporary_directory,
        }

    def rasterize(self, request: RasterRequest) -> RasterResult:
        artifact = load_approved_artifact()
        expected_build = approved_build_identity(artifact)
        limits = request.resource_limits
        request_header = {
            "protocol_version": PROTOCOL_VERSION,
            "payload_length": len(request.raw_pdf_bytes),
            "source": request.source.to_dict(),
            "page": {"page": request.page.page, "total_pages": request.page.total_pages},
            "configuration": request.configuration.to_dict(),
            "resource_limits": request.resource_limits.to_dict(),
        }
        overall_seconds = (
            limits.document_open_timeout_seconds
            + limits.renderer_timeout_seconds_per_page
            + self._watchdog_grace_seconds
        )
        deadline = time.monotonic() + overall_seconds
        command = (sys.executable, "-s", "-m", self._worker_module)
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0

        with tempfile.TemporaryDirectory(prefix="agy-pdfium-worker-") as temporary_directory:
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                cwd=temporary_directory,
                env=self._environment(temporary_directory),
                close_fds=True,
                start_new_session=os.name == "posix",
                creationflags=creationflags,
            )
            assert process.stdin is not None and process.stdout is not None
            primary_error: BaseException | None = None
            try:
                ready, _ = read_frame_deadline(process.stdout.fileno(), max_payload=0, deadline=deadline)
                if ready.get("status") != "ready":
                    raise IPCError("PDFium worker did not enter restricted ready state")
                isolation = ready.get("isolation")
                if not isinstance(isolation, dict) or isolation.get("credentials") is not False or isolation.get("network") is not False:
                    raise IPCError("PDFium worker isolation state is invalid")

                write_deadline(process.stdin.fileno(), canonical_header(request_header), deadline)
                write_deadline(process.stdin.fileno(), request.raw_pdf_bytes, deadline)
                process.stdin.close()
                response, png_bytes = read_frame_deadline(
                    process.stdout.fileno(),
                    max_payload=limits.max_raster_output_bytes_per_page,
                    deadline=deadline,
                )
                try:
                    exit_code = process.wait(timeout=max(0.1, deadline - time.monotonic()))
                except subprocess.TimeoutExpired as exc:
                    raise TimeoutError("PDFium worker watchdog expired") from exc
                if exit_code != 0:
                    raise IPCError("PDFium worker exited abnormally")
                if os.read(process.stdout.fileno(), 1):
                    raise IPCError("PDFium worker returned trailing IPC data")
            except TimeoutError as exc:
                primary_error = exc
                self._terminate_group(process)
                raise PDFOCRError("PDFium worker watchdog expired", PDFOCRErrorCode.RESOURCE_LIMIT_EXCEEDED) from exc
            except IPCError as exc:
                primary_error = exc
                self._terminate_group(process)
                code = PDFOCRErrorCode.RESOURCE_LIMIT_EXCEEDED if "exceeds configured limit" in str(exc) else PDFOCRErrorCode.RASTERIZATION_FAILED
                raise PDFOCRError(str(exc), code) from exc
            except BaseException as exc:
                primary_error = exc
                self._terminate_group(process)
                raise
            finally:
                if process.poll() is None:
                    try:
                        self._terminate_group(process)
                    except Exception as exc:
                        if primary_error is None:
                            raise PDFOCRError("PDFium worker cleanup failed", PDFOCRErrorCode.CLEANUP_FAILED) from exc
                try:
                    if process.stdin is not None and not process.stdin.closed:
                        process.stdin.close()
                    if process.stdout is not None and not process.stdout.closed:
                        process.stdout.close()
                except Exception as exc:
                    if primary_error is None:
                        raise PDFOCRError("PDFium worker IPC cleanup failed", PDFOCRErrorCode.CLEANUP_FAILED) from exc

        if response.get("status") == "error":
            code = response.get("error_code")
            diagnostic = response.get("diagnostic")
            if not isinstance(diagnostic, str) or len(diagnostic) > 512:
                diagnostic = "PDFium worker reported a controlled failure"
            try:
                raise PDFOCRError(diagnostic, code)
            except ValueError as exc:
                raise PDFOCRError("PDFium worker returned an invalid error code", PDFOCRErrorCode.RASTERIZATION_FAILED) from exc
        if response.get("status") != "ok":
            raise PDFOCRError("PDFium worker returned an invalid status", PDFOCRErrorCode.RASTERIZATION_FAILED)

        expected_identity = {
            "renderer_id": RENDERER_ID,
            "renderer_version": RENDERER_VERSION,
            "renderer_engine_version": ENGINE_VERSION,
            "approved_build_identity": expected_build,
        }
        if any(response.get(name) != value for name, value in expected_identity.items()):
            raise PDFOCRError("PDFium worker returned an unapproved identity", PDFOCRErrorCode.RASTERIZATION_FAILED)
        if response.get("draw_annots") is not False or response.get("may_draw_forms") is not False:
            raise PDFOCRError("PDFium worker enabled annotations or forms", PDFOCRErrorCode.RASTERIZATION_FAILED)

        provenance = RasterProvenance(
            renderer_id=RENDERER_ID,
            renderer_version=RENDERER_VERSION,
            renderer_engine_version=ENGINE_VERSION,
            approved_build_identity=expected_build,
            dpi=request.configuration.dpi,
            output_format=request.configuration.output_format,
            colorspace=request.configuration.colorspace,
            alpha=request.configuration.alpha,
            rotation_policy=request.configuration.rotation_policy,
            effective_rotation=response.get("effective_rotation"),
            box_policy=request.configuration.box_policy,
            selected_box=response.get("selected_box"),
            box_coordinates=tuple(response.get("box_coordinates", ())),
            render_annotations=request.configuration.render_annotations,
            semantic_preprocessing=request.configuration.semantic_preprocessing,
            width=response.get("width"),
            height=response.get("height"),
            raster_digest=response.get("raster_digest"),
        )
        return RasterResult(raster_bytes=png_bytes, provenance=provenance)
