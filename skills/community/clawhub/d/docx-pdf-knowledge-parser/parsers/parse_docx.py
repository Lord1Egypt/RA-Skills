#!/usr/bin/env python3
from pathlib import Path
from docx import Document


def extract_docx_text(path: Path) -> str:
    doc = Document(str(path))
    parts = []
    for p in doc.paragraphs:
        txt = p.text.strip()
        if txt:
            parts.append(txt)
    return '\n'.join(parts)
