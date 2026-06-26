#!/usr/bin/env python3
import argparse
import akshare as ak
import pandas as pd

from _lib import pick_col


def compute_indicators(df: pd.DataFrame):
    close_col = pick_col(df, ['close', '收盘', '收盘价', '最新价', '价格', 'Close'])
    if close_col is None:
        raise ValueError(f"Cannot find close column in: {list(df.columns)}")
    close = pd.to_numeric(df[close_col], errors='coerce')

    out = df.copy()
    out['ma_5'] = close.rolling(5).mean()
    out['ma_10'] = close.rolling(10).mean()
    out['ma_20'] = close.rolling(20).mean()

    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    out['ema_12'] = ema12
    out['ema_26'] = ema26

    macd_line = ema12 - ema26
    signal = macd_line.ewm(span=9, adjust=False).mean()
    out['macd'] = macd_line
    out['macd_signal'] = signal
    out['macd_hist'] = macd_line - signal

    # Simple RSI(14)
    delta = close.diff()
    up = delta.clip(lower=0)
    down = (-delta).clip(lower=0)
    rs = up.rolling(14).mean() / down.rolling(14).mean()
    out['rsi_14'] = 100 - (100 / (1 + rs))

    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--contract', required=True, help='合约，如 IF2008 / RB2410 等')
    ap.add_argument('--period', type=int, default=5, choices=[1,5,15,30,60])
    ap.add_argument('--tail', type=int, default=60)
    args = ap.parse_args()

    df = ak.futures_zh_minute_sina(symbol=args.contract, period=str(args.period))
    out = compute_indicators(df)

    with pd.option_context('display.max_columns', 50, 'display.width', 200):
        print(out.tail(args.tail))


if __name__ == '__main__':
    main()
