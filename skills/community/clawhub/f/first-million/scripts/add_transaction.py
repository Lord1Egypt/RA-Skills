#!/usr/bin/env python3
"""
Add income or expense transaction to ledger (first-million data directory).
Usage: python3 add_transaction.py --type expense|income --amount <number> --category <category> [--note <note>] [--date <YYYY-MM-DD>]
"""

import argparse
import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.expanduser("~/.openclaw/workspace"), "first-million", "ledger.json")

def ensure_data_dir():
    """Ensure first-million data directory exists."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

def load_ledger():
    """Load existing ledger data."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"transactions": [], "categories": {}}

def save_ledger(ledger):
    """Save ledger data."""
    with open(DATA_FILE, 'w') as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)

def add_transaction(trans_type, amount, category, note=None, date=None):
    """Add a transaction to the ledger."""
    ensure_data_dir()
    ledger = load_ledger()

    transaction = {
        "type": trans_type,  # "income" or "expense"
        "amount": float(amount),
        "category": category,
        "date": date or datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now().isoformat()
    }

    if note:
        transaction["note"] = note

    ledger["transactions"].append(transaction)
    save_ledger(ledger)

    return transaction

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add financial transaction")
    parser.add_argument("--type", required=True, choices=["income", "expense"], help="Transaction type")
    parser.add_argument("--amount", required=True, type=float, help="Amount")
    parser.add_argument("--category", required=True, help="Category")
    parser.add_argument("--note", help="Optional note")
    parser.add_argument("--date", help="Date (YYYY-MM-DD), defaults to today")

    args = parser.parse_args()

    transaction = add_transaction(args.type, args.amount, args.category, args.note, args.date)
    print(f"✓ Added {transaction['type']}: {transaction['amount']} - {transaction['category']}")
