#!/usr/bin/env python3
"""
pdf_parser.py — Extract text from PDFs using pypdf (replaces deprecated PyPDF2)
Usage: python3 pdf_parser.py [papers_dir] [max_papers]
"""

import os
import sys
import json

def parse_pdfs(papers_dir="papers_pdf", max_papers=40):
    # Load metadata if available
    metadata_path = f"{papers_dir}/metadata.json"
    metadata = {}
    if os.path.exists(metadata_path):
        with open(metadata_path) as f:
            for p in json.load(f):
                metadata[p.get("filename", "")] = p

    # Try pypdf first, fallback to PyPDF2
    try:
        from pypdf import PdfReader
    except ImportError:
        try:
            from PyPDF2 import PdfReader
            print("⚠️  Using deprecated PyPDF2. Run: pip install pypdf")
        except ImportError:
            print("❌ No PDF library found. Run: pip install pypdf")
            sys.exit(1)

    pdf_files = [f for f in os.listdir(papers_dir) if f.endswith(".pdf")]
    pdf_files = sorted(pdf_files)[:max_papers]

    if not pdf_files:
        print(f"❌ No PDF files found in {papers_dir}/")
        sys.exit(1)

    print(f"📖 Parsing {len(pdf_files)} PDFs...")

    with open("notes.md", "w") as out:
        out.write("# Research Notes — Extracted from PDFs\n\n")

        for i, pdf_file in enumerate(pdf_files):
            full_path = f"{papers_dir}/{pdf_file}"
            meta = metadata.get(full_path, {})
            title = meta.get("title", pdf_file)
            authors = meta.get("authors", [])
            abstract = meta.get("abstract", "")

            out.write(f"## {i+1}. {title}\n")
            if authors:
                out.write(f"**Authors:** {', '.join(authors[:4])}\n\n")
            if abstract:
                out.write(f"**Abstract:** {abstract[:800]}\n\n")

            # Extract PDF text
            try:
                reader = PdfReader(full_path)
                text = ""
                for page in reader.pages[:4]:  # First 4 pages
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted

                # Clean up text
                text = text.replace("\x00", "").strip()
                if text:
                    out.write(f"**Extracted Content:**\n{text[:1500]}\n\n")
                else:
                    out.write("**Note:** Could not extract text (possibly scanned PDF)\n\n")

            except Exception as e:
                out.write(f"**Error:** Could not parse PDF — {e}\n\n")
                print(f"  ⚠️  [{i+1}] Parse error: {pdf_file}: {e}")
                continue

            out.write("---\n\n")
            print(f"  ✅ [{i+1}/{len(pdf_files)}] {title[:60]}...")

    print(f"\n✅ Parsed {len(pdf_files)} PDFs → notes.md")


if __name__ == "__main__":
    papers_dir = sys.argv[1] if len(sys.argv) > 1 else "papers_pdf"
    max_papers = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    parse_pdfs(papers_dir, max_papers)
