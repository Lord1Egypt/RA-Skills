#!/usr/bin/env python3
"""Render a fact-safe mixed card from a generated background and an exact text plan."""

from __future__ import annotations

import argparse
import random
from collections import Counter
from pathlib import Path
from typing import Any

from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont

from handoff_common import load_json, parse_dimensions, save_json, sha256_file, utc_now


FONT_CANDIDATES: dict[tuple[str, bool], tuple[tuple[str, int], ...]] = {
    ("cjk", False): (
        ("/System/Library/Fonts/Hiragino Sans GB.ttc", 0),
        ("/System/Library/Fonts/PingFang.ttc", 0),
        ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 0),
    ),
    ("cjk", True): (
        ("/System/Library/Fonts/Hiragino Sans GB.ttc", 2),
        ("/System/Library/Fonts/PingFang.ttc", 0),
        ("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 0),
    ),
    ("mono", False): (
        ("/System/Library/Fonts/Menlo.ttc", 0),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 0),
    ),
    ("mono", True): (
        ("/System/Library/Fonts/Menlo.ttc", 1),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 0),
    ),
}


def parse_color(value: Any, label: str) -> tuple[int, int, int]:
    try:
        return ImageColor.getrgb(str(value))
    except ValueError as error:
        raise ValueError(f"Invalid color for {label}: {value}") from error


def parse_box(value: Any, width: int, height: int, label: str) -> tuple[int, int, int, int]:
    if not isinstance(value, list) or len(value) != 4:
        raise ValueError(f"{label} must be [x1, y1, x2, y2]")
    try:
        x1, y1, x2, y2 = (int(item) for item in value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{label} must contain integers") from error
    if not (0 <= x1 < x2 <= width and 0 <= y1 < y2 <= height):
        raise ValueError(f"{label} is outside {width}x{height}: {value}")
    return x1, y1, x2, y2


def parse_line(value: Any, width: int, height: int, label: str) -> tuple[int, int, int, int]:
    if not isinstance(value, list) or len(value) != 4:
        raise ValueError(f"{label} must be [x1, y1, x2, y2]")
    try:
        x1, y1, x2, y2 = (int(item) for item in value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{label} must contain integers") from error
    if not (0 <= x1 <= width and 0 <= x2 <= width and 0 <= y1 <= height and 0 <= y2 <= height):
        raise ValueError(f"{label} is outside {width}x{height}: {value}")
    if x1 == x2 and y1 == y2:
        raise ValueError(f"{label} must have non-zero length")
    return x1, y1, x2, y2


def resolve_font(family: str, bold: bool, size: int) -> ImageFont.FreeTypeFont:
    if family not in {"cjk", "mono"}:
        raise ValueError(f"Unsupported font family: {family}")
    for path, index in FONT_CANDIDATES[(family, bold)]:
        if not Path(path).is_file():
            continue
        try:
            return ImageFont.truetype(path, size, index=index)
        except OSError:
            continue
    raise ValueError(f"No usable {family} font found (bold={bold})")


def fit_font(
    draw: ImageDraw.ImageDraw,
    text: str,
    family: str,
    bold: bool,
    start_size: int,
    minimum_size: int,
    box_width: int,
    box_height: int,
) -> tuple[ImageFont.FreeTypeFont, tuple[int, int, int, int]]:
    for size in range(start_size, minimum_size - 1, -1):
        face = resolve_font(family, bold, size)
        bounds = draw.textbbox((0, 0), text, font=face)
        if bounds[2] - bounds[0] <= box_width and bounds[3] - bounds[1] <= box_height:
            return face, bounds
    raise ValueError(f"Text does not fit its box at minimum size {minimum_size}: {text}")


def render_background(source: Image.Image, plan: dict[str, Any]) -> Image.Image:
    background = plan.get("background", {})
    if not isinstance(background, dict):
        raise ValueError("background must be an object")
    blur_radius = float(background.get("blur_radius", 0))
    if not 0 <= blur_radius <= 100:
        raise ValueError("background.blur_radius must be between 0 and 100")
    overlay_opacity = int(background.get("overlay_opacity", 0))
    if not 0 <= overlay_opacity <= 255:
        raise ValueError("background.overlay_opacity must be between 0 and 255")
    overlay_color = parse_color(background.get("overlay_color", "#FFFFFF"), "background.overlay_color")

    rendered = source.convert("RGB")
    if blur_radius:
        rendered = rendered.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    rendered = rendered.convert("RGBA")
    tint = Image.new("RGBA", rendered.size, (*overlay_color, overlay_opacity))
    rendered = Image.alpha_composite(rendered, tint)

    grain = background.get("grain", {})
    if grain:
        if not isinstance(grain, dict):
            raise ValueError("background.grain must be an object")
        count = int(grain.get("count", 0))
        alpha = int(grain.get("alpha", 18))
        radius = int(grain.get("radius", 1))
        if not 0 <= count <= 50000 or not 0 <= alpha <= 255 or not 1 <= radius <= 8:
            raise ValueError("background.grain values are outside supported bounds")
        colors = grain.get("colors", ["#D8C7AC", "#F8EDD9"])
        if not isinstance(colors, list) or not colors:
            raise ValueError("background.grain.colors must be a non-empty array")
        palette = [parse_color(color, "background.grain.colors") for color in colors]
        rng = random.Random(int(grain.get("seed", 0)))
        grain_layer = Image.new("RGBA", rendered.size, (0, 0, 0, 0))
        grain_draw = ImageDraw.Draw(grain_layer)
        for _ in range(count):
            x = rng.randrange(rendered.width)
            y = rng.randrange(rendered.height)
            color = rng.choice(palette)
            grain_draw.ellipse((x, y, x + radius, y + radius), fill=(*color, alpha))
        rendered = Image.alpha_composite(rendered, grain_layer)
    return rendered


def render_element(
    draw: ImageDraw.ImageDraw,
    element: dict[str, Any],
    width: int,
    height: int,
    allowed_text: set[str],
) -> str | None:
    element_type = str(element.get("type", ""))
    if element_type == "line":
        draw.line(
            parse_line(element.get("box"), width, height, "line.box"),
            fill=parse_color(element.get("fill", "#000000"), "line.fill"),
            width=int(element.get("width", 1)),
        )
        return None
    box = parse_box(element.get("box"), width, height, f"{element_type}.box")
    if element_type == "panel":
        fill = (*parse_color(element.get("fill", "#FFFFFF"), "panel.fill"), int(element.get("opacity", 255)))
        outline_value = element.get("outline")
        outline = parse_color(outline_value, "panel.outline") if outline_value else None
        draw.rounded_rectangle(
            box,
            radius=int(element.get("radius", 0)),
            fill=fill,
            outline=outline,
            width=int(element.get("width", 1)),
        )
        return None
    if element_type == "ellipse":
        fill_value = element.get("fill")
        outline_value = element.get("outline")
        draw.ellipse(
            box,
            fill=parse_color(fill_value, "ellipse.fill") if fill_value else None,
            outline=parse_color(outline_value, "ellipse.outline") if outline_value else None,
            width=int(element.get("width", 1)),
        )
        return None
    if element_type != "text":
        raise ValueError(f"Unsupported element type: {element_type}")

    text = str(element.get("text", ""))
    if text not in allowed_text:
        raise ValueError(f"Text is outside allowed_text: {text}")
    x1, y1, x2, y2 = box
    padding = int(element.get("padding", 0))
    inner_width = x2 - x1 - padding * 2
    inner_height = y2 - y1 - padding * 2
    if inner_width <= 0 or inner_height <= 0:
        raise ValueError(f"Text padding consumes the box: {text}")
    face, bounds = fit_font(
        draw,
        text,
        str(element.get("family", "cjk")),
        bool(element.get("bold", False)),
        int(element.get("size", 48)),
        int(element.get("minimum_size", 18)),
        inner_width,
        inner_height,
    )
    text_width = bounds[2] - bounds[0]
    text_height = bounds[3] - bounds[1]
    align = str(element.get("align", "left"))
    valign = str(element.get("valign", "middle"))
    if align == "left":
        text_x = x1 + padding
    elif align == "center":
        text_x = x1 + (x2 - x1 - text_width) / 2
    elif align == "right":
        text_x = x2 - padding - text_width
    else:
        raise ValueError(f"Unsupported text align: {align}")
    if valign == "top":
        text_y = y1 + padding
    elif valign == "middle":
        text_y = y1 + (y2 - y1 - text_height) / 2
    elif valign == "bottom":
        text_y = y2 - padding - text_height
    else:
        raise ValueError(f"Unsupported text valign: {valign}")
    draw.text(
        (round(text_x - bounds[0]), round(text_y - bounds[1])),
        text,
        font=face,
        fill=parse_color(element.get("fill", "#000000"), "text.fill"),
    )
    return text


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    plan_path = args.plan.expanduser().resolve()
    output = args.output.expanduser().resolve()
    if not source.is_file() or not plan_path.is_file():
        raise SystemExit("Source image and overlay plan must exist")
    if source == output:
        raise SystemExit("Output must not overwrite the source image")
    if output.suffix.lower() != ".png":
        raise SystemExit("Mixed overlay output must use a .png filename")

    plan = load_json(plan_path)
    if int(plan.get("schema_version", 0)) != 1:
        raise SystemExit("Unsupported mixed overlay plan schema_version")
    dimensions = parse_dimensions(str(plan.get("dimensions", "")))
    source_checksum = sha256_file(source)
    expected_checksum = str(plan.get("expected_source_sha256", "")).strip()
    if expected_checksum and source_checksum != expected_checksum:
        raise SystemExit("Source checksum does not match the reviewed overlay plan")

    allowed_text_raw = plan.get("allowed_text")
    if not isinstance(allowed_text_raw, list) or not allowed_text_raw:
        raise SystemExit("allowed_text must be a non-empty array")
    allowed_text_list = [str(value) for value in allowed_text_raw]
    if len(set(allowed_text_list)) != len(allowed_text_list):
        raise SystemExit("allowed_text must not contain duplicates")

    source_fit = str(plan.get("source_fit", "exact"))
    if source_fit not in {"exact", "resize_matching_ratio"}:
        raise SystemExit(f"Unsupported source_fit: {source_fit}")
    with Image.open(source) as opened:
        source_dimensions = opened.size
        source_image = opened.convert("RGB")
        if source_dimensions != dimensions:
            if source_fit != "resize_matching_ratio":
                raise SystemExit(
                    f"Source dimensions {opened.width}x{opened.height} do not match "
                    f"plan dimensions {dimensions[0]}x{dimensions[1]}"
                )
            source_ratio = opened.width / opened.height
            target_ratio = dimensions[0] / dimensions[1]
            ratio_difference = abs(source_ratio - target_ratio) / target_ratio
            if ratio_difference > 0.015:
                raise SystemExit("Source ratio does not match the reviewed overlay plan")
            source_image = source_image.resize(dimensions, Image.Resampling.LANCZOS)
        rendered = render_background(source_image, plan)
    draw = ImageDraw.Draw(rendered)
    elements = plan.get("elements")
    if not isinstance(elements, list) or not elements:
        raise SystemExit("elements must be a non-empty array")
    rendered_text: list[str] = []
    try:
        for raw in elements:
            if not isinstance(raw, dict):
                raise ValueError("Every element must be an object")
            value = render_element(draw, raw, dimensions[0], dimensions[1], set(allowed_text_list))
            if value is not None:
                rendered_text.append(value)
    except ValueError as error:
        raise SystemExit(str(error)) from error

    if bool(plan.get("require_all_allowed_text", True)):
        if Counter(rendered_text) != Counter(allowed_text_list):
            raise SystemExit("Rendered text does not exactly match allowed_text")

    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(f".{output.name}.tmp{output.suffix}")
    rendered.convert("RGB").save(temporary, format="PNG", optimize=True)
    temporary.replace(output)

    report_path = args.report.expanduser().resolve() if args.report else None
    if report_path:
        save_json(
            report_path,
            {
                "schema_version": 1,
                "render_strategy": "mixed",
                "source_path": str(source),
                "source_sha256": source_checksum,
                "source_dimensions": f"{source_dimensions[0]}x{source_dimensions[1]}",
                "source_fit": source_fit,
                "plan_path": str(plan_path),
                "plan_sha256": sha256_file(plan_path),
                "output_path": str(output),
                "output_sha256": sha256_file(output),
                "dimensions": f"{dimensions[0]}x{dimensions[1]}",
                "rendered_text": rendered_text,
                "text_policy_check": "passed",
                "rendered_at": utc_now(),
            },
        )
    print(output)
    if report_path:
        print(report_path)


if __name__ == "__main__":
    main()
