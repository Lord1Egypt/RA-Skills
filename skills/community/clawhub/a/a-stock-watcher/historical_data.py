#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票历史数据获取模块

数据源：
- 腾讯财经 API（免费，支持 A 股/港股/美股）
- 新浪财经 API（免费，A 股）
"""

import requests
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional

def get_stock_history_tencent(stock_code: str, days: int = 60) -> Dict:
    """
    获取腾讯财经历史数据（K 线）
    
    Args:
        stock_code: 股票代码
        days: 获取天数，默认 60 天
    
    Returns:
        包含历史数据的字典
    """
    try:
        # 适配股票代码格式
        if stock_code.startswith('6'):
            tencent_code = f"sh{stock_code}"
        elif stock_code.startswith(('0', '3')):
            tencent_code = f"sz{stock_code}"
        else:
            return {"error": "仅支持 A 股代码"}
        
        # 腾讯历史数据 API
        # 日 K 线：q=sh600036&qt=1&begin=0&count=60
        url = f"http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={tencent_code},day,,,60,qfq"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://stockapp.finance.qq.com/"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        data = response.json()
        
        if data.get("code") == 0 and data.get("data"):
            stock_data = data["data"].get(tencent_code, {})
            klines = stock_data.get("day", [])
            
            if not klines:
                return {"error": "无历史数据"}
            
            # 解析 K 线数据
            # 格式：[日期，开盘，收盘，最高，最低，成交量，成交额，换手率]
            dates = []
            open_prices = []
            close_prices = []
            high_prices = []
            low_prices = []
            volumes = []
            
            for kline in klines[-days:]:
                dates.append(kline[0])
                open_prices.append(float(kline[1]))
                close_prices.append(float(kline[2]))
                high_prices.append(float(kline[3]))
                low_prices.append(float(kline[4]))
                volumes.append(int(float(kline[5]) * 100))  # 手
            
            return {
                "success": True,
                "source": "tencent",
                "code": stock_code,
                "dates": dates,
                "open": open_prices,
                "close": close_prices,
                "high": high_prices,
                "low": low_prices,
                "volume": volumes,
                "count": len(dates)
            }
        
        return {"error": "数据获取失败"}
    
    except Exception as e:
        return {"error": f"异常：{str(e)}"}


def get_stock_history_sina(stock_code: str, days: int = 60) -> Dict:
    """
    获取新浪财经历史数据（日 K 线）
    
    Args:
        stock_code: 股票代码
        days: 获取天数，默认 60 天
    
    Returns:
        包含历史数据的字典
    """
    try:
        # 适配股票代码格式
        if stock_code.startswith('6'):
            sina_code = f"sh{stock_code}"
        elif stock_code.startswith(('0', '3')):
            sina_code = f"sz{stock_code}"
        else:
            return {"error": "仅支持 A 股代码"}
        
        # 新浪财经历史数据 API
        # 日 K 线：symbol=sh600036&scale=240&datalen=60
        url = f"http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={sina_code}&scale=240&datalen={days}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            dates = []
            open_prices = []
            close_prices = []
            high_prices = []
            low_prices = []
            volumes = []
            
            for kline in data:
                dates.append(kline["day"])
                open_prices.append(float(kline["open"]))
                close_prices.append(float(kline["close"]))
                high_prices.append(float(kline["high"]))
                low_prices.append(float(kline["low"]))
                volumes.append(int(kline["volume"]))
            
            return {
                "success": True,
                "source": "sina",
                "code": stock_code,
                "dates": dates,
                "open": open_prices,
                "close": close_prices,
                "high": high_prices,
                "low": low_prices,
                "volume": volumes,
                "count": len(dates)
            }
        
        return {"error": "数据获取失败"}
    
    except Exception as e:
        return {"error": f"异常：{str(e)}"}


def get_stock_history(stock_code: str, days: int = 60, prefer_source: str = None) -> Dict:
    """
    获取股票历史数据 - 多数据源智能选择
    
    Args:
        stock_code: 股票代码
        days: 获取天数，默认 60 天
        prefer_source: 优先数据源 (可选)
    
    Returns:
        包含历史数据的字典
    """
    # 优先尝试腾讯，其次新浪
    sources = ["tencent", "sina"]
    if prefer_source and prefer_source in sources:
        sources.remove(prefer_source)
        sources.insert(0, prefer_source)
    
    for source in sources:
        try:
            if source == "tencent":
                result = get_stock_history_tencent(stock_code, days)
            else:
                result = get_stock_history_sina(stock_code, days)
            
            if result.get("success"):
                return result
        
        except Exception as e:
            print(f"[{source} 失败]: {e}")
            continue
    
    return {"error": f"所有数据源均失败（尝试：{', '.join(sources)}）"}


# ============== 测试 ==============
if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    print("=" * 60)
    print("历史数据模块测试")
    print("=" * 60)
    
    # 测试腾讯 API
    print("\n[测试] 腾讯财经 API - 600036")
    result_tc = get_stock_history_tencent("600036", 30)
    if result_tc.get("success"):
        print(f"✅ 获取成功：{result_tc['count']}天数据")
        print(f"最新日期：{result_tc['dates'][-1]}")
        print(f"最新收盘：{result_tc['close'][-1]:.2f}")
        print(f"30 日最高：{max(result_tc['high']):.2f}")
        print(f"30 日最低：{min(result_tc['low']):.2f}")
    else:
        print(f"❌ 失败：{result_tc.get('error')}")
    
    # 测试新浪 API
    print("\n[测试] 新浪财经 API - 600036")
    result_sina = get_stock_history_sina("600036", 30)
    if result_sina.get("success"):
        print(f"✅ 获取成功：{result_sina['count']}天数据")
        print(f"最新日期：{result_sina['dates'][-1]}")
        print(f"最新收盘：{result_sina['close'][-1]:.2f}")
    else:
        print(f"❌ 失败：{result_sina.get('error')}")
    
    # 测试智能选择
    print("\n[测试] 智能选择 - 002892 (科力尔)")
    result = get_stock_history("002892", 30)
    if result.get("success"):
        print(f"✅ 获取成功：{result['count']}天数据 (数据源：{result['source']})")
        print(f"最新收盘：{result['close'][-1]:.2f}")
    else:
        print(f"❌ 失败：{result.get('error')}")
