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
    parser = argparse.ArgumentParser(description="Record a manual strategy trade or cash movement.")
    parser.add_argument("fund_code", help="Fund code.")
    parser.add_argument("--account-id", default="main", help="Strategy account id. Default: main")
    parser.add_argument("--db", default=str(engine.DEFAULT_DB_PATH), help=f"SQLite path. Default: {engine.DEFAULT_DB_PATH}")
    parser.add_argument(
        "--trade-type",
        required=True,
        choices=["cash_inflow", "cash_outflow", "manual_buy", "manual_sell"],
        help="Trade type to record.",
    )
    parser.add_argument("--gross-amount", type=float, help="Gross amount. Required for cash flows and manual_buy.")
    parser.add_argument("--price", type=float, help="Price per unit. Required for buy/sell.")
    parser.add_argument("--units", type=float, help="Units. Optional for manual_buy and manual_sell.")
    parser.add_argument("--fee-rate-pct", type=float, help="Override fee rate percentage.")
    parser.add_argument("--use-fund-rate", action="store_true", help="Use the imported fund current_rate for manual buy/sell.")
    parser.add_argument("--refresh", action="store_true", help="Refresh fund data before reading the current fund rate.")
    parser.add_argument("--trade-date", help="Trade date in YYYY-MM-DD. Default: today in Asia/Shanghai.")
    parser.add_argument("--trade-time", help="Trade time in HH:MM.")
    parser.add_argument("--note", help="Optional note.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    db_path = Path(args.db)
    now = engine.shanghai_now()
    trade_date = args.trade_date or now.date().isoformat()
    trade_time = args.trade_time or now.strftime("%H:%M")

    with engine.connect_db(db_path) as connection:
        fee_rate_pct = float(args.fee_rate_pct or 0.0)
        if args.trade_type in {"manual_buy", "manual_sell"} and (args.use_fund_rate or args.fee_rate_pct is None):
            market_state = engine.get_market_state(connection, args.fund_code, lookback_days=20, refresh=args.refresh)
            fee_rate_pct = float(market_state.get("fee_rate_pct") or 0.0)

        if args.trade_type in {"cash_inflow", "cash_outflow"}:
            if args.gross_amount is None:
                raise SystemExit("--gross-amount is required for cash_inflow and cash_outflow")
            result = engine.record_trade(
                connection,
                account_id=args.account_id,
                fund_code=args.fund_code,
                trade_date=trade_date,
                trade_time_local=trade_time,
                trade_type=args.trade_type,
                gross_amount=args.gross_amount,
                price=None,
                units=0.0,
                fee_rate_pct=0.0,
                note=args.note,
            )
        elif args.trade_type == "manual_buy":
            if args.gross_amount is None or args.price is None:
                raise SystemExit("--gross-amount and --price are required for manual_buy")
            units = args.units if args.units is not None else args.gross_amount / args.price
            result = engine.record_trade(
                connection,
                account_id=args.account_id,
                fund_code=args.fund_code,
                trade_date=trade_date,
                trade_time_local=trade_time,
                trade_type=args.trade_type,
                gross_amount=args.gross_amount,
                price=args.price,
                units=units,
                fee_rate_pct=fee_rate_pct,
                note=args.note,
            )
        else:
            if args.price is None:
                raise SystemExit("--price is required for manual_sell")
            if args.units is None and args.gross_amount is None:
                raise SystemExit("manual_sell requires --units or --gross-amount")
            units = args.units if args.units is not None else args.gross_amount / args.price
            gross_amount = args.gross_amount if args.gross_amount is not None else units * args.price
            result = engine.record_trade(
                connection,
                account_id=args.account_id,
                fund_code=args.fund_code,
                trade_date=trade_date,
                trade_time_local=trade_time,
                trade_type=args.trade_type,
                gross_amount=gross_amount,
                price=args.price,
                units=units,
                fee_rate_pct=fee_rate_pct,
                note=args.note,
            )

        connection.commit()
        account = result["account"]
        print(f"Recorded trade: {args.trade_type} for {args.account_id} / {args.fund_code}")
        print(f"cash_pool={account['cash_pool']:.2f}")
        print(f"position_units={account['position_units']:.6f}")
        print(f"avg_cost_price={account['avg_cost_price'] if account['avg_cost_price'] is not None else 'N/A'}")


if __name__ == "__main__":
    main()
