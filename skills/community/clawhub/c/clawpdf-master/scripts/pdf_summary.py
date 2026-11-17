#!/usr/bin/env python3
"""ClawPDF Master — Automatisk dokument-resumé (unik feature)."""
import sys
import re
from collections import Counter


def summarize(pdf_path: str, max_points: int = 8) -> str:
    try:
        import pdfplumber
    except ImportError:
        sys.exit("FEJL: pip install pdfplumber")

    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join((pg.extract_text() or "") for pg in pdf.pages)

    words = re.findall(r"\b\w{4,}\b", text.lower())
    common = Counter(words).most_common(12)
    sentences = re.split(r"(?<=[.!?])\s+", text.replace("\n", " "))
    sentences = [s.strip() for s in sentences if len(s.split()) > 6][:40]

    # Heuristik: vælg sætninger med nøgleord (skal, skal, kontrakt, beløb, dato, ansvar...)
    keys = re.compile(r"(skal|kontrakt|beløb|dato|ansvar|betal|frist|aftale|måned|kr\.|euro|procent|sikkerhed|ret til)", re.I)
    scored = [(len(keys.findall(s)), s) for s in sentences]
    top = [s for _, s in sorted(scored, key=lambda x: -x[0])[:max_points]]

    lines = [f"# Resumé: {pdf_path}", ""]
    lines.append(f"**Sider:** {len(pdf.pages)} · **Ord:** {len(text.split())}")
    lines.append("")
    lines.append("## Nøglepunkter")
    for i, s in enumerate(top, 1):
        lines.append(f"{i}. {s}")
    lines.append("")
    lines.append("## Hyppige begreber")
    lines.append(", ".join(f"**{w}** ({n})" for w, n in common[:8]))
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("BRUG: python3 pdf_summary.py dokument.pdf")
    print(summarize(sys.argv[1]))
