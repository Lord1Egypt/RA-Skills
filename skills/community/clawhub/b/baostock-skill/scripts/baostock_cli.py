#!/usr/bin/env python3
"""
BaoStock CLI for OpenClaw skill
"""

import sys
import json
import argparse
import datetime
from pathlib import Path

try:
    import baostock as bs
    import pandas as pd
except ImportError as e:
    print(json.dumps({"error": f"Missing dependency: {e}. Install: pip3 install baostock"}), file=sys.stderr)
    sys.exit(1)

def login():
    """Login to BaoStock (no credentials needed for basic data)."""
    lg = bs.login()
    if lg.error_code != '0':
        raise RuntimeError(f"BaoStock login failed: {lg.error_msg}")
    return lg

def format_symbol(symbol: str) -> str:
    """Ensure symbol has proper BaoStock format: sh.600519 or sz.000001."""
    if '.' in symbol:
        return symbol  # already correct
    if symbol.startswith(("sh", "sz", "bj")):
        return f"{symbol[0:2]}.{symbol[2:]}"  # convert sh600519 -> sh.600519
    if symbol.isdigit() and len(symbol) == 6:
        if symbol.startswith(("60", "68", "688")):
            return f"sh.{symbol}"
        elif symbol.startswith(("00", "30")):
            return f"sz.{symbol}"
        elif symbol.startswith(("43", "83", "89")):
            return f"bj.{symbol}"
    return symbol  # fallback

def cmd_quote(args):
    """Real-time quote for a symbol (using latest daily data)."""
    symbol = format_symbol(args.symbol)
    end_date = datetime.date.today().strftime("%Y-%m-%d")
    start_date = (datetime.date.today() - datetime.timedelta(days=5)).strftime("%Y-%m-%d")

    lg = login()
    try:
        # Query recent daily data; take latest
        rs = bs.query_history_k_data_plus(
            symbol,
            "date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg,isST,tradestatus",
            start_date=start_date,
            end_date=end_date,
            frequency="d",
            adjustflag="3"
        )
        if rs.error_code != '0':
            raise RuntimeError(rs.error_msg)
        data_list = []
        while (rs.next()):
            data_list.append(rs.get_row_data())
        if not data_list:
            return {"error": "No data found"}

        # Get the latest row
        row = data_list[-1]
        result = {
            "symbol": symbol,
            "date": row[0],
            "code": row[1],
            "open": float(row[2]),
            "high": float(row[3]),
            "low": float(row[4]),
            "close": float(row[5]),
            "volume": float(row[6]),
            "amount": float(row[7]),
            "adjustflag": row[8],
            "turnover": float(row[9]) if row[9] else None,
            "pct_change": float(row[10]),
            "isST": row[11],
            "tradestatus": row[12],
        }
        result["price"] = result["close"]
        result["change"] = result["close"] * result["pct_change"] / 100
        return result
    finally:
        bs.logout()

def cmd_history(args):
    """Historical data."""
    symbol = format_symbol(args.symbol)
    start_date = args.start_date
    end_date = args.end_date or datetime.date.today().strftime("%Y-%m-%d")
    frequency = args.frequency  # "d", "w", "m", "5", "15", "30", "60"

    # For minute data, keep YYYY-MM-DD format; for daily, BaoStock accepts both
    # For simplicity, keep as-is (BaoStock handles both)
    # But minute data queries need YYYY-MM-DD
    pass

    # Determine fields based on frequency
    if frequency in ("5", "15", "30", "60"):
        # 分钟线字段：time,open,high,low,close,volume,amount
        fields = "time,open,high,low,close,volume,amount"
    else:
        # 日线/周线/月线字段
        fields = "date,open,high,low,close,volume,amount,adjustflag,turn,pctChg"

    lg = login()
    try:
        rs = bs.query_history_k_data_plus(
            symbol,
            fields,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            adjustflag="3"
        )
        if rs.error_code != '0':
            raise RuntimeError(rs.error_msg)
        data_list = []
        while (rs.next()):
            data_list.append(rs.get_row_data())
        # Convert to records, handling NaN and dates
        cols = fields.split(',')
        records = []
        for row in data_list:
            rec = {}
            for col, val in zip(cols, row):
                if not val or val == '':
                    rec[col] = None
                elif col in ('date', 'time'):
                    rec[col] = str(val)
                else:
                    try:
                        fval = float(val)
                        rec[col] = fval
                    except (ValueError, TypeError):
                        rec[col] = val
            records.append(rec)
        return records
    finally:
        bs.logout()

def cmd_stock_list(args):
    """List all A-shares."""
    lg = login()
    try:
        rs = bs.query_stock_basic()
        if rs.error_code != '0':
            raise RuntimeError(rs.error_msg)
        data_list = []
        while (rs.next()):
            data_list.append(rs.get_row_data())
        cols = ["code","code_name","ipoDate","outDate","type","status"]
        result = []
        for row in data_list:
            result.append(dict(zip(cols, row)))
        return result
    finally:
        bs.logout()

def cmd_index_history(args):
    """Index historical data."""
    symbol = format_symbol(args.symbol)
    start_date = args.start_date
    end_date = args.end_date or datetime.date.today().strftime("%Y-%m-%d")
    frequency = args.frequency or "d"

    if '-' in start_date:
        start_date = start_date.replace('-', '')
    if '-' in end_date:
        end_date = end_date.replace('-', '')

    lg = login()
    try:
        rs = bs.query_history_k_data_plus(
            symbol,
            "date,open,high,low,close,volume,amount,pctChg",
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            adjustflag="3"
        )
        if rs.error_code != '0':
            raise RuntimeError(rs.error_msg)
        data_list = []
        while (rs.next()):
            data_list.append(rs.get_row_data())
        cols = ["date","open","high","low","close","volume","amount","pctChg"]
        result = []
        for row in data_list:
            item = {}
            for col, val in zip(cols, row):
                if not val:
                    item[col] = None
                elif col == "date":
                    item[col] = str(val)
                else:
                    try:
                        item[col] = float(val)
                    except:
                        item[col] = val
            result.append(item)
        return result
    finally:
        bs.logout()

def main():
    parser = argparse.ArgumentParser(description="BaoStock CLI for OpenClaw")
    parser.add_argument("--symbol", help="Stock or index symbol (e.g., sh600519)")
    parser.add_argument("--type", choices=["quote", "history", "stock-list", "index-history"], help="Query type")
    parser.add_argument("--start-date", default=(datetime.date.today() - datetime.timedelta(days=7)).strftime("%Y-%m-%d"), help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="End date (YYYY-MM-DD), default today")
    parser.add_argument("--frequency", default="d", choices=["d","w","m","5","15","30","60"], help="Data frequency: d=day, w=week, m=month, 5=5min etc.")
    parser.add_argument("--output", "-o", help="Output JSON file (default stdout)")

    args = parser.parse_args()

    if not args.type:
        parser.error("--type is required")

    try:
        if args.type == "quote":
            result = cmd_quote(args)
        elif args.type == "history":
            result = cmd_history(args)
        elif args.type == "stock-list":
            result = cmd_stock_list(args)
        elif args.type == "index-history":
            result = cmd_index_history(args)
        else:
            raise ValueError(f"Unknown type: {args.type}")
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    output_json = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(output_json, encoding="utf-8")
        print(f"Data written to {args.output}, records: {len(result) if isinstance(result, list) else 1}")
    else:
        print(output_json)

if __name__ == "__main__":
    main()