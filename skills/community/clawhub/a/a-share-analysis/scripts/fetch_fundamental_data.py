#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股基本面数据获取脚本
支持：财务指标、估值分析、业绩分析
"""

import requests
import json
import time
from typing import Dict, List, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AShareFundamentalFetcher:
    """A股基本面数据获取器"""

    # 东方财富财务数据API
    EASTMONEY_FINANCE_URL = "http://push2his.eastmoney.com/api/qt/clist/get"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

    def fetch_financial_report(self, stock_code: str, report_type: str = "20231231") -> Optional[Dict]:
        """
        获取财务报表数据
        report_type: 财报类型，如 "20231231" (2023年报), "20230930" (2023三季报)
        """
        try:
            # 财务指标
            params = {
                "pn": 1,
                "pz": 100,
                "po": 1,
                "np": 1,
                "fltt": 2,
                "invt": 2,
                "fid": "f62",
                "fs": f"m:{stock_code}",
                "fields": "f12,f14,f57,f58,f59,f60,f61,f62,f63,f64,f65,f66,f67,f68,f69,f70,f71,f72,f73,f74,f75,f76,f77,f78,f79,f80,f81,f82,f83,f84,f85,f86,f87,f88,f89,f90,f91,f92,f93,f94,f95,f96,f97,f98,f99,f100,f101,f102,f103,f104,f105,f106,f107,f108,f109,f110,f111,f112,f113,f114,f115,f116,f117,f118,f119,f120,f121,f122,f123,f124,f125,f126,f127,f128,f129,f130,f131,f132,f133,f134,f135,f136,f137,f138,f139,f140,f141,f142,f143,f144,f145,f146,f147,f148,f149,f150,f151,f152,f153,f154,f155,f156,f157,f158,f159,f160,f161,f162,f163,f164,f165,f166,f167,f168,f169,f170,f171,f172,f173,f174,f175,f176,f177,f178,f179,f180,f181,f182,f183,f184,f185,f186,f187,f188,f189,f190,f191,f192,f193,f194,f195,f196,f197,f198,f199,f200,f201,f202,f203,f204,f205,f206,f207,f208,f209,f210,f211,f212,f213,f214,f215,f216,f217,f218,f219,f220,f221,f222,f223,f224,f225,f226,f227,f228,f229,f230,f231,f232,f233,f234,f235,f236,f237,f238,f239,f240,f241,f242,f243,f244,f245,f246,f247,f248,f249,f250,f251,f252,f253,f254,f255,f256,f257,f258,f259,f260,f261,f262,f263,f264,f265,f266,f267,f268,f269,f270,f271,f272,f273,f274,f275,f276,f277,f278,f279,f280,f281,f282,f283,f284,f285,f286,f287,f288,f289,f290,f291,f292,f293,f294,f295,f296,f297,f298,f299,f300,f301,f302,f303,f304,f305,f306,f307,f308,f309,f310,f311,f312,f313,f314,f315,f316,f317,f318,f319,f320,f321,f322,f323,f324,f325,f326,f327,f328,f329,f330,f331,f332,f333,f334,f335,f336,f337,f338,f339,f340,f341,f342,f343,f344,f345,f346,f347,f348,f349,f350,f351,f352,f353,f354,f355,f356,f357,f358,f359,f360,f361,f362,f363,f364,f365,f366,f367,f368,f369,f370,f371,f372,f373,f374,f375,f376,f377,f378,f379,f380,f381,f382,f383,f384,f385,f386,f387,f388,f389,f390,f391,f392,f393,f394,f395,f396,f397,f398,f399,f400,f401,f402,f403,f404,f405,f406,f407,f408,f409,f410,f411,f412,f413,f414,f415,f416,f417,f418,f419,f420,f421,f422,f423,f424,f425,f426,f427,f428,f429,f430,f431,f432,f433,f434,f435,f436,f437,f438,f439,f440,f441,f442,f443,f444,f445,f446,f447,f448,f449,f450,f451,f452,f453,f454,f455,f456,f457,f458,f459,f460,f461,f462,f463,f464,f465,f466,f467,f468,f469,f470,f471,f472,f473,f474,f475,f476,f477,f478,f479,f480,f481,f482,f483,f484,f485,f486,f487,f488,f489,f490,f491,f492,f493,f494,f495,f496,f497,f498,f499,f500"
            }

            response = self.session.get(self.EASTMONEY_FINANCE_URL, params=params, timeout=10)
            data = response.json()

            if data.get("data") and data["data"].get("diff"):
                item = data["data"]["diff"][0]
                return {
                    "code": item.get("f12"),
                    "name": item.get("f14"),
                    "report_date": report_type,
                    "total_revenue": item.get("f57", 0),  # 营业总收入
                    "operating_revenue": item.get("f58", 0),  # 营业收入
                    "net_profit": item.get("f60", 0),  # 净利润
                    "total_profit": item.get("f61", 0),  # 利润总额
                    "total_revenue_growth": item.get("f63", 0),  # 营业收入同比增长
                    "net_profit_growth": item.get("f65", 0),  # 净利润同比增长
                    "roe": item.get("f67", 0),  # ROE
                    "debt_to_asset": item.get("f69", 0),  # 资产负债率
                    "gross_margin": item.get("f71", 0),  # 毛利率
                    "net_margin": item.get("f72", 0),  # 净利率
                    "return_on_asset": item.get("f74", 0),  # ROA
                    "current_ratio": item.get("f76", 0),  # 流动比率
                    "quick_ratio": item.get("f77", 0),  # 速动比率
                    "psr": item.get("f79", 0),  # 市销率
                    "pe_ttm": item.get("f80", 0),  # 市盈率TTM
                    "pb": item.get("f81", 0),  # 市净率
                    "market_cap": item.get("f25", 0),  # 总市值
                    "circulating_market_cap": item.get("f26", 0),  # 流通市值
                }

        except Exception as e:
            logger.error(f"获取股票 {stock_code} 财务数据失败: {e}")

        return None

    def calculate_valuation_metrics(self, stock_code: str, price: float) -> Optional[Dict]:
        """
        计算估值指标
        需要传入当前股价
        """
        financial = self.fetch_financial_report(stock_code)
        if not financial:
            return None

        market_cap = financial.get("market_cap", 0)
        net_profit = financial.get("net_profit", 0)
        operating_revenue = financial.get("operating_revenue", 0)

        return {
            "code": stock_code,
            "name": financial.get("name"),
            "current_price": price,
            "market_cap": market_cap,
            "pe": round(net_profit / price, 2) if price > 0 else 0,  # PE = 净利润 / 股价
            "pb": round(market_cap / (financial.get("total_assets", 1)), 2),  # PB = 市值 / 总资产
            "ps": round(market_cap / operating_revenue, 2) if operating_revenue > 0 else 0,  # PS = 市值 / 营收
            "roe": financial.get("roe", 0),
            "net_margin": financial.get("net_margin", 0),
            "debt_to_asset": financial.get("debt_to_asset", 0),
        }


if __name__ == "__main__":
    fetcher = AShareFundamentalFetcher()

    # 测试：获取贵州茅台财务数据
    stock_code = "600519"
    print("=" * 60)
    print(f"贵州茅台 ({stock_code}) 财务数据")
    print("=" * 60)

    # 假设当前股价为1800元
    price = 1800.0
    financial = fetcher.fetch_financial_report(stock_code)
    if financial:
        print(f"报告期: {financial['report_date']}")
        print(f"营业总收入: {financial['total_revenue']:,}")
        print(f"营业利润: {financial['operating_revenue']:,}")
        print(f"净利润: {financial['net_profit']:,}")
        print(f"营收同比增长: {financial['total_revenue_growth']:.2f}%")
        print(f"净利润同比增长: {financial['net_profit_growth']:.2f}%")
        print(f"ROE: {financial['roe']:.2f}%")
        print(f"毛利率: {financial['gross_margin']:.2f}%")
        print(f"净利率: {financial['net_margin']:.2f}%")
        print(f"ROA: {financial['return_on_asset']:.2f}%")
        print(f"资产负债率: {financial['debt_to_asset']:.2f}%")
        print(f"流动比率: {financial['current_ratio']:.2f}")
        print(f"速动比率: {financial['quick_ratio']:.2f}")
        print()

    # 计算估值指标
    print("=" * 60)
    print(f"估值指标 (股价: {price}元)")
    print("=" * 60)
    valuation = fetcher.calculate_valuation_metrics(stock_code, price)
    if valuation:
        print(f"当前价格: {valuation['current_price']:.2f}元")
        print(f"总市值: {valuation['market_cap']:,}")
        print(f"市盈率PE: {valuation['pe']:.2f}")
        print(f"市净率PB: {valuation['pb']:.2f}")
        print(f"市销率PS: {valuation['ps']:.2f}")
        print(f"ROE: {valuation['roe']:.2f}%")
        print(f"净利率: {valuation['net_margin']:.2f}%")
