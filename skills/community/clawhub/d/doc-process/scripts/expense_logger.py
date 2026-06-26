#!/usr/bin/env python3
"""
expense_logger.py — Manage an expense CSV log.

Subcommands:
  add       Add a new expense entry (with duplicate detection)
  list      List entries with optional filters
  summary   Category/monthly/merchant summary
  export    Export entries as JSON
  delete    Delete an entry by line number or match criteria
  edit      Edit specific fields on a given line

Usage examples:
  python expense_logger.py add --date 2024-03-15 --merchant "Starbucks" \\
      --amount 13.12 --category "Food & Dining" --subcategory "Coffee & Cafes" \\
      --file expenses.csv

  python expense_logger.py list --file expenses.csv --from-date 2024-01-01 --category "Travel"
  python expense_logger.py list --file expenses.csv --merchant starbucks --min-amount 5
  python expense_logger.py summary --file expenses.csv --monthly --top 10
  python expense_logger.py export --file expenses.csv --output expenses.json
  python expense_logger.py delete --file expenses.csv --line 3
  python expense_logger.py edit --file expenses.csv --line 3 --amount 15.00 --notes "corrected"
"""

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils import (
    sanitize_csv_value,
    normalise_date,
    parse_amount,
    validate_category,
    safe_output_path,
    auto_categorise,
)

CSV_HEADER = [
    "date", "merchant", "category", "subcategory",
    "subtotal", "tax", "tip", "total", "currency",
    "payment", "receipt_number", "notes",
]

DEFAULT_CURRENCY = "USD"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _load_entries(csv_path: Path) -> list[dict]:
    if not csv_path.exists():
        return []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    # Ensure all CSV_HEADER keys exist (handle files written with different headers)
    for row in rows:
        for key in CSV_HEADER:
            row.setdefault(key, "")
    return rows


def _write_entries(csv_path: Path, entries: list[dict]) -> None:
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADER, extrasaction="ignore")
        writer.writeheader()
        for entry in entries:
            sanitised = {k: sanitize_csv_value(str(entry.get(k, "") or "")) for k in CSV_HEADER}
            writer.writerow(sanitised)


def _append_entry(csv_path: Path, entry: dict) -> None:
    file_exists = csv_path.exists() and csv_path.stat().st_size > 0
    # If file exists but has no header, rewrite cleanly
    if csv_path.exists() and csv_path.stat().st_size > 0:
        try:
            with csv_path.open(newline="", encoding="utf-8") as f:
                first = f.readline()
            if not any(h in first for h in ["date", "merchant", "amount", "total"]):
                # No header detected — prepend one
                existing = _load_entries(csv_path)
                _write_entries(csv_path, existing)
                file_exists = True
        except Exception:
            pass

    with csv_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADER, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()
        sanitised = {k: sanitize_csv_value(str(entry.get(k, "") or "")) for k in CSV_HEADER}
        writer.writerow(sanitised)


def _is_duplicate(entries: list[dict], entry: dict, tolerance_days: int = 1) -> bool:
    """Return True if an entry with same merchant+amount+date(±tolerance) already exists."""
    try:
        new_total = parse_amount(str(entry.get("total", "0") or "0"))
    except ValueError:
        return False

    for e in entries:
        try:
            existing_total = parse_amount(str(e.get("total", "0") or "0"))
        except ValueError:
            continue

        if (
            e.get("merchant", "").lower() == entry.get("merchant", "").lower()
            and abs(existing_total - new_total) < 0.01
            and e.get("date", "") == entry.get("date", "")
        ):
            return True
    return False


def _fmt_row(e: dict, col_widths: dict) -> str:
    merchant = (e.get("merchant", "") or "")[:col_widths["merchant"]]
    category = (e.get("category", "") or "")[:col_widths["category"]]
    total_str = e.get("total", "") or ""
    currency = (e.get("currency", "") or "")[:5]
    return (
        f"{e.get('date', ''):<10}  "
        f"{merchant:<{col_widths['merchant']}}  "
        f"{category:<{col_widths['category']}}  "
        f"{total_str:>9}  "
        f"{currency:<5}"
    )


# ---------------------------------------------------------------------------
# Subcommand: add
# ---------------------------------------------------------------------------

def cmd_add(args: argparse.Namespace) -> int:
    csv_path = safe_output_path(args.file)

    try:
        date = normalise_date(args.date)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    try:
        total = parse_amount(args.amount)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    try:
        subtotal = parse_amount(args.subtotal) if args.subtotal else ""
        tax = parse_amount(args.tax) if args.tax else ""
        tip = parse_amount(args.tip) if args.tip else ""
    except ValueError as e:
        print(f"Error in optional amount field: {e}", file=sys.stderr)
        return 1

    if args.category:
        try:
            category, subcategory = validate_category(args.category, args.subcategory or "")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    else:
        category, subcategory = auto_categorise(args.merchant)
        if args.subcategory:
            subcategory = args.subcategory

    currency = (args.currency or DEFAULT_CURRENCY).upper()
    if len(currency) != 3 or not currency.isalpha():
        print(f"Warning: '{currency}' may not be a valid ISO currency code.", file=sys.stderr)

    entry = {
        "date": date,
        "merchant": args.merchant,
        "category": category,
        "subcategory": subcategory,
        "subtotal": f"{subtotal:.2f}" if subtotal != "" else "",
        "tax": f"{tax:.2f}" if tax != "" else "",
        "tip": f"{tip:.2f}" if tip != "" else "",
        "total": f"{total:.2f}",
        "currency": currency,
        "payment": args.payment or "",
        "receipt_number": args.receipt or "",
        "notes": args.notes or "",
    }

    # Duplicate detection
    if not getattr(args, "force", False):
        existing = _load_entries(csv_path)
        if _is_duplicate(existing, entry):
            print(
                f"Warning: A matching entry already exists "
                f"({date} | {args.merchant} | {total:.2f} {currency}). "
                "Use --force to add anyway.",
                file=sys.stderr,
            )
            return 1

    _append_entry(csv_path, entry)
    print(f"Added: {date} | {args.merchant} | {category} | {total:.2f} {currency}")
    if args.category is None:
        print(f"  (Category auto-detected: {category} / {subcategory})")
    print(f"File:  {csv_path}")
    return 0


# ---------------------------------------------------------------------------
# Subcommand: list
# ---------------------------------------------------------------------------

def cmd_list(args: argparse.Namespace) -> int:
    csv_path = safe_output_path(args.file)
    entries = _load_entries(csv_path)

    if not entries:
        print("No entries found.")
        return 0

    # Filters
    if getattr(args, "category", None):
        entries = [e for e in entries if e.get("category", "").lower() == args.category.lower()]
    if getattr(args, "subcategory", None):
        entries = [e for e in entries if e.get("subcategory", "").lower() == args.subcategory.lower()]
    if getattr(args, "merchant", None):
        term = args.merchant.lower()
        entries = [e for e in entries if term in (e.get("merchant", "") or "").lower()]
    if args.from_date:
        try:
            from_dt = normalise_date(args.from_date)
            entries = [e for e in entries if e.get("date", "") >= from_dt]
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    if args.to_date:
        try:
            to_dt = normalise_date(args.to_date)
            entries = [e for e in entries if e.get("date", "") <= to_dt]
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    if getattr(args, "min_amount", None) is not None:
        try:
            mn = parse_amount(str(args.min_amount))
            entries = [e for e in entries if _safe_amount(e.get("total", "0")) >= mn]
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    if getattr(args, "max_amount", None) is not None:
        try:
            mx = parse_amount(str(args.max_amount))
            entries = [e for e in entries if _safe_amount(e.get("total", "0")) <= mx]
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    if not entries:
        print("No entries match the filter.")
        return 0

    # Sort
    sort_key = getattr(args, "sort", None) or "date"
    reverse = getattr(args, "desc", False)
    if sort_key == "amount":
        entries.sort(key=lambda e: _safe_amount(e.get("total", "0")), reverse=reverse)
    elif sort_key == "merchant":
        entries.sort(key=lambda e: e.get("merchant", "").lower(), reverse=reverse)
    elif sort_key == "category":
        entries.sort(key=lambda e: e.get("category", "").lower(), reverse=reverse)
    else:
        entries.sort(key=lambda e: e.get("date", ""), reverse=reverse)

    col_widths = {"merchant": 28, "category": 20}
    header = (
        f"{'Date':<10}  {'Merchant':<{col_widths['merchant']}}  "
        f"{'Category':<{col_widths['category']}}  {'Total':>9}  {'Cur':<5}"
    )
    print(header)
    print("-" * len(header))
    running_total = 0.0
    for e in entries:
        print(_fmt_row(e, col_widths))
        running_total += _safe_amount(e.get("total", "0"))

    print("-" * len(header))
    print(f"Total entries: {len(entries)}   Grand total: {running_total:.2f}")
    return 0


def _safe_amount(val) -> float:
    try:
        return parse_amount(str(val))
    except ValueError:
        return 0.0


# ---------------------------------------------------------------------------
# Subcommand: summary
# ---------------------------------------------------------------------------

def cmd_summary(args: argparse.Namespace) -> int:
    csv_path = safe_output_path(args.file)
    entries = _load_entries(csv_path)

    if not entries:
        print("No entries found.")
        return 0

    # ── Category breakdown ────────────────────────────────────────────────
    cat_totals: dict[str, float] = {}
    cat_counts: dict[str, int] = {}
    grand_total = 0.0
    errors = 0

    for e in entries:
        cat = e.get("category", "Unknown") or "Unknown"
        try:
            amount = _safe_amount(e.get("total", "0"))
        except ValueError:
            errors += 1
            continue
        cat_totals[cat] = cat_totals.get(cat, 0.0) + amount
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
        grand_total += amount

    print(f"\n{'='*60}")
    print(f"  Expense Summary  ({len(entries)} entries)")
    print(f"{'='*60}")

    print(f"\n{'Category':<30}  {'Count':>5}  {'Total':>10}  {'%':>5}")
    print("-" * 56)
    for cat in sorted(cat_totals, key=lambda c: -cat_totals[c]):
        pct = (cat_totals[cat] / grand_total * 100) if grand_total else 0
        print(f"{cat:<30}  {cat_counts[cat]:>5}  {cat_totals[cat]:>10.2f}  {pct:>4.1f}%")
    print("-" * 56)
    print(f"{'TOTAL':<30}  {len(entries):>5}  {grand_total:>10.2f}  100.0%")

    # ── Currency breakdown ────────────────────────────────────────────────
    currencies: dict[str, float] = {}
    for e in entries:
        cur = (e.get("currency", "") or "").strip().upper() or "?"
        currencies[cur] = currencies.get(cur, 0.0) + _safe_amount(e.get("total", "0"))

    if len(currencies) > 1:
        print(f"\n{'Currency Breakdown':}")
        print("-" * 30)
        for cur, total in sorted(currencies.items(), key=lambda x: -x[1]):
            print(f"  {cur:<5}  {total:>10.2f}")

    # ── Monthly breakdown ─────────────────────────────────────────────────
    if getattr(args, "monthly", False):
        by_month: dict[str, float] = {}
        by_month_count: dict[str, int] = {}
        for e in entries:
            month = (e.get("date", "") or "")[:7]
            if not month:
                continue
            by_month[month] = by_month.get(month, 0.0) + _safe_amount(e.get("total", "0"))
            by_month_count[month] = by_month_count.get(month, 0) + 1

        print(f"\n{'Monthly Breakdown':}")
        print(f"{'Month':<10}  {'Count':>5}  {'Total':>10}")
        print("-" * 30)
        for month in sorted(by_month):
            print(f"{month:<10}  {by_month_count[month]:>5}  {by_month[month]:>10.2f}")

    # ── Top merchants ─────────────────────────────────────────────────────
    top_n = getattr(args, "top", None) or 10
    merchant_totals: dict[str, float] = {}
    merchant_counts: dict[str, int] = {}
    for e in entries:
        m = (e.get("merchant", "") or "").strip()
        if m:
            merchant_totals[m] = merchant_totals.get(m, 0.0) + _safe_amount(e.get("total", "0"))
            merchant_counts[m] = merchant_counts.get(m, 0) + 1

    if merchant_totals:
        top_merchants = sorted(merchant_totals, key=lambda m: -merchant_totals[m])[:top_n]
        print(f"\n{'Top Merchants (by spend)':}")
        print(f"{'Merchant':<30}  {'Count':>5}  {'Total':>10}")
        print("-" * 50)
        for m in top_merchants:
            print(f"{m[:30]:<30}  {merchant_counts[m]:>5}  {merchant_totals[m]:>10.2f}")

    if errors:
        print(f"\nWarning: {errors} entries had unparseable amounts and were skipped.")
    return 0


# ---------------------------------------------------------------------------
# Subcommand: export
# ---------------------------------------------------------------------------

def cmd_export(args: argparse.Namespace) -> int:
    csv_path = safe_output_path(args.file)
    entries = _load_entries(csv_path)

    if not entries:
        print("No entries to export.")
        return 0

    output_path = safe_output_path(args.output)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

    print(f"Exported {len(entries)} entries to {output_path}")
    return 0


# ---------------------------------------------------------------------------
# Subcommand: delete
# ---------------------------------------------------------------------------

def cmd_delete(args: argparse.Namespace) -> int:
    csv_path = safe_output_path(args.file)
    entries = _load_entries(csv_path)

    if not entries:
        print("No entries found.")
        return 0

    if args.line is not None:
        # 1-based line number (not counting header)
        idx = args.line - 1
        if idx < 0 or idx >= len(entries):
            print(f"Error: Line {args.line} is out of range (1–{len(entries)}).", file=sys.stderr)
            return 1
        removed = entries.pop(idx)
        _write_entries(csv_path, entries)
        print(f"Deleted line {args.line}: {removed.get('date')} | {removed.get('merchant')} | {removed.get('total')}")
        return 0

    if args.match:
        # Match on merchant substring (case-insensitive) + optional date
        term = args.match.lower()
        before = len(entries)
        if args.date:
            try:
                match_date = normalise_date(args.date)
            except ValueError as e:
                print(f"Error: {e}", file=sys.stderr)
                return 1
            entries = [
                e for e in entries
                if not (term in (e.get("merchant", "") or "").lower() and e.get("date", "") == match_date)
            ]
        else:
            entries = [e for e in entries if term not in (e.get("merchant", "") or "").lower()]
        removed_count = before - len(entries)
        if removed_count == 0:
            print("No entries matched the criteria.")
            return 0
        _write_entries(csv_path, entries)
        print(f"Deleted {removed_count} entry/entries matching '{args.match}'.")
        return 0

    print("Error: Provide --line or --match.", file=sys.stderr)
    return 1


# ---------------------------------------------------------------------------
# Subcommand: edit
# ---------------------------------------------------------------------------

def cmd_edit(args: argparse.Namespace) -> int:
    csv_path = safe_output_path(args.file)
    entries = _load_entries(csv_path)

    if not entries:
        print("No entries found.")
        return 0

    idx = args.line - 1
    if idx < 0 or idx >= len(entries):
        print(f"Error: Line {args.line} is out of range (1–{len(entries)}).", file=sys.stderr)
        return 1

    entry = entries[idx]
    changed_fields = []

    if args.date:
        try:
            entry["date"] = normalise_date(args.date)
            changed_fields.append("date")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    if args.merchant:
        entry["merchant"] = args.merchant
        changed_fields.append("merchant")

    if args.amount:
        try:
            entry["total"] = f"{parse_amount(args.amount):.2f}"
            changed_fields.append("total")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    if args.category:
        try:
            cat, sub = validate_category(args.category, args.subcategory or entry.get("subcategory", ""))
            entry["category"] = cat
            entry["subcategory"] = sub
            changed_fields.append("category")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    if args.subcategory and "category" not in changed_fields:
        entry["subcategory"] = args.subcategory
        changed_fields.append("subcategory")

    if args.notes is not None:
        entry["notes"] = args.notes
        changed_fields.append("notes")

    if args.currency:
        entry["currency"] = args.currency.upper()
        changed_fields.append("currency")

    if args.payment:
        entry["payment"] = args.payment
        changed_fields.append("payment")

    if not changed_fields:
        print("No fields to update. Provide at least one field flag.")
        return 1

    entries[idx] = entry
    _write_entries(csv_path, entries)
    print(f"Updated line {args.line}: {', '.join(changed_fields)} changed.")
    print(f"  {entry.get('date')} | {entry.get('merchant')} | {entry.get('total')} {entry.get('currency', '')}")
    return 0


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="expense_logger",
        description="Manage an expense CSV log.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # ── add ──────────────────────────────────────────────────────────────
    p_add = sub.add_parser("add", help="Add a new expense entry")
    p_add.add_argument("--date", required=True, help="Transaction date (YYYY-MM-DD or common formats)")
    p_add.add_argument("--merchant", required=True, help="Merchant name")
    p_add.add_argument("--amount", required=True, help="Total charged amount")
    p_add.add_argument("--category", help="Expense category (auto-detected if omitted)")
    p_add.add_argument("--subcategory", help="Expense subcategory")
    p_add.add_argument("--subtotal", help="Pre-tax subtotal")
    p_add.add_argument("--tax", help="Tax amount")
    p_add.add_argument("--tip", help="Tip/gratuity amount")
    p_add.add_argument("--currency", default="USD", help="ISO currency code (default: USD)")
    p_add.add_argument("--payment", help="Payment method (e.g. Visa ••••4521)")
    p_add.add_argument("--receipt", help="Receipt or invoice number")
    p_add.add_argument("--notes", help="Optional notes")
    p_add.add_argument("--file", default="expenses.csv", help="Path to expense CSV")
    p_add.add_argument("--force", action="store_true", help="Skip duplicate detection")

    # ── list ─────────────────────────────────────────────────────────────
    p_list = sub.add_parser("list", help="List expense entries")
    p_list.add_argument("--file", default="expenses.csv")
    p_list.add_argument("--category", help="Filter by category")
    p_list.add_argument("--subcategory", help="Filter by subcategory")
    p_list.add_argument("--merchant", help="Filter by merchant name (substring match)")
    p_list.add_argument("--from-date", dest="from_date", help="From date (inclusive)")
    p_list.add_argument("--to-date", dest="to_date", help="To date (inclusive)")
    p_list.add_argument("--min-amount", dest="min_amount", type=float, help="Minimum total amount")
    p_list.add_argument("--max-amount", dest="max_amount", type=float, help="Maximum total amount")
    p_list.add_argument("--sort", choices=["date", "amount", "merchant", "category"], default="date")
    p_list.add_argument("--desc", action="store_true", help="Sort descending")

    # ── summary ──────────────────────────────────────────────────────────
    p_sum = sub.add_parser("summary", help="Print expense summary")
    p_sum.add_argument("--file", default="expenses.csv")
    p_sum.add_argument("--monthly", action="store_true", help="Include monthly breakdown")
    p_sum.add_argument("--top", type=int, default=10, help="Number of top merchants to show (default: 10)")

    # ── export ───────────────────────────────────────────────────────────
    p_exp = sub.add_parser("export", help="Export entries as JSON")
    p_exp.add_argument("--file", default="expenses.csv")
    p_exp.add_argument("--output", required=True, help="Output JSON file path")

    # ── delete ───────────────────────────────────────────────────────────
    p_del = sub.add_parser("delete", help="Delete an expense entry")
    p_del.add_argument("--file", default="expenses.csv")
    p_del.add_argument("--line", type=int, help="1-based data row number to delete")
    p_del.add_argument("--match", help="Delete rows where merchant contains this string")
    p_del.add_argument("--date", help="Narrow --match to a specific date")

    # ── edit ─────────────────────────────────────────────────────────────
    p_edit = sub.add_parser("edit", help="Edit fields on a specific entry")
    p_edit.add_argument("--file", default="expenses.csv")
    p_edit.add_argument("--line", type=int, required=True, help="1-based data row number to edit")
    p_edit.add_argument("--date", help="New date")
    p_edit.add_argument("--merchant", help="New merchant name")
    p_edit.add_argument("--amount", help="New total amount")
    p_edit.add_argument("--category", help="New category")
    p_edit.add_argument("--subcategory", help="New subcategory")
    p_edit.add_argument("--notes", help="New notes (use empty string to clear)")
    p_edit.add_argument("--currency", help="New currency code")
    p_edit.add_argument("--payment", help="New payment method")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    dispatch = {
        "add": cmd_add,
        "list": cmd_list,
        "summary": cmd_summary,
        "export": cmd_export,
        "delete": cmd_delete,
        "edit": cmd_edit,
    }
    return dispatch[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
