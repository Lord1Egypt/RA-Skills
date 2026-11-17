"""Restricted subprocess for Phase 15.3 Pillow image preparation."""

from __future__ import annotations

from contextlib import contextmanager
from io import BytesIO
import os
import signal
import sys
import warnings
from typing import Any, Iterator

from source_grounding import compute_source_digest

from .errors import ImageOCRError, ImageOCRErrorCode
from .ipc import IPCError, PROTOCOL_VERSION, read_frame, write_frame
from .models import ImagePreparationConfiguration, ImagePreparationProvenance, ImageResourceLimits, ImageSourceIdentity


_MAX_RAW_IMAGE_BYTES = 100 * 1024 * 1024
_ALLOWED_FORMATS = frozenset({"PNG", "JPEG", "TIFF"})
_ALLOWED_MODES = frozenset({"1", "L", "LA", "P", "RGB", "RGBA", "CMYK"})


class _StageTimeout(RuntimeError):
    pass


def _apply_worker_restrictions() -> dict[str, Any]:
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
            raise PermissionError("network and child-process creation are disabled in image worker")

    sys.addaudithook(deny_dangerous_runtime)
    if os.name == "posix":
        import resource

        controls = (
            (resource.RLIMIT_CORE, 0),
            (resource.RLIMIT_NOFILE, 64),
            (resource.RLIMIT_FSIZE, 256 * 1024 * 1024),
            (resource.RLIMIT_CPU, 35),
        )
        if sys.platform.startswith("linux"):
            controls += ((resource.RLIMIT_AS, 512 * 1024 * 1024),)
        for resource_id, value in controls:
            _soft, hard = resource.getrlimit(resource_id)
            effective = min(value, hard) if hard != resource.RLIM_INFINITY else value
            resource.setrlimit(resource_id, (effective, effective))
        result["resource_limits"] = True
    return result


@contextmanager
def _stage_timeout(seconds: float) -> Iterator[None]:
    if os.name != "posix" or not hasattr(signal, "setitimer"):
        yield
        return

    def expired(_signum: int, _frame: object) -> None:
        raise _StageTimeout("image preparation timed out")

    previous = signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)


def _resource_preflight(width: int, height: int, limits: ImageResourceLimits) -> None:
    if width > limits.max_width or height > limits.max_height:
        raise ImageOCRError("image dimensions exceed configured limits", ImageOCRErrorCode.RESOURCE_LIMIT_EXCEEDED)
    pixels = width * height
    if pixels > limits.max_pixels:
        raise ImageOCRError("image pixel count exceeds configured limit", ImageOCRErrorCode.RESOURCE_LIMIT_EXCEEDED)
    if pixels * 4 > limits.max_decoded_packed_bytes:
        raise ImageOCRError("estimated decoded footprint exceeds configured limit", ImageOCRErrorCode.RESOURCE_LIMIT_EXCEEDED)


def _convert_to_rgb(image: Any) -> tuple[Any, str]:
    from PIL import Image

    mode = image.mode
    if mode == "RGB":
        return image.copy(), "preserve_rgb"
    if mode in {"1", "L"}:
        return image.convert("RGB"), "grayscale_channel_replication"
    if mode in {"LA", "RGBA"} or (mode == "P" and "transparency" in image.info):
        rgba = image.convert("RGBA")
        white = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        composite = None
        try:
            composite = Image.alpha_composite(white, rgba)
            return composite.convert("RGB"), "alpha_composite_on_white"
        finally:
            rgba.close()
            white.close()
            if composite is not None:
                composite.close()
    if mode == "P":
        return image.convert("RGB"), "palette_to_rgb"
    if mode == "CMYK":
        return image.convert("RGB"), "cmyk_ycck_to_rgb"
    raise ImageOCRError("image color mode is unsupported", ImageOCRErrorCode.FORMAT_UNSUPPORTED)


def _prepare(raw_image: bytes, request: dict[str, Any]) -> tuple[dict[str, Any], bytes]:
    from PIL import Image, ImageOps, UnidentifiedImageError, __version__ as pillow_version

    limits = ImageResourceLimits(**request["resource_limits"])
    configuration = ImagePreparationConfiguration(**request["configuration"])
    source = ImageSourceIdentity(**request["source"])
    if len(raw_image) > limits.max_raw_image_bytes:
        raise ImageOCRError("raw image exceeds configured byte limit", ImageOCRErrorCode.RESOURCE_LIMIT_EXCEEDED)
    if compute_source_digest(raw_image) != source.source_digest:
        raise ImageOCRError("source digest does not identify raw image bytes", ImageOCRErrorCode.INPUT_INVALID)

    image = None
    oriented = None
    rgb = None
    primary_error: BaseException | None = None
    try:
        with _stage_timeout(limits.preparation_timeout_seconds), warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            image = Image.open(BytesIO(raw_image))
            source_format = image.format
            if source_format not in _ALLOWED_FORMATS:
                raise ImageOCRError("image format is outside Phase 15.3", ImageOCRErrorCode.FORMAT_UNSUPPORTED)
            frame_count = getattr(image, "n_frames", 1)
            if isinstance(frame_count, bool) or not isinstance(frame_count, int) or frame_count != 1:
                raise ImageOCRError("multi-frame image is outside Phase 15.3", ImageOCRErrorCode.FORMAT_UNSUPPORTED)
            original_width, original_height = image.size
            original_mode = image.mode
            if original_mode not in _ALLOWED_MODES:
                raise ImageOCRError("image color mode is unsupported", ImageOCRErrorCode.FORMAT_UNSUPPORTED)
            _resource_preflight(original_width, original_height, limits)
            exif = image.getexif()
            orientation_value = exif.get(274)
            if orientation_value is not None and (
                isinstance(orientation_value, bool)
                or not isinstance(orientation_value, int)
                or orientation_value not in range(1, 9)
            ):
                raise ImageOCRError("EXIF orientation is invalid", ImageOCRErrorCode.INPUT_INVALID)
            orientation = orientation_value if isinstance(orientation_value, int) and not isinstance(orientation_value, bool) and orientation_value in range(1, 9) else None
            icc_present = bool(image.info.get("icc_profile"))
            image.load()
            oriented = ImageOps.exif_transpose(image)
            rgb, conversion = _convert_to_rgb(oriented)
            prepared_width, prepared_height = rgb.size
            _resource_preflight(prepared_width, prepared_height, limits)
            # Pillow image copies may retain source metadata in ``info``.  The
            # Phase 15.3 provider input intentionally contains pixels only.
            rgb.info.clear()
            output = BytesIO()
            rgb.save(output, format="PNG", optimize=False, compress_level=9)
            png_bytes = output.getvalue()
    except ImageOCRError as exc:
        primary_error = exc
        raise
    except (_StageTimeout, Image.DecompressionBombWarning, Image.DecompressionBombError, MemoryError) as exc:
        primary_error = exc
        raise ImageOCRError("image preparation exceeded resource limits", ImageOCRErrorCode.RESOURCE_LIMIT_EXCEEDED) from exc
    except (UnidentifiedImageError, OSError, SyntaxError, ValueError, EOFError) as exc:
        primary_error = exc
        raise ImageOCRError("image input is malformed or truncated", ImageOCRErrorCode.INPUT_INVALID) from exc
    except Exception as exc:
        primary_error = exc
        raise ImageOCRError("image decoder or preparation failed", ImageOCRErrorCode.DECODE_FAILED) from exc
    finally:
        closed: set[int] = set()
        for prepared_object in (rgb, oriented, image):
            if prepared_object is None or id(prepared_object) in closed:
                continue
            closed.add(id(prepared_object))
            try:
                prepared_object.close()
            except Exception as exc:
                if primary_error is None:
                    raise ImageOCRError("image decoder cleanup failed", ImageOCRErrorCode.CLEANUP_FAILED) from exc

    if len(png_bytes) > limits.max_prepared_png_bytes:
        raise ImageOCRError("prepared PNG exceeds configured limit", ImageOCRErrorCode.RESOURCE_LIMIT_EXCEEDED)
    provenance = ImagePreparationProvenance(
        decoder_id="Pillow",
        decoder_version=pillow_version,
        source_format=source_format,
        original_width=original_width,
        original_height=original_height,
        original_mode=original_mode,
        exif_orientation=orientation,
        orientation_transform_applied=orientation in range(2, 9) if orientation is not None else False,
        icc_profile_present=icc_present,
        alpha_policy=configuration.alpha_policy,
        color_conversion_policy=conversion,
        target_format=configuration.target_format,
        target_mode=configuration.target_mode,
        prepared_width=prepared_width,
        prepared_height=prepared_height,
        prepared_image_digest=compute_source_digest(png_bytes),
    )
    return {
        "protocol_version": PROTOCOL_VERSION,
        "status": "ok",
        "payload_length": len(png_bytes),
        "provenance": provenance.to_dict(),
    }, png_bytes


def main() -> int:
    isolation = _apply_worker_restrictions()
    write_frame(sys.stdout.buffer, {"protocol_version": PROTOCOL_VERSION, "status": "ready", "payload_length": 0, "isolation": isolation})
    try:
        request, raw_image = read_frame(sys.stdin.buffer, max_payload=_MAX_RAW_IMAGE_BYTES)
        response, payload = _prepare(raw_image, request)
        write_frame(sys.stdout.buffer, response, payload)
        return 0
    except ImageOCRError as exc:
        write_frame(sys.stdout.buffer, {"protocol_version": PROTOCOL_VERSION, "status": "error", "payload_length": 0, "error_code": exc.error_code, "diagnostic": str(exc)[:512]})
        return 0
    except (IPCError, KeyError, TypeError, ValueError) as exc:
        write_frame(sys.stdout.buffer, {"protocol_version": PROTOCOL_VERSION, "status": "error", "payload_length": 0, "error_code": ImageOCRErrorCode.INPUT_INVALID.value, "diagnostic": str(exc)[:512]})
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
