#!/usr/bin/env python3
"""
extract_pdf.py — Extract text from PDF files using pdfplumber.
Usage: python3 extract_pdf.py <input.pdf> <output.txt>
"""

import sys
import os

def extract_pdf(input_path: str, output_path: str) -> None:
    try:
        import pdfplumber
    except ImportError:
        import subprocess, pathlib
        python = str(pathlib.Path.home() / ".workbuddy/binaries/python/envs/default/bin/python3")
        subprocess.run([python, "-m", "pip", "install", "pdfplumber", "-q"], check=True)
        import pdfplumber

    if not os.path.exists(input_path):
        print(f"ERROR: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Extracting text from: {input_path}")

    all_text = []
    with pdfplumber.open(input_path) as pdf:
        total = len(pdf.pages)
        print(f"Total pages: {total}")
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                all_text.append(f"\n{'='*60}\nPage {i}/{total}\n{'='*60}\n{text}")
            if i % 20 == 0:
                print(f"  Processed {i}/{total} pages...")

    output = "\n".join(all_text)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"Done! Extracted {len(all_text)} pages with text.")
    print(f"Output: {output_path}")
    print(f"File size: {os.path.getsize(output_path) / 1024:.1f} KB")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 extract_pdf.py <input.pdf> <output.txt>")
        sys.exit(1)
    extract_pdf(sys.argv[1], sys.argv[2])
