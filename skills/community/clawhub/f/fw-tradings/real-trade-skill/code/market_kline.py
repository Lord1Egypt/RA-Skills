"""行情：K线  POST /api/v1/market/kline"""
from __future__ import annotations

import argparse

from _client import build_client, dump_with_directive, normalize_codes_inplace, run


def main():
    parser = argparse.ArgumentParser(description="查询 K 线数据")
    parser.add_argument(
        "--code", "--stock-code", "--symbol", "--symbols",
        required=True,
        help=(
            "证券代码（v1.7.5 起支持「用户原话格式」自动规范化：`01810` → `hk01810`、`AAPL` → `usAAPL`）；"
            "alias 接受 --stock-code/--symbol/--symbols（抗参数名脑补）"
        ),
    )
    parser.add_argument("--ktype", required=True,
                        help="min1/min5/min15/min30/min60/day/week/month/quarter/year")
    parser.add_argument("--delay", action="store_true")
    parser.add_argument("--num", type=int)
    parser.add_argument("--right", choices=["noward", "forward", "backward"])
    parser.add_argument("--start-time", type=int)
    parser.add_argument("--end-time", type=int)
    parser.add_argument("--time", type=int)
    parser.add_argument("--suspension", type=int)
    args = parser.parse_args()
    normalize_codes_inplace(args, "code")

    client = build_client()
    dump_with_directive(
        client.market.kline(
            code=args.code,
            ktype=args.ktype,
            delay=args.delay or None,
            end_time=args.end_time,
            num=args.num,
            right=args.right,
            start_time=args.start_time,
            suspension=args.suspension,
            time=args.time,
        ),
        next_action="已返回 K 线，**先汇报关键走势、然后停手**等下一步指令。**禁止**自动接 order_*——单步原则（第 0 条铁律）。",
    )


if __name__ == "__main__":
    run(main)
