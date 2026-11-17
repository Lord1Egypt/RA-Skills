#!/usr/bin/env python3
"""Batch remove fixed-position watermarks with OpenCV inpainting."""

import argparse
import json
import sys
from pathlib import Path


SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Batch remove watermarks from images you own or have permission to edit. "
            "Provide one or more rectangle masks, or a white-on-black mask image."
        )
    )
    parser.add_argument("input_dir", type=Path, help="Folder containing source images.")
    parser.add_argument("output_dir", type=Path, help="Folder for cleaned images.")
    parser.add_argument(
        "--rect",
        action="append",
        default=[],
        metavar="X,Y,W,H",
        help="Watermark rectangle. Can be used multiple times.",
    )
    parser.add_argument(
        "--rects-json",
        type=Path,
        help='JSON file with rectangles, e.g. [[20,30,180,48], {"x":20,"y":30,"w":180,"h":48}].',
    )
    parser.add_argument(
        "--mask",
        type=Path,
        help="Mask image: white pixels mark the watermark area to repair.",
    )
    parser.add_argument(
        "--radius",
        type=float,
        default=3.0,
        help="Inpaint radius. Try 3-7 for larger watermarks.",
    )
    parser.add_argument(
        "--clear-alpha",
        action="store_true",
        help="For transparent PNGs, make the masked watermark area fully transparent.",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Also process images in nested folders.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing output files.",
    )
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        metavar="FILENAME",
        help="Only process matching file name. Can be used multiple times.",
    )
    return parser.parse_args()


def ensure_dependencies():
    try:
        import cv2
        import numpy as np
    except ImportError as exc:
        missing = exc.name or "required package"
        print(
            f"Missing dependency: {missing}\n\n"
            "Install once with:\n"
            "  python3 -m pip install -r requirements-watermark.txt\n",
            file=sys.stderr,
        )
        raise SystemExit(2) from exc

    return cv2, np


def iter_images(input_dir, recursive):
    pattern = "**/*" if recursive else "*"
    return sorted(
        path
        for path in input_dir.glob(pattern)
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTS
    )


def parse_rect(value):
    parts = [item.strip() for item in value.split(",")]
    if len(parts) != 4:
        raise ValueError(f"Invalid rectangle: {value}")
    x, y, width, height = [int(float(item)) for item in parts]
    if width <= 0 or height <= 0:
        raise ValueError(f"Rectangle width and height must be positive: {value}")
    return x, y, width, height


def load_rects(args):
    rects = [parse_rect(value) for value in args.rect]

    if args.rects_json:
        with args.rects_json.expanduser().open("r", encoding="utf-8") as file:
            data = json.load(file)
        for item in data:
            if isinstance(item, dict):
                rects.append(
                    (
                        int(item["x"]),
                        int(item["y"]),
                        int(item["w"]),
                        int(item["h"]),
                    )
                )
            else:
                rects.append(tuple(int(float(value)) for value in item))

    return rects


def build_mask(cv2, np, image_shape, rects, mask_path):
    height, width = image_shape[:2]
    mask = np.zeros((height, width), dtype=np.uint8)

    for x, y, rect_width, rect_height in rects:
        left = max(0, x)
        top = max(0, y)
        right = min(width, x + rect_width)
        bottom = min(height, y + rect_height)
        if left < right and top < bottom:
            mask[top:bottom, left:right] = 255

    if mask_path:
        mask_image = cv2.imread(str(mask_path.expanduser()), cv2.IMREAD_GRAYSCALE)
        if mask_image is None:
            raise ValueError(f"Cannot read mask image: {mask_path}")
        if mask_image.shape[:2] != (height, width):
            mask_image = cv2.resize(mask_image, (width, height), interpolation=cv2.INTER_NEAREST)
        mask = cv2.bitwise_or(mask, mask_image)

    _, mask = cv2.threshold(mask, 16, 255, cv2.THRESH_BINARY)
    return mask


def output_path_for(source, input_dir, output_dir):
    relative = source.relative_to(input_dir)
    if source.suffix.lower() == ".webp":
        return output_dir / relative.with_suffix(".png")
    return output_dir / relative


def main():
    args = parse_args()
    input_dir = args.input_dir.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()
    mask_path = args.mask.expanduser() if args.mask else None

    if not input_dir.is_dir():
        print(f"Input folder does not exist: {input_dir}", file=sys.stderr)
        return 1

    cv2, np = ensure_dependencies()
    rects = load_rects(args)
    if not rects and not mask_path:
        print("Provide at least one --rect, --rects-json, or --mask.", file=sys.stderr)
        return 1

    images = iter_images(input_dir, args.recursive)
    if args.only:
        wanted = set(args.only)
        images = [path for path in images if path.name in wanted]
    if not images:
        print(f"No supported images found in: {input_dir}")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    done = 0
    skipped = 0
    failed = 0

    for source in images:
        relative = source.relative_to(input_dir)
        target = output_path_for(source, input_dir, output_dir)
        target.parent.mkdir(parents=True, exist_ok=True)

        if target.exists() and not args.force:
            skipped += 1
            print(f"skip  {relative}")
            continue

        image = cv2.imread(str(source), cv2.IMREAD_UNCHANGED)
        if image is None:
            failed += 1
            print(f"fail  {relative}: cannot read image", file=sys.stderr)
            continue

        try:
            alpha = None
            if len(image.shape) == 3 and image.shape[2] == 4:
                alpha = image[:, :, 3]
                image = image[:, :, :3]

            mask = build_mask(cv2, np, image.shape, rects, mask_path)
            result = cv2.inpaint(image, mask, args.radius, cv2.INPAINT_TELEA)
            if alpha is not None:
                if args.clear_alpha:
                    alpha = alpha.copy()
                    alpha[mask > 0] = 0
                result = cv2.merge([result[:, :, 0], result[:, :, 1], result[:, :, 2], alpha])

            if not cv2.imwrite(str(target), result):
                raise ValueError("cannot write output image")

            done += 1
            print(f"done  {relative} -> {target.relative_to(output_dir)}")
        except Exception as exc:
            failed += 1
            print(f"fail  {relative}: {exc}", file=sys.stderr)

    print(f"\nProcessed: {done}, skipped: {skipped}, failed: {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
