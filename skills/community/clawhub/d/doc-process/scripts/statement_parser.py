#!/usr/bin/env python3
"""
statement_parser.py — Parse a bank/credit card CSV export and categorise transactions.

Supports:
  - date, description, amount
  - date, description, debit, credit
  - date, description, amount, balance
  - Files with metadata preamble rows (common in bank exports)
  - Comma, tab, semicolon, pipe delimiters
  - UTF-8, UTF-8-BOM, Latin-1, CP1252 encodings
  - European and US number formats

Usage:
  python statement_parser.py --file statement.csv --output categorized.json
  python statement_parser.py --file statement.csv --output categorized.json --period "Jan 2024"
  python statement_parser.py --file statement.csv --output categorized.json --no-detect-subs
"""

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils import (
    normalise_date,
    parse_amount,
    safe_output_path,
    auto_categorise,
    detect_currency,
)


# ---------------------------------------------------------------------------
# Encoding detection
# ---------------------------------------------------------------------------

def _open_with_fallback(path: Path):
    """Try common encodings in order; return (file_object, encoding_used)."""
    for enc in ("utf-8-sig", "utf-8", "latin-1", "cp1252"):
        try:
            f = path.open(newline="", encoding=enc)
            f.read(512)
            f.seek(0)
            return f, enc
        except (UnicodeDecodeError, Exception):
            try:
                f.close()
            except Exception:
                pass
    raise ValueError(f"Could not decode file '{path}' with any supported encoding.")


# ---------------------------------------------------------------------------
# Preamble skip
# ---------------------------------------------------------------------------

# Header-like keywords that suggest a row is the column header row
_HEADER_KEYWORDS = {
    "date", "description", "amount", "debit", "credit", "balance",
    "memo", "narrative", "payee", "merchant", "particulars", "details",
    "withdrawal", "deposit", "transaction", "type", "reference",
}


def _looks_like_header(row: list[str]) -> bool:
    """Return True if ≥2 cells match known header keywords."""
    hits = sum(
        1 for cell in row
        if re.sub(r"[^a-z]", "", cell.lower().strip()) in _HEADER_KEYWORDS
        or any(kw in cell.lower() for kw in _HEADER_KEYWORDS)
    )
    return hits >= 2


def _skip_preamble(lines: list[str], delimiter: str) -> int:
    """
    Scan lines for the actual CSV header row.
    Returns the 0-based index of the header line.
    Handles bank exports that prepend account metadata.
    """
    for i, line in enumerate(lines[:30]):  # only scan first 30 lines
        if not line.strip():
            continue
        try:
            row = next(csv.reader([line], delimiter=delimiter))
        except Exception:
            continue
        if _looks_like_header(row):
            return i
    return 0  # fallback: assume first line is header


# ---------------------------------------------------------------------------
# CSV format detection
# ---------------------------------------------------------------------------

def _normalise_header(h: str) -> str:
    return re.sub(r"[^a-z0-9]", "", h.lower().strip())


def _detect_columns(headers: list[str]) -> dict[str, str]:
    """
    Map raw header names to logical roles: date, description, amount, debit, credit, balance.
    Returns dict: role → original_header_name.
    """
    mapping: dict[str, str] = {}
    norm = {_normalise_header(h): h for h in headers}

    # Date
    for key in ["date", "transactiondate", "valuedate", "posteddate", "txdate",
                "settledate", "settlementdate", "trxdate", "bookdate", "bookingdate",
                "datetransaction", "processingdate", "entrydate", "datum", "fecha",
                "data", "датаоперации"]:
        if key in norm:
            mapping["date"] = norm[key]
            break

    # Description
    for key in ["description", "memo", "narrative", "details", "payee", "merchant",
                "particulars", "transactiondescription", "transactiondetails",
                "remarks", "reference", "narration", "label", "transaction",
                "merchantname", "beneficiaryname", "name", "counterpart",
                "tradingname", "descriptiondetails"]:
        if key in norm:
            mapping["description"] = norm[key]
            break

    # Amount (single column)
    for key in ["amount", "transactionamount", "value", "net", "netamount",
                "transactionvalue", "amt", "sum", "total", "txnamount"]:
        if key in norm:
            mapping["amount"] = norm[key]
            break

    # Debit
    for key in ["debit", "withdrawal", "debitamount", "dr", "moneyout",
                "charged", "spend", "debet", "ausgaben", "debe"]:
        if key in norm:
            mapping["debit"] = norm[key]
            break

    # Credit
    for key in ["credit", "deposit", "creditamount", "cr", "moneyin",
                "received", "income", "credit", "habere", "ingresos"]:
        if key in norm:
            mapping["credit"] = norm[key]
            break

    # Balance
    for key in ["balance", "runningbalance", "closingbalance", "ledgerbalance",
                "availablebalance", "currentbalance", "accountbalance",
                "closingbal", "saldo"]:
        if key in norm:
            mapping["balance"] = norm[key]
            break

    # Currency (optional)
    for key in ["currency", "currencycode", "ccy", "cur"]:
        if key in norm:
            mapping["currency"] = norm[key]
            break

    return mapping


# ---------------------------------------------------------------------------
# Transaction parsing
# ---------------------------------------------------------------------------

def _parse_row(row: dict, col_map: dict[str, str], row_num: int) -> dict | None:
    """Parse a single CSV row into a transaction dict. Returns None on failure."""
    # Skip completely empty rows
    if not any(v.strip() for v in row.values() if v):
        return None

    # Date
    date_col = col_map.get("date")
    if not date_col:
        return None
    raw_date = (row.get(date_col) or "").strip()
    if not raw_date:
        return None
    try:
        date = normalise_date(raw_date)
    except ValueError:
        return None  # unparseable date: skip silently

    # Description
    desc_col = col_map.get("description")
    description = (row.get(desc_col) or "").strip() if desc_col else f"Row {row_num}"
    if not description:
        description = f"Row {row_num}"

    # Amount
    amount: float
    if "amount" in col_map:
        raw = (row.get(col_map["amount"]) or "").strip()
        if not raw:
            return None
        try:
            amount = parse_amount(raw)
        except ValueError:
            return None

    elif "debit" in col_map or "credit" in col_map:
        debit_str = (row.get(col_map.get("debit", ""), "") or "").strip() if "debit" in col_map else ""
        credit_str = (row.get(col_map.get("credit", ""), "") or "").strip() if "credit" in col_map else ""
        try:
            debit = parse_amount(debit_str) if debit_str else 0.0
            credit = parse_amount(credit_str) if credit_str else 0.0
        except ValueError:
            return None
        amount = credit - debit  # debits are outflows → negative net
    else:
        return None

    # Skip zero-amount rows (header artefacts, subtotals)
    if amount == 0.0:
        return None

    # Balance (optional)
    balance: float | None = None
    if "balance" in col_map:
        bal_raw = (row.get(col_map["balance"]) or "").strip()
        try:
            balance = parse_amount(bal_raw) if bal_raw else None
        except ValueError:
            balance = None

    # Currency (optional, per-row)
    currency: str | None = None
    if "currency" in col_map:
        currency = (row.get(col_map["currency"]) or "").strip().upper() or None

    category, subcategory = auto_categorise(description)

    result = {
        "date": date,
        "description": description,
        "amount": round(amount, 2),
        "category": category,
        "subcategory": subcategory,
    }
    if balance is not None:
        result["balance"] = round(balance, 2)
    if currency:
        result["currency"] = currency

    return result


# ---------------------------------------------------------------------------
# Subscription detection
# ---------------------------------------------------------------------------

def _date_to_ordinal(date_str: str) -> int:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").toordinal()
    except ValueError:
        return 0


def _infer_frequency(dates: list[str]) -> str:
    if len(dates) < 2:
        return "monthly"
    ordinals = sorted(_date_to_ordinal(d) for d in dates if d)
    if len(ordinals) < 2:
        return "monthly"
    gaps = [ordinals[i + 1] - ordinals[i] for i in range(len(ordinals) - 1)]
    median_gap = sorted(gaps)[len(gaps) // 2]
    if median_gap <= 8:
        return "weekly"
    if median_gap <= 16:
        return "bi-weekly"
    if median_gap <= 35:
        return "monthly"
    if median_gap <= 65:
        return "bi-monthly"
    if median_gap <= 100:
        return "quarterly"
    if median_gap <= 200:
        return "semi-annual"
    return "annual"


_FREQ_ANNUAL_MULTIPLIER = {
    "weekly": 52, "bi-weekly": 26, "monthly": 12,
    "bi-monthly": 6, "quarterly": 4, "semi-annual": 2, "annual": 1,
}


def _detect_subscriptions(transactions: list[dict]) -> list[dict]:
    """
    Identify recurring charges by grouping similar descriptions + amounts
    across multiple time periods.
    """
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for tx in transactions:
        if tx["amount"] >= 0:
            continue  # only expenses
        # Normalise description: strip digits, extra spaces
        key_desc = re.sub(r"\d+", "", tx["description"].lower())
        key_desc = re.sub(r"\s+", " ", key_desc).strip()
        # Bucket amount to nearest cent to handle minor rounding variance
        key_amount = round(abs(tx["amount"]), 0)
        groups[(key_desc, key_amount)].append(tx)

    subscriptions = []
    for (desc_key, amount_bucket), txs in groups.items():
        if len(txs) < 2:
            continue

        dates = [tx["date"] for tx in txs]
        months = set(d[:7] for d in dates)

        # Require at least 2 different calendar months
        months = set(d[:7] for d in dates)
        if len(months) < 2:
            continue

        ordinals = sorted(_date_to_ordinal(d) for d in dates)
        if len(ordinals) < 2:
            continue

        frequency = _infer_frequency(dates)
        multiplier = _FREQ_ANNUAL_MULTIPLIER.get(frequency, 12)

        # Use most common actual description
        descriptions = [tx["description"] for tx in txs]
        service_name = max(set(descriptions), key=descriptions.count)

        # Use median amount (more robust than first occurrence)
        amounts = sorted(abs(tx["amount"]) for tx in txs)
        median_amount = amounts[len(amounts) // 2]

        subscriptions.append({
            "service": service_name,
            "amount": round(median_amount, 2),
            "frequency": frequency,
            "annual_cost": round(median_amount * multiplier, 2),
            "occurrences": len(txs),
            "months_seen": len(months),
            "last_charge": max(dates),
        })

    return sorted(subscriptions, key=lambda s: -s["annual_cost"])


# ---------------------------------------------------------------------------
# Anomaly detection
# ---------------------------------------------------------------------------

def _detect_anomalies(transactions: list[dict]) -> list[dict]:
    """Flag statistically and contextually unusual transactions."""
    if not transactions:
        return []

    expense_txs = [tx for tx in transactions if tx["amount"] < 0]
    if not expense_txs:
        return []

    amounts = [abs(tx["amount"]) for tx in expense_txs]
    mean_amount = sum(amounts) / len(amounts)
    threshold_large = mean_amount * 3

    anomalies = []
    seen: list[dict] = []

    # Build a lookup for refund detection: description → list of expense amounts
    desc_expense_map: dict[str, list[float]] = defaultdict(list)
    for tx in expense_txs:
        desc_expense_map[tx["description"].lower()].append(abs(tx["amount"]))

    for tx in transactions:
        abs_amount = abs(tx["amount"])
        issues = []

        # 1. Unusually large expense
        if tx["amount"] < 0 and abs_amount > threshold_large and abs_amount > 50:
            issues.append(
                f"Large charge: {abs_amount:.2f} is >{threshold_large:.0f} "
                f"(3× avg {mean_amount:.2f})"
            )

        # 2. Duplicate charge: same description + amount within 7 days
        if tx["amount"] < 0:
            for prev in seen:
                if (
                    prev["amount"] < 0
                    and prev["description"].lower() == tx["description"].lower()
                    and abs(abs(prev["amount"]) - abs_amount) < 0.02
                ):
                    diff = abs(_date_to_ordinal(tx["date"]) - _date_to_ordinal(prev["date"]))
                    if 0 < diff <= 7:
                        issues.append(
                            f"Possible duplicate charge (same amount within {diff} day(s))"
                        )
                        break

        # 3. Micro / test charge (< $2.00 excluding coffee/transit)
        if (
            tx["amount"] < 0
            and 0 < abs_amount < 2.0
            and tx["category"] not in ("Food & Dining", "Travel")
        ):
            issues.append(
                f"Micro charge ({abs_amount:.2f}) — possible card verification or error"
            )

        # 4. Exact round number (potential ATM, gift card, or manual entry)
        if (
            tx["amount"] < 0
            and abs_amount >= 50
            and abs_amount == int(abs_amount)
            and abs_amount % 50 == 0
        ):
            issues.append(
                f"Round-number charge ({abs_amount:.0f}) — possible cash withdrawal or gift card"
            )

        # 5. Multiple charges from same merchant on same day
        if tx["amount"] < 0:
            same_day_same_merchant = [
                s for s in seen
                if s["date"] == tx["date"]
                and s["description"].lower() == tx["description"].lower()
                and s["amount"] < 0
            ]
            if len(same_day_same_merchant) >= 2:
                issues.append(
                    f"3+ charges from '{tx['description']}' on {tx['date']} — review for errors"
                )

        # 6. Suspected foreign transaction (non-ASCII chars in description)
        if tx["amount"] < 0:
            try:
                tx["description"].encode("ascii")
            except UnicodeEncodeError:
                issues.append("Description contains non-ASCII characters — possible foreign transaction")

        # 7. Potential refund without matching prior charge
        if tx["amount"] > 0 and tx["amount"] >= 1.0:
            desc_lower = tx["description"].lower()
            prior_expenses = desc_expense_map.get(desc_lower, [])
            if not prior_expenses:
                issues.append(
                    f"Credit/refund of {tx['amount']:.2f} with no matching prior charge found"
                )

        if issues:
            anomalies.append({
                "date": tx["date"],
                "description": tx["description"],
                "amount": tx["amount"],
                "issues": issues,
                "issue": issues[0],  # backwards compat
            })

        seen.append(tx)

    return anomalies


# ---------------------------------------------------------------------------
# Category & monthly aggregation
# ---------------------------------------------------------------------------

def _aggregate_categories(transactions: list[dict]) -> list[dict]:
    totals: dict[str, float] = defaultdict(float)
    counts: dict[str, int] = defaultdict(int)
    for tx in transactions:
        if tx["amount"] < 0:
            cat = tx["category"]
            totals[cat] += abs(tx["amount"])
            counts[cat] += 1
    return [
        {"category": cat, "transaction_count": counts[cat], "total": round(totals[cat], 2)}
        for cat in sorted(totals, key=lambda c: -totals[c])
    ]


def _aggregate_monthly(transactions: list[dict]) -> list[dict]:
    by_month: dict[str, dict] = defaultdict(lambda: {"debits": 0.0, "credits": 0.0, "count": 0})
    for tx in transactions:
        month = tx["date"][:7]
        if tx["amount"] < 0:
            by_month[month]["debits"] += abs(tx["amount"])
        else:
            by_month[month]["credits"] += tx["amount"]
        by_month[month]["count"] += 1
    return [
        {
            "month": m,
            "debits": round(v["debits"], 2),
            "credits": round(v["credits"], 2),
            "net": round(v["credits"] - v["debits"], 2),
            "count": v["count"],
        }
        for m, v in sorted(by_month.items())
    ]


def _top_merchants(transactions: list[dict], n: int = 10) -> list[dict]:
    by_merchant: dict[str, dict] = defaultdict(lambda: {"total": 0.0, "count": 0})
    for tx in transactions:
        if tx["amount"] < 0:
            by_merchant[tx["description"]]["total"] += abs(tx["amount"])
            by_merchant[tx["description"]]["count"] += 1
    ranked = sorted(
        [{"merchant": m, "total": round(v["total"], 2), "count": v["count"]} for m, v in by_merchant.items()],
        key=lambda x: -x["total"],
    )
    return ranked[:n]


# ---------------------------------------------------------------------------
# Main parsing function
# ---------------------------------------------------------------------------

def parse_statement(csv_path: Path, detect_subs: bool = True, period: str = "") -> dict:
    f, encoding = _open_with_fallback(csv_path)

    with f:
        raw_content = f.read()

    lines = raw_content.splitlines()
    if not lines:
        raise ValueError("CSV file is empty.")

    # Detect delimiter from first non-empty line
    sample_line = next((l for l in lines if l.strip()), "")
    sniffer = csv.Sniffer()
    try:
        detected = sniffer.sniff(sample_line, delimiters=",\t;|")
        delimiter = detected.delimiter
    except csv.Error:
        delimiter = ","

    # Skip preamble metadata rows
    header_idx = _skip_preamble(lines, delimiter)
    data_lines = lines[header_idx:]

    if not data_lines:
        raise ValueError("No data found after skipping preamble.")

    import io
    reader = csv.DictReader(io.StringIO("\n".join(data_lines)), delimiter=delimiter)

    if not reader.fieldnames:
        raise ValueError("CSV has no column headers.")

    col_map = _detect_columns(list(reader.fieldnames))

    if "date" not in col_map:
        raise ValueError(
            "Could not find a date column. Headers found: " + ", ".join(reader.fieldnames)
        )
    if "amount" not in col_map and "debit" not in col_map and "credit" not in col_map:
        raise ValueError(
            "Could not find an amount column. Headers found: " + ", ".join(reader.fieldnames)
        )

    transactions = []
    skipped = 0
    for i, row in enumerate(reader, start=2):
        parsed = _parse_row(row, col_map, i)
        if parsed:
            transactions.append(parsed)
        else:
            skipped += 1

    if not transactions:
        raise ValueError(
            f"No valid transactions found. Skipped {skipped} rows. "
            "Check that the file has parseable dates and amounts."
        )

    transactions.sort(key=lambda t: t["date"])

    # Detect primary currency from descriptions if not in column
    all_descriptions = " ".join(tx["description"] for tx in transactions)
    primary_currency = detect_currency(all_descriptions)

    total_credits = sum(tx["amount"] for tx in transactions if tx["amount"] > 0)
    total_debits = sum(tx["amount"] for tx in transactions if tx["amount"] < 0)

    result = {
        "meta": {
            "source_file": csv_path.name,
            "encoding": encoding,
            "period": period or f"{transactions[0]['date']} to {transactions[-1]['date']}",
            "currency": primary_currency,
            "rows_skipped": skipped,
        },
        "summary": {
            "total_transactions": len(transactions),
            "total_credits": round(total_credits, 2),
            "total_debits": round(total_debits, 2),
            "net_change": round(total_credits + total_debits, 2),
            "date_from": transactions[0]["date"],
            "date_to": transactions[-1]["date"],
        },
        "transactions": transactions,
        "by_category": _aggregate_categories(transactions),
        "by_month": _aggregate_monthly(transactions),
        "top_merchants": _top_merchants(transactions),
        "subscriptions": _detect_subscriptions(transactions) if detect_subs else [],
        "anomalies": _detect_anomalies(transactions),
    }

    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="statement_parser",
        description="Parse a bank CSV export and categorise transactions.",
    )
    parser.add_argument("--file", required=True, help="Path to the bank statement CSV")
    parser.add_argument("--output", required=True, help="Output JSON file path")
    parser.add_argument("--period", default="", help='Label for the statement period e.g. "Jan 2024"')
    parser.add_argument(
        "--detect-subs", action="store_true", default=True,
        help="Detect recurring subscriptions (default: on)",
    )
    parser.add_argument(
        "--no-detect-subs", dest="detect_subs", action="store_false",
        help="Disable subscription detection",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        csv_path = safe_output_path(args.file)
        if not csv_path.exists():
            print(f"Error: File not found: {csv_path}", file=sys.stderr)
            return 1

        result = parse_statement(csv_path, detect_subs=args.detect_subs, period=args.period)

        output_path = safe_output_path(args.output)
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        s = result["summary"]
        m = result["meta"]
        print(f"Parsed {s['total_transactions']} transactions ({s['date_from']} → {s['date_to']})")
        print(f"Credits: +{s['total_credits']:.2f}  |  Debits: {s['total_debits']:.2f}  |  Net: {s['net_change']:+.2f}")
        print(f"Currency: {m['currency']}  |  Skipped rows: {m['rows_skipped']}")
        print(f"Subscriptions detected: {len(result['subscriptions'])}")
        print(f"Anomalies flagged: {len(result['anomalies'])}")
        print(f"Output: {output_path}")
        return 0

    except (ValueError, OSError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
