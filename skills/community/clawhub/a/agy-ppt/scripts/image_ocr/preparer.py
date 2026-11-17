"""Parent-side restricted Pillow image preparation boundary."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time

from source_grounding import compute_source_digest

from .errors import ImageOCRError, ImageOCRErrorCode
from .ipc import IPCError, PROTOCOL_VERSION, canonical_header, read_frame_deadline, write_deadline
from .models import ImagePreparationConfiguration, ImagePreparationProvenance, ImageResourceLimits, ImageSourceIdentity, PreparedImage


@dataclass(frozen=True)
class ImagePreparationRequest:
    raw_image_bytes: bytes
    source: ImageSourceIdentity
    configuration: ImagePreparationConfiguration
    resource_limits: ImageResourceLimits

    def __post_init__(self) -> None:
        if not isinstance(self.raw_image_bytes, bytes):
            raise ImageOCRError("raw image input must be immutable bytes", ImageOCRErrorCode.INPUT_INVALID)
        if not isinstance(self.source, ImageSourceIdentity):
            raise ImageOCRError("image source identity is invalid", ImageOCRErrorCode.INPUT_INVALID)
        if not isinstance(self.configuration, ImagePreparationConfiguration):
            raise ImageOCRError("image preparation configuration is invalid", ImageOCRErrorCode.DECODE_FAILED)
        if not isinstance(self.resource_limits, ImageResourceLimits):
            raise ImageOCRError("image resource limits are invalid", ImageOCRErrorCode.RESOURCE_LIMIT_EXCEEDED)
        if len(self.raw_image_bytes) > self.resource_limits.max_raw_image_bytes:
            raise ImageOCRError("raw image exceeds configured byte limit", ImageOCRErrorCode.RESOURCE_LIMIT_EXCEEDED)
        if compute_source_digest(self.raw_image_bytes) != self.source.source_digest:
            raise ImageOCRError("source digest does not identify original image bytes", ImageOCRErrorCode.INPUT_INVALID)


class ImagePreparer(ABC):
    @abstractmethod
    def prepare(self, request: ImagePreparationRequest) -> PreparedImage:
        """Return a canonical prepared RGB PNG and derived provenance."""


class PillowImagePreparer(ImagePreparer):
    """Prepare one standalone image in a killable restricted subprocess."""

    def __init__(self, *, _worker_module: str = "image_ocr.worker", _worker_pythonpath: str | None = None, _watchdog_grace_seconds: float = 5.0) -> None:
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
        pythonpath = str(Path(__file__).resolve().parents[1])
        if self._worker_pythonpath:
            pythonpath += os.pathsep + self._worker_pythonpath
        return {"PYTHONIOENCODING": "utf-8", "PYTHONNOUSERSITE": "1", "PYTHONPATH": pythonpath, "TMPDIR": temporary_directory}

    def prepare(self, request: ImagePreparationRequest) -> PreparedImage:
        if not isinstance(request, ImagePreparationRequest):
            raise ImageOCRError("image preparation request is invalid", ImageOCRErrorCode.INPUT_INVALID)
        limits = request.resource_limits
        header = {
            "protocol_version": PROTOCOL_VERSION,
            "payload_length": len(request.raw_image_bytes),
            "source": request.source.to_dict(),
            "configuration": request.configuration.to_dict(),
            "resource_limits": limits.to_dict(),
        }
        deadline = time.monotonic() + limits.preparation_timeout_seconds + self._watchdog_grace_seconds
        command = (sys.executable, "-s", "-m", self._worker_module)
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
        with tempfile.TemporaryDirectory(prefix="agy-image-worker-") as temporary_directory:
            process = subprocess.Popen(
                command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                cwd=temporary_directory, env=self._environment(temporary_directory), close_fds=True,
                start_new_session=os.name == "posix", creationflags=creationflags,
            )
            assert process.stdin is not None and process.stdout is not None
            primary_error: BaseException | None = None
            try:
                ready, _ = read_frame_deadline(process.stdout.fileno(), max_payload=0, deadline=deadline)
                isolation = ready.get("isolation")
                if ready.get("status") != "ready" or not isinstance(isolation, dict) or isolation.get("credentials") is not False or isolation.get("network") is not False:
                    raise IPCError("image worker did not enter restricted ready state")
                write_deadline(process.stdin.fileno(), canonical_header(header), deadline)
                write_deadline(process.stdin.fileno(), request.raw_image_bytes, deadline)
                process.stdin.close()
                response, png_bytes = read_frame_deadline(process.stdout.fileno(), max_payload=limits.max_prepared_png_bytes, deadline=deadline)
                try:
                    exit_code = process.wait(timeout=max(0.1, deadline - time.monotonic()))
                except subprocess.TimeoutExpired as exc:
                    raise TimeoutError("image worker watchdog expired") from exc
                if exit_code != 0:
                    raise IPCError("image worker exited abnormally")
                if os.read(process.stdout.fileno(), 1):
                    raise IPCError("image worker returned trailing IPC data")
            except TimeoutError as exc:
                primary_error = exc
                try:
                    self._terminate_group(process)
                except Exception:
                    pass
                raise ImageOCRError("image worker watchdog expired", ImageOCRErrorCode.RESOURCE_LIMIT_EXCEEDED) from exc
            except IPCError as exc:
                primary_error = exc
                try:
                    self._terminate_group(process)
                except Exception:
                    pass
                code = ImageOCRErrorCode.RESOURCE_LIMIT_EXCEEDED if "exceeds configured limit" in str(exc) else ImageOCRErrorCode.DECODE_FAILED
                raise ImageOCRError(str(exc), code) from exc
            except BaseException as exc:
                primary_error = exc
                try:
                    self._terminate_group(process)
                except Exception:
                    pass
                raise
            finally:
                if process.poll() is None:
                    try:
                        self._terminate_group(process)
                    except Exception as exc:
                        if primary_error is None:
                            raise ImageOCRError("image worker cleanup failed", ImageOCRErrorCode.CLEANUP_FAILED) from exc
                try:
                    if process.stdin is not None and not process.stdin.closed:
                        process.stdin.close()
                    if process.stdout is not None and not process.stdout.closed:
                        process.stdout.close()
                except Exception as exc:
                    if primary_error is None:
                        raise ImageOCRError("image worker IPC cleanup failed", ImageOCRErrorCode.CLEANUP_FAILED) from exc

        if response.get("status") == "error":
            diagnostic = response.get("diagnostic")
            if not isinstance(diagnostic, str) or len(diagnostic) > 512:
                diagnostic = "image worker reported a controlled failure"
            try:
                raise ImageOCRError(diagnostic, response.get("error_code"))
            except ValueError as exc:
                raise ImageOCRError("image worker returned an invalid error code", ImageOCRErrorCode.DECODE_FAILED) from exc
        if response.get("status") != "ok":
            raise ImageOCRError("image worker returned invalid status", ImageOCRErrorCode.DECODE_FAILED)
        try:
            provenance = ImagePreparationProvenance(**response["provenance"])
        except (KeyError, TypeError, ImageOCRError) as exc:
            raise ImageOCRError("image worker returned invalid provenance", ImageOCRErrorCode.DECODE_FAILED) from exc
        if len(png_bytes) > limits.max_prepared_png_bytes:
            raise ImageOCRError("prepared PNG exceeds configured limit", ImageOCRErrorCode.RESOURCE_LIMIT_EXCEEDED)
        if provenance.prepared_width > limits.max_width or provenance.prepared_height > limits.max_height or provenance.prepared_width * provenance.prepared_height > limits.max_pixels:
            raise ImageOCRError("prepared image dimensions exceed configured limits", ImageOCRErrorCode.RESOURCE_LIMIT_EXCEEDED)
        return PreparedImage(png_bytes, provenance)
