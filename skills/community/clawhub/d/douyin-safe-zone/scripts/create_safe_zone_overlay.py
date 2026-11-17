#!/usr/bin/env python3
"""Create a transparent Douyin layout guide PNG with an outside dim mask."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw


@dataclass(frozen=True)
class Profile:
    width: int
    height: int
    top: int
    right: int
    bottom: int
    left: int


PROFILES = {
    # Reference layout, not a platform guarantee. Adjust from the actual preview.
    "douyin-playback-reference": Profile(1080, 1920, 170, 86, 288, 86),
    "douyin-cover-3x4": Profile(1080, 1440, 115, 86, 216, 86),
}


def dashed_line(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: tuple[int, int, int, int], width: int = 2, dash: int = 14, gap: int = 8) -> None:
    x1, y1 = start
    x2, y2 = end
    horizontal = y1 == y2
    distance = abs((x2 - x1) if horizontal else (y2 - y1))
    position = 0
    while position < distance:
        segment_end = min(position + dash, distance)
        if horizontal:
            draw.line((x1 + position, y1, x1 + segment_end, y2), fill=color, width=width)
        else:
            draw.line((x1, y1 + position, x2, y1 + segment_end), fill=color, width=width)
        position = segment_end + gap


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=sorted(PROFILES), default="douyin-playback-reference")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--top", type=int)
    parser.add_argument("--right", type=int)
    parser.add_argument("--bottom", type=int)
    parser.add_argument("--left", type=int)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    base = PROFILES[args.profile]
    profile = Profile(
        width=base.width,
        height=base.height,
        top=args.top if args.top is not None else base.top,
        right=args.right if args.right is not None else base.right,
        bottom=args.bottom if args.bottom is not None else base.bottom,
        left=args.left if args.left is not None else base.left,
    )
    if min(profile.top, profile.right, profile.bottom, profile.left) < 0:
        raise SystemExit("Margins must be non-negative.")
    if max(profile.top, profile.bottom) >= profile.height or max(profile.left, profile.right) >= profile.width:
        raise SystemExit("Margins must be smaller than the canvas dimensions.")
    x1, y1 = profile.left, profile.top
    x2, y2 = profile.width - profile.right, profile.height - profile.bottom
    if x1 >= x2 or y1 >= y2:
        raise SystemExit("Margins leave no usable safe rectangle.")

    image = Image.new("RGBA", (profile.width, profile.height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, profile.width - 1, profile.height - 1), fill=(0, 0, 0, 64))
    draw.rectangle((x1, y1, x2, y2), fill=(0, 0, 0, 0))
    green = (0, 255, 0, 255)
    dashed_line(draw, (x1, y1), (x2, y1), green)
    dashed_line(draw, (x2, y1), (x2, y2), green)
    dashed_line(draw, (x2, y2), (x1, y2), green)
    dashed_line(draw, (x1, y2), (x1, y1), green)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.output, "PNG")
    print(f"profile={args.profile}")
    print(f"canvas={profile.width}x{profile.height}")
    print(f"safe_rect=x={x1}, y={y1}, width={x2 - x1}, height={y2 - y1}")
    print(f"output={args.output}")


if __name__ == "__main__":
    main()
