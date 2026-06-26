#!/usr/bin/env python3
import argparse
import pandas as pd
import numpy as np
from utils import init_tushare, get_daily

def calc_ma(df, window):
    """Calculate moving average"""
    return df['close'].rolling(window=window).mean()

def calc_macd(df, fast=12, slow=26, signal=9):
    """Calculate MACD"""
    ema_fast = df['close'].ewm(span=fast, adjust=False).mean()
    ema_slow = df['close'].ewm(span=slow, adjust=False).mean()
    diff = ema_fast - ema_slow
    dea = diff.ewm(span=signal, adjust=False).mean()
    macd = 2 * (diff - dea)
    return diff, dea, macd

def calc_rsi(df, period=14):
    """Calculate RSI"""
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def main():
    parser = argparse.ArgumentParser(description='Calculate technical indicators')
    parser.add_argument('--code', required=True, help='Stock code (6-digit for A share, 5-digit for HK)')
    parser.add_argument('--start', help='Start date (YYYYMMDD)')
    parser.add_argument('--end', help='End date (YYYYMMDD)')
    parser.add_argument('--output', help='Output CSV file')
    args = parser.parse_args()
    
    pro = init_tushare()
    df = get_daily(pro, args.code, args.start, args.end)
    
    if df.empty:
        print(f"No data found for {args.code}")
        return
    
    # Calculate indicators
    df['ma5'] = calc_ma(df, 5)
    df['ma10'] = calc_ma(df, 10)
    df['ma20'] = calc_ma(df, 20)
    df['ma60'] = calc_ma(df, 60)
    df['diff'], df['dea'], df['macd'] = calc_macd(df)
    df['rsi14'] = calc_rsi(df, 14)
    
    # Show latest
    latest = df.iloc[-1]
    print(f"=== Technical Indicators for {args.code} (Latest trading day: {latest['trade_date']}) ===\n")
    print(f"Current price: {latest['close']:.2f}")
    print(f"MA5:  {latest['ma5']:.2f}")
    print(f"MA10: {latest['ma10']:.2f}")
    print(f"MA20: {latest['ma20']:.2f}")
    print(f"MA60: {latest['ma60']:.2f}")
    print(f"MACD: {latest['macd']:.3f} (DIFF: {latest['diff']:.3f}, DEA: {latest['dea']:.3f})")
    print(f"RSI(14): {latest['rsi14']:.2f}")
    
    # Simple trend analysis
    print("\n=== Trend Summary ===")
    if not pd.isna(latest['ma5']) and not pd.isna(latest['ma20']):
        if latest['ma5'] > latest['ma20']:
            print("- MA5 above MA20 -> Short-term uptrend")
        else:
            print("- MA5 below MA20 -> Short-term downtrend")
    
    if not pd.isna(latest['rsi14']):
        if latest['rsi14'] > 70:
            print("- RSI > 70 -> Potentially overbought")
        elif latest['rsi14'] < 30:
            print("- RSI < 30 -> Potentially oversold")
        else:
            print("- RSI in neutral range")
    
    if args.output:
        df.to_csv(args.output, index=False)
        print(f"\nFull data saved to {args.output}")

if __name__ == '__main__':
    main()
