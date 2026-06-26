#!/usr/bin/env python3
"""
doc_scanner.py — Microsoft Lens-style document scanner.

Detects document edges in a photo, applies perspective correction (four-point warp),
removes shadows, and enhances the image to produce a clean scanned appearance.

Requires: opencv-python-headless, numpy, Pillow
Optional: img2pdf (for PDF output)

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


# ---------------------------------------------------------------------------
# Dependency checks
# ---------------------------------------------------------------------------

def _require_cv2():
    try:
        import cv2
        return cv2
    except ImportError:
        print(
            "Error: opencv-python-headless is not installed.\n"
            "Install it with:  pip install opencv-python-headless",
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
            "Install it with:  pip install Pillow",
            file=sys.stderr,
        )
        sys.exit(1)


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def _order_points(pts: np.ndarray) -> np.ndarray:
    """
    Order four corner points as: top-left, top-right, bottom-right, bottom-left.
    """
    rect = np.zeros((4, 2), dtype=np.float32)
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]   # top-left: smallest x+y
    rect[2] = pts[np.argmax(s)]   # bottom-right: largest x+y
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # top-right: smallest y-x
    rect[3] = pts[np.argmax(diff)]  # bottom-left: largest y-x
    return rect


def _four_point_transform(image: np.ndarray, pts: np.ndarray) -> np.ndarray:
    """
    Apply a perspective warp to extract the document region defined by pts.
    Output is warped to a standard A4 aspect ratio at the detected width.
    """
    cv2 = _require_cv2()
    rect = _order_points(pts)
    tl, tr, br, bl = rect

    # Compute output dimensions
    width_a = np.linalg.norm(br - bl)
    width_b = np.linalg.norm(tr - tl)
    max_width = max(int(width_a), int(width_b))

    height_a = np.linalg.norm(tr - br)
    height_b = np.linalg.norm(tl - bl)
    max_height = max(int(height_a), int(height_b))

    # If detected shape is wider than tall, swap to portrait
    if max_width > max_height:
        max_width, max_height = max_height, max_width

    dst = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1],
    ], dtype=np.float32)

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (max_width, max_height))
    return warped


# ---------------------------------------------------------------------------
# Document edge detection
# ---------------------------------------------------------------------------

def _find_document_corners(image: np.ndarray) -> np.ndarray | None:
    """
    Detect the four corners of a document in the image.
    Returns a (4, 2) float32 array of corner points, or None if not found.
    """
    cv2 = _require_cv2()
    h, w = image.shape[:2]

    # Resize for faster processing
    scale = min(1.0, 800 / max(h, w))
    small = cv2.resize(image, (int(w * scale), int(h * scale)))

    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Edge detection with auto-threshold
    v = np.median(blurred)
    lower = max(0, int(0.67 * v))
    upper = min(255, int(1.33 * v))
    edges = cv2.Canny(blurred, lower, upper)

    # Dilate to close gaps
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    edges = cv2.dilate(edges, kernel, iterations=1)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    # Sort by area descending; document should be one of the largest contours
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for contour in contours[:10]:
        area = cv2.contourArea(contour)
        image_area = small.shape[0] * small.shape[1]

        # Document must occupy at least 15% of the image
        if area < 0.15 * image_area:
            continue

        # Approximate polygon
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        if len(approx) == 4:
            # Rescale back to original resolution
            corners = approx.reshape(4, 2).astype(np.float32) / scale
            return corners

    return None


def _parse_manual_corners(corners_str: str, img_w: int, img_h: int) -> np.ndarray:
    """
    Parse a manual corners string like "50,30 800,20 820,1100 40,1120".
    Also supports percentages: "5%,3% 80%,2% 82%,110% 4%,112%" (will be clipped).
    Returns (4, 2) float32 array.
    """
    parts = corners_str.strip().split()
    if len(parts) != 4:
        raise ValueError(f"Expected 4 corner points, got {len(parts)}")
    corners = []
    for p in parts:
        x_str, y_str = p.split(",")
        x = (float(x_str.strip("%")) / 100 * img_w) if "%" in x_str else float(x_str)
        y = (float(y_str.strip("%")) / 100 * img_h) if "%" in y_str else float(y_str)
        corners.append([x, y])
    return np.array(corners, dtype=np.float32)


# ---------------------------------------------------------------------------
# Image enhancement
# ---------------------------------------------------------------------------

def _remove_shadows(image: np.ndarray) -> np.ndarray:
    """
    Estimate and remove uneven lighting / shadows using morphological operations.
    Works on BGR or grayscale images.
    """
    cv2 = _require_cv2()
    if len(image.shape) == 3:
        channels = cv2.split(image)
        result_channels = []
        for ch in channels:
            result_channels.append(_remove_shadows_channel(ch))
        return cv2.merge(result_channels)
    return _remove_shadows_channel(image)


def _remove_shadows_channel(ch: np.ndarray) -> np.ndarray:
    cv2 = _require_cv2()
    # Dilate to estimate the background (removes foreground text)
    dilated = cv2.dilate(ch, np.ones((21, 21), np.uint8))
    # Blur to get a smooth background estimate
    bg = cv2.GaussianBlur(dilated, (21, 21), 0)
    # Normalize: foreground = ch / bg
    normalized = cv2.divide(ch.astype(np.float32), bg.astype(np.float32))
    # Scale to 0–255
    result = np.clip(normalized * 255, 0, 255).astype(np.uint8)
    return result


def _enhance_bw(image: np.ndarray) -> np.ndarray:
    """
    Convert to clean black-and-white using adaptive thresholding (Sauvola-like).
    Returns a grayscale image with clean binary appearance.
    """
    cv2 = _require_cv2()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    # Adaptive threshold — handles uneven lighting better than global
    bw = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=21,
        C=10,
    )
    # Light denoising
    bw = cv2.fastNlMeansDenoising(bw, h=10)
    return bw


def _enhance_gray(image: np.ndarray) -> np.ndarray:
    """
    Grayscale output with CLAHE contrast enhancement.
    """
    cv2 = _require_cv2()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    return enhanced


def _enhance_color(image: np.ndarray) -> np.ndarray:
    """
    Color output: sharpen and boost contrast while preserving colors.
    """
    cv2 = _require_cv2()
    # Sharpen
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)
    sharpened = cv2.filter2D(image, -1, kernel)
    # CLAHE on L channel (LAB color space)
    lab = cv2.cvtColor(sharpened, cv2.COLOR_BGR2LAB)
    l_ch, a_ch, b_ch = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l_ch = clahe.apply(l_ch)
    enhanced_lab = cv2.merge([l_ch, a_ch, b_ch])
    enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    return enhanced


# ---------------------------------------------------------------------------
# DPI embedding
# ---------------------------------------------------------------------------

def _save_with_dpi(image_array: np.ndarray, output_path: Path, dpi: int, mode: str) -> None:
    """Save image with DPI metadata using Pillow."""
    Image = _require_pil()
    cv2 = _require_cv2()

    if mode == "bw":
        pil_image = Image.fromarray(image_array, mode="L")
    elif mode == "gray":
        pil_image = Image.fromarray(image_array, mode="L")
    else:
        # cv2 is BGR; Pillow expects RGB
        rgb = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb)

    pil_image.save(str(output_path), dpi=(dpi, dpi))


def _save_as_pdf(image_paths: list[Path], output_path: Path, dpi: int) -> None:
    """Combine images into a PDF using img2pdf if available, else Pillow."""
    try:
        import img2pdf
        with open(str(output_path), "wb") as f:
            f.write(img2pdf.convert([str(p) for p in image_paths]))
    except ImportError:
        Image = _require_pil()
        images = [Image.open(str(p)).convert("RGB") for p in image_paths]
        if images:
            images[0].save(
                str(output_path), save_all=True,
                append_images=images[1:],
                resolution=dpi,
            )


# ---------------------------------------------------------------------------
# Core scan pipeline
# ---------------------------------------------------------------------------

def scan_image(
    input_path: Path,
    output_path: Path,
    mode: str = "bw",
    dpi: int = 300,
    no_warp: bool = False,
    manual_corners: str | None = None,
) -> dict:
    """
    Full scan pipeline for one image.
    Returns a status dict with metadata.
    """
    cv2 = _require_cv2()
    t_start = time.time()

    image = cv2.imread(str(input_path))
    if image is None:
        return {"status": "error", "error": f"Could not read image: {input_path}"}

    h, w = image.shape[:2]
    result = {
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

    # 1. Detect or parse corners
    corners = None
    if not no_warp:
        if manual_corners:
            try:
                corners = _parse_manual_corners(manual_corners, w, h)
                result["corners_detected"] = True
                result["corners"] = corners.tolist()
            except ValueError as e:
                result["warnings"].append(f"Manual corners parse error: {e} — skipping warp")
                corners = None
        else:
            corners = _find_document_corners(image)
            if corners is not None:
                result["corners_detected"] = True
                result["corners"] = corners.tolist()
            else:
                result["warnings"].append(
                    "Auto edge-detection could not find document corners — skipping perspective warp"
                )

    # 2. Perspective warp
    if corners is not None and not no_warp:
        image = _four_point_transform(image, corners)
        result["warp_applied"] = True

    # 3. Shadow removal (before enhancement)
    image = _remove_shadows(image)

    # 4. Enhancement
    if mode == "bw":
        final = _enhance_bw(image)
    elif mode == "gray":
        final = _enhance_gray(image)
    else:
        final = _enhance_color(image)

    out_h, out_w = final.shape[:2]
    result["output_size"] = [out_w, out_h]

    # 5. Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    _save_with_dpi(final, output_path, dpi, mode)

    result["processing_time_s"] = round(time.time() - t_start, 2)
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="doc_scanner",
        description="Microsoft Lens-style document scanner — perspective correction and enhancement.",
    )
    parser.add_argument("--input", nargs="+", required=True, help="Input image file(s)")
    parser.add_argument("--output", required=True, help="Output file (.png, .jpg, or .pdf)")
    parser.add_argument(
        "--mode", choices=["bw", "gray", "color"], default="bw",
        help="Enhancement mode: bw (black & white), gray, color (default: bw)",
    )
    parser.add_argument(
        "--format", choices=["image", "pdf"], default="image",
        help="Output format: image (default) or pdf",
    )
    parser.add_argument("--dpi", type=int, default=300, help="Output DPI (default: 300)")
    parser.add_argument("--no-warp", action="store_true", help="Skip perspective correction")
    parser.add_argument(
        "--corners",
        help='Manual corner points: "x1,y1 x2,y2 x3,y3 x4,y4" (pixels or %%)',
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    input_paths = [Path(p).expanduser() for p in args.input]
    output_path = Path(args.output).expanduser()

    for p in input_paths:
        if not p.exists():
            print(f"Error: Input file not found: {p}", file=sys.stderr)
            return 1

    # Determine output format from extension if not set
    out_fmt = args.format
    if output_path.suffix.lower() == ".pdf":
        out_fmt = "pdf"

    if out_fmt == "pdf" or len(input_paths) > 1:
        # Multi-page or PDF mode
        temp_pages: list[Path] = []
        all_results = []

        for i, inp in enumerate(input_paths):
            temp_out = output_path.parent / f"_scan_temp_page{i+1:03d}.png"
            result = scan_image(
                inp, temp_out,
                mode=args.mode,
                dpi=args.dpi,
                no_warp=args.no_warp,
                manual_corners=getattr(args, "corners", None),
            )
            all_results.append(result)
            if result["status"] == "success":
                temp_pages.append(temp_out)
            else:
                print(f"Error processing {inp}: {result.get('error')}", file=sys.stderr)

        if temp_pages:
            _save_as_pdf(temp_pages, output_path, args.dpi)
            # Clean up temp files
            for tp in temp_pages:
                tp.unlink(missing_ok=True)

        summary = {
            "status": "success" if all(r["status"] == "success" for r in all_results) else "partial",
            "pages": len(temp_pages),
            "output_file": str(output_path),
            "output_dpi": args.dpi,
            "enhancement_mode": args.mode,
            "page_results": all_results,
        }
        print(json.dumps(summary), file=sys.stderr)
        if not temp_pages:
            return 1
    else:
        # Single image mode
        result = scan_image(
            input_paths[0], output_path,
            mode=args.mode,
            dpi=args.dpi,
            no_warp=args.no_warp,
            manual_corners=getattr(args, "corners", None),
        )
        print(json.dumps(result), file=sys.stderr)
        if result["status"] != "success":
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
