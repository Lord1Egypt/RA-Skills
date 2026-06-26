#!/usr/bin/env python3
"""
模拟数据生成器
用于测试和演示，无需真实API Key
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

def generate_fund_list(keyword: str = None) -> List[Dict[str, Any]]:
    """生成模拟基金列表"""
    all_funds = [
        {
            "fund_code": "510300",
            "fund_name": "华泰柏瑞沪深300ETF",
            "fund_type": "指数型-股票",
            "fund_market": "SH",
            "establish_date": "2012-05-04"
        },
        {
            "fund_code": "510500",
            "fund_name": "南方中证500ETF",
            "fund_type": "指数型-股票",
            "fund_market": "SH",
            "establish_date": "2013-02-06"
        },
        {
            "fund_code": "159919",
            "fund_name": "嘉实沪深300ETF",
            "fund_type": "指数型-股票",
            "fund_market": "SZ",
            "establish_date": "2012-03-30"
        },
        {
            "fund_code": "159915",
            "fund_name": "易方达创业板ETF",
            "fund_type": "指数型-股票",
            "fund_market": "SZ",
            "establish_date": "2011-09-20"
        },
        {
            "fund_code": "518880",
            "fund_name": "华安黄金ETF",
            "fund_type": "商品型",
            "fund_market": "SH",
            "establish_date": "2013-07-18"
        }
    ]

    if not keyword:
        return all_funds

    keyword_lower = keyword.lower()
    filtered_funds = []
    for fund in all_funds:
        if (keyword_lower in fund["fund_code"].lower() or
            keyword_lower in fund["fund_name"].lower() or
            keyword_lower in fund["fund_type"].lower()):
            filtered_funds.append(fund)

    return filtered_funds


def generate_historical_data(
    symbols: List[str],
    start_date: str,
    end_date: str,
    adjust: str = "none"
) -> Dict[str, List[List[Any]]]:
    """生成模拟历史行情数据"""

    # 解析日期
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    # 生成交易日列表（排除周末）
    trading_days = []
    current = start
    while current <= end:
        # 简单模拟：周一至周五为交易日
        if current.weekday() < 5:  # 0-4表示周一到周五
            trading_days.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)

    if not trading_days:
        trading_days = [start_date, end_date]

    result = {}

    # 基础价格，不同基金有不同的基础价格
    base_prices = {
        "510300": 3.5,
        "510500": 5.5,
        "159919": 3.6,
        "159915": 2.0,
        "518880": 4.5
    }

    for symbol in symbols:
        base_price = base_prices.get(symbol, 10.0)
        fund_data = []

        prev_price = base_price
        for i, date_str in enumerate(trading_days):
            # 模拟价格波动
            if i == 0:
                open_price = base_price
            else:
                # 基于前一日收盘价
                open_price = prev_price * (1 + random.uniform(-0.02, 0.02))

            # 日内波动
            daily_volatility = random.uniform(0.005, 0.03)
            change = open_price * daily_volatility * random.choice([-1, 1])
            close_price = open_price + change

            high_price = max(open_price, close_price) * (1 + random.uniform(0, 0.01))
            low_price = min(open_price, close_price) * (1 - random.uniform(0, 0.01))

            # 确保价格合理
            high_price = max(open_price, close_price, high_price)
            low_price = min(open_price, close_price, low_price)

            # 计算涨跌幅
            if i == 0:
                change_percent = 0.0
            else:
                change_percent = (close_price - prev_price) / prev_price * 100

            # 生成成交量（与价格波动相关）
            volume = int(abs(change) * 1000000) + random.randint(100000, 500000)

            fund_data.append([
                date_str,
                round(open_price, 3),
                round(close_price, 3),
                round(high_price, 3),
                round(low_price, 3),
                round(change_percent, 2),
                volume
            ])

            prev_price = close_price

        result[symbol] = fund_data

    return result


class MockCifangAPI:
    """模拟次方量化API，用于测试"""

    def __init__(self, api_key: str = None):
        """初始化模拟API，api_key参数仅为兼容性保留"""
        self.api_key = api_key or "mock-api-key-for-testing"

    def get_fund_list(self, key_word: str = None) -> List[Dict[str, Any]]:
        """获取模拟基金列表"""
        return generate_fund_list(key_word)

    def get_historical_data(
        self,
        symbols: List[str],
        start_date: str,
        end_date: str,
        adjust: str = "none"
    ) -> Dict[str, List[List[Any]]]:
        """获取模拟历史数据"""
        return generate_historical_data(symbols, start_date, end_date, adjust)

    def search_funds_by_name(self, name_keyword: str) -> List[Dict[str, Any]]:
        """模拟按名称搜索基金"""
        all_funds = self.get_fund_list()
        keyword_lower = name_keyword.lower()
        return [
            fund for fund in all_funds
            if keyword_lower in fund.get("fund_name", "").lower()
        ]


def main():
    """测试模拟数据生成"""
    import argparse

    parser = argparse.ArgumentParser(description="模拟数据生成器")
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # 基金列表命令
    list_parser = subparsers.add_parser("list", help="生成基金列表")
    list_parser.add_argument("--keyword", help="搜索关键词")

    # 历史数据命令
    history_parser = subparsers.add_parser("history", help="生成历史数据")
    history_parser.add_argument("symbols", nargs="+", help="基金代码")
    history_parser.add_argument("--start-date", default="2024-01-01", help="开始日期")
    history_parser.add_argument("--end-date", default="2024-12-31", help="结束日期")
    history_parser.add_argument("--adjust", default="none", help="复权类型")

    args = parser.parse_args()

    if args.command == "list":
        funds = generate_fund_list(args.keyword)
        print(json.dumps(funds, ensure_ascii=False, indent=2))

    elif args.command == "history":
        data = generate_historical_data(
            args.symbols, args.start_date, args.end_date, args.adjust
        )
        print(json.dumps(data, ensure_ascii=False, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()