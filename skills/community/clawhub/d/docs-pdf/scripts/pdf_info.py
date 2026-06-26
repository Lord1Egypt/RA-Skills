#!/usr/bin/env python3
"""
pdf_info.py — Display detailed information about a PDF file.

Shows: page count, file size, PDF version, page dimensions, encryption status,
form fields, metadata (author, creator, dates), and more.

Usage:
    python scripts/pdf_info.py input.pdf
    python scripts/pdf_info.py input.pdf --json           # machine-readable output
    python scripts/pdf_info.py input.pdf --pages           # include per-page details
    python scripts/pdf_info.py *.pdf                       # batch info
"""
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from pypdf import PdfReader


def human_size(nbytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if abs(nbytes) < 1024:
            return f"{nbytes:.1f} {unit}"
        nbytes /= 1024
    return f"{nbytes:.1f} TB"


def get_pdf_info(path: Path, include_pages: bool = False) -> dict:
    """Collect all PDF metadata into a dictionary."""
    file_size = path.stat().st_size
    reader = PdfReader(str(path))

    # Basic info
    info = {
        "file": str(path),
        "file_size": file_size,
        "file_size_human": human_size(file_size),
        "page_count": len(reader.pages),
        "encrypted": reader.is_encrypted,
    }

    # PDF version (from header)
    try:
        with open(path, "rb") as f:
            header = f.readline().decode("latin-1", errors="ignore").strip()
            if header.startswith("%PDF-"):
                info["pdf_version"] = header.replace("%PDF-", "")
    except Exception:
        pass

    # Page dimensions (from first page)
    if reader.pages:
        page0 = reader.pages[0]
        w = float(page0.mediabox.width)
        h = float(page0.mediabox.height)
        # Convert points to mm (1 pt = 0.3528 mm)
        w_mm = w * 0.3528
        h_mm = h * 0.3528
        info["page_size"] = {
            "width_pt": round(w, 1),
            "height_pt": round(h, 1),
            "width_mm": round(w_mm, 1),
            "height_mm": round(h_mm, 1),
            "label": _guess_page_size(w_mm, h_mm),
        }

    # Form fields
    fields = reader.get_fields()
    if fields:
        info["has_forms"] = True
        info["form_field_count"] = len(fields)
        info["form_fields"] = list(fields.keys())[:20]  # limit output
    else:
        info["has_forms"] = False
        info["form_field_count"] = 0

    # Metadata
    meta = reader.metadata
    if meta:
        md = {}
        if meta.title:
            md["title"] = meta.title
        if meta.author:
            md["author"] = meta.author
        if meta.creator:
            md["creator"] = meta.creator
        if meta.producer:
            md["producer"] = meta.producer
        if meta.subject:
            md["subject"] = meta.subject
        if meta.creation_date:
            md["creation_date"] = str(meta.creation_date)
        if meta.modification_date:
            md["modification_date"] = str(meta.modification_date)
        info["metadata"] = md

    # Check for text content (is it a scan?)
    try:
        import pdfplumber
        with pdfplumber.open(str(path)) as pdf:
            sample_text = ""
            for p in pdf.pages[:3]:
                t = p.extract_text()
                if t:
                    sample_text += t
            info["has_text"] = len(sample_text.strip()) > 20
            info["is_likely_scan"] = not info["has_text"]
    except ImportError:
        info["has_text"] = "unknown (pdfplumber not installed)"

    # Per-page details
    if include_pages:
        pages_info = []
        for i, page in enumerate(reader.pages):
            pg = {
                "page": i + 1,
                "width_pt": round(float(page.mediabox.width), 1),
                "height_pt": round(float(page.mediabox.height), 1),
                "rotation": page.get("/Rotate", 0),
            }
            pages_info.append(pg)
        info["pages"] = pages_info

    return info


def _guess_page_size(w_mm: float, h_mm: float) -> str:
    """Guess standard page size from dimensions."""
    sizes = {
        "A4": (210, 297),
        "A3": (297, 420),
        "A5": (148, 210),
        "Letter": (216, 279),
        "Legal": (216, 356),
        "B5": (176, 250),
    }
    for name, (sw, sh) in sizes.items():
        if (abs(w_mm - sw) < 5 and abs(h_mm - sh) < 5) or \
           (abs(w_mm - sh) < 5 and abs(h_mm - sw) < 5):
            orientation = "portrait" if h_mm > w_mm else "landscape"
            return f"{name} ({orientation})"
    return "custom"


def print_info(info: dict) -> None:
    """Pretty-print PDF info to terminal."""
    print(f"\n{'='*60}")
    print(f"📄 {info['file']}")
    print(f"{'='*60}")
    print(f"  File size:     {info['file_size_human']} ({info['file_size']:,} bytes)")
    print(f"  Pages:         {info['page_count']}")
    print(f"  PDF version:   {info.get('pdf_version', 'unknown')}")
    print(f"  Encrypted:     {'Yes ⚠️' if info['encrypted'] else 'No'}")

    if "page_size" in info:
        ps = info["page_size"]
        print(f"  Page size:     {ps['width_mm']}×{ps['height_mm']} mm"
              f"  ({ps['width_pt']}×{ps['height_pt']} pt)"
              f"  [{ps['label']}]")

    print(f"  Has forms:     {'Yes (' + str(info['form_field_count']) + ' fields)' if info['has_forms'] else 'No'}")

    if "is_likely_scan" in info and isinstance(info.get("is_likely_scan"), bool):
        print(f"  Likely scan:   {'Yes (use OCR)' if info['is_likely_scan'] else 'No (has selectable text)'}")

    if "metadata" in info:
        print(f"\n  📋 Metadata:")
        for k, v in info["metadata"].items():
            print(f"    {k}: {v}")

    if "pages" in info:
        print(f"\n  📑 Per-page details:")
        for pg in info["pages"]:
            rot = f"  (rotated {pg['rotation']}°)" if pg["rotation"] else ""
            print(f"    Page {pg['page']:>4d}: {pg['width_pt']}×{pg['height_pt']} pt{rot}")

    print()


def main():
    parser = argparse.ArgumentParser(description="Display PDF file information")
    parser.add_argument("inputs", nargs="+", help="Input PDF file(s)")
    parser.add_argument("--json", "-j", action="store_true",
                        help="Output as JSON")
    parser.add_argument("--pages", "-p", action="store_true",
                        help="Include per-page details")
    args = parser.parse_args()

    all_info = []
    for pattern in args.inputs:
        from glob import glob as g
        expanded = g(pattern)
        paths = [Path(p) for p in expanded] if expanded else [Path(pattern)]

        for path in paths:
            if not path.exists():
                print(f"  ✗ Not found: {path}", file=sys.stderr)
                continue
            try:
                info = get_pdf_info(path, include_pages=args.pages)
                all_info.append(info)
                if not args.json:
                    print_info(info)
            except Exception as e:
                print(f"  ✗ Error reading {path}: {e}", file=sys.stderr)

    if args.json:
        output = all_info if len(all_info) > 1 else (all_info[0] if all_info else {})
        print(json.dumps(output, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
