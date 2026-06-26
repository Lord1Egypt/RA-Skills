#!/usr/bin/env python3
"""Extract readable text and basic metadata from a PDF file."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PDFINFO_KEYS = {
    "Title": "title",
    "Author": "author",
    "Creator": "creator",
    "Producer": "producer",
    "CreationDate": "created_at",
    "ModDate": "modified_at",
    "Pages": "total_pages",
    "Encrypted": "encrypted",
    "Tagged": "tagged",
    "Page size": "page_size",
    "File size": "file_size",
}


@dataclass
class ExtractionResult:
    metadata: dict[str, Any]
    text: str
    warnings: list[str]
    extraction_method: str


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract readable text and metadata from a PDF file."
    )
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument(
        "--page-start",
        type=int,
        default=1,
        help="First page to extract (1-based)",
    )
    parser.add_argument(
        "--page-end",
        type=int,
        default=None,
        help="Last page to extract (1-based, defaults to the last page)",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=24000,
        help="Maximum number of characters to keep in extracted text",
    )
    parser.add_argument(
        "--output",
        help="Optional JSON output path",
    )
    return parser


def run_command(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        capture_output=True,
        text=True,
        check=False,
    )


def normalize_whitespace(text: str) -> str:
    lines = [line.rstrip() for line in text.replace("\x0c", "\n").splitlines()]
    collapsed: list[str] = []
    previous_blank = False
    for line in lines:
        if not line.strip():
            if not previous_blank:
                collapsed.append("")
            previous_blank = True
            continue
        collapsed.append(re.sub(r"[ \t]+", " ", line).strip())
        previous_blank = False
    return "\n".join(collapsed).strip()


def count_text_units(text: str) -> int:
    tokens = re.findall(r"[A-Za-z0-9_]+|[\u4e00-\u9fff]", text)
    return len(tokens)


def parse_pdfinfo_output(stdout: str) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    for line in stdout.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        mapped_key = PDFINFO_KEYS.get(key.strip())
        if not mapped_key:
            continue
        value = value.strip()
        if mapped_key == "total_pages":
            try:
                metadata[mapped_key] = int(value)
            except ValueError:
                metadata[mapped_key] = value
        else:
            metadata[mapped_key] = value
    return metadata


def extract_with_pdfinfo(pdf_path: Path) -> tuple[dict[str, Any], list[str]]:
    warnings: list[str] = []
    if not shutil.which("pdfinfo"):
        warnings.append("pdfinfo not available; metadata may be incomplete.")
        return {}, warnings

    result = run_command(["pdfinfo", str(pdf_path)])
    if result.returncode != 0:
        warnings.append(
            "pdfinfo failed: "
            + (result.stderr.strip() or result.stdout.strip() or "unknown error")
        )
        return {}, warnings

    return parse_pdfinfo_output(result.stdout), warnings


def extract_with_pdftotext(
    pdf_path: Path,
    page_start: int,
    page_end: int | None,
) -> tuple[str, list[str], str]:
    warnings: list[str] = []
    if not shutil.which("pdftotext"):
        raise RuntimeError("pdftotext is not installed.")

    command = [
        "pdftotext",
        "-enc",
        "UTF-8",
        "-nopgbrk",
        "-f",
        str(page_start),
    ]
    if page_end is not None:
        command.extend(["-l", str(page_end)])
    command.extend([str(pdf_path), "-"])

    result = run_command(command)
    if result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip() or result.stdout.strip() or "pdftotext failed"
        )

    text = normalize_whitespace(result.stdout)
    if not text:
        warnings.append(
            "No readable text extracted. The PDF may be scanned, image-based, or protected."
        )
    return text, warnings, "pdftotext"


def extract_with_mdls(pdf_path: Path) -> tuple[str, list[str], str]:
    warnings: list[str] = []
    if not shutil.which("mdls"):
        raise RuntimeError("mdls is not available.")

    result = run_command(["mdls", "-raw", "-name", "kMDItemTextContent", str(pdf_path)])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "mdls failed")

    stdout = result.stdout.strip()
    if stdout in {"(null)", ""}:
        warnings.append("Spotlight did not return text content for this PDF.")
        return "", warnings, "mdls"

    return normalize_whitespace(stdout), warnings, "mdls"


def extract_pdf(pdf_path: Path, page_start: int, page_end: int | None) -> ExtractionResult:
    metadata, warnings = extract_with_pdfinfo(pdf_path)

    extractors = [
        lambda: extract_with_pdftotext(pdf_path, page_start, page_end),
        lambda: extract_with_mdls(pdf_path),
    ]

    errors: list[str] = []
    for extractor in extractors:
        try:
            text, extractor_warnings, method = extractor()
        except RuntimeError as exc:
            errors.append(str(exc))
            continue
        warnings.extend(extractor_warnings)
        return ExtractionResult(
            metadata=metadata,
            text=text,
            warnings=warnings,
            extraction_method=method,
        )

    combined = "; ".join(error for error in errors if error)
    raise RuntimeError(combined or "No PDF extraction backend succeeded.")


def build_response(
    pdf_path: Path,
    page_start: int,
    page_end: int | None,
    max_chars: int,
) -> dict[str, Any]:
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a .pdf file, got: {pdf_path.name}")
    if page_start < 1:
        raise ValueError("--page-start must be >= 1")
    if page_end is not None and page_end < page_start:
        raise ValueError("--page-end must be >= --page-start")

    result = extract_pdf(pdf_path, page_start, page_end)
    text = result.text
    truncated = len(text) > max_chars
    if truncated:
        text = text[:max_chars].rstrip() + "\n...[truncated]"

    total_pages = result.metadata.get("total_pages")
    extracted_page_end = page_end or total_pages
    word_count = count_text_units(text)
    low_text_pdf = word_count < 120
    warnings = list(result.warnings)
    if low_text_pdf:
        warnings.append(
            "Extracted text is sparse. This PDF may need OCR or a narrower page range."
        )

    response: dict[str, Any] = {
        "status": "ok",
        "source_type": "pdf",
        "file_path": str(pdf_path),
        "file_name": pdf_path.name,
        "title": result.metadata.get("title"),
        "author": result.metadata.get("author"),
        "creator": result.metadata.get("creator"),
        "producer": result.metadata.get("producer"),
        "created_at": result.metadata.get("created_at"),
        "modified_at": result.metadata.get("modified_at"),
        "total_pages": total_pages,
        "page_range": {
            "start": page_start,
            "end": extracted_page_end,
        },
        "text": text,
        "char_count": len(text),
        "word_count": word_count,
        "truncated": truncated,
        "low_text_pdf": low_text_pdf,
        "extraction_method": result.extraction_method,
        "warnings": warnings,
    }
    return response


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    pdf_path = Path(args.pdf_path).expanduser().resolve()

    try:
        response = build_response(
            pdf_path=pdf_path,
            page_start=args.page_start,
            page_end=args.page_end,
            max_chars=args.max_chars,
        )
    except Exception as exc:
        response = {
            "status": "error",
            "source_type": "pdf",
            "file_path": str(pdf_path),
            "message": str(exc),
        }
        text = json.dumps(response, ensure_ascii=False, indent=2)
        if args.output:
            Path(args.output).expanduser().write_text(text + "\n", encoding="utf-8")
        else:
            print(text)
        return 1

    output_text = json.dumps(response, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).expanduser().write_text(output_text + "\n", encoding="utf-8")
    else:
        print(output_text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
