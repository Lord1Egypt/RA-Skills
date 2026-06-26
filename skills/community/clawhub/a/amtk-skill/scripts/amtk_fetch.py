# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "pandas>=2.2.3",
#   "pyarrow>=16.1.0",
#   "python-dotenv>=1.0.1",
#   "tushare>=1.4.24",
#   "openpyxl>=3.1.5",
# ]
# ///
"""AMtkSkill fetch — pull A-share data from Tushare into local Parquet/CSV files.

Usage (run from project root):
  uv run skills/amtk-skill/scripts/amtk_fetch.py init [--start-date YYYYMMDD] [--end-date YYYYMMDD] [--limit N]
  uv run skills/amtk-skill/scripts/amtk_fetch.py daily --end-date YYYYMMDD
  uv run skills/amtk-skill/scripts/amtk_fetch.py resume [--start-date YYYYMMDD] [--end-date YYYYMMDD]
  uv run scripts/fetch.py stock-list [--list-status L] [--exchange SSE]
  uv run scripts/fetch.py overview
"""

import argparse
import sys
from pathlib import Path

# Ensure project root is importable
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))


def cmd_init(args):
    from fetcher.pipeline import init_fetch
    init_fetch(
        start_date=args.start_date,
        end_date=args.end_date,
        sleep_seconds=args.sleep_seconds,
        batch_size=args.batch_size,
        limit=args.limit,
    )


def cmd_daily(args):
    from fetcher.pipeline import daily_update
    daily_update(
        end_date=args.end_date,
        start_date=args.start_date,
        sleep_seconds=args.sleep_seconds,
        batch_size=args.batch_size,
        limit=args.limit,
    )


def cmd_resume(args):
    cmd_init(args)


def cmd_stock_list(args):
    from fetcher.common import load_dotenv_if_needed
    from fetcher.stock_basic import fetch_and_save_stock_basic
    load_dotenv_if_needed(None)
    fetch_and_save_stock_basic(list_status=args.list_status, exchange=args.exchange)


def cmd_overview(args):
    from query import data_overview
    print(data_overview().to_string(index=False))


def build_parser():
    parser = argparse.ArgumentParser(
        description="AMtkSkill fetch — pull A-share data from Tushare.",
    )
    sub = parser.add_subparsers(dest="action", required=True)

    # init
    p = sub.add_parser("init", help="Full fetch with resume (first-time or continue).")
    p.add_argument("--start-date", default=None, help="Start date YYYYMMDD (default: 1 year ago).")
    p.add_argument("--end-date", default=None, help="End date YYYYMMDD (default: today).")
    p.add_argument("--sleep-seconds", type=float, default=0.5, help="Delay between API requests.")
    p.add_argument("--batch-size", type=int, default=100, help="Stocks per write batch.")
    p.add_argument("--limit", type=int, default=None, help="Fetch only N stocks (for testing).")

    # daily
    p = sub.add_parser("daily", help="Incremental daily update.")
    p.add_argument("--end-date", required=True, help="End date YYYYMMDD.")
    p.add_argument("--start-date", default=None, help="Start date YYYYMMDD (default: 1 year ago).")
    p.add_argument("--sleep-seconds", type=float, default=0.5)
    p.add_argument("--batch-size", type=int, default=100)
    p.add_argument("--limit", type=int, default=None)

    # resume
    p = sub.add_parser("resume", help="Resume interrupted fetch (alias for init).")
    p.add_argument("--start-date", default=None)
    p.add_argument("--end-date", default=None)
    p.add_argument("--sleep-seconds", type=float, default=0.5)
    p.add_argument("--batch-size", type=int, default=100)
    p.add_argument("--limit", type=int, default=None)

    # stock-list
    p = sub.add_parser("stock-list", help="Fetch stock list only.")
    p.add_argument("--list-status", default="L", help="L=listed, D=delisted, P=paused.")
    p.add_argument("--exchange", default=None, help="SSE / SZSE / BSE.")

    # overview
    sub.add_parser("overview", help="Show data overview.")

    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    handlers = {
        "init": cmd_init,
        "daily": cmd_daily,
        "resume": cmd_resume,
        "stock-list": cmd_stock_list,
        "overview": cmd_overview,
    }
    try:
        handlers[args.action](args)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
