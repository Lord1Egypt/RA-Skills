#!/usr/bin/env python3
"""Extract page text and per-page Relativity IDs from produced PDFs.

The script inspects the bottom-right area of each page and extracts numeric ID
candidates. If two numbers appear, it selects the smaller value as requested.
"""

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Sequence


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Extract page text and bottom-right document IDs from Relativity-exported PDFs."
        )
    )
    parser.add_argument(
        "--input",
        action="append",
        required=True,
        help="PDF file or directory. Repeat for multiple inputs.",
    )
    parser.add_argument(
        "--pattern",
        default="*.pdf",
        help="File pattern when an --input value is a directory (default: *.pdf).",
    )
    parser.add_argument(
        "--recurse",
        action="store_true",
        help="Search directories recursively.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output JSON path.",
    )
    parser.add_argument(
        "--corner-width-ratio",
        type=float,
        default=0.35,
        help="Fraction of page width to treat as bottom-right search area.",
    )
    parser.add_argument(
        "--corner-height-ratio",
        type=float,
        default=0.15,
        help="Fraction of page height to treat as bottom-right search area.",
    )
    parser.add_argument(
        "--id-min-digits",
        type=int,
        default=3,
        help="Minimum digit length for numeric ID candidates.",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=0,
        help="Optional page limit per PDF (0 means no limit).",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print output JSON.",
    )
    return parser.parse_args()


def resolve_pdf_files(inputs: Sequence[str], pattern: str, recurse: bool) -> List[Path]:
    files: List[Path] = []
    seen = set()

    for raw in inputs:
        path = Path(raw)

        if path.is_file():
            if path.suffix.lower() != ".pdf":
                raise ValueError(f"Input is not a PDF: {path}")
            resolved = path.resolve()
            if resolved not in seen:
                seen.add(resolved)
                files.append(resolved)
            continue

        if path.is_dir():
            iterator = path.rglob(pattern) if recurse else path.glob(pattern)
            for candidate in iterator:
                if not candidate.is_file() or candidate.suffix.lower() != ".pdf":
                    continue
                resolved = candidate.resolve()
                if resolved not in seen:
                    seen.add(resolved)
                    files.append(resolved)
            continue

        raise FileNotFoundError(f"Input path not found: {path}")

    files.sort()
    return files


def extract_bottom_right_text(page: Any, width_ratio: float, height_ratio: float) -> str:
    width = float(page.width)
    height = float(page.height)

    x0 = max(0.0, width * (1.0 - width_ratio))
    top = max(0.0, height * (1.0 - height_ratio))
    bbox = (x0, top, width, height)

    corner_page = page.crop(bbox)
    text = (corner_page.extract_text() or "").strip()
    if text:
        return text

    words = page.extract_words() or []
    tokens = [
        word.get("text", "")
        for word in words
        if float(word.get("x0", 0.0)) >= x0 and float(word.get("top", 0.0)) >= top
    ]
    return " ".join(token for token in tokens if token).strip()


def extract_numeric_candidates(text: str, min_digits: int) -> List[int]:
    if not text:
        return []

    pattern = re.compile(rf"\d{{{min_digits},}}")
    return [int(match) for match in pattern.findall(text)]


def process_pdf(
    pdf_path: Path,
    pdfplumber_module: Any,
    width_ratio: float,
    height_ratio: float,
    min_digits: int,
    max_pages: int,
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []

    with pdfplumber_module.open(pdf_path) as pdf:
        for index, page in enumerate(pdf.pages, start=1):
            if max_pages > 0 and index > max_pages:
                break

            page_text = (page.extract_text() or "").strip()
            corner_text = extract_bottom_right_text(page, width_ratio, height_ratio)
            candidates = extract_numeric_candidates(corner_text, min_digits)
            selected_document_id = min(candidates) if candidates else None

            rows.append(
                {
                    "pdf_file": str(pdf_path),
                    "pdf_name": pdf_path.name,
                    "page_number": index,
                    "selected_document_id": selected_document_id,
                    "document_id_candidates": candidates,
                    "bottom_right_text": corner_text,
                    "page_text": page_text,
                }
            )

    return rows


def validate_ratios(width_ratio: float, height_ratio: float) -> None:
    if width_ratio <= 0 or width_ratio > 1:
        raise ValueError("--corner-width-ratio must be > 0 and <= 1")
    if height_ratio <= 0 or height_ratio > 1:
        raise ValueError("--corner-height-ratio must be > 0 and <= 1")


def main() -> int:
    args = parse_args()
    validate_ratios(args.corner_width_ratio, args.corner_height_ratio)

    try:
        import pdfplumber  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "Missing dependency: pdfplumber. Install with: python -m pip install --user pdfplumber"
        ) from exc

    pdf_files = resolve_pdf_files(args.input, args.pattern, args.recurse)
    if not pdf_files:
        raise SystemExit("No PDF files found for the provided --input values.")

    pages: List[Dict[str, Any]] = []
    for pdf_file in pdf_files:
        pages.extend(
            process_pdf(
                pdf_file,
                pdfplumber,
                args.corner_width_ratio,
                args.corner_height_ratio,
                args.id_min_digits,
                args.max_pages,
            )
        )

    missing_id_count = sum(1 for row in pages if row["selected_document_id"] is None)

    result = {
        "source_inputs": args.input,
        "pdf_count": len(pdf_files),
        "page_count": len(pages),
        "missing_document_id_pages": missing_id_count,
        "selection_rule": "Select the smaller numeric value when multiple IDs appear in the bottom-right corner.",
        "pages": pages,
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2 if args.pretty else None)

    print(f"Wrote {len(pages)} page records to {output_path}")
    print(f"Pages without detected document ID: {missing_id_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
