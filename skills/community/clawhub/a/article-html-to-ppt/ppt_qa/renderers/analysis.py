from __future__ import annotations

from pathlib import Path
from typing import Any

from PIL import Image, ImageStat


def blank_score(image_path: Path) -> float:
    with Image.open(image_path) as image:
        rgba = image.convert("RGBA")
        background = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        composited = Image.alpha_composite(background, rgba).convert("RGB")
        sample = composited.copy()
        sample.thumbnail((320, 320))
        pixels = list(sample.getdata())
    if not pixels:
        return 1.0

    quantized = Image.new("RGB", sample.size)
    quantized.putdata(pixels)
    colors = quantized.quantize(colors=16, method=Image.MEDIANCUT).convert("RGB")
    dominant = colors.getcolors(maxcolors=sample.width * sample.height)
    if dominant:
        _, background_color = max(dominant, key=lambda item: item[0])
    else:
        background_color = pixels[0]

    threshold = 8
    near_background = 0
    for pixel in pixels:
        if all(abs(pixel[channel] - background_color[channel]) <= threshold for channel in range(3)):
            near_background += 1
    near_fraction = near_background / len(pixels)

    stat = ImageStat.Stat(sample)
    mean_variance = sum(stat.var) / len(stat.var)
    variance_penalty = min(mean_variance / 8000.0, 1.0)
    return max(0.0, min(1.0, round(near_fraction * (1.0 - 0.15 * variance_penalty), 6)))


def image_metrics(image_path: Path) -> dict[str, Any]:
    with Image.open(image_path) as image:
        width, height = image.size
    return {
        "width_px": width,
        "height_px": height,
        "blank_score": blank_score(image_path),
    }
