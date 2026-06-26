"""交易：查询订单列表  POST /api/v1/trade/OrderList

⚠️ 治本说明：服务端实际强制要求 fromDate/toDate（与文档"不传则默认查询最近7天"不符），
本脚本在用户未显式指定时自动补默认日期范围（今日往前 7 天），匹配文档语义。
"""
import argparse
from datetime import date, timedelta

from _client import (
    StructuredScriptError,
    build_client,
    call_with_account_retry,
    dump,
    ensure_sim_trade_markets,
    ensure_sim_trade_show_type,
    normalize_codes_inplace,
    run,
)

# 「未成交」语义：报送中 + 已报 + 部成（部分成交里仍有未成交部分）
# 与 TESTING.md 6.5「未成交（status 10/20/22/23/40/60）」保持一致。
ACTIVE_STATUS_CODES = [10, 20, 22, 23, 40, 60]

EPILOG = """\
何时调用：
  - 用户问"今天的订单 / 委托记录 / 哪些订单还没成"

示例：
  # 默认 7 天内全部订单
  order_list.py
  # 只看某只股票最近订单
  order_list.py --stock-code AAPL --market us
  # 只看“还没成”的订单（报送中+已报+部成；与 --status-arr 互斥）
  order_list.py --active-only
  # 只看港股
  order_list.py --market hk
  # 自定义日期
  order_list.py --from-date 2026-04-01 --to-date 2026-04-23

订单状态码（正股常用）：
  10/20/22/23 = 报送/待处理链    40 = 已报      50 = 全成
  60 = 部成    70 = 已撤   80 = 部撤      90 = 废单    100 = 已失效
  服务端通用枚举还可能返回 21/71/91/101/901；模拟盘新下单仍只支持限价单/市价单

注意：
  - 服务端对 Count 字段强校验。脚本默认 count=20；若报 APIERROR_50001，加 --count 50 重试
  - 本脚本**不支持** `--order-id` 直接过滤。要确认某笔单，先用 `--stock-code` + 日期 / 市场 / 状态缩小范围，再从结果里反查 `orderId`
  - 若返回 `Session expired`，说明共享凭证里的券商会话已失效；这不是“订单不存在”，应先体检，仍失败则回同级 fosun-env-setup 修复凭证
"""


def main():
    parser = argparse.ArgumentParser(
        description="分页查询订单列表（模拟盘）",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--sub-account-id")
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument(
        "--stock-code", "--code", "--symbol", "--symbols",
        help=(
            "标的过滤（v1.7.5 起支持「用户原话格式」自动规范化：`00700` → `hk00700`、`AAPL` → `usAAPL`）；"
            "alias 接受 --code/--symbol/--symbols（抗参数名脑补）"
        ),
    )
    parser.add_argument("--status-arr", action="append", type=int,
                        help="按状态码过滤（可多次传）；与 --active-only 互斥")
    parser.add_argument("--active-only", action="store_true",
                        help="只看“还没成”的订单（自动展开为 status 10/20/22/23/40/60）；与 --status-arr 互斥")
    parser.add_argument("--from-date", help="开始日期 yyyy-mm-dd（默认 7 天前）")
    parser.add_argument("--to-date", help="结束日期 yyyy-mm-dd（默认今天）")
    parser.add_argument("--direction", type=int, choices=[1, 2], help="1=买 2=卖（与网关 direction 一致）")
    parser.add_argument("--market", action="append", help="可多次传：hk us")
    parser.add_argument("--sort", default="desc", choices=["desc", "asc"])
    parser.add_argument("--client-id", type=int)
    parser.add_argument("--apply-account-id")
    parser.add_argument(
        "--show-type",
        type=int,
        choices=[0, 1, 2],
        help=(
            "展示类型 showType：0=只有正股订单 1=正股和期权订单 2=只有期权订单（与 OrderList 文档一致）；"
            "模拟盘勿传 1/2，请用默认或显式 0"
        ),
    )
    args = parser.parse_args()
    normalize_codes_inplace(args, "stock_code")
    ensure_sim_trade_markets(args.market)
    ensure_sim_trade_show_type(args.show_type)

    if args.active_only and args.status_arr:
        raise StructuredScriptError(
            "`--active-only` 与 `--status-arr` 互斥：前者已固定展开为 status 10/20/22/23/40/60，再叠加 --status-arr 会让筛选语义模糊。",
            error_code="INVALID_PARAM",
            hint="同时传 `--active-only` 和 `--status-arr` 会覆盖彼此意图，无法判断你到底想看哪些状态。",
            next_action="二选一：要“还没成”的订单就只用 `--active-only`；要自定义状态组合就只用 `--status-arr`。",
            exit_code=2,
        )
    status_arr = ACTIVE_STATUS_CODES if args.active_only else args.status_arr

    client = build_client()

    today = date.today()
    from_date = args.from_date or (today - timedelta(days=7)).isoformat()
    to_date = args.to_date or today.isoformat()

    def factory(sub_account_id):
        return client.trade.list_orders(
            sub_account_id=sub_account_id,
            start=args.start,
            count=args.count,
            stock_code=args.stock_code,
            status_arr=status_arr,
            from_date=from_date,
            to_date=to_date,
            direction=args.direction,
            market=args.market,
            sort=args.sort,
            client_id=args.client_id,
            apply_account_id=args.apply_account_id,
            show_type=args.show_type,
        )

    dump(call_with_account_retry(client, factory, args.sub_account_id))


if __name__ == "__main__":
    run(main)
