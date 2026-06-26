"""CLI entry point for geminipdfocr - OCR PDF processing with Gemini."""

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path

from service import get_ocr_cloud_service
from schemas import OcrResultSchema


def _format_plain_text(results: list[OcrResultSchema]) -> str:
    """Concatenate extracted text from all pages of all documents."""
    parts = []
    for result in results:
        for page in sorted(result.pages, key=lambda p: p.page_number):
            if page.text:
                parts.append(page.text)
    return "\n\n".join(parts)


def _format_json(results: list[OcrResultSchema]) -> str:
    """Output results as JSON."""
    return json.dumps(
        [r.model_dump() for r in results],
        indent=2,
        ensure_ascii=False,
    )


async def _process_pdfs(
    pdf_paths: list[Path],
    max_pages: int | None,
) -> list[OcrResultSchema]:
    """Process multiple PDFs and return results."""
    service = get_ocr_cloud_service()
    results = await service.process_multiple_pdfs(pdf_paths, max_pages)
    return results


def main() -> int:
    """Run the CLI. Returns exit code (0 = success, 1 = failure)."""
    parser = argparse.ArgumentParser(
        description="Extract text from PDFs using Google Gemini OCR.",
        prog="geminipdfocr",
    )
    parser.add_argument(
        "pdf_path",
        type=Path,
        nargs="+",
        help="Path(s) to PDF file(s)",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        metavar="N",
        help="Limit pages per PDF (for testing)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON instead of plain text",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        metavar="FILE",
        help="Write result to file (default: stdout)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress logs",
    )
    args = parser.parse_args()

    if args.quiet:
        logging.basicConfig(level=logging.WARNING)
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    # Validate paths exist
    missing = [p for p in args.pdf_path if not p.exists()]
    if missing:
        for p in missing:
            print(f"Error: File not found: {p}", file=sys.stderr)
        return 1

    try:
        results = asyncio.run(_process_pdfs(args.pdf_path, args.max_pages))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Check overall success
    has_error = any(r.status == "error" for r in results)
    if has_error and all(r.status == "error" for r in results):
        return 1

    # Format output
    if args.json:
        output = _format_json(results)
    else:
        output = _format_plain_text(results)

    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
