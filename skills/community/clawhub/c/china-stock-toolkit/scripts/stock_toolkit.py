#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全球市场实时仪表盘 - 多源聚合引擎
Author: Lin Hui
Version: 2.0.0
"""

import json
import os
import re
import urllib.request
import urllib.error
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from news_aggregator import NewsAggregator


# ============================================================================
# 数据模型
# ============================================================================

@dataclass
class IndexData:
    """指数数据"""
    code: str
    name: str
    price: Decimal
    change: Decimal
    change_pct: Decimal
    volume: Optional[Decimal] = None
    amount: Optional[Decimal] = None
    source: str = "unknown"
    timestamp: str = ""


@dataclass
class StockData:
    """个股数据"""
    code: str
    name: str
    price: Decimal
    change: Decimal
    change_pct: Decimal
    open_price: Decimal
    high: Decimal
    low: Decimal
    volume: Decimal
    amount: Decimal
    ma5: Optional[Decimal] = None
    ma10: Optional[Decimal] = None
    ma20: Optional[Decimal] = None
    source: str = "unknown"


@dataclass
class PreciousMetalData:
    """贵金属数据"""
    code: str
    name: str
    price: Decimal
    change: Decimal
    change_pct: Decimal
    high: Decimal
    low: Decimal
    source: str = "tencent"


# ============================================================================
# 配置管理
# ============================================================================

class Config:
    """配置管理器"""
    
    def __init__(self):
        self.yahoo_api_key = os.getenv("YAHOO_API_KEY", "")
        self.alpha_vantage_key = os.getenv("ALPHA_VANTAGE_KEY", "")
        self.http_proxy = os.getenv("HTTP_PROXY", "")
        self.https_proxy = os.getenv("HTTPS_PROXY", "")
        
        # 默认佣金率（万分之三）
        self.commission_rate = Decimal("0.0003")
        # 印花税率（千分之0.5，仅卖出）
        self.stamp_tax_rate = Decimal("0.00005")
        # 过户费率（十万分之一）
        self.transfer_fee_rate = Decimal("0.00001")
        # 最低佣金（5元）
        self.min_commission = Decimal("5.00")
    
    def has_yahoo(self) -> bool:
        return bool(self.yahoo_api_key)
    
    def has_alpha_vantage(self) -> bool:
        return bool(self.alpha_vantage_key)
    
    def has_proxy(self) -> bool:
        return bool(self.http_proxy)


# ============================================================================
# 数据源管理器
# ============================================================================

class DataSourceManager:
    """可插拔多源数据管理器"""
    
    # A股指数代码映射
    A_INDEX_MAP = {
        "sh000001": ("上证指数", "sh000001"),
        "sz399001": ("深证成指", "sz399001"),
        "sz399006": ("创业板指", "sz399006"),
        "sh000688": ("科创50", "sh000688"),
        "sh899050": ("北证50", "sh899050"),
    }
    
    # 港股代码映射
    HK_INDEX_MAP = {
        "r_hkHSI": ("恒生指数", "HSI"),
    }
    
    # 贵金属代码映射
    PRECIOUS_MAP = {
        "hf_XAU": ("黄金", "XAU"),
        "hf_XAG": ("白银", "XAG"),
    }
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
    
    # ========================================================================
    # A股指数
    # ========================================================================
    
    def get_a_indices(self) -> List[IndexData]:
        """获取A股5大指数（多源聚合）"""
        results = []
        for code, (name, _) in self.A_INDEX_MAP.items():
            # 尝试腾讯数据源
            tencent_data = self._fetch_tencent_index(code, name)
            # 尝试新浪数据源
            sina_data = self._fetch_sina_index(code, name)
            
            # 交叉验证
            final_data = self._cross_validate_index(tencent_data, sina_data)
            if final_data:
                results.append(final_data)
        
        return results
    
    def _fetch_tencent_index(self, code: str, name: str) -> Optional[IndexData]:
        """从腾讯获取指数数据"""
        try:
            url = f"https://web.sqt.gtimg.cn/q={code}"
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
            })
            
            with urllib.request.urlopen(req, timeout=5) as response:
                content = response.read().decode('gbk')
                
                # 解析数据
                match = re.search(r'v_{}="([^"]+)"'.format(code), content)
                if not match:
                    return None
                
                parts = match.group(1).split('~')
                if len(parts) < 35:
                    return None
                
                price = Decimal(parts[3])
                pre_close = Decimal(parts[4])
                change = price - pre_close
                change_pct = (change / pre_close * 100) if pre_close != 0 else Decimal("0")
                
                return IndexData(
                    code=code,
                    name=name,
                    price=price,
                    change=change,
                    change_pct=change_pct,
                    volume=Decimal(parts[6]) if parts[6] else None,
                    amount=Decimal(parts[37]) if len(parts) > 37 and parts[37] else None,
                    source="tencent",
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
        except Exception as e:
            return None
    
    def _fetch_sina_index(self, code: str, name: str) -> Optional[IndexData]:
        """从新浪获取指数数据"""
        try:
            url = f"https://hq.sinajs.cn/list={code}"
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
            })
            
            with urllib.request.urlopen(req, timeout=5) as response:
                content = response.read().decode('gbk')
                
                match = re.search(r'="([^"]+)"', content)
                if not match:
                    return None
                
                parts = match.group(1).split(',')
                if len(parts) < 35:
                    return None
                
                price = Decimal(parts[3])
                pre_close = Decimal(parts[2])
                change = price - pre_close
                change_pct = (change / pre_close * 100) if pre_close != 0 else Decimal("0")
                
                return IndexData(
                    code=code,
                    name=name,
                    price=price,
                    change=change,
                    change_pct=change_pct,
                    volume=Decimal(parts[8]) if parts[8] else None,
                    amount=Decimal(parts[9]) if parts[9] else None,
                    source="sina",
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
        except Exception as e:
            return None
    
    def _cross_validate_index(self, *sources: Optional[IndexData]) -> Optional[IndexData]:
        """交叉验证多个数据源"""
        valid_sources = [s for s in sources if s is not None]
        
        if not valid_sources:
            return None
        
        if len(valid_sources) == 1:
            return valid_sources[0]
        
        # 取多数一致的价格
        prices = [float(s.price) for s in valid_sources]
        avg_price = sum(prices) / len(prices)
        
        # 找最接近平均值的数据源
        best = min(valid_sources, key=lambda s: abs(float(s.price) - avg_price))
        best.source = "+".join([s.source for s in valid_sources])
        
        return best
    
    # ========================================================================
    # 港股指数
    # ========================================================================
    
    def get_hk_indices(self) -> List[IndexData]:
        """获取港股恒生指数"""
        results = []
        for code, (name, _) in self.HK_INDEX_MAP.items():
            data = self._fetch_tencent_hk_index(code, name)
            if data:
                results.append(data)
        return results
    
    def _fetch_tencent_hk_index(self, code: str, name: str) -> Optional[IndexData]:
        """从腾讯获取港股指数数据"""
        try:
            url = f"https://web.sqt.gtimg.cn/q={code}"
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
            })
            
            with urllib.request.urlopen(req, timeout=5) as response:
                content = response.read().decode('gbk')
                
                match = re.search(r'v_{}="([^"]+)"'.format(code), content)
                if not match:
                    return None
                
                parts = match.group(1).split('~')
                if len(parts) < 10:
                    return None
                
                price = Decimal(parts[3])
                pre_close = Decimal(parts[4])
                change = price - pre_close
                change_pct = Decimal(parts[5]) if parts[5] else Decimal("0")
                
                return IndexData(
                    code=code,
                    name=name,
                    price=price,
                    change=change,
                    change_pct=change_pct,
                    volume=Decimal(parts[7]) if parts[7] else None,
                    amount=Decimal(parts[8]) if parts[8] else None,
                    source="tencent",
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
        except Exception as e:
            return None
    
    # ========================================================================
    # 贵金属
    # ========================================================================
    
    def get_precious_metals(self) -> List[PreciousMetalData]:
        """获取贵金属数据"""
        results = []
        for code, (name, _) in self.PRECIOUS_MAP.items():
            data = self._fetch_tencent_precious(code, name)
            if data:
                results.append(data)
        return results
    
    def _fetch_tencent_precious(self, code: str, name: str) -> Optional[PreciousMetalData]:
        """从腾讯获取贵金属数据"""
        try:
            url = f"https://web.sqt.gtimg.cn/q={code}"
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
            })
            
            with urllib.request.urlopen(req, timeout=5) as response:
                content = response.read().decode('gbk')
                
                match = re.search(r'v_{}="([^"]+)"'.format(code), content)
                if not match:
                    return None
                
                parts = match.group(1).split(',')
                if len(parts) < 8:
                    return None
                
                price = Decimal(parts[0])
                change_pct = Decimal(parts[1])
                change = price * change_pct / 100
                high = Decimal(parts[4])
                low = Decimal(parts[5])
                
                return PreciousMetalData(
                    code=code,
                    name=name,
                    price=price,
                    change=change,
                    change_pct=change_pct,
                    high=high,
                    low=low,
                    source="tencent"
                )
        except Exception as e:
            return None
    
    # ========================================================================
    # 个股数据
    # ========================================================================
    
    def get_stock(self, code: str) -> Optional[StockData]:
        """获取个股数据"""
        # 尝试腾讯
        data = self._fetch_tencent_stock(code)
        if data:
            return data
        
        # 尝试新浪
        data = self._fetch_sina_stock(code)
        return data
    
    def _fetch_tencent_stock(self, code: str) -> Optional[StockData]:
        """从腾讯获取个股数据"""
        try:
            url = f"https://web.sqt.gtimg.cn/q={code}"
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
            })
            
            with urllib.request.urlopen(req, timeout=5) as response:
                content = response.read().decode('gbk')
                
                match = re.search(r'v_{}="([^"]+)"'.format(code), content)
                if not match:
                    return None
                
                parts = match.group(1).split('~')
                if len(parts) < 45:
                    return None
                
                name = parts[1]
                price = Decimal(parts[3])
                pre_close = Decimal(parts[4])
                change = price - pre_close
                change_pct = (change / pre_close * 100) if pre_close != 0 else Decimal("0")
                
                return StockData(
                    code=code,
                    name=name,
                    price=price,
                    change=change,
                    change_pct=change_pct,
                    open_price=Decimal(parts[5]),
                    high=Decimal(parts[33]),
                    low=Decimal(parts[34]),
                    volume=Decimal(parts[6]),
                    amount=Decimal(parts[37]),
                    source="tencent"
                )
        except Exception as e:
            return None
    
    def _fetch_sina_stock(self, code: str) -> Optional[StockData]:
        """从新浪获取个股数据"""
        try:
            url = f"https://hq.sinajs.cn/list={code}"
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
            })
            
            with urllib.request.urlopen(req, timeout=5) as response:
                content = response.read().decode('gbk')
                
                match = re.search(r'="([^"]+)"', content)
                if not match:
                    return None
                
                parts = match.group(1).split(',')
                if len(parts) < 32:
                    return None
                
                name = parts[0]
                price = Decimal(parts[3])
                pre_close = Decimal(parts[2])
                change = price - pre_close
                change_pct = (change / pre_close * 100) if pre_close != 0 else Decimal("0")
                
                return StockData(
                    code=code,
                    name=name,
                    price=price,
                    change=change,
                    change_pct=change_pct,
                    open_price=Decimal(parts[1]),
                    high=Decimal(parts[4]),
                    low=Decimal(parts[5]),
                    volume=Decimal(parts[8]),
                    amount=Decimal(parts[9]),
                    source="sina"
                )
        except Exception as e:
            return None
    
    # ========================================================================
    # 美股/日韩（需配置）
    # ========================================================================
    
    def get_us_indices(self) -> List[IndexData]:
        """获取美股指数（需要配置YAHOO_API_KEY）"""
        if not self.config.has_yahoo():
            return []
        
        # TODO: 实现Yahoo Finance API调用
        return []
    
    def get_asia_indices(self) -> List[IndexData]:
        """获取日韩指数（需要配置YAHOO_API_KEY）"""
        if not self.config.has_yahoo():
            return []
        
        # TODO: 实现Yahoo Finance API调用
        return []


# ============================================================================
# 税费计算器
# ============================================================================

class TaxCalculator:
    """交易税费计算器"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
    
    def calculate_buy(self, amount: Decimal) -> Dict[str, Any]:
        """计算买入费用"""
        commission = max(amount * self.config.commission_rate, self.config.min_commission)
        transfer_fee = amount * self.config.transfer_fee_rate
        total = commission + transfer_fee
        
        return {
            "amount": float(amount),
            "commission": float(commission.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
            "stamp_tax": 0.0,
            "transfer_fee": float(transfer_fee.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
            "total_fee": float(total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
        }
    
    def calculate_sell(self, amount: Decimal) -> Dict[str, Any]:
        """计算卖出费用"""
        commission = max(amount * self.config.commission_rate, self.config.min_commission)
        stamp_tax = amount * self.config.stamp_tax_rate
        transfer_fee = amount * self.config.transfer_fee_rate
        total = commission + stamp_tax + transfer_fee
        
        return {
            "amount": float(amount),
            "commission": float(commission.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
            "stamp_tax": float(stamp_tax.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
            "transfer_fee": float(transfer_fee.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
            "total_fee": float(total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
        }
    
    def calculate_profit(
        self,
        buy_price: Decimal,
        sell_price: Decimal,
        volume: int
    ) -> Dict[str, Any]:
        """计算盈亏"""
        buy_amount = buy_price * volume
        sell_amount = sell_price * volume
        
        buy_fees = self.calculate_buy(buy_amount)
        sell_fees = self.calculate_sell(sell_amount)
        
        total_cost = buy_amount + Decimal(str(buy_fees["total_fee"]))
        total_revenue = sell_amount - Decimal(str(sell_fees["total_fee"]))
        
        profit = total_revenue - total_cost
        profit_pct = (profit / total_cost * 100) if total_cost != 0 else Decimal("0")
        
        return {
            "buy_price": float(buy_price),
            "sell_price": float(sell_price),
            "volume": volume,
            "buy_amount": float(buy_amount),
            "sell_amount": float(sell_amount),
            "buy_fees": buy_fees,
            "sell_fees": sell_fees,
            "total_cost": float(total_cost.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
            "total_revenue": float(total_revenue.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
            "profit": float(profit.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
            "profit_pct": float(profit_pct.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
        }


# ============================================================================
# 主入口
# ============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="全球市场实时仪表盘")
    parser.add_argument("--action", required=True, choices=[
        "indices", "hk", "precious", "us", "asia",
        "stock", "calc_tax", "all",
        "stock_news", "sector_news", "policy_news", "market_sentiment"
    ])
    parser.add_argument("--code", help="股票代码")
    parser.add_argument("--buy_price", type=float, help="买入价")
    parser.add_argument("--sell_price", type=float, help="卖出价")
    parser.add_argument("--volume", type=int, help="数量")
    parser.add_argument("--name", help="股票名称或板块名称")
    
    args = parser.parse_args()
    
    manager = DataSourceManager()
    calculator = TaxCalculator()
    
    if args.action == "indices":
        data = manager.get_a_indices()
        result = {
            "market": "A股指数",
            "data": [
                {
                    "code": d.code,
                    "name": d.name,
                    "price": float(d.price),
                    "change": float(d.change),
                    "change_pct": float(d.change_pct),
                    "source": d.source,
                    "timestamp": d.timestamp
                }
                for d in data
            ]
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.action == "hk":
        data = manager.get_hk_indices()
        result = {
            "market": "港股指数",
            "data": [
                {
                    "code": d.code,
                    "name": d.name,
                    "price": float(d.price),
                    "change": float(d.change),
                    "change_pct": float(d.change_pct),
                    "source": d.source
                }
                for d in data
            ]
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.action == "precious":
        data = manager.get_precious_metals()
        result = {
            "market": "贵金属",
            "data": [
                {
                    "code": d.code,
                    "name": d.name,
                    "price": float(d.price),
                    "change": float(d.change),
                    "change_pct": float(d.change_pct),
                    "high": float(d.high),
                    "low": float(d.low),
                    "source": d.source
                }
                for d in data
            ]
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.action == "stock":
        if not args.code:
            print(json.dumps({"error": "请提供股票代码 --code"}))
            return
        data = manager.get_stock(args.code)
        if data:
            result = {
                "code": data.code,
                "name": data.name,
                "price": float(data.price),
                "change": float(data.change),
                "change_pct": float(data.change_pct),
                "open": float(data.open_price),
                "high": float(data.high),
                "low": float(data.low),
                "volume": float(data.volume),
                "amount": float(data.amount),
                "source": data.source
            }
        else:
            result = {"error": f"无法获取 {args.code} 的数据"}
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.action == "calc_tax":
        if not all([args.buy_price, args.sell_price, args.volume]):
            print(json.dumps({"error": "请提供 --buy_price, --sell_price, --volume"}))
            return
        
        result = calculator.calculate_profit(
            Decimal(str(args.buy_price)),
            Decimal(str(args.sell_price)),
            args.volume
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.action == "all":
        # 获取所有市场数据
        a_indices = manager.get_a_indices()
        hk_indices = manager.get_hk_indices()
        precious = manager.get_precious_metals()
        
        result = {
            "A股指数": [
                {"name": d.name, "price": float(d.price), "change_pct": float(d.change_pct)}
                for d in a_indices
            ],
            "港股指数": [
                {"name": d.name, "price": float(d.price), "change_pct": float(d.change_pct)}
                for d in hk_indices
            ],
            "贵金属": [
                {"name": d.name, "price": float(d.price), "change_pct": float(d.change_pct)}
                for d in precious
            ]
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.action == "us":
        if not manager.config.has_yahoo():
            print(json.dumps({
                "error": "需要配置YAHOO_API_KEY环境变量才能查询美股数据",
                "hint": "export YAHOO_API_KEY=your_key_here"
            }, ensure_ascii=False, indent=2))
        else:
            data = manager.get_us_indices()
            result = {"market": "美股指数", "data": data}
            print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.action == "asia":
        if not manager.config.has_yahoo():
            print(json.dumps({
                "error": "需要配置YAHOO_API_KEY环境变量才能查询日韩数据",
                "hint": "export YAHOO_API_KEY=your_key_here"
            }, ensure_ascii=False, indent=2))
        else:
            data = manager.get_asia_indices()
            result = {"market": "日韩指数", "data": data}
            print(json.dumps(result, ensure_ascii=False, indent=2))

    # ========================================================================
    # 新闻聚合 + 情感分析
    # ========================================================================
    
    elif args.action == "stock_news":
        """个股新闻+情感分析"""
        if not args.code or not args.name:
            print(json.dumps({"error": "请提供 --code 和 --name"}))
            return
        aggregator = NewsAggregator()
        result = aggregator.get_stock_news_with_sentiment(args.code, args.name)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.action == "sector_news":
        """板块新闻+情感分析"""
        if not args.name:
            print(json.dumps({"error": "请提供 --name 板块名称"}))
            return
        aggregator = NewsAggregator()
        result = aggregator.get_sector_news_with_sentiment(args.name)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.action == "policy_news":
        """政策新闻+情感分析"""
        aggregator = NewsAggregator()
        result = aggregator.get_policy_news_with_sentiment()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.action == "market_sentiment":
        """市场整体情绪"""
        aggregator = NewsAggregator()
        result = aggregator.get_market_sentiment()
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
