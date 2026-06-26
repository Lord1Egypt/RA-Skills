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
    parser = argparse.ArgumentParser(description="Confirm and execute the current suggested strategy action.")
    parser.add_argument("fund_code", help="Fund code.")
    parser.add_argument("--account-id", default="main", help="Strategy account id. Default: main")
    parser.add_argument("--db", default=str(engine.DEFAULT_DB_PATH), help=f"SQLite path. Default: {engine.DEFAULT_DB_PATH}")
    parser.add_argument("--refresh", action="store_true", help="Refresh fund market data before confirmation.")
    parser.add_argument("--date", help="Evaluation date in YYYY-MM-DD. Default: today in Asia/Shanghai.")
    parser.add_argument("--time", help="Trade time in HH:MM. Default: current time in Asia/Shanghai.")
    parser.add_argument(
        "--expected-action",
        choices=["buy_dca", "buy_dip", "sell_take_profit"],
        help="Optional safety check: only execute if the suggested action matches this value.",
    )
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

        action = decision.get("action")
        if action not in {"buy_dca", "buy_dip", "sell_take_profit"}:
            print("当前没有可执行的策略动作，因此不会写入交易流水。")
            connection.commit()
            return

        if args.expected_action and action != args.expected_action:
            raise SystemExit(
                f"当前建议动作是 {action}，与 --expected-action={args.expected_action} 不一致，因此未执行。"
            )

        applied = engine.apply_strategy_decision(
            connection,
            account_id=args.account_id,
            fund_code=args.fund_code,
            decision=decision,
            note=f"confirmed:{action}",
        )
        connection.commit()

        if applied is None:
            print("策略动作未写入交易流水。")
            return

        updated_account = applied["account"]
        print("已根据你的确认写入交易流水。")
        print(f"cash_pool={updated_account['cash_pool']:.2f}")
        print(f"position_units={updated_account['position_units']:.6f}")
        print(
            f"avg_cost_price={updated_account['avg_cost_price'] if updated_account['avg_cost_price'] is not None else 'N/A'}"
        )


if __name__ == "__main__":
    main()
