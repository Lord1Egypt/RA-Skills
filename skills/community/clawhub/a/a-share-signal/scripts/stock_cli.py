#!/usr/bin/env python3
"""
A股数据查询脚本，本地回退方案基于 AkShare。
仅在用户明确同意使用非 mx-skills 数据源后，才应调用它查看行情、K线、板块、资金流和股票搜索结果。
"""

import argparse
import json
import sys
from datetime import datetime, timedelta

try:
    import akshare as ak
except ImportError:
    print("请先安装: pip install akshare")
    sys.exit(1)


def 获取实时行情(symbols=None):
    """实时行情。"""
    df = ak.stock_zh_a_spot_em()
    if symbols:
        df = df[df["代码"].isin(symbols)]
    return df.to_dict(orient="records")


def 获取历史K线(symbol, period="daily", days=30):
    """历史K线。"""
    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")

    df = ak.stock_zh_a_hist(
        symbol=symbol,
        period=period,
        start_date=start_date,
        end_date=end_date,
        adjust="qfq",
    )
    return df.to_dict(orient="records")


def 获取行业板块():
    """行业板块。"""
    df = ak.stock_board_industry_name_em()
    return df.head(20).to_dict(orient="records")


def 获取概念板块():
    """概念板块。"""
    df = ak.stock_board_concept_name_em()
    return df.head(20).to_dict(orient="records")


def 获取资金流(symbol, market="sh"):
    """个股资金流向。"""
    df = ak.stock_individual_fund_flow(stock=symbol, market=market)
    return df.to_dict(orient="records")


def 搜索股票(keyword):
    """按代码或名称搜索股票。"""
    df = ak.stock_zh_a_spot_em()
    result = df[df["代码"].str.contains(keyword) | df["名称"].str.contains(keyword)]
    return result.head(10).to_dict(orient="records")


def main():
    parser = argparse.ArgumentParser(description="A股数据查询工具（经用户同意后使用的本地 AkShare 回退）")
    parser.add_argument(
        "action",
        choices=["quote", "kline", "industry", "concept", "flow", "search"],
        help="操作类型",
    )
    parser.add_argument("--symbol", help="股票代码")
    parser.add_argument("--period", default="daily", choices=["daily", "weekly", "monthly"])
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--keyword", help="搜索关键词")
    parser.add_argument("--market", default="sh", help="市场代码，如 sh / sz")

    args = parser.parse_args()

    try:
        if args.action == "quote":
            data = 获取实时行情()
            print(json.dumps(data[:5], ensure_ascii=False, indent=2))

        elif args.action == "kline":
            if not args.symbol:
                print("错误: 需要 --symbol 参数")
                sys.exit(1)
            data = 获取历史K线(args.symbol, args.period, args.days)
            print(json.dumps(data, ensure_ascii=False, indent=2))

        elif args.action == "industry":
            data = 获取行业板块()
            print(json.dumps(data, ensure_ascii=False, indent=2))

        elif args.action == "concept":
            data = 获取概念板块()
            print(json.dumps(data, ensure_ascii=False, indent=2))

        elif args.action == "flow":
            if not args.symbol:
                print("错误: 需要 --symbol 参数")
                sys.exit(1)
            data = 获取资金流(args.symbol, args.market)
            print(json.dumps(data, ensure_ascii=False, indent=2))

        elif args.action == "search":
            if not args.keyword:
                print("错误: 需要 --keyword 参数")
                sys.exit(1)
            data = 搜索股票(args.keyword)
            print(json.dumps(data, ensure_ascii=False, indent=2))

    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
