"""交易：下单  POST /api/v1/trade/OrderCreate"""
import argparse
from datetime import datetime
from zoneinfo import ZoneInfo

from _client import (
    build_client,
    call_with_account_retry,
    dump_with_directive,
    ensure_sim_hk_order_time_window,
    ensure_order_create_effective,
    ensure_sim_trade_order_type,
    ensure_sim_us_night_session_order_supported,
    ensure_user_confirmed,
    normalize_trade_stock_code,
    resolve_market_args,
    run,
    StructuredScriptError,
)

ORDER_TYPE_LABELS = {
    3: "限价单",
    9: "市价单",
}
_US_MARKET_TZ = ZoneInfo("America/New_York")
_US_PRE_START = 4 * 60          # 04:00
_US_REGULAR_START = 9 * 60 + 30  # 09:30
_US_REGULAR_END = 16 * 60        # 16:00
_US_AFTER_END = 20 * 60          # 20:00

UNSUPPORTED_ORDER_FIELD_NAMES = {
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
  - 用户明确说"买 / 卖 / 下单"，且已经选择了模拟盘

市场参数（推荐 `--market` 简写，零脑补）：
  港股：--market hk    （等价 --market-code hk --currency HKD --product-type 5）
  美股：--market us    （等价 --market-code us --currency USD --product-type 6）

示例：
  # 港股限价单：买 100 股腾讯 @ 100
  order_create.py --market hk \\
    --stock-code 00700 --direction 1 --order-type 3 \\
    --quantity 100 --price 100.000

  # 美股限价单：买 100 股苹果 @ 200
  order_create.py --market us \\
    --stock-code AAPL --direction 1 --order-type 3 \\
    --quantity 100 --price 200.000

订单类型：
  - 模拟盘只支持 3=限价单、9=市价单
  - 美股盘前/盘后（timeInForce=2）和夜盘（timeInForce=4）都不支持市价单，只支持限价单
  - 条件单、跟踪止损、止盈止损、竞价/增强/特殊限价、暗盘订单均不属于模拟盘能力

强制规则（本地拦截，零网络代价）：
  - 必须传 `--market hk|us`，或同时显式三件套（不允许混用）
  - 港股最小手数 100，下不到 100 不要试，先和用户确认
  - 港股模拟盘在 16:10-00:00 禁止下单（限价/市价都不允许）
  - 模拟盘只支持港股 / 美股正股；A 股、期权能力外
  - **必须传 `--confirm`**：模型先用自然语言复述意图（市场+方向+数量+价格+标的），
    用户明确确认后才能加 `--confirm` 跑；未传直接 NEED_CONFIRMATION 拦截
"""


def _raise_missing_for_order_type(args, missing):
    label = ORDER_TYPE_LABELS.get(args.order_type, f"orderType={args.order_type}")
    fields = "、".join(f"`--{field}`" for field in missing)
    raise StructuredScriptError(
        f"{label} 缺少必填字段：{fields}",
        error_code="INVALID_PARAM",
        hint=(
            "模拟盘限价单必须提供委托价；脚本在本地拦截，避免把不完整下单请求发到网关。"
        ),
        next_action=(
            f"补齐 {fields} 后重新复述完整下单意图，得到用户明确确认后再带 `--confirm` 执行。"
        ),
        exit_code=2,
    )


def validate_order_create_args(args):
    """校验模拟盘订单类型与字段：仅支持限价单/市价单。"""
    ensure_sim_trade_order_type(args.order_type)

    unsupported_fields = [
        cli_name
        for attr, cli_name in UNSUPPORTED_ORDER_FIELD_NAMES.items()
        if getattr(args, attr) not in (None, "")
    ]
    if unsupported_fields:
        fields = "、".join(f"`{field}`" for field in unsupported_fields)
        raise StructuredScriptError(
            f"模拟盘限价/市价单不支持这些条件类字段：{fields}",
            error_code="INVALID_PARAM",
            hint=(
                "模拟盘只开放限价单(3)和市价单(9)，"
                "不支持条件触发、跟踪止损或止盈止损字段。"
            ),
            next_action="移除这些字段；若用户想要条件/止损/止盈止损能力，明确告知模拟盘当前不支持。",
            exit_code=2,
        )

    missing = []
    if args.order_type == 3 and not args.price:
        missing.append("price")
    if missing:
        _raise_missing_for_order_type(args, missing)

    if args.order_type == 9 and args.price:
        raise StructuredScriptError(
            "市价单(orderType=9)不应传 `--price`。",
            error_code="INVALID_PARAM",
            hint="模拟盘市价单由 orderType=9 表达，不需要委托价；带 price 容易造成用户意图和请求体不一致。",
            next_action="移除 `--price`，重新复述市价单意图并确认后再执行。",
            exit_code=2,
        )


def _resolve_us_session() -> tuple[str, int]:
    """按 ET 当前时间返回美股会话标签与默认 timeInForce。"""
    now_et = datetime.now(_US_MARKET_TZ)
    minute_of_day = now_et.hour * 60 + now_et.minute
    if _US_PRE_START <= minute_of_day < _US_REGULAR_START:
        return "盘前", 2
    if _US_REGULAR_START <= minute_of_day < _US_REGULAR_END:
        return "盘中", 0
    if _US_REGULAR_END <= minute_of_day < _US_AFTER_END:
        return "盘后", 2
    return "夜盘", 4


def apply_us_time_in_force_policy(args) -> None:
    """美股订单时段策略：未显式传参时自动填充 timeInForce，并限制会话内订单类型。"""
    if (args.market_code or "").strip().lower() != "us":
        return
    session_label, default_tif = _resolve_us_session()
    if args.time_in_force is None:
        args.time_in_force = default_tif
    # 盘前/盘后/夜盘均仅支持限价单
    if args.time_in_force in (2, 4) and args.order_type == 9:
        raise StructuredScriptError(
            f"美股{session_label}不支持市价单（orderType=9）。",
            error_code="INVALID_PARAM",
            hint=(
                f"当前 ET 时段为{session_label}，脚本自动使用 timeInForce={args.time_in_force}；"
                "该时段仅支持限价单。"
            ),
            next_action="改用限价单（orderType=3 并传 --price）后重试，或等待盘中时段再下市价单。",
            exit_code=2,
        )


def main():
    parser = argparse.ArgumentParser(
        description="提交委托订单（模拟盘）",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--sub-account-id")
    parser.add_argument(
        "--stock-code", "--code", "--symbol", "--symbols",
        required=True,
        help=(
            "标的纯代码（首选/正确格式：港股 `00700`，美股 `AAPL`；请求体由 marketCode 单独表达市场，"
            "即 marketCode=hk + stockCode=00700）。兼容兜底：误传 `hk00700` / `HK.00700` / `usAAPL` 时，"
            "脚本会按 marketCode 校验后剥离前缀；前缀和 marketCode 冲突会本地拦截。"
            "alias 接受 --code/--symbol/--symbols（抗参数名脑补）"
        ),
    )
    parser.add_argument("--direction", type=int, required=True, choices=[1, 2], help="1=买 2=卖")
    parser.add_argument(
        "--order-type",
        type=int,
        required=True,
        help=(
            "模拟盘订单类型：3=限价单，9=市价单；"
            "市价是 9，不是 4。"
        ),
    )
    parser.add_argument("--quantity", required=True)
    parser.add_argument("--market", choices=["hk", "us"],
                        help="推荐：一键展开市场三件套；hk=港股(HKD/5) us=美股(USD/6)；与 --market-code/--currency/--product-type 互斥")
    parser.add_argument("--market-code", choices=["hk", "us"],
                        help="高级用法（与 --market 互斥）；hk=港股 us=美股")
    parser.add_argument("--currency", choices=["HKD", "USD"],
                        help="高级用法（与 --market 互斥）；港股传 HKD，美股传 USD")
    parser.add_argument("--product-type", type=int, choices=[5, 6],
                        help="高级用法（与 --market 互斥）；5=港股 6=美股，必须与 --market-code 对齐")
    parser.add_argument(
        "--price",
        help=(
            "委托价：限价单(orderType=3)必填；市价单(orderType=9)不传。"
        ),
    )
    parser.add_argument("--client-id", type=int)
    parser.add_argument(
        "--time-in-force",
        type=int,
        help="时段(timeInForce)：0=当日有效 2=允许美股盘前盘后 4=允许夜盘；美股未传时按 ET 时段自动填充（盘前/盘后=2，夜盘=4，其余=0）",
    )
    parser.add_argument(
        "--exp-type",
        type=int,
        help="订单时效 expType：常用 1=当日有效（详见 OrderCreate 请求体说明）",
    )
    parser.add_argument("--short-sell-type")
    parser.add_argument("--trig-price", help=argparse.SUPPRESS)
    parser.add_argument("--tail-type", type=int, help=argparse.SUPPRESS)
    parser.add_argument("--tail-amount", help=argparse.SUPPRESS)
    parser.add_argument("--tail-pct", help=argparse.SUPPRESS)
    parser.add_argument("--spread", help=argparse.SUPPRESS)
    parser.add_argument("--profit-price", help=argparse.SUPPRESS)
    parser.add_argument("--profit-quantity", help=argparse.SUPPRESS)
    parser.add_argument("--stop-loss-price", help=argparse.SUPPRESS)
    parser.add_argument("--stop-loss-quantity", help=argparse.SUPPRESS)
    parser.add_argument("--apply-account-id")
    parser.add_argument(
        "--intent",
        required=True,
        help=(
            "**必传**：用一段中文复述本次下单的完整意图，必须包含：操作（买/卖）+ 市场（港股/美股）+ "
            "标的（含中文名最好）+ 数量 + 价格（市价单说明不传价格）+ 订单类型。"
            "例：『港股买入 100 股腾讯（00700）@ 270 港币 限价单』。"
            "本字段会被原样打印到 stdout 与 NEED_CONFIRMATION 错误，让用户立即看到模型理解的意图——意图不对用户就能立刻纠正。"
            "把『复述意图』从靠模型自觉升级为 argparse 强制项，抗长会话衰减。"
        ),
    )
    parser.add_argument("--confirm", action="store_true",
                        help="必传：用户已明确确认下单意图后再加这个 flag；未传将被 NEED_CONFIRMATION 拦截")
    parser.add_argument("--confirm-token",
                        help="二次确认令牌：先触发一次 NEED_CONFIRMATION 后，从返回信息复制 token，再与 --confirm 一起提交")
    args = parser.parse_args()
    args.market_code, args.currency, args.product_type = resolve_market_args(
        args.market, args.market_code, args.currency, args.product_type,
        require_currency=True,
    )
    args.stock_code = normalize_trade_stock_code(args.stock_code, args.market_code)
    validate_order_create_args(args)
    apply_us_time_in_force_policy(args)
    ensure_sim_hk_order_time_window(args.market_code)
    ensure_sim_us_night_session_order_supported(
        args.market_code,
        args.order_type,
        args.time_in_force,
    )
    ensure_user_confirmed(
        args.confirm,
        action="下单",
        intent_summary=args.intent,
        confirm_token=args.confirm_token,
    )

    client = build_client()

    def factory(sub_account_id):
        return client.trade.create_order(
            sub_account_id=sub_account_id,
            stock_code=args.stock_code,
            direction=args.direction,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
            market_code=args.market_code,
            currency=args.currency,
            client_id=args.client_id,
            time_in_force=args.time_in_force,
            exp_type=args.exp_type,
            short_sell_type=args.short_sell_type,
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
    order_id = ensure_order_create_effective(result)
    dump_with_directive(
        {"intent": args.intent, "orderId": order_id, "result": result},
        next_action=(
            "下单请求已发送。**先把下单结果（含 orderId）汇报给用户、然后停手**等下一步指令。"
            "汇报时不能只说 code/orderStatus 数字，必须同时说明对应文字状态（如 code=0 表示接口成功，orderStatus=40 表示已报）。"
            "**禁止**自动接 order_list / holdings / cash_summary——单步原则（第 0 条铁律）。"
            "如果用户接下来问『成了吗 / 撮合到没』，再单独跑 order_list.py 查最新状态。"
        ),
    )


if __name__ == "__main__":
    run(main)
