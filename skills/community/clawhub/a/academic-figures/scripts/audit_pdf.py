#!/usr/bin/env python3
"""PDF text-size auditor: flags text spans below the journal minimum.

Scans every text span in a PDF and reports those under a size threshold
(default 7pt — the safe line for print figures). Mirrors the behaviour of
nature-figure's audit_pdf_text.py: report-only by default, hard-fail with
--fail-below for CI pipelines.

Usage:
  python audit_pdf.py figure.pdf
  python audit_pdf.py figure.pdf --min-size 6 --fail-below
"""
import argparse
import sys

try:
    import fitz
except ImportError:
    print("audit_pdf.py requires PyMuPDF — install with: pip install pymupdf", file=sys.stderr)
    sys.exit(2)

MIN_SIZE = 7.0


def audit(pdf_path, min_size=MIN_SIZE):
    """Return [(page_no, size, text, bbox)] for spans below min_size."""
    offenders = []
    doc = fitz.open(pdf_path)
    try:
        for pno, page in enumerate(doc):
            d = page.get_text("rawdict")
            for block in d["blocks"]:
                if block["type"] != 0:
                    continue
                for line in block.get("lines", []):
                    for span in line["spans"]:
                        txt = "".join(ch["c"] for ch in span.get("chars", [])).strip()
                        if not txt:
                            continue
                        if span["size"] < min_size:
                            offenders.append((pno + 1, round(span["size"], 2), txt[:40],
                                              tuple(round(v, 1) for v in span["bbox"])))
    finally:
        doc.close()
    return offenders


def main():
    ap = argparse.ArgumentParser(description="Audit PDF text sizes against the journal minimum")
    ap.add_argument("pdf", nargs="?", default=None, help="Input PDF (omit with --selftest)")
    ap.add_argument("--min-size", type=float, default=MIN_SIZE,
                    help=f"Minimum font size in pt (default: {MIN_SIZE})")
    ap.add_argument("--fail-below", action="store_true",
                    help="Exit code 1 if any span is below --min-size (CI mode)")
    ap.add_argument("--max-reports", type=int, default=20,
                    help="Max offenders to print (default: 20)")
    # v7.8.0 批次2（B4 尺寸双保险）：页宽 vs 目标栏宽 ±3mm 机械核验——引擎按
    # --journal 预设控尺寸，本参数是交付前独立复核（89=single 183=double 列宽）。
    ap.add_argument("--expect-width", type=float, default=None, metavar="MM",
                    help="Expected page width in mm (89=journal single, 183=double); "
                         "tolerance ±3mm vs actual PDF page width")
    ap.add_argument("--fail-width", action="store_true",
                    help="Exit code 1 on width mismatch (CI mode; default report-only)")
    ap.add_argument("--selftest", action="store_true",
                    help="Run built-in self-test (synthetic PDF, no input needed)")
    args = ap.parse_args()

    if args.selftest:
        import tempfile, os
        ok = True
        with tempfile.TemporaryDirectory() as td:
            fp = os.path.join(td, "t.pdf")
            doc = fitz.open()
            # 89mm=252.28pt；造一页精确 89mm 宽 + 一页 100mm（应判失配）
            for w_mm, expect in ((89.0, True), (100.0, False)):
                page = doc.new_page(width=w_mm / 25.4 * 72, height=120)
                page.insert_text((50, 60), "width probe", fontsize=10)
            doc.save(fp)
            doc.close()
            doc = fitz.open(fp)
            for pno, page in enumerate(doc):
                actual_mm = page.rect.width / 72 * 25.4
                m = abs(actual_mm - 89.0) <= 3.0
                good = (m == (pno == 0))
                ok = ok and good
                print(f"  selftest p{pno}: actual={actual_mm:.2f}mm expect=89.0 "
                      f"match={m} 判定={'PASS' if good else 'FAIL'}")
            doc.close()
        print("audit_pdf --selftest:", "PASS" if ok else "FAIL")
        sys.exit(0 if ok else 1)

    if args.expect_width is not None:
        doc = fitz.open(args.pdf)
        actual_mm = doc[0].rect.width / 72 * 25.4
        doc.close()
        diff = abs(actual_mm - args.expect_width)
        if diff <= 3.0:
            print(f"OK: page width {actual_mm:.2f}mm ≈ expected {args.expect_width:.1f}mm "
                  f"(diff {diff:.2f}mm ≤ 3.0mm)")
        else:
            print(f"WIDTH MISMATCH: page width {actual_mm:.2f}mm vs expected "
                  f"{args.expect_width:.1f}mm（diff {diff:.2f}mm > 3.0mm）——"
                  "检查渲染时是否带 --journal/--column 预设，或导出后被缩放"
                  "（缩放=字号报废，为印刷设计不为屏幕设计）")
            if args.fail_width:
                sys.exit(1)

    offenders = audit(args.pdf, args.min_size)
    if not offenders:
        print(f"OK: no text below {args.min_size}pt in {args.pdf}")
        sys.exit(0)

    print(f"FOUND {len(offenders)} text span(s) below {args.min_size}pt in {args.pdf}:")
    for pno, size, txt, bbox in offenders[: args.max_reports]:
        print(f"  p{pno} {size:5.2f}pt '{txt}' bbox={bbox}")
    if len(offenders) > args.max_reports:
        print(f"  ... and {len(offenders) - args.max_reports} more")
    sys.exit(1 if args.fail_below else 0)


if __name__ == "__main__":
    main()
