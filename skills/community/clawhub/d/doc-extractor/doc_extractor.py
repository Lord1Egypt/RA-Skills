#!/usr/bin/env python3
"""
Document Text Extractor — extract readable text from DOCX, PDF, and TXT files.

Backends:
  - DOCX: zipfile + xml.etree (stdlib)
  - PDF: pymupdf (optional, `pip install pymupdf`)
  - TXT: direct read with encoding detection (stdlib)

Usage:
  python doc_extractor.py extract <file> [--output out.txt]
  python doc_extractor.py list-formats
  python doc_extractor.py batch <dir> [--outdir ./out] [--ext .docx,.txt]
"""

import argparse
import os
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from typing import Dict, List, Optional, Set


# ── DOCX Extractor (stdlib only) ────────────────────────────────────────────


def _extract_docx_text(path: str) -> str:
    """Extract text from a .docx file using zipfile + xml.etree."""
    parts: List[str] = []

    with zipfile.ZipFile(path, "r") as z:
        # Main document body
        if "word/document.xml" in z.namelist():
            tree = ET.parse(z.open("word/document.xml"))
            root = tree.getroot()
            # Office Open XML namespace
            ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

            for t in root.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"):
                if t.text:
                    parts.append(t.text)

            # Add paragraph breaks (p elements)
            for p in root.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"):
                parts.append("\n")

        # Also extract text from headers/footers if present
        for extra in ["word/header1.xml", "word/header2.xml", "word/footer1.xml", "word/footer2.xml"]:
            if extra in z.namelist():
                try:
                    tree = ET.parse(z.open(extra))
                    root = tree.getroot()
                    for t in root.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"):
                        if t.text:
                            parts.append(t.text)
                except Exception:
                    pass

    text = "".join(parts)
    # Clean up excessive whitespace
    import re
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ── PDF Extractor (optional pymupdf) ─────────────────────────────────────────


def _extract_pdf_text(path: str) -> str:
    """Extract text from a PDF using pymupdf (optional dependency)."""
    try:
        import fitz  # pymupdf
    except ImportError:
        print(
            "⚠  PDF extraction requires pymupdf. Install with: pip install pymupdf",
            file=sys.stderr,
        )
        sys.exit(1)

    doc = fitz.open(path)
    parts: List[str] = []
    for page_num, page in enumerate(doc):
        text = page.get_text()
        if text.strip():
            parts.append(f"--- Page {page_num + 1} ---\n{text.strip()}")
    doc.close()
    return "\n\n".join(parts)


# ── Text File Extractor ─────────────────────────────────────────────────────


ENCODINGS = ["utf-8", "utf-16", "latin-1", "cp1252"]


def _extract_text_file(path: str) -> str:
    """Read a plain text file with encoding auto-detection."""
    for enc in ENCODINGS:
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read().strip()
        except UnicodeDecodeError:
            continue
        except UnicodeError:
            continue
    # Last resort: read with errors replaced
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read().strip()


# ── Format detection ────────────────────────────────────────────────────────


SUPPORTED_FORMATS: Dict[str, tuple] = {
    ".docx": ("DOCX (Word)", _extract_docx_text, "stdlib"),
    ".pdf": ("PDF (Adobe)", _extract_pdf_text, "pymupdf"),
    ".txt": ("Plain Text", _extract_text_file, "stdlib"),
    ".md": ("Markdown", _extract_text_file, "stdlib (read as txt)"),
    ".csv": ("CSV", _extract_text_file, "stdlib (read as txt)"),
    ".json": ("JSON", _extract_text_file, "stdlib (read as txt)"),
    ".xml": ("XML", _extract_text_file, "stdlib (read as txt)"),
    ".html": ("HTML", _extract_text_file, "stdlib (read as txt)"),
    ".htm": ("HTML", _extract_text_file, "stdlib (read as txt)"),
    ".log": ("Log", _extract_text_file, "stdlib (read as txt)"),
    ".yaml": ("YAML", _extract_text_file, "stdlib (read as txt)"),
    ".yml": ("YAML", _extract_text_file, "stdlib (read as txt)"),
    ".toml": ("TOML", _extract_text_file, "stdlib (read as txt)"),
    ".ini": ("INI", _extract_text_file, "stdlib (read as txt)"),
    ".cfg": ("Config", _extract_text_file, "stdlib (read as txt)"),
}


def _get_extractor(path: str):
    """Return the extractor function for a file, or None if unsupported."""
    ext = os.path.splitext(path)[1].lower()
    info = SUPPORTED_FORMATS.get(ext)
    if info:
        return info[1]
    return None


def _check_pymupdf_available() -> bool:
    """Check if pymupdf is installed."""
    try:
        import fitz  # noqa: F401
        return True
    except ImportError:
        return False


# ── Commands ─────────────────────────────────────────────────────────────────


def cmd_extract(args: argparse.Namespace) -> None:
    path = args.file
    if not os.path.isfile(path):
        print(f"⚠  File not found: {path}", file=sys.stderr)
        sys.exit(1)

    extractor = _get_extractor(path)
    if not extractor:
        ext = os.path.splitext(path)[1]
        print(f"⚠  Unsupported format: {ext}", file=sys.stderr)
        print("   Run 'list-formats' to see supported formats.", file=sys.stderr)
        sys.exit(1)

    # Check PDF dependency
    if path.lower().endswith(".pdf") and not _check_pymupdf_available():
        print(
            "⚠  PDF extraction requires pymupdf. Install with: pip install pymupdf",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        text = extractor(path)
    except Exception as e:
        print(f"⚠  Failed to extract {path}: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"✅  Extracted {path}")
        print(f"   Saved to: {args.output}  ({len(text)} chars)")
    else:
        print(f"📄  {os.path.basename(path)} ({len(text)} chars)\n")
        print("─" * 50)
        print(text[:5000])
        if len(text) > 5000:
            print("\n… (truncated, use --output to save full text)")
        print("─" * 50)


def cmd_list_formats() -> None:
    pymupdf_ok = _check_pymupdf_available()
    print("📋  Supported Document Formats\n")
    print(f"{'Extension':<12} {'Format':<30} {'Required':<20}")
    print("─" * 62)
    for ext, (name, _, dep) in sorted(SUPPORTED_FORMATS.items()):
        dep_label = dep
        if ext == ".pdf":
            dep_label = "✓ pymupdf" if pymupdf_ok else "✗ pymupdf (pip install)"
        print(f"{ext:<12} {name:<30} {dep_label:<20}")
    print()
    if not pymupdf_ok:
        print("💡  Install PDF support: pip install pymupdf")


def cmd_batch(args: argparse.Namespace) -> None:
    directory = args.dir
    if not os.path.isdir(directory):
        print(f"⚠  Directory not found: {directory}", file=sys.stderr)
        sys.exit(1)

    # Filter by extensions if provided
    allowed_exts: Optional[Set[str]] = None
    if args.ext:
        allowed_exts = {e if e.startswith(".") else f".{e}" for e in args.ext.split(",")}

    outdir = args.outdir
    if outdir:
        os.makedirs(outdir, exist_ok=True)

    files_found = []
    for root, _dirs, files in os.walk(directory):
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if allowed_exts and ext not in allowed_exts:
                continue
            if ext in SUPPORTED_FORMATS:
                files_found.append(os.path.join(root, fname))

    if not files_found:
        print("⚠  No supported files found in", directory)
        return

    total = len(files_found)
    success = 0
    failed = 0

    print(f"📂  Batch extracting {total} file(s) from {directory}\n")

    for i, fpath in enumerate(files_found, 1):
        rel = os.path.relpath(fpath, directory)
        ext = os.path.splitext(fpath)[1].lower()

        # Check PDF dependency
        if ext == ".pdf" and not _check_pymupdf_available():
            print(f"  [{i}/{total}] ⚠  {rel} — PDF support requires pymupdf, skipping")
            failed += 1
            continue

        extractor = _get_extractor(fpath)
        try:
            text = extractor(fpath)
        except Exception as e:
            print(f"  [{i}/{total}] ✗  {rel} — {e}")
            failed += 1
            continue

        if outdir:
            out_path = os.path.join(outdir, os.path.splitext(rel)[0] + ".txt")
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"  [{i}/{total}] ✓  {rel} → {out_path} ({len(text)} chars)")
        else:
            print(f"  [{i}/{total}] ✓  {rel} ({len(text)} chars)")
        success += 1

    print(f"\nDone: {success} succeeded, {failed} failed out of {total} file(s)")


# ── CLI ─────────────────────────────────────────────────────────────────────


def _self_test():
    """Real test of the core text/encoding extraction (no PDF/DOCX deps)."""
    import tempfile, os
    d = tempfile.mkdtemp(prefix="de_selftest_")
    try:
        # Plain text file extraction
        p = os.path.join(d, "sample.txt")
        with open(p, "w", encoding="utf-8") as f:
            f.write("Hello world\nSecond line\n")
        txt = _extract_text_file(p)
        if txt != "Hello world\nSecond line":
            print(f"self-test: FAIL (txt extract: {txt!r})")
            return 1

        # UTF-16 encoding auto-detection
        p2 = os.path.join(d, "utf16.txt")
        with open(p2, "w", encoding="utf-16") as f:
            f.write("unicode content 你好")
        txt2 = _extract_text_file(p2)
        if txt2 != "unicode content 你好":
            print(f"self-test: FAIL (utf16 extract: {txt2!r})")
            return 1

        # Format detection
        if _get_extractor(p) is not _extract_text_file:
            print("self-test: FAIL (extractor routing for .txt wrong)")
            return 1
        if _get_extractor(os.path.join(d, "x.unknownext")) is not None:
            print("self-test: FAIL (unknown ext should have no extractor)")
            return 1
        print("self-test: PASS")
        return 0
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(
        description="Document Text Extractor — extract text from DOCX, PDF, and TXT files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s extract report.docx\n"
            "  %(prog)s extract paper.pdf --output paper.txt\n"
            "  %(prog)s batch ./documents/ --outdir ./texts/\n"
            "  %(prog)s batch ./reports/ --ext .docx,.pdf\n"
            "  %(prog)s list-formats\n"
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # extract
    p_extract = sub.add_parser("extract", help="Extract text from a single file")
    p_extract.add_argument("file", help="Path to the file (DOCX, PDF, or TXT)")
    p_extract.add_argument("--output", "-o", help="Save extracted text to file")

    # list-formats
    p_list = sub.add_parser("list-formats", help="List supported file formats")
    p_list.set_defaults(func=lambda _: cmd_list_formats())

    # batch
    p_batch = sub.add_parser("batch", help="Batch extract all files in a directory")
    p_batch.add_argument("dir", help="Directory containing documents")
    p_batch.add_argument("--outdir", help="Output directory (default: print all)")
    p_batch.add_argument("--ext", help="Comma-separated extensions (e.g., .docx,.pdf)")

    # self-test
    sub.add_parser("self-test", help="Run built-in self tests")

    args = parser.parse_args()

    if args.command == "extract":
        cmd_extract(args)
    elif args.command == "list-formats":
        cmd_list_formats()
    elif args.command == "batch":
        cmd_batch(args)
    elif args.command == "self-test":
        sys.exit(_self_test())
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
