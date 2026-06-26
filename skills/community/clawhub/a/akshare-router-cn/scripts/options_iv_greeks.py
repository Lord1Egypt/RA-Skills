#!/usr/bin/env python3
import argparse
import akshare as ak
import pandas as pd

from _lib import kv_df_to_dict, normalize_greeks_kv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--underlying', default='510050', help='510050(50ETF) or 510300(300ETF)')
    ap.add_argument('--trade_date', default=None, help='YYYYMM，如 202603；不填则取最近月')
    ap.add_argument('--n', type=int, default=10, help='抓取前 N 个合约（MVP）')
    args = ap.parse_args()

    # pick trade_date
    if args.trade_date is None:
        sym = '50ETF' if args.underlying == '510050' else '300ETF'
        months = ak.option_sse_list_sina(symbol=sym)
        args.trade_date = months[0]

    call_df = ak.option_sse_codes_sina(symbol='看涨期权', trade_date=args.trade_date, underlying=args.underlying)
    put_df = ak.option_sse_codes_sina(symbol='看跌期权', trade_date=args.trade_date, underlying=args.underlying)

    codes = []
    if '期权代码' in call_df.columns:
        codes += call_df['期权代码'].astype(str).head(args.n//2).tolist()
    if '期权代码' in put_df.columns:
        codes += put_df['期权代码'].astype(str).head(args.n - len(codes)).tolist()

    rows = []
    for code in codes:
        gdf = ak.option_sse_greeks_sina(symbol=code)
        kv = kv_df_to_dict(gdf)
        norm = normalize_greeks_kv(kv)
        norm['sina_code'] = code
        rows.append(norm)

    out = pd.DataFrame(rows)
    cols = ['sina_code','name','trade_code','strike','price_last','iv','delta','gamma','theta','vega','volume','theo_value']
    cols = [c for c in cols if c in out.columns]

    with pd.option_context('display.max_columns', 50, 'display.width', 200):
        print(f"underlying={args.underlying} trade_date={args.trade_date}")
        print(out[cols])


if __name__ == '__main__':
    main()
