#!/usr/bin/env python3
"""
Log Analysis Snapshot

Save an analysis decision into a local JSONL log for later review.

Usage:
  python3 scripts/log_analysis_snapshot.py --symbol BTC --action BUY --price 82000 --thesis "Trend intact"
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = ROOT / 'data'
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / 'analysis_snapshots.jsonl'


def main():
    parser = argparse.ArgumentParser(description='Log crypto analysis snapshot')
    parser.add_argument('--symbol', required=True)
    parser.add_argument('--action', required=True)
    parser.add_argument('--price', type=float, required=True)
    parser.add_argument('--confidence', default='medium')
    parser.add_argument('--thesis', required=True)
    parser.add_argument('--entry1')
    parser.add_argument('--entry2')
    parser.add_argument('--stop')
    parser.add_argument('--tp1')
    parser.add_argument('--tp2')
    parser.add_argument('--notes', default='')
    args = parser.parse_args()

    row = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'symbol': args.symbol.upper(),
        'action': args.action,
        'price': args.price,
        'confidence': args.confidence,
        'thesis': args.thesis,
        'plan': {
            'entry1': args.entry1,
            'entry2': args.entry2,
            'stop': args.stop,
            'tp1': args.tp1,
            'tp2': args.tp2,
        },
        'notes': args.notes,
    }

    with LOG_FILE.open('a', encoding='utf-8') as f:
        f.write(json.dumps(row, ensure_ascii=False) + '\n')

    print(json.dumps({'saved': True, 'path': str(LOG_FILE), 'snapshot': row}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
