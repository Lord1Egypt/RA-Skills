#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Optional

import cv2

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from calibration import ensure_calibration  # noqa: E402

DEFAULT_IMAGE = Path('/tmp/macos_desktop_control/screen_logical.png')


def locate_template(image_path: Path, template_path: Path, threshold: float = 0.8) -> Optional[dict]:
    image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    template = cv2.imread(str(template_path), cv2.IMREAD_COLOR)

    if image is None:
        raise FileNotFoundError(f'Could not read image: {image_path}')
    if template is None:
        raise FileNotFoundError(f'Could not read template: {template_path}')

    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    _min_val, max_val, _min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val < threshold:
        return None

    h, w = template.shape[:2]
    x, y = max_loc
    return {
        'type': 'opencv_template',
        'x': x + w / 2,
        'y': y + h / 2,
        'box': {'left': x, 'top': y, 'width': w, 'height': h},
        'confidence': float(max_val),
        'threshold': threshold,
    }


def main() -> None:
    ensure_calibration()
    parser = argparse.ArgumentParser(description='Locate an image template on a logical screenshot using OpenCV.')
    parser.add_argument('--image', type=Path, default=DEFAULT_IMAGE)
    parser.add_argument('--template', type=Path, required=True)
    parser.add_argument('--threshold', type=float, default=0.8)
    parser.add_argument('--json', action='store_true', help='Print full JSON result instead of x y only.')
    args = parser.parse_args()

    result = locate_template(args.image, args.template, args.threshold)
    if not result:
        raise SystemExit(f'Template not found above threshold: {args.threshold}')

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{int(result['x'])} {int(result['y'])}")


if __name__ == '__main__':
    main()
