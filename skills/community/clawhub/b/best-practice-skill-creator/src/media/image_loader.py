"""Load and process image sequences for MLLM analysis."""

import base64
import io
from pathlib import Path

from PIL import Image


def load_image_sequence(
    input_path: str,
    supported_formats: list[str] | None = None,
    max_resolution: tuple[int, int] = (1280, 720),
) -> list[str]:
    """Load images from a directory or single file, return as base64 JPEGs.

    Args:
        input_path: Path to an image file or directory of images.
        supported_formats: List of supported extensions (without dot).
        max_resolution: Maximum (width, height) for resizing.

    Returns:
        List of base64-encoded JPEG strings, sorted by filename.
    """
    if supported_formats is None:
        supported_formats = ["png", "jpg", "jpeg", "webp", "bmp"]

    path = Path(input_path)

    if path.is_file():
        return [_encode_image(path, max_resolution)]

    if path.is_dir():
        image_files = sorted(
            f
            for f in path.iterdir()
            if f.is_file() and f.suffix.lstrip(".").lower() in supported_formats
        )
        if not image_files:
            raise FileNotFoundError(
                f"No supported images found in: {input_path} "
                f"(supported: {supported_formats})"
            )
        return [_encode_image(f, max_resolution) for f in image_files]

    raise FileNotFoundError(f"Input path not found: {input_path}")


def _encode_image(
    image_path: Path, max_resolution: tuple[int, int]
) -> str:
    """Load a single image, resize, and encode as base64 JPEG."""
    img = Image.open(image_path)
    img = img.convert("RGB")
    img.thumbnail(max_resolution, Image.LANCZOS)

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode("utf-8")
