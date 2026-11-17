#!/usr/bin/env python3
"""DRT Self-Improving Agent — journal.py
Add a trade to trades.json (the agent's trading memory).
Eksempel:
  python3 journal.py --symbol SP500 --bias LONG --type 2 --entry 7741 \
    --sl 7681 --tp 7802 --rr 2.5 --result win --killzone NY
"""
import argparse, json, os, sys
from datetime import datetime, timezone

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB = os.path.join(DATA_DIR, "trades.json")

def load():
    if os.path.exists(DB):
        try:
            with open(DB) as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save(trades):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DB, "w") as f:
        json.dump(trades, f, indent=2)

def main():
    p = argparse.ArgumentParser(description="Journaliser en DRT-trade")
    p.add_argument("--symbol", required=True)
    p.add_argument("--bias", required=True, choices=["LONG", "SHORT"])
    p.add_argument("--type", type=int, required=True, choices=[1, 2, 3])
    p.add_argument("--entry", type=float, required=True)
    p.add_argument("--sl", type=float, required=True)
    p.add_argument("--tp", type=float, required=True)
    p.add_argument("--rr", type=float, required=True)
    p.add_argument("--result", required=True, choices=["win", "loss", "be"])
    p.add_argument("--killzone", default="", help="London/NY/SB-AM/SB-PM")
    p.add_argument("--notes", default="")
    a = p.parse_args()

    trade = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "symbol": a.symbol.upper(),
        "bias": a.bias,
        "type": a.type,
        "entry": a.entry, "sl": a.sl, "tp": a.tp,
        "rr": a.rr, "result": a.result,
        "killzone": a.killzone, "notes": a.notes,
    }
    trades = load()
    trades.append(trade)
    save(trades)
    print(f"✅ Journaliseret: {a.bias} {a.symbol} Type {a.type} → {a.result} ({a.rr}R)")
    print(f"   Total trades i hukommelse: {len(trades)}")

if __name__ == "__main__":
    main()
