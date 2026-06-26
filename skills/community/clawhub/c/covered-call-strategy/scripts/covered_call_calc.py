#!/usr/bin/env python3
"""
Covered Call Portfolio Scenario Calculator

Calculates total P&L across multiple stock price scenarios for different
covered call strategy options.

Usage:
  python covered_call_calc.py --stock-price 750 --cost-basis 500.7 --shares 300 \
    --calls "580:54.85:262,580:80.05:262,820:115:166" \
    --strategies "hold,roll_up:820,roll_partial:820:1,close:1"

Output: Scenario matrix as markdown table
"""

import argparse
import json
import sys

def parse_calls(calls_str):
    """Parse 'strike:premium:current,...' format"""
    calls = []
    for c in calls_str.split(','):
        parts = c.split(':')
        calls.append({
            'strike': float(parts[0]),
            'premium': float(parts[1]),
            'current': float(parts[2])
        })
    return calls

def calc_pnl(stock_price, avg_cost, shares, calls, net_premium_total):
    """Calculate total P&L at a given stock price at expiry"""
    stock_pnl = 0
    remaining_shares = shares
    calls_sorted = sorted(calls, key=lambda x: x['strike'])  # lower strikes assigned first
    
    for call in calls_sorted:
        call_shares = 100
        if stock_price > call['strike']:
            # ITM: shares assigned at strike
            stock_pnl += (call['strike'] - avg_cost) * call_shares
        else:
            # OTM: shares not assigned, sell at market
            stock_pnl += (stock_price - avg_cost) * call_shares
        remaining_shares -= call_shares
    
    # Any unassigned shares
    if remaining_shares > 0:
        stock_pnl += (stock_price - avg_cost) * remaining_shares
    
    premium_pnl = net_premium_total
    return stock_pnl + premium_pnl

def main():
    parser = argparse.ArgumentParser(description='Covered Call Scenario Calculator')
    parser.add_argument('--stock-price', type=float, required=True, help='Current stock price')
    parser.add_argument('--cost-basis', type=float, required=True, help='Average cost basis per share')
    parser.add_argument('--shares', type=int, required=True, help='Total shares held')
    parser.add_argument('--calls', type=str, required=True, help='Calls as strike:premium:current,...')
    parser.add_argument('--roll-strike', type=float, help='New strike for roll strategy')
    parser.add_argument('--roll-count', type=int, default=0, help='Number of calls to roll')
    
    args = parser.parse_args()
    calls = parse_calls(args.calls)
    
    # Calculate net premium for "do nothing"
    net_premium_hold = sum(c['premium'] for c in calls) * 100
    
    # Generate price scenarios
    prices = []
    for pct in [-30, -20, -15, -10, -5, 0, 5, 10, 15, 20, 30, 50]:
        p = args.stock_price * (1 + pct/100)
        prices.append(round(p, 2))
    
    # Add strike prices
    for c in calls:
        if c['strike'] not in prices:
            prices.append(c['strike'])
    if args.roll_strike and args.roll_strike not in prices:
        prices.append(args.roll_strike)
    prices.sort()
    
    print(f"# Covered Call Scenario Analysis")
    print(f"\nStock: ${args.stock_price} | Cost Basis: ${args.cost_basis} | Shares: {args.shares}")
    print(f"\n## Strategy: Hold (Do Nothing)")
    print(f"Net Premium Cushion: ${net_premium_hold:,.0f}")
    print(f"\n| Stock at Expiry | Stock P&L | Premium | **Total P&L** |")
    print(f"|----------------|-----------|---------|-------------|")
    
    for p in prices:
        total = calc_pnl(p, args.cost_basis, args.shares, calls, net_premium_hold)
        stock_pnl = (p - args.cost_basis) * args.shares  # approximate
        sign = "+" if total > 0 else ""
        print(f"| ${p:,.0f} | ${stock_pnl:+,.0f} | ${net_premium_hold:,.0f} | {sign}${total:+,.0f} |")

if __name__ == '__main__':
    main()
