"""行情：盘口/买卖档  GET /api/v1/market/secu/orderbook"""
from __future__ import annotations

import argparse

from _client import build_client, dump_with_directive, normalize_codes_inplace, run


def main():
    parser = argparse.ArgumentParser(description="查询盘口/买卖档")
    parser.add_argument(
        "--code", "--stock-code", "--symbol", "--symbols",
        required=True,
        help=(
            "证券代码（v1.7.5 起支持「用户原话格式」自动规范化：`01810` → `hk01810`、`AAPL` → `usAAPL`）；"
            "alias 接受 --stock-code/--symbol/--symbols（抗参数名脑补）"
        ),
    )
    parser.add_argument("--count", type=int, default=5)
    args = parser.parse_args()
    normalize_codes_inplace(args, "code")

    client = build_client()
    dump_with_directive(
        client.market.orderbook(code=args.code, count=args.count),
        next_action="已返回盘口，**先汇报、然后停手**等下一步指令。**禁止**自动接 order_*——单步原则（第 0 条铁律）。",
    )


if __name__ == "__main__":
    run(main)
