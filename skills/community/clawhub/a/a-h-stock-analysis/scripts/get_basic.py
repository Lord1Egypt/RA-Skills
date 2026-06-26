#!/usr/bin/env python3
import argparse
import sys
from utils import get_stock_basic

def main():
    parser = argparse.ArgumentParser(description='Get stock basic information')
    parser.add_argument('--code', required=True, help='Stock code (6-digit for A share, 5-digit for HK)')
    args = parser.parse_args()
    
    df, source = get_stock_basic(args.code)
    
    if df.empty:
        print(f"No data found for {args.code} from any source")
        sys.exit(1)
    
    print(f"Source: {source}")
    print()
    print(df.T.to_string(header=False))

if __name__ == '__main__':
    main()
