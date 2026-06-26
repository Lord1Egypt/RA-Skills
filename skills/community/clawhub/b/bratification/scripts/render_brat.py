from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFilter, ImageFont

DEFAULT_FONT = Path(r"C:\Windows\Fonts\ARIALNB.TTF")
FALLBACK_FONTS = [
    DEFAULT_FONT,
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    Path("/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"),
    Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render brat-style cover text to PNG/WEBP.")
    parser.add_argument("text", help="Text to render")
    parser.add_argument("--png", help="Output PNG path")
    parser.add_argument("--webp", help="Output WEBP path")
    parser.add_argument("--size", type=int, default=1024, help="Canvas size (default: 1024)")
    parser.add_argument("--font-size", type=int, default=120, help="Preferred starting font size")
    parser.add_argument("--blur", type=float, default=2.8, help="Blur radius")
    parser.add_argument("--padding-x", type=int, default=120, help="Horizontal padding")
    parser.add_argument("--shift-y", type=int, default=0, help="Vertical shift from center")
    parser.add_argument("--background", default="#FFFFFF", help="Background color")
    parser.add_argument("--color", default="#111111", help="Text color")
    parser.add_argument("--min-font-size", type=int, default=16, help="Minimum fallback font size")
    parser.add_argument("--font", default=str(DEFAULT_FONT), help="Path to TTF font")
    return parser.parse_args()


def resolve_font_path(font_path: str | None = None) -> Path:
    candidates = []
    if font_path:
        candidates.append(Path(font_path))
    candidates.extend(FALLBACK_FONTS)

    for candidate in candidates:
        if candidate and candidate.exists() and candidate.is_file():
            return candidate

    raise FileNotFoundError(
        "No usable TTF font found. Supply --font with a valid font path on this host."
    )


def load_font(font_path: str, size: int) -> ImageFont.FreeTypeFont:
    resolved = resolve_font_path(font_path)
    return ImageFont.truetype(str(resolved), size=size)


def measure_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> Tuple[int, int]:
    if not text:
        return 0, 0
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def wrap_words(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> List[str]:
    words = [w for w in text.split() if w]
    if not words:
        return ["brat"]

    lines: List[str] = []
    current = words[0]

    for word in words[1:]:
        test = f"{current} {word}"
        width, _ = measure_text(draw, test, font)
        if width <= max_width:
            current = test
        else:
            lines.append(current)
            current = word

    lines.append(current)
    return lines


def fit_layout(
    text: str,
    size: int,
    padding_x: int,
    preferred_font_size: int,
    min_font_size: int,
    font_path: str,
) -> dict:
    probe = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(probe)

    max_width = max(120, size - (padding_x * 2))
    max_height = max(120, size - 80)
    safe_text = text.strip().lower() or "brat"

    best = None
    for current_size in range(preferred_font_size, min_font_size - 1, -2):
        font = load_font(font_path, current_size)
        lines = wrap_words(draw, safe_text, font, max_width)
        line_height = current_size * 0.84
        total_height = len(lines) * line_height
        widest = max((measure_text(draw, line, font)[0] for line in lines), default=0)
        if widest <= max_width and total_height <= max_height:
            best = {
                "font": font,
                "font_size": current_size,
                "lines": lines,
                "line_height": line_height,
                "widest": widest,
                "total_height": total_height,
                "box_width": min(max_width, max(widest + current_size * 0.08, size * 0.34)),
            }
            break

    if best is None:
        current_size = min(max(preferred_font_size, min_font_size), 34)
        font = load_font(font_path, current_size)
        lines = wrap_words(draw, safe_text, font, max_width)
        line_height = current_size * 0.84
        widest = max((measure_text(draw, line, font)[0] for line in lines), default=0)
        best = {
            "font": font,
            "font_size": current_size,
            "lines": lines,
            "line_height": line_height,
            "widest": widest,
            "total_height": len(lines) * line_height,
            "box_width": min(max_width, max(widest + current_size * 0.08, size * 0.34)),
        }

    return best


def should_justify(line: str, index: int, lines: List[str]) -> bool:
    return len(line.split()) > 1 and index < len(lines) - 1


def render_image(
    text: str,
    size: int,
    font_size: int,
    blur: float,
    padding_x: int,
    shift_y: int,
    background: str,
    color: str,
    min_font_size: int,
    font_path: str,
) -> Image.Image:
    layout = fit_layout(text, size, padding_x, font_size, min_font_size, font_path)
    image = Image.new("RGBA", (size, size), background)
    text_layer = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_layer)

    left = (size - layout["box_width"]) / 2
    top = ((size - layout["total_height"]) / 2) + shift_y

    for index, line in enumerate(layout["lines"]):
        y = top + (index * layout["line_height"])
        words = line.split()
        if should_justify(line, index, layout["lines"]):
            word_widths = [measure_text(draw, word, layout["font"])[0] for word in words]
            total_words_width = sum(word_widths)
            gap = max(0, (layout["box_width"] - total_words_width) / max(1, len(words) - 1))
            cursor = left
            for word, width in zip(words, word_widths):
                draw.text((cursor, y), word, font=layout["font"], fill=color)
                cursor += width + gap
        else:
            line_width, _ = measure_text(draw, line, layout["font"])
            x = left + ((layout["box_width"] - line_width) / 2)
            draw.text((x, y), line, font=layout["font"], fill=color)

    if blur > 0:
        text_layer = text_layer.filter(ImageFilter.GaussianBlur(radius=blur))

    return Image.alpha_composite(image, text_layer).convert("RGB")


def ensure_parent(path_str: str | None) -> Path | None:
    if not path_str:
        return None
    path = Path(path_str)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def main() -> int:
    args = parse_args()
    image = render_image(
        text=args.text,
        size=args.size,
        font_size=args.font_size,
        blur=args.blur,
        padding_x=args.padding_x,
        shift_y=args.shift_y,
        background=args.background,
        color=args.color,
        min_font_size=args.min_font_size,
        font_path=args.font,
    )

    png_path = ensure_parent(args.png)
    webp_path = ensure_parent(args.webp)

    if png_path:
        image.save(png_path, format="PNG")
        print(f"PNG:{png_path}")

    if webp_path:
        image.save(webp_path, format="WEBP", lossless=True, quality=95, method=6)
        print(f"WEBP:{webp_path}")

    if not png_path and not webp_path:
        raise SystemExit("Provide at least --png or --webp")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
