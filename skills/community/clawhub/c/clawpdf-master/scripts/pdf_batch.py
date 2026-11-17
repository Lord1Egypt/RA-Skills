#!/usr/bin/env python3
"""ClawPDF Master — Batch-behandling af PDF-mapper (unik feature)."""
import sys
import os
import glob


def extract_all(folder: str, out: str) -> None:
    import pdfplumber
    os.makedirs(out, exist_ok=True)
    for pdf in sorted(glob.glob(os.path.join(folder, "*.pdf"))):
        try:
            with pdfplumber.open(pdf) as p:
                text = "\n".join((pg.extract_text() or "") for pg in p.pages)
            name = os.path.splitext(os.path.basename(pdf))[0]
            with open(os.path.join(out, f"{name}.txt"), "w", encoding="utf-8") as f:
                f.write(text)
            print(f"  ✅ {os.path.basename(pdf)} → {name}.txt")
        except Exception as e:
            print(f"  ⚠️ {os.path.basename(pdf)}: {e}")


def merge_all(folder: str, out: str) -> None:
    from pypdf import PdfWriter, PdfReader
    writer = PdfWriter()
    for pdf in sorted(glob.glob(os.path.join(folder, "*.pdf"))):
        try:
            reader = PdfReader(pdf)
            for page in reader.pages:
                writer.add_page(page)
            print(f"  ✅ {os.path.basename(pdf)} ({len(reader.pages)} sider)")
        except Exception as e:
            print(f"  ⚠️ {os.path.basename(pdf)}: {e}")
    with open(out, "wb") as f:
        writer.write(f)
    print(f"✅ Samlet: {out}")


if __name__ == "__main__":
    if len(sys.argv) < 5 or "--action" not in sys.argv or "--out" not in sys.argv:
        sys.exit("BRUG: python3 pdf_batch.py ./mappe --action extract|merge --out ./resultat")
    folder = sys.argv[1]
    action = sys.argv[sys.argv.index("--action") + 1]
    out = sys.argv[sys.argv.index("--out") + 1]
    if action == "extract":
        extract_all(folder, out)
    elif action == "merge":
        merge_all(folder, out)
    else:
        sys.exit(f"Ukendt action: {action}")
