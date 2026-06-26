"""交易：资金流水  POST /api/v1/trade/CashFlows"""
import argparse

from _client import (
    build_client,
    call_with_account_retry,
    dump_with_directive,
    ensure_sim_sub_account_class,
    run,
)

EPILOG = """\
何时调用：
  - 用户问"流水 / 出入金 / 资金变动 / 今天买卖了什么"

示例：
  # 默认全部
  cash_flows.py
  # 单日
  cash_flows.py --date 2026-04-23
  # 区间
  cash_flows.py --trade-date-from 2026-04-01 --trade-date-to 2026-04-23
"""


def main():
    parser = argparse.ArgumentParser(
        description="资金流水查询（模拟盘）",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--sub-account-id")
    parser.add_argument("--apply-account-id")
    parser.add_argument(
        "--sub-account-class",
        type=int,
        help=(
            "subAccountClass：网关默认按 1=主账号；9=期权账户见 CashFlows 文档。"
            "**模拟盘 skill 禁止传 9**（本地拦截），只查正股资金流水。"
        ),
    )
    parser.add_argument("--business-type", action="append", type=int)
    parser.add_argument("--date", help="单日 YYYY-MM-DD")
    parser.add_argument("--flow-type", type=int)
    parser.add_argument("--trade-date-from")
    parser.add_argument("--trade-date-to")
    args = parser.parse_args()
    ensure_sim_sub_account_class(args.sub_account_class)

    client = build_client()

    def factory(sub_account_id):
        return client.trade.get_cash_flows(
            sub_account_id=sub_account_id,
            apply_account_id=args.apply_account_id,
            sub_account_class=args.sub_account_class,
            business_type=args.business_type,
            date=args.date,
            flow_type=args.flow_type,
            trade_date_from=args.trade_date_from,
            trade_date_to=args.trade_date_to,
        )

    dump_with_directive(
        call_with_account_retry(client, factory, args.sub_account_id),
        next_action=(
            "已返回模拟盘资金流水，**先汇报给用户、然后停手**等下一步指令。"
            "**禁止**自动接 cash_summary / holdings / order_* 等任何脚本——单步原则（第 0 条铁律）。"
        ),
    )


if __name__ == "__main__":
    run(main)
