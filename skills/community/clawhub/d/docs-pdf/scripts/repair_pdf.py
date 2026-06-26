#!/usr/bin/env python3
"""
repair_pdf.py — Attempt to repair a corrupted/damaged PDF file.

Uses qpdf's repair capabilities as the primary method, with pypdf as fallback.

Usage:
    python scripts/repair_pdf.py broken.pdf
    python scripts/repair_pdf.py broken.pdf -o fixed.pdf
    python scripts/repair_pdf.py broken.pdf --force    # try harder (qpdf --replace-input)
    python scripts/repair_pdf.py *.pdf -o ./repaired/  # batch mode
"""
import argparse
import glob
import shutil
import subprocess
import sys
from pathlib import Path


def has_qpdf() -> bool:
    return shutil.which("qpdf") is not None


def check_pdf(path: Path) -> dict:
    """Quick health check on a PDF file."""
    result = {"readable": False, "pages": 0, "errors": []}

    # Try pypdf first
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(path))
        result["pages"] = len(reader.pages)
        result["readable"] = True
    except Exception as e:
        result["errors"].append(f"pypdf: {e}")

    # Try qpdf check
    if has_qpdf():
        try:
            proc = subprocess.run(
                ["qpdf", "--check", str(path)],
                capture_output=True, text=True,
            )
            if proc.returncode == 0:
                result["qpdf_ok"] = True
            else:
                result["qpdf_ok"] = False
                # Extract warnings
                for line in proc.stderr.splitlines():
                    if line.strip() and "WARNING" in line.upper():
                        result["errors"].append(f"qpdf: {line.strip()}")
        except Exception:
            pass

    return result


def repair_with_qpdf(src: Path, dst: Path, force: bool = False) -> bool:
    """Attempt repair using qpdf."""
    try:
        cmd = ["qpdf", str(src), str(dst)]
        if force:
            # More aggressive: attempt to recover even with severe errors
            cmd = ["qpdf", "--qdf", "--object-streams=disable", str(src), str(dst)]

        proc = subprocess.run(cmd, capture_output=True, text=True)

        if proc.returncode in (0, 3):  # 0=ok, 3=warnings but succeeded
            if proc.stderr:
                for line in proc.stderr.splitlines()[:5]:
                    if line.strip():
                        print(f"    qpdf: {line.strip()}")
            return True
        else:
            print(f"    qpdf repair failed (exit {proc.returncode})", file=sys.stderr)
            if proc.stderr:
                for line in proc.stderr.splitlines()[:3]:
                    print(f"      {line.strip()}", file=sys.stderr)
            return False
    except Exception as e:
        print(f"    qpdf error: {e}", file=sys.stderr)
        return False


def repair_with_pypdf(src: Path, dst: Path) -> bool:
    """Attempt repair by re-writing with pypdf (drops damaged objects)."""
    try:
        from pypdf import PdfReader, PdfWriter

        reader = PdfReader(str(src))
        writer = PdfWriter()

        recovered = 0
        for i, page in enumerate(reader.pages):
            try:
                writer.add_page(page)
                recovered += 1
            except Exception as e:
                print(f"    Skipped page {i+1}: {e}", file=sys.stderr)

        if recovered == 0:
            print("    No pages could be recovered.", file=sys.stderr)
            return False

        if reader.metadata:
            try:
                writer.add_metadata(reader.metadata)
            except Exception:
                pass

        with open(dst, "wb") as f:
            writer.write(f)

        print(f"    pypdf recovered {recovered}/{len(reader.pages)} pages")
        return True
    except Exception as e:
        print(f"    pypdf repair failed: {e}", file=sys.stderr)
        return False


def repair_one(src: Path, dst: Path, force: bool) -> bool:
    """Try to repair a single PDF using available methods."""
    print(f"\n  Checking {src.name}...")
    health = check_pdf(src)

    if health["readable"] and health.get("qpdf_ok", True):
        print(f"    ✓ File appears healthy ({health['pages']} pages)")
        # Still copy to output for consistency
        if src != dst:
            shutil.copy2(src, dst)
        return True

    if health["errors"]:
        for err in health["errors"][:3]:
            print(f"    ⚠ {err}")

    # Try qpdf first (better for structural repairs)
    if has_qpdf():
        print(f"    Attempting qpdf repair...")
        if repair_with_qpdf(src, dst, force):
            # Verify result
            result_health = check_pdf(dst)
            if result_health["readable"]:
                print(f"    ✓ Repaired successfully ({result_health['pages']} pages)")
                return True

    # Fallback to pypdf
    print(f"    Attempting pypdf repair (re-write)...")
    if repair_with_pypdf(src, dst):
        result_health = check_pdf(dst)
        if result_health["readable"]:
            print(f"    ✓ Repaired with pypdf ({result_health['pages']} pages)")
            return True

    print(f"    ✗ Could not repair {src.name}", file=sys.stderr)
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Attempt to repair corrupted PDF files"
    )
    parser.add_argument("inputs", nargs="+", help="Input PDF file(s)")
    parser.add_argument("--output", "-o",
                        help="Output file or directory")
    parser.add_argument("--force", action="store_true",
                        help="Try more aggressive repair methods")
    parser.add_argument("--check-only", action="store_true",
                        help="Only check file health, don't repair")
    args = parser.parse_args()

    # Expand globs
    all_inputs = []
    for pattern in args.inputs:
        expanded = glob.glob(pattern)
        if expanded:
            all_inputs.extend(Path(p) for p in expanded if p.endswith(".pdf"))
        else:
            all_inputs.append(Path(pattern))

    if not all_inputs:
        print("No PDF files found.", file=sys.stderr)
        sys.exit(1)

    if not has_qpdf():
        print("⚠ qpdf not installed. Only pypdf repair will be attempted.",
              file=sys.stderr)
        print("  Install: brew install qpdf (macOS) or apt install qpdf (Linux)\n",
              file=sys.stderr)

    batch = len(all_inputs) > 1
    success_count = 0

    for src in all_inputs:
        if not src.exists():
            print(f"  ✗ Not found: {src}", file=sys.stderr)
            continue

        if args.check_only:
            print(f"\n  Checking {src.name}...")
            health = check_pdf(src)
            status = "✓ OK" if (health["readable"] and health.get("qpdf_ok", True)) else "⚠ Issues"
            print(f"    {status}  ({health['pages']} pages)")
            for err in health["errors"]:
                print(f"    {err}")
            continue

        # Determine output path
        if batch:
            outdir = Path(args.output) if args.output else Path(".")
            outdir.mkdir(parents=True, exist_ok=True)
            dst = outdir / src.name
        elif args.output:
            dst = Path(args.output)
        else:
            dst = src.with_stem(src.stem + "_repaired")

        dst.parent.mkdir(parents=True, exist_ok=True)

        if repair_one(src, dst, args.force):
            success_count += 1

    if not args.check_only:
        print(f"\n{'='*40}")
        print(f"✓ {success_count}/{len(all_inputs)} files repaired successfully")


if __name__ == "__main__":
    main()
