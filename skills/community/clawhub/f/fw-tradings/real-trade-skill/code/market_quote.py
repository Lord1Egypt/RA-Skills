"""行情：证券报价（批量）  POST /api/v1/market/secu/quote"""
from __future__ import annotations

import argparse

from _client import build_client, dump_with_directive, normalize_codes_inplace, run


def main():
    parser = argparse.ArgumentParser(description="批量查询证券报价")
    parser.add_argument(
        "--code", "--stock-code", "--symbol", "--symbols",
        action="append", required=True,
        help=(
            "可多次传，支持「用户原话格式」（v1.7.5 起自动规范化）：`01810` → `hk01810`、"
            "`AAPL` → `usAAPL`、`HK.00700` → `hk00700`、`us.aapl` → `usAAPL`。"
            "alias 接受 --stock-code/--symbol/--symbols（抗参数名脑补）"
        ),
    )
    parser.add_argument("--field", action="append", help="可多次传，如 --field price --field low")
    args = parser.parse_args()
    normalize_codes_inplace(args, "code")

    client = build_client()
    dump_with_directive(
        client.market.quote(codes=args.code, fields=args.field),
        next_action=(
            "已返回实时报价，**先把价格汇报给用户、然后停手**等下一步指令。"
            "价格解码必须按 `power`：实际值=raw/(10^power)，小数位按 power 截取，"
            "禁止按经验猜测小数位。"
            "**禁止**自动接 order_* —— 用户报价后是否下单要再次询问；单步原则（第 0 条铁律）。"
        ),
    )


if __name__ == "__main__":
    run(main)
