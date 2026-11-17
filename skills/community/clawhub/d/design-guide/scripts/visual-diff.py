#!/usr/bin/env python3
import argparse
import json
import pathlib
import sys

try:
    from i18n import add_locale_argument, t
except ModuleNotFoundError:  # Imported by the repository test suite.
    from scripts.i18n import add_locale_argument, t


def load_pillow():
    try:
        from PIL import Image, ImageChops
    except ModuleNotFoundError as exc:
        raise RuntimeError("Pillow is required: python3 -m pip install Pillow") from exc
    return Image, ImageChops


def compare_images(
    baseline_path: pathlib.Path,
    current_path: pathlib.Path,
    diff_path: pathlib.Path | None = None,
    pixel_threshold: int = 16,
) -> dict:
    if not 0 <= pixel_threshold <= 255:
        raise ValueError("pixel_threshold must be between 0 and 255")
    Image, ImageChops = load_pillow()
    with Image.open(baseline_path) as baseline_source:
        baseline = baseline_source.convert("RGBA")
    with Image.open(current_path) as current_source:
        current = current_source.convert("RGBA")
    if baseline.size != current.size:
        return {
            "comparable": False,
            "baselineSize": list(baseline.size),
            "currentSize": list(current.size),
            "differentPixels": None,
            "totalPixels": None,
            "ratio": 1.0,
        }

    difference = ImageChops.difference(baseline, current).convert("RGB")
    different_pixels = sum(
        1 for red, green, blue in difference.getdata() if max(red, green, blue) > pixel_threshold
    )
    total_pixels = baseline.width * baseline.height
    ratio = different_pixels / total_pixels if total_pixels else 0.0
    if diff_path:
        diff_path.parent.mkdir(parents=True, exist_ok=True)
        difference.save(diff_path)
    return {
        "comparable": True,
        "baselineSize": list(baseline.size),
        "currentSize": list(current.size),
        "differentPixels": different_pixels,
        "totalPixels": total_pixels,
        "ratio": ratio,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=t("Compare two UI screenshots with a pixel tolerance."))
    add_locale_argument(parser)
    parser.add_argument("baseline")
    parser.add_argument("current")
    parser.add_argument("--diff-out")
    parser.add_argument("--max-ratio", type=float, default=0.01)
    parser.add_argument("--pixel-threshold", type=int, default=16)
    parser.add_argument("--json-out")
    args = parser.parse_args()

    if not 0 <= args.max_ratio <= 1:
        parser.error("--max-ratio must be between 0 and 1")
    if not 0 <= args.pixel_threshold <= 255:
        parser.error("--pixel-threshold must be between 0 and 255")

    baseline = pathlib.Path(args.baseline).expanduser().resolve()
    current = pathlib.Path(args.current).expanduser().resolve()
    diff = pathlib.Path(args.diff_out).expanduser().resolve() if args.diff_out else None
    try:
        result = compare_images(
            baseline,
            current,
            diff,
            pixel_threshold=args.pixel_threshold,
        )
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(t("visual-diff failed: {error}", args.locale, error=exc), file=sys.stderr)
        return 2
    result["maxRatio"] = args.max_ratio
    result["passed"] = result["comparable"] and result["ratio"] <= args.max_ratio
    output = json.dumps(result, indent=2) + "\n"
    if args.json_out:
        output_path = pathlib.Path(args.json_out).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
    print(output, end="")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
