#!/usr/bin/env python3
"""Knock a solid background color out of **flat art** (logos, line art, decals).

This is the right tool when the artwork sits on a *solid* color — a white plate,
a colored field — and you want that color to become transparent with clean,
anti-aliased edges. It is **not** segmentation: unlike ``remove_background.py``
(rembg / U²-Net, built for *photographic* subjects), this keys on the actual
pixel color, so it never leaves a soft matte halo and never guesses.

Two modes, pick by intent:

* ``color-to-alpha`` (default) — GIMP-style "color to alpha". Every pixel's
  alpha becomes proportional to its distance from the key color, and the
  foreground color is un-multiplied back out. A mid-gray anti-aliased edge pixel
  (a 50/50 blend of black art and white plate) becomes 50%-opaque *black* — so
  edges stay crisp instead of turning into a muddy gray rim, and there is no
  light halo. Removes the key color **everywhere**, including enclosed regions
  (letter counters, the field inside an outline). Best for single-color line art
  you want printed as ink-on-garment.

* ``flood`` — remove only the background *connected to the border* (a flood fill
  with tolerance), feathered with the same color-to-alpha math at the boundary.
  Enclosed regions of the key color are **kept** (a white field stays white).
  This is the "die-cut sticker" look. Use it when interior key-color areas are
  intentional and must print.

Which mode? The honest answer is "it depends whether the key color is an *ink* on
this decoration." Don't eyeball-guess it and don't blindly trust the color list
either — run ``--analyze`` first. Analyze reports the key color, how much of the
image each mode would remove, and (the number that actually decides it) the
**enclosed fraction**: pixels of the key color that sit *inside* the art rather
than around it. Pass the decoration's declared inks via ``--expect-colors`` and
analyze cross-checks them against the pixels and recommends a mode — while still
handing you the raw evidence to overrule it.

The key color defaults to ``auto`` (median of the four corners) and can be set
explicitly with ``--color '#RRGGBB'``. Pre-existing transparency is preserved
(multiplied in); an input that is *already* cut out is skipped unless ``--force``.

Deterministic image manipulation only — **no model-generated pixels**.

Usage:
    # Look before you leap — what would each mode do, and which fits the inks?
    python3 scripts/knockout_color.py --input thumb.png --analyze \
        --expect-colors '#000000'
    # Then knock it out:
    python3 scripts/knockout_color.py --input thumb.png --output cut.png \
        --mode color-to-alpha
    python3 scripts/knockout_color.py --input in.png --output out.png \
        --mode flood --color '#FFFFFF' --fuzz 0.12 --feather 2

Prints a JSON receipt (analyze diagnostics, or the knockout result).
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _bootstrap  # noqa: E402

_bootstrap.ensure(_bootstrap.IMAGING, _bootstrap.IMAGING_MODS)

import numpy as np  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter  # noqa: E402

# Two colors within this RGB Euclidean distance are treated as "the same ink"
# when cross-checking the detected background against the declared color list.
_INK_MATCH_TOL = 42.0
# Enclosed key-color area at/above this fraction of the image means the
# flood-vs-color-to-alpha choice materially changes the print.
_DECISION_MATTERS = 0.01


def _parse_color(spec: str, rgb: "np.ndarray") -> "np.ndarray":
    """Return the len-3 float key color. ``auto`` = median of the corner patches."""
    spec = spec.strip().lower()
    if spec in ("auto", ""):
        h, w, _ = rgb.shape
        c = min(8, h, w)
        patches = [
            rgb[0:c, 0:c], rgb[0:c, w - c:w],
            rgb[h - c:h, 0:c], rgb[h - c:h, w - c:w],
        ]
        px = np.concatenate([p.reshape(-1, 3) for p in patches], axis=0)
        return np.median(px, axis=0).astype(np.float32)
    return _hex_to_rgb(spec)


def _hex_to_rgb(spec: str) -> "np.ndarray":
    s = spec.strip().lstrip("#")
    if len(s) == 3:
        s = "".join(ch * 2 for ch in s)
    if len(s) != 6:
        raise ValueError(f"bad color '{spec}': use '#RRGGBB'")
    return np.array([int(s[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32)


def _hexstr(c: "np.ndarray") -> str:
    return "#{:02X}{:02X}{:02X}".format(*(int(round(v)) for v in c))


def _color_to_alpha(rgb: "np.ndarray", key: "np.ndarray"):
    """GIMP color-to-alpha. ``rgb`` is HxWx3 float32 (0..255); ``key`` is len-3.

    Returns ``(out_rgb uint8 HxWx3, alpha01 HxW float32 in 0..1)``.
    """
    p = rgb.astype(np.float32)
    k = key.astype(np.float32)

    # Per-channel opacity needed so that (result over key) reproduces the pixel.
    dist_hi = np.where(p > k, (p - k) / np.maximum(255.0 - k, 1e-6), 0.0)
    dist_lo = np.where(p < k, (k - p) / np.maximum(k, 1e-6), 0.0)
    per_ch = np.clip(np.maximum(dist_hi, dist_lo), 0.0, 1.0)  # HxWx3
    alpha = per_ch.max(axis=2)  # HxW in 0..1

    # Un-multiply the key back out to recover the true foreground color.
    safe = np.maximum(alpha[..., None], 1e-6)
    fg = np.clip(k + (p - k) / safe, 0.0, 255.0)
    out_rgb = np.where(alpha[..., None] > 0.0, fg, 0.0).astype(np.uint8)
    return out_rgb, alpha


def _ramp(cta_alpha: "np.ndarray", fuzz: float) -> "np.ndarray":
    """Widen the fully-transparent band near the key color by ``fuzz``."""
    if fuzz > 0:
        return np.clip((cta_alpha - fuzz) / max(1e-6, 1.0 - fuzz), 0.0, 1.0)
    return cta_alpha


def _flood_region(rgb: "np.ndarray", fuzz: float) -> "np.ndarray":
    """Boolean HxW mask of background *connected to the border* within tolerance.

    Uses Pillow's flood fill seeded from every corner (art often touches an
    edge, so a single seed can be blocked). ``thresh`` is scaled from ``fuzz``.
    """
    h, w, _ = rgb.shape
    work = Image.fromarray(rgb.astype(np.uint8))
    sentinel = (1, 254, 1)  # unlikely in real art; we detect fill by this value
    thresh = float(fuzz) * 255.0 * 3.0  # Pillow sums the per-channel abs diff
    seeds = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
    for xy in seeds:
        if tuple(work.getpixel(xy)) == sentinel:
            continue
        ImageDraw.floodfill(work, xy, sentinel, thresh=thresh)
    filled = np.asarray(work)
    return np.all(filled == np.array(sentinel, dtype=np.uint8), axis=2)


def _load(input_path: Path):
    src = Image.open(input_path).convert("RGBA")  # normalizes CMYK/palette/gray
    arr = np.asarray(src)
    rgb = arr[:, :, :3].astype(np.float32)
    orig_alpha = arr[:, :, 3].astype(np.float32) / 255.0
    already_transparent = bool((orig_alpha < 0.98).mean() > 0.005)
    return src, arr, rgb, orig_alpha, already_transparent


def analyze(input_path: Path, color_spec: str, fuzz: float,
            expect_colors: list) -> dict:
    """Report what each mode would do and (if inks given) recommend one.

    The recommendation is *derived from* the declared inks but never asserted
    without the evidence beside it — the caller reconciles the two.
    """
    src, arr, rgb, orig_alpha, already_transparent = _load(input_path)
    key = _parse_color(color_spec, rgb)
    _, cta_alpha = _color_to_alpha(rgb, key)
    ramp = _ramp(cta_alpha, fuzz)

    cta_out = ramp * orig_alpha
    region = _flood_region(rgb, fuzz)
    flood_out = np.where(region, ramp, 1.0) * orig_alpha

    total = cta_out.size
    cta_removed = float((cta_out < 0.02).mean())
    flood_removed = float((flood_out < 0.02).mean())
    enclosed = max(0.0, cta_removed - flood_removed)  # interior key-color area
    edge = float(((cta_out >= 0.02) & (cta_out < 0.98)).mean())
    decision_matters = enclosed >= _DECISION_MATTERS

    # Cross-check the detected background color against the declared inks.
    inks = [(_hexstr(c), float(np.sqrt(((key - c) ** 2).sum()))) for c in expect_colors]
    nearest = min(inks, key=lambda t: t[1]) if inks else None
    key_is_declared_ink = bool(nearest and nearest[1] <= _INK_MATCH_TOL)

    recommended, reason = None, None
    if expect_colors:
        if key_is_declared_ink:
            recommended = "flood"
            reason = (f"background {_hexstr(key)} matches declared ink {nearest[0]} "
                      f"(dist {nearest[1]:.0f}) — it prints, so keep enclosed areas.")
        else:
            recommended = "color-to-alpha"
            reason = (f"background {_hexstr(key)} is not among the declared inks "
                      f"(nearest {nearest[0]} at dist {nearest[1]:.0f}) — knock it out.")
        if not decision_matters:
            reason += (" (Low stakes: almost no enclosed key-color area, so both "
                       "modes look nearly identical here.)")
    else:
        reason = ("No --expect-colors given, so no mode is recommended. Pass the "
                  "decoration's declared inks to get one; otherwise choose by intent.")

    warnings = []
    if already_transparent:
        warnings.append("input already has transparency — it may be cut out "
                        "already; knockout needs --force to run.")
    if cta_removed < 0.01:
        warnings.append(f"barely any of {_hexstr(key)} present ({cta_removed:.1%}) "
                        "— the key color may be wrong, or there is no solid background.")
    if decision_matters and expect_colors is not None:
        warnings.append(f"the mode choice changes {enclosed:.1%} of the image "
                        "(a real interior key-color region) — verify by eye before trusting the recommendation.")

    return {
        "analyze": True,
        "input": str(input_path),
        "size_px": [int(src.width), int(src.height)],
        "key_color": _hexstr(key),
        "key_source": "auto" if color_spec.strip().lower() in ("auto", "") else "explicit",
        "already_transparent": already_transparent,
        "fuzz": fuzz,
        "would_remove": {
            "color_to_alpha_fraction": round(cta_removed, 4),  # everything keyed
            "flood_fraction": round(flood_removed, 4),          # border-connected only
            "enclosed_fraction": round(enclosed, 4),            # the interior at stake
            "edge_fraction": round(edge, 4),
        },
        "declared_inks": [h for h, _ in inks],
        "key_is_declared_ink": key_is_declared_ink,
        "decision_matters": decision_matters,
        "recommended_mode": recommended,
        "reason": reason,
        "warnings": warnings,
    }


def knockout(input_path: Path, output_path: Path, mode: str, color_spec: str,
             fuzz: float, feather: int, force: bool, expect_colors: list) -> dict:
    src, arr, rgb, orig_alpha, already_transparent = _load(input_path)

    if already_transparent and not force and color_spec.strip().lower() in ("auto", ""):
        if input_path.resolve() != output_path.resolve():
            shutil.copyfile(input_path, output_path)
        return {"skipped": True, "reason": "input already has transparency",
                "output": str(output_path)}

    key = _parse_color(color_spec, rgb)
    cta_rgb, cta_alpha = _color_to_alpha(rgb, key)
    ramp_alpha = _ramp(cta_alpha, fuzz)

    if mode == "color-to-alpha":
        out_rgb = cta_rgb
        out_alpha = ramp_alpha * orig_alpha
    elif mode == "flood":
        region = _flood_region(rgb, fuzz)
        if feather > 0:
            m = Image.fromarray((region * 255).astype(np.uint8))
            m = m.filter(ImageFilter.MaxFilter(2 * feather + 1))  # catch the AA fringe
            region_d = np.asarray(m) > 0
        else:
            region_d = region
        out_rgb = np.where(region_d[..., None], cta_rgb, arr[:, :, :3])
        out_alpha = np.where(region_d, ramp_alpha, 1.0) * orig_alpha
    else:
        raise ValueError(f"unknown --mode '{mode}' (use color-to-alpha or flood)")

    out = np.dstack([
        out_rgb.astype(np.uint8),
        np.clip(out_alpha * 255.0, 0, 255).round().astype(np.uint8),
    ])
    Image.fromarray(out).save(output_path, format="PNG")

    total = out_alpha.size
    removed = int((out_alpha < 0.02).sum())
    partial = int(((out_alpha >= 0.02) & (out_alpha < 0.98)).sum())

    # Non-fatal sanity check against the declared inks, if provided.
    warnings = []
    if expect_colors:
        dists = [float(np.sqrt(((key - c) ** 2).sum())) for c in expect_colors]
        key_is_ink = min(dists) <= _INK_MATCH_TOL
        if key_is_ink and mode == "color-to-alpha":
            warnings.append(f"knocked out {_hexstr(key)} but it matches a declared "
                            "ink — if that color is meant to print, use --mode flood.")
        if not key_is_ink and mode == "flood":
            warnings.append(f"kept enclosed {_hexstr(key)} (flood) but it is not a "
                            "declared ink — if it is background, use --mode color-to-alpha.")

    return {
        "output": str(output_path),
        "mode": mode,
        "key_color": _hexstr(key),
        "key_source": "auto" if color_spec.strip().lower() in ("auto", "") else "explicit",
        "fuzz": fuzz,
        "feather": feather if mode == "flood" else None,
        "size_px": [int(src.width), int(src.height)],
        "removed_fraction": round(removed / total, 4),
        "edge_fraction": round(partial / total, 4),
        "warnings": warnings,
    }


def _parse_expect(raw: str) -> list:
    if not raw:
        return []
    out = []
    for tok in raw.replace(",", " ").split():
        out.append(_hex_to_rgb(tok))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Knock a solid background color out of flat art (color-key, not segmentation)")
    parser.add_argument("--input", required=True, help="Path to the source image")
    parser.add_argument("--output", help="Path to write the RGBA PNG to (required unless --analyze)")
    parser.add_argument(
        "--analyze", action="store_true",
        help="Don't write anything — report what each mode would do and, with "
             "--expect-colors, recommend one. Run this first when unsure.")
    parser.add_argument(
        "--mode", default="color-to-alpha", choices=["color-to-alpha", "flood"],
        help="color-to-alpha: remove the key color everywhere with clean edges "
             "(default). flood: remove only the border-connected background, "
             "keeping enclosed regions (die-cut).")
    parser.add_argument(
        "--color", default="auto",
        help="Key color as '#RRGGBB', or 'auto' to read it from the corners (default).")
    parser.add_argument(
        "--expect-colors", default="",
        help="The decoration's declared inks as '#RRGGBB' (comma/space separated). "
             "Used to recommend a mode (analyze) and to warn on a conflicting choice. "
             "A guide, not gospel — reconcile it with the reported evidence.")
    parser.add_argument(
        "--fuzz", type=float, default=0.10,
        help="Tolerance 0..1: pixels within this fraction of the key color go "
             "fully transparent (soaks up JPEG speckle). Default 0.10.")
    parser.add_argument(
        "--feather", type=int, default=2,
        help="flood mode only: dilate the removed region by this many pixels so "
             "the anti-aliased fringe is feathered too. Default 2.")
    parser.add_argument(
        "--force", action="store_true",
        help="Run even if the input already has transparency (otherwise skipped).")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: input not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    if not 0.0 <= args.fuzz <= 1.0:
        print("ERROR: --fuzz must be between 0 and 1", file=sys.stderr)
        sys.exit(1)

    try:
        expect = _parse_expect(args.expect_colors)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        if args.analyze:
            receipt = analyze(input_path, args.color, args.fuzz, expect)
        else:
            if not args.output:
                print("ERROR: --output is required unless --analyze", file=sys.stderr)
                sys.exit(1)
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            receipt = knockout(input_path, output_path, args.mode, args.color,
                               args.fuzz, max(0, args.feather), args.force, expect)
    except Exception as e:
        print(f"ERROR: knockout failed: {e}", file=sys.stderr)
        sys.exit(2)

    print(json.dumps(receipt))


if __name__ == "__main__":
    main()
