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
    parser = argparse.ArgumentParser(description="Create, update, or inspect a strategy account state.")
    parser.add_argument("--db", default=str(engine.DEFAULT_DB_PATH), help=f"SQLite path. Default: {engine.DEFAULT_DB_PATH}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    upsert = subparsers.add_parser("upsert", help="Create or overwrite the stored strategy account state.")
    upsert.add_argument("fund_code", help="Fund code.")
    upsert.add_argument("--account-id", default="main", help="Strategy account id. Default: main")
    upsert.add_argument("--fund-type", default="equity_fund", help="Fund type. Default: equity_fund")
    upsert.add_argument("--cash-pool", type=float, required=True, help="Current cash_pool amount.")
    upsert.add_argument("--position-units", type=float, default=0.0, help="Current position units.")
    upsert.add_argument("--avg-cost-price", type=float, help="Average holding cost price.")
    upsert.add_argument("--note", help="Optional note.")
    upsert.add_argument("--refresh", action="store_true", help="Refresh fund market data before saving.")

    show = subparsers.add_parser("show", help="Show the current account state and current strategy action.")
    show.add_argument("fund_code", help="Fund code.")
    show.add_argument("--account-id", default="main", help="Strategy account id. Default: main")
    show.add_argument("--refresh", action="store_true", help="Refresh fund market data before showing.")
    show.add_argument("--date", help="Override evaluation date in YYYY-MM-DD.")
    show.add_argument("--time", help="Override local trade time in HH:MM.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    db_path = Path(args.db)

    with engine.connect_db(db_path) as connection:
        if args.command == "upsert":
            if args.refresh:
                engine.ensure_market_snapshot(connection, args.fund_code, refresh=True)
            account = engine.upsert_account(
                connection,
                args.account_id,
                args.fund_code,
                fund_type=args.fund_type,
                cash_pool=args.cash_pool,
                position_units=args.position_units,
                avg_cost_price=args.avg_cost_price,
                note=args.note,
            )
            connection.commit()
            print(f"Saved strategy account: {account['account_id']} / {account['fund_code']}")
            print(f"cash_pool={account['cash_pool']:.2f}")
            print(f"position_units={account['position_units']:.6f}")
            print(f"avg_cost_price={account['avg_cost_price'] if account['avg_cost_price'] is not None else 'N/A'}")
            return

        now = engine.shanghai_now()
        as_of_date = date.fromisoformat(args.date) if args.date else now.date()
        trade_time = args.time or now.strftime("%H:%M")
        decision = engine.evaluate_strategy(
            connection,
            account_id=args.account_id,
            fund_code=args.fund_code,
            as_of_date=as_of_date,
            trade_time_local=trade_time,
            refresh=args.refresh,
        )
        print(engine.format_account_summary(decision.get("account"), decision))


if __name__ == "__main__":
    main()
