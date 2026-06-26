"""资产：查询账户资金金额  POST /api/v1/portfolio/CashSummary"""
import argparse

from _client import build_client, call_with_account_retry, dump_with_directive, run

EPILOG = """\
何时调用：
  - 用户问"余额 / 现金 / 购买力 / 还能买多少"

示例：
  # 全币种汇总
  cash_summary.py
  # 只看港币
  cash_summary.py --currency HKD
  # 调试某个具体账户
  cash_summary.py --sub-account-id 12345

注意：
  - subAccountId 默认从共享凭证缓存自动取（mock 桶第一个），不需要先跑 account_list
  - 港股购买力只看 HKD，美股只看 USD，模拟盘不自动换汇
"""


def main():
    parser = argparse.ArgumentParser(
        description="查询账户资金金额（模拟盘）",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--sub-account-id", help="证券账号；默认自动取共享凭证缓存里 mock 桶第一个")
    parser.add_argument("--currency", help="HKD / USD / CNH，不传 = 全币种汇总")
    parser.add_argument("--client-id", type=int)
    parser.add_argument("--apply-account-id")
    args = parser.parse_args()

    client = build_client()

    def factory(sub_account_id):
        return client.portfolio.get_assets_summary(
            sub_account_id=sub_account_id,
            currency=args.currency,
            client_id=args.client_id,
            apply_account_id=args.apply_account_id,
        )

    dump_with_directive(
        call_with_account_retry(client, factory, args.sub_account_id),
        next_action=(
            "已返回模拟盘资金/购买力，**先把关键数字汇报给用户、然后停手**等下一步指令。"
            "**禁止**自动接 holdings / cash_flows / order_* 等任何脚本——单步原则（第 0 条铁律）。"
        ),
    )


if __name__ == "__main__":
    run(main)
