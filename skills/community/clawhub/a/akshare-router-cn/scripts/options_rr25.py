#!/usr/bin/env python3
import argparse
import akshare as ak
import pandas as pd

from _lib import kv_df_to_dict, normalize_greeks_kv


def fetch_side(trade_date, underlying, side):
    df = ak.option_sse_codes_sina(symbol=side, trade_date=trade_date, underlying=underlying)
    if '期权代码' not in df.columns:
        raise ValueError(f"Unexpected columns from option_sse_codes_sina: {list(df.columns)}")
    codes = df['期权代码'].astype(str).tolist()
    rows = []
    for code in codes:
        gdf = ak.option_sse_greeks_sina(symbol=code)
        kv = kv_df_to_dict(gdf)
        norm = normalize_greeks_kv(kv)
        norm['sina_code'] = code
        rows.append(norm)
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--underlying', default='510050')
    ap.add_argument('--trade_date', default=None)
    args = ap.parse_args()

    if args.trade_date is None:
        sym = '50ETF' if args.underlying == '510050' else '300ETF'
        args.trade_date = ak.option_sse_list_sina(symbol=sym)[0]

    call = fetch_side(args.trade_date, args.underlying, '看涨期权')
    put = fetch_side(args.trade_date, args.underlying, '看跌期权')

    # clean
    call = call.dropna(subset=['delta','iv'])
    put = put.dropna(subset=['delta','iv'])

    call['dist'] = (call['delta'] - 0.25).abs()
    put['dist'] = (put['delta'] + 0.25).abs()

    c = call.sort_values('dist').head(1).iloc[0].to_dict() if len(call) else None
    p = put.sort_values('dist').head(1).iloc[0].to_dict() if len(put) else None

    if not c or not p:
        raise SystemExit('Not enough data to compute RR25')

    rr25 = c['iv'] - p['iv']

    print(f"underlying={args.underlying} trade_date={args.trade_date}")
    print(f"RR25 = iv_call25({c['iv']}) - iv_put25({p['iv']}) = {rr25}")
    print('\nCALL (+0.25Δ) chosen:')
    for k in ['sina_code','trade_code','name','strike','price_last','delta','iv','volume']:
        if k in c:
            print(f"  {k}: {c[k]}")
    print('\nPUT (-0.25Δ) chosen:')
    for k in ['sina_code','trade_code','name','strike','price_last','delta','iv','volume']:
        if k in p:
            print(f"  {k}: {p[k]}")


if __name__ == '__main__':
    main()
