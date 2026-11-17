#!/usr/bin/env python3
"""
Crypto Tax Calculator — FIFO cost-basis and capital gains report generator.

Reads a CSV of buy/sell transactions and produces a FIFO-matched capital
gains report (short-term vs long-term), per-asset summary, and an
IRS Form 8949-style CSV export.

Input CSV columns (header required):
    date,type,asset,quantity,price_usd,fee_usd
    2025-01-15,buy,BTC,0.5,42000,10
    2025-06-01,sell,BTC,0.2,68000,5

- date: ISO format YYYY-MM-DD (or YYYY-MM-DDTHH:MM:SS)
- type: "buy" or "sell"
- asset: ticker symbol, e.g. BTC, ETH, SOL
- quantity: amount of asset transacted (positive number)
- price_usd: price per unit in USD at time of transaction
- fee_usd: transaction fee in USD (optional, defaults to 0)

Usage:
    python3 tax_calc.py transactions.csv
    python3 tax_calc.py transactions.csv --year 2025
    python3 tax_calc.py transactions.csv --out report.csv
"""

import argparse
import csv
import sys
from collections import defaultdict, deque
from datetime import datetime, timedelta

LONG_TERM_DAYS = 365


def parse_date(s: str) -> datetime:
    s = s.strip()
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unrecognized date format: {s}")


def load_transactions(path: str):
    txns = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        required = {"date", "type", "asset", "quantity", "price_usd"}
        missing = required - set(h.strip() for h in reader.fieldnames or [])
        if missing:
            sys.exit(f"CSV missing required columns: {sorted(missing)}")
        for row in reader:
            txns.append({
                "date": parse_date(row["date"]),
                "type": row["type"].strip().lower(),
                "asset": row["asset"].strip().upper(),
                "quantity": float(row["quantity"]),
                "price_usd": float(row["price_usd"]),
                "fee_usd": float(row.get("fee_usd") or 0),
            })
    txns.sort(key=lambda t: t["date"])
    return txns


def fifo_match(txns, year=None):
    """Match sells against buys FIFO per-asset. Returns list of realized gain lots."""
    lots = defaultdict(deque)  # asset -> deque of {qty, cost_basis_per_unit, date}
    realized = []

    for t in txns:
        asset = t["asset"]
        if t["type"] == "buy":
            per_unit_cost = t["price_usd"] + (t["fee_usd"] / t["quantity"] if t["quantity"] else 0)
            lots[asset].append({"qty": t["quantity"], "basis": per_unit_cost, "date": t["date"]})
        elif t["type"] == "sell":
            qty_to_sell = t["quantity"]
            sell_fee_per_unit = t["fee_usd"] / t["quantity"] if t["quantity"] else 0
            proceeds_per_unit = t["price_usd"] - sell_fee_per_unit
            while qty_to_sell > 1e-12 and lots[asset]:
                lot = lots[asset][0]
                matched_qty = min(lot["qty"], qty_to_sell)
                gain = (proceeds_per_unit - lot["basis"]) * matched_qty
                holding_days = (t["date"] - lot["date"]).days
                term = "long" if holding_days >= LONG_TERM_DAYS else "short"
                if year is None or t["date"].year == year:
                    realized.append({
                        "asset": asset,
                        "acquired": lot["date"].date().isoformat(),
                        "sold": t["date"].date().isoformat(),
                        "quantity": round(matched_qty, 8),
                        "cost_basis": round(lot["basis"] * matched_qty, 2),
                        "proceeds": round(proceeds_per_unit * matched_qty, 2),
                        "gain_loss": round(gain, 2),
                        "term": term,
                        "holding_days": holding_days,
                    })
                lot["qty"] -= matched_qty
                qty_to_sell -= matched_qty
                if lot["qty"] <= 1e-12:
                    lots[asset].popleft()
            if qty_to_sell > 1e-6:
                print(f"WARNING: sold {qty_to_sell:.6f} {asset} on {t['date'].date()} "
                      f"with no matching cost basis (possible missing buy history)", file=sys.stderr)
    return realized


def summarize(realized):
    by_asset = defaultdict(lambda: {"short_gain": 0.0, "long_gain": 0.0, "trades": 0})
    total_short = total_long = 0.0
    for r in realized:
        b = by_asset[r["asset"]]
        b["trades"] += 1
        if r["term"] == "short":
            b["short_gain"] += r["gain_loss"]
            total_short += r["gain_loss"]
        else:
            b["long_gain"] += r["gain_loss"]
            total_long += r["gain_loss"]
    return by_asset, total_short, total_long


def main():
    ap = argparse.ArgumentParser(description="FIFO crypto capital gains calculator")
    ap.add_argument("csv_path", help="Path to transactions CSV")
    ap.add_argument("--year", type=int, default=None, help="Only report sales in this tax year")
    ap.add_argument("--out", default=None, help="Write Form-8949-style CSV export to this path")
    args = ap.parse_args()

    txns = load_transactions(args.csv_path)
    realized = fifo_match(txns, year=args.year)
    by_asset, total_short, total_long = summarize(realized)

    print("=" * 60)
    print("CRYPTO CAPITAL GAINS REPORT (FIFO)")
    if args.year:
        print(f"Tax year: {args.year}")
    print("=" * 60)
    for asset, b in sorted(by_asset.items()):
        print(f"\n{asset}: {b['trades']} closed lots")
        print(f"  Short-term gain/loss: ${b['short_gain']:,.2f}")
        print(f"  Long-term gain/loss:  ${b['long_gain']:,.2f}")
    print("\n" + "-" * 60)
    print(f"TOTAL short-term gain/loss: ${total_short:,.2f}")
    print(f"TOTAL long-term gain/loss:  ${total_long:,.2f}")
    print(f"TOTAL realized gain/loss:   ${total_short + total_long:,.2f}")
    print("-" * 60)

    if not realized:
        print("\nNo closed lots found for the given year/data.")

    if args.out:
        with open(args.out, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "asset", "acquired", "sold", "quantity", "cost_basis",
                "proceeds", "gain_loss", "term", "holding_days"
            ])
            writer.writeheader()
            writer.writerows(realized)
        print(f"\nDetailed lot-by-lot export written to {args.out}")

    print("\nNote: this is a cost-basis estimation tool, not tax advice. "
          "Verify results with a licensed tax professional before filing.")


if __name__ == "__main__":
    main()
