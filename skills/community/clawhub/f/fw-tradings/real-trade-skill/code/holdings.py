"""资产：当前持仓  POST /api/v1/portfolio/Holdings"""
import argparse

from _client import (
    build_client,
    call_with_account_retry,
    dump_with_directive,
    ensure_sim_sub_account_class,
    ensure_sim_trade_product_types,
    normalize_codes_inplace,
    run,
)

EPILOG = """\
何时调用：
  - 用户问"持仓 / 我买了什么 / 现在有什么股票"

示例：
  # 全部持仓
  holdings.py
  # 只看港股
  holdings.py --product-types 5
  # 只看美股
  holdings.py --product-types 6
  # 只看某只
  holdings.py --symbols hk00700
"""


def main():
    parser = argparse.ArgumentParser(
        description="查询当前持仓（实盘）",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--sub-account-id")
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument(
        "--product-types", action="append", type=int,
        help="产品类型（可多次传）：5=港股 6=美股 7=A股 15=期权",
    )
    parser.add_argument("--currencies", action="append")
    parser.add_argument(
        "--symbols", "--code", "--stock-code", "--symbol",
        action="append",
        help=(
            "标的过滤（v1.7.5 起支持「用户原话格式」自动规范化：`00700` → `hk00700`、`AAPL` → `usAAPL`，可多次传）；"
            "alias 接受 --code/--stock-code/--symbol（抗参数名脑补）"
        ),
    )
    parser.add_argument("--use-us-pre", action="store_true")
    parser.add_argument("--use-us-post", action="store_true")
    parser.add_argument("--use-us-night", action="store_true")
    parser.add_argument("--client-id", type=int)
    parser.add_argument("--apply-account-id")
    parser.add_argument("--sub-account-class", type=int)
    args = parser.parse_args()
    normalize_codes_inplace(args, "symbols")
    ensure_sim_trade_product_types(args.product_types)
    ensure_sim_sub_account_class(args.sub_account_class)

    client = build_client()

    def factory(sub_account_id):
        return client.portfolio.get_holdings(
            sub_account_id=sub_account_id,
            start=args.start,
            count=args.count,
            product_types=args.product_types,
            currencies=args.currencies,
            symbols=args.symbols,
            use_us_pre=args.use_us_pre,
            use_us_post=args.use_us_post,
            use_us_night=args.use_us_night,
            client_id=args.client_id,
            apply_account_id=args.apply_account_id,
            sub_account_class=args.sub_account_class,
        )

    dump_with_directive(
        call_with_account_retry(client, factory, args.sub_account_id),
        next_action=(
            "已返回实盘持仓，**先把关键标的+数量+市值汇报给用户、然后停手**等下一步指令。"
            "**禁止**自动接 cash_summary / cash_flows / order_* 等任何脚本——单步原则（第 0 条铁律）。"
        ),
    )


if __name__ == "__main__":
    run(main)
