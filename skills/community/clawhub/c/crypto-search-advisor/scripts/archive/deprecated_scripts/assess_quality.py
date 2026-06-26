#!/usr/bin/env python3
import sys
import json
import argparse
sys.path.insert(0, '.')

from crypto_advisor import assess_screenshot_quality

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', default='assess')
    parser.add_argument('--clarity', default='clear')
    parser.add_argument('--confidence', default='high')
    parser.add_argument('--missing', default='')
    args = parser.parse_args()
    
    missing_list = [x.strip() for x in args.missing.split(',') if x.strip()]
    result = assess_screenshot_quality(args.clarity, args.confidence, missing_list)
    print(json.dumps(result, ensure_ascii=False, indent=2))
