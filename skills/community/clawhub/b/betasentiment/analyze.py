#!/usr/bin/env python3
"""Sentiment Analyzer for financial text"""
import argparse, re

POSITIVE = ['bullish','moon','pump','to the moon','profit','gain','rise','up','breakout','buy','long','moon','APE','wagmi','ngmi','bull']
NEGATIVE = ['bearish','dump','crash','loss','fall','down','sell','short','fud','rug','scam','risk','warn','drop','breakdown']

def score(text):
    t = text.lower()
    pos = sum(1 for w in POSITIVE if w in t)
    neg = sum(1 for w in NEGATIVE if w in t)
    total = pos + neg
    if total == 0: return 0.5, 'NEUTRAL', 0.5
    ratio = pos / total
    if ratio > 0.7: return ratio, 'BULLISH 🐂', ratio
    if ratio < 0.3: return ratio, 'BEARISH 🐻', 1-ratio
    return ratio, 'NEUTRAL ⚖️', 0.5

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--text', default=None)
    p.add_argument('--file', default=None)
    args = p.parse_args()
    if args.file:
        with open(args.file) as f: text = f.read()
    else: text = args.text or input("Text: ")
    s, label, conf = score(text)
    print(f"\n🔍 SENTIMENT ANALYSIS\n━━━━━━━━━━━━━━━━━━━━━\nText: {text[:80]}...\nScore: {s:.2f}\nVerdict: {label}\nConfidence: {conf:.0%}\n")

if __name__ == '__main__':
    main()
