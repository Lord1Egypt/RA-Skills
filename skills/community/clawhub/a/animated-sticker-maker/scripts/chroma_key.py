#!/usr/bin/env python3
"""Remove a flat chroma background from a raster image using Pillow and NumPy."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image


def parse_hex_color(value: str) -> np.ndarray:
    value = value.strip().lstrip("#")
    if len(value) != 6:
        raise argparse.ArgumentTypeError("key must be 'auto' or a six-digit RGB hex color")
    try:
        return np.array([int(value[i : i + 2], 16) for i in (0, 2, 4)], dtype=np.float32)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("key must be 'auto' or a six-digit RGB hex color") from exc


def border_pixels(rgb: np.ndarray, border_width: int) -> np.ndarray:
    height, width, _ = rgb.shape
    border_width = max(1, min(border_width, height // 2, width // 2))
    return np.concatenate(
        [
            rgb[:border_width].reshape(-1, 3),
            rgb[-border_width:].reshape(-1, 3),
            rgb[:, :border_width].reshape(-1, 3),
            rgb[:, -border_width:].reshape(-1, 3),
        ],
        axis=0,
    )


def estimate_border_key(rgb: np.ndarray, border_width: int) -> np.ndarray:
    border = border_pixels(rgb, border_width)
    # Median resists small subject protrusions and antialiasing along the canvas edge.
    return np.median(border, axis=0).astype(np.float32)


def remove_chroma(
    image: Image.Image,
    key: np.ndarray,
    transparent_threshold: float,
    opaque_threshold: float,
    despill: bool,
) -> Image.Image:
    if opaque_threshold <= transparent_threshold:
        raise ValueError("opaque threshold must be greater than transparent threshold")

    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32)
    rgb = rgba[..., :3]
    source_alpha = rgba[..., 3] / 255.0
    distance = np.linalg.norm(rgb - key.reshape(1, 1, 3), axis=2)
    matte = np.clip(
        (distance - transparent_threshold) / (opaque_threshold - transparent_threshold),
        0.0,
        1.0,
    )
    alpha = source_alpha * matte

    if despill:
        partial = (alpha > 0.02) & (alpha < 0.995)
        safe_alpha = np.maximum(alpha, 0.02)[..., None]
        recovered = (rgb - (1.0 - alpha[..., None]) * key.reshape(1, 1, 3)) / safe_alpha
        recovered = np.clip(recovered, 0.0, 255.0)
        rgb = np.where(partial[..., None], recovered, rgb)

    output = np.empty_like(rgba, dtype=np.uint8)
    output[..., :3] = np.rint(np.clip(rgb, 0.0, 255.0)).astype(np.uint8)
    output[..., 3] = np.rint(alpha * 255.0).astype(np.uint8)
    output[output[..., 3] == 0, :3] = 0
    return Image.fromarray(output, mode="RGBA")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--key",
        default="auto",
        help="'auto' to estimate from the border or a six-digit RGB hex color",
    )
    parser.add_argument("--border-width", type=int, default=8)
    parser.add_argument("--transparent-threshold", type=float)
    parser.add_argument("--opaque-threshold", type=float, default=180.0)
    parser.add_argument("--despill", action="store_true")
    args = parser.parse_args()

    image = Image.open(args.input)
    rgb = np.asarray(image.convert("RGB"), dtype=np.float32)
    key = estimate_border_key(rgb, args.border_width) if args.key == "auto" else parse_hex_color(args.key)
    transparent_threshold = (
        12.0 if args.transparent_threshold is None else args.transparent_threshold
    )
    if args.key == "auto":
        # Image generators often introduce a small background gradient even when
        # asked for a flat color. The subject must not touch the border, so auto-key
        # mode always covers the full observed border variation. Callers that need a
        # deliberately lower threshold must provide an explicit key.
        border = border_pixels(rgb, args.border_width)
        border_distance = np.linalg.norm(border - key.reshape(1, 3), axis=1)
        transparent_threshold = max(transparent_threshold, float(border_distance.max()) + 2.0)
    result = remove_chroma(
        image,
        key,
        transparent_threshold,
        args.opaque_threshold,
        args.despill,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.save(args.output)
    key_hex = "#" + "".join(f"{round(channel):02X}" for channel in key)
    alpha = np.asarray(result.getchannel("A"))
    print(f"Wrote {args.output}")
    print(f"Key color: {key_hex}")
    print(f"Transparent threshold: {transparent_threshold:.2f}")
    print(f"Transparent pixels: {int(np.count_nonzero(alpha == 0))}/{alpha.size}")
    print(f"Partially transparent pixels: {int(np.count_nonzero((alpha > 0) & (alpha < 255)))}/{alpha.size}")


if __name__ == "__main__":
    main()
