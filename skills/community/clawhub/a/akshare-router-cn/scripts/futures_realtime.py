#!/usr/bin/env python3
import argparse
import akshare as ak
import pandas as pd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--symbol', default='PTA', help='品种名称，如 PTA；可用 ak.futures_symbol_mark() 查询')
    ap.add_argument('--top', type=int, default=10)
    args = ap.parse_args()

    df = ak.futures_zh_realtime(symbol=args.symbol)
    print(f"rows={len(df)} cols={list(df.columns)}")

    # Best-effort: try common volume/oi columns
    vol_cols = [c for c in df.columns if '成交' in c or '成交量' in c or c.lower() in ('volume',)]
    oi_cols = [c for c in df.columns if '持仓' in c or '持仓量' in c or c.lower() in ('open_interest','oi')]

    sort_col = (vol_cols[0] if vol_cols else (oi_cols[0] if oi_cols else None))
    if sort_col:
        sdf = df.copy()
        sdf[sort_col] = pd.to_numeric(sdf[sort_col], errors='coerce')
        sdf = sdf.sort_values(sort_col, ascending=False).head(args.top)
    else:
        sdf = df.head(args.top)

    # print compact
    with pd.option_context('display.max_columns', 50, 'display.width', 200):
        print(sdf)


if __name__ == '__main__':
    main()
