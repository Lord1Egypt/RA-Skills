#!/usr/bin/env python
"""Render a PDF preview to PNG pages and locate each caption's page.

Usage:
    python verify_layout.py preview.pdf --pages-dir pages [--scale 1.7] [--out pages.txt]

Writes pages/pNN.png plus a UTF-8 index listing which page holds each
"图N"/"表N" caption, so the exhibit pages can be opened and inspected visually.

Requires pypdfium2 (`pip install pypdfium2`).
"""

import argparse
import re
from pathlib import Path

import pypdfium2 as pdfium


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--pages-dir", default="pages")
    ap.add_argument("--scale", type=float, default=1.7)
    ap.add_argument("--out", default="pages.txt")
    args = ap.parse_args()

    pdf = pdfium.PdfDocument(args.pdf)
    pages_dir = Path(args.pages_dir)
    pages_dir.mkdir(parents=True, exist_ok=True)
    for old in pages_dir.glob("p*.png"):
        old.unlink()

    lines = ["pdf: %s" % args.pdf, "pages: %d" % len(pdf)]
    for index in range(len(pdf)):
        page = pdf[index]
        bitmap = page.render(scale=args.scale)
        image = bitmap.to_pil()
        image.save(pages_dir / ("p%02d.png" % (index + 1)))
        text = page.get_textpage().get_text_range()
        found = re.findall(r"(图\s?\d+|表\s?\d+)", text)
        if found:
            lines.append("p%02d: %s" % (index + 1, " ".join(dict.fromkeys(found))))

    Path(args.out).write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
