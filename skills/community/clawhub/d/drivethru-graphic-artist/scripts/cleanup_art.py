#!/usr/bin/env python3
"""Clean up degraded / AI-generated *flat* artwork for production — deterministic.

The problem this solves: "fake vector" art — a logo that was drawn by an image
model (or scaled/JPEG-mangled) and *looks* like clean spot-color vector art in a
thumbnail, but at print size (e.g. 13") reveals the tell-tale AI defects:

  * ghosting / doubled edges (a faint offset copy of the marks)
  * desaturated haze bleeding around the inks
  * outlines that are jagged, broken, or fade out and vary in width
  * soft, blurry edges instead of crisp ones

A human artist wouldn't try to salvage those blurry pixels and wouldn't
re-*generate* the art (a generative model would change the letterforms and text).
They'd treat it as what it's meant to be — a few flat inks on transparency —
**snap it back to those inks, rebuild the broken outlines, and re-render crisp.**
That's exactly this pipeline, and it is 100% deterministic (no model-made pixels):

  1. INK PALETTE   — the true inks. Pass the decoration's declared colors with
                     --inks '#RRGGBB,...' (best: drives classification from ground
                     truth), or let the script auto-detect them by quantization.
  2. CLASSIFY      — assign every opaque-enough pixel to its nearest ink; pixels
                     too far from any ink (the haze / ghost) are dropped. This is
                     the de-ghost / de-haze step.
  3. RESTORE       — per ink mask: despeckle (kills ghost fragments & stray
                     anti-alias specks) + morphological close (rejoins the broken,
                     faded outline into one continuous stroke).
  4. RE-RENDER     — redraw each mask crisp at print resolution:
                     * vector (default): trace the mask to contours and smooth
                       them with a CORNER-PRESERVING filter (pins sharp letter
                       corners, smooths only the straight runs) -> no staircase,
                       no ripple, corners intact. Best for print.
                     * raster (--method raster): high-res gaussian anti-alias.
                       No OpenCV needed; slightly softer curves.
  5. COMPOSITE     — stack inks (lightest first, darkest/outline on top) onto
                     transparency and write a transparency-preserving PNG.

It also writes a *_proof.png (before vs after on neutral + dark, plus an
auto-zoom on the outline detail) so YOU — the agent running this skill — can
`Read` it and judge the result the way the human eye couldn't at thumbnail size.

This does NOT invent art. It only re-expresses the inks already present. If the
source is genuinely missing a mark (not just faded), or is a photograph, or the
user wants a redesign, this is the wrong tool — see references/production_cleanup.md.

Usage:
    python3 scripts/cleanup_art.py --input /tmp/logo.png \
        [--inks '#26296B,#A0283? ,#FFFFFF']   # decoration colors[].rgb_hex (recommended)
        [--colors 3]                          # else auto-detect this many inks
        [--method vector|raster]              # default vector
        [--supersample 4] [--long-edge-px N]  # print resolution
        [--min-speck AUTO] [--close AUTO] [--corner-deg 42] [--smooth-iters 14]
        [--output /tmp/logo_clean.png] [--proof /tmp/logo_clean_proof.png]

Prints a JSON receipt (ink palette, per-ink pixel counts, params, output size,
and a review_checklist). Always `Read` the proof before trusting the result.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _bootstrap  # noqa: E402


def _hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))


def _parse_inks(s):
    out = []
    for tok in s.split(","):
        tok = tok.strip().lstrip("#")
        if len(tok) != 6:
            continue
        out.append((int(tok[0:2], 16), int(tok[2:4], 16), int(tok[4:6], 16)))
    return out


def detect_inks(a, np, k, a_min):
    """Auto-detect k DISTINCT ink colors from opaque pixels.

    Median-cut alone fails on spot-color art: it allocates palette slots by
    population, so a large fill (white) grabs several near-identical slots while a
    small but important ink (a red outline) gets merged away. So we over-quantize,
    merge near-duplicates, then farthest-point-select k maximally-distinct inks
    among colors with real coverage. Auto-detect is a fallback — passing the
    decoration's declared colors via --inks is always more reliable."""
    from PIL import Image
    solid = a[..., 3] >= max(a_min, 160)
    px = a[..., :3][solid].astype(np.float32)
    if len(px) == 0:
        return []
    if len(px) > 60000:
        px = px[np.linspace(0, len(px) - 1, 60000).astype(int)]
    strip = Image.new("RGB", (len(px), 1))
    strip.putdata([tuple(int(v) for v in p) for p in px])
    q = strip.quantize(colors=min(32, max(4, k * 6)), method=Image.MEDIANCUT)
    pal = q.getpalette()
    cand = []  # (color, population)
    for count, i in (q.getcolors() or []):
        cand.append((np.array(pal[i * 3:i * 3 + 3], np.float32), count))
    total = sum(c for _, c in cand) or 1
    # merge near-duplicates (AA blends of the same ink) into the higher-pop one
    cand.sort(key=lambda x: -x[1])
    merged = []
    for col, cnt in cand:
        for j, (mc, mp) in enumerate(merged):
            if np.sqrt(((col - mc) ** 2).sum()) < 28:
                merged[j] = (mc, mp + cnt)
                break
        else:
            merged.append((col, cnt))
    # keep colors with >=1.5% coverage as real inks; farthest-point pick k of them
    real = [(c, p) for c, p in merged if p / total >= 0.015] or merged
    chosen = [max(real, key=lambda x: x[1])[0]]
    while len(chosen) < min(k, len(real)):
        nxt = max(real, key=lambda cp: min(np.sqrt(((cp[0] - s) ** 2).sum()) for s in chosen))
        if any(np.array_equal(nxt[0], s) for s in chosen):
            break
        chosen.append(nxt[0])
    return [tuple(int(v) for v in c) for c in chosen]


def classify(a, np, inks, a_min, tol):
    """Assign each present pixel to its nearest ink within `tol`; others dropped."""
    present = a[..., 3] >= a_min
    rgb = a[..., :3].astype(np.float32)
    H, W = present.shape
    best = np.full((H, W), -1, np.int32)
    bestd = np.full((H, W), 1e9, np.float32)
    for i, ink in enumerate(inks):
        d = np.sqrt(((rgb - np.array(ink, np.float32)) ** 2).sum(2))
        take = present & (d < bestd)
        best[take] = i
        bestd[take] = d[take]
    best[bestd > tol] = -1        # too far from every ink -> haze/ghost -> drop
    best[~present] = -1
    masks = [(best == i) for i in range(len(inks))]
    return masks


def clean_mask(mask, ndi, np, min_speck, close_it):
    lbl, n = ndi.label(mask)
    if n:
        sizes = ndi.sum(np.ones_like(lbl), lbl, index=np.arange(1, n + 1))
        keep = np.where(sizes >= min_speck)[0] + 1
        mask = np.isin(lbl, keep)
    if close_it:
        mask = ndi.binary_closing(mask, iterations=int(close_it))
    return mask


def _smooth_contour(cv2, np, c, iters, corner_deg, win):
    """Corner-preserving smoothing: pin sharp corners (turn angle over a +/-win
    window exceeds corner_deg), smooth only the straight runs via a constrained
    Laplacian. Removes the AI staircase/ripple without rounding letter corners."""
    pts = c.reshape(-1, 2).astype(np.float32)
    n = len(pts)
    if n < 12:
        return pts
    idx = np.arange(n)
    v1 = pts - pts[(idx - win) % n]
    v2 = pts[(idx + win) % n] - pts
    ang = np.abs((np.arctan2(v2[:, 1], v2[:, 0]) - np.arctan2(v1[:, 1], v1[:, 0])
                  + np.pi) % (2 * np.pi) - np.pi)
    w = (ang < np.deg2rad(corner_deg)).astype(np.float32)
    w = np.minimum.reduce([w, np.roll(w, 1), np.roll(w, -1)])  # protect corner neighbours
    p = pts.copy()
    for _ in range(int(iters)):
        mid = 0.5 * (np.roll(p, 1, 0) + np.roll(p, -1, 0))
        p = p + w[:, None] * (mid - p)
    return p


def render_vector(mask, cv2, np, ss, corner_deg, iters, win):
    m = (mask.astype(np.uint8)) * 255
    H, W = m.shape
    canvas = np.zeros((H * ss, W * ss), np.float32)
    cnts, hier = cv2.findContours(m, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    if hier is None:
        return canvas
    hier = hier[0]
    for i, c in enumerate(cnts):
        if len(c) < 3:
            continue
        sp = _smooth_contour(cv2, np, c, iters, corner_deg, win) * ss
        sp = np.round(sp).astype(np.int32).reshape(-1, 1, 2)
        tmp = np.zeros_like(canvas)
        cv2.fillPoly(tmp, [sp], 1.0, lineType=cv2.LINE_AA)
        if hier[i][3] != -1:      # hole (counter of an O/A/B, interior cutout)
            canvas = np.clip(canvas - tmp, 0, 1)
        else:
            canvas = np.clip(canvas + tmp, 0, 1)
    return canvas


def render_raster(mask, ndi, np, ss, smooth=2.2, ramp=0.16):
    up = np.kron(mask.astype(np.float32), np.ones((ss, ss), np.float32))
    if smooth > 0:
        up = ndi.gaussian_filter(up, sigma=smooth)
    return np.clip((up - 0.5) / (2.0 * ramp) + 0.5, 0.0, 1.0).astype(np.float32)


def main() -> None:
    p = argparse.ArgumentParser(description="Deterministically clean up degraded flat art for print")
    p.add_argument("--input", required=True)
    p.add_argument("--inks", default="", help="Comma-separated #RRGGBB true inks (decoration colors[].rgb_hex). Recommended.")
    p.add_argument("--colors", type=int, default=0, help="If --inks omitted, auto-detect this many inks (default: auto by coverage)")
    p.add_argument("--method", choices=["vector", "raster"], default="vector")
    p.add_argument("--supersample", type=int, default=4, help="Upscale factor for the crisp re-render (default 4)")
    p.add_argument("--long-edge-px", type=int, default=0, help="Instead of --supersample, target this long-edge pixel size")
    p.add_argument("--alpha-min", type=int, default=100, help="Pixels below this alpha are background (default 100)")
    p.add_argument("--tolerance", type=float, default=0.0, help="Max RGB distance to snap to an ink (0=auto)")
    p.add_argument("--min-speck", type=int, default=0, help="Drop connected components smaller than this (0=auto by size)")
    p.add_argument("--close", type=int, default=-1, help="Morphological close iterations to rejoin broken outlines (-1=auto)")
    p.add_argument("--corner-deg", type=float, default=42.0, help="Vector: turn angle that counts as a corner to preserve")
    p.add_argument("--smooth-iters", type=int, default=14, help="Vector: Laplacian smoothing iterations on straight runs")
    p.add_argument("--corner-win", type=int, default=6, help="Vector: window (px) for corner detection")
    p.add_argument("--output", default="")
    p.add_argument("--proof", default="")
    p.add_argument("--dpi", type=int, default=300, help="DPI to stamp into the output PNG (default 300)")
    args = p.parse_args()

    need_cv2 = args.method == "vector"
    _bootstrap.ensure(_bootstrap.CLEANUP,
                      _bootstrap.CLEANUP_MODS if need_cv2 else _bootstrap.IMAGING_MODS + ["scipy"])
    import numpy as np
    from PIL import Image
    from scipy import ndimage as ndi
    cv2 = None
    if need_cv2:
        import cv2  # noqa

    inp = Path(args.input)
    if not inp.exists():
        print(f"ERROR: input not found: {inp}", file=sys.stderr)
        sys.exit(1)
    a = np.array(Image.open(inp).convert("RGBA")).astype(np.int32)
    H, W = a.shape[:2]

    # 1) ink palette
    if args.inks:
        inks = _parse_inks(args.inks)
        ink_source = "declared"
    else:
        k = args.colors if args.colors > 0 else 4
        inks = detect_inks(a, np, k, args.alpha_min)
        ink_source = "auto"
    if not inks:
        print("ERROR: no inks (empty or fully transparent image?)", file=sys.stderr)
        sys.exit(2)

    # auto tolerance: a bit under half the closest ink-pair distance, so snapping
    # never overlaps two inks; clamped to a sane band.
    if args.tolerance > 0:
        tol = args.tolerance
    else:
        dmin = 1e9
        for i in range(len(inks)):
            for j in range(i + 1, len(inks)):
                d = sum((inks[i][c] - inks[j][c]) ** 2 for c in range(3)) ** 0.5
                dmin = min(dmin, d)
        tol = float(np.clip(0.45 * dmin if dmin < 1e8 else 90, 55, 120))

    masks = classify(a, np, inks, args.alpha_min, tol)

    # 2) morphology params auto-scaled to resolution
    scale = min(H, W) / 1024.0
    min_speck = args.min_speck if args.min_speck > 0 else max(8, int(round(18 * scale * scale)))
    close_it = args.close if args.close >= 0 else (1 if scale < 1.6 else 2)
    cleaned = [clean_mask(m, ndi, np, min_speck, close_it) for m in masks]

    # supersample factor from long-edge target if given
    ss = args.supersample
    if args.long_edge_px > 0:
        ss = max(1, int(round(args.long_edge_px / max(H, W))))

    # 3) re-render each ink
    if args.method == "vector":
        covs = [render_vector(m, cv2, np, ss, args.corner_deg, args.smooth_iters, args.corner_win)
                for m in cleaned]
    else:
        covs = [render_raster(m, ndi, np, ss) for m in cleaned]

    # 4) composite: lightest ink first, darkest (outline) last -> on top at edges
    order = sorted(range(len(inks)), key=lambda i: -(0.3 * inks[i][0] + 0.59 * inks[i][1] + 0.11 * inks[i][2]))
    out = np.zeros((H * ss, W * ss, 4), np.float32)
    counts = {}
    for i in order:
        col = np.array(inks[i], np.float32) / 255.0
        acov = np.clip(covs[i], 0, 1)[..., None]
        out[..., :3] = col * acov + out[..., :3] * (1 - acov)
        out[..., 3:4] = acov + out[..., 3:4] * (1 - acov)
        counts[_hex(inks[i])] = int(masks[i].sum())
    img = Image.fromarray((out * 255).round().clip(0, 255).astype(np.uint8))
    # trim to content
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)

    out_path = Path(args.output) if args.output else inp.with_name(inp.stem + "_clean.png")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, format="PNG", dpi=(args.dpi, args.dpi))

    # 5) proof sheet for self-review: before/after on neutral+dark + an auto-zoom
    proof_path = Path(args.proof) if args.proof else out_path.with_name(out_path.stem + "_proof.png")
    try:
        _write_proof(proof_path, a, out, inks, np, Image)
    except Exception as exc:  # a proof failure must never lose the real output
        print(f"WARN: proof not written ({exc})", file=sys.stderr)
        proof_path = None

    print(json.dumps({
        "input": str(inp),
        "output": str(out_path),
        "proof": str(proof_path) if proof_path else None,
        "method": args.method,
        "ink_source": ink_source,
        "inks": [_hex(i) for i in inks],
        "ink_pixel_counts": counts,
        "params": {"alpha_min": args.alpha_min, "tolerance": round(tol, 1),
                    "min_speck": min_speck, "close": close_it, "supersample": ss,
                    "corner_deg": args.corner_deg, "smooth_iters": args.smooth_iters},
        "source_px": [W, H],
        "output_px": list(img.size),
        "print_inches_at_dpi": {"dpi": args.dpi,
                                 "width": round(img.size[0] / args.dpi, 2),
                                 "height": round(img.size[1] / args.dpi, 2)},
        "review_checklist": [
            "Read the proof. Zoom row: are outlines crisp, continuous, uniform width?",
            "Corners of letters/marks still sharp (not rounded by smoothing)?",
            "Letterforms/text unchanged; nothing merged, dropped, or invented?",
            "Ghost/haze gone; no stray specks; colors match the true inks?",
            "If a mark is MISSING (not just faded) this tool can't add it — flag it.",
        ],
    }))


def _write_proof(path, a, out_hi, inks, np, Image):
    """before vs after — on neutral gray and on a dark garment — plus an auto-zoom
    on the darkest-ink (outline) detail, where the AI defects hide at thumbnail size."""
    from PIL import ImageDraw
    H, W = a.shape[:2]
    before = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    after = Image.fromarray((out_hi * 255).round().clip(0, 255).astype(np.uint8)).resize((W, H), Image.LANCZOS)

    def flat(im, bg):
        return Image.alpha_composite(Image.new("RGBA", im.size, bg), im).convert("RGB")

    # auto-zoom window: median location of the darkest ink (the outline) in the source
    dark = min(range(len(inks)), key=lambda i: 0.3 * inks[i][0] + 0.59 * inks[i][1] + 0.11 * inks[i][2])
    A = a[..., 3]
    d = np.sqrt(((a[..., :3] - np.array(inks[dark])) ** 2).sum(2))
    ys, xs = np.where((A >= 100) & (d < 70))
    cx, cy = (int(np.median(xs)), int(np.median(ys))) if len(xs) else (W // 2, H // 2)
    zw, zh = W // 3, H // 6
    l = max(0, min(W - zw, cx - zw // 2)); t = max(0, min(H - zh, cy - zh // 2))
    box = (l, t, l + zw, t + zh)

    cell, pad = 300, 10
    zoom_w = 2 * cell + pad                     # zoom spans both columns
    zoom_h = int(zh * (zoom_w / zw))
    Wc = 2 * cell + 3 * pad
    Hc = 18 + cell + 18 + cell + 22 + 2 * zoom_h + pad + 12
    canvas = Image.new("RGB", (Wc, Hc), (244, 244, 246))
    dr = ImageDraw.Draw(canvas)
    GRAY, DARK = (128, 128, 128, 255), (26, 28, 42, 255)
    y = 16
    dr.text((pad, 3), "BEFORE (source)                             AFTER (cleaned)", fill=(20, 20, 20))
    for bg in (GRAY, DARK):
        canvas.paste(flat(before, bg).resize((cell, cell), Image.LANCZOS), (pad, y))
        canvas.paste(flat(after, bg).resize((cell, cell), Image.LANCZOS), (2 * pad + cell, y))
        y += cell + (2 if bg is GRAY else 20)
    dr.text((pad, y - 16), "ZOOM on outline detail — defects hide here:   BEFORE (top) / AFTER (bottom)", fill=(180, 30, 30))
    canvas.paste(flat(before, GRAY).crop(box).resize((zoom_w, zoom_h), Image.NEAREST), (pad, y))
    canvas.paste(flat(after, GRAY).crop(box).resize((zoom_w, zoom_h), Image.NEAREST), (pad, y + zoom_h + pad))
    canvas.save(path, format="PNG")


if __name__ == "__main__":
    main()
