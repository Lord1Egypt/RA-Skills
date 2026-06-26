"""交易：改单  POST /api/v1/trade/OrderModify"""
import argparse

from _client import (
    build_client,
    call_with_account_retry,
    dump_with_directive,
    ensure_order_modify_effective,
    ensure_sim_trade_modify_type,
    ensure_user_confirmed,
    resolve_market_args,
    run,
    StructuredScriptError,
)

UNSUPPORTED_MODIFY_FIELD_NAMES = {
    "trig_price": "--trig-price",
    "tail_type": "--tail-type",
    "tail_amount": "--tail-amount",
    "tail_pct": "--tail-pct",
    "spread": "--spread",
    "profit_price": "--profit-price",
    "profit_quantity": "--profit-quantity",
    "stop_loss_price": "--stop-loss-price",
    "stop_loss_quantity": "--stop-loss-quantity",
}

EPILOG = """\
何时调用：
  - 用户明确说"改价 / 改单 / 改数量"

示例（推荐 `--market` 简写）：
  # 改任意可改订单：按用户意图传要修改的字段
  order_modify.py --order-id 1234567890 --modify-type 1 \\
    --price 105.000 --market hk --confirm

要点：
  - 模拟盘只支持限价单/市价单，因此改单只支持普通订单可改字段（数量、价格）
  - --modify-type 仅允许 1=改普通订单；不支持条件单改单
  - --market hk|us 必须与原订单市场一致（高级用户也可显式 --product-type 5|6）
  - 不知道 order-id 时，先跑 order_list.py
  - **必须传 `--confirm`**：模型先用自然语言复述改单意图（订单 + 市场 + 要修改的字段），
    用户明确确认后才能加 `--confirm` 跑；未传直接 NEED_CONFIRMATION 拦截
"""


def validate_order_modify_args(args):
    ensure_sim_trade_modify_type(args.modify_type)

    unsupported_fields = [
        cli_name
        for attr, cli_name in UNSUPPORTED_MODIFY_FIELD_NAMES.items()
        if getattr(args, attr) not in (None, "")
    ]
    if unsupported_fields:
        fields = "、".join(f"`{field}`" for field in unsupported_fields)
        raise StructuredScriptError(
            f"模拟盘普通改单不支持这些条件类字段：{fields}",
            error_code="INVALID_PARAM",
            hint="模拟盘只支持限价单/市价单，不支持条件单、跟踪止损、止盈止损相关改单字段。",
            next_action="移除这些字段；如果用户要改价或改数量，使用 `--price` / `--quantity` 并保持 `--modify-type 1`。",
            exit_code=2,
        )

    changed_fields = [
        args.quantity,
        args.price,
    ]
    if not any(value not in (None, "") for value in changed_fields):
        raise StructuredScriptError(
            "改单请求没有任何要修改的字段。",
            error_code="INVALID_PARAM",
            hint="模拟盘普通订单改单至少要提供一个新数量或新价格。",
            next_action="向用户确认具体要改什么字段后，重新复述完整改单意图并再次确认。",
            exit_code=2,
        )


def main():
    parser = argparse.ArgumentParser(
        description="修改未成交/部成订单（模拟盘）",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--order-id", required=True)
    parser.add_argument("--modify-type", type=int, required=True,
                        help="模拟盘仅允许 1=修改普通订单")
    parser.add_argument("--quantity")
    parser.add_argument("--sub-account-id")
    parser.add_argument("--client-id", type=int)
    parser.add_argument(
        "--price",
        help="修改后委托价：仅普通限价/市价订单改单使用",
    )
    parser.add_argument("--trig-price", help=argparse.SUPPRESS)
    parser.add_argument("--tail-type", type=int, help=argparse.SUPPRESS)
    parser.add_argument("--tail-amount", help=argparse.SUPPRESS)
    parser.add_argument("--tail-pct", help=argparse.SUPPRESS)
    parser.add_argument("--spread", help=argparse.SUPPRESS)
    parser.add_argument("--profit-price", help=argparse.SUPPRESS)
    parser.add_argument("--profit-quantity", help=argparse.SUPPRESS)
    parser.add_argument("--stop-loss-price", help=argparse.SUPPRESS)
    parser.add_argument("--stop-loss-quantity", help=argparse.SUPPRESS)
    parser.add_argument("--market", choices=["hk", "us"],
                        help="推荐：一键解析 product_type；hk=5(港股) us=6(美股)；与 --product-type 互斥")
    parser.add_argument("--product-type", type=int, choices=[5, 6],
                        help="高级用法（与 --market 互斥）；5=港股 6=美股，必须与原订单市场一致")
    parser.add_argument("--apply-account-id")
    parser.add_argument(
        "--intent",
        required=True,
        help=(
            "**必传**：用一段中文复述本次改单的完整意图，必须包含：要改的 orderId + 市场 + 要修改的字段 + 修改类型。"
            "例：『改港股 00700 订单 1234567890 → 价格 105 港币、普通订单』。"
            "本字段会被原样打印到 stdout 与 NEED_CONFIRMATION 错误，让用户立即看到模型理解的意图。"
        ),
    )
    parser.add_argument("--confirm", action="store_true",
                        help="必传：用户已明确确认改单意图后再加这个 flag；未传将被 NEED_CONFIRMATION 拦截")
    parser.add_argument("--confirm-token",
                        help="二次确认令牌：先触发一次 NEED_CONFIRMATION 后，从返回信息复制 token，再与 --confirm 一起提交")
    args = parser.parse_args()
    ensure_user_confirmed(
        args.confirm,
        action="改单",
        intent_summary=args.intent,
        confirm_token=args.confirm_token,
    )
    _, _, args.product_type = resolve_market_args(
        args.market, None, None, args.product_type,
        require_currency=False,
    )
    validate_order_modify_args(args)

    client = build_client()

    def factory(sub_account_id):
        return client.trade.order_modify(
            sub_account_id=sub_account_id,
            order_id=args.order_id,
            modify_type=args.modify_type,
            client_id=args.client_id,
            quantity=args.quantity,
            price=args.price,
            trig_price=args.trig_price,
            tail_type=args.tail_type,
            tail_amount=args.tail_amount,
            tail_pct=args.tail_pct,
            spread=args.spread,
            profit_trig_price=args.profit_price,
            profit_quantity=args.profit_quantity,
            stop_loss_trig_price=args.stop_loss_price,
            stop_loss_quantity=args.stop_loss_quantity,
            product_type=args.product_type,
            apply_account_id=args.apply_account_id,
        )

    result = call_with_account_retry(client, factory, args.sub_account_id)
    evidence = ensure_order_modify_effective(result)
    dump_with_directive(
        {"intent": args.intent, **evidence, "result": result},
        next_action=(
            "改单请求已发送。**先汇报改单结果给用户、然后停手**等下一步指令。"
            "汇报时不能只说 code/orderStatus 数字，必须同时说明对应文字状态（如 code=0 表示接口成功，orderStatus=40 表示已报）。"
            "**禁止**自动接 order_list / holdings——单步原则（第 0 条铁律）。"
            "如果用户接下来问『改成功没』，再单独跑 order_list.py 查最新状态。"
        ),
    )


if __name__ == "__main__":
    run(main)
