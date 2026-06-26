# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "pandas>=2.2.3",
#   "pyarrow>=16.1.0",
#   "python-dotenv>=1.0.1",
#   "tushare>=1.4.24",
# ]
# ///
"""AMtkSkill analyze — technical analysis on local A-share data.

Usage:
  uv run scripts/analyze.py ma --ts-code 000001.SZ [--windows 5,10,20,60]
  uv run scripts/analyze.py rsi --ts-code 000001.SZ [--period 14]
  uv run scripts/analyze.py macd --ts-code 000001.SZ
  uv run scripts/analyze.py bollinger --ts-code 000001.SZ [--window 20]
  uv run scripts/analyze.py adjusted --ts-code 000001.SZ [--method forward]
  uv run scripts/analyze.py stats --ts-code 000001.SZ
  uv run scripts/analyze.py corporate-actions --ts-code 000001.SZ
  uv run scripts/analyze.py compare --ts-codes 000001.SZ,600519.SH,000858.SZ
"""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))


def cmd_ma(args):
    from analysis import moving_average
    windows = [int(w) for w in args.windows.split(",")]
    df = moving_average(args.ts_code, windows=windows, start_date=args.start_date, end_date=args.end_date)
    if df.empty:
        print(f"No data for {args.ts_code}.")
        return
    cols = ["trade_date", "close"] + [f"ma{w}" for w in windows]
    print(df[cols].tail(args.tail).to_string(index=False))


def cmd_rsi(args):
    from analysis import rsi
    df = rsi(args.ts_code, period=args.period, start_date=args.start_date, end_date=args.end_date)
    if df.empty:
        print(f"No data for {args.ts_code}.")
        return
    print(df[["trade_date", "close", "rsi"]].tail(args.tail).to_string(index=False))


def cmd_macd(args):
    from analysis import macd
    df = macd(args.ts_code, fast=args.fast, slow=args.slow, signal=args.signal,
              start_date=args.start_date, end_date=args.end_date)
    if df.empty:
        print(f"No data for {args.ts_code}.")
        return
    print(df[["trade_date", "close", "macd", "macd_signal", "macd_hist"]].tail(args.tail).to_string(index=False))


def cmd_bollinger(args):
    from analysis import bollinger_bands
    df = bollinger_bands(args.ts_code, window=args.window, num_std=args.num_std,
                         start_date=args.start_date, end_date=args.end_date)
    if df.empty:
        print(f"No data for {args.ts_code}.")
        return
    print(df[["trade_date", "close", "bb_upper", "bb_mid", "bb_lower"]].tail(args.tail).to_string(index=False))


def cmd_adjusted(args):
    if args.method == "forward":
        from analysis import forward_adjusted_prices
        df = forward_adjusted_prices(args.ts_code, start_date=args.start_date, end_date=args.end_date)
    else:
        from analysis import backward_adjusted_prices
        df = backward_adjusted_prices(args.ts_code, start_date=args.start_date, end_date=args.end_date)
    if df.empty:
        print(f"No data for {args.ts_code}.")
        return
    cols = ["trade_date", "close"]
    if "close_adj" in df.columns:
        cols.append("close_adj")
    if "adj_factor" in df.columns:
        cols.append("adj_factor")
    print(df[cols].tail(args.tail).to_string(index=False))


def cmd_stats(args):
    from analysis import price_statistics
    stats = price_statistics(args.ts_code, start_date=args.start_date, end_date=args.end_date)
    if not stats:
        print(f"No data for {args.ts_code}.")
        return
    for k, v in stats.items():
        print(f"{k}: {v}")


def cmd_corporate_actions(args):
    from analysis import detect_corporate_actions
    df = detect_corporate_actions(args.ts_code, start_date=args.start_date, end_date=args.end_date)
    if df.empty:
        print("No corporate actions detected.")
        return
    print(df.to_string(index=False))


def cmd_compare(args):
    from analysis import price_statistics
    codes = [c.strip() for c in args.ts_codes.split(",")]
    for code in codes:
        stats = price_statistics(code, start_date=args.start_date, end_date=args.end_date)
        if stats:
            print(f"{stats['ts_code']:12s} "
                  f"return={stats['total_return_pct']:>7.2f}%  "
                  f"vol={stats['annualized_volatility_pct']:>6.2f}%  "
                  f"drawdown={stats['max_drawdown_pct']:>7.2f}%  "
                  f"sharpe={stats['sharpe_ratio']:>6.4f}")
        else:
            print(f"{code:12s} No data")


def add_common_args(p):
    p.add_argument("--ts-code", required=True, help="Stock code, e.g. 000001.SZ.")
    p.add_argument("--start-date", default=None, help="YYYYMMDD.")
    p.add_argument("--end-date", default=None, help="YYYYMMDD.")
    p.add_argument("--tail", type=int, default=20, help="Show last N rows (default: 20).")


def build_parser():
    parser = argparse.ArgumentParser(description="AMtkSkill analyze — technical analysis on A-share data.")
    sub = parser.add_subparsers(dest="action", required=True)

    p = sub.add_parser("ma", help="Moving averages.")
    add_common_args(p)
    p.add_argument("--windows", default="5,10,20,60", help="Comma-separated window sizes.")

    p = sub.add_parser("rsi", help="Relative Strength Index.")
    add_common_args(p)
    p.add_argument("--period", type=int, default=14)

    p = sub.add_parser("macd", help="MACD indicator.")
    add_common_args(p)
    p.add_argument("--fast", type=int, default=12)
    p.add_argument("--slow", type=int, default=26)
    p.add_argument("--signal", type=int, default=9)

    p = sub.add_parser("bollinger", help="Bollinger Bands.")
    add_common_args(p)
    p.add_argument("--window", type=int, default=20)
    p.add_argument("--num-std", type=float, default=2.0)

    p = sub.add_parser("adjusted", help="Adjusted prices.")
    add_common_args(p)
    p.add_argument("--method", default="forward", choices=["forward", "backward"])

    p = sub.add_parser("stats", help="Return / volatility / drawdown / Sharpe.")
    p.add_argument("--ts-code", required=True)
    p.add_argument("--start-date", default=None)
    p.add_argument("--end-date", default=None)

    p = sub.add_parser("corporate-actions", help="Detect dividends and splits.")
    p.add_argument("--ts-code", required=True)
    p.add_argument("--start-date", default=None)
    p.add_argument("--end-date", default=None)

    p = sub.add_parser("compare", help="Compare stats across multiple stocks.")
    p.add_argument("--ts-codes", required=True, help="Comma-separated codes.")
    p.add_argument("--start-date", default=None)
    p.add_argument("--end-date", default=None)

    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    handlers = {
        "ma": cmd_ma,
        "rsi": cmd_rsi,
        "macd": cmd_macd,
        "bollinger": cmd_bollinger,
        "adjusted": cmd_adjusted,
        "stats": cmd_stats,
        "corporate-actions": cmd_corporate_actions,
        "compare": cmd_compare,
    }
    try:
        handlers[args.action](args)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
