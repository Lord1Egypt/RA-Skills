from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import strategy_engine as engine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate reminders and evaluate the strategy without changing account state.")
    parser.add_argument("fund_code", help="Fund code.")
    parser.add_argument("--account-id", default="main", help="Strategy account id. Default: main")
    parser.add_argument("--db", default=str(engine.DEFAULT_DB_PATH), help=f"SQLite path. Default: {engine.DEFAULT_DB_PATH}")
    parser.add_argument("--refresh", action="store_true", help="Refresh fund market data before evaluation.")
    parser.add_argument("--date", help="Evaluation date in YYYY-MM-DD. Default: today in Asia/Shanghai.")
    parser.add_argument("--time", help="Trade time in HH:MM. Default: current time in Asia/Shanghai.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    db_path = Path(args.db)
    now = engine.shanghai_now()
    as_of_date = date.fromisoformat(args.date) if args.date else now.date()
    trade_time = args.time or now.strftime("%H:%M")

    with engine.connect_db(db_path) as connection:
        decision = engine.evaluate_strategy(
            connection,
            account_id=args.account_id,
            fund_code=args.fund_code,
            as_of_date=as_of_date,
            trade_time_local=trade_time,
            refresh=args.refresh,
        )
        print(engine.format_account_summary(decision.get("account"), decision))
        print("说明: 此命令只生成提醒和策略建议，不会修改 cash_pool、持仓份额或交易流水。")
        print("如需真正执行建议动作，请在确认后运行 confirm_strategy_action.py 或 record_strategy_trade.py。")
        connection.commit()


if __name__ == "__main__":
    main()
