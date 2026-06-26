#!/usr/bin/env python3
"""
Review Snapshots

Compare logged analysis snapshots with current market price.

Usage:
  python3 scripts/review_snapshots.py --limit 20
"""

import argparse
import json
import subprocess
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
FETCH_SCRIPT = SCRIPT_DIR / 'fetch_crypto_data.py'
LOG_FILE = SCRIPT_DIR.parent / 'data' / 'analysis_snapshots.jsonl'


def current_price(symbol: str):
    result = subprocess.run(
        ['python3', str(FETCH_SCRIPT), '--symbol', symbol, '--mode', 'ticker'],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    try:
        payload = json.loads(result.stdout)
        return float(payload.get('price')) if payload.get('price') is not None else None
    except Exception:
        return None


def main():
    parser = argparse.ArgumentParser(description='Review logged crypto snapshots')
    parser.add_argument('--limit', type=int, default=20)
    parser.add_argument('--symbol')
    args = parser.parse_args()

    if not LOG_FILE.exists():
        print(json.dumps({'error': 'No snapshot log found', 'path': str(LOG_FILE)}, indent=2))
        return

    rows = []
    for line in LOG_FILE.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if args.symbol and row.get('symbol') != args.symbol.upper():
            continue
        rows.append(row)

    rows = rows[-args.limit:]
    review = []
    for row in rows:
        symbol = row['symbol']
        now_price = current_price(symbol)
        then_price = float(row['price'])
        pnl_pct = None
        outcome = 'unknown'
        if now_price is not None and then_price > 0:
            pnl_pct = round((now_price - then_price) / then_price * 100, 2)
            if row['action'] in ['BUY', 'SCALE_IN', 'HOLD']:
                outcome = 'positive' if pnl_pct > 0 else 'negative' if pnl_pct < 0 else 'flat'
            elif row['action'] in ['REDUCE', 'EXIT', 'SELL']:
                outcome = 'positive' if pnl_pct < 0 else 'negative' if pnl_pct > 0 else 'flat'

        review.append({
            'timestamp': row['timestamp'],
            'symbol': symbol,
            'action': row['action'],
            'then_price': then_price,
            'now_price': now_price,
            'move_pct_since_call': pnl_pct,
            'outcome': outcome,
            'confidence': row.get('confidence'),
            'thesis': row.get('thesis'),
        })

    print(json.dumps({'count': len(review), 'reviews': review}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
