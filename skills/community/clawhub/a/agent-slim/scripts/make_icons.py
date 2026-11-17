#!/usr/bin/env python3
"""Generate Agent Slim icons (blueprint series) using only the Python standard library.

风格与 skill 系列蓝图蓝标一致：深蓝底 #0A1F3C、青蓝线 #4AD3FF、浅蓝 #BEEEFF、
圆角描边 + 网格底纹。几何按 256 单位设计，按目标尺寸等比缩放；
每个图元用有符号距离做 1px 抗锯齿，不依赖 PIL。
"""

from __future__ import annotations

import argparse
import math
import struct
import zlib
from pathlib import Path

BG = (10, 31, 60)
FG = (74, 211, 255)
FG2 = (190, 238, 255)
GRID = (26, 60, 100)
GRID_ALPHA = 0.47


def _clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return lo if v < lo else hi if v > hi else v


def _sd_round_rect(x: float, y: float, x0: float, y0: float, x1: float, y1: float, r: float) -> float:
    cx = (x0 + x1) / 2.0
    cy = (y0 + y1) / 2.0
    hx = (x1 - x0) / 2.0 - r
    hy = (y1 - y0) / 2.0 - r
    qx = abs(x - cx) - hx
    qy = abs(y - cy) - hy
    ax = max(qx, 0.0)
    ay = max(qy, 0.0)
    return math.hypot(ax, ay) + min(max(qx, qy), 0.0) - r


def _sd_segment(x: float, y: float, x0: float, y0: float, x1: float, y1: float) -> float:
    dx, dy = x1 - x0, y1 - y0
    length2 = dx * dx + dy * dy
    t = 0.0 if length2 == 0 else _clamp(((x - x0) * dx + (y - y0) * dy) / length2)
    return math.hypot(x - (x0 + t * dx), y - (y0 + t * dy))


def _in_triangle(x: float, y: float, a, b, c) -> bool:
    def cross(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

    d1 = cross(a, b, (x, y))
    d2 = cross(b, c, (x, y))
    d3 = cross(c, a, (x, y))
    has_neg = d1 < 0 or d2 < 0 or d3 < 0
    has_pos = d1 > 0 or d2 > 0 or d3 > 0
    return not (has_neg and has_pos)


class Canvas:
    """RGBA float canvas; all drawing is anti-aliased via signed distance."""

    def __init__(self, size: int, unit: float = 256.0) -> None:
        self.size = size
        self.k = size / unit
        self.px = [[0.0, 0.0, 0.0, 0.0] for _ in range(size * size)]

    def _blend(self, i: int, color, alpha: float) -> None:
        if alpha <= 0.0:
            return
        r, g, b = color
        dst = self.px[i]
        sa = alpha
        da = dst[3]
        oa = sa + da * (1 - sa)
        if oa <= 0.0:
            return
        for c, v in enumerate((r, g, b)):
            dst[c] = (v * sa + dst[c] * da * (1 - sa)) / oa
        dst[3] = oa

    def _bbox(self, x0, y0, x1, y1, pad: float):
        s = self.size
        ix0 = max(0, int(math.floor(x0)) - 2)
        iy0 = max(0, int(math.floor(y0)) - 2)
        ix1 = min(s - 1, int(math.ceil(x1)) + 2)
        iy1 = min(s - 1, int(math.ceil(y1)) + 2)
        return ix0, iy0, ix1, iy1

    def round_rect(self, x0, y0, x1, y1, r, *, stroke=None, width=0.0, fill=None,
                   fill_alpha=1.0, stroke_alpha=1.0) -> None:
        k = self.k
        X0, Y0, X1, Y1, R = x0 * k, y0 * k, x1 * k, y1 * k, r * k
        half = width * k / 2.0
        ix0, iy0, ix1, iy1 = self._bbox(X0 - half, Y0 - half, X1 + half, Y1 + half, 0)
        for iy in range(iy0, iy1 + 1):
            fy = iy + 0.5
            row = iy * self.size
            for ix in range(ix0, ix1 + 1):
                d = _sd_round_rect(ix + 0.5, fy, X0, Y0, X1, Y1, R)
                if fill is not None:
                    a = _clamp(0.5 - d) * fill_alpha
                    if a > 0:
                        self._blend(row + ix, fill, a)
                if stroke is not None:
                    a = _clamp(0.5 - (abs(d) - half)) * stroke_alpha
                    if a > 0:
                        self._blend(row + ix, stroke, a)

    def line(self, x0, y0, x1, y1, color, width, *, alpha=1.0) -> None:
        k = self.k
        X0, Y0, X1, Y1 = x0 * k, y0 * k, x1 * k, y1 * k
        half = width * k / 2.0
        ix0, iy0, ix1, iy1 = self._bbox(min(X0, X1) - half, min(Y0, Y1) - half,
                                       max(X0, X1) + half, max(Y0, Y1) + half, 0)
        for iy in range(iy0, iy1 + 1):
            fy = iy + 0.5
            row = iy * self.size
            for ix in range(ix0, ix1 + 1):
                a = _clamp(0.5 - (_sd_segment(ix + 0.5, fy, X0, Y0, X1, Y1) - half)) * alpha
                if a > 0:
                    self._blend(row + ix, color, a)

    def triangle(self, a, b, c, color, *, alpha=1.0) -> None:
        k = self.k
        pts = [(p[0] * k, p[1] * k) for p in (a, b, c)]
        ix0, iy0, ix1, iy1 = self._bbox(min(p[0] for p in pts), min(p[1] for p in pts),
                                       max(p[0] for p in pts), max(p[1] for p in pts), 0)
        for iy in range(iy0, iy1 + 1):
            fy = iy + 0.5
            row = iy * self.size
            for ix in range(ix0, ix1 + 1):
                if _in_triangle(ix + 0.5, fy, *pts):
                    self._blend(row + ix, color, alpha)

    def to_png(self, path: Path) -> None:
        raw = bytearray()
        for iy in range(self.size):
            raw.append(0)
            row = iy * self.size
            for ix in range(self.size):
                p = self.px[row + ix]
                raw.extend((
                    int(_clamp(p[0] / 255.0) * 255 + 0.5),
                    int(_clamp(p[1] / 255.0) * 255 + 0.5),
                    int(_clamp(p[2] / 255.0) * 255 + 0.5),
                    int(_clamp(p[3]) * 255 + 0.5),
                ))
        header = struct.pack(">IIBBBBB", self.size, self.size, 8, 6, 0, 0, 0)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(
            b"\x89PNG\r\n\x1a\n"
            + _chunk(b"IHDR", header)
            + _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + _chunk(b"IEND", b"")
        )


def _chunk(kind: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def draw(size: int) -> Canvas:
    c = Canvas(size)
    c.round_rect(4, 4, 251, 251, 40, fill=BG, stroke=FG, width=4)
    for g in range(32, 256, 32):
        c.line(g, 14, g, 242, GRID, 1, alpha=GRID_ALPHA)
        c.line(14, g, 242, g, GRID, 1, alpha=GRID_ALPHA)
    for x0, y0, x1, y1 in ((56, 84, 200, 118), (56, 130, 164, 164), (56, 176, 128, 210)):
        c.round_rect(x0, y0, x1, y1, 9, fill=BG, stroke=FG, width=5)
        for k in range(2):
            yy = y0 + 12 + k * 11
            c.line(x0 + 12, yy, x1 - 12, yy, FG2, 2)
    c.line(40, 78, 40, 216, FG2, 3)
    for yy in (84, 130, 176, 210):
        c.line(34, yy, 48, yy, FG2, 3)
    c.line(226, 84, 226, 200, FG, 4)
    c.triangle((218, 200), (226, 214), (234, 200), FG)
    return c


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Agent Slim icons.")
    parser.add_argument("--out-dir", default=str(Path(__file__).resolve().parents[1] / "icons"))
    args = parser.parse_args()
    out = Path(args.out_dir)
    draw(128).to_png(out / "icon_small.png")
    draw(512).to_png(out / "icon_large.png")
    print("icons=2 dir={}".format(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
