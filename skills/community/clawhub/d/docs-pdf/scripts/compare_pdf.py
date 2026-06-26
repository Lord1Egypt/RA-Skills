#!/usr/bin/env python3
"""
compare_pdf.py — Compare two PDF files and report text differences.

Extracts text from each page and generates a diff report (text or HTML).
Useful for contract version comparison, document revision tracking, etc.

Usage:
    python scripts/compare_pdf.py a.pdf b.pdf
    python scripts/compare_pdf.py old.pdf new.pdf -o diff_report.html
    python scripts/compare_pdf.py v1.pdf v2.pdf --format text
    python scripts/compare_pdf.py v1.pdf v2.pdf --pages 1-5
"""
import argparse
import difflib
import html
import sys
from pathlib import Path
import pdfplumber


def extract_pages(pdf_path: Path, page_range: str = None) -> list[tuple[int, str]]:
    """Extract text per page. Returns list of (page_num, text)."""
    pages = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        total = len(pdf.pages)
        if page_range:
            indices = parse_range(page_range, total)
        else:
            indices = list(range(total))

        for i in indices:
            text = pdf.pages[i].extract_text() or ""
            pages.append((i + 1, text))
    return pages


def parse_range(spec: str, total: int) -> list[int]:
    """Parse '1-5,7' → [0,1,2,3,4,6]."""
    indices = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            indices.update(range(int(a) - 1, min(int(b), total)))
        else:
            indices.add(int(part) - 1)
    return sorted(indices)


def generate_text_diff(pages_a: list, pages_b: list,
                       name_a: str, name_b: str) -> str:
    """Generate unified text diff."""
    lines = []
    max_pages = max(len(pages_a), len(pages_b))

    total_added = 0
    total_removed = 0
    total_changed_pages = 0

    for i in range(max_pages):
        text_a = pages_a[i][1].splitlines() if i < len(pages_a) else []
        text_b = pages_b[i][1].splitlines() if i < len(pages_b) else []
        page_num = (pages_a[i][0] if i < len(pages_a)
                    else pages_b[i][0] if i < len(pages_b) else i + 1)

        diff = list(difflib.unified_diff(
            text_a, text_b,
            fromfile=f"{name_a} (page {page_num})",
            tofile=f"{name_b} (page {page_num})",
            lineterm="",
        ))

        if diff:
            total_changed_pages += 1
            for line in diff:
                if line.startswith("+") and not line.startswith("+++"):
                    total_added += 1
                elif line.startswith("-") and not line.startswith("---"):
                    total_removed += 1
            lines.append("\n".join(diff))

    # Summary
    summary = (
        f"{'='*60}\n"
        f"PDF Diff Summary\n"
        f"{'='*60}\n"
        f"  File A:  {name_a}\n"
        f"  File B:  {name_b}\n"
        f"  Pages compared:   {max_pages}\n"
        f"  Pages with diffs: {total_changed_pages}\n"
        f"  Lines added:      +{total_added}\n"
        f"  Lines removed:    -{total_removed}\n"
        f"{'='*60}\n"
    )

    if not lines:
        return summary + "\n✓ No differences found — files are identical in text content.\n"

    return summary + "\n\n".join(lines) + "\n"


def generate_html_diff(pages_a: list, pages_b: list,
                       name_a: str, name_b: str) -> str:
    """Generate an HTML diff report with side-by-side comparison."""
    parts = []
    parts.append("""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>PDF Diff Report</title>
<style>
  body { font-family: -apple-system, system-ui, sans-serif; margin: 20px; background: #f5f5f5; }
  h1 { color: #333; }
  .summary { background: #fff; padding: 15px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
  .page-diff { background: #fff; margin-bottom: 15px; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
  .page-header { background: #e8e8e8; padding: 8px 15px; font-weight: bold; color: #555; }
  .identical { background: #d4edda; padding: 8px 15px; color: #155724; }
  table.diff { width: 100%; border-collapse: collapse; font-family: monospace; font-size: 13px; }
  table.diff td { padding: 2px 8px; vertical-align: top; white-space: pre-wrap; word-break: break-all; }
  table.diff .line-num { width: 40px; text-align: right; color: #999; user-select: none; background: #fafafa; }
  .diff-add { background-color: #e6ffed; }
  .diff-del { background-color: #ffeef0; }
  .diff-chg { background-color: #fff3cd; }
  .stats { display: flex; gap: 20px; margin-top: 10px; }
  .stat { padding: 5px 12px; border-radius: 4px; font-weight: bold; }
  .stat-add { background: #d4edda; color: #155724; }
  .stat-del { background: #f8d7da; color: #721c24; }
  .stat-pages { background: #cce5ff; color: #004085; }
</style></head><body>
""")

    max_pages = max(len(pages_a), len(pages_b))
    total_added = 0
    total_removed = 0
    changed_pages = 0
    page_diffs = []

    for i in range(max_pages):
        text_a = pages_a[i][1].splitlines() if i < len(pages_a) else []
        text_b = pages_b[i][1].splitlines() if i < len(pages_b) else []
        page_num = (pages_a[i][0] if i < len(pages_a)
                    else pages_b[i][0] if i < len(pages_b) else i + 1)

        sm = difflib.SequenceMatcher(None, text_a, text_b)
        opcodes = sm.get_opcodes()
        has_diff = any(op != "equal" for op, *_ in opcodes)

        if has_diff:
            changed_pages += 1

        rows = []
        for op, a1, a2, b1, b2 in opcodes:
            if op == "equal":
                for j in range(a1, a2):
                    rows.append(("", a1 + j + 1, html.escape(text_a[j]),
                                 b1 + (j - a1) + 1, html.escape(text_b[j - a1 + b1])))
            elif op == "delete":
                for j in range(a1, a2):
                    total_removed += 1
                    rows.append(("diff-del", j + 1, html.escape(text_a[j]), "", ""))
            elif op == "insert":
                for j in range(b1, b2):
                    total_added += 1
                    rows.append(("diff-add", "", "", j + 1, html.escape(text_b[j])))
            elif op == "replace":
                max_len = max(a2 - a1, b2 - b1)
                for j in range(max_len):
                    ai = a1 + j if j < (a2 - a1) else None
                    bi = b1 + j if j < (b2 - b1) else None
                    la = html.escape(text_a[ai]) if ai is not None else ""
                    lb = html.escape(text_b[bi]) if bi is not None else ""
                    cls = "diff-chg"
                    if ai is not None and bi is None:
                        cls = "diff-del"
                        total_removed += 1
                    elif ai is None and bi is not None:
                        cls = "diff-add"
                        total_added += 1
                    else:
                        total_added += 1
                        total_removed += 1
                    rows.append((cls,
                                 ai + 1 if ai is not None else "",
                                 la,
                                 bi + 1 if bi is not None else "",
                                 lb))

        page_diffs.append((page_num, has_diff, rows))

    # Summary
    parts.append(f"""
<h1>📄 PDF Diff Report</h1>
<div class="summary">
  <p><strong>File A:</strong> {html.escape(name_a)}</p>
  <p><strong>File B:</strong> {html.escape(name_b)}</p>
  <div class="stats">
    <span class="stat stat-pages">{changed_pages}/{max_pages} pages changed</span>
    <span class="stat stat-add">+{total_added} added</span>
    <span class="stat stat-del">-{total_removed} removed</span>
  </div>
</div>
""")

    # Page diffs
    for page_num, has_diff, rows in page_diffs:
        parts.append(f'<div class="page-diff">')
        parts.append(f'<div class="page-header">Page {page_num}</div>')
        if not has_diff:
            parts.append('<div class="identical">✓ Identical</div>')
        else:
            parts.append('<table class="diff">')
            parts.append(f'<tr><th style="width:40px"></th><th>{html.escape(name_a)}</th>'
                         f'<th style="width:40px"></th><th>{html.escape(name_b)}</th></tr>')
            for cls, ln_a, txt_a, ln_b, txt_b in rows:
                parts.append(
                    f'<tr class="{cls}">'
                    f'<td class="line-num">{ln_a}</td><td>{txt_a}</td>'
                    f'<td class="line-num">{ln_b}</td><td>{txt_b}</td>'
                    f'</tr>'
                )
            parts.append("</table>")
        parts.append("</div>")

    parts.append("</body></html>")
    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(
        description="Compare two PDF files and report text differences"
    )
    parser.add_argument("file_a", help="First PDF (base/old version)")
    parser.add_argument("file_b", help="Second PDF (new version)")
    parser.add_argument("--output", "-o",
                        help="Output file (default: stdout for text, required for HTML)")
    parser.add_argument("--format", "-f",
                        choices=["text", "html"], default=None,
                        help="Output format (auto-detected from -o extension)")
    parser.add_argument("--pages", "-p",
                        help="Page range to compare, e.g. '1-5'")
    args = parser.parse_args()

    path_a = Path(args.file_a)
    path_b = Path(args.file_b)

    for p in (path_a, path_b):
        if not p.exists():
            print(f"File not found: {p}", file=sys.stderr)
            sys.exit(1)

    # Auto-detect format
    fmt = args.format
    if not fmt:
        if args.output and args.output.endswith(".html"):
            fmt = "html"
        else:
            fmt = "text"

    print(f"Comparing: {path_a.name} ↔ {path_b.name}")
    pages_a = extract_pages(path_a, args.pages)
    pages_b = extract_pages(path_b, args.pages)
    print(f"  File A: {len(pages_a)} pages")
    print(f"  File B: {len(pages_b)} pages")

    if fmt == "html":
        report = generate_html_diff(pages_a, pages_b, path_a.name, path_b.name)
    else:
        report = generate_text_diff(pages_a, pages_b, path_a.name, path_b.name)

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
        print(f"\n✓ Diff report saved to {out}")
    else:
        print("\n" + report)


if __name__ == "__main__":
    main()
