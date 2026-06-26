#!/usr/bin/env python3
"""
次方量化基金数据获取脚本
封装API调用，提供便捷的数据获取功能

支持功能：
1. 基金列表查询
2. 历史行情数据获取
3. 实时行情数据获取（延迟不超过2分钟）
4. 场内基金收益率排行
5. 基金搜索

使用前需要设置环境变量 CIFANG_API_KEY 或通过 --api-key 参数提供API密钥
"""

import os
import sys
import json
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional
import argparse

class CifangQuantAPI:
    """次方量化API客户端"""

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化API客户端

        Args:
            api_key: API密钥，如果为None则从环境变量CIFANG_API_KEY读取
        """
        self.api_key = api_key or os.getenv("CIFANG_API_KEY")
        if not self.api_key:
            raise ValueError("API Key未设置。请设置环境变量CIFANG_API_KEY或直接传入api_key参数")

        self.base_url = "https://www.cifangquant.com/api"
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """发送API请求"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            result = response.json()

            # 检查API返回码
            if result.get("code") != 0:
                raise Exception(f"API错误: {result.get('message', '未知错误')}")

            return result.get("data", {})

        except requests.exceptions.RequestException as e:
            raise Exception(f"请求失败: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"JSON解析失败: {str(e)}")

    def get_fund_list(self, key_word: str = None) -> List[Dict[str, Any]]:
        """
        获取基金列表

        Args:
            key_word: 关键词，基金代码或名称

        Returns:
            基金信息列表
        """
        params = {}
        if key_word:
            params["key_word"] = key_word

        data = self._make_request("/fund/list", params)
        return data if isinstance(data, list) else []

    def get_historical_data(
        self,
        symbols: List[str],
        start_date: str,
        end_date: str,
        adjust: str = "none"
    ) -> Dict[str, List[List[Any]]]:
        """
        获取基金历史行情数据

        Args:
            symbols: 基金代码列表
            start_date: 开始日期，格式YYYY-MM-DD
            end_date: 结束日期，格式YYYY-MM-DD
            adjust: 复权类型，none/qfq/hfq

        Returns:
            历史行情数据，键为基金代码，值为行情数据列表
        """
        valid_adjust = ["none", "qfq", "hfq"]
        if adjust not in valid_adjust:
            raise ValueError(f"adjust参数必须是{valid_adjust}之一")

        # 验证日期格式
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("日期格式必须为YYYY-MM-DD")

        # 限制最多50个基金代码
        if len(symbols) > 50:
            raise ValueError("最多支持50个基金代码")

        params = {
            "symbol": ",".join(symbols),
            "start_date": start_date,
            "end_date": end_date,
            "adjust": adjust
        }

        return self._make_request("/fund/hist_em", params)

    def search_funds_by_name(self, name_keyword: str) -> List[Dict[str, Any]]:
        """
        根据名称关键词搜索基金

        Args:
            name_keyword: 名称关键词

        Returns:
            匹配的基金列表
        """
        all_funds = self.get_fund_list()
        if not all_funds:
            return []

        keyword_lower = name_keyword.lower()
        return [
            fund for fund in all_funds
            if keyword_lower in fund.get("fund_name", "").lower()
        ]

    def get_fund_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        获取单个基金的详细信息

        Args:
            symbol: 基金代码

        Returns:
            基金信息，如果未找到则返回None
        """
        funds = self.get_fund_list(symbol)
        for fund in funds:
            if fund.get("fund_code") == symbol:
                return fund
        return None

    def get_spot_data(self, symbols: List[str] = None) -> Dict[str, Dict[str, Any]]:
        """
        获取基金实时行情数据

        Args:
            symbols: 基金代码列表，如果不传则返回全量实时行情

        Returns:
            实时行情数据，键为基金代码，值为行情对象
        """
        params = {}
        if symbols:
            params["symbol"] = ",".join(symbols)

        return self._make_request("/fund/spot", params)

    def get_exchange_rank(
        self,
        sort_by: str = "1yzf",
        sort_order: str = "desc",
        limit: int = 30000
    ) -> List[Dict[str, Any]]:
        """
        获取场内基金收益率排行榜

        Args:
            sort_by: 排序字段：zzf(近1周)、1yzf(近1月)、3yzf(近3月)、6yzf(近6月)、
                    1nzf(近1年)、2nzf(近2年)、3nzf(近3年)、jnzf(今年来)、lnzf(成立以来)
            sort_order: 排序方向：desc(降序)或asc(升序)
            limit: 返回数量上限

        Returns:
            排行结果列表
        """
        valid_sort_fields = ["zzf", "1yzf", "3yzf", "6yzf", "1nzf", "2nzf", "3nzf", "jnzf", "lnzf"]
        if sort_by not in valid_sort_fields:
            raise ValueError(f"sort_by参数必须是{valid_sort_fields}之一")

        valid_sort_orders = ["desc", "asc"]
        if sort_order not in valid_sort_orders:
            raise ValueError(f"sort_order参数必须是{valid_sort_orders}之一")

        if limit < 1 or limit > 30000:
            raise ValueError("limit参数必须在1-30000之间")

        params = {
            "sort_by": sort_by,
            "sort_order": sort_order,
            "limit": limit
        }

        data = self._make_request("/fund/exchange_rank", params)
        return data if isinstance(data, list) else []


def convert_to_readable_format(raw_data: List[List[Any]]) -> List[Dict[str, Any]]:
    """
    将原始数据格式转换为易读的对象格式

    Args:
        raw_data: 原始数据，格式为[[date, open, close, high, low, change_percent, volume], ...]

    Returns:
        转换后的数据列表
    """
    readable_data = []
    for row in raw_data:
        if len(row) >= 7:
            readable_data.append({
                "date": row[0],
                "open": row[1],
                "close": row[2],
                "high": row[3],
                "low": row[4],
                "change_percent": row[5],
                "volume": row[6]
            })
    return readable_data


def calculate_statistics(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    计算基本统计指标

    Args:
        data: 转换后的行情数据

    Returns:
        统计指标
    """
    if not data:
        return {}

    closes = [d["close"] for d in data if "close" in d]
    if not closes:
        return {}

    # 计算期间收益率
    start_price = closes[0]
    end_price = closes[-1]
    total_return = (end_price - start_price) / start_price * 100 if start_price != 0 else 0

    # 计算波动率（简单版本）
    returns = []
    for i in range(1, len(closes)):
        if closes[i-1] != 0:
            daily_return = (closes[i] - closes[i-1]) / closes[i-1]
            returns.append(daily_return)

    volatility = (sum((r - sum(returns)/len(returns))**2 for r in returns) / len(returns))**0.5 * 100 if returns else 0

    # 计算最大回撤
    peak = closes[0]
    max_drawdown = 0
    for price in closes:
        if price > peak:
            peak = price
        drawdown = (peak - price) / peak * 100 if peak != 0 else 0
        if drawdown > max_drawdown:
            max_drawdown = drawdown

    return {
        "start_date": data[0]["date"],
        "end_date": data[-1]["date"],
        "start_price": start_price,
        "end_price": end_price,
        "total_return_percent": round(total_return, 2),
        "volatility_percent": round(volatility, 2),
        "max_drawdown_percent": round(max_drawdown, 2),
        "trading_days": len(data)
    }


def main():
    """命令行入口点"""
    parser = argparse.ArgumentParser(description="次方量化基金数据获取工具")
    parser.add_argument("--api-key", help="API密钥，如果不提供则从环境变量读取")

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 基金列表命令
    list_parser = subparsers.add_parser("list", help="获取基金列表")
    list_parser.add_argument("--keyword", help="搜索关键词")

    # 历史数据命令
    history_parser = subparsers.add_parser("history", help="获取历史数据")
    history_parser.add_argument("symbols", nargs="+", help="基金代码，多个用空格分隔")
    history_parser.add_argument("--start-date", required=True, help="开始日期 YYYY-MM-DD")
    history_parser.add_argument("--end-date", required=True, help="结束日期 YYYY-MM-DD")
    history_parser.add_argument("--adjust", choices=["none", "qfq", "hfq"], default="none", help="复权类型")
    history_parser.add_argument("--format", choices=["raw", "readable", "stats"], default="readable", help="输出格式")

    # 搜索命令
    search_parser = subparsers.add_parser("search", help="搜索基金")
    search_parser.add_argument("keyword", help="搜索关键词")

    # 实时行情命令
    spot_parser = subparsers.add_parser("spot", help="获取实时行情")
    spot_parser.add_argument("symbols", nargs="*", help="基金代码，多个用空格分隔，不传则返回全量")
    spot_parser.add_argument("--format", choices=["raw", "readable"], default="raw", help="输出格式")

    # 场内基金排行命令
    rank_parser = subparsers.add_parser("rank", help="获取场内基金排行")
    rank_parser.add_argument("--sort-by", choices=["zzf", "1yzf", "3yzf", "6yzf", "1nzf", "2nzf", "3nzf", "jnzf", "lnzf"],
                           default="1yzf", help="排序字段")
    rank_parser.add_argument("--sort-order", choices=["desc", "asc"], default="desc", help="排序方向")
    rank_parser.add_argument("--limit", type=int, default=100, help="返回数量上限")

    args = parser.parse_args()

    try:
        api = CifangQuantAPI(args.api_key)

        if args.command == "list":
            funds = api.get_fund_list(args.keyword)
            print(json.dumps(funds, ensure_ascii=False, indent=2))

        elif args.command == "history":
            # 获取历史数据
            raw_data = api.get_historical_data(
                args.symbols, args.start_date, args.end_date, args.adjust
            )

            if args.format == "raw":
                # 原始格式
                print(json.dumps(raw_data, ensure_ascii=False, indent=2))

            elif args.format == "readable":
                # 可读格式
                result = {}
                for symbol, data in raw_data.items():
                    result[symbol] = convert_to_readable_format(data)
                print(json.dumps(result, ensure_ascii=False, indent=2))

            elif args.format == "stats":
                # 统计信息
                result = {}
                for symbol, data in raw_data.items():
                    readable_data = convert_to_readable_format(data)
                    stats = calculate_statistics(readable_data)
                    result[symbol] = stats
                print(json.dumps(result, ensure_ascii=False, indent=2))

        elif args.command == "search":
            funds = api.search_funds_by_name(args.keyword)
            print(json.dumps(funds, ensure_ascii=False, indent=2))

        elif args.command == "spot":
            # 获取实时行情
            symbols = args.symbols if args.symbols else None
            spot_data = api.get_spot_data(symbols)

            if args.format == "raw":
                # 原始格式
                print(json.dumps(spot_data, ensure_ascii=False, indent=2))
            elif args.format == "readable":
                # 可读格式（已经是对象格式，直接输出）
                print(json.dumps(spot_data, ensure_ascii=False, indent=2))

        elif args.command == "rank":
            # 获取场内基金排行
            rank_data = api.get_exchange_rank(
                sort_by=args.sort_by,
                sort_order=args.sort_order,
                limit=args.limit
            )
            print(json.dumps(rank_data, ensure_ascii=False, indent=2))

        else:
            parser.print_help()

    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()