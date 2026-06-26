#!/usr/bin/env python3
"""
Portfolio Allocation Helper

Create a practical allocation plan across BTC, ETH, altcoins, and stablecoins.

Usage:
  python3 scripts/allocate_portfolio.py --capital 10000 --risk medium
"""

import argparse
import json


def base_mix(risk: str):
    risk = risk.lower()
    if risk == 'low':
        return {'BTC': 40, 'ETH': 25, 'ALTS': 10, 'STABLES': 25}
    if risk == 'high':
        return {'BTC': 30, 'ETH': 20, 'ALTS': 35, 'STABLES': 15}
    return {'BTC': 35, 'ETH': 25, 'ALTS': 20, 'STABLES': 20}


def apply_regime(mix: dict, regime: str):
    regime = regime.lower()
    adjusted = dict(mix)

    if regime in ['downtrend', 'risk-off', 'defensive', 'bearish']:
        adjusted['STABLES'] += 15
        adjusted['ALTS'] -= 10
        adjusted['BTC'] += 5
    elif regime in ['uptrend', 'bullish']:
        adjusted['ALTS'] += 10
        adjusted['STABLES'] -= 10
    elif regime in ['range', 'sideways']:
        adjusted['STABLES'] += 5
        adjusted['ALTS'] -= 5

    total = sum(adjusted.values())
    normalized = {k: round(v * 100 / total, 2) for k, v in adjusted.items()}
    return normalized


def staged_deployment(amount: float, regime: str):
    regime = regime.lower()
    if regime in ['downtrend', 'risk-off', 'defensive', 'bearish']:
        return [25, 25, 50]
    if regime in ['uptrend', 'bullish']:
        return [40, 30, 30]
    return [30, 30, 40]


def main():
    parser = argparse.ArgumentParser(description='Allocate crypto portfolio by risk and regime')
    parser.add_argument('--capital', type=float, required=True, help='Total capital in USDT or USD')
    parser.add_argument('--risk', choices=['low', 'medium', 'high'], default='medium')
    parser.add_argument('--regime', default='range', help='Market regime: uptrend, downtrend, range, risk-off')
    parser.add_argument('--output', '-o')
    args = parser.parse_args()

    mix = base_mix(args.risk)
    mix = apply_regime(mix, args.regime)
    deployment_steps = staged_deployment(args.capital, args.regime)

    allocation_amounts = {k: round(args.capital * v / 100, 2) for k, v in mix.items()}

    output = {
        'capital': args.capital,
        'risk_profile': args.risk,
        'market_regime': args.regime,
        'allocation_pct': mix,
        'allocation_amounts': allocation_amounts,
        'deployment_plan_pct': {
            'stage_1': deployment_steps[0],
            'stage_2': deployment_steps[1],
            'stage_3': deployment_steps[2],
        },
        'notes': [
            'Use staged entries instead of all-in deployment.',
            'Increase stablecoin reserve when volatility is extreme.',
            'Review allocation after major BTC regime changes.'
        ]
    }

    text = json.dumps(output, indent=2)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(text)
    else:
        print(text)


if __name__ == '__main__':
    main()
