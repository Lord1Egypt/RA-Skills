"""交易：撤单  POST /api/v1/trade/OrderCancel"""
import argparse

from _client import (
    build_client,
    call_with_account_retry,
    dump_with_directive,
    ensure_order_cancel_effective,
    ensure_user_confirmed,
    resolve_market_args,
    run,
)

EPILOG = """\
何时调用：
  - 用户明确说"撤单 / 取消那张单"

示例（推荐 `--market` 简写，与原订单市场一致）：
  # 撤港股任意可撤订单
  order_cancel.py --order-id 1234567890 --market hk --confirm
  # 撤美股任意可撤订单
  order_cancel.py --order-id 1234567890 --market us --confirm

要点：
  - 模型不知道 order-id 时，先跑 order_list.py 给用户列出来让其选
  - 不知道是港股还是美股 → 先问用户或从 order_list 输出里读 market
  - 撤单按 orderId 撤销任意可撤订单；是否可撤由服务端按订单状态判断
  - 高级用户也可显式 --product-type 5|6（与 --market 互斥）
  - **必须传 `--confirm`**：模型先用自然语言复述要撤的订单（orderId + 市场 + 标的 + 方向/数量/订单类型/关键条件），
    用户明确确认后才能加 `--confirm` 跑；未传直接 NEED_CONFIRMATION 拦截
"""


def main():
    parser = argparse.ArgumentParser(
        description="撤销未成交/部成订单（实盘）",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--order-id", required=True)
    parser.add_argument("--sub-account-id")
    parser.add_argument("--client-id", type=int)
    parser.add_argument("--market", choices=["hk", "us"],
                        help="推荐：一键解析 product_type；hk=5(港股) us=6(美股)；与 --product-type 互斥")
    parser.add_argument("--product-type", type=int, choices=[5, 6],
                        help="高级用法（与 --market 互斥）；5=港股 6=美股，必须与原订单市场一致")
    parser.add_argument("--apply-account-id")
    parser.add_argument(
        "--intent",
        required=True,
        help=(
            "**必传**：用一段中文复述本次撤单的完整意图，必须包含：要撤的 orderId + 市场 + 该订单的标的/方向/数量/订单类型/关键条件摘要。"
            "例：『撤掉港股 00700 订单 1234567890（买 100 股，限价单 @ 270 港币）』。"
            "本字段会被原样打印到 stdout 与 NEED_CONFIRMATION 错误，让用户立即看到模型理解的意图。"
        ),
    )
    parser.add_argument("--confirm", action="store_true",
                        help="必传：用户已明确确认撤单意图后再加这个 flag；未传将被 NEED_CONFIRMATION 拦截")
    parser.add_argument("--confirm-token",
                        help="二次确认令牌：先触发一次 NEED_CONFIRMATION 后，从返回信息复制 token，再与 --confirm 一起提交")
    args = parser.parse_args()
    ensure_user_confirmed(
        args.confirm,
        action="撤单",
        intent_summary=args.intent,
        confirm_token=args.confirm_token,
    )
    _, _, args.product_type = resolve_market_args(
        args.market, None, None, args.product_type,
        require_currency=False,
    )

    client = build_client()

    def factory(sub_account_id):
        return client.trade.cancel_order(
            order_id=args.order_id,
            sub_account_id=sub_account_id,
            client_id=args.client_id,
            product_type=args.product_type,
            apply_account_id=args.apply_account_id,
        )

    result = call_with_account_retry(client, factory, args.sub_account_id)
    evidence = ensure_order_cancel_effective(result)
    dump_with_directive(
        {"intent": args.intent, **evidence, "result": result},
        next_action=(
            "撤单请求已发送。**先汇报撤单结果给用户、然后停手**等下一步指令。"
            "汇报时不能只说 code/orderStatus 数字，必须同时说明对应文字状态（如 code=0 表示接口成功，orderStatus=70 表示已撤）。"
            "**禁止**自动接 order_list / holdings——单步原则（第 0 条铁律）。"
            "如果用户接下来问『撤了没』，再单独跑 order_list.py 查最新状态。"
        ),
    )


if __name__ == "__main__":
    run(main)
