#!/usr/bin/env python3
from pathlib import Path
from pypdf import PdfReader


def extract_pdf_text(path: Path) -> str:
    reader = PdfReader(str(path))
    parts = []
    for page in reader.pages:
        txt = page.extract_text() or ''
        txt = txt.strip()
        if txt:
            parts.append(txt)
    return '\n'.join(parts)
