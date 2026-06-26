# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "pandas>=2.2.3",
#   "pyarrow>=16.1.0",
#   "python-dotenv>=1.0.1",
#   "tushare>=1.4.24",
# ]
# ///
"""AMtkSkill query — query local A-share Parquet/CSV data.

Usage:
  uv run scripts/query.py overview
  uv run scripts/query.py stock-info --keyword 银行
  uv run scripts/query.py daily --ts-code 000001.SZ [--start-date ...] [--end-date ...]
  uv run scripts/query.py full --ts-code 000001.SZ
  uv run scripts/query.py cross-section --date 20260417 [--sort-by amount] [--limit 20]
  uv run scripts/query.py top-movers --date 20260417 [--direction up] [--limit 10]
  uv run scripts/query.py valuation --metric pe [--date 20260417] [--limit 10]
  uv run scripts/query.py industry [--date 20260417]
"""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))


def cmd_overview(args):
    from query import data_overview
    print(data_overview().to_string(index=False))


def cmd_stock_info(args):
    from query import search_stocks
    result = search_stocks(keyword=args.keyword, industry=args.industry, exchange=args.exchange)
    if result.empty:
        print("No stocks found.")
        return
    cols = [c for c in ["ts_code", "name", "industry", "market", "exchange", "list_status"] if c in result.columns]
    print(result[cols].to_string(index=False))


def cmd_daily(args):
    from query import load_market_daily
    df = load_market_daily(args.ts_code, args.start_date, args.end_date)
    if df.empty:
        print(f"No data for {args.ts_code}.")
        return
    print(df.tail(args.tail).to_string(index=False))


def cmd_full(args):
    from query import load_full_daily
    df = load_full_daily(args.ts_code, args.start_date, args.end_date)
    if df.empty:
        print(f"No data for {args.ts_code}.")
        return
    print(df.tail(args.tail).to_string(index=False))


def cmd_cross_section(args):
    from query import cross_section
    df = cross_section(args.date, sort_by=args.sort_by, limit=args.limit)
    if df.empty:
        print(f"No data for {args.date}.")
        return
    print(df.to_string(index=False))


def cmd_top_movers(args):
    from query import top_movers
    df = top_movers(args.date, direction=args.direction, limit=args.limit)
    if df.empty:
        print(f"No data for {args.date}.")
        return
    print(df.to_string(index=False))


def cmd_valuation(args):
    from query import load_daily_basic, load_stock_basic, latest_trading_date
    date = args.date or latest_trading_date()
    if not date:
        print("Error: no data available. Run fetch init first.", file=sys.stderr)
        sys.exit(1)
    db = load_daily_basic(start_date=date, end_date=date)
    if db.empty:
        print(f"No valuation data for {date}.")
        return
    metric = args.metric
    if metric in ("pe", "pb"):
        db = db[db[metric] > 0].nsmallest(args.limit, metric)
    elif metric == "total_mv":
        db = db.nlargest(args.limit, metric)
    elif metric == "turnover_rate":
        db = db.nlargest(args.limit, metric)
    else:
        print(f"Error: --metric must be one of: pe, pb, total_mv, turnover_rate. Got: {metric}", file=sys.stderr)
        sys.exit(1)
    try:
        sb = load_stock_basic(list_status=None)
        db = db.merge(sb[["ts_code", "name", "industry"]], on="ts_code", how="left")
    except RuntimeError:
        pass
    cols = [c for c in ["ts_code", "name", "industry", metric, "pe", "pb", "total_mv"] if c in db.columns]
    print(db[cols].to_string(index=False))


def cmd_industry(args):
    from query import load_daily_basic, load_stock_basic, latest_trading_date
    date = args.date or latest_trading_date()
    if not date:
        print("Error: no data available. Run fetch init first.", file=sys.stderr)
        sys.exit(1)
    db = load_daily_basic(start_date=date, end_date=date)
    try:
        sb = load_stock_basic(list_status=None)
    except RuntimeError:
        print("Error: no stock_basic CSV found.", file=sys.stderr)
        sys.exit(1)
    merged = db.merge(sb[["ts_code", "industry"]], on="ts_code", how="left")
    stats = merged.groupby("industry").agg(
        avg_pe=("pe", "mean"), avg_pb=("pb", "mean"),
        total_mv=("total_mv", "sum"), count=("ts_code", "count"),
    ).round(2).sort_values("total_mv", ascending=False)
    print(stats.head(args.limit).to_string())


def build_parser():
    parser = argparse.ArgumentParser(description="AMtkSkill query — query local A-share data.")
    sub = parser.add_subparsers(dest="action", required=True)

    sub.add_parser("overview", help="Data overview: row counts, date ranges, stock counts.")

    p = sub.add_parser("stock-info", help="Search stocks.")
    p.add_argument("--keyword", default=None, help="Search by name, code, or pinyin.")
    p.add_argument("--industry", default=None, help="Filter by industry.")
    p.add_argument("--exchange", default=None, help="SSE / SZSE / BSE.")

    p = sub.add_parser("daily", help="Daily OHLCV for a stock.")
    p.add_argument("--ts-code", required=True, help="Stock code, e.g. 000001.SZ.")
    p.add_argument("--start-date", default=None, help="YYYYMMDD.")
    p.add_argument("--end-date", default=None, help="YYYYMMDD.")
    p.add_argument("--tail", type=int, default=20, help="Show last N rows (default: 20).")

    p = sub.add_parser("full", help="Daily + valuation + adj_factor for a stock.")
    p.add_argument("--ts-code", required=True)
    p.add_argument("--start-date", default=None)
    p.add_argument("--end-date", default=None)
    p.add_argument("--tail", type=int, default=20)

    p = sub.add_parser("cross-section", help="All stocks for a given date.")
    p.add_argument("--date", required=True, help="YYYYMMDD.")
    p.add_argument("--sort-by", default="amount")
    p.add_argument("--limit", type=int, default=20)

    p = sub.add_parser("top-movers", help="Top gainers/losers.")
    p.add_argument("--date", required=True, help="YYYYMMDD.")
    p.add_argument("--direction", default="up", choices=["up", "down"])
    p.add_argument("--limit", type=int, default=10)

    p = sub.add_parser("valuation", help="Valuation ranking (PE/PB/market cap/turnover).")
    p.add_argument("--metric", required=True, choices=["pe", "pb", "total_mv", "turnover_rate"])
    p.add_argument("--date", default=None, help="YYYYMMDD (default: latest).")
    p.add_argument("--limit", type=int, default=10)

    p = sub.add_parser("industry", help="Industry average valuation.")
    p.add_argument("--date", default=None, help="YYYYMMDD (default: latest).")
    p.add_argument("--limit", type=int, default=20)

    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    handlers = {
        "overview": cmd_overview,
        "stock-info": cmd_stock_info,
        "daily": cmd_daily,
        "full": cmd_full,
        "cross-section": cmd_cross_section,
        "top-movers": cmd_top_movers,
        "valuation": cmd_valuation,
        "industry": cmd_industry,
    }
    try:
        handlers[args.action](args)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
