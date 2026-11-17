#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pillow"]
# ///
"""Within-group rind texture ranking for same-batch watermelon candidates.

Implements the `X` variable of `fruit-picker/references/fruits/watermelon.md`
section 2.3: equal-size square crops from the mid-body rind opposite the
ground spot -> lacunarity of the dark-stripe mask, dark stripe area ratio,
gray-level contrast -> group-relative direction only. It never produces
cross-batch or absolute sweetness claims, and it refuses to run when the
crops are not directly comparable (different sizes, fewer than two melons).

Core math is stdlib-only so tests run without third-party packages; Pillow is
imported lazily inside the CLI image-loading path only. Run real crops with:

    uv run <skill>/scripts/watermelon_texture.py --g usable \
        --crop melon1.png --crop melon2.png --crop melon3.png

(or `pip3 install pillow` once and use plain python3).
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from dataclasses import dataclass


LACUNARITY_BOX = 16
LACUNARITY_STRIDE = 8
WORKING_SIZE = 192

STATE_VALUES = {"A": 75, "B": 50, "C": 25}


def otsu_threshold(gray: list[list[int]]) -> int:
    """Otsu's threshold over an 8-bit grayscale grid."""
    hist = [0] * 256
    total = 0
    for row in gray:
        for v in row:
            hist[v] += 1
            total += 1
    if total == 0:
        raise ValueError("empty image")
    sum_all = sum(i * hist[i] for i in range(256))
    sum_bg = 0.0
    weight_bg = 0
    best_threshold, best_variance = 0, -1.0
    for t in range(256):
        weight_bg += hist[t]
        if weight_bg == 0:
            continue
        weight_fg = total - weight_bg
        if weight_fg == 0:
            break
        sum_bg += t * hist[t]
        mean_bg = sum_bg / weight_bg
        mean_fg = (sum_all - sum_bg) / weight_fg
        variance = weight_bg * weight_fg * (mean_bg - mean_fg) ** 2
        if variance > best_variance:
            best_variance = variance
            best_threshold = t
    return best_threshold


def dark_mask(gray: list[list[int]], threshold: int | None = None) -> list[list[bool]]:
    t = otsu_threshold(gray) if threshold is None else threshold
    return [[v <= t for v in row] for row in gray]


def lacunarity(mask: list[list[bool]], box: int = LACUNARITY_BOX, stride: int = LACUNARITY_STRIDE) -> float:
    """Gliding-box lacunarity of a binary mask: var/mean^2 + 1 of box mass."""
    h = len(mask)
    w = len(mask[0])
    if h < box or w < box:
        raise ValueError(f"mask smaller than box size {box}")
    masses: list[int] = []
    for top in range(0, h - box + 1, stride):
        for left in range(0, w - box + 1, stride):
            mass = 0
            for row in mask[top : top + box]:
                mass += sum(row[left : left + box])
            masses.append(mass)
    mean = statistics.fmean(masses)
    if mean == 0:
        return float("inf")
    variance = statistics.pvariance(masses)
    return variance / (mean * mean) + 1.0


def largest_bright_gap_share(mask: list[list[bool]]) -> float:
    """Largest connected bright (non-stripe) component as a share of pixels."""
    h = len(mask)
    w = len(mask[0])
    seen = [[False] * w for _ in range(h)]
    best = 0
    for start_y in range(h):
        for start_x in range(w):
            if mask[start_y][start_x] or seen[start_y][start_x]:
                continue
            size = 0
            queue = [(start_y, start_x)]
            seen[start_y][start_x] = True
            while queue:
                y, x = queue.pop()
                size += 1
                for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                    if 0 <= ny < h and 0 <= nx < w and not seen[ny][nx] and not mask[ny][nx]:
                        seen[ny][nx] = True
                        queue.append((ny, nx))
            best = max(best, size)
    return best / (h * w)


@dataclass(frozen=True)
class TextureMetrics:
    lacunarity: float
    bright_gap_share: float
    dark_ratio: float
    gray_std: float


def texture_metrics(gray: list[list[int]]) -> TextureMetrics:
    mask = dark_mask(gray)
    flat = [v for row in gray for v in row]
    dark = sum(sum(row) for row in mask)
    return TextureMetrics(
        lacunarity=lacunarity(mask),
        bright_gap_share=largest_bright_gap_share(mask),
        dark_ratio=dark / len(flat),
        gray_std=statistics.pstdev(flat),
    )


def rank_group(metrics: list[TextureMetrics]) -> list[str]:
    """Assign X=A/B/C per melon from group-relative direction.

    Lower lacunarity and smaller largest bright gap point toward the mature
    direction (doc 2.3). A melon gets A only when both features agree on the
    mature side, C only when both agree on the early side, otherwise B.

    Ties share an average rank, so indistinguishable crops land on B
    together instead of being split into a fake mature/early pair — the
    tool exists to rank genuinely middle-band candidates, and inventing a
    difference between equal melons would mislead the purchase choice.
    """
    if len(metrics) < 2:
        raise ValueError("group ranking needs at least two melons")

    def _ranks(values: list[float]) -> list[float]:
        order = sorted(range(len(values)), key=lambda i: values[i])
        ranks = [0.0] * len(values)
        position = 0
        while position < len(order):
            tie_end = position
            while (
                tie_end + 1 < len(order)
                and values[order[tie_end + 1]] == values[order[position]]
            ):
                tie_end += 1
            average = (position + tie_end) / 2
            for tied in range(position, tie_end + 1):
                ranks[order[tied]] = average
            position = tie_end + 1
        return ranks

    lac_ranks = _ranks([m.lacunarity for m in metrics])
    gap_ranks = _ranks([m.bright_gap_share for m in metrics])
    midpoint = (len(metrics) - 1) / 2
    labels = []
    for lac_rank, gap_rank in zip(lac_ranks, gap_ranks):
        if lac_rank < midpoint and gap_rank < midpoint:
            labels.append("A")
        elif lac_rank > midpoint and gap_rank > midpoint:
            labels.append("C")
        else:
            labels.append("B")
    return labels


def _load_gray(path: str) -> tuple[list[list[int]], dict]:
    from PIL import Image

    with Image.open(path) as img:
        gray = img.convert("L")
        if gray.width != gray.height:
            raise ValueError(f"{path}: crop must be square, got {gray.width}x{gray.height}")
        original_size = gray.width
        if gray.width != WORKING_SIZE:
            gray = gray.resize((WORKING_SIZE, WORKING_SIZE))
        read = getattr(gray, "get_flattened_data", gray.getdata)
        pixels = list(read())
        grid = [pixels[y * WORKING_SIZE : (y + 1) * WORKING_SIZE] for y in range(WORKING_SIZE)]
        grid_meta = {"path": path, "original_size": original_size}
        return grid, grid_meta


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--crop", action="append", required=True, help="equal-size square rind crop, one per melon; repeatable")
    parser.add_argument("--g", choices=("usable", "weak"), required=True, help="light-source state already asked from the user; disabled/unknown must not reach this tool")
    args = parser.parse_args(argv)

    if len(args.crop) < 2:
        print(json.dumps({"error": "X 只做组内排序：至少两颗（单颗填 X=D）"}, ensure_ascii=False))
        return 1

    loaded = [_load_gray(p) for p in args.crop]
    sizes = {meta["original_size"] for _, meta in loaded}
    if len(sizes) > 1:
        print(
            json.dumps(
                {"error": f"裁剪边长不一致 {sorted(sizes)}：不可比，重新按同缩放裁剪（否则 X=D）"},
                ensure_ascii=False,
            )
        )
        return 1

    metrics = [texture_metrics(grid) for grid, _ in loaded]
    labels = rank_group(metrics)
    out = {
        "g": args.g,
        "melons": [
            {
                "crop": meta["path"],
                "x": label,
                "state_value": STATE_VALUES[label],
                "lacunarity": round(m.lacunarity, 4),
                "bright_gap_share": round(m.bright_gap_share, 4),
                "dark_ratio": round(m.dark_ratio, 4),
                "gray_std": round(m.gray_std, 2),
            }
            for (_, meta), m, label in zip(loaded, metrics, labels)
        ],
        "note": "组内相对方向，不是甜度；跨品种/跨批次/拍摄条件不同时不可用",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
