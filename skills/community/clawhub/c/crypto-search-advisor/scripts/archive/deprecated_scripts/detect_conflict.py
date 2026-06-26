#!/usr/bin/env python3
import sys
import json
import argparse
sys.path.insert(0, '.')

from crypto_advisor import detect_conflict

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--screenshot-price', type=float, default=0)
    parser.add_argument('--search-min', type=float, default=0)
    parser.add_argument('--search-max', type=float, default=0)
    args = parser.parse_args()
    
    result = detect_conflict(args.screenshot_price, args.search_min, args.search_max)
    print(json.dumps(result, ensure_ascii=False, indent=2))
