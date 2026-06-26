#!/usr/bin/env python3
"""
compress_pdf.py — Compress / optimize a PDF to reduce file size.

Uses qpdf (if available) for linearization and stream optimization,
plus pypdf for removing duplicate objects and compressing streams.

Usage:
    python scripts/compress_pdf.py input.pdf
    python scripts/compress_pdf.py input.pdf -o smaller.pdf
    python scripts/compress_pdf.py input.pdf --quality low       # aggressive
    python scripts/compress_pdf.py input.pdf --quality medium    # balanced (default)
    python scripts/compress_pdf.py input.pdf --quality high      # minimal compression
    python scripts/compress_pdf.py *.pdf -o ./compressed/        # batch mode
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from pypdf import PdfReader, PdfWriter


QUALITY_PRESETS = {
    "low":    {"remove_duplication": True, "remove_images": False, "reduce_image_quality": True},
    "medium": {"remove_duplication": True, "remove_images": False, "reduce_image_quality": False},
    "high":   {"remove_duplication": False, "remove_images": False, "reduce_image_quality": False},
}


def human_size(nbytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if abs(nbytes) < 1024:
            return f"{nbytes:.1f} {unit}"
        nbytes /= 1024
    return f"{nbytes:.1f} TB"


def has_qpdf() -> bool:
    return shutil.which("qpdf") is not None


def qpdf_optimize(src: Path, dst: Path) -> bool:
    """Use qpdf to linearize and optimize object streams."""
    try:
        subprocess.run(
            ["qpdf", "--linearize",
             "--object-streams=generate",
             "--compress-streams=y",
             "--recompress-flate",
             str(src), str(dst)],
            check=True, capture_output=True, text=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def pypdf_compress(src: Path, dst: Path, quality: str) -> None:
    """Use pypdf to compress by removing duplicates and compressing pages."""
    preset = QUALITY_PRESETS[quality]
    reader = PdfReader(str(src))
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # Copy metadata
    if reader.metadata:
        writer.add_metadata(reader.metadata)

    if preset["remove_duplication"]:
        writer.compress_identical_objects(
            remove_identicals=True,
            remove_orphans=True,
        )

    for page in writer.pages:
        page.compress_content_streams()

    with open(dst, "wb") as f:
        writer.write(f)


def compress_one(src: Path, dst: Path, quality: str) -> dict:
    """Compress a single PDF, return stats."""
    original_size = src.stat().st_size

    # Strategy: try qpdf first for linearization, then pypdf for object compression
    tmpdir = tempfile.mkdtemp()
    try:
        intermediate = Path(tmpdir) / "qpdf_out.pdf"

        if has_qpdf() and quality != "high":
            if qpdf_optimize(src, intermediate):
                pypdf_compress(intermediate, dst, quality)
            else:
                pypdf_compress(src, dst, quality)
        else:
            pypdf_compress(src, dst, quality)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    compressed_size = dst.stat().st_size
    saved = original_size - compressed_size
    ratio = (saved / original_size * 100) if original_size > 0 else 0

    return {
        "original": original_size,
        "compressed": compressed_size,
        "saved": saved,
        "ratio": ratio,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Compress / optimize PDF files to reduce size"
    )
    parser.add_argument("inputs", nargs="+", help="Input PDF file(s)")
    parser.add_argument("--output", "-o", help="Output file or directory")
    parser.add_argument(
        "--quality", "-q",
        choices=["low", "medium", "high"],
        default="medium",
        help="Compression quality: low (aggressive), medium (balanced), high (minimal)"
    )
    args = parser.parse_args()

    inputs = []
    for pattern in args.inputs:
        from glob import glob
        expanded = glob(pattern)
        if expanded:
            inputs.extend(Path(p) for p in expanded if p.endswith(".pdf"))
        else:
            inputs.append(Path(pattern))

    if not inputs:
        print("No PDF files found.", file=sys.stderr)
        sys.exit(1)

    batch = len(inputs) > 1

    # Determine output
    if batch:
        outdir = Path(args.output) if args.output else Path(".")
        outdir.mkdir(parents=True, exist_ok=True)
    else:
        if args.output and Path(args.output).suffix == "":
            outdir = Path(args.output)
            outdir.mkdir(parents=True, exist_ok=True)
        else:
            outdir = None

    total_original = 0
    total_compressed = 0

    for src in inputs:
        if not src.exists():
            print(f"  ✗ Not found: {src}", file=sys.stderr)
            continue

        if batch or outdir:
            out_path = (outdir or Path(".")) / src.name
        elif args.output:
            out_path = Path(args.output)
        else:
            out_path = src.with_stem(src.stem + "_compressed")

        out_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"  Compressing {src.name} (quality={args.quality})...")
        try:
            stats = compress_one(src, out_path, args.quality)
            total_original += stats["original"]
            total_compressed += stats["compressed"]
            print(
                f"    {human_size(stats['original'])} → {human_size(stats['compressed'])}"
                f"  (saved {human_size(stats['saved'])}, {stats['ratio']:.1f}%)"
                f"  → {out_path}"
            )
        except Exception as e:
            print(f"  ✗ Failed: {e}", file=sys.stderr)

    if batch:
        total_saved = total_original - total_compressed
        ratio = (total_saved / total_original * 100) if total_original > 0 else 0
        print(f"\n✓ {len(inputs)} files: {human_size(total_original)} → {human_size(total_compressed)} (saved {ratio:.1f}%)")
    else:
        print("✓ Done")


if __name__ == "__main__":
    main()
