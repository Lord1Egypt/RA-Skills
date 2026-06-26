#!/usr/bin/env python3
"""
Asset Scoring Helper

Score multiple crypto assets using lightweight rule-based inputs.
This script is designed for practical ranking, not perfect prediction.

Usage:
  python3 scripts/score_assets.py --input data.json
"""

import argparse
import json
import sys
from typing import Dict, List


def clamp(value: float, min_value: float = 0, max_value: float = 100) -> float:
    return max(min_value, min(max_value, value))


def score_asset(asset: Dict) -> Dict:
    symbol = asset.get('symbol', 'UNKNOWN')
    price_change_24h = float(asset.get('price_change_24h_pct', 0) or 0)
    rsi = asset.get('rsi')
    trend = str(asset.get('trend', 'sideways')).lower()
    above_ma20 = bool(asset.get('above_ma20', False))
    above_ma50 = bool(asset.get('above_ma50', False))
    volatility = float(asset.get('volatility_pct', 0) or 0)
    narrative = float(asset.get('narrative_score', 50) or 50)
    liquidity = float(asset.get('liquidity_score', 50) or 50)
    tokenomics = float(asset.get('tokenomics_score', 50) or 50)

    technical = 50
    if trend in ['uptrend', 'up', 'bullish']:
        technical += 15
    elif trend in ['downtrend', 'down', 'bearish']:
        technical -= 15

    if above_ma20:
        technical += 7
    if above_ma50:
        technical += 8

    if rsi is not None:
        rsi = float(rsi)
        if 45 <= rsi <= 65:
            technical += 8
        elif 65 < rsi <= 75:
            technical += 2
        elif rsi > 75:
            technical -= 8
        elif 35 <= rsi < 45:
            technical += 2
        elif rsi < 30:
            technical -= 5

    technical = clamp(technical)

    entry_quality = 50
    if -3 <= price_change_24h <= 5:
        entry_quality += 10
    elif price_change_24h > 10:
        entry_quality -= 10
    elif price_change_24h < -8:
        entry_quality -= 6

    if volatility <= 4:
        entry_quality += 8
    elif volatility <= 8:
        entry_quality += 3
    elif volatility > 12:
        entry_quality -= 10

    entry_quality = clamp(entry_quality)

    risk_score = 50
    if volatility > 12:
        risk_score += 20
    elif volatility > 8:
        risk_score += 10
    elif volatility < 4:
        risk_score -= 5

    if trend in ['downtrend', 'down', 'bearish']:
        risk_score += 10
    if liquidity < 40:
        risk_score += 10
    if tokenomics < 40:
        risk_score += 10
    risk_score = clamp(risk_score)

    overall = (
        technical * 0.30 +
        entry_quality * 0.20 +
        narrative * 0.15 +
        liquidity * 0.15 +
        tokenomics * 0.20
    )
    overall = clamp(round(overall, 2))

    if overall >= 75 and risk_score <= 55:
        action = 'BUY'
    elif overall >= 65:
        action = 'SCALE_IN'
    elif overall >= 50:
        action = 'HOLD_OR_WAIT'
    else:
        action = 'AVOID'

    confidence = 'high' if overall >= 75 else 'medium' if overall >= 60 else 'low'

    return {
        'symbol': symbol,
        'scores': {
            'technical': round(technical, 2),
            'entry_quality': round(entry_quality, 2),
            'narrative': round(narrative, 2),
            'liquidity': round(liquidity, 2),
            'tokenomics': round(tokenomics, 2),
            'risk': round(risk_score, 2),
            'overall': overall,
        },
        'action': action,
        'confidence': confidence,
    }


def main():
    parser = argparse.ArgumentParser(description='Score crypto assets from structured input JSON')
    parser.add_argument('--input', '-i', required=True, help='Path to JSON file with asset list')
    parser.add_argument('--output', '-o', help='Optional output path')
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        payload = json.load(f)

    assets: List[Dict] = payload.get('assets', payload if isinstance(payload, list) else [])
    if not assets:
        print(json.dumps({'error': 'No assets found in input'}), file=sys.stderr)
        sys.exit(1)

    results = [score_asset(asset) for asset in assets]
    results.sort(key=lambda x: x['scores']['overall'], reverse=True)

    output = {
        'ranked_assets': results,
        'best_candidate': results[0] if results else None,
    }

    text = json.dumps(output, indent=2)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(text)
    else:
        print(text)


if __name__ == '__main__':
    main()
