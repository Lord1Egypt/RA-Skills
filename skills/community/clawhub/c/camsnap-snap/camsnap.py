#!/usr/bin/env python3
"""
Camera snapshot utility - part of the camsnap skill
"""

from __future__ import annotations

import argparse
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

import cv2

__all__ = ["take_snapshot"]

logger = logging.getLogger(__name__)

_ALLOWED_EXTENSIONS = frozenset({".jpg", ".jpeg", ".png", ".bmp", ".webp"})


def _validate_output_path(path: str) -> Path:
    """Validate and normalize an output path, guarding against traversal and bad extensions."""
    resolved = Path(path).resolve()
    ext = resolved.suffix.lower()
    if ext and ext not in _ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported image extension: {ext!r}. Allowed: {sorted(_ALLOWED_EXTENSIONS)}")
    return resolved


def take_snapshot(
    output_path: Optional[str] = None,
    show_preview: bool = False,
    output_dir: str = "snapshots",
    camera_index: int = 0,
) -> Optional[str]:
    """
    Take a snapshot from the default webcam.

    Args:
        output_path: Optional path to save the image.
        show_preview: Whether to show a preview window (GUI only).
        output_dir: Directory to save if no output_path provided.
        camera_index: Camera device index (default 0).

    Returns:
        Path to saved image, or None on failure.

    Raises:
        ValueError: If output_path has an unsupported extension or traverses outside allowed dirs.
    """
    # Resolve and validate output path
    if output_path:
        dest = _validate_output_path(output_path)
        dest.parent.mkdir(parents=True, exist_ok=True)
    else:
        out_dir = Path(output_dir).resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = out_dir / f"snapshot_{timestamp}.jpg"

    cap = cv2.VideoCapture(camera_index)
    try:
        if not cap.isOpened():
            logger.error("Could not access webcam (index %d)", camera_index)
            return None

        ret, frame = cap.read()
        if not ret:
            logger.error("Failed to capture frame from webcam")
            return None

        success = cv2.imwrite(str(dest), frame)
        if not success:
            logger.error("Failed to write image to %s", dest)
            return None

        logger.info("Snapshot saved to: %s", dest)
    finally:
        cap.release()

    # Show preview only after resources are released (GUI only)
    if show_preview:
        cv2.imshow("Snapshot Preview", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return str(dest)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(description="Take webcam snapshot")
    parser.add_argument("output_path", nargs="?", help="Path to save the snapshot")
    parser.add_argument("--preview", action="store_true", help="Show preview window (GUI only)")
    parser.add_argument("--output-dir", default="./snapshots", help="Directory for auto-generated filenames")
    parser.add_argument("--camera", type=int, default=0, help="Camera device index (default: 0)")

    args = parser.parse_args()
    result = take_snapshot(args.output_path, args.preview, args.output_dir, args.camera)
    if result is None:
        raise SystemExit(1)
