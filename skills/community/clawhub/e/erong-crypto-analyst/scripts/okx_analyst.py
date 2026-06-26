#!/usr/bin/env python3
"""
OKX Trading Analyst - 完整技术分析
增加更多指标、详细报告和相关新闻
"""

import requests
import pandas as pd
import numpy as np
import argparse
from datetime import datetime
import re
import json
import sys

# API配置
import os
from dotenv import load_dotenv

# 加载环境变量（从 .env 文件）
load_dotenv()

# OKX API 配置（从环境变量读取，不要硬编码！）
API_KEY = os.getenv('OKX_API_KEY', '')
API_SECRET = os.getenv('OKX_API_SECRET', '')
BASE_URL = "https://www.okx.com"

# NS3 新闻API
NS3_BASE = "https://api.ns3.ai/feed"


class OKXAnalyzer:
    def __init__(self):
        if not API_KEY or not API_SECRET:
            print("⚠️  警告: OKX_API_KEY 和 OKX_API_SECRET 未设置")
            print("   请在项目根目录创建 .env 文件并添加:")
            print("   OKX_API_KEY=your-api-key")
            print("   OKX_API_SECRET=your-api-secret")
        self.session = requests.Session()
        self.session.headers.update({
            'OK-ACCESS-KEY': API_KEY,
            'Content-Type': 'application/json'
        })
        self.api_secret = API_SECRET
        self.base_url = BASE_URL

    def get_klines(self, symbol, bar="4H", limit=300):
        """获取K线数据"""
        url = f"{BASE_URL}/api/v5/market/history-candles"
        params = {"instId": symbol, "bar": bar, "limit": limit}

        try:
            response = self.session.get(url, params=params, timeout=30)
            data = response.json()

            if data["code"] == "0" and data["data"]:
                columns = ["timestamp", "open", "high", "low", "close", "vol", "vol_ccy", "vol_ccy_quote", "confirm"]
                df = pd.DataFrame(data["data"], columns=columns)
                df["timestamp"] = pd.to_datetime(df["timestamp"].astype(float), unit="ms")
                for col in ["open", "high", "low", "close", "vol"]:
                    df[col] = df[col].astype(float)
                return df.sort_values("timestamp").reset_index(drop=True)
        except Exception as e:
            print(f"Error: {e}")
        return None

    def calculate_indicators(self, df):
        """计算所有技术指标"""
        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else None

        indicators = {}

        # ==================== 1. 移动平均线 MA ====================
        for period in [5, 10, 20, 30, 60, 120]:
            df[f"MA{period}"] = df["close"].rolling(window=period).mean()
            indicators[f"MA{period}"] = df[f"MA{period}"].iloc[-1]

        # ==================== 2. 指数移动平均线 EMA ====================
        for period in [7, 12, 25, 99]:
            df[f"EMA{period}"] = df["close"].ewm(span=period, adjust=False).mean()
            indicators[f"EMA{period}"] = df[f"EMA{period}"].iloc[-1]

        # ==================== 3. MACD ====================
        ema12 = df["close"].ewm(span=12, adjust=False).mean()
        ema26 = df["close"].ewm(span=26, adjust=False).mean()
        df["MACD"] = ema12 - ema26
        df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
        df["MACD_Hist"] = df["MACD"] - df["MACD_Signal"]

        indicators["MACD"] = df["MACD"].iloc[-1]
        indicators["MACD_Signal"] = df["MACD_Signal"].iloc[-1]
        indicators["MACD_Hist"] = df["MACD_Hist"].iloc[-1]

        # MACD方向判断
        if len(df) >= 3:
            macd_trend = "开口扩大" if abs(df["MACD_Hist"].iloc[-1]) > abs(df["MACD_Hist"].iloc[-2]) else "开口收缩"
        else:
            macd_trend = "盘整"
        indicators["MACD_Trend"] = macd_trend

        # ==================== 4. RSI ====================
        for period in [6, 12, 24]:
            delta = df["close"].diff()
            gain = delta.where(delta > 0, 0).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            df[f"RSI{period}"] = 100 - (100 / (1 + rs))
            indicators[f"RSI{period}"] = df[f"RSI{period}"].iloc[-1]

        # ==================== 5. 布林带 ====================
        df["BB_Middle"] = df["close"].rolling(window=20).mean()
        bb_std = df["close"].rolling(window=20).std()
        df["BB_Upper"] = df["BB_Middle"] + (bb_std * 2)
        df["BB_Lower"] = df["BB_Middle"] - (bb_std * 2)
        df["BB_Width"] = (df["BB_Upper"] - df["BB_Lower"]) / df["BB_Middle"]
        df["BB_Position"] = (df["close"] - df["BB_Lower"]) / (df["BB_Upper"] - df["BB_Lower"])

        indicators["BB_Upper"] = df["BB_Upper"].iloc[-1]
        indicators["BB_Middle"] = df["BB_Middle"].iloc[-1]
        indicators["BB_Lower"] = df["BB_Lower"].iloc[-1]
        indicators["BB_Width"] = df["BB_Width"].iloc[-1]
        indicators["BB_Position"] = df["BB_Position"].iloc[-1]

        # 布林带信号
        bb_pos = indicators["BB_Position"]
        if bb_pos > 0.95:
            indicators["BB_Signal"] = "上轨突破，超买区域"
        elif bb_pos < 0.05:
            indicators["BB_Signal"] = "下轨支撑，超卖区域"
        elif bb_pos > 0.7:
            indicators["BB_Signal"] = "上半段运行，偏强"
        elif bb_pos < 0.3:
            indicators["BB_Signal"] = "下半段运行，偏弱"
        else:
            indicators["BB_Signal"] = "中轨附近震荡"

        # ==================== 6. KDJ 随机指标 ====================
        low_min = df["low"].rolling(window=9).min()
        high_max = df["high"].rolling(window=9).max()
        df["K"] = 100 * ((df["close"] - low_min) / (high_max - low_min))
        df["D"] = df["K"].rolling(window=3).mean()
        df["J"] = 3 * df["K"] - 2 * df["D"]

        indicators["K"] = df["K"].iloc[-1]
        indicators["D"] = df["D"].iloc[-1]
        indicators["J"] = df["J"].iloc[-1]

        # KDJ信号
        k, d = indicators["K"], indicators["D"]
        if k > 80 and d > 80:
            indicators["KDJ_Signal"] = "超买区域，警惕回调"
        elif k < 20 and d < 20:
            indicators["KDJ_Signal"] = "超卖区域，可能反弹"
        elif k > d and prev is not None and df["K"].iloc[-2] <= df["D"].iloc[-2]:
            indicators["KDJ_Signal"] = "KDJ金叉，买入信号"
        elif k < d and prev is not None and df["K"].iloc[-2] >= df["D"].iloc[-2]:
            indicators["KDJ_Signal"] = "KDJ死叉，卖出信号"
        else:
            indicators["KDJ_Signal"] = "中性区域"

        # ==================== 7. CCI 商品通道指标 ====================
        tp = (df["high"] + df["low"] + df["close"]) / 3
        sma_tp = tp.rolling(window=20).mean()
        mean_dev = tp.rolling(window=20).apply(lambda x: np.fabs(x - x.mean()).mean())
        df["CCI"] = (tp - sma_tp) / (0.015 * mean_dev)

        indicators["CCI"] = df["CCI"].iloc[-1]
        cci = indicators["CCI"]
        if cci > 100:
            indicators["CCI_Signal"] = "强势区域(CCI>+100)"
        elif cci < -100:
            indicators["CCI_Signal"] = "弱势区域(CCI<-100)"
        elif cci > 0:
            indicators["CCI_Signal"] = "多方控制区域"
        else:
            indicators["CCI_Signal"] = "空方控制区域"

        # ==================== 8. ATR 真实波动幅度 ====================
        high_low = df["high"] - df["low"]
        high_close = np.abs(df["high"] - df["close"].shift())
        low_close = np.abs(df["low"] - df["close"].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        df["ATR"] = true_range.rolling(window=14).mean()

        indicators["ATR"] = df["ATR"].iloc[-1]
        indicators["ATR_Pct"] = (df["ATR"].iloc[-1] / df["close"].iloc[-1]) * 100

        # ==================== 9. OBV 能量潮 ====================
        obv_change = np.where(df["close"] > df["close"].shift(1), df["vol"],
                              np.where(df["close"] < df["close"].shift(1), -df["vol"], 0))
        df["OBV"] = pd.Series(obv_change).cumsum()
        df["OBV_MA"] = df["OBV"].rolling(window=10).mean()

        indicators["OBV"] = df["OBV"].iloc[-1]
        indicators["OBV_MA"] = df["OBV_MA"].iloc[-1]
        indicators["OBV_Trend"] = "上升" if df["OBV"].iloc[-1] > df["OBV"].iloc[-5] else "下降"

        # ==================== 10. 成交量分析 ====================
        df["Vol_MA5"] = df["vol"].rolling(window=5).mean()
        df["Vol_MA20"] = df["vol"].rolling(window=20).mean()

        indicators["Vol_Current"] = df["vol"].iloc[-1]
        indicators["Vol_MA5"] = df["Vol_MA5"].iloc[-1]
        indicators["Vol_MA20"] = df["Vol_MA20"].iloc[-1]

        # 量能判断
        vol_ratio = df["vol"].iloc[-1] / df["Vol_MA20"].iloc[-1] if df["Vol_MA20"].iloc[-1] > 0 else 0
        if vol_ratio > 1.5:
            indicators["Vol_Signal"] = f"放量上涨({vol_ratio:.1f}x)"

            # 检查价格涨跌
            price_change = (df["close"].iloc[-1] - df["close"].iloc[-2]) / df["close"].iloc[-2] * 100
            if price_change > 0:
                indicators["Vol_Signal"] = f"放量上涨({vol_ratio:.1f}x)，价量配合"
            else:
                indicators["Vol_Signal"] = f"放量下跌({vol_ratio:.1f}x)，警惕"
        elif vol_ratio < 0.5:
            indicators["Vol_Signal"] = f"缩量整理({vol_ratio:.1f}x)"
        else:
            indicators["Vol_Signal"] = f"常态成交量({vol_ratio:.1f}x)"

        # ==================== 11. 支撑位和阻力位 ====================
        indicators["Support_Level"] = df["BB_Lower"].iloc[-1]
        indicators["Resistance_Level"] = df["BB_Upper"].iloc[-1]

        # 近期高低点
        indicators["High_20"] = df["high"].rolling(window=20).max().iloc[-1]
        indicators["Low_20"] = df["low"].rolling(window=20).min().iloc[-1]
        indicators["High_50"] = df["high"].rolling(window=50).max().iloc[-1]
        indicators["Low_50"] = df["low"].rolling(window=50).min().iloc[-1]

        # ==================== 12. 斐波那契回撤位 ====================
        high_20 = indicators["High_20"]
        low_20 = indicators["Low_20"]
        diff = high_20 - low_20

        indicators["Fib_236"] = high_20 - diff * 0.236
        indicators["Fib_382"] = high_20 - diff * 0.382
        indicators["Fib_500"] = high_20 - diff * 0.500
        indicators["Fib_618"] = high_20 - diff * 0.618
        indicators["Fib_786"] = high_20 - diff * 0.786

        # ==================== 13. 均线排列判断 ====================
        ma5 = indicators.get("MA5", 0)
        ma20 = indicators.get("MA20", 0)
        ma60 = indicators.get("MA60", 0)

        if ma5 > ma20 > ma60:
            indicators["MA_Arrangement"] = "多头排列(激进)"
        elif ma5 > ma20 and ma20 < ma60:
            indicators["MA_Arrangement"] = "混乱排列"
        elif ma5 < ma20 < ma60:
            indicators["MA_Arrangement"] = "空头排列(看跌)"
        elif ma20 > ma60 and ma5 < ma20:
            indicators["MA_Arrangement"] = "回调整理"
        else:
            indicators["MA_Arrangement"] = "震荡整理"

        # ==================== 14. 均线金叉死叉 ====================
        if len(df) >= 3:
            ma5_prev = df["MA5"].iloc[-2]
            ma20_prev = df["MA20"].iloc[-2]
            ma5_curr = indicators["MA5"]
            ma20_curr = indicators["MA20"]

            if ma5_curr > ma20_curr and ma5_prev <= ma20_prev:
                indicators["MA_Cross"] = "MA5上穿MA20，形成金叉"
            elif ma5_curr < ma20_curr and ma5_prev >= ma20_prev:
                indicators["MA_Cross"] = "MA5下穿MA20，形成死叉"
            elif ma5_curr > ma20_curr:
                indicators["MA_Cross"] = "MA5在MA20上方运行"
            else:
                indicators["MA_Cross"] = "MA5在MA20下方运行"
        else:
            indicators["MA_Cross"] = "数据不足"

        # ==================== 15. 年内涨跌幅 ====================
        indicators["Change_Year"] = (df["close"].iloc[-1] - df["close"].iloc[0]) / df["close"].iloc[0] * 100

        # ==================== 16. 波动率分析 ====================
        df["Returns"] = df["close"].pct_change()
        indicators["Volatility_20"] = (df["Returns"].rolling(window=20).std() * 100 * np.sqrt(365)).iloc[-1]  # 年化波动率

        return df, indicators

    def generate_signals(self, df, indicators):
        """生成综合交易信号"""
        signals = []
        strength = 0
        latest = df.iloc[-1]
        price = latest["close"]

        # ==================== 1. 趋势信号 (权重2) ====================

        # MA均线排列
        ma_arr = indicators.get("MA_Arrangement", "")
        if "多头排列" in ma_arr:
            signals.append({"type": "📈 趋势", "signal": "✅ 看涨", "desc": f"均线多头排列({ma_arr})", "weight": +3})
            strength += 3
        elif "空头排列" in ma_arr:
            signals.append({"type": "📉 趋势", "signal": "❌ 看跌", "desc": f"均线空头排列({ma_arr})", "weight": -3})
            strength -= 3
        elif "回调整理" in ma_arr:
            signals.append({"type": "📊 趋势", "signal": "⚠️ 回调", "desc": "中长期向上，短期回调", "weight": -1})
            strength -= 1

        # MA金叉死叉
        ma_cross = indicators.get("MA_Cross", "")
        if "金叉" in ma_cross:
            signals.append({"type": "📈 趋势", "signal": "✅ 看涨", "desc": ma_cross, "weight": +2})
            strength += 2
        elif "死叉" in ma_cross:
            signals.append({"type": "📉 趋势", "signal": "❌ 看跌", "desc": ma_cross, "weight": -2})
            strength -= 2

        # 价格vs MA60
        ma60 = indicators.get("MA60", 0)
        if price > ma60:
            signals.append({"type": "📈 趋势", "signal": "✅ 看涨", "desc": f"价格站稳MA60上方", "weight": +2})
            strength += 2
        else:
            signals.append({"type": "📉 趋势", "signal": "❌ 看跌", "desc": f"价格跌破MA60下方", "weight": -2})
            strength -= 2

        # EMA多空判断
        ema12 = indicators.get("EMA12", 0)
        ema25 = indicators.get("EMA25", 0)
        if ema12 > ema25:
            signals.append({"type": "📈 趋势", "signal": "✅ 看涨", "desc": "EMA12 > EMA25，短期多方控制", "weight": +1})
            strength += 1
        else:
            signals.append({"type": "📉 趋势", "signal": "❌ 看跌", "desc": "EMA12 < EMA25，短期空方控制", "weight": -1})
            strength -= 1

        # ==================== 2. 动量信号 (权重2) ====================

        # MACD
        macd = indicators.get("MACD", 0)
        macd_signal = indicators.get("MACD_Signal", 0)
        macd_hist = indicators.get("MACD_Hist", 0)

        if macd > macd_signal and macd_hist > 0:
            signals.append({"type": "⚡ 动量", "signal": "✅ 看涨", "desc": f"MACD零轴上方金叉(MACD={macd:.4f})", "weight": +2})
            strength += 2
        elif macd > macd_signal and macd_hist < 0:
            signals.append({"type": "⚡ 动量", "signal": "🟡 偏强", "desc": f"MACD零轴下方金叉，反弹中", "weight": +1})
            strength += 1
        elif macd < macd_signal and macd_hist < 0:
            signals.append({"type": "⚡ 动量", "signal": "❌ 看跌", "desc": f"MACD零轴下方死叉(MACD={macd:.4f})", "weight": -2})
            strength -= 2
        else:
            signals.append({"type": "⚡ 动量", "signal": "🟠 偏弱", "desc": f"MACD零轴上方死叉，回调中", "weight": -1})
            strength -= 1

        # RSI
        rsi14 = indicators.get("RSI14", 50)
        if rsi14 > 70:
            signals.append({"type": "🔥 RSI", "signal": "❌ 超买", "desc": f"RSI14={rsi14:.1f}，警惕回调风险", "weight": -2})
            strength -= 2
        elif rsi14 < 30:
            signals.append({"type": "🔥 RSI", "signal": "✅ 超卖", "desc": f"RSI14={rsi14:.1f}，关注反弹机会", "weight": +2})
            strength += 2
        elif rsi14 > 60:
            signals.append({"type": "🔥 RSI", "signal": "✅ 偏强", "desc": f"RSI14={rsi14:.1f}，多方控制", "weight": +1})
            strength += 1
        elif rsi14 < 40:
            signals.append({"type": "🔥 RSI", "signal": "❌ 偏弱", "desc": f"RSI14={rsi14:.1f}，空方控制", "weight": -1})
            strength -= 1
        else:
            signals.append({"type": "🔥 RSI", "signal": "⚪ 中性", "desc": f"RSI14={rsi14:.1f}，中性区域", "weight": 0})

        # KDJ
        kdj_sig = indicators.get("KDJ_Signal", "")
        if "金叉" in kdj_sig:
            signals.append({"type": "🎯 KDJ", "signal": "✅ 买入", "desc": kdj_sig, "weight": +2})
            strength += 2
        elif "死叉" in kdj_sig:
            signals.append({"type": "🎯 KDJ", "signal": "❌ 卖出", "desc": kdj_sig, "weight": -2})
            strength -= 2
        elif "超买" in kdj_sig:
            signals.append({"type": "🎯 KDJ", "signal": "⚠️ 警惕", "desc": kdj_sig, "weight": -1})
            strength -= 1
        elif "超卖" in kdj_sig:
            signals.append({"type": "🎯 KDJ", "signal": "💡 关注", "desc": kdj_sig, "weight": +1})
            strength += 1

        # CCI
        cci_sig = indicators.get("CCI_Signal", "")
        if "强势" in cci_sig:
            signals.append({"type": "📊 CCI", "signal": "✅ 强势", "desc": cci_sig, "weight": +1})
            strength += 1
        elif "弱势" in cci_sig:
            signals.append({"type": "📊 CCI", "signal": "❌ 弱势", "desc": cci_sig, "weight": -1})
            strength -= 1

        # ==================== 3. 波动率信号 (权重1) ====================

        # 布林带
        bb_sig = indicators.get("BB_Signal", "")
        bb_pos = indicators.get("BB_Position", 0.5)
        if "超买" in bb_sig:
            signals.append({"type": "📊 布林带", "signal": "⚠️ 超买", "desc": bb_sig, "weight": -1})
            strength -= 1
        elif "超卖" in bb_sig:
            signals.append({"type": "📊 布林带", "signal": "💡 超卖", "desc": bb_sig, "weight": +1})
            strength += 1
        elif "偏强" in bb_sig:
            signals.append({"type": "📊 布林带", "signal": "🟡 偏强", "desc": bb_sig, "weight": 0})
        elif "偏弱" in bb_sig:
            signals.append({"type": "📊 布林带", "signal": "🟠 偏弱", "desc": bb_sig, "weight": 0})

        # ATR波动率
        atr_pct = indicators.get("ATR_Pct", 0)
        if atr_pct > 5:
            signals.append({"type": "🌊 波动", "signal": "⚡ 高波动", "desc": f"ATR={atr_pct:.2f}%，波动剧烈", "weight": 0})
        elif atr_pct < 2:
            signals.append({"type": "🌊 波动", "signal": "📉 低波动", "desc": f"ATR={atr_pct:.2f}%，可能蓄势", "weight": 0})

        # ==================== 4. 成交量信号 (权重1) ====================

        vol_sig = indicators.get("Vol_Signal", "")
        if "价量配合" in vol_sig:
            signals.append({"type": "📊 成交量", "signal": "✅ 价量配合", "desc": vol_sig, "weight": +1})
            strength += 1
        elif "放量" in vol_sig and "上涨" in vol_sig:
            signals.append({"type": "📊 成交量", "signal": "🟡 偏强", "desc": vol_sig, "weight": 0})
        elif "放量" in vol_sig and "警惕" in vol_sig:
            signals.append({"type": "📊 成交量", "signal": "⚠️ 警惕", "desc": vol_sig, "weight": -1})
            strength -= 1
        elif "缩量" in vol_sig:
            signals.append({"type": "📊 成交量", "signal": "⚪ 观望", "desc": vol_sig, "weight": 0})

        # ==================== 5. 综合评分 ====================

        # 限制strength范围
        strength = max(-10, min(10, strength))

        return {
            "signals": signals,
            "strength": strength,
            "indicators": indicators,
            "recommendation": self._get_recommendation(strength, price, indicators),
            "latest_price": price
        }

    def _get_recommendation(self, strength, price, indicators):
        """获取详细交易建议"""
        # 止损计算 (基于ATR)
        atr = indicators.get("ATR", price * 0.02)
        stop_loss_pct = atr / price

        if strength >= 7:
            return {
                "signal": "强烈看涨",
                "emoji": "🟢",
                "action": "积极做多",
                "stop_loss": f"${price * (1 - stop_loss_pct * 1.5):.2f}",
                "target1": f"${price * 1.05:.2f} (+5%)",
                "target2": f"${price * 1.10:.2f} (+10%)",
                "risk_ratio": "优秀(>3:1)"
            }
        elif strength >= 4:
            return {
                "signal": "温和看涨",
                "emoji": "🟡",
                "action": "轻仓做多",
                "stop_loss": f"${price * (1 - stop_loss_pct * 2):.2f}",
                "target1": f"${price * 1.03:.2f} (+3%)",
                "target2": f"${price * 1.06:.2f} (+6%)",
                "risk_ratio": "良好(2-3:1)"
            }
        elif strength >= 1:
            return {
                "signal": "轻微看涨",
                "emoji": "🔵",
                "action": "观望或小仓",
                "stop_loss": f"${price * (1 - stop_loss_pct * 2):.2f}",
                "target1": f"${price * 1.02:.2f} (+2%)",
                "target2": f"${price * 1.04:.2f} (+4%)",
                "risk_ratio": "一般(1-2:1)"
            }
        elif strength <= -7:
            return {
                "signal": "强烈看跌",
                "emoji": "🔴",
                "action": "积极做空",
                "stop_loss": f"${price * (1 + stop_loss_pct * 1.5):.2f}",
                "target1": f"${price * 0.95:.2f} (-5%)",
                "target2": f"${price * 0.90:.2f} (-10%)",
                "risk_ratio": "优秀(>3:1)"
            }
        elif strength <= -4:
            return {
                "signal": "温和看跌",
                "emoji": "🟠",
                "action": "轻仓做空",
                "stop_loss": f"${price * (1 + stop_loss_pct * 2):.2f}",
                "target1": f"${price * 0.97:.2f} (-3%)",
                "target2": f"${price * 0.94:.2f} (-6%)",
                "risk_ratio": "良好(2-3:1)"
            }
        elif strength <= -1:
            return {
                "signal": "轻微看跌",
                "emoji": "🟣",
                "action": "观望或小仓",
                "stop_loss": f"${price * (1 + stop_loss_pct * 2):.2f}",
                "target1": f"${price * 0.98:.2f} (-2%)",
                "target2": f"${price * 0.96:.2f} (-4%)",
                "risk_ratio": "一般(1-2:1)"
            }
        else:
            return {
                "signal": "中性",
                "emoji": "⚪",
                "action": "观望为主",
                "stop_loss": "等待信号",
                "target1": "等待信号",
                "target2": "等待信号",
                "risk_ratio": "无明确信号"
            }


def format_report(symbol, timeframe, df, result, ns3_items=None, wire_items=None):
    """格式化输出完整报告"""
    if ns3_items is None:
        ns3_items = []
    if wire_items is None:
        wire_items = []
    
    indicators = result["indicators"]
    signals = result["signals"]
    rec = result["recommendation"]
    price = result["latest_price"]

    # 统计信号
    bullish = sum(1 for s in signals if "✅" in s["signal"] or "看涨" in s["signal"] or "偏强" in s["signal"] or "买入" in s["signal"] or "超卖" in s["signal"])
    bearish = sum(1 for s in signals if "❌" in s["signal"] or "看跌" in s["signal"] or "偏弱" in s["signal"] or "卖出" in s["signal"] or "超买" in s["signal"])
    neutral = len(signals) - bullish - bearish

    report = []
    report.append("")
    report.append("╔" + "═" * 66 + "╗")
    report.append("║" + " " * 10 + f"📊 {symbol} 完整技术分析报告" + " " * 20 + "║")
    report.append("║" + f"周期: {timeframe} | 数据: {len(df)}根K线 | {datetime.now().strftime('%Y-%m-%d %H:%M')}" + " " * 10 + "║")
    report.append("╚" + "═" * 66 + "╝")

    # ========== 1. 价格概览 ==========
    change_1 = (df["close"].iloc[-1] - df["close"].iloc[-2]) / df["close"].iloc[-2] * 100
    change_5 = (df["close"].iloc[-1] - df["close"].iloc[-5]) / df["close"].iloc[-5] * 100 if len(df) >= 5 else 0

    report.append("")
    report.append("┌─────────────────────────────────────────────────────────────────┐")
    report.append("│  💰 价格信息                                                    │")
    report.append("├─────────────────────────────────────────────────────────────────┤")
    report.append(f"│  当前价格:  ${price:,.4f}                                      │")
    report.append(f"│  1周期涨跌:  {change_1:+.2f}%                                       │")
    report.append(f"│  5周期涨跌:  {change_5:+.2f}%                                       │")
    report.append(f"│  年内涨跌:   {indicators.get('Change_Year', 0):+.2f}%                                       │")
    report.append("│  20周期高:  ${:.4f}  低: ${:.4f}               │".format(
        indicators.get("High_20", 0), indicators.get("Low_20", 0)))
    report.append("│  50周期高:  ${:.4f}  低: ${:.4f}               │".format(
        indicators.get("High_50", 0), indicators.get("Low_50", 0)))
    report.append("└─────────────────────────────────────────────────────────────────┘")

    # ========== 2. 均线系统 ==========
    report.append("")
    report.append("┌─────────────────────────────────────────────────────────────────┐")
    report.append("│  📈 均线系统 (MA)                                               │")
    report.append("├─────────────────────────────────────────────────────────────────┤")
    ma_str = "│  "
    for m in [5, 10, 20, 30, 60, 120]:
        v = indicators.get(f"MA{m}", 0)
        if price > v:
            ma_str += f"MA{m}:${v:,.4f} ✅  "
        else:
            ma_str += f"MA{m}:${v:,.4f} ❌  "
        if m % 30 == 0:
            ma_str += "│\n│  "
    report.append(ma_str.rstrip("│\n│  "))
    report.append("├─────────────────────────────────────────────────────────────────┤")
    report.append(f"│  均线排列: {indicators.get('MA_Arrangement', 'N/A'):<48}│")
    report.append(f"│  MA5/20:   {indicators.get('MA_Cross', 'N/A'):<48}│")
    report.append("└─────────────────────────────────────────────────────────────────┘")

    # ========== 3. EMA系统 ==========
    report.append("")
    report.append("┌─────────────────────────────────────────────────────────────────┐")
    report.append("│  📈 指数移动平均 (EMA)                                          │")
    report.append("├─────────────────────────────────────────────────────────────────┤")
    ema_str = f"│  EMA7: ${indicators.get('EMA7', 0):,.4f}  EMA12: ${indicators.get('EMA12', 0):,.4f}          │\n"
    ema_str += f"│  EMA25: ${indicators.get('EMA25', 0):,.4f}  EMA99: ${indicators.get('EMA99', 0):,.4f}         │"
    report.append(ema_str)
    report.append("└─────────────────────────────────────────────────────────────────┘")

    # ========== 4. MACD ==========
    report.append("")
    report.append("┌─────────────────────────────────────────────────────────────────┐")
    report.append("│  ⚡ MACD 指标                                                   │")
    report.append("├─────────────────────────────────────────────────────────────────┤")
    macd_val = indicators.get("MACD", 0)
    macd_sig = indicators.get("MACD_Signal", 0)
    macd_hist = indicators.get("MACD_Hist", 0)
    macd_trend = indicators.get("MACD_Trend", "")

    macd_state = "🟢 零轴上方" if macd_val > 0 else "🔴 零轴下方"
    report.append(f"│  MACD: {macd_val:+.6f}  Signal: {macd_sig:+.6f}  Hist: {macd_hist:+.6f}  │")
    report.append(f"│  状态: {macd_state:<50}│")
    report.append(f"│  动能: {macd_trend:<50}│")
    report.append("└─────────────────────────────────────────────────────────────────┘")

    # ========== 5. RSI ==========
    report.append("")
    report.append("┌─────────────────────────────────────────────────────────────────┐")
    report.append("│  🔥 RSI 相对强弱指标                                             │")
    report.append("├─────────────────────────────────────────────────────────────────┤")
    rsi6 = indicators.get("RSI6", 0)
    rsi14 = indicators.get("RSI14", 0)
    rsi24 = indicators.get("RSI24", 0)

    rsi_bar = ""
    for rsi_val, name in [(rsi6, "RSI6"), (rsi14, "RSI14"), (rsi24, "RSI24")]:
        if rsi_val > 70:
            status = "🔴超买"
        elif rsi_val < 30:
            status = "🟢超卖"
        elif rsi_val > 50:
            status = "🟡偏强"
        else:
            status = "🟠偏弱"
        rsi_bar += f"│  {name}: {rsi_val:5.1f} {status:<8}"

    report.append(rsi_bar)
    report.append("│  ─────────────────────────────────────────────────────────────── │")
    report.append("│  RSI区间: 0-30超卖 | 30-50偏弱 | 50-60中性 | 60-70偏强 | 70-100超买│")
    report.append("└─────────────────────────────────────────────────────────────────┘")

    # ========== 6. KDJ ==========
    report.append("")
    report.append("┌─────────────────────────────────────────────────────────────────┐")
    report.append("│  🎯 KDJ 随机指标                                                │")
    report.append("├─────────────────────────────────────────────────────────────────┤")
    k = indicators.get("K", 0)
    d = indicators.get("D", 0)
    j = indicators.get("J", 0)
    kdj_sig = indicators.get("KDJ_Signal", "")

    report.append(f"│  K: {k:5.1f}  D: {d:5.1f}  J: {j:5.1f}                               │")
    report.append(f"│  信号: {kdj_sig:<50}│")
    report.append("│  ─────────────────────────────────────────────────────────────── │")
    report.append("│  KDJ区间: 0-20超卖 | 20-80中性 | 80-100超买                          │")
    report.append("└─────────────────────────────────────────────────────────────────┘")

    # ========== 7. CCI ==========
    report.append("")
    report.append("┌─────────────────────────────────────────────────────────────────┐")
    report.append("│  📊 CCI 商品通道指标                                             │")
    report.append("├─────────────────────────────────────────────────────────────────┤")
    cci = indicators.get("CCI", 0)
    cci_sig = indicators.get("CCI_Signal", "")

    report.append(f"│  CCI(20): {cci:+8.1f}                                          │")
    report.append(f"│  信号: {cci_sig:<50}│")
    report.append("│  ─────────────────────────────────────────────────────────────── │")
    report.append("│  CCI区间: <-100弱势 | -100~+100中性 | >+100强势                      │")
    report.append("└─────────────────────────────────────────────────────────────────┘")

    # ========== 8. 布林带 ==========
    report.append("")
    report.append("┌─────────────────────────────────────────────────────────────────┐")
    report.append("│  📊 布林带 (BB)                                                  │")
    report.append("├─────────────────────────────────────────────────────────────────┤")
    bb_upper = indicators.get("BB_Upper", 0)
    bb_mid = indicators.get("BB_Middle", 0)
    bb_lower = indicators.get("BB_Lower", 0)
    bb_pos = indicators.get("BB_Position", 0) * 100
    bb_width = indicators.get("BB_Width", 0)
    bb_sig = indicators.get("BB_Signal", "")

    report.append(f"│  上轨: ${bb_upper:,.4f}                                        │")
    report.append(f"│  中轨: ${bb_mid:,.4f}  (MA20)                              │")
    report.append(f"│  下轨: ${bb_lower:,.4f}                                        │")
    report.append(f"│  位置: {bb_pos:5.1f}% (价格处于布林带位置)                        │")
    report.append(f"│  宽度: {bb_width:.4f} (波动率指标)                             │")
    report.append(f"│  信号: {bb_sig:<46}│")
    report.append("└─────────────────────────────────────────────────────────────────┘")

    # ========== 9. ATR ==========
    report.append("")
    report.append("┌─────────────────────────────────────────────────────────────────┐")
    report.append("│  🌊 ATR 真实波动幅度                                             │")
    report.append("├─────────────────────────────────────────────────────────────────┤")
    atr = indicators.get("ATR", 0)
    atr_pct = indicators.get("ATR_Pct", 0)

    report.append(f"│  ATR(14): ${atr:,.4f}                                          │")
    report.append(f"│  ATR占比: {atr_pct:.2f}% (波动占价格比例)                           │")
    report.append(f"│  年化波动率: {float(indicators.get('Volatility_20', 0)):.1f}%                               │")
    report.append("└─────────────────────────────────────────────────────────────────┘")

    # ========== 10. 成交量 ==========
    report.append("")
    report.append("┌─────────────────────────────────────────────────────────────────┐")
    report.append("│  📊 成交量分析                                                   │")
    report.append("├─────────────────────────────────────────────────────────────────┤")
    vol_curr = indicators.get("Vol_Current", 0)
    vol_ma5 = indicators.get("Vol_MA5", 0)
    vol_ma20 = indicators.get("Vol_MA20", 0)
    vol_sig = indicators.get("Vol_Signal", "")
    obv_trend = indicators.get("OBV_Trend", "")

    report.append(f"│  当前量: {vol_curr:,.0f}  MA5: {vol_ma5:,.0f}  MA20: {vol_ma20:,.0f}       │")
    report.append(f"│  OBV趋势: {obv_trend:<45}│")
    report.append(f"│  量能: {vol_sig:<50}│")
    report.append("└─────────────────────────────────────────────────────────────────┘")

    # ========== 11. 支撑阻力 ==========
    report.append("")
    report.append("┌─────────────────────────────────────────────────────────────────┐")
    report.append("│  🎯 支撑位与阻力位                                               │")
    report.append("├─────────────────────────────────────────────────────────────────┤")
    support = indicators.get("Support_Level", 0)
    resistance = indicators.get("Resistance_Level", 0)
    fib_236 = indicators.get("Fib_236", 0)
    fib_382 = indicators.get("Fib_382", 0)
    fib_500 = indicators.get("Fib_500", 0)
    fib_618 = indicators.get("Fib_618", 0)

    report.append(f"│  布林下轨支撑:  ${support:,.4f}                                 │")
    report.append(f"│  布林上轨阻力:  ${resistance:,.4f}                                 │")
    report.append("│  ─────────────────────────────────────────────────────────────── │")
    report.append(f"│  斐波那契回撤位:                                                 │")
    report.append(f"│    23.6%: ${fib_236:,.4f}                                     │")
    report.append(f"│    38.2%: ${fib_382:,.4f}                                     │")
    report.append(f"│    50.0%: ${fib_500:,.4f}                                     │")
    report.append(f"│    61.8%: ${fib_618:,.4f}                                     │")
    report.append("└─────────────────────────────────────────────────────────────────┘")

    # ========== 12. 信号汇总 ==========
    report.append("")
    report.append("╔" + "═" * 66 + "╗")
    report.append("║" + " " * 20 + "📋 技术信号汇总" + " " * 27 + "║")
    report.append("╠" + "═" * 66 + "╣")
    report.append(f"║  看涨信号: {bullish}个  |  看跌信号: {bearish}个  |  中性信号: {neutral}个          ║")
    report.append("╠" + "═" * 66 + "╣")

    # 分行显示所有信号
    for i, sig in enumerate(signals):
        line = f"║  {sig['type']} {sig['desc']}"
        line = line[:62] + " " * (62 - len(line)) + "║"
        report.append(line)

    report.append("╚" + "═" * 66 + "╝")

    # ========== 13. 最终建议 ==========
    report.append("")
    report.append("╔" + "═" * 66 + "╗")
    report.append("║" + " " * 18 + "🎯 综合交易建议" + " " * 29 + "║")
    report.append("╠" + "═" * 66 + "╣")
    report.append(f"║  {rec['emoji']} {rec['signal']}  (信号强度: {result['strength']:+d}/+10)                      ║")
    report.append(f"║  ───────────────────────────────────────────────────────────   ║")
    report.append(f"║  建议操作: {rec['action']:<50}║")
    report.append(f"║  止损价位: {rec['stop_loss']:<50}║")
    report.append(f"║  第一目标: {rec['target1']:<50}║")
    report.append(f"║  第二目标: {rec['target2']:<50}║")
    report.append(f"║  盈亏比: {rec['risk_ratio']:<54}║")
    report.append("╚" + "═" * 66 + "╝")
    report.append("")
    report.append("⚠️ 风险提示: 技术分析仅供参考，不构成投资建议。市场有风险，投资需谨慎。")

    # ========== 14. 相关新闻 ==========
    if ns3_items or wire_items:
        news_lines = format_news_section(ns3_items, wire_items, symbol)
        report.extend(news_lines)

    return "\n".join(report)


def extract_base_symbol(symbol):
    """从交易对中提取基础币种符号"""
    # 移除 -USDT-SWAP, -USDT, -SWAP 等后缀
    clean = re.sub(r'[-_](USDT|SWAP|USD|USDT-SWAP)', '', symbol, flags=re.IGNORECASE)
    return clean.upper()


def time_ago(pub_date):
    """将时间转换为"XX分钟前"格式"""
    if not pub_date:
        return ""
    try:
        from time import mktime
        diff = (datetime.now().timestamp() - datetime.fromisoformat(pub_date.replace('Z', '+00:00')).timestamp())
        if diff < 60:
            return f"{int(diff)}秒前"
        elif diff < 3600:
            return f"{int(diff / 60)}分钟前"
        elif diff < 86400:
            return f"{int(diff / 3600)}小时前"
        else:
            return f"{int(diff / 86400)}天前"
    except:
        return pub_date


def parse_time_ago(time_str):
    """从'XX分钟前'/'XX小时前'/'XX天前'解析出总秒数"""
    if not time_str:
        return None
    try:
        if '秒前' in time_str:
            num = int(time_str.replace('秒前', '').strip())
            return num
        elif '分钟前' in time_str:
            num = int(time_str.replace('分钟前', '').strip())
            return num * 60
        elif '小时前' in time_str:
            num = int(time_str.replace('小时前', '').strip())
            return num * 3600
        elif '天前' in time_str:
            num = int(time_str.replace('天前', '').strip())
            return num * 86400
        return None
    except:
        return None


def fetch_crypto_news(symbol, limit=5, lang='zh-CN', max_age_hours=24):
    """从NS3 API获取加密货币新闻 (通过Node.js脚本)
    只保留最近 max_age_hours 小时内的新闻"""
    import subprocess
    base_symbol = extract_base_symbol(symbol)
    
    try:
        # 调用Node.js脚本获取新闻，获取更多然后过滤
        script_path = '/Users/yirongcao/.openclaw/skills/crypto-monitor/scripts/news.js'
        cmd = ['node', script_path, f'--coin={base_symbol}', f'--lang={lang}', f'--limit={max(20, limit * 4)}']
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            return []
        
        output = result.stdout
        
        # 解析Node.js输出
        items = []
        lines = output.split('\n')
        
        current_item = {}
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 解析emoji级别的新闻
            if line.startswith('🟡') or line.startswith('🔴') or line.startswith('⚪'):
                if current_item and 'title' in current_item:
                    # 过滤：只保留24小时内的新闻
                    seconds_ago = parse_time_ago(current_item.get('time_str', ''))
                    if seconds_ago is None or seconds_ago < max_age_hours * 3600:
                        items.append(current_item)
                # 提取标题
                title = line[2:].strip()  # 去掉emoji
                if title.startswith('📰'):
                    title = title[3:].strip()
                current_item = {'title': title[:60], 'level': '3' if line.startswith('🟡') else '4'}
            elif line.startswith('  ') and current_item:
                if '前' in line:
                    # 时间行
                    parts = line.strip().split('|')
                    for p in parts:
                        p = p.strip()
                        if '前' in p:
                            current_item['time_str'] = p
                        elif 'BTC' in p or 'ETH' in p or p.startswith('💰'):
                            current_item['coins'] = p.replace('💰', '').strip()
            
            # 提前停止如果已经够了
            if len(items) >= limit:
                break
        
        # 添加最后一个item（检查时间）
        if current_item and 'title' in current_item and len(items) < limit:
            seconds_ago = parse_time_ago(current_item.get('time_str', ''))
            if seconds_ago is None or seconds_ago < max_age_hours * 3600:
                items.append(current_item)
        
        # 如果过滤后太少，放宽限制到48小时
        if len(items) == 0 and max_age_hours < 48:
            return fetch_crypto_news(symbol, limit, lang, max_age_hours=48)
        
        return items[:limit]
    except Exception as e:
        print(f"  ⚠️ 新闻获取失败: {e}", file=sys.stderr)
        return []


def fetch_wire_news(symbol, limit=5, max_age_hours=24):
    """从通讯社RSS获取新闻
    只保留最近 max_age_hours 小时内的新闻"""
    import subprocess
    from datetime import datetime
    try:
        # 调用wire-news脚本，获取更多然后过滤
        script_path = '/Users/yirongcao/.openclaw/skills/wire-news-aggregator/scripts/wire_news.py'
        cmd = ['python3', script_path, '--limit', str(max(20, limit * 4)), '--json']
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            return []
        
        import json
        data = json.loads(result.stdout)
        
        items = []
        now = datetime.now()
        
        for item in data.get('news', []):
            # 清理标题
            title = item.get('title', '')[:55]
            source = item.get('source', '')
            source_color = item.get('source_color', '⚪')
            
            # 解析发布时间，过滤超过24小时的
            published_at = item.get('published_at', '')
            time_str = item.get('datetime', '')
            
            keep = True
            if published_at:
                try:
                    pub_dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                    pub_dt = pub_dt.astimezone()  # 转本地时间
                    diff = (now - pub_dt).total_seconds()
                    if diff > max_age_hours * 3600:
                        keep = False
                except:
                    pass  # 解析失败保留
            
            if title and keep:
                items.append({
                    'title': title,
                    'source': source,
                    'source_color': source_color,
                    'time_str': time_str,
                    'level': '3'  # 通讯社默认中等重要
                })
            
            if len(items) >= limit:
                break
        
        # 如果过滤后太少，放宽限制到48小时
        if len(items) == 0 and max_age_hours < 48:
            return fetch_wire_news(symbol, limit, max_age_hours=48)
        
        return items[:limit]
    except Exception as e:
        print(f"  ⚠️ 通讯社新闻获取失败: {e}", file=sys.stderr)
        return []


def format_news_section(ns3_items, wire_items, symbol):
    """格式化新闻部分 - 整合NS3和通讯社新闻"""
    if not ns3_items and not wire_items:
        return []
    
    lines = []
    
    lines.append("")
    lines.append("╔" + "═" * 66 + "╗")
    lines.append("║" + " " * 12 + f"📰 市场新闻汇总" + " " * 36 + "║")
    lines.append("╠" + "═" * 66 + "╣")
    
    # 计算总条目数
    total = len(ns3_items) + len(wire_items)
    lines.append(f"║  📊 共 {total} 条  |  🔵NS3: {len(ns3_items)}条  |  🟢通讯社: {len(wire_items)}条")
    lines.append("╠" + "═" * 66 + "╣")
    
    # 通讯社新闻优先显示 (更权威)
    if wire_items:
        lines.append("║  " + "─" * 62 + "  ║")
        lines.append("║  🟢 通讯社快讯 (权威来源)")
        lines.append("║  " + "─" * 62 + "  ║")
        
        for i, item in enumerate(wire_items[:3], 1):
            source_color = item.get('source_color', '⚪')
            source = item.get('source', '')
            title = item.get('title', '')
            time_str = item.get('time_str', '')
            
            lines.append(f"║  {source_color}[{source}] {title[:40]}")
            if time_str:
                lines.append(f"║      ⏰ {time_str}")
    
    # NS3加密货币新闻
    if ns3_items:
        lines.append("║  " + "─" * 62 + "  ║")
        lines.append("║  🔵 加密货币快讯 (NS3)")
        lines.append("║  " + "─" * 62 + "  ║")
        
        for i, item in enumerate(ns3_items[:3], 1):
            level = int(item.get('level', 4))
            if level <= 2:
                emoji = "🔴"
            elif level == 3:
                emoji = "🟡"
            else:
                emoji = "⚪"
            
            title = item.get('title', '')
            time_str = item.get('time_str', '')
            coins = item.get('coins', '')
            
            lines.append(f"║  {emoji} {title[:48]}")
            meta = [x for x in [time_str, coins] if x]
            if meta:
                lines.append(f"║      {' | '.join(meta)}")
    
    lines.append("╚" + "═" * 66 + "╝")
    
    return lines


def normalize_symbol(symbol):
    """标准化交易对格式"""
    # 移除空格
    symbol = symbol.strip().upper()
    
    # 如果已经包含 -USDT 或 -USDT-SWAP，直接返回
    if '-USDT-SWAP' in symbol:
        return symbol
    if '-USDT' in symbol:
        # 检查是否是永续合约
        return symbol + '-SWAP'
    
    # 处理 CLUSDT 格式 -> CL-USDT-SWAP
    if symbol.endswith('USDT'):
        base = symbol[:-4]
        return f"{base}-USDT-SWAP"
    
    # 处理纯字母如 CL -> CL-USDT-SWAP
    if len(symbol) <= 10 and symbol.isalpha():
        return f"{symbol}-USDT-SWAP"
    
    return symbol + '-SWAP'

def main():
    parser = argparse.ArgumentParser(description='OKX Trading Analyst - 完整技术分析')
    parser.add_argument('symbol', nargs='?', default='BTC-USDT', help='交易对 (如 BTC-USDT, CL-USDT-SWAP, CLUSDT)')
    parser.add_argument('-t', '--timeframe', default='4H', help='时间周期 (1m/5m/15m/30m/1H/4H/1D)')
    parser.add_argument('-l', '--limit', type=int, default=300, help='数据条数')
    parser.add_argument('-s', '--signal-only', action='store_true', help='只输出交易信号')
    parser.add_argument('-n', '--news', action='store_true', default=True, help='获取相关新闻 (默认开启)')
    parser.add_argument('--no-news', action='store_true', help='禁用新闻')
    args = parser.parse_args()

    # 标准化交易对格式
    original_symbol = args.symbol
    args.symbol = normalize_symbol(args.symbol)

    analyzer = OKXAnalyzer()

    print(f"🔍 正在获取 {original_symbol} -> {args.symbol} 数据 ({args.timeframe}周期)...\n")

    df = analyzer.get_klines(args.symbol, args.timeframe, args.limit)
    if df is None or len(df) < 30:
        print("❌ 数据获取失败或数据不足")
        return

    print(f"✅ 获取到 {len(df)} 条K线数据")
    print("🔄 正在计算技术指标...\n")

    df, indicators = analyzer.calculate_indicators(df)
    result = analyzer.generate_signals(df, indicators)

    # 获取相关新闻 - NS3 + 通讯社
    ns3_items = []
    wire_items = []
    if not args.no_news:
        print(f"📰 正在获取新闻 (NS3 + 通讯社) [过滤24小时内]...", file=sys.stderr)
        try:
            # NS3加密货币新闻 - 只保留24小时内
            ns3_items = fetch_crypto_news(args.symbol, limit=5, lang='zh-CN', max_age_hours=24)
            if not ns3_items:
                ns3_items = fetch_crypto_news(args.symbol, limit=5, lang='en', max_age_hours=24)
            if ns3_items:
                print(f"✅ NS3: {len(ns3_items)}条", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ NS3新闻获取失败: {e}", file=sys.stderr)
        
        try:
            # 通讯社新闻 - 只保留24小时内
            wire_items = fetch_wire_news(args.symbol, limit=3, max_age_hours=24)
            if wire_items:
                print(f"✅ 通讯社: {len(wire_items)}条", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ 通讯社新闻获取失败: {e}", file=sys.stderr)

    if args.signal_only:
        # 简洁输出
        print(f"\n{'='*50}")
        print(f"📊 {args.symbol} 交易信号")
        print(f"{'='*50}")
        print(f"价格: ${result['latest_price']:,.4f}")
        print(f"信号: {result['recommendation']['emoji']} {result['recommendation']['signal']}")
        print(f"强度: {result['strength']:+d}/+10")
        print(f"操作: {result['recommendation']['action']}")
        print(f"止损: {result['recommendation']['stop_loss']}")
        print(f"目标: {result['recommendation']['target1']}")
        print(f"{'='*50}")

        # 列出关键信号
        print("\n关键信号:")
        for sig in result['signals'][:8]:
            print(f"  {sig['type']} {sig['signal']} {sig['desc']}")
    else:
        # 完整报告
        report = format_report(args.symbol, args.timeframe, df, result, ns3_items, wire_items)
        print(report)


if __name__ == "__main__":
    main()
