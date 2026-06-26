#!/usr/bin/env python3
"""
Run Investment Workflow

One-command workflow for:
- auto ranking assets from live market data
- portfolio allocation by capital / risk / regime
- execution summary
- optional snapshot logging for the top candidate

Usage:
  python3 scripts/run_investment_workflow.py --symbols BTC ETH SOL --capital 10000 --risk medium --regime uptrend
  python3 scripts/run_investment_workflow.py --symbols BTC ETH SOL --capital 10000 --risk medium --regime uptrend --log-top-pick
"""

import argparse
import json
import subprocess
import tempfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
AUTO_RANK = SCRIPT_DIR / 'auto_rank_assets.py'
ALLOCATE = SCRIPT_DIR / 'allocate_portfolio.py'
LOG_SNAPSHOT = SCRIPT_DIR / 'log_analysis_snapshot.py'


def run_json(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or 'Command failed')
    return json.loads(result.stdout)


def build_execution_plan(top_pick: dict, risk: str, regime: str, capital: float):
    symbol = top_pick.get('symbol', 'UNKNOWN')
    overall = top_pick.get('scores', {}).get('overall', 0)
    action = top_pick.get('action', 'WAIT')
    confidence = top_pick.get('confidence', 'low')

    risk = risk.lower()
    regime = regime.lower()

    max_position_map = {
        'low': 0.10,
        'medium': 0.18,
        'high': 0.25,
    }
    regime_factor = 0.8 if regime in ['downtrend', 'risk-off', 'defensive', 'bearish'] else 1.0
    max_position_pct = round(max_position_map.get(risk, 0.18) * regime_factor * 100, 2)
    position_amount = round(capital * max_position_pct / 100, 2)

    stage_1 = round(position_amount * 0.4, 2)
    stage_2 = round(position_amount * 0.3, 2)
    stage_3 = round(position_amount * 0.3, 2)

    if overall >= 80:
        thesis = f'{symbol} is the strongest candidate in the current basket with a high-quality profile.'
    elif overall >= 65:
        thesis = f'{symbol} is acceptable, but staged entry discipline matters.'
    else:
        thesis = f'{symbol} is not strong enough for aggressive deployment. Keep sizing small or wait.'

    return {
        'symbol': symbol,
        'action': action,
        'confidence': confidence,
        'overall_score': overall,
        'max_position_pct': max_position_pct,
        'max_position_amount': position_amount,
        'staged_entries': {
            'stage_1_amount': stage_1,
            'stage_2_amount': stage_2,
            'stage_3_amount': stage_3,
        },
        'thesis': thesis,
    }


def maybe_log_top_pick(plan: dict):
    return run_json([
        'python3', str(LOG_SNAPSHOT),
        '--symbol', plan['symbol'],
        '--action', plan['action'],
        '--price', str(plan.get('market_price', 0) or 0),
        '--confidence', plan['confidence'],
        '--thesis', plan['thesis'],
        '--notes', 'auto workflow top pick'
    ])


def main():
    parser = argparse.ArgumentParser(description='One-command crypto investment workflow')
    parser.add_argument('--symbols', nargs='+', required=True, help='Symbols to rank, e.g. BTC ETH SOL')
    parser.add_argument('--capital', type=float, required=True, help='Total capital in USDT or USD')
    parser.add_argument('--risk', choices=['low', 'medium', 'high'], default='medium')
    parser.add_argument('--regime', default='range', help='Market regime: uptrend, downtrend, range, risk-off')
    parser.add_argument('--log-top-pick', action='store_true', help='Save a snapshot for the top ranked asset')
    parser.add_argument('--output', '-o', help='Optional output file')
    args = parser.parse_args()

    ranking = run_json([
        'python3', str(AUTO_RANK),
        '--symbols', *args.symbols,
    ])

    allocation = run_json([
        'python3', str(ALLOCATE),
        '--capital', str(args.capital),
        '--risk', args.risk,
        '--regime', args.regime,
    ])

    top_pick = ranking.get('ranking', {}).get('best_candidate') or {}
    execution = build_execution_plan(top_pick, args.risk, args.regime, args.capital)

    market_price = None
    for item in ranking.get('input_assets', []):
        if item.get('symbol') == execution['symbol']:
            market_price = item.get('market_snapshot', {}).get('price')
            break
    execution['market_price'] = market_price

    snapshot_result = None
    if args.log_top_pick and execution['symbol'] and market_price is not None:
        snapshot_result = maybe_log_top_pick(execution)

    output = {
        'workflow': {
            'symbols': [s.upper() for s in args.symbols],
            'capital': args.capital,
            'risk': args.risk,
            'regime': args.regime,
        },
        'ranking': ranking,
        'allocation': allocation,
        'top_pick_execution_plan': execution,
        'snapshot': snapshot_result,
    }

    text = json.dumps(output, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(text, encoding='utf-8')
    else:
        print(text)


if __name__ == '__main__':
    main()
