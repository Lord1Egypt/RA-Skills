#!/usr/bin/env python3
"""Create circular PNG images with transparent corners."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageChops, ImageDraw
except ImportError as exc:  # pragma: no cover - exercised only without Pillow
    raise SystemExit(
        "Pillow is required. Install it with: python -m pip install pillow"
    ) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a PNG image into a circular PNG with transparency."
    )
    parser.add_argument("input", type=Path, help="Path to the source PNG image.")
    parser.add_argument("output", type=Path, help="Path for the generated PNG image.")
    parser.add_argument(
        "--fit",
        choices=("cover", "contain"),
        default="cover",
        help=(
            "cover center-crops to fill the circle; contain pads the full image "
            "inside a transparent square. Default: cover."
        ),
    )
    parser.add_argument(
        "--size",
        type=int,
        help="Optional output diameter in pixels. Must be a positive integer.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the output file if it already exists.",
    )
    return parser.parse_args()


def make_square(image: Image.Image, fit: str) -> Image.Image:
    width, height = image.size

    if fit == "cover":
        side = min(width, height)
        left = (width - side) // 2
        top = (height - side) // 2
        return image.crop((left, top, left + side, top + side))

    side = max(width, height)
    square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    left = (side - width) // 2
    top = (side - height) // 2
    square.alpha_composite(image, (left, top))
    return square


def apply_circle_mask(image: Image.Image) -> Image.Image:
    side = image.size[0]
    mask = Image.new("L", (side, side), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, side - 1, side - 1), fill=255)

    result = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    result.alpha_composite(image)
    original_alpha = result.getchannel("A")
    result.putalpha(ImageChops.multiply(original_alpha, mask))
    return result


def convert_to_circle(input_path: Path, output_path: Path, fit: str, size: int | None) -> None:
    if size is not None and size <= 0:
        raise ValueError("--size must be a positive integer.")

    with Image.open(input_path) as source:
        image = source.convert("RGBA")

    square = make_square(image, fit)
    if size is not None and square.size != (size, size):
        square = square.resize((size, size), Image.Resampling.LANCZOS)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    apply_circle_mask(square).save(output_path, format="PNG")


def main() -> int:
    args = parse_args()

    if not args.input.exists():
        print(f"Input file does not exist: {args.input}", file=sys.stderr)
        return 2

    if args.input.suffix.lower() != ".png":
        print(f"Input must be a PNG file: {args.input}", file=sys.stderr)
        return 2

    if args.output.exists() and not args.force:
        print(
            f"Output file already exists: {args.output}. Use --force to overwrite.",
            file=sys.stderr,
        )
        return 2

    try:
        convert_to_circle(args.input, args.output, args.fit, args.size)
    except Exception as exc:  # noqa: BLE001 - CLI should report concise failures.
        print(f"Failed to create circular PNG: {exc}", file=sys.stderr)
        return 1

    print(f"Created circular PNG: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
