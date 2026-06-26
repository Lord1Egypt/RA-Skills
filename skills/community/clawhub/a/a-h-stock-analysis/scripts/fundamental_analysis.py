#!/usr/bin/env python3
import argparse
import pandas as pd
from utils import init_tushare, format_ts_code, HAVE_TUSHARE, HAVE_AKSHARE, ak

def get_financial_indicator_tushare(pro, ts_code):
    """Get financial indicators from Tushare"""
    if not pro:
        return pd.DataFrame()
    try:
        df = pro.fina_indicator(ts_code=ts_code)
        return df
    except Exception:
        return pd.DataFrame()

def get_financial_indicator_akshare(code):
    """Get financial indicators from AKShare"""
    try:
        # AKShare gets financial report for A shares
        if len(code.strip()) == 6:
            # A share
            df = ak.stock_financial_report(stock=code, symbol="报告期")
            return df
        elif len(code.strip()) == 5:
            # HK stock
            df = ak.hk_stock_financial_report(symbol=code)
            return df
    except Exception as e:
        print(f"AKShare finance fetch failed: {e}", file=sys.stderr)
        return pd.DataFrame()
    return pd.DataFrame()

def main():
    parser = argparse.ArgumentParser(description='Fundamental analysis for stock')
    parser.add_argument('--code', required=True, help='Stock code (6-digit for A share, 5-digit for HK)')
    parser.add_argument('--quarters', type=int, default=8, help='Number of recent quarters to show')
    args = parser.parse_args()
    
    pro = init_tushare()
    ts_code = format_ts_code(args.code)
    
    # Try Tushare first
    df = get_financial_indicator_tushare(pro, ts_code)
    source = "Tushare"
    
    if df.empty:
        # Fallback to AKShare
        print("Tushare didn't return data, trying AKShare...")
        df = get_financial_indicator_akshare(args.code)
        source = "AKShare"
    
    if df.empty:
        print(f"No financial data found for {args.code} from any source")
        return
    
    # Sort by latest first and take recent N quarters
    if 'end_date' in df.columns:
        df = df.sort_values('end_date', ascending=False).head(args.quarters)
    elif '报告期' in df.columns:
        df = df.sort_values('报告期', ascending=False).head(args.quarters)
    
    print(f"=== Fundamental Analysis for {args.code} (Source: {source}) ===\n")
    print(df.head(args.quarters).to_string(index=False))

if __name__ == '__main__':
    import sys
    main()
