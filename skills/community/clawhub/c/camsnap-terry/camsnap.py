#!/usr/bin/env python3
"""
Camera snapshot utility - part of the camsnap skill.

Captures a single frame from the default webcam and saves it to disk.
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

import cv2

ALLOWED_EXTENSIONS: set[str] = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
DEFAULT_OUTPUT_DIR: str = "snapshots"


def _validate_output_path(output_path: str) -> str:
    """Resolve and validate an output path, guarding against traversal."""
    resolved = Path(output_path).resolve()
    # Block path traversal outside cwd tree
    cwd = Path.cwd().resolve()
    try:
        resolved.relative_to(cwd)
    except ValueError:
        raise ValueError(
            f"Output path escapes working directory: {output_path}"
        )
    ext = resolved.suffix.lower()
    if ext and ext not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported image extension '{ext}'. Allowed: {sorted(ALLOWED_EXTENSIONS)}"
        )
    if not ext:
        # Default to .jpg when no extension given
        resolved = resolved.with_suffix(".jpg")
    return str(resolved)


def take_snapshot(
    output_path: str | None = None,
    show_preview: bool = False,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> str | None:
    """
    Take a snapshot from the default webcam.

    Args:
        output_path: Optional path to save the image.
        show_preview: Whether to show a preview window (GUI only).
        output_dir: Directory to save if no output_path provided.

    Returns:
        Path to saved image, or None on failure.
    """
    # Generate output path if not provided
    if output_path:
        output_path = _validate_output_path(output_path)
    else:
        output_dir = _validate_output_path(output_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"snapshot_{timestamp}.jpg")

    # Ensure parent directory exists
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    cap: cv2.VideoCapture | None = None
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not access webcam", file=sys.stderr)
            return None

        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame", file=sys.stderr)
            return None

        success = cv2.imwrite(output_path, frame)
        if not success:
            print(f"Error: Failed to write image to {output_path}", file=sys.stderr)
            return None

        print(f"✅ Snapshot saved to: {output_path}")

        if show_preview:
            cv2.imshow("Snapshot Preview", frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return output_path
    finally:
        if cap is not None:
            cap.release()


def main() -> None:
    parser = argparse.ArgumentParser(description="Take webcam snapshot")
    parser.add_argument("output_path", nargs="?", help="Path to save the snapshot")
    parser.add_argument("--preview", action="store_true", help="Show preview window (GUI only)")
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory for auto-generated filenames (default: {DEFAULT_OUTPUT_DIR})",
    )

    args = parser.parse_args()

    try:
        result = take_snapshot(args.output_path, args.preview, args.output_dir)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if result is None:
        sys.exit(1)


if __name__ == "__main__":
    main()
