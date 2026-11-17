#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pillow"]
# ///
"""Calibrated CIELAB measurement for Monthong spine-tip / shell photos.

Implements the conversion chain confirmed in TSAEJ 2018 (Monthong spine-tip
colour study):
8-bit sRGB -> linear RGB -> XYZ (D65, 2 deg, Xn=95.047 Yn=100 Zn=108.883)
-> CIELAB -> hue angle, with optional von Kries white-balance correction
from a same-light white/gray reference crop.

Band thresholds mirror `fruit-picker/references/fruits/durian-monthong.md`
section 1.1 (spine, M1) and 1.2 (shell, M2). The tool reports stage bands and
guard flags; it never overrides the G light-source gate — callers must only
invoke it after G has been asked and is > 0.

Core math is stdlib-only so tests run without third-party packages; Pillow is
imported lazily inside the CLI image-loading path only. Run real photos with:

    uv run <skill>/scripts/color_lab.py --surface spine --g 1.0 \
        --target spine1.png --target spine2.png [--ref white-card.png]

(or `pip3 install pillow` once and use plain python3).
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from dataclasses import dataclass


D65_XN = 95.047
D65_YN = 100.0
D65_ZN = 108.883

SPECULAR_MAX_CHANNEL = 250
SHADOW_MIN_LIGHTNESS = 2.0
DROPPED_FRACTION_WARN = 0.30

SPINE_STAGES = (
    {
        "stage": "明显偏早",
        "m1_range": (15, 35),
        "L": lambda v: v >= 35,
        "b": lambda v: v <= 19,
        "hue": lambda v: v <= 67,
    },
    {
        "stage": "过渡",
        "m1_range": (45, 65),
        "L": lambda v: 32.5 < v < 35,
        "b": lambda v: 19 < v < 21.5,
        "hue": lambda v: 67 < v < 72,
    },
    {
        "stage": "成熟倾向",
        "m1_range": (75, 95),
        "L": lambda v: 29 <= v <= 32.5,
        "b": lambda v: 21.5 <= v <= 23,
        "hue": lambda v: 72 <= v <= 79,
    },
)


def _srgb_channel_to_linear(v8: float) -> float:
    c = v8 / 255.0
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def linear_rgb_to_xyz(r: float, g: float, b: float) -> tuple[float, float, float]:
    x = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) * 100.0
    y = (0.2126729 * r + 0.7151522 * g + 0.0721750 * b) * 100.0
    z = (0.0193339 * r + 0.1191920 * g + 0.9503041 * b) * 100.0
    return x, y, z


def _lab_f(t: float) -> float:
    if t > (6 / 29) ** 3:
        return t ** (1 / 3)
    return t / (3 * (6 / 29) ** 2) + 4 / 29


def xyz_to_lab(x: float, y: float, z: float) -> tuple[float, float, float]:
    fx = _lab_f(x / D65_XN)
    fy = _lab_f(y / D65_YN)
    fz = _lab_f(z / D65_ZN)
    lightness = 116 * fy - 16
    a_star = 500 * (fx - fy)
    b_star = 200 * (fy - fz)
    return lightness, a_star, b_star


def hue_angle(a_star: float, b_star: float) -> float:
    hue = math.degrees(math.atan2(b_star, a_star))
    return hue + 360 if hue < 0 else hue


def srgb8_to_lab(
    r8: float, g8: float, b8: float, gains: tuple[float, float, float] | None = None
) -> tuple[float, float, float, float]:
    r = _srgb_channel_to_linear(r8)
    g = _srgb_channel_to_linear(g8)
    b = _srgb_channel_to_linear(b8)
    if gains is not None:
        r = min(r * gains[0], 1.0)
        g = min(g * gains[1], 1.0)
        b = min(b * gains[2], 1.0)
    lightness, a_star, b_star = xyz_to_lab(*linear_rgb_to_xyz(r, g, b))
    return lightness, a_star, b_star, hue_angle(a_star, b_star)


def white_balance_gains(ref_pixels: list[tuple[int, int, int]]) -> tuple[float, float, float]:
    """Von Kries channel gains from a neutral (white/gray) reference crop."""
    if not ref_pixels:
        raise ValueError("reference crop has no pixels")
    means = [0.0, 0.0, 0.0]
    for r8, g8, b8 in ref_pixels:
        means[0] += _srgb_channel_to_linear(r8)
        means[1] += _srgb_channel_to_linear(g8)
        means[2] += _srgb_channel_to_linear(b8)
    means = [m / len(ref_pixels) for m in means]
    if min(means) <= 0.0:
        raise ValueError("reference crop too dark to derive gains")
    target = sum(means) / 3
    return (target / means[0], target / means[1], target / means[2])


@dataclass(frozen=True)
class CropSummary:
    n_used: int
    dropped_fraction: float
    lightness: float
    a_star: float
    b_star: float
    hue: float
    spread_l: float
    spread_b: float


def summarize_pixels(
    pixels: list[tuple[int, int, int]], gains: tuple[float, float, float] | None = None
) -> CropSummary:
    """Median Lab summary of one crop, dropping specular/deep-shadow pixels."""
    ls: list[float] = []
    as_: list[float] = []
    bs: list[float] = []
    hues: list[float] = []
    dropped = 0
    for r8, g8, b8 in pixels:
        if max(r8, g8, b8) >= SPECULAR_MAX_CHANNEL:
            dropped += 1
            continue
        lightness, a_star, b_star, hue = srgb8_to_lab(r8, g8, b8, gains)
        if lightness < SHADOW_MIN_LIGHTNESS:
            dropped += 1
            continue
        ls.append(lightness)
        as_.append(a_star)
        bs.append(b_star)
        hues.append(hue)
    if not ls:
        raise ValueError("no usable pixels after dropping specular/shadow areas")

    def _iqr(values: list[float]) -> float:
        ordered = sorted(values)
        n = len(ordered)
        return ordered[(3 * n) // 4] - ordered[n // 4]

    return CropSummary(
        n_used=len(ls),
        dropped_fraction=dropped / len(pixels),
        lightness=statistics.median(ls),
        a_star=statistics.median(as_),
        b_star=statistics.median(bs),
        hue=statistics.median(hues),
        spread_l=_iqr(ls),
        spread_b=_iqr(bs),
    )


def classify_spine(lightness: float, b_star: float, hue: float) -> dict:
    """Band one spine-tip measurement per durian-monthong.md section 1.1.

    All three axes must land in the same stage; otherwise M1 is not filled.
    Guard flags mirror the doc's dark-light/stain and yellow-light checks.
    """
    flags: list[str] = []
    if lightness <= 32.5 and b_star < 21:
        flags.append("先排查暗光或污渍：L* 偏低但 b* 未达成熟区")
    if b_star >= 21 and hue < 72:
        flags.append("b* 与 Hue 方向冲突：不填 M1")
        return {"stage": None, "m1_range": None, "flags": flags}
    if lightness >= 35 and b_star >= 21:
        flags.append("先排查黄光：L* 偏早区但 b* 偏成熟区")
        return {"stage": None, "m1_range": None, "flags": flags}
    for stage in SPINE_STAGES:
        if stage["L"](lightness) and stage["b"](b_star) and stage["hue"](hue):
            return {"stage": stage["stage"], "m1_range": stage["m1_range"], "flags": flags}
    flags.append("三轴未同时落入同一阶段：不填 M1")
    return {"stage": None, "m1_range": None, "flags": flags}


def classify_shell(lightness: float, b_star: float) -> dict:
    """Band one shell measurement per durian-monthong.md section 1.2 (M2)."""
    if 16 <= lightness <= 20 and 9 <= b_star <= 13:
        return {"stage": "偏早/偏硬", "m2_range": (25, 45), "flags": []}
    if 14 <= lightness < 16 and 15 <= b_star <= 19:
        return {"stage": "成熟强信号", "m2_range": (70, 90), "flags": []}
    return {
        "stage": None,
        "m2_range": None,
        "flags": ["不在 M2 已定义区间：查光源或风险，不填"],
    }


def combine_crops(surface: str, summaries: list[CropSummary]) -> dict:
    """Cross-crop verdict: every crop must land in the same stage to fill."""
    per_crop = []
    stages = set()
    flags: list[str] = []
    for summary in summaries:
        if surface == "spine":
            band = classify_spine(summary.lightness, summary.b_star, summary.hue)
        else:
            band = classify_shell(summary.lightness, summary.b_star)
        per_crop.append({"summary": summary, "band": band})
        stages.add(band["stage"])
        flags.extend(band["flags"])
        if summary.dropped_fraction > DROPPED_FRACTION_WARN:
            flags.append(
                f"超过 {DROPPED_FRACTION_WARN:.0%} 像素因反光/阴影被剔除，建议重拍"
            )
    if len(stages) == 1 and None not in stages:
        stage = next(iter(stages))
        value_key = "m1_range" if surface == "spine" else "m2_range"
        value_range = per_crop[0]["band"][value_key]
        return {"stage": stage, "range": value_range, "flags": flags, "per_crop": per_crop}
    if len(stages) > 1:
        flags.append("多张裁剪落入不同阶段：不填，补拍同部位")
    return {"stage": None, "range": None, "flags": flags, "per_crop": per_crop}


def _load_pixels(path: str, max_pixels: int = 40_000) -> list[tuple[int, int, int]]:
    from PIL import Image

    with Image.open(path) as img:
        rgb = img.convert("RGB")
        stride = max(1, int(math.sqrt(rgb.width * rgb.height / max_pixels)))
        if stride > 1:
            rgb = rgb.resize((max(1, rgb.width // stride), max(1, rgb.height // stride)))
        read = getattr(rgb, "get_flattened_data", rgb.getdata)
        return list(read())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--target", action="append", required=True, help="spine/shell crop image; repeatable")
    parser.add_argument("--ref", help="same-light white/gray reference crop image")
    parser.add_argument("--surface", choices=("spine", "shell"), default="spine")
    parser.add_argument("--g", type=float, required=True, choices=(1.0, 0.5), help="light-source reliability already asked from the user; G=0 must not reach this tool")
    args = parser.parse_args(argv)

    gains = None
    if args.ref:
        gains = white_balance_gains(_load_pixels(args.ref))
    elif args.g < 1.0:
        print(json.dumps({"error": "G=0.5 需要同光源白/灰参照裁剪图（--ref）"}, ensure_ascii=False))
        return 1

    summaries = [summarize_pixels(_load_pixels(p), gains) for p in args.target]
    verdict = combine_crops(args.surface, summaries)
    out = {
        "surface": args.surface,
        "g": args.g,
        "white_balance_gains": gains,
        "stage": verdict["stage"],
        "range": verdict["range"],
        "flags": sorted(set(verdict["flags"])),
        "crops": [
            {
                "target": path,
                "L": round(item["summary"].lightness, 2),
                "a": round(item["summary"].a_star, 2),
                "b": round(item["summary"].b_star, 2),
                "hue": round(item["summary"].hue, 2),
                "iqr_L": round(item["summary"].spread_l, 2),
                "iqr_b": round(item["summary"].spread_b, 2),
                "dropped_fraction": round(item["summary"].dropped_fraction, 3),
                "stage": item["band"]["stage"],
            }
            for path, item in zip(args.target, verdict["per_crop"])
        ],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
