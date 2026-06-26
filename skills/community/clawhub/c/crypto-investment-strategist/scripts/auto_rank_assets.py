#!/usr/bin/env python3
"""
Auto Rank Assets

Fetch market data for multiple symbols, calculate simple features,
and rank them using the local score_assets logic.

Usage:
  python3 scripts/auto_rank_assets.py --symbols BTC ETH SOL
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
FETCH_SCRIPT = SCRIPT_DIR / 'fetch_crypto_data.py'
INDICATOR_SCRIPT = SCRIPT_DIR / 'calculate_indicators.py'
SCORING_SCRIPT = SCRIPT_DIR / 'score_assets.py'


def run_json(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or 'Command failed')
    return json.loads(result.stdout)


def infer_narrative_score(symbol: str) -> float:
    core = {'BTC': 85, 'ETH': 82, 'SOL': 74, 'BNB': 72, 'XRP': 68}
    return core.get(symbol.upper(), 60)


def infer_tokenomics_score(symbol: str) -> float:
    core = {'BTC': 95, 'ETH': 85, 'SOL': 62, 'DOGE': 45, 'XRP': 58}
    return core.get(symbol.upper(), 55)


def liquidity_score(volume_usd: float) -> float:
    if volume_usd >= 5_000_000_000:
        return 95
    if volume_usd >= 1_000_000_000:
        return 85
    if volume_usd >= 250_000_000:
        return 75
    if volume_usd >= 50_000_000:
        return 65
    return 50


def process_symbol(symbol: str):
    summary = run_json(['python3', str(FETCH_SCRIPT), '--symbol', symbol, '--mode', 'summary'])

    with tempfile.NamedTemporaryFile('w+', suffix='.json', delete=False) as tf:
        json.dump({'candles': summary.get('hourly_data', [])}, tf)
        tf.flush()
        indicators = run_json(['python3', str(INDICATOR_SCRIPT), '--file', tf.name])

    trend = indicators.get('Trend', {}).get('trend', 'sideways')
    rsi = indicators.get('RSI', {}).get('value')
    price_vs_ma = indicators.get('PriceVsMA', {})

    return {
        'symbol': symbol.upper(),
        'price_change_24h_pct': summary.get('change_24h_pct', 0),
        'rsi': rsi,
        'trend': trend,
        'above_ma20': bool(price_vs_ma.get('MA20', {}).get('above', False)),
        'above_ma50': bool(price_vs_ma.get('MA50', {}).get('above', False)),
        'volatility_pct': indicators.get('ATR', {}).get('pct_of_price', 0),
        'narrative_score': infer_narrative_score(symbol),
        'liquidity_score': liquidity_score(float(summary.get('volume_24h_usd', 0) or 0)),
        'tokenomics_score': infer_tokenomics_score(symbol),
        'market_snapshot': {
            'price': summary.get('current_price'),
            'change_24h_pct': summary.get('change_24h_pct'),
            'volume_24h_usd': summary.get('volume_24h_usd'),
        }
    }


def main():
    parser = argparse.ArgumentParser(description='Automatically rank multiple crypto assets')
    parser.add_argument('--symbols', nargs='+', required=True, help='Symbols like BTC ETH SOL')
    parser.add_argument('--output', '-o', help='Optional output path')
    args = parser.parse_args()

    assets = []
    errors = []

    for symbol in args.symbols:
        try:
            assets.append(process_symbol(symbol))
        except Exception as e:
            errors.append({'symbol': symbol.upper(), 'error': str(e)})

    if not assets:
        print(json.dumps({'error': 'No assets processed successfully', 'details': errors}, indent=2))
        sys.exit(1)

    with tempfile.NamedTemporaryFile('w+', suffix='.json', delete=False) as tf:
        json.dump({'assets': assets}, tf)
        tf.flush()
        ranked = run_json(['python3', str(SCORING_SCRIPT), '--input', tf.name])

    output = {
        'input_assets': assets,
        'ranking': ranked,
        'errors': errors,
    }

    text = json.dumps(output, indent=2)
    if args.output:
        Path(args.output).write_text(text)
    else:
        print(text)


if __name__ == '__main__':
    main()
