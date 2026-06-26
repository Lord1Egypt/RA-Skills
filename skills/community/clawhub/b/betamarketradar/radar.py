#!/usr/bin/env python3
"""Market Radar — real-time market monitoring"""
import argparse, sys

def main():
    p = argparse.ArgumentParser(description='Market Radar')
    p.add_argument('--watch', default='SPX,QQQ,VIX', help='Comma-separated symbols')
    p.add_argument('--threshold', type=float, default=1.5, help='Alert threshold %')
    args = p.parse_args()
    symbols = [s.strip() for s in args.watch.split(',')]
    print(f"📡 Market Radar Active")
    print(f"Watching: {', '.join(symbols)}")
    print(f"Alert threshold: {args.threshold}% move")
    print("\n(Simulated — connect Tiger API for real data)")
    for s in symbols:
        print(f"  {s}: ---")

if __name__ == '__main__':
    main()
