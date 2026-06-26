#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A 股技术分析脚本（免费数据源版）
使用东方财富网免费 API 获取技术指标数据
"""

import requests
import json
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AShareTechnicalAnalyzer:
    """A 股技术分析器 - 免费数据源版"""

    # 东方财富 API
    EASTMONEY_KLINE_URL = "http://push2his.eastmoney.com/api/qt/stock/kline/get"
    EASTMONEY_DETAIL_URL = "http://push2.eastmoney.com/api/qt/stock/get"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "http://quote.eastmoney.com/"
        })

    def fetch_kline_data(self, stock_code: str, period: str = "101") -> Optional[Dict]:
        """
        获取 K 线数据
        
        Args:
            stock_code: 股票代码 (格式：0.600519 或 1.000858)
            period: 周期 (101=日线，102=周线，103=月线)
        
        Returns:
            K 线数据字典
        """
        try:
            params = {
                "secid": stock_code,
                "klt": period,
                "fqt": "1",  # 前复权
                "beg": "19000101",
                "end": "20500101",
                "fields1": "f1,f2,f3,f4,f5,f6",
                "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
                "forcect": "1"
            }
            
            response = self.session.get(self.EASTMONEY_KLINE_URL, params=params, timeout=10)
            data = response.json()
            
            if data.get("data") and data["data"].get("klines"):
                klines = data["data"]["klines"]
                # 解析 K 线数据
                parsed_klines = []
                for line in klines[-60:]:  # 取最近 60 条
                    parts = line.split(",")
                    parsed_klines.append({
                        "date": parts[0],
                        "open": float(parts[1]),
                        "close": float(parts[2]),
                        "high": float(parts[3]),
                        "low": float(parts[4]),
                        "volume": float(parts[5]),
                        "amount": float(parts[6]),
                        "amplitude": float(parts[7]),
                        "change": float(parts[8]),
                        "change_percent": float(parts[9]),
                        "turnover": float(parts[10])
                    })
                
                return {
                    "stock_code": stock_code,
                    "klines": parsed_klines,
                    "count": len(parsed_klines)
                }
            
        except Exception as e:
            logger.error(f"获取 K 线数据失败：{e}")
        
        return None

    def calculate_ma(self, prices: List[float], period: int) -> Optional[float]:
        """计算移动平均线"""
        if len(prices) < period:
            return None
        return sum(prices[-period:]) / period

    def calculate_macd(self, prices: List[float]) -> Dict:
        """
        计算 MACD 指标
        
        MACD = 快线 (EMA12) - 慢线 (EMA26)
        Signal = MACD 的 9 日 EMA
        """
        if len(prices) < 26:
            return {"dif": 0, "dea": 0, "macd": 0, "signal": "unknown"}
        
        # 计算 EMA12
        ema12 = self._calculate_ema(prices, 12)
        # 计算 EMA26
        ema26 = self._calculate_ema(prices, 26)
        
        if ema12 is None or ema26 is None:
            return {"dif": 0, "dea": 0, "macd": 0, "signal": "unknown"}
        
        dif = ema12 - ema26
        
        # 计算 DEA (MACD 的 9 日 EMA)
        macd_values = []
        for i in range(26, len(prices)):
            e12 = self._calculate_ema(prices[:i+1], 12)
            e26 = self._calculate_ema(prices[:i+1], 26)
            if e12 and e26:
                macd_values.append(e12 - e26)
        
        dea = self._calculate_ema(macd_values, 9) if len(macd_values) >= 9 else dif * 0.9
        macd_bar = (dif - dea) * 2
        
        # 判断信号
        if dif > dea and dif > 0:
            signal = "bullish"
        elif dif < dea and dif < 0:
            signal = "bearish"
        elif dif > dea:
            signal = "golden_cross"
        else:
            signal = "dead_cross"
        
        return {
            "dif": round(dif, 4),
            "dea": round(dea, 4),
            "macd": round(macd_bar, 4),
            "signal": signal
        }

    def _calculate_ema(self, prices: List[float], period: int) -> Optional[float]:
        """计算指数移动平均"""
        if len(prices) < period:
            return None
        
        multiplier = 2 / (period + 1)
        ema = sum(prices[:period]) / period
        
        for price in prices[period:]:
            ema = (price - ema) * multiplier + ema
        
        return ema

    def calculate_rsi(self, prices: List[float], period: int = 14) -> Optional[float]:
        """计算 RSI 指标"""
        if len(prices) < period + 1:
            return None
        
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return round(rsi, 2)

    def analyze_technical_indicators(self, stock_code: str) -> Optional[Dict]:
        """
        综合分析技术指标
        
        Args:
            stock_code: 股票代码 (格式：0.600519 或 1.000858)
        
        Returns:
            技术指标分析结果
        """
        # 获取 K 线数据
        kline_data = self.fetch_kline_data(stock_code)
        
        if not kline_data or not kline_data.get("klines"):
            return None
        
        klines = kline_data["klines"]
        closes = [k["close"] for k in klines]
        highs = [k["high"] for k in klines]
        lows = [k["low"] for k in klines]
        volumes = [k["volume"] for k in klines]
        
        current_price = closes[-1]
        
        # 计算均线
        ma5 = self.calculate_ma(closes, 5)
        ma10 = self.calculate_ma(closes, 10)
        ma20 = self.calculate_ma(closes, 20)
        ma60 = self.calculate_ma(closes, 60)
        
        # 判断均线排列
        if ma5 and ma10 and ma20 and ma60:
            if ma5 > ma10 > ma20 > ma60:
                ma_arrangement = "多头排列"
            elif ma5 < ma10 < ma20 < ma60:
                ma_arrangement = "空头排列"
            else:
                ma_arrangement = "震荡整理"
        else:
            ma_arrangement = "数据不足"
        
        # 计算 MACD
        macd = self.calculate_macd(closes)
        
        # 计算 RSI
        rsi = self.calculate_rsi(closes)
        
        # 计算成交量比
        if len(volumes) >= 5:
            avg_volume = sum(volumes[-5:]) / 5
            volume_ratio = volumes[-1] / avg_volume if avg_volume > 0 else 1
        else:
            volume_ratio = 1
        
        # 判断趋势
        if ma5 and ma20:
            if current_price > ma5 > ma20:
                trend = "bullish"
            elif current_price < ma5 < ma20:
                trend = "bearish"
            else:
                trend = "neutral"
        else:
            trend = "unknown"
        
        # 计算支撑位和阻力位
        recent_lows = lows[-10:]
        recent_highs = highs[-10:]
        support = min(recent_lows) if recent_lows else current_price * 0.95
        resistance = max(recent_highs) if recent_highs else current_price * 1.05
        
        # 综合信号判断
        bullish_signals = 0
        bearish_signals = 0
        
        if trend == "bullish":
            bullish_signals += 1
        elif trend == "bearish":
            bearish_signals += 1
        
        if macd["signal"] in ["bullish", "golden_cross"]:
            bullish_signals += 1
        elif macd["signal"] in ["bearish", "dead_cross"]:
            bearish_signals += 1
        
        if rsi and rsi > 50:
            bullish_signals += 1
        elif rsi and rsi < 50:
            bearish_signals += 1
        
        if volume_ratio > 1.5:
            bullish_signals += 1
        elif volume_ratio < 0.5:
            bearish_signals += 1
        
        if bullish_signals > bearish_signals:
            signal = "bullish"
        elif bearish_signals > bullish_signals:
            signal = "bearish"
        else:
            signal = "neutral"
        
        return {
            "code": stock_code,
            "current_price": round(current_price, 2),
            "ma": {
                "5": round(ma5, 2) if ma5 else None,
                "10": round(ma10, 2) if ma10 else None,
                "20": round(ma20, 2) if ma20 else None,
                "60": round(ma60, 2) if ma60 else None
            },
            "ma_arrangement": ma_arrangement,
            "macd": macd,
            "rsi": rsi,
            "volume_ratio": round(volume_ratio, 2),
            "trend": trend,
            "support": round(support, 2),
            "resistance": round(resistance, 2),
            "signal": signal,
            "bullish_signals": bullish_signals,
            "bearish_signals": bearish_signals,
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


if __name__ == "__main__":
    analyzer = AShareTechnicalAnalyzer()
    
    print("=" * 60)
    print("A 股技术分析测试 (免费数据源)")
    print("=" * 60)
    
    # 测试股票 (正确格式：市场代码。股票代码)
    # 上海市场：1.600519, 深圳市场：0.000858
    test_stocks = [
        ("1.600519", "贵州茅台"),
        ("0.000858", "五粮液"),
        ("1.603258", "电魂网络")
    ]
    
    for code, name in test_stocks:
        print(f"\n分析 {name} ({code})...")
        result = analyzer.analyze_technical_indicators(code)
        
        if result:
            print(f"  当前价：{result['current_price']}")
            print(f"  趋势：{result['trend']}")
            print(f"  信号：{result['signal']}")
            print(f"  MACD: {result['macd']['signal']}")
            print(f"  RSI: {result['rsi']}")
            print(f"  支撑/阻力：{result['support']} / {result['resistance']}")
        else:
            print(f"  分析失败")
        
        time.sleep(0.5)
