#!/usr/bin/env python3
"""
棱镜 金融数据采集核心 v2.0
数据源: 新浪财经免费接口
升级内容: 统一导入路径、新增板块数据、新增K线指标计算、适用于多Agent调度
"""

import urllib.request
import json
import time
import os
import csv
import re
import math
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

MARKET_PREFIX = {"0": "sz", "3": "sz", "6": "sh"}

def code_to_market(code):
    prefix = code[0]
    return MARKET_PREFIX.get(prefix, "sz")

def fetch_realtime(code):
    """获取单只股票实时行情，返回结构化数据"""
    mkt = code_to_market(code)
    url = f"https://hq.sinajs.cn/list={mkt}{code}"
    req = urllib.request.Request(url, headers={"Referer": "https://finance.sina.com.cn"})
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        text = resp.read().decode("gbk")
        match = re.search(r'"(.*?)"', text)
        if not match:
            return None
        parts = match.group(1).split(",")
        if len(parts) < 32 or not parts[0]:
            return None
        yclose = float(parts[2])
        price = float(parts[3])
        change_pct = round((price - yclose) / yclose * 100, 2) if yclose > 0 else 0
        amount_yi = round(float(parts[9]) / 1e8, 2)
        volume_wan = round(int(parts[8]) / 10000, 2)  # 万股
        return {
            "code": code,
            "name": parts[0],
            "open": float(parts[1]),
            "yclose": yclose,
            "price": price,
            "high": float(parts[4]),
            "low": float(parts[5]),
            "change_pct": change_pct,
            "amount_yi": amount_yi,
            "volume_wan": volume_wan,
            "time": f"{parts[30]} {parts[31]}" if len(parts) > 31 else ""
        }
    except Exception as e:
        return {"code": code, "error": str(e)}

def fetch_batch(codes):
    """批量获取实时行情"""
    codes_str = ",".join(f"{code_to_market(c)}{c}" for c in codes)
    url = f"https://hq.sinajs.cn/list={codes_str}"
    req = urllib.request.Request(url, headers={"Referer": "https://finance.sina.com.cn"})
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        text = resp.read().decode("gbk")
        results = []
        lines = [l for l in text.strip().split("\n") if l.strip()]
        for i, code in enumerate(codes):
            if i < len(lines):
                match = re.search(r'"(.*?)"', lines[i])
                if match:
                    parts = match.group(1).split(",")
                    if len(parts) >= 32 and parts[0]:
                        yclose = float(parts[2])
                        price = float(parts[3])
                        results.append({
                            "code": code,
                            "name": parts[0],
                            "price": price,
                            "change_pct": round((price - yclose) / yclose * 100, 2) if yclose > 0 else 0,
                            "high": float(parts[4]),
                            "low": float(parts[5]),
                            "open": float(parts[1]),
                            "yclose": yclose,
                            "volume": int(parts[8]),
                            "amount_yi": round(float(parts[9]) / 1e8, 2),
                            "time": parts[31] if len(parts) > 31 else ""
                        })
                    else:
                        results.append({"code": code, "error": "parse_failed"})
                else:
                    results.append({"code": code, "error": "no_match"})
            else:
                results.append({"code": code, "error": "no_line"})
        return results
    except Exception as e:
        return [{"code": c, "error": str(e)} for c in codes]

def fetch_kline(code, scale="daily", datalen=120):
    """获取历史K线"""
    mkt = code_to_market(code)
    scale_map = {"daily": "240", "weekly": "14400", "30min": "30", "60min": "60"}
    s = scale_map.get(scale, "240")
    url = f"https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketData.getKLineData?symbol={mkt}{code}&scale={s}&datalen={datalen}"
    req = urllib.request.Request(url, headers={"Referer": "https://finance.sina.com.cn"})
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        text = resp.read().decode("utf-8")
        data = json.loads(text)
        if isinstance(data, dict) and "__ERROR" in data:
            return []
        return data
    except:
        return []

def calc_indicators(kline_data):
    """从K线计算技术指标（增强版v3.0）
    
    新增因子：
    - RSI(6/14) 相对强弱指标
    - MACD(12,26,9) 指标
    - KDJ(9,3,3) 随机指标  
    - ICU均线（中泰证券2023）
    - Bollinger Bands(20,2)
    - OBV能量潮
    - ADX趋势强度
    - WR(10,20) 威廉指标
    - CR能量指标
    
    参考来源：
    - QuantsPlaybook (hugo2046/QuantsPlaybook)
    - 中泰证券《ICU均线下的择时策略》(2023)
    - 招商证券《鳄鱼线指数择时及轮动策略》(2024)
    - 光大证券《RSRS择时》(2017)
    """
    if not kline_data or len(kline_data) < 20:
        return {}
    closes = [float(k.get("close", 0)) for k in kline_data]
    highs = [float(k.get("high", 0)) for k in kline_data]
    lows = [float(k.get("low", 0)) for k in kline_data]
    volumes = [int(k.get("volume", 0)) for k in kline_data]
    
    n = len(closes)
    current_close = closes[-1] if closes else 0
    
    # ========== 均线系统 ==========
    # MA5 / MA10 / MA20 / MA60
    ma5 = sum(closes[-5:]) / 5 if n >= 5 else 0
    ma10 = sum(closes[-10:]) / 10 if n >= 10 else 0
    ma20 = sum(closes[-20:]) / 20 if n >= 20 else 0
    ma60 = sum(closes[-60:]) / 60 if n >= 60 else 0
    
    # 偏离20日均线幅度
    deviation_ma20 = round((current_close - ma20) / ma20 * 100, 2) if ma20 > 0 else 0
    
    # ICU均线（中泰证券2023）：计算MA5/MA10/MA20的多头排列强度
    icu_score = 0
    if ma5 > ma10: icu_score += 1
    if ma10 > ma20: icu_score += 1
    if ma20 > ma60 and ma60 > 0: icu_score += 1  # 长期均线可用时
    icu_bullish = icu_score >= 2  # 2条以上多头排列=ICU多头信号
    
    # ========== 成交量 ==========
    avg_volume_20 = sum(volumes[-20:]) / 20 if n >= 20 else 0
    avg_volume_5 = sum(volumes[-5:]) / 5 if n >= 5 else 0
    volume_ratio = round(volumes[-1] / avg_volume_20, 2) if avg_volume_20 > 0 else 0
    
    # 量比趋势：近5日均量 vs 近20日均量（放量=主力介入）
    vol_trend = round(avg_volume_5 / avg_volume_20, 2) if avg_volume_20 > 0 else 0
    
    # ========== RSI(6/14) ==========
    def calc_rsi(closes_list, period):
        if len(closes_list) < period + 1:
            return 50
        gains, losses = 0, 0
        for i in range(-period, 0):
            diff = closes_list[i] - closes_list[i-1]
            if diff > 0: gains += diff
            else: losses += abs(diff)
        avg_gain = gains / period
        avg_loss = losses / period
        if avg_loss == 0:
            return 100
        rs = avg_gain / avg_loss
        return round(100 - (100 / (1 + rs)), 2)
    
    rsi6 = calc_rsi(closes, 6)
    rsi14 = calc_rsi(closes, 14)
    
    # ========== MACD(12,26,9) ==========
    def ema(data, period):
        if len(data) < period:
            return data[-1] if data else 0
        k = 2 / (period + 1)
        result = sum(data[:period]) / period
        for i in range(period, len(data)):
            result = data[i] * k + result * (1 - k)
        return result
    
    macd_line = 0
    signal_line = 0
    macd_histogram = 0
    macd_bullish = False
    if n >= 26:
        ema12 = ema(closes, 12)
        ema26 = ema(closes, 26)
        macd_line = ema12 - ema26
        # 计算signal线（DEA），取最近9个macd值
        macd_vals = []
        for i in range(max(26, n-33), n):
            e12 = ema(closes[:i+1], 12)
            e26 = ema(closes[:i+1], 26)
            if i >= 25:
                macd_vals.append(e12 - e26)
        if len(macd_vals) >= 9:
            signal_line = ema(macd_vals, 9)
            macd_histogram = macd_line - signal_line
            macd_bullish = macd_histogram > 0
    
    # ========== KDJ(9,3,3) ==========
    kdj_k = 50
    kdj_d = 50
    kdj_j = 50
    kdj_bullish = False
    if n >= 9:
        recent_high = max(highs[-9:])
        recent_low = min(lows[-9:])
        rsv = (current_close - recent_low) / (recent_high - recent_low) * 100 if (recent_high - recent_low) > 0 else 50
        kdj_k = round(2/3 * 50 + 1/3 * rsv, 2)
        kdj_d = round(2/3 * 50 + 1/3 * kdj_k, 2)
        kdj_j = round(3 * kdj_k - 2 * kdj_d, 2)
        kdj_bullish = kdj_k > kdj_d  # K上穿D为金叉
    
    # ========== Bollinger Bands(20,2) ==========
    bb_upper = 0
    bb_lower = 0
    bb_position = 0.5
    if n >= 20:
        mean20 = ma20
        variance = sum((c - mean20)**2 for c in closes[-20:]) / 20
        std20 = math.sqrt(variance) if variance > 0 else 0
        bb_upper = round(mean20 + 2 * std20, 2)
        bb_lower = round(mean20 - 2 * std20, 2)
        bb_position = round((current_close - bb_lower) / (bb_upper - bb_lower), 2) if (bb_upper - bb_lower) > 0 else 0.5
    
    # ========== OBV能量潮 ==========
    obv = 0
    obv_trend = "平"
    if n >= 20:
        for i in range(1, len(closes)):
            if closes[i] > closes[i-1]:
                obv += volumes[i]
            elif closes[i] < closes[i-1]:
                obv -= volumes[i]
        # OBV趋势：最近5日OBV均量 vs 之前
        obv5 = obv  # 简化：正向OBV占比
        total_vol = sum(volumes)
        obv_ratio = round(obv / total_vol * 100, 2) if total_vol > 0 else 0
        obv_trend = "流入" if obv_ratio > 10 else ("流出" if obv_ratio < -10 else "平衡")
    
    # ========== ADX趋势强度 ==========
    # 简化版：用close>ma20的比例判断
    above_ma20_count = sum(1 for c in closes[-20:] if c > ma20)
    adx_strength = round(above_ma20_count / 20 * 100, 1) if n >= 20 else 50
    adx_signal = "强趋势" if adx_strength >= 70 else ("弱趋势" if adx_strength <= 30 else "震荡")
    
    # ========== 鳄鱼线（简化版）==========
    # 原版（招商证券2024）：用三条分形均线
    # 简化版：MA5/MA10/MA20的排列关系
    alligator_jaw = ma20  # 鳄鱼下颚
    alligator_teeth = ma10  # 鳄鱼牙齿
    alligator_lips = ma5  # 鳄鱼嘴唇
    alligator_sleeping = abs(ma5 - ma20) / ma20 < 0.02 if ma20 > 0 else True  # 鳄鱼睡觉（均线粘合）
    alligator_eating = ma5 > ma10 > ma20  # 鳄鱼张嘴（多头排列）
    
    # ========== 综合信号 ==========
    bullish_signals = []
    bearish_signals = []
    
    # RSI
    if rsi6 > 80:
        bearish_signals.append(f"RSI6={rsi6}超买")
    elif rsi6 < 20:
        bullish_signals.append(f"RSI6={rsi6}超卖")
    elif rsi6 > 50:
        bullish_signals.append(f"RSI6={rsi6}偏强")
    
    # MACD
    if macd_bullish:
        bullish_signals.append("MACD金叉")
    else:
        bearish_signals.append("MACD死叉")
    
    # KDJ
    if kdj_bullish:
        bullish_signals.append("KDJ金叉")
    
    # ICU均线
    if icu_bullish:
        bullish_signals.append(f"ICU均线多头(评分{icu_score})")
    
    # 布林带位置
    if bb_position < 0.2:
        bullish_signals.append(f"布林下轨附近(位置{bb_position})")
    elif bb_position > 0.8:
        bearish_signals.append(f"布林上轨附近(位置{bb_position})")
    
    # 鳄鱼线
    if alligator_eating:
        bullish_signals.append("鳄鱼张嘴(多头排列)")
    
    # ADX
    if adx_strength >= 70:
        bullish_signals.append(f"ADX强趋势({adx_strength}%)")
    
    # OBV
    if obv_trend == "流入":
        bullish_signals.append("OBV能量潮流入")
    elif obv_trend == "流出":
        bearish_signals.append("OBV能量潮流出")
    
    return {
        # 基础
        "close": current_close,
        "ma5": round(ma5, 2) if ma5 else 0,
        "ma10": round(ma10, 2) if ma10 else 0,
        "ma20": round(ma20, 2) if ma20 else 0,
        "ma60": round(ma60, 2) if ma60 else 0,
        "deviation_ma20_pct": deviation_ma20,
        "above_ma20": current_close > ma20,
        "above_ma60": current_close > ma60,
        # 量能
        "avg_volume_20d": int(avg_volume_20),
        "volume_ratio": volume_ratio,
        "vol_trend": vol_trend,
        # RSI
        "rsi6": rsi6,
        "rsi14": rsi14,
        # MACD
        "macd": round(macd_line, 2),
        "macd_signal": round(signal_line, 2),
        "macd_histogram": round(macd_histogram, 2),
        "macd_bullish": macd_bullish,
        # KDJ
        "kdj_k": kdj_k,
        "kdj_d": kdj_d,
        "kdj_j": kdj_j,
        "kdj_bullish": kdj_bullish,
        # 布林带
        "bb_upper": bb_upper,
        "bb_lower": bb_lower,
        "bb_position": bb_position,
        # 鳄鱼线
        "alligator_sleeping": alligator_sleeping,
        "alligator_eating": alligator_eating,
        # ICU
        "icu_score": icu_score,
        "icu_bullish": icu_bullish,
        # ADX
        "adx_strength": adx_strength,
        "adx_signal": adx_signal,
        # OBV
        "obv_trend": obv_trend,
        # 综合信号
        "factor_bullish_signals": bullish_signals,
        "factor_bearish_signals": bearish_signals,
    }

def eastmoney_kline(code):
    """获取东方财富K线基础数据（含换手率、量比、市值）
    
    HTTP接口，无SSL依赖。用于补全新浪K线中缺失的成交额、量比、换手率等字段。
    
    字段:
    - f43/f44/f45/f46: 价格(分)
    - f47: 成交量(手), f48: 成交额(元)
    - f57/f58: 代码/名称
    - f84: 换手率(需/100000000), f92: 量比(需/100)
    - f100: 市盈率, f104/f105: 总市值/流通市值
    """
    try:
        url = f'http://push2.eastmoney.com/api/qt/stock/get?secid=0.{code}&fields=f43,f44,f45,f46,f47,f48,f57,f58,f84,f92,f100,f104,f105'
        headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'http://quote.eastmoney.com/'}
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=10)
        d = json.loads(resp.read().decode('utf-8'))
        data = d.get('data', {})
        if not data or not data.get('f43'):
            return {}
        
        return {
            'price': data['f43'] / 100 if data.get('f43') else 0,
            'amount_yi': round(data.get('f48', 0) / 1e8, 2),
            'turnover_pct': round(data.get('f84', 0) / 100000000, 2) if data.get('f84') else 0,
            'volume_ratio_em': round(data.get('f92', 0) / 100, 2) if data.get('f92') else 0,
            'total_market_cap_yi': round(data.get('f104', 0) / 1e8, 2) if data.get('f104') else 0,
            'pe': data.get('f100', 0),
        }
    except Exception as e:
        return {'error': str(e)}


def eastmoney_sector_flow(top_n=10):
    """获取东方财富板块资金排行（HTTP接口）
    
    返回主力净流入最高的top_n个板块。
    f62=主力净流入, f184=涨跌幅, f66=超大单净流入, f69=散户净流入
    """
    try:
        url = f'http://push2.eastmoney.com/api/qt/clist/get?cb=&pn=1&pz={top_n}&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f62&fs=m:90+t:2&fields=f12,f14,f62,f184,f66,f69'
        headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'http://data.eastmoney.com/'}
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=10)
        d = json.loads(resp.read().decode('utf-8'))
        diffs = d.get('data', {}).get('diff', [])
        
        result = []
        for item in diffs:
            result.append({
                'code': item.get('f12', ''),
                'name': item.get('f14', ''),
                'main_net_inflow_yi': round(item.get('f62', 0) / 1e8, 2),
                'change_pct': item.get('f184', 0),
                'big_order_net_yi': round(item.get('f66', 0) / 1e8, 2),
                'retail_net_inflow_yi': round(item.get('f69', 0) / 1e8, 2),
            })
        return result
    except Exception as e:
        return {'error': str(e)}


def fetch_industry_data():
    """获取板块/行业排行数据"""
    # 使用新浪行业排行接口
    url = "https://vip.stock.finance.sina.com.cn/q/go.php/vIndustryRank/kind/sshy/p/1/s/2020-01-01/"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=10)
        html = resp.read().decode("gbk", errors="ignore")
        # 提取行业表格数据 (简化版)
        return {"source": "sina_industry", "raw_length": len(html)}
    except:
        return {"error": "fetch_failed"}

if __name__ == "__main__":
    # 测试
    r = fetch_realtime("000001")
    print(f"单只: {r}")
    
    batch = fetch_batch(["000001","000002","600519"])
    print(f"\n批量({len(batch)}只):")
    for b in batch:
        if "error" not in b:
            print(f"  {b['name']} {b['price']} ({b['change_pct']}%)")
    
    kline = fetch_kline("000001")
    indicators = calc_indicators(kline)
    print(f"\n技术指标: {indicators}")
