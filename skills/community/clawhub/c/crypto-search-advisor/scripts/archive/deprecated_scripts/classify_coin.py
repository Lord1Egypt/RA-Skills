#!/usr/bin/env python3
import sys
import json
import argparse
sys.path.insert(0, '.')

from crypto_advisor import classify_coin

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--symbol', required=True)
    parser.add_argument('--price', type=float, default=None)
    args = parser.parse_args()
    
    result = classify_coin(args.symbol, args.price)
    print(json.dumps(result, ensure_ascii=False, indent=2))
