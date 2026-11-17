#!/usr/bin/env python3
"""Extract text from a PDF file.

Usage:
    python extract_pdf_text.py <pdf_path> [out_txt]

Tries (in order): pypdf, pdfplumber, pdfminer.six. If none is installed,
prints a clear install hint and exits 2.
"""
from __future__ import annotations

import sys
from pathlib import Path


def _try_pypdf(pdf_path: str) -> str:
    from pypdf import PdfReader

    reader = PdfReader(pdf_path)
    chunks = []
    for i, page in enumerate(reader.pages):
        chunks.append(f"\n\n----- PAGE {i + 1} -----\n")
        chunks.append(page.extract_text() or "")
    return "".join(chunks)


def _try_pdfplumber(pdf_path: str) -> str:
    import pdfplumber

    chunks = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            chunks.append(f"\n\n----- PAGE {i + 1} -----\n")
            chunks.append(page.extract_text() or "")
    return "".join(chunks)


def _try_pdfminer(pdf_path: str) -> str:
    from pdfminer.high_level import extract_text

    return extract_text(pdf_path)


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: extract_pdf_text.py <pdf_path> [out_txt]", file=sys.stderr)
        return 1

    pdf_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) >= 3 else None

    if not Path(pdf_path).exists():
        print(f"ERROR: file not found: {pdf_path}", file=sys.stderr)
        return 1

    text = None
    last_err: Exception | None = None
    for fn in (_try_pypdf, _try_pdfplumber, _try_pdfminer):
        try:
            text = fn(pdf_path)
            break
        except Exception as e:  # noqa: BLE001
            last_err = e
            continue

    if text is None:
        print(
            "ERROR: no PDF library available. Install one of:\n"
            "  pip install pypdf\n"
            "  pip install pdfplumber\n"
            "  pip install pdfminer.six\n"
            f"Last error: {last_err}",
            file=sys.stderr,
        )
        return 2

    if out_path:
        Path(out_path).write_text(text, encoding="utf-8")
        print(f"Wrote {len(text):,} chars to {out_path}")
    else:
        sys.stdout.write(text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
