#!/usr/bin/env python3
"""
batch_convert.py — Batch PDF operations (merge / split / rotate / watermark / encrypt).

Usage:
    python scripts/batch_convert.py merge   --input ./docs/  --output merged.pdf
    python scripts/batch_convert.py split   --input big.pdf  --every 10 --output ./parts/
    python scripts/batch_convert.py rotate  --input ./scans/ --deg 90  --output ./rotated/
    python scripts/batch_convert.py watermark --input ./docs/ --text "DRAFT" --output ./wm/
"""
import argparse
import glob
import io
import sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter

# ── Helpers ───────────────────────────────────────────────────────────────────

def collect_pdfs(src: str, sort=True) -> list[Path]:
    p = Path(src)
    if p.is_dir():
        paths = list(p.glob("*.pdf"))
    else:
        paths = [Path(x) for x in glob.glob(src)]
    return sorted(paths) if sort else paths

def build_wm_page(text, font_size, color, alpha, angle, pagesize):
    from reportlab.pdfgen import canvas as rl
    from reportlab.lib.colors import HexColor
    buf = io.BytesIO()
    c   = rl.Canvas(buf, pagesize=pagesize)
    c.saveState()
    c.setFillColor(HexColor(color))
    c.setFillAlpha(alpha)
    c.setFont("Helvetica-Bold", font_size)
    c.translate(pagesize[0]/2, pagesize[1]/2)
    c.rotate(angle)
    c.drawCentredString(0, 0, text)
    c.restoreState()
    c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]

# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_merge(args):
    paths = collect_pdfs(args.input)
    if not paths:
        print("No PDFs found."); sys.exit(1)
    writer = PdfWriter()
    total  = 0
    for p in paths:
        r = PdfReader(str(p))
        writer.append(r)
        total += len(r.pages)
        print(f"  + {p.name}  ({len(r.pages)}p)")
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "wb") as f:
        writer.write(f)
    print(f"\n✓ {len(paths)} files, {total} pages → {out}")

def cmd_split(args):
    reader  = PdfReader(args.input)
    total   = len(reader.pages)
    outdir  = Path(args.output)
    outdir.mkdir(parents=True, exist_ok=True)
    stem    = Path(args.input).stem
    n       = args.every or 1
    chunk   = 0
    for start in range(0, total, n):
        chunk  += 1
        indices = list(range(start, min(start+n, total)))
        label   = f"{start+1}-{indices[-1]+1}"
        w = PdfWriter()
        for i in indices: w.add_page(reader.pages[i])
        out = outdir / f"{stem}_part{chunk:02d}_{label}.pdf"
        with open(out, "wb") as f: w.write(f)
        print(f"  → {out.name}  ({len(indices)}p)")
    print(f"\n✓ {chunk} parts from {total} pages")

def cmd_rotate(args):
    paths  = collect_pdfs(args.input)
    outdir = Path(args.output)
    outdir.mkdir(parents=True, exist_ok=True)
    deg    = args.deg or 90
    for p in paths:
        r = PdfReader(str(p))
        w = PdfWriter()
        for page in r.pages:
            page.rotate(deg)
            w.add_page(page)
        out = outdir / p.name
        with open(out, "wb") as f: w.write(f)
        print(f"  ✓ {p.name} rotated {deg}°")
    print(f"\n✓ {len(paths)} files rotated")

def cmd_watermark(args):
    paths  = collect_pdfs(args.input)
    outdir = Path(args.output)
    outdir.mkdir(parents=True, exist_ok=True)
    text   = args.text or "DRAFT"
    for p in paths:
        r        = PdfReader(str(p))
        pw       = float(r.pages[0].mediabox.width)
        ph       = float(r.pages[0].mediabox.height)
        wm_page  = build_wm_page(text, args.size, args.color, args.alpha, args.angle, (pw,ph))
        w        = PdfWriter()
        for page in r.pages:
            page.merge_page(wm_page)
            w.add_page(page)
        out = outdir / p.name
        with open(out, "wb") as f: w.write(f)
        print(f"  ✓ {p.name}")
    print(f"\n✓ {len(paths)} files watermarked")

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Batch PDF operations")
    sub    = parser.add_subparsers(dest="command", required=True)

    # merge
    p1 = sub.add_parser("merge")
    p1.add_argument("--input",  "-i", required=True)
    p1.add_argument("--output", "-o", required=True)

    # split
    p2 = sub.add_parser("split")
    p2.add_argument("--input",  "-i", required=True)
    p2.add_argument("--output", "-o", required=True)
    p2.add_argument("--every",  "-n", type=int, default=1)

    # rotate
    p3 = sub.add_parser("rotate")
    p3.add_argument("--input",  "-i", required=True)
    p3.add_argument("--output", "-o", required=True)
    p3.add_argument("--deg",         type=int, default=90,
                    choices=[90,180,270])

    # watermark
    p4 = sub.add_parser("watermark")
    p4.add_argument("--input",  "-i", required=True)
    p4.add_argument("--output", "-o", required=True)
    p4.add_argument("--text",         default="DRAFT")
    p4.add_argument("--size",   type=int,   default=60)
    p4.add_argument("--color",        default="#888888")
    p4.add_argument("--alpha",  type=float, default=0.15)
    p4.add_argument("--angle",  type=float, default=45)

    args = parser.parse_args()
    {"merge": cmd_merge, "split": cmd_split,
     "rotate": cmd_rotate, "watermark": cmd_watermark}[args.command](args)

if __name__ == "__main__":
    main()
