#!/usr/bin/env python3
"""Extract text from a PDF file using PyMuPDF."""
import sys
import json
import fitz  # PyMuPDF

def extract(path: str, max_pages: int = 0) -> dict:
    doc = fitz.open(path)
    pages = []
    for i, page in enumerate(doc):
        if max_pages and i >= max_pages:
            break
        text = page.get_text("text")
        pages.append({"page": i + 1, "text": text})
    return {
        "total_pages": len(doc),
        "extracted_pages": len(pages),
        "pages": pages,
    }

if __name__ == "__main__":
    path = sys.argv[1]
    max_p = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    result = extract(path, max_p)
    print(json.dumps(result, ensure_ascii=False))
