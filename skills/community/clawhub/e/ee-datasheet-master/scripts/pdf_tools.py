#!/usr/bin/env python3
"""
通用 PDF 工具 - 不包含业务逻辑，只提供数据提取能力
LLM 负责理解和决策，脚本只负责提取可验证信号

Usage:
    python pdf_tools.py info <pdf_path>
    python pdf_tools.py search <pdf_path> <keyword>
    python pdf_tools.py tables <pdf_path> <page_num>
    python pdf_tools.py text <pdf_path> <page_num>
    python pdf_tools.py search_table <pdf_path> <keyword>
    python pdf_tools.py toc <pdf_path>
    python pdf_tools.py page_stats <pdf_path> [page_num]
    python pdf_tools.py page_hints <pdf_path> [page_num] [--patterns <json_file>]
    python pdf_tools.py search_caption <pdf_path> [keyword]
    python pdf_tools.py nearby_text <pdf_path> <page_num> <pattern> [context_lines]
    python pdf_tools.py render_page <pdf_path> <page_num> [dpi] [out_path]
    python pdf_tools.py dump_patterns  # 输出默认 patterns JSON

Patterns JSON format (for --patterns):
    {
        "likely_block_diagram": ["block diagram", "框图"],
        "likely_timing_diagram": ["timing diagram", "时序图"]
    }
"""

from __future__ import annotations

import json
import io
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

import pdfplumber
from contextlib import contextmanager


@contextmanager
def _open_pdf(pdf_path: str | Path):
    """Open a PDF, retrying with an empty password for owner-protected files.

    Accepts str or Path; normalizes to Path internally so backslash paths on
    Windows are handled correctly regardless of how the caller passes the path.

    Many datasheets are encrypted with an empty user password (owner password
    only) to restrict printing/editing. PDF viewers handle this silently;
    pdfplumber raises an exception. We mirror that behaviour by retrying once
    with password="" before giving up.
    """
    path = Path(pdf_path)  # normalize: handles both \\ and / on Windows
    try:
        with pdfplumber.open(path) as pdf:
            yield pdf
    except Exception as exc:
        err = str(exc).lower()
        if any(kw in err for kw in ("encrypt", "password", "pdfpassword")):
            with pdfplumber.open(path, password="") as pdf:
                yield pdf
        else:
            raise


CAPTION_REGEX = re.compile(
    r"^\s*(Figure|Table|图|表)\s*[A-Za-z0-9\u4e00-\u9fff][A-Za-z0-9\u4e00-\u9fff\-\.]*\s*[:\.：]?\s*(.*)$",
    re.IGNORECASE,
)

# Default patterns for figure/page classification
DEFAULT_LIKELY_PATTERNS: dict[str, tuple[str, ...]] = {
    "likely_block_diagram": (
        "functional block diagram",
        "block diagram",
        "框图",
        "功能框图",
    ),
    "likely_application_figure": (
        "typical application",
        "simplified schematic",
        "reference design",
        "典型应用",
        "参考设计",
    ),
    "likely_timing_diagram": (
        "timing diagram",
        "timing requirements",
        "power-up sequence",
        "power-down sequence",
        "sequence",
        "时序图",
    ),
    "likely_curve_page": (
        "typical characteristics",
        "application curves",
        "efficiency",
        "performance curves",
        "特性曲线",
        "效率曲线",
    ),
    "likely_pinout_page": (
        "pin configuration",
        "pin functions",
        "pinout",
        "pin assignment",
        "pin description",
        "引脚配置",
        "引脚定义",
        "引脚功能",
    ),
    "likely_package_page": (
        "package drawing",
        "mechanical drawing",
        "mechanical dimensions",
        "package dimensions",
        "package outline",
        "封装尺寸",
        "封装图",
    ),
    "likely_register_figure": (
        "register",
        "field descriptions",
        "bit field",
        "寄存器",
        "位域",
    ),
}

# Module-level default (can be overridden)
LIKELY_PATTERNS = DEFAULT_LIKELY_PATTERNS


def pdf_info(pdf_path: str) -> dict[str, Any]:
    path = Path(pdf_path)
    if not path.exists():
        return {"error": f"File not found: {pdf_path}"}

    try:
        with _open_pdf(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            sample_pages = [0, min(5, total_pages - 1), min(10, total_pages - 1)]
            sample_text = ""
            for index in sample_pages:
                if index < len(pdf.pages):
                    sample_text += pdf.pages[index].extract_text() or ""

            is_text_based = len(sample_text.strip()) > 200
            return {
                "pages": total_pages,
                "is_text_based": is_text_based,
                "file_size_kb": path.stat().st_size // 1024,
            }
    except Exception as exc:
        return {"error": str(exc)}



def search_text(pdf_path: str, keyword: str, context_lines: int = 2) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    try:
        with _open_pdf(pdf_path) as pdf:
            for page_index, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                lines = text.split("\n")

                for line_index, line in enumerate(lines):
                    if keyword.lower() in line.lower():
                        start = max(0, line_index - context_lines)
                        end = min(len(lines), line_index + context_lines + 1)
                        results.append(
                            {
                                "page": page_index,
                                "line": line.strip(),
                                "context": "\n".join(lines[start:end]),
                            }
                        )
        return results
    except Exception as exc:
        return [{"error": str(exc)}]



def extract_page_tables(pdf_path: str, page_num: int) -> list[Any]:
    try:
        with _open_pdf(pdf_path) as pdf:
            if page_num < 1 or page_num > len(pdf.pages):
                return [{"error": f"Page {page_num} out of range (1-{len(pdf.pages)})"}]

            page = pdf.pages[page_num - 1]
            tables = page.extract_tables()
            cleaned_tables: list[list[list[str]]] = []
            for table in tables:
                if not table:
                    continue
                cleaned_table: list[list[str]] = []
                for row in table:
                    cleaned_row = ["" if cell is None else str(cell).strip() for cell in row]
                    cleaned_table.append(cleaned_row)
                if cleaned_table:
                    cleaned_tables.append(cleaned_table)
            return cleaned_tables if cleaned_tables else []
    except Exception as exc:
        return [{"error": str(exc)}]



def extract_page_text(pdf_path: str, page_num: int) -> str:
    try:
        with _open_pdf(pdf_path) as pdf:
            if page_num < 1 or page_num > len(pdf.pages):
                return f"Error: Page {page_num} out of range (1-{len(pdf.pages)})"
            return pdf.pages[page_num - 1].extract_text() or ""
    except Exception as exc:
        return f"Error: {str(exc)}"



def search_in_tables(pdf_path: str, keyword: str, pages: list[int] | None = None) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    try:
        with _open_pdf(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            search_pages = pages if pages else list(range(1, total_pages + 1))

            for page_num in search_pages:
                if page_num < 1 or page_num > total_pages:
                    continue
                page = pdf.pages[page_num - 1]
                tables = page.extract_tables()
                for table_index, table in enumerate(tables):
                    if not table:
                        continue
                    for row_index, row in enumerate(table):
                        row_text = " ".join(str(cell) if cell else "" for cell in row)
                        if keyword.lower() in row_text.lower():
                            results.append(
                                {
                                    "page": page_num,
                                    "table_index": table_index,
                                    "row_index": row_index,
                                    "row": ["" if cell is None else str(cell).strip() for cell in row],
                                    "full_table": [
                                        ["" if cell is None else str(cell).strip() for cell in table_row]
                                        for table_row in table
                                    ],
                                }
                            )
        return results
    except Exception as exc:
        return [{"error": str(exc)}]



def extract_toc(pdf_path: str) -> list[dict[str, Any]]:
    toc: list[dict[str, Any]] = []

    try:
        with _open_pdf(pdf_path) as pdf:
            for page in pdf.pages[: min(10, len(pdf.pages))]:
                text = page.extract_text() or ""
                if not any(keyword in text.lower() for keyword in ("contents", "目录", "table of contents")):
                    continue
                lines = text.split("\n")
                for line in lines:
                    match = re.search(r"(.+?)\s+[\.·\s]+\s*(\d+)\s*$", line.strip())
                    if not match:
                        continue
                    title = match.group(1).strip()
                    page_num = int(match.group(2))
                    if 0 < page_num <= len(pdf.pages):
                        toc.append({"title": title, "page": page_num})
                if toc:
                    return toc
        return []
    except Exception as exc:
        return [{"error": str(exc)}]



def _extract_words(page: pdfplumber.page.Page) -> list[dict[str, Any]]:
    try:
        return page.extract_words() or []
    except Exception:
        return []



def _compact_text(text: str) -> str:
    return re.sub(r"\s+", "", text.lower())


def _caption_hits(text: str) -> dict[str, int]:
    lowered = text.lower()
    figure_caption_hits = len(re.findall(r"figure\s*[a-z0-9]", lowered))
    table_caption_hits = len(re.findall(r"table\s*[a-z0-9]", lowered))
    return {
        "figure_caption_hits": figure_caption_hits,
        "table_caption_hits": table_caption_hits,
    }



def _page_stats(page: pdfplumber.page.Page, page_num: int) -> dict[str, Any]:
    text = page.extract_text() or ""
    words = _extract_words(page)
    caption_hits = _caption_hits(text)
    try:
        table_count = len(page.extract_tables() or [])
    except Exception:
        table_count = 0

    return {
        "page": page_num,
        "width": page.width,
        "height": page.height,
        "text_len": len(text),
        "word_count": len(words),
        "char_count": len(page.chars),
        "image_count": len(page.images),
        "rect_count": len(page.rects),
        "line_count": len(page.lines),
        "curve_count": len(page.curves),
        "table_count": table_count,
        "has_extractable_text": bool(text.strip()),
        **caption_hits,
    }



def collect_page_stats(pdf_path: str, page_num: int | None = None) -> list[dict[str, Any]]:
    try:
        with _open_pdf(pdf_path) as pdf:
            if page_num is not None:
                if page_num < 1 or page_num > len(pdf.pages):
                    return [{"error": f"Page {page_num} out of range (1-{len(pdf.pages)})"}]
                return [_page_stats(pdf.pages[page_num - 1], page_num)]
            return [_page_stats(page, index) for index, page in enumerate(pdf.pages, start=1)]
    except Exception as exc:
        return [{"error": str(exc)}]



def _add_hint(hints: list[dict[str, Any]], label: str, score: float, reasons: list[str]) -> None:
    if score <= 0:
        return
    hints.append(
        {
            "label": label,
            "score": round(min(score, 0.95), 2),
            "reasons": reasons,
        }
    )



def _build_hints(
    page_text: str,
    stats: dict[str, Any],
    patterns_override: dict[str, tuple[str, ...]] | None = None,
) -> list[dict[str, Any]]:
    """Build heuristic hints for page classification.

    Args:
        page_text: Extracted text from the page
        stats: Page statistics from _page_stats()
        patterns_override: Custom patterns dict, uses DEFAULT_LIKELY_PATTERNS if None

    Returns:
        List of hint dicts with 'label', 'score', and 'reasons' keys
    """
    lowered = page_text.lower()
    compact = _compact_text(page_text)
    hints: list[dict[str, Any]] = []
    vector_primitives = stats["rect_count"] + stats["line_count"] + stats["curve_count"]

    # Use override patterns or fall back to default
    patterns_to_use = patterns_override if patterns_override is not None else LIKELY_PATTERNS

    figure_score = 0.0
    figure_reasons: list[str] = []
    if stats["figure_caption_hits"] > 0:
        figure_score += 0.45
        figure_reasons.append("page text contains Figure caption")
    if vector_primitives > 80:
        figure_score += 0.20
        figure_reasons.append("vector primitives are moderate/high")
    if stats["table_caption_hits"] == 0:
        figure_score += 0.05
        figure_reasons.append("table caption absent")
    if stats["image_count"] > 0 and stats["char_count"] < 400:
        figure_score += 0.10
        figure_reasons.append("raster/image objects present with relatively low text density")
    _add_hint(hints, "likely_figure_page", figure_score, figure_reasons)

    table_score = 0.0
    table_reasons: list[str] = []
    if stats["table_caption_hits"] > 0:
        table_score += 0.40
        table_reasons.append("page text contains Table caption")
    if stats["table_count"] > 0:
        table_score += 0.20
        table_reasons.append("table extraction found tabular structure")
    if stats["rect_count"] > 150 and stats["line_count"] < 20:
        table_score += 0.10
        table_reasons.append("many rectangular cells with relatively few line graphics")
    _add_hint(hints, "likely_table_page", table_score, table_reasons)

    for label, patterns in patterns_to_use.items():
        score = 0.0
        reasons: list[str] = []
        for pattern in patterns:
            compact_pattern = _compact_text(pattern)
            # Use substring matching for both normal and compacted text
            if pattern.lower() in lowered or compact_pattern in compact:
                score += 0.55
                reasons.append(f"caption/title matches '{pattern}'")
        if label in {"likely_curve_page", "likely_timing_diagram", "likely_block_diagram"} and vector_primitives > 40:
            score += 0.10
            reasons.append("page has non-trivial vector graphics")
        _add_hint(hints, label, score, reasons)

    if figure_score > 0.35 and table_score > 0.35:
        _add_hint(hints, "likely_mixed_page", 0.60, ["figure and table cues both present"])

    return hints



def collect_page_hints(
    pdf_path: str,
    page_num: int | None = None,
    patterns_override: dict[str, tuple[str, ...]] | None = None,
) -> list[dict[str, Any]]:
    """Collect heuristic hints for page classification.

    Args:
        pdf_path: Path to the PDF file
        page_num: Specific page number, or None for all pages
        patterns_override: Custom patterns dict, uses DEFAULT_LIKELY_PATTERNS if None

    Returns:
        List of page hint results with signals and heuristic_hints
    """
    try:
        with _open_pdf(pdf_path) as pdf:
            target_pages: list[tuple[int, pdfplumber.page.Page]]
            if page_num is not None:
                if page_num < 1 or page_num > len(pdf.pages):
                    return [{"error": f"Page {page_num} out of range (1-{len(pdf.pages)})"}]
                target_pages = [(page_num, pdf.pages[page_num - 1])]
            else:
                target_pages = list(enumerate(pdf.pages, start=1))

            results: list[dict[str, Any]] = []
            for page_index, page in target_pages:
                stats = _page_stats(page, page_index)
                page_text = page.extract_text() or ""
                results.append(
                    {
                        "page": page_index,
                        "signals": stats,
                        "heuristic_hints": _build_hints(page_text, stats, patterns_override),
                        "warning": "Hints are heuristic only; not final evidence.",
                    }
                )
            return results
    except Exception as exc:
        return [{"error": str(exc)}]



def _extract_captions_from_lines(lines: list[str], page_num: int) -> list[dict[str, Any]]:
    """Extract figure/table captions from text lines.

    Supports both English (Figure, Table) and Chinese (图, 表) captions.
    """
    captions: list[dict[str, Any]] = []
    for line_index, line in enumerate(lines):
        match = CAPTION_REGEX.match(line.strip())
        if not match:
            continue
        caption_type = match.group(1).lower()
        captions.append(
            {
                "page": page_num,
                "caption_type": caption_type,
                "caption": line.strip(),
                "line_index": line_index,
            }
        )
    return captions



def search_captions(pdf_path: str, keyword: str | None = None) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    try:
        with _open_pdf(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                lines = text.split("\n")
                page_captions = _extract_captions_from_lines(lines, page_num)
                for caption_info in page_captions:
                    if keyword:
                        keyword_lower = keyword.lower()
                        caption_lower = caption_info["caption"].lower()
                        if keyword_lower not in caption_lower and _compact_text(keyword) not in _compact_text(caption_info["caption"]):
                            continue
                    results.append(caption_info)
        return results
    except Exception as exc:
        return [{"error": str(exc)}]



def extract_nearby_text(pdf_path: str, page_num: int, pattern: str, context_lines: int = 2) -> list[dict[str, Any]]:
    try:
        with _open_pdf(pdf_path) as pdf:
            if page_num < 1 or page_num > len(pdf.pages):
                return [{"error": f"Page {page_num} out of range (1-{len(pdf.pages)})"}]
            text = pdf.pages[page_num - 1].extract_text() or ""
            lines = text.split("\n")
            results: list[dict[str, Any]] = []
            regex = re.compile(pattern, re.IGNORECASE)
            for line_index, line in enumerate(lines):
                if not regex.search(line):
                    continue
                start = max(0, line_index - context_lines)
                end = min(len(lines), line_index + context_lines + 1)
                results.append(
                    {
                        "page": page_num,
                        "pattern": pattern,
                        "matched_line": line.strip(),
                        "line_index": line_index,
                        "before": lines[start:line_index],
                        "after": lines[line_index + 1 : end],
                    }
                )
            return results
    except Exception as exc:
        return [{"error": str(exc)}]



def render_page(pdf_path: str, page_num: int, dpi: int = 180, out_path: str | None = None) -> dict[str, Any]:
    path = Path(pdf_path)
    if not path.exists():
        return {"error": f"File not found: {pdf_path}"}

    output_path = Path(out_path) if out_path else Path(tempfile.gettempdir()) / f"{path.stem}_page_{page_num}.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Try pymupdf (same MuPDF engine as mutool, no external binary needed)
    try:
        import fitz  # pymupdf
        doc = fitz.open(str(path))
        if doc.is_encrypted:
            doc.authenticate("")  # empty password for owner-protected PDFs
        if page_num < 1 or page_num > len(doc):
            return {"error": f"Page {page_num} out of range (1-{len(doc)})"}
        page = doc[page_num - 1]
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat)
        pix.save(str(output_path))
        return {"page": page_num, "dpi": dpi, "output_path": str(output_path), "renderer": "pymupdf"}
    except ImportError:
        pass
    except Exception as exc:
        return {"error": str(exc), "renderer": "pymupdf"}

    # Fall back to pypdfium2 (PDFium engine, no external binary needed)
    try:
        import pypdfium2 as pdfium
        try:
            pdf = pdfium.PdfDocument(str(path))
        except Exception:
            pdf = pdfium.PdfDocument(str(path), password="")
        if page_num < 1 or page_num > len(pdf):
            return {"error": f"Page {page_num} out of range (1-{len(pdf)})"}
        page = pdf[page_num - 1]
        bitmap = page.render(scale=dpi / 72)
        pil_image = bitmap.to_pil()
        pil_image.save(str(output_path))
        return {"page": page_num, "dpi": dpi, "output_path": str(output_path), "renderer": "pypdfium2"}
    except ImportError:
        pass
    except Exception as exc:
        return {"error": str(exc), "renderer": "pypdfium2"}

    return {"error": "No PDF renderer available. Install pymupdf or pypdfium2."}



def _parse_optional_page(value: str | None) -> int | None:
    if value is None:
        return None
    return int(value)


def _load_patterns_from_file(json_path: str) -> dict[str, tuple[str, ...]] | None:
    """Load custom patterns from a JSON file.

    Args:
        json_path: Path to JSON file with pattern definitions

    Returns:
        Dict mapping labels to tuples of patterns, or None on error
    """
    try:
        path = Path(json_path)
        if not path.exists():
            return None
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        # Convert lists to tuples
        return {k: tuple(v) if isinstance(v, list) else v for k, v in data.items()}
    except (json.JSONDecodeError, OSError):
        return None


def dump_default_patterns() -> dict[str, list[str]]:
    """Return default patterns as JSON-serializable dict (lists instead of tuples)."""
    return {k: list(v) for k, v in DEFAULT_LIKELY_PATTERNS.items()}



def main() -> None:
    # Force UTF-8 stdout so JSON with non-ASCII characters works on Windows,
    # where the default console encoding is often GBK/CP936.
    # sys.stdout.reconfigure() is the clean Python 3.7+ way; the io.TextIOWrapper
    # fallback covers edge cases (e.g. stdout already replaced by a test harness).
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        if hasattr(sys.stdout, "buffer"):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    # Handle commands that don't need PDF path
    if len(sys.argv) >= 2 and sys.argv[1] == "dump_patterns":
        print(json.dumps(dump_default_patterns(), indent=2, ensure_ascii=False))
        return

    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]
    pdf_path = Path(sys.argv[2])  # normalize early: handles \\ vs / on Windows

    # Parse --patterns flag if present
    patterns_override: dict[str, tuple[str, ...]] | None = None
    args = sys.argv[3:]

    if "--patterns" in args:
        patterns_idx = args.index("--patterns")
        if patterns_idx + 1 < len(args):
            patterns_file = args[patterns_idx + 1]
            patterns_override = _load_patterns_from_file(patterns_file)
            if patterns_override is None:
                print(f"Error: Failed to load patterns from {patterns_file}")
                sys.exit(1)
            # Remove --patterns and its argument from args
            args = args[:patterns_idx] + args[patterns_idx + 2 :]

    if command == "info":
        result = pdf_info(pdf_path)
    elif command == "search":
        if not args:
            print("Usage: python pdf_tools.py search <pdf_path> <keyword>")
            sys.exit(1)
        result = search_text(pdf_path, args[0])
    elif command == "tables":
        if not args:
            print("Usage: python pdf_tools.py tables <pdf_path> <page_num>")
            sys.exit(1)
        result = extract_page_tables(pdf_path, int(args[0]))
    elif command == "text":
        if not args:
            print("Usage: python pdf_tools.py text <pdf_path> <page_num>")
            sys.exit(1)
        result = extract_page_text(pdf_path, int(args[0]))
    elif command == "search_table":
        if not args:
            print("Usage: python pdf_tools.py search_table <pdf_path> <keyword>")
            sys.exit(1)
        result = search_in_tables(pdf_path, args[0])
    elif command == "toc":
        result = extract_toc(pdf_path)
    elif command == "page_stats":
        page_num = int(args[0]) if args else None
        result = collect_page_stats(pdf_path, page_num)
    elif command == "page_hints":
        page_num = int(args[0]) if args else None
        result = collect_page_hints(pdf_path, page_num, patterns_override)
    elif command == "search_caption":
        keyword = args[0] if args else None
        result = search_captions(pdf_path, keyword)
    elif command == "nearby_text":
        if len(args) < 2:
            print("Usage: python pdf_tools.py nearby_text <pdf_path> <page_num> <pattern> [context_lines]")
            sys.exit(1)
        context_lines = int(args[2]) if len(args) >= 3 else 2
        result = extract_nearby_text(pdf_path, int(args[0]), args[1], context_lines)
    elif command == "render_page":
        if not args:
            print("Usage: python pdf_tools.py render_page <pdf_path> <page_num> [dpi] [out_path]")
            sys.exit(1)
        dpi = int(args[1]) if len(args) >= 2 else 180
        out_path = args[2] if len(args) >= 3 else None
        result = render_page(pdf_path, int(args[0]), dpi, out_path)
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)

    if isinstance(result, str):
        print(result)
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
