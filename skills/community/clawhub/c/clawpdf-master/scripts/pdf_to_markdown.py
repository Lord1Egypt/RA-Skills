#!/usr/bin/env python3
"""ClawPDF Master — PDF → Markdown-konvertering (unik feature)."""
import sys
import re


def pdf_to_markdown(pdf_path: str) -> str:
    try:
        import pdfplumber
    except ImportError:
        sys.exit("FEJL: pip install pdfplumber")

    md_lines = []
    with pdfplumber.open(pdf_path) as pdf:
        for pno, page in enumerate(pdf.pages, 1):
            md_lines.append(f"\n<!-- Side {pno} -->\n")
            # Tables first
            for table in page.extract_tables() or []:
                if not table:
                    continue
                rows = [[(c or "").replace("\n", " ").strip() for c in row] for row in table]
                if not rows:
                    continue
                widths = [max(len(r[i]) for r in rows if i < len(r)) for i in range(len(rows[0]))]
                header = "| " + " | ".join(rows[0]) + " |"
                sep = "|" + "|".join("-" * (w + 2) for w in widths) + "|"
                md_lines.append(header)
                md_lines.append(sep)
                for row in rows[1:]:
                    md_lines.append("| " + " | ".join(row) + " |")
                md_lines.append("")
            # Tekst med layout
            text = page.extract_text() or ""
            for raw in text.splitlines():
                line = raw.rstrip()
                if not line:
                    continue
                if re.match(r"^#{1,6}\s", line) or re.match(r"^[-*]\s", line) or re.match(r"^\d+\.\s", line):
                    md_lines.append(line)
                elif len(line) > 120:
                    md_lines.append(line)
                else:
                    md_lines.append(line)
    return "\n".join(md_lines)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("BRUG: python3 pdf_to_markdown.py input.pdf output.md")
    md = pdf_to_markdown(sys.argv[1])
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ Konverteret: {sys.argv[1]} → {sys.argv[2]} ({len(md)} tegn)")
