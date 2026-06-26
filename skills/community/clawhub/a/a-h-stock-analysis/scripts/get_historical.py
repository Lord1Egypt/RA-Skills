#!/usr/bin/env python3
import argparse
import pandas as pd
from utils import init_tushare, get_daily

def main():
    parser = argparse.ArgumentParser(description='Get historical daily data')
    parser.add_argument('--code', required=True, help='Stock code (6-digit for A share, 5-digit for HK)')
    parser.add_argument('--start', help='Start date (YYYYMMDD)')
    parser.add_argument('--end', help='End date (YYYYMMDD)')
    parser.add_argument('--output', help='Output CSV file')
    args = parser.parse_args()
    
    pro = init_tushare()
    df = get_daily(pro, args.code, args.start, args.end)
    
    if df.empty:
        print(f"No historical data found for {args.code}")
        return
    
    print(f"Got {len(df)} trading days for {args.code}")
    print(df.head(10).to_string(index=False))
    
    if args.output:
        df.to_csv(args.output, index=False)
        print(f"\nData saved to {args.output}")

if __name__ == '__main__':
    main()
