#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Optional

import Quartz
import Vision
from PIL import Image

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from calibration import ensure_calibration  # noqa: E402

DEFAULT_IMAGE = Path('/tmp/macos_desktop_control/screen_logical.png')


def crop_region(image_path: Path, x1: int, y1: int, x2: int, y2: int) -> tuple[Path, int, int]:
    with Image.open(image_path) as img:
        left = max(0, min(x1, img.width))
        top = max(0, min(y1, img.height))
        right = max(0, min(x2, img.width))
        bottom = max(0, min(y2, img.height))
        if right <= left or bottom <= top:
            raise ValueError(f'Invalid region after clamping: {(left, top, right, bottom)}')

        cropped = img.crop((left, top, right, bottom))
        region_path = image_path.with_name(f'{image_path.stem}-region{image_path.suffix}')
        cropped.save(region_path)
        return region_path, left, top


def load_cgimage(image_path: Path):
    path_str = str(image_path)
    url = Quartz.CFURLCreateFromFileSystemRepresentation(None, path_str.encode('utf-8'), len(path_str), False)
    image_source = Quartz.CGImageSourceCreateWithURL(url, None)
    if image_source is None:
        raise FileNotFoundError(f'Could not read image: {image_path}')

    cg_image = Quartz.CGImageSourceCreateImageAtIndex(image_source, 0, None)
    if cg_image is None:
        raise FileNotFoundError(f'Could not decode image: {image_path}')
    return cg_image


def prepare_image_for_ocr(image_path: Path, upscale: int = 3) -> Path:
    if upscale <= 1:
        return image_path

    img = Image.open(image_path)
    upscaled_path = image_path.with_name(f'{image_path.stem}-upscaled{image_path.suffix}')
    img.resize((img.width * upscale, img.height * upscale)).save(upscaled_path)
    return upscaled_path


def locate_text(
    image_path: Path,
    target_text: str,
    upscale: int = 3,
    region: Optional[tuple[int, int, int, int]] = None,
) -> Optional[dict]:
    offset_x = 0
    offset_y = 0
    working_image = image_path
    if region is not None:
        working_image, offset_x, offset_y = crop_region(image_path, *region)

    prepared_image = prepare_image_for_ocr(working_image, upscale=upscale)
    cg_image = load_cgimage(prepared_image)
    image_width = Quartz.CGImageGetWidth(cg_image)
    image_height = Quartz.CGImageGetHeight(cg_image)

    request = Vision.VNRecognizeTextRequest.alloc().init()
    request.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)
    request.setUsesLanguageCorrection_(True)
    request.setRecognitionLanguages_(['zh-Hans', 'zh-Hant', 'en-US'])

    handler = Vision.VNImageRequestHandler.alloc().initWithCGImage_options_(cg_image, None)
    success, error = handler.performRequests_error_([request], None)
    if not success:
        message = str(error) if error is not None else 'Unknown Vision OCR error'
        raise RuntimeError(message)

    target = target_text.strip().lower()
    best = None

    for observation in request.results() or []:
        top_candidates = observation.topCandidates_(3)
        if not top_candidates:
            continue

        chosen = None
        for recognized in top_candidates:
            text = str(recognized.string() or '').strip()
            if not text:
                continue
            lower_text = text.lower()
            if target in lower_text or lower_text in target:
                chosen = recognized
                break

        if chosen is None:
            continue

        text = str(chosen.string() or '').strip()
        bbox = observation.boundingBox()
        left = bbox.origin.x * image_width
        width = bbox.size.width * image_width
        top = (1.0 - bbox.origin.y - bbox.size.height) * image_height
        height = bbox.size.height * image_height
        confidence = float(chosen.confidence())

        # Convert coordinates back to the original image scale when upscaling was used.
        scale = float(upscale if upscale > 1 else 1)
        candidate = {
            'type': 'vision_text',
            'text': text,
            'target': target_text,
            'x': (left + width / 2) / scale + offset_x,
            'y': (top + height / 2) / scale + offset_y,
            'box': {
                'left': int(round(left / scale)) + offset_x,
                'top': int(round(top / scale)) + offset_y,
                'width': int(round(width / scale)),
                'height': int(round(height / scale)),
            },
            'confidence': confidence,
        }
        if best is None or candidate['confidence'] > best['confidence']:
            best = candidate

    return best


def main() -> None:
    ensure_calibration()
    parser = argparse.ArgumentParser(description='Locate text on a logical screenshot using Apple Vision OCR.')
    parser.add_argument('--image', type=Path, default=DEFAULT_IMAGE)
    parser.add_argument('--text', required=True)
    parser.add_argument('--upscale', type=int, default=3, help='Upscale factor before Apple Vision OCR.')
    parser.add_argument('--x1', type=int, help='Optional region left bound.')
    parser.add_argument('--y1', type=int, help='Optional region top bound.')
    parser.add_argument('--x2', type=int, help='Optional region right bound.')
    parser.add_argument('--y2', type=int, help='Optional region bottom bound.')
    parser.add_argument('--json', action='store_true', help='Print full JSON result instead of x y only.')
    args = parser.parse_args()

    region = None
    region_args = [args.x1, args.y1, args.x2, args.y2]
    if any(v is not None for v in region_args):
        if not all(v is not None for v in region_args):
            raise SystemExit('Region search requires --x1 --y1 --x2 --y2 together.')
        region = (args.x1, args.y1, args.x2, args.y2)

    result = locate_text(args.image, args.text, upscale=args.upscale, region=region)
    if not result:
        raise SystemExit(f'Text not found: {args.text}')

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{int(result['x'])} {int(result['y'])}")


if __name__ == '__main__':
    main()
