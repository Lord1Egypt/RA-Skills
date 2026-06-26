#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股情绪分析脚本
支持：北向资金、龙虎榜、市场情绪指标
"""

import requests
import json
import time
from typing import Dict, List, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AShareSentimentAnalyzer:
    """A股情绪分析器"""

    # 东方财富北向资金API
    NORTHBOUND_URL = "http://datacenter-web.eastmoney.com/api/data/v1/get"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

    def fetch_northbound_flow(self, date: Optional[str] = None) -> Optional[Dict]:
        """
        获取北向资金流向
        date: 日期，格式YYYYMMDD，默认为今天
        """
        try:
            if not date:
                date = datetime.now().strftime("%Y%m%d")

            params = {
                "reportName": "RPT_LIVE_NORTHBOUND_FLOW",
                "columns": "ALL",
                "filters": f"(trade_date='{date}')",
                "pageNumber": "1",
                "pageSize": "1000",
                "sortColumns": "ts_code",
                "sortTypes": "-1"
            }

            response = self.session.get(self.NORTHBOUND_URL, params=params, timeout=10)
            data = response.json()

            if data.get("result") and data["result"].get("data"):
                records = data["result"]["data"]
                total_inflow = 0
                net_inflow = 0
                stock_count = len(records)

                for record in records:
                    total_inflow += record.get("total_amt", 0)  # 总成交额
                    net_inflow += record.get("net_amt", 0)  # 净买入

                return {
                    "date": date,
                    "stock_count": stock_count,
                    "total_inflow": total_inflow / 100000000,  # 转换为亿元
                    "net_inflow": net_inflow / 100000000,
                    "avg_net_inflow": net_inflow / stock_count / 100000000 if stock_count > 0 else 0,
                }

        except Exception as e:
            logger.error(f"获取北向资金数据失败: {e}")

        return None

    def fetch_market_sentiment(self) -> Optional[Dict]:
        """
        获取市场整体情绪指标
        """
        try:
            # 东方财富市场情绪API
            params = {
                "reportName": "RPT_DATA_MKT_EMOTION",
                "columns": "ALL",
                "pageNumber": "1",
                "pageSize": "1000",
            }

            response = self.session.get(self.NORTHBOUND_URL, params=params, timeout=10)
            data = response.json()

            if data.get("result") and data["result"].get("data"):
                records = data["result"]["data"]
                if records:
                    record = records[0]
                    return {
                        "date": record.get("trade_date"),
                        "bullish_ratio": record.get("bullish_ratio", 0),  # 看多比例
                        "bearish_ratio": record.get("bearish_ratio", 0),  # 看空比例
                        "neutral_ratio": record.get("neutral_ratio", 0),  # 观望比例
                        "market_sentiment": "bullish" if record.get("bullish_ratio", 0) > 50 else "bearish" if record.get("bearish_ratio", 0) > 50 else "neutral",
                    }

        except Exception as e:
            logger.error(f"获取市场情绪数据失败: {e}")

        return None

    def fetch_l2h_list(self, date: Optional[str] = None, limit: int = 50) -> Optional[List[Dict]]:
        """
        获取龙虎榜数据
        date: 日期，格式YYYYMMDD，默认为今天
        limit: 返回条数
        """
        try:
            if not date:
                date = datetime.now().strftime("%Y%m%d")

            params = {
                "reportName": "RPT_L2H_L2H_LIST",
                "columns": "ALL",
                "filters": f"(trade_date='{date}')",
                "pageNumber": "1",
                "pageSize": str(limit),
                "sortColumns": "change_percent",
                "sortTypes": "-1"
            }

            response = self.session.get(self.NORTHBOUND_URL, params=params, timeout=10)
            data = response.json()

            if data.get("result") and data["result"].get("data"):
                records = data["result"]["data"]
                l2h_list = []

                for record in records:
                    l2h_list.append({
                        "code": record.get("ts_code"),
                        "name": record.get("sec_name"),
                        "change_percent": record.get("change_percent"),
                        "limit_type": record.get("l2h_type"),
                        "net_amount": record.get("net_amount"),
                        "buy_amount": record.get("buy_amount"),
                        "sell_amount": record.get("sell_amount"),
                        "deal_amount": record.get("deal_amount"),
                    })

                return l2h_list

        except Exception as e:
            logger.error(f"获取龙虎榜数据失败: {e}")

        return None

    def analyze_sentiment_summary(self, date: Optional[str] = None) -> Dict:
        """
        综合情绪分析
        """
        result = {
            "date": date or datetime.now().strftime("%Y-%m-%d"),
            "northbound": self.fetch_northbound_flow(date),
            "market_sentiment": self.fetch_market_sentiment(),
            "l2h_list": self.fetch_l2h_list(date, limit=20),
        }

        # 情绪判断
        if result["northbound"]:
            net_inflow = result["northbound"]["net_inflow"]
            if net_inflow > 10:
                northbound_signal = "强势流入"
            elif net_inflow > 0:
                northbound_signal = "小幅流入"
            elif net_inflow > -10:
                northbound_signal = "小幅流出"
            else:
                northbound_signal = "强势流出"

            result["northbound"]["signal"] = northbound_signal

        if result["market_sentiment"]:
            sentiment = result["market_sentiment"]["market_sentiment"]
            result["market_sentiment"]["signal"] = sentiment.upper()

        return result


if __name__ == "__main__":
    analyzer = AShareSentimentAnalyzer()

    # 测试：获取市场情绪数据
    print("=" * 60)
    print("A股市场情绪分析")
    print("=" * 60)

    sentiment = analyzer.analyze_sentiment_summary()

    print(f"日期: {sentiment['date']}")
    print()

    # 北向资金
    if sentiment["northbound"]:
        nb = sentiment["northbound"]
        print("北向资金:")
        print(f"  涨跌家数: {nb['stock_count']}")
        print(f"  总成交额: {nb['total_inflow']:.2f}亿元")
        print(f"  净流入: {nb['net_inflow']:+.2f}亿元")
        print(f"  平均净流入: {nb['avg_net_inflow']:+.2f}亿元/只")
        print(f"  信号: {nb['signal']}")
        print()

    # 市场情绪
    if sentiment["market_sentiment"]:
        ms = sentiment["market_sentiment"]
        print("市场情绪:")
        print(f"  看多比例: {ms['bullish_ratio']:.2f}%")
        print(f"  看空比例: {ms['bearish_ratio']:.2f}%")
        print(f"  观望比例: {ms['neutral_ratio']:.2f}%")
        print(f"  信号: {ms['signal']}")
        print()

    # 龙虎榜
    if sentiment["l2h_list"]:
        print("龙虎榜上榜股票 (前20名):")
        for item in sentiment["l2h_list"]:
            print(f"  {item['name']} ({item['code']})")
            print(f"    涨跌幅: {item['change_percent']:.2f}%")
            print(f"    上榜类型: {item['limit_type']}")
            print(f"    净买入: {item['net_amount']:+.2f}万元")
            print(f"    买入额: {item['buy_amount']:.2f}万元")
            print(f"    卖出额: {item['sell_amount']:.2f}万元")
            print()
