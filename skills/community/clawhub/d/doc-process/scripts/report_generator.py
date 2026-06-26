#!/usr/bin/env python3
"""
report_generator.py — Format categorised JSON data into a markdown report.

Supported report types:
  bank        Bank statement analysis (from statement_parser.py output)
  expenses    Expense log summary (from expense_logger.py export)

Usage:
  python report_generator.py --file categorized.json --type bank
  python report_generator.py --file categorized.json --type bank --output report.md
  python report_generator.py --file expenses.json --type expenses --output report.md
  python report_generator.py --file categorized.json --type bank --top 15
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils import safe_output_path


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

_CURRENCY_SYMBOLS = {
    "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥", "INR": "₹",
    "KRW": "₩", "CNY": "¥", "CNH": "¥", "RUB": "₽", "TRY": "₺",
    "ILS": "₪", "THB": "฿", "VND": "₫", "NGN": "₦", "UAH": "₴",
    "AED": "د.إ", "SAR": "﷼", "SGD": "S$", "HKD": "HK$", "AUD": "A$",
    "CAD": "CA$", "NZD": "NZ$", "CHF": "Fr", "SEK": "kr", "NOK": "kr",
    "DKK": "kr", "BRL": "R$", "MXN": "MX$", "ZAR": "R",
}


def _sym(currency: str) -> str:
    return _CURRENCY_SYMBOLS.get(currency.upper(), currency + " ") if currency else "$"


def _fmt(value: float | int | str, currency: str = "USD") -> str:
    try:
        sym = _sym(currency)
        return f"{sym}{float(value):,.2f}"
    except (TypeError, ValueError):
        return str(value)


def _pct(part: float, total: float) -> str:
    if total == 0:
        return "—"
    return f"{part / total * 100:.1f}%"


def _bar(value: float, max_value: float, width: int = 20) -> str:
    """Simple text progress bar."""
    if max_value == 0:
        return ""
    filled = round(value / max_value * width)
    return "█" * filled + "░" * (width - filled)


# ---------------------------------------------------------------------------
# Bank statement report
# ---------------------------------------------------------------------------

def _bank_report(data: dict, top_n: int = 10) -> str:
    lines = []
    s = data.get("summary", {})
    meta = data.get("meta", {})
    currency = meta.get("currency", "USD")

    lines.append("## Bank Statement Analysis")
    lines.append("")

    # ── Account Summary ──────────────────────────────────────────────────
    lines.append("### Account Summary")
    lines.append("")
    lines.append("| Field | Value |")
    lines.append("|---|---|")
    period = meta.get("period") or f"{s.get('date_from', '?')} to {s.get('date_to', '?')}"
    lines.append(f"| Period | {period} |")
    lines.append(f"| Currency | {currency} |")
    lines.append(f"| Total Transactions | {s.get('total_transactions', 0)} |")
    lines.append(f"| Total Credits (Income) | {_fmt(s.get('total_credits', 0), currency)} |")
    lines.append(f"| Total Debits (Spend) | {_fmt(abs(s.get('total_debits', 0)), currency)} |")
    net = s.get('net_change', 0)
    net_sign = "+" if net >= 0 else ""
    lines.append(f"| Net Change | {net_sign}{_fmt(net, currency)} |")
    if meta.get("rows_skipped"):
        lines.append(f"| Rows Skipped (unparseable) | {meta['rows_skipped']} |")
    lines.append("")

    # ── Monthly Trend ────────────────────────────────────────────────────
    monthly = data.get("by_month", [])
    if monthly:
        lines.append("### Monthly Trend")
        lines.append("")
        lines.append(f"| Month | Transactions | Credits | Debits | Net |")
        lines.append("|---|---|---|---|---|")
        for m in monthly:
            net_m = m.get("net", 0)
            net_str = f"{'+' if net_m >= 0 else ''}{_fmt(net_m, currency)}"
            lines.append(
                f"| {m['month']} "
                f"| {m['count']} "
                f"| {_fmt(m.get('credits', 0), currency)} "
                f"| {_fmt(m.get('debits', 0), currency)} "
                f"| {net_str} |"
            )
        lines.append("")

    # ── Spending by Category ─────────────────────────────────────────────
    categories = data.get("by_category", [])
    if categories:
        lines.append("### Spending by Category")
        lines.append("")
        grand_total = sum(c.get("total", 0) for c in categories)
        lines.append(f"| Category | Transactions | Total | % of Spend | Bar |")
        lines.append("|---|---|---|---|---|")
        max_cat = max((c.get("total", 0) for c in categories), default=1)
        for c in categories:
            total = c.get("total", 0)
            lines.append(
                f"| {c.get('category', '')} "
                f"| {c.get('transaction_count', 0)} "
                f"| {_fmt(total, currency)} "
                f"| {_pct(total, grand_total)} "
                f"| {_bar(total, max_cat)} |"
            )
        lines.append(f"| **TOTAL** | | **{_fmt(grand_total, currency)}** | 100% | |")
        lines.append("")

    # ── Top Merchants ────────────────────────────────────────────────────
    top_merchants = data.get("top_merchants", [])
    if not top_merchants:
        # Compute from transactions if missing (older JSON format)
        txs = data.get("transactions", [])
        merchant_totals: dict[str, float] = defaultdict(float)
        merchant_counts: dict[str, int] = defaultdict(int)
        for tx in txs:
            if tx.get("amount", 0) < 0:
                merchant_totals[tx["description"]] += abs(tx["amount"])
                merchant_counts[tx["description"]] += 1
        top_merchants = sorted(
            [{"merchant": m, "total": round(v, 2), "count": merchant_counts[m]} for m, v in merchant_totals.items()],
            key=lambda x: -x["total"],
        )[:top_n]

    if top_merchants:
        show = top_merchants[:top_n]
        max_spend = show[0]["total"] if show else 1
        lines.append(f"### Top {len(show)} Merchants by Spend")
        lines.append("")
        lines.append(f"| Merchant | Visits | Total | Bar |")
        lines.append("|---|---|---|---|")
        for m in show:
            lines.append(
                f"| {m['merchant']} "
                f"| {m['count']} "
                f"| {_fmt(m['total'], currency)} "
                f"| {_bar(m['total'], max_spend)} |"
            )
        lines.append("")

    # ── Subscriptions ─────────────────────────────────────────────────────
    subs = data.get("subscriptions", [])
    if subs:
        total_monthly = sum(
            s.get("amount", 0) / (_FREQ_ANNUAL_MULTIPLIER.get(s.get("frequency", "monthly"), 12) / 12)
            for s in subs
        )
        total_annual = sum(s.get("annual_cost", 0) for s in subs)
        lines.append(f"### Subscriptions Detected ({len(subs)})")
        lines.append("")
        lines.append(f"| Service | Frequency | Per Charge | Annual Cost | Seen |")
        lines.append("|---|---|---|---|---|")
        for sub in subs:
            lines.append(
                f"| {sub.get('service', '')} "
                f"| {sub.get('frequency', 'monthly')} "
                f"| {_fmt(sub.get('amount', 0), currency)} "
                f"| {_fmt(sub.get('annual_cost', 0), currency)} "
                f"| {sub.get('occurrences', '?')}× |"
            )
        lines.append(
            f"| **Total** | | | **{_fmt(total_annual, currency)}/yr** | |"
        )
        lines.append("")

    # ── Anomalies ─────────────────────────────────────────────────────────
    anomalies = data.get("anomalies", [])
    if anomalies:
        lines.append(f"### Anomalies & Flags ({len(anomalies)})")
        lines.append("")
        lines.append("| Date | Description | Amount | Issues |")
        lines.append("|---|---|---|---|")
        for a in anomalies:
            issues = a.get("issues") or [a.get("issue", "")]
            issue_str = "; ".join(issues)
            amount_val = a.get("amount", 0)
            lines.append(
                f"| {a.get('date', '')} "
                f"| {a.get('description', '')} "
                f"| {_fmt(amount_val, currency)} "
                f"| {issue_str} |"
            )
        lines.append("")

    # ── Tax Deduction Candidates ──────────────────────────────────────────
    TAX_CATEGORIES = {
        "Technology":              "Likely deductible (business use)",
        "Professional Services":   "Likely deductible",
        "Office & Supplies":       "Likely deductible",
        "Education":               "Likely deductible",
        "Travel":                  "Deductible if work-related",
        "Marketing":               "Likely deductible",
        "Food & Dining":           "50% deductible as business meals",
        "Financial Services":      "May be deductible (bank/investment fees)",
        "Health & Medical":        "May be deductible (self-employed health insurance)",
    }
    tax_candidates = [
        tx for tx in data.get("transactions", [])
        if tx.get("amount", 0) < 0 and tx.get("category") in TAX_CATEGORIES
    ]
    if tax_candidates:
        lines.append("### Potential Tax Deduction Candidates")
        lines.append("")
        lines.append("| Date | Description | Category | Amount | Note |")
        lines.append("|---|---|---|---|---|")
        for tx in tax_candidates:
            cat = tx.get("category", "")
            note = TAX_CATEGORIES.get(cat, "")
            lines.append(
                f"| {tx.get('date', '')} "
                f"| {tx.get('description', '')} "
                f"| {cat} "
                f"| {_fmt(abs(tx.get('amount', 0)), currency)} "
                f"| {note} |"
            )
        tax_total = sum(abs(tx.get("amount", 0)) for tx in tax_candidates)
        lines.append(f"\n**Estimated deductible total: {_fmt(tax_total, currency)}**")
        lines.append("")
        lines.append(
            "_Disclaimer: Confirm deductibility with your accountant. "
            "Rules vary by jurisdiction and business structure._"
        )
        lines.append("")

    return "\n".join(lines)


_FREQ_ANNUAL_MULTIPLIER = {
    "weekly": 52, "bi-weekly": 26, "monthly": 12,
    "bi-monthly": 6, "quarterly": 4, "semi-annual": 2, "annual": 1,
}


# ---------------------------------------------------------------------------
# Expense log report
# ---------------------------------------------------------------------------

def _expenses_report(entries: list[dict], top_n: int = 10) -> str:
    if not entries:
        return "## Expense Report\n\nNo entries found.\n"

    lines = []
    lines.append(f"## Expense Report ({len(entries)} entries)")
    lines.append("")

    # Detect currencies
    currencies = set((e.get("currency", "") or "USD").strip().upper() for e in entries)
    primary_currency = "USD" if "USD" in currencies else (currencies.pop() if len(currencies) == 1 else "")

    # ── Grand total ───────────────────────────────────────────────────────
    grand_total = sum(_safe_amount(e.get("total", "0")) for e in entries)
    lines.append(f"**Grand Total: {_fmt(grand_total, primary_currency)}**")
    lines.append("")

    # ── Category breakdown ─────────────────────────────────────────────────
    by_cat: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        cat = e.get("category", "Unknown") or "Unknown"
        by_cat[cat].append(e)

    cat_totals = {cat: sum(_safe_amount(e.get("total", "0")) for e in items) for cat, items in by_cat.items()}

    lines.append("### Spending by Category")
    lines.append("")
    lines.append(f"| Category | Transactions | Total | % |")
    lines.append("|---|---|---|---|")
    for cat in sorted(cat_totals, key=lambda c: -cat_totals[c]):
        lines.append(
            f"| {cat} "
            f"| {len(by_cat[cat])} "
            f"| {_fmt(cat_totals[cat], primary_currency)} "
            f"| {_pct(cat_totals[cat], grand_total)} |"
        )
    lines.append(f"| **TOTAL** | **{len(entries)}** | **{_fmt(grand_total, primary_currency)}** | 100% |")
    lines.append("")

    # ── Monthly breakdown ──────────────────────────────────────────────────
    by_month: dict[str, float] = defaultdict(float)
    by_month_count: dict[str, int] = defaultdict(int)
    for e in entries:
        month = (e.get("date", "") or "")[:7]
        if month:
            by_month[month] += _safe_amount(e.get("total", "0"))
            by_month_count[month] += 1

    if len(by_month) > 1:
        lines.append("### Monthly Breakdown")
        lines.append("")
        lines.append(f"| Month | Count | Total |")
        lines.append("|---|---|---|")
        for month in sorted(by_month):
            lines.append(
                f"| {month} "
                f"| {by_month_count[month]} "
                f"| {_fmt(by_month[month], primary_currency)} |"
            )
        lines.append("")

    # ── Top merchants ──────────────────────────────────────────────────────
    merchant_totals: dict[str, float] = defaultdict(float)
    merchant_counts: dict[str, int] = defaultdict(int)
    for e in entries:
        m = (e.get("merchant", "") or "").strip()
        if m:
            merchant_totals[m] += _safe_amount(e.get("total", "0"))
            merchant_counts[m] += 1

    top_merchants = sorted(merchant_totals, key=lambda m: -merchant_totals[m])[:top_n]
    if top_merchants:
        max_spend = merchant_totals[top_merchants[0]]
        lines.append(f"### Top {len(top_merchants)} Merchants")
        lines.append("")
        lines.append(f"| Merchant | Visits | Total | Bar |")
        lines.append("|---|---|---|---|")
        for m in top_merchants:
            lines.append(
                f"| {m} "
                f"| {merchant_counts[m]} "
                f"| {_fmt(merchant_totals[m], primary_currency)} "
                f"| {_bar(merchant_totals[m], max_spend)} |"
            )
        lines.append("")

    # ── Per-category detail tables ─────────────────────────────────────────
    lines.append("### Detail by Category")
    lines.append("")
    for cat in sorted(by_cat, key=lambda c: -cat_totals[c]):
        cat_entries = sorted(by_cat[cat], key=lambda e: e.get("date", ""))
        cat_total = cat_totals[cat]
        lines.append(f"#### {cat}  ({_fmt(cat_total, primary_currency)})")
        lines.append("")
        lines.append("| Date | Merchant | Subcategory | Total | Currency |")
        lines.append("|---|---|---|---|---|")
        for e in cat_entries:
            cur = (e.get("currency", "") or primary_currency or "USD").strip()
            lines.append(
                f"| {e.get('date', '')} "
                f"| {e.get('merchant', '')} "
                f"| {e.get('subcategory', '')} "
                f"| {_fmt(_safe_amount(e.get('total', '0')), cur)} "
                f"| {cur} |"
            )
        lines.append(f"\n**Category Total: {_fmt(cat_total, primary_currency)}**")
        lines.append("")

    # ── Multi-currency notice ──────────────────────────────────────────────
    if len(currencies) > 1:
        lines.append("---")
        lines.append("")
        lines.append(
            f"_Note: This report contains entries in multiple currencies "
            f"({', '.join(sorted(currencies))}). "
            "Totals above are not converted — use a single currency for accurate aggregation._"
        )
        lines.append("")

    return "\n".join(lines)


def _safe_amount(val) -> float:
    try:
        from utils import parse_amount
        return parse_amount(str(val))
    except (ValueError, Exception):
        return 0.0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="report_generator",
        description="Format categorised JSON data into a markdown report.",
    )
    parser.add_argument("--file", required=True, help="Path to input JSON file")
    parser.add_argument(
        "--type", required=True, choices=["bank", "expenses"],
        help="Report type",
    )
    parser.add_argument("--output", help="Output .md file (prints to stdout if omitted)")
    parser.add_argument("--top", type=int, default=10, help="Number of top merchants to show (default: 10)")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        json_path = safe_output_path(args.file)
        if not json_path.exists():
            print(f"Error: File not found: {json_path}", file=sys.stderr)
            return 1

        with json_path.open(encoding="utf-8") as f:
            data = json.load(f)

        if args.type == "bank":
            report = _bank_report(data, top_n=args.top)
        else:
            entries = data if isinstance(data, list) else data.get("entries", data)
            if not isinstance(entries, list):
                print("Error: Could not find entries list in JSON.", file=sys.stderr)
                return 1
            report = _expenses_report(entries, top_n=args.top)

        if args.output:
            output_path = safe_output_path(args.output)
            with output_path.open("w", encoding="utf-8") as f:
                f.write(report)
            print(f"Report written to {output_path}")
        else:
            print(report)

        return 0

    except (ValueError, OSError, json.JSONDecodeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
