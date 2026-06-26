#!/usr/bin/env python3
import json
import sys
from pathlib import Path

try:
    from PIL import Image
except Exception as exc:
    Image = None
    PIL_IMPORT_ERROR = exc
else:
    PIL_IMPORT_ERROR = None


def analyze(path: Path) -> dict:
    im = Image.open(path).convert("RGB")
    w, h = im.size
    if w < 120 or h < 120:
        return {"ok": False, "reason": "too_small", "width": w, "height": h}

    all_pixels = list(im.getdata())
    total = max(1, len(all_pixels))
    black_all_ratio = sum(1 for r, g, b in all_pixels if max(r, g, b) < 85) / total
    dark_all_ratio = sum(1 for r, g, b in all_pixels if max(r, g, b) < 150) / total
    bright_all_ratio = sum(1 for r, g, b in all_pixels if min(r, g, b) > 245) / total
    faint_gray_ratio = sum(
        1
        for r, g, b in all_pixels
        if 150 <= max(r, g, b) < 235 and max(r, g, b) - min(r, g, b) < 35
    ) / total
    mid_gray_ratio = sum(
        1
        for r, g, b in all_pixels
        if abs(r - g) < 12 and abs(g - b) < 12 and 70 < max(r, g, b) < 210
    ) / total

    x1, y1 = int(w * 0.35), int(h * 0.35)
    x2, y2 = int(w * 0.65), int(h * 0.65)
    center = [im.getpixel((x, y)) for y in range(y1, y2) for x in range(x1, x2)]
    center_total = max(1, len(center))
    black_center_ratio = sum(1 for r, g, b in center if max(r, g, b) < 85) / center_total
    dark_center_ratio = sum(1 for r, g, b in center if max(r, g, b) < 150) / center_total
    gray_center_ratio = sum(
        1
        for r, g, b in center
        if abs(r - g) < 12 and abs(g - b) < 12 and 70 < max(r, g, b) < 210
    ) / center_total

    metrics = {
        "width": w,
        "height": h,
        "blackAllRatio": round(black_all_ratio, 4),
        "darkAllRatio": round(dark_all_ratio, 4),
        "brightAllRatio": round(bright_all_ratio, 4),
        "faintGrayRatio": round(faint_gray_ratio, 4),
        "midGrayRatio": round(mid_gray_ratio, 4),
        "blackCenterRatio": round(black_center_ratio, 4),
        "darkCenterRatio": round(dark_center_ratio, 4),
        "grayCenterRatio": round(gray_center_ratio, 4),
    }

    # Expired Douyin QR crops are usually washed out: the QR modules become
    # pale gray, and a gray refresh mask/text sits over the center. A valid
    # Douyin QR has a dark logo in the center, so center darkness alone is not
    # an invalid signal.
    if black_all_ratio < 0.08 and gray_center_ratio > 0.18:
        return {
            "ok": False,
            "reason": "expired_refresh_overlay",
            **metrics,
        }

    if black_all_ratio < 0.12 or dark_all_ratio < 0.18:
        return {
            "ok": False,
            "reason": "too_faint",
            **metrics,
        }

    if bright_all_ratio < 0.25:
        return {
            "ok": False,
            "reason": "missing_quiet_zone_or_overlaid",
            **metrics,
        }

    return {
        "ok": True,
        "reason": "looks_scannable",
        **metrics,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(json.dumps({"ok": False, "reason": "usage", "usage": "detect-qr-image.py /path/qrcode.png"}))
        return 2
    path = Path(sys.argv[1])
    if not path.exists():
        print(json.dumps({"ok": False, "reason": "not_found", "path": str(path)}))
        return 2
    if Image is None:
        print(json.dumps({
            "ok": False,
            "reason": "dependency_missing_pillow",
            "error": str(PIL_IMPORT_ERROR),
            "path": str(path),
        }, ensure_ascii=False))
        return 2
    try:
        result = analyze(path)
    except Exception as exc:
        result = {"ok": False, "reason": "analysis_error", "error": str(exc), "path": str(path)}
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
