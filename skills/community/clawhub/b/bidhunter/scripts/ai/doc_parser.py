#!/usr/bin/env python3
"""
doc_parser.py - Extract plain text from bid documents (BidHunter v2.0, B1).

Supports PDF and DOCX. Uses the best available backend, gracefully degrading:
  1. PyPDF2 (if installed) for PDF
  2. `pdftotext` (poppler CLI, if available) for PDF
  3. python-docx (if installed) for DOCX
  4. last-resort regex stream extraction (PDF) — partial text only

This keeps the skill dependency-free by default; users who want best-in-class
parsing just `pip install PyPDF2 python-docx` (optional).

Usage:
  python3 doc_parser.py <file.pdf|file.docx>   # prints extracted text to stdout
"""
import os
import sys
import re


def extract_pdf(path):
    # 1. PyPDF2
    try:
        import PyPDF2
        r = PyPDF2.PdfReader(path)
        parts = [p.extract_text() or "" for p in r.pages]
        txt = "\n".join(parts)
        if txt.strip():
            return txt, "PyPDF2"
    except Exception:
        pass
    # 2. pdftotext CLI
    try:
        import subprocess
        r = subprocess.run(["pdftotext", "-layout", path, "-"],
                           capture_output=True, text=True, timeout=60)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout, "pdftotext"
    except Exception:
        pass
    # 3. regex fallback (between stream/endstream, decode printable runs)
    try:
        with open(path, "rb") as f:
            data = f.read()
        chunks = re.findall(rb"stream\r?\n(.*?)\r?\nendstream", data, re.S)
        texts = []
        for c in chunks:
            try:
                s = c.decode("utf-8", "ignore")
            except Exception:
                continue
            s = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", " ", s)
            if len(s.strip()) > 20:
                texts.append(s)
        if texts:
            return "\n".join(texts), "regex-fallback"
    except Exception:
        pass
    return "", "none"


def extract_docx(path):
    try:
        import docx
        d = docx.Document(path)
        parts = [p.text for p in d.paragraphs if p.text.strip()]
        # tables
        for t in d.tables:
            for row in t.rows:
                parts.append(" | ".join(c.text for c in row.cells))
        txt = "\n".join(parts)
        if txt.strip():
            return txt, "python-docx"
    except Exception:
        pass
    return "", "none"


def parse(path):
    """Parse a document into plain text. Returns (text, backend_name).

    Backends degrade gracefully. Never raises for content issues — only for
    a missing file. This is the single entry point every other module uses.
    """
    if not os.path.exists(path):
        return "", "missing"
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return extract_pdf(path)
    if ext in (".docx", ".doc"):
        if ext == ".doc":
            return "", "unsupported-doc"
        return extract_docx(path)
    # plain text / markdown / html-as-text
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read(), "text"
    except Exception:
        return "", "none"


def parse_document(path):
    """Backwards-compatible alias returning only the text.

    Added v2.8: compliance_scanner.py imported `parse_document`, which never
    existed, so every PDF/DOCX scan silently degraded to empty text and the
    regex engine reported zero findings. This alias fixes that call site.
    """
    return parse(path)[0]


def segment(text, budget=8000, overlap=300, min_tail=800):
    """Split long tender text into overlapping segments for batch extraction.

    v2.8 — the single most important fix in this file. A 300-page tender runs
    150k~400k characters; the old fixed MAX_CHARS=9000 window fed the model
    only the first ~3% and the rest of the document was never read. Segmentation
    is aware of document structure so a scoring table is not cut in half.

    Returns a list of (segment_index, segment_text) tuples.
    """
    if not text:
        return []
    if len(text) <= budget:
        return [(0, text)]

    # Structural anchors, in priority order. A 2-char prefix match on "第X章"
    # catches 第三章 / 第3章 / 第四章一、 but also 第38条, which is a real risk;
    # we accept it because the segmenter only needs reasonable boundaries.
    anchors = []
    for pat in (r"\n\s*第[0-9一二三四五六七八九十百]+[章篇]\s*",
                r"\n\s*\d+\s*[、．.]\s*\S",
                r"\n\s*附[件表]\s*[一二三四五六七八九十\d]",
                r"\n\s*[一二三四五六七八九十]+\s*[、．]\s*\S"):
        for m in re.finditer(pat, text):
            anchors.append(m.start())
    anchors = sorted(set(anchors))

    segs = []
    start = 0
    idx = 0
    while start < len(text):
        end = min(start + budget, len(text))
        if end < len(text):
            # Prefer to cut at a structural anchor just past the budget
            cand = [a for a in anchors if start + budget * 0.6 < a <= end]
            if cand:
                end = cand[-1]
        elif len(text) - end < min_tail:
            # Tail too small to be its own segment — fold it into this one
            end = len(text)
        piece = text[start:end]
        if piece.strip():
            segs.append((idx, piece))
            idx += 1
        if end >= len(text):
            break
        start = max(start + 1, end - overlap)
    return segs


def coverage(total_chars, budget=8000):
    """Legacy single-window coverage ratio. Kept for the warning path so
    output can honestly state what fraction of the document was seen."""
    if not total_chars:
        return 0.0
    return min(total_chars, budget) / total_chars * 100.0


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 doc_parser.py <file>", file=sys.stderr)
        sys.exit(1)
    txt, backend = parse(sys.argv[1])
    if not txt:
        print(f"[doc_parser] 未能提取文本（backend={backend}）。"
              f"如需更好效果：pip install PyPDF2 python-docx，或安装 poppler 的 pdftotext。",
              file=sys.stderr)
        sys.exit(1)
    print(txt)


if __name__ == "__main__":
    main()
