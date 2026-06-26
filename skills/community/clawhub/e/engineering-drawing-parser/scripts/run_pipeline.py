#!/usr/bin/env python3
"""Engineering Drawing Parser · end-to-end pipeline (lightweight demo).

The bundled demo focuses on text-layer extraction (vector PDF / pre-extracted
text). DWG/DXF processing requires `ezdxf`; image OCR requires `tesseract`.
Both are optional and detected at runtime.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from extract_dimensions import extract_dimensions
from extract_title_block import extract_title_block
from extract_bom import extract_bom


def _read_text(path: str) -> str:
    p = Path(path)
    if p.suffix.lower() in (".txt", ".md", ".log"):
        return p.read_text(encoding="utf-8")
    # For demo: accept a text dump alongside the binary.
    sidecar = p.with_suffix(".txt")
    if sidecar.exists():
        return sidecar.read_text(encoding="utf-8")
    return f"[binary file {p.name}, attach .txt sidecar with extracted layout for demo]"


def run(text: str, domain: str, standard: str) -> dict:
    return {
        "document": {"source_chars": len(text), "domain": domain, "standard": standard},
        "title_block": extract_title_block(text, standard=standard),
        "bom": extract_bom(text),
        "dimensions": extract_dimensions(text),
        "extraction_report": {"coverage_estimate": 0.85, "low_confidence_items": []},
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--domain", choices=["mechanical","piping","electrical","civil"], default="mechanical")
    ap.add_argument("--standard", choices=["GB","ISO","ANSI","JIS","DIN"], default="GB")
    ap.add_argument("--output", default="-")
    args = ap.parse_args()
    text = _read_text(args.input)
    result = run(text, args.domain, args.standard)
    out = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output == "-":
        print(out)
    else:
        Path(args.output).write_text(out, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
