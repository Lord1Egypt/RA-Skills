#!/usr/bin/env python3
"""
Decision Calculator — Expected Value & Kelly Criterion Calculator

Usage:
    python decision_calculator.py --ev -p 0.3 -g 100000 -l 20000
    python decision_calculator.py --kelly -p 0.4 -o 3
    python decision_calculator.py --full -p 0.3 -g 100000 -l 20000 --capital 500000
"""

from __future__ import annotations

import argparse
import sys


def calculate_expected_value(probability: float, gain: float, loss: float) -> float:
    """Calculate Expected Value: EV = p * gain - (1-p) * loss"""
    return probability * gain - (1 - probability) * loss


def calculate_kelly(probability: float, odds: float) -> float:
    """Calculate Kelly Criterion: f* = (p*b - q) / b"""
    q = 1 - probability
    return (probability * odds - q) / odds


def analyze_decision(
    probability: float,
    gain: float,
    loss: float,
    capital: float | None = None,
    conservative: bool = False,
    very_conservative: bool = False,
) -> dict:
    """Full decision analysis"""
    ev = calculate_expected_value(probability, gain, loss)
    odds = gain / loss if loss > 0 else float("inf")
    kelly = calculate_kelly(probability, odds)

    # Conservative strategy adjustment
    if very_conservative:
        kelly *= 0.25
        strategy = "Ultra-conservative (quarter-Kelly)"
    elif conservative:
        kelly *= 0.5
        strategy = "Conservative (half-Kelly)"
    else:
        strategy = "Standard Kelly"

    # Clamp Kelly fraction to [0, 1]
    kelly = max(0, min(kelly, 1))

    result = {
        "ev": ev,
        "ev_positive": ev > 0,
        "odds": odds,
        "kelly_fraction": kelly,
        "strategy": strategy,
        "recommendation": "",
    }

    if capital:
        result["suggested_investment"] = capital * kelly

    # Generate recommendation
    if ev <= 0:
        result["recommendation"] = "Negative EV — do not participate"
    elif kelly <= 0:
        result["recommendation"] = "Kelly suggests no bet (win rate too low or odds unfavorable)"
    elif kelly < 0.05:
        result["recommendation"] = "Tiny exploratory position (<5%)"
    elif kelly < 0.2:
        result["recommendation"] = "Light position (5-20%)"
    elif kelly < 0.4:
        result["recommendation"] = "Moderate position (20-40%)"
    else:
        result["recommendation"] = "Can take a large position but never go all-in"

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Decision Calculator")
    parser.add_argument("--ev", action="store_true", help="Calculate Expected Value only")
    parser.add_argument("--kelly", action="store_true", help="Calculate Kelly Criterion only")
    parser.add_argument("--full", action="store_true", help="Full analysis")
    parser.add_argument("-p", "--probability", type=float, required=True, help="Win rate (0-1)")
    parser.add_argument("-g", "--gain", type=float, help="Gain amount")
    parser.add_argument("-l", "--loss", type=float, help="Loss amount")
    parser.add_argument("-o", "--odds", type=float, help="Odds (win/loss ratio)")
    parser.add_argument("--capital", type=float, help="Total capital")
    parser.add_argument("--conservative", action="store_true", help="Use half-Kelly")
    parser.add_argument("--very-conservative", action="store_true", help="Use quarter-Kelly")

    args = parser.parse_args()

    if args.probability < 0 or args.probability > 1:
        print("Error: Win rate must be between 0 and 1", file=sys.stderr)
        return 1

    # Expected Value calculation
    if args.ev or args.full:
        if args.gain is None or args.loss is None:
            print("Error: --gain and --loss required for EV calculation", file=sys.stderr)
            return 1
        ev = calculate_expected_value(args.probability, args.gain, args.loss)
        print(f"Expected Value (EV): {ev:,.2f}")
        print(f"  Win rate: {args.probability*100:.1f}%")
        print(f"  Gain: {args.gain:,.2f}")
        print(f"  Loss: {args.loss:,.2f}")
        print(f"  Verdict: {'Positive EV' if ev > 0 else 'Negative EV'}")
        print()

    # Kelly Criterion calculation
    if args.kelly or args.full:
        if args.odds:
            odds = args.odds
        elif args.gain and args.loss and args.loss > 0:
            odds = args.gain / args.loss
        else:
            print("Error: --odds or --gain and --loss required for Kelly calculation", file=sys.stderr)
            return 1

        kelly = calculate_kelly(args.probability, odds)
        print(f"Kelly Criterion (f*): {kelly:.4f} ({kelly*100:.2f}%)")
        print(f"  Win rate: {args.probability*100:.1f}%")
        print(f"  Odds: {odds:.2f}")
        if args.capital:
            print(f"  Suggested investment: {args.capital * kelly:,.2f}")
        print()

    # Full analysis
    if args.full:
        if args.gain is None or args.loss is None:
            print("Error: --gain and --loss required for full analysis", file=sys.stderr)
            return 1

        result = analyze_decision(
            probability=args.probability,
            gain=args.gain,
            loss=args.loss,
            capital=args.capital,
            conservative=args.conservative,
            very_conservative=args.very_conservative,
        )

        print("=" * 40)
        print("Decision Analysis Report")
        print("=" * 40)
        print(f"Expected Value: {result['ev']:,.2f} ({'Positive' if result['ev_positive'] else 'Negative'})")
        print(f"Odds: {result['odds']:.2f}")
        print(f"Kelly Fraction: {result['kelly_fraction']*100:.2f}% ({result['strategy']})")
        if args.capital:
            print(f"Suggested Investment: {result['suggested_investment']:,.2f}")
        print(f"Recommendation: {result['recommendation']}")
        print("=" * 40)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
