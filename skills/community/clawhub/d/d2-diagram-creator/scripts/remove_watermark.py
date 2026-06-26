#!/usr/bin/env python3
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: python remove_watermark.py <svg_file_path>")
        sys.exit(1)

    svg_path = Path(sys.argv[1])

    if not svg_path.exists():
        print(f"Error: File not found - {svg_path}")
        sys.exit(1)

    content = svg_path.read_text(encoding='utf-8')
    new_content = content.replace('UNLICENSED COPY', '')

    if content == new_content:
        print("'UNLICENSED COPY' text not found")
        return

    svg_path.write_text(new_content, encoding='utf-8')
    print(f"Watermark removed: {svg_path}")


if __name__ == '__main__':
    main()
