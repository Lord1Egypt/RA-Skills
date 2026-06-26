#!/usr/bin/env python3
"""
财经数据获取脚本 - 钉钉优化版
支持：美股、A股、港股、外汇、大宗商品、加密货币
"""

import requests
import json
import time
import sys
from datetime import datetime

# 配置
SYMBOLS = {
    "纳指": {"code": "^IXIC", "currency": "USD", "market": "stock"},
    "道指": {"code": "^DJI", "currency": "USD", "market": "stock"},
    "美元指数": {"code": "DX-Y.NYB", "currency": "", "market": "forex"},
    "黄金": {"code": "GC=F", "currency": "USD", "market": "commodity"},
    "原油": {"code": "CL=F", "currency": "USD", "market": "commodity"},
    "比特币": {"code": "BTC-USD", "currency": "USD", "market": "crypto"},
    "沪指": {"code": "000001.SS", "currency": "CNY", "market": "stock"},
    "恒生": {"code": "^HSI", "currency": "HKD", "market": "stock"},
    "日经": {"code": "^N225", "currency": "JPY", "market": "stock"},
    "人民币/美元": {"code": "CNY=X", "currency": "", "market": "forex"},
}

def get_yahoo_data(symbol_info, max_retries=3):
    """获取数据，带重试"""
    symbol = symbol_info["code"]
    market = symbol_info.get("market", "stock")
    
    for attempt in range(max_retries):
        try:
            # 加密货币使用1小时数据获取24小时前价格
            if market == "crypto":
                url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1h&range=2d"
            else:
                url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=2d"
            
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=15)
            data = response.json()
            
            if "chart" in data and data["chart"]["result"]:
                result = data["chart"]["result"][0]
                meta = result["meta"]
                
                current = meta.get("regularMarketPrice", 0)
                previous = meta.get("previousClose", 0)
                
                # 从 indicators 获取价格
                if "indicators" in result and "quote" in result["indicators"]:
                    quotes = result["indicators"]["quote"][0]
                    if "close" in quotes and quotes["close"]:
                        closes = [c for c in quotes["close"] if c is not None]
                        if len(closes) >= 2:
                            if market == "crypto":
                                # 加密货币：24小时前的价格（约24个1小时数据点）
                                if len(closes) >= 24:
                                    previous = closes[-24]
                                else:
                                    previous = closes[0]
                            else:
                                # 股票：昨天收盘价
                                previous = closes[-2]
                
                change = current - previous if current and previous else 0
                change_pct = (change / previous * 100) if previous else 0
                
                return {
                    "price": current,
                    "previous": previous,
                    "change": change,
                    "change_pct": change_pct,
                    "currency": symbol_info.get("currency", "USD"),
                    "market": market,
                }
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Retry {attempt + 1}/{max_retries} for {symbol}...")
                time.sleep(1)
            else:
                print(f"Error: {symbol} failed after {max_retries} attempts")
    
    return None

def format_price(price, currency):
    if price is None:
        return "N/A"
    if currency == "USD":
        return f"${price:,.2f}"
    elif currency == "CNY":
        return f"¥{price:,.2f}"
    elif currency == "HKD":
        return f"HK${price:,.2f}"
    elif currency == "JPY":
        return f"¥{price:,.0f}"
    else:
        return f"{price:,.2f}"

def generate_report():
    report = []
    report.append(f"📊 实时财经数据 [{datetime.now().strftime('%Y-%m-%d %H:%M')}]\n")
    report.append("💡 数据来源: Yahoo Finance API\n")
    
    categories = [
        ("🇺🇸 美股指数", ["纳指", "道指"]),
        ("💵 外汇", ["美元指数", "人民币/美元"]),
        ("🪙 加密货币", ["比特币"]),
        ("🏆 大宗商品", ["黄金", "原油"]),
        ("🇨🇳 A股", ["沪指"]),
        ("🇭🇰 港股", ["恒生"]),
        ("🇯🇵 日股", ["日经"]),
    ]
    
    for category_name, symbols in categories:
        report.append(category_name)
        report.append("-" * 40)
        for name in symbols:
            data = get_yahoo_data(SYMBOLS[name])
            if data:
                emoji = "📈" if data["change"] >= 0 else "📉"
                market = data.get("market", "stock")
                # 加密货币显示"24h前"，其他显示"昨收"
                ref_label = "24h前" if market == "crypto" else "昨收"
                
                report.append(f"{emoji} {name}")
                report.append(f"   代码: {SYMBOLS[name]['code']}")
                report.append(f"   现价: {format_price(data['price'], data['currency'])}")
                report.append(f"   {ref_label}: {format_price(data['previous'], data['currency'])}")
                report.append(f"   涨跌: {data['change']:+.2f} ({data['change_pct']:+.2f}%)")
                report.append("")
            else:
                report.append(f"⚠️ {name}: 数据获取失败")
                report.append("")
        report.append("")
    
    return "\n".join(report)

if __name__ == "__main__":
    report = generate_report()
    print(report)
