#!/usr/bin/env python3
"""Generate a collage-style cover module image from an existing cover asset."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a collage cover module image.")
    parser.add_argument("input", help="Path to the source cover image.")
    parser.add_argument("output", help="Path to the generated collage PNG.")
    parser.add_argument(
        "--style",
        default="collage-editorial",
        choices=["collage-editorial", "poster-quiet"],
        help="Cover module style.",
    )
    parser.add_argument("--width", type=int, default=900, help="Canvas width.")
    parser.add_argument("--height", type=int, default=1120, help="Canvas height.")
    return parser.parse_args()


def framed_image(source: Image.Image, size: tuple[int, int], *, border: int = 18) -> Image.Image:
    fitted = ImageOps.fit(source, size, method=Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (size[0] + border * 2, size[1] + border * 2), (255, 251, 246, 255))
    canvas.paste(fitted, (border, border))
    return canvas


def drop_shadow(size: tuple[int, int], *, radius: int = 18, opacity: int = 55) -> Image.Image:
    shadow = Image.new("RGBA", size, (0, 0, 0, 0))
    block = Image.new("RGBA", (size[0] - radius * 2, size[1] - radius * 2), (0, 0, 0, opacity))
    shadow.paste(block, (radius, radius))
    return shadow.filter(ImageFilter.GaussianBlur(radius=radius / 1.5))


def main() -> int:
    args = parse_args()
    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    base = Image.open(input_path).convert("RGBA")
    canvas = Image.new("RGBA", (args.width, args.height), "#f6ede3")

    if args.style == "poster-quiet":
        top_strip = Image.new("RGBA", (args.width - 100, 2), "#d8ccb7")
        canvas.paste(top_strip, (50, 58))
        poster = framed_image(base, (690, 760), border=22)
        poster_shadow = drop_shadow((poster.width + 14, poster.height + 14), radius=18, opacity=28)
        canvas.alpha_composite(poster_shadow, (94, 168))
        canvas.alpha_composite(poster, (104, 154))
        rule = Image.new("RGBA", (3, 770), "#3a3027")
        canvas.paste(rule, (96, 186))
    else:
        strip = Image.new("RGBA", (args.width - 84, 3), "#cbb79f")
        canvas.paste(strip, (42, 44))

        main_size = (680, 700)
        main_card = framed_image(base, main_size, border=16)
        main_shadow = drop_shadow((main_card.width + 10, main_card.height + 10), radius=18, opacity=34)
        canvas.alpha_composite(main_shadow, (168, 124))
        canvas.alpha_composite(main_card, (176, 116))

        inset_size = (255, 360)
        inset_card = framed_image(base, inset_size, border=18)
        inset_shadow = drop_shadow((inset_card.width + 10, inset_card.height + 10), radius=16, opacity=46)
        canvas.alpha_composite(inset_shadow, (54, 448))
        canvas.alpha_composite(inset_card, (62, 440))

        rule = Image.new("RGBA", (4, 810), "#2f2620")
        canvas.paste(rule, (78, 162))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output_path, format="PNG", optimize=True)
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
