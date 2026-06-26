#!/usr/bin/env python3
"""List and render agentic development invoice templates."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_MD = ROOT / "references" / "invoice-catalog.md"
INDEX_JSON = ROOT / "references" / "template-index.json"


def load_index() -> list[dict[str, str]]:
    data = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
    return data["templates"]


def extract_template(template_id: str) -> str:
    text = CATALOG_MD.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"^### {re.escape(template_id)}\n(?P<body>.*?)(?=^### |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        raise KeyError(f"Template not found in invoice-catalog.md: {template_id}")
    return match.group("body").strip()


class SafeDict(dict[str, str]):
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


def parse_vars(raw_vars: list[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in raw_vars:
        if "=" not in raw:
            raise ValueError(f"--var must be key=value, got: {raw}")
        key, value = raw.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"--var key cannot be empty: {raw}")
        values[key] = value
    return values


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="List available invoice template IDs.")
    parser.add_argument("--stage", help="Filter --list by stage.")
    parser.add_argument("--type", dest="invoice_type", help="Filter --list by invoice type.")
    parser.add_argument("--template", help="Template ID to render.")
    parser.add_argument("--var", action="append", default=[], help="Placeholder value as key=value.")
    parser.add_argument("--out", default=None,
                        help="Branded billing PDF output path (default: output/<template>.pdf).")
    parser.add_argument("--markdown-out", default=None, help="Also write the filled Markdown here.")
    parser.add_argument("--png", default=None, help="Optional PNG preview montage path.")
    parser.add_argument("--no-pdf", action="store_true", help="Emit Markdown only; skip PDF.")
    parser.add_argument("--no-cover", action="store_true", help="Skip the PDF cover page.")
    parser.add_argument("--title", default=None, help="PDF title (defaults to the template subject/id).")
    parser.add_argument("--doc-type", default=None, help="Billing PDF doc-type label (defaults to the template type).")
    parser.add_argument("--subtitle", default="", help="Cover subtitle, e.g. \"Prepared for <b>Client</b>\".")
    parser.add_argument("--logo", default=None, help="Logo path (defaults to assets/logo.png).")
    parser.add_argument("--meta", action="append", default=[], help="Cover/letterhead chip as LABEL=VALUE.")
    parser.add_argument("--watermark", default="BILLING DRAFT", help="Watermark text (empty to disable).")
    parser.add_argument("--footer", default="CompleteTech LLC - billing draft only - verify before use", help="Footer text.")
    args = parser.parse_args()

    templates = load_index()
    if args.list:
        for item in templates:
            if args.stage and item["stage"] != args.stage:
                continue
            if args.invoice_type and item["type"] != args.invoice_type:
                continue
            print(f"{item['id']}\t{item['stage']}\t{item['type']}")
        return 0

    if not args.template:
        parser.error("provide --list or --template")

    ids = {item["id"] for item in templates}
    if args.template not in ids:
        print(f"Unknown template: {args.template}", file=sys.stderr)
        return 2

    values = parse_vars(args.var)
    rendered = extract_template(args.template).format_map(SafeDict(values))
    print(rendered)

    if args.no_pdf:
        return 0

    # Branded billing PDF output. One command -> Markdown + PDF.
    from datetime import date
    here = Path(__file__).resolve().parent
    sys.path.insert(0, str(here))
    try:
        from render_pdf import build_pdf, montage
    except ImportError as exc:
        print(f"[skip PDF] {exc}; run 'pip install -r requirements.txt' to enable PDF.", file=sys.stderr)
        return 0

    item = next((t for t in templates if t["id"] == args.template), {})
    meta = []
    for entry in args.meta:
        if "=" in entry:
            k, v = entry.split("=", 1)
            meta.append((k.strip(), v.strip()))
    if not meta:
        meta = [("REFERENCE", args.template.upper()), ("DATE", date.today().isoformat())]
    title = args.title or item.get("subject") or item.get("title") or args.template.replace("-", " ").title()
    template_id = str(item.get("id", args.template))
    template_kind = str(item.get("type", "")).replace("_", " ").upper()
    if args.doc_type is not None:
        doc_type = args.doc_type
    elif "receipt" in template_id:
        doc_type = "PAID-IN-FULL RECEIPT" if "paid-in-full" in template_id else "PAYMENT RECEIPT"
    elif "refund" in template_id:
        doc_type = "REFUND MEMO"
    elif "credit" in template_id:
        doc_type = "CREDIT MEMO"
    elif "void" in template_id:
        doc_type = "VOIDED INVOICE NOTICE"
    elif "memo" in template_id:
        doc_type = template_kind or "BILLING MEMO"
    else:
        doc_type = f"{template_kind} INVOICE".strip() if template_kind else "INVOICE"
    logo = Path(args.logo) if args.logo else (ROOT / "assets" / "logo.png")
    out_pdf = Path(args.out) if args.out else (ROOT / "output" / f"{args.template}.pdf")
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    if args.markdown_out:
        md_out = Path(args.markdown_out)
        md_out.parent.mkdir(parents=True, exist_ok=True)
        md_out.write_text(rendered, encoding="utf-8")
    cfg = {
        "logo": logo if logo.exists() else None,
        "title": title, "eyebrow": "CompleteTech LLC", "doc_type": doc_type,
        "subtitle": args.subtitle, "meta": meta, "doc_id": meta[0][1] if meta else "",
        "watermark": args.watermark, "footer": args.footer,
        "disclaimer": "Billing draft generated from provided facts. Verify client, contract, tax, payment, and approval details before use.",
        "cover": not args.no_cover,
    }
    build_pdf(rendered, cfg, out_pdf)
    print(f"PDF: {out_pdf}", file=sys.stderr)
    if args.png:
        montage(out_pdf, Path(args.png))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
