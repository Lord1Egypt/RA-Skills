#!/usr/bin/env python3
import sys
import json
import argparse
sys.path.insert(0, '.')

from crypto_advisor import analyze

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--symbol', required=True)
    parser.add_argument('--category', default='mainstream')
    parser.add_argument('--screenshot-price', type=float, default=0)
    parser.add_argument('--search-min', type=float, default=0)
    parser.add_argument('--search-max', type=float, default=0)
    args = parser.parse_args()
    
    sc_data = {
        'price': args.screenshot_price,
        'clarity': 'clear',
        'confidence': 'high'
    }
    se_data = {
        'min': args.search_min,
        'max': args.search_max
    }
    result = analyze(args.symbol, sc_data, se_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
