#!/usr/bin/env python3
"""
doc_scanner.py — Professional-quality document scanner.

Converts a photo of a document into a clean, flat scan by:
  1. Detecting document edges (multi-strategy: Canny, gradient, colour-contrast)
  2. Applying four-point perspective warp to flatten and deskew the document
  3. Removing shadows and uneven lighting
  4. Enhancing the result to look like a real flatbed scanner output
     (crisp text, pure-white background, no table/background visible)

Requires: opencv-python-headless>=4.9, numpy>=1.24, Pillow>=10.0
Optional:  img2pdf>=0.5  (for PDF output; Pillow fallback used if absent)

Usage:
  python doc_scanner.py --input photo.jpg --output scanned.png
  python doc_scanner.py --input photo.jpg --output scanned.png --mode bw
  python doc_scanner.py --input photo.jpg --output scanned.png --mode color
  python doc_scanner.py --input photo.jpg --output scanned.pdf --format pdf
  python doc_scanner.py --input p1.jpg p2.jpg p3.jpg --output doc.pdf --format pdf
  python doc_scanner.py --input photo.jpg --output scanned.png --corners "50,30 800,20 820,1100 40,1120"
  python doc_scanner.py --input photo.jpg --output scanned.png --no-warp
  python doc_scanner.py --input photo.jpg --output scanned.png --dpi 300
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np


# ─────────────────────────────────────────────────────────────────────────────
# Dependency guards
# ─────────────────────────────────────────────────────────────────────────────

def _require_cv2():
    try:
        import cv2
        return cv2
    except ImportError:
        print(
            "Error: opencv-python-headless is not installed.\n"
            "Install with:  pip install opencv-python-headless",
            file=sys.stderr,
        )
        sys.exit(1)


def _require_pil():
    try:
        from PIL import Image
        return Image
    except ImportError:
        print(
            "Error: Pillow is not installed.\n"
            "Install with:  pip install Pillow",
            file=sys.stderr,
        )
        sys.exit(1)


# ─────────────────────────────────────────────────────────────────────────────
# Geometry helpers
# ─────────────────────────────────────────────────────────────────────────────

def _order_points(pts: np.ndarray) -> np.ndarray:
    """Order four points as: top-left, top-right, bottom-right, bottom-left."""
    rect = np.zeros((4, 2), dtype=np.float32)
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]    # top-left:     smallest x+y
    rect[2] = pts[np.argmax(s)]    # bottom-right: largest  x+y
    diff = np.diff(pts, axis=1).ravel()
    rect[1] = pts[np.argmin(diff)] # top-right:    smallest y-x
    rect[3] = pts[np.argmax(diff)] # bottom-left:  largest  y-x
    return rect


def _four_point_transform(image: np.ndarray, pts: np.ndarray) -> np.ndarray:
    """Perspective-warp the document region defined by pts to a flat rectangle."""
    cv2 = _require_cv2()
    rect = _order_points(pts)
    tl, tr, br, bl = rect

    width_a  = float(np.linalg.norm(br - bl))
    width_b  = float(np.linalg.norm(tr - tl))
    max_width = max(int(width_a), int(width_b))

    height_a  = float(np.linalg.norm(tr - br))
    height_b  = float(np.linalg.norm(tl - bl))
    max_height = max(int(height_a), int(height_b))

    # Ensure portrait orientation
    if max_width > max_height:
        max_width, max_height = max_height, max_width

    dst = np.array([
        [0,           0],
        [max_width-1, 0],
        [max_width-1, max_height-1],
        [0,           max_height-1],
    ], dtype=np.float32)

    M = cv2.getPerspectiveTransform(rect, dst)
    return cv2.warpPerspective(image, M, (max_width, max_height),
                                flags=cv2.INTER_LANCZOS4)


def _is_valid_quad(corners: np.ndarray, img_w: int, img_h: int) -> bool:
    """
    Sanity-check a four-point polygon:
    - Must be convex
    - Must cover at least 10 % of image area
    - All corners inside (or just outside) the image frame
    """
    cv2 = _require_cv2()
    hull = cv2.convexHull(corners.astype(np.float32))
    area = cv2.contourArea(hull)
    image_area = img_w * img_h
    if area < 0.10 * image_area:
        return False
    # Check all corners are within 10 % of image boundaries
    margin_x, margin_y = 0.10 * img_w, 0.10 * img_h
    for x, y in corners:
        if x < -margin_x or x > img_w + margin_x:
            return False
        if y < -margin_y or y > img_h + margin_y:
            return False
    return True


# ─────────────────────────────────────────────────────────────────────────────
# Document edge detection  (multi-strategy)
# ─────────────────────────────────────────────────────────────────────────────

def _find_quad_in_contours(contours, scale: float, img_w: int, img_h: int,
                            min_area_frac: float = 0.10) -> np.ndarray | None:
    """
    Walk contours largest-first looking for a convex 4-sided polygon that
    covers at least *min_area_frac* of the image.
    """
    cv2 = _require_cv2()
    image_area = img_w * img_h
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < min_area_frac * image_area * scale * scale:
            continue
        peri  = cv2.arcLength(contour, True)
        # Try progressively looser approximations to find a 4-side polygon
        for eps_factor in (0.02, 0.03, 0.04, 0.05, 0.06):
            approx = cv2.approxPolyDP(contour, eps_factor * peri, True)
            if len(approx) == 4:
                corners = (approx.reshape(4, 2).astype(np.float32) / scale)
                if _is_valid_quad(corners, img_w, img_h):
                    return corners
    return None


def _find_document_corners(image: np.ndarray) -> np.ndarray | None:
    """
    Detect the four corners of a document in *image* using three strategies
    tried in order; returns the first that yields a valid quadrilateral.

    Strategy A — Canny edges on greyscale (best for high-contrast docs)
    Strategy B — Morphological gradient on greyscale (handles low contrast)
    Strategy C — Colour-based: brightest region assumed to be the document
                 (works when the doc is white on a dark or coloured table)
    """
    cv2 = _require_cv2()
    h, w = image.shape[:2]

    # Work on a downscaled copy for speed
    long_side = max(h, w)
    scale = min(1.0, 1024 / long_side)
    small = cv2.resize(image, (int(w * scale), int(h * scale)),
                       interpolation=cv2.INTER_AREA)
    sh, sw = small.shape[:2]

    gray    = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    # ── Strategy A: Canny ────────────────────────────────────────────────────
    v      = float(np.median(blurred))
    lower  = max(0,   int(0.50 * v))
    upper  = min(255, int(1.50 * v))
    edges  = cv2.Canny(blurred, lower, upper)
    # Close gaps with a moderate kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.dilate(edges, kernel, iterations=2)
    closed = cv2.morphologyEx(closed, cv2.MORPH_CLOSE, kernel, iterations=1)
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    result = _find_quad_in_contours(contours, scale, w, h)
    if result is not None:
        return result

    # ── Strategy B: Morphological gradient ──────────────────────────────────
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    grad    = cv2.morphologyEx(blurred, cv2.MORPH_GRADIENT, kernel2)
    _, thresh_grad = cv2.threshold(grad, 0, 255,
                                   cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    closed2  = cv2.dilate(thresh_grad, kernel, iterations=2)
    contours2, _ = cv2.findContours(closed2, cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
    contours2 = sorted(contours2, key=cv2.contourArea, reverse=True)
    result = _find_quad_in_contours(contours2, scale, w, h)
    if result is not None:
        return result

    # ── Strategy C: Colour / brightness thresholding ─────────────────────────
    # Assume the document is brighter than its background; find the largest
    # bright region and approximate its bounding quad.
    hsv     = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
    _, bright_mask = cv2.threshold(hsv[:, :, 2], 0, 255,
                                   cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    bright_mask = cv2.morphologyEx(bright_mask, cv2.MORPH_CLOSE,
                                   np.ones((15, 15), np.uint8))
    contours3, _ = cv2.findContours(bright_mask, cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
    contours3 = sorted(contours3, key=cv2.contourArea, reverse=True)
    result = _find_quad_in_contours(contours3, scale, w, h, min_area_frac=0.15)
    if result is not None:
        return result

    return None


def _refine_corners(image: np.ndarray, corners: np.ndarray) -> np.ndarray:
    """
    Sub-pixel corner refinement using cv2.cornerSubPix so the warp is as
    precise as possible.
    """
    cv2 = _require_cv2()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    pts  = corners.copy().reshape(-1, 1, 2).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    refined = cv2.cornerSubPix(gray, pts, (11, 11), (-1, -1), criteria)
    return refined.reshape(4, 2)


def _parse_manual_corners(corners_str: str, img_w: int, img_h: int) -> np.ndarray:
    """
    Parse a corners string like "50,30 800,20 820,1100 40,1120".
    Accepts pixel values or percentages ("5%,3%").
    """
    parts = corners_str.strip().split()
    if len(parts) != 4:
        raise ValueError(f"Expected 4 corner points, got {len(parts)}")
    corners = []
    for p in parts:
        x_s, y_s = p.split(",")
        x = (float(x_s.strip("%")) / 100 * img_w) if "%" in x_s else float(x_s)
        y = (float(y_s.strip("%")) / 100 * img_h) if "%" in y_s else float(y_s)
        corners.append([x, y])
    return np.array(corners, dtype=np.float32)


# ─────────────────────────────────────────────────────────────────────────────
# Image enhancement — scan quality
# ─────────────────────────────────────────────────────────────────────────────

def _remove_shadows(image: np.ndarray) -> np.ndarray:
    """
    Estimate and subtract uneven lighting/shadows per channel.
    Uses a large dilate to estimate the background, then normalises.
    """
    cv2 = _require_cv2()
    def _normalise_channel(ch: np.ndarray) -> np.ndarray:
        dilated = cv2.dilate(ch, np.ones((31, 31), np.uint8))
        bg      = cv2.GaussianBlur(dilated, (31, 31), 0).astype(np.float32)
        norm    = cv2.divide(ch.astype(np.float32), bg)
        return np.clip(norm * 255, 0, 255).astype(np.uint8)

    if len(image.shape) == 3:
        channels = cv2.split(image)
        return cv2.merge([_normalise_channel(c) for c in channels])
    return _normalise_channel(image)


def _enhance_bw(image: np.ndarray) -> np.ndarray:
    """
    Produce a crisp, scanner-quality black-and-white image.

    Pipeline:
      1. Convert to greyscale
      2. Auto-levels: stretch histogram to 0–255
      3. Adaptive threshold with block size proportional to resolution
      4. Morphological close to reconnect broken strokes
      5. Fast non-local-means denoising
      6. Ensure pure white background (invert if needed)
    """
    cv2 = _require_cv2()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image

    # Auto-levels: stretch contrast
    lo, hi = np.percentile(gray, (2, 98))
    if hi > lo:
        gray = np.clip((gray.astype(np.float32) - lo) / (hi - lo) * 255,
                       0, 255).astype(np.uint8)

    # Adaptive threshold — block size 1/20 of shortest dimension, always odd
    short_side  = min(gray.shape[:2])
    block_size  = max(11, int(short_side / 20) | 1)   # ensure odd
    bw = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=block_size,
        C=12,
    )

    # Close small gaps in strokes (prevents speckled text)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    bw = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)

    # Denoise
    bw = cv2.fastNlMeansDenoising(bw, h=8, templateWindowSize=7,
                                   searchWindowSize=21)

    # Ensure the background is white (more white pixels → correct polarity)
    if np.count_nonzero(bw < 128) > bw.size * 0.5:
        bw = cv2.bitwise_not(bw)

    return bw


def _enhance_gray(image: np.ndarray) -> np.ndarray:
    """
    Greyscale output: auto-levels + CLAHE + unsharp mask for crisp text.
    """
    cv2 = _require_cv2()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image

    # Auto-levels
    lo, hi = np.percentile(gray, (1, 99))
    if hi > lo:
        gray = np.clip((gray.astype(np.float32) - lo) / (hi - lo) * 255,
                       0, 255).astype(np.uint8)

    # CLAHE
    clahe   = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Unsharp mask
    blurred  = cv2.GaussianBlur(enhanced, (0, 0), 1.5)
    sharp    = cv2.addWeighted(enhanced, 1.5, blurred, -0.5, 0)
    return sharp


def _enhance_color(image: np.ndarray) -> np.ndarray:
    """
    Colour output: white-balance normalisation + CLAHE + sharpening.
    Preserves all colour content while making the background as white as possible.
    """
    cv2 = _require_cv2()
    # White-balance: stretch each channel independently
    balanced = image.copy().astype(np.float32)
    for i in range(3):
        lo, hi = np.percentile(balanced[:, :, i], (1, 99))
        if hi > lo:
            balanced[:, :, i] = np.clip(
                (balanced[:, :, i] - lo) / (hi - lo) * 255, 0, 255)
    balanced = balanced.astype(np.uint8)

    # CLAHE on L channel (LAB) for contrast boost without colour shift
    lab               = cv2.cvtColor(balanced, cv2.COLOR_BGR2LAB)
    l_ch, a_ch, b_ch  = cv2.split(lab)
    clahe             = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_ch              = clahe.apply(l_ch)
    enhanced          = cv2.cvtColor(cv2.merge([l_ch, a_ch, b_ch]),
                                     cv2.COLOR_LAB2BGR)

    # Sharpen
    kernel   = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)
    sharpened = cv2.filter2D(enhanced, -1, kernel)
    return sharpened


def _add_scan_border(image: np.ndarray, border_px: int = 8) -> np.ndarray:
    """
    Add a clean white border to simulate the scanner bed edge.
    Works for both greyscale (2D) and colour (3D) images.
    """
    cv2 = _require_cv2()
    fill = 255
    return cv2.copyMakeBorder(image, border_px, border_px, border_px, border_px,
                              cv2.BORDER_CONSTANT, value=fill)


# ─────────────────────────────────────────────────────────────────────────────
# Output helpers
# ─────────────────────────────────────────────────────────────────────────────

def _save_with_dpi(array: np.ndarray, output_path: Path, dpi: int,
                   mode: str) -> None:
    """Save with embedded DPI metadata using Pillow."""
    cv2 = _require_cv2()
    Image = _require_pil()
    if mode in ("bw", "gray"):
        pil_img = Image.fromarray(array, mode="L")
    else:
        pil_img = Image.fromarray(cv2.cvtColor(array, cv2.COLOR_BGR2RGB))
    pil_img.save(str(output_path), dpi=(dpi, dpi))


def _save_as_pdf(image_paths: list[Path], output_path: Path, dpi: int) -> None:
    """Combine images into a PDF (img2pdf preferred, Pillow fallback)."""
    try:
        import img2pdf
        with open(str(output_path), "wb") as f:
            f.write(img2pdf.convert([str(p) for p in image_paths]))
    except ImportError:
        Image = _require_pil()
        images = [Image.open(str(p)).convert("RGB") for p in image_paths]
        if images:
            images[0].save(str(output_path), save_all=True,
                           append_images=images[1:], resolution=dpi)


# ─────────────────────────────────────────────────────────────────────────────
# Core pipeline
# ─────────────────────────────────────────────────────────────────────────────

def scan_image(
    input_path: Path,
    output_path: Path,
    mode: str = "bw",
    dpi: int = 300,
    no_warp: bool = False,
    manual_corners: str | None = None,
) -> dict:
    """
    Full scan pipeline for a single image.  Returns a status dict.

    Steps:
      1. Load image
      2. Detect document corners (multi-strategy) or use manual hints
      3. Sub-pixel corner refinement
      4. Four-point perspective warp (flattens the document)
      5. Shadow / uneven-lighting removal
      6. Mode-specific enhancement (bw / gray / color)
      7. Add scanner border
      8. Save with DPI metadata
    """
    cv2 = _require_cv2()
    t0 = time.time()

    image = cv2.imread(str(input_path))
    if image is None:
        return {"status": "error", "error": f"Cannot read: {input_path}"}

    h, w = image.shape[:2]
    result: dict = {
        "status": "success",
        "corners_detected": False,
        "corners": None,
        "warp_applied": False,
        "enhancement_mode": mode,
        "input_size": [w, h],
        "output_size": None,
        "output_dpi": dpi,
        "pages": 1,
        "output_file": str(output_path),
        "warnings": [],
    }

    # ── 1. Corner detection ──────────────────────────────────────────────────
    corners = None
    if not no_warp:
        if manual_corners:
            try:
                corners = _parse_manual_corners(manual_corners, w, h)
                result["corners_detected"] = True
            except ValueError as e:
                result["warnings"].append(f"Manual corners error: {e} — skipping warp")
        else:
            corners = _find_document_corners(image)
            if corners is not None:
                result["corners_detected"] = True
            else:
                result["warnings"].append(
                    "Auto edge-detection could not locate document corners — "
                    "enhancement applied without perspective warp. "
                    "Try --corners to provide hints, or re-photograph with the "
                    "document on a contrasting background."
                )

    # ── 2. Sub-pixel refinement + perspective warp ───────────────────────────
    if corners is not None and not no_warp:
        try:
            corners = _refine_corners(image, corners)
        except Exception:
            pass  # refinement is best-effort
        result["corners"] = corners.tolist()
        image = _four_point_transform(image, corners)
        result["warp_applied"] = True

    # ── 3. Shadow removal ────────────────────────────────────────────────────
    image = _remove_shadows(image)

    # ── 4. Enhancement ───────────────────────────────────────────────────────
    if mode == "bw":
        final = _enhance_bw(image)
    elif mode == "gray":
        final = _enhance_gray(image)
    else:
        final = _enhance_color(image)

    # ── 5. Scanner border ────────────────────────────────────────────────────
    final = _add_scan_border(final)

    out_h, out_w = final.shape[:2]
    result["output_size"] = [out_w, out_h]

    # ── 6. Save ──────────────────────────────────────────────────────────────
    output_path.parent.mkdir(parents=True, exist_ok=True)
    _save_with_dpi(final, output_path, dpi, mode)

    result["processing_time_s"] = round(time.time() - t0, 2)
    return result


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="doc_scanner",
        description="Professional document scanner — perspective correction and scan-quality output.",
    )
    p.add_argument("--input",  nargs="+", required=True, help="Input image file(s)")
    p.add_argument("--output", required=True, help="Output file (.png, .jpg, or .pdf)")
    p.add_argument("--mode",   choices=["bw", "gray", "color"], default="bw",
                   help="Enhancement mode: bw (default), gray, color")
    p.add_argument("--format", choices=["image", "pdf"], default="image",
                   help="Output format: image (default) or pdf")
    p.add_argument("--dpi",    type=int, default=300, help="Output DPI (default: 300)")
    p.add_argument("--no-warp", action="store_true",
                   help="Skip perspective correction (apply enhancement only)")
    p.add_argument("--corners",
                   help='Manual corner points: "x1,y1 x2,y2 x3,y3 x4,y4" (pixels or %%)')
    return p


def main() -> int:
    args   = build_parser().parse_args()
    inputs = [Path(p).expanduser() for p in args.input]
    output = Path(args.output).expanduser()

    for p in inputs:
        if not p.exists():
            print(f"Error: file not found: {p}", file=sys.stderr)
            return 1

    out_fmt = args.format
    if output.suffix.lower() == ".pdf":
        out_fmt = "pdf"

    if out_fmt == "pdf" or len(inputs) > 1:
        temp_pages: list[Path] = []
        all_results: list[dict] = []
        for i, inp in enumerate(inputs):
            tmp = output.parent / f"_scan_tmp_{i:03d}.png"
            r   = scan_image(inp, tmp, mode=args.mode, dpi=args.dpi,
                             no_warp=args.no_warp,
                             manual_corners=getattr(args, "corners", None))
            all_results.append(r)
            if r["status"] == "success":
                temp_pages.append(tmp)
            else:
                print(f"Error on {inp}: {r.get('error')}", file=sys.stderr)

        if temp_pages:
            _save_as_pdf(temp_pages, output, args.dpi)
            for tp in temp_pages:
                tp.unlink(missing_ok=True)

        summary = {
            "status": "success" if all(r["status"] == "success" for r in all_results) else "partial",
            "pages": len(temp_pages),
            "output_file": str(output),
            "output_dpi": args.dpi,
            "enhancement_mode": args.mode,
            "page_results": all_results,
        }
        print(json.dumps(summary), file=sys.stderr)
        return 0 if temp_pages else 1
    else:
        r = scan_image(inputs[0], output, mode=args.mode, dpi=args.dpi,
                       no_warp=args.no_warp,
                       manual_corners=getattr(args, "corners", None))
        print(json.dumps(r), file=sys.stderr)
        return 0 if r["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
