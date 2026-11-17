#!/usr/bin/env python3
"""Read a job description (JD) from any common file format into plain text.

Supports .txt / .md / .markdown / .rtf directly, and .pdf / .docx via the pdfmuse
engine (auto-installed on first use, same as the resume-parsing skill). Prints the
plain text to stdout; use --out to also write it to a file.

Usage:
    python scripts/read_jd.py JD.pdf
    python scripts/read_jd.py JD.md --out jd.txt
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

PLAIN_EXT = {".txt", ".md", ".markdown", ".text"}
PDFMUSE_EXT = {".pdf", ".docx"}


def _ensure_pdfmuse():
    try:
        import pdfmuse  # noqa: F401
        return pdfmuse
    except ImportError:
        print("pdfmuse not found -- installing (one-time)...", file=sys.stderr)
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "pdfmuse"],
                       check=True)
        import pdfmuse  # noqa: F401
        return pdfmuse


def _strip_rtf(data: bytes) -> str:
    """Very small RTF-to-text fallback (control words stripped)."""
    import re
    text = data.decode("latin-1", errors="ignore")
    text = re.sub(r"\\'[0-9a-fA-F]{2}", "", text)      # hex escapes
    text = re.sub(r"\\[a-zA-Z]+-?\d* ?", "", text)     # control words
    text = re.sub(r"[{}]", "", text)                    # groups
    return text.strip()


def read_jd(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext in PLAIN_EXT:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read().strip()
    if ext == ".rtf":
        with open(path, "rb") as f:
            return _strip_rtf(f.read())
    if ext in PDFMUSE_EXT:
        pdfmuse = _ensure_pdfmuse()
        with open(path, "rb") as f:
            return pdfmuse.to_text(f.read()).strip()
    if ext == ".doc":
        raise SystemExit(
            "Legacy .doc (binary Word 97-2003) is not supported. Re-save the JD "
            "as .docx, .pdf, or .txt and try again."
        )
    # Unknown extension: try reading as UTF-8 text before giving up.
    try:
        with open(path, encoding="utf-8") as f:
            return f.read().strip()
    except (UnicodeDecodeError, OSError) as e:
        raise SystemExit(f"Cannot read JD '{path}' ({ext or 'no extension'}): {e}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Read a JD file into plain text.")
    ap.add_argument("path", help="JD file (.txt/.md/.pdf/.docx/.rtf)")
    ap.add_argument("--out", help="also write the text to this file")
    args = ap.parse_args()

    if not os.path.isfile(args.path):
        raise SystemExit(f"File not found: {args.path}")

    text = read_jd(args.path)
    if not text:
        print("WARN: JD text is empty after extraction.", file=sys.stderr)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"wrote {args.out} ({len(text)} chars)", file=sys.stderr)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
