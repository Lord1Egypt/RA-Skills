#!/usr/bin/env python3
import argparse
from pathlib import Path

from PIL import Image


def main():
    parser = argparse.ArgumentParser(description='Crop a rectangular region from an image.')
    parser.add_argument('--image', required=True, help='Source image path')
    parser.add_argument('--x1', required=True, type=int)
    parser.add_argument('--y1', required=True, type=int)
    parser.add_argument('--x2', required=True, type=int)
    parser.add_argument('--y2', required=True, type=int)
    parser.add_argument('--output', required=True, help='Output image path')
    args = parser.parse_args()

    src = Path(args.image)
    dst = Path(args.output)
    if not src.exists():
        raise SystemExit(f'source image not found: {src}')

    with Image.open(src) as img:
        x1 = max(0, min(args.x1, img.width))
        y1 = max(0, min(args.y1, img.height))
        x2 = max(0, min(args.x2, img.width))
        y2 = max(0, min(args.y2, img.height))
        if x2 <= x1 or y2 <= y1:
            raise SystemExit(f'invalid crop bounds after clamping: {(x1, y1, x2, y2)}')
        cropped = img.crop((x1, y1, x2, y2))
        dst.parent.mkdir(parents=True, exist_ok=True)
        cropped.save(dst)

    print(f'{dst}')


if __name__ == '__main__':
    main()
