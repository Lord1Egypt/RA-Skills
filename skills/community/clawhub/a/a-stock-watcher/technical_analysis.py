#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票技术分析模块
提供 20+ 常用技术指标计算

功能：
- MA (移动平均线)
- EMA (指数移动平均线)
- RSI (相对强弱指标)
- MACD (平滑异同移动平均线)
- BOLL (布林带)
- KDJ (随机指标)
- DMI (趋向指标)
- CCI (顺势指标)
- WR (威廉指标)
- ROC (变动率指标)
"""

import numpy as np
from typing import List, Dict, Optional, Tuple
from datetime import datetime

# ============== 基础指标 ==============

def MA(data: List[float], period: int = 5) -> List[float]:
    """
    移动平均线 (Moving Average)
    
    Args:
        data: 价格数据列表（通常是收盘价）
        period: 周期，默认 5
    
    Returns:
        MA 值列表
    """
    if len(data) < period:
        return []
    
    result = []
    for i in range(len(data) - period + 1):
        ma = sum(data[i:i+period]) / period
        result.append(ma)
    
    return result


def EMA(data: List[float], period: int = 12) -> List[float]:
    """
    指数移动平均线 (Exponential Moving Average)
    
    Args:
        data: 价格数据列表
        period: 周期，默认 12
    
    Returns:
        EMA 值列表
    """
    if len(data) < period:
        return []
    
    multiplier = 2 / (period + 1)
    ema = [sum(data[:period]) / period]  # 初始值为 SMA
    
    for price in data[period:]:
        ema.append((price - ema[-1]) * multiplier + ema[-1])
    
    return ema


# ============== 动量指标 ==============

def RSI(data: List[float], period: int = 14) -> List[float]:
    """
    相对强弱指标 (Relative Strength Index)
    
    判断超买超卖：
    - RSI > 70: 超买区，可能回调
    - RSI < 30: 超卖区，可能反弹
    
    Args:
        data: 价格数据列表（收盘价）
        period: 周期，默认 14
    
    Returns:
        RSI 值列表 (0-100)
    """
    if len(data) < period + 1:
        return []
    
    result = []
    gains = []
    losses = []
    
    # 计算涨跌幅
    for i in range(1, len(data)):
        change = data[i] - data[i-1]
        gains.append(max(0, change))
        losses.append(max(0, -change))
    
    # 初始平均
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    
    if avg_loss == 0:
        result.append(100)
    else:
        rs = avg_gain / avg_loss
        result.append(100 - (100 / (1 + rs)))
    
    # 后续使用平滑移动平均
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        
        if avg_loss == 0:
            result.append(100)
        else:
            rs = avg_gain / avg_loss
            result.append(100 - (100 / (1 + rs)))
    
    return result


def MACD(data: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
    """
    平滑异同移动平均线 (Moving Average Convergence Divergence)
    
    组成：
    - DIF: 快线 (EMA12 - EMA26)
    - DEA: 慢线 (DIF 的 9 日 EMA)
    - MACD 柱：(DIF - DEA) * 2
    
    用法：
    - DIF 上穿 DEA: 金叉，买入信号
    - DIF 下穿 DEA: 死叉，卖出信号
    
    Args:
        data: 价格数据列表
        fast: 快线周期，默认 12
        slow: 慢线周期，默认 26
        signal: 信号线周期，默认 9
    
    Returns:
        字典包含 dif, dea, macd_hist 列表
    """
    ema_fast = EMA(data, fast)
    ema_slow = EMA(data, slow)
    
    if len(ema_fast) < len(ema_slow):
        ema_fast = ema_fast[-len(ema_slow):]
    elif len(ema_slow) < len(ema_fast):
        ema_slow = ema_slow[-len(ema_fast):]
    
    # DIF = EMA(快) - EMA(慢)
    dif = [f - s for f, s in zip(ema_fast, ema_slow)]
    
    # DEA = DIF 的 EMA
    dea = EMA(dif, signal) if len(dif) >= signal else []
    
    # MACD 柱 = (DIF - DEA) * 2
    macd_hist = []
    if dea:
        # 对齐长度
        dif_aligned = dif[-len(dea):]
        macd_hist = [(d - e) * 2 for d, e in zip(dif_aligned, dea)]
    
    return {
        'dif': dif,
        'dea': dea,
        'macd_hist': macd_hist
    }


def KDJ(high: List[float], low: List[float], close: List[float], 
        n: int = 9, m1: int = 3, m2: int = 3) -> Dict:
    """
    随机指标 (Stochastic Oscillator)
    
    组成：
    - K: 快速确认线
    - D: 慢速主干线
    - J: 方向敏感线
    
    用法：
    - K > 80: 超买
    - K < 20: 超卖
    - K 上穿 D: 金叉
    - K 下穿 D: 死叉
    
    Args:
        high: 最高价列表
        low: 最低价列表
        close: 收盘价列表
        n: RSV 周期，默认 9
        m1: K 周期，默认 3
        m2: D 周期，默认 3
    
    Returns:
        字典包含 k, d, j 列表
    """
    if len(close) < n:
        return {'k': [], 'd': [], 'j': []}
    
    # 计算 RSV
    rsv = []
    for i in range(len(close) - n + 1):
        highest = max(high[i:i+n])
        lowest = min(low[i:i+n])
        if highest == lowest:
            rsv.append(50)
        else:
            rsv.append((close[i+n-1] - lowest) / (highest - lowest) * 100)
    
    # 计算 K, D, J
    k = [50]  # 初始值 50
    for r in rsv[1:]:
        k.append((k[-1] * (m1 - 1) + r) / m1)
    
    d = [50]  # 初始值 50
    for ki in k[1:]:
        d.append((d[-1] * (m2 - 1) + ki) / m2)
    
    j = [3 * ki - 2 * di for ki, di in zip(k, d)]
    
    return {'k': k, 'd': d, 'j': j}


# ============== 波动率指标 ==============

def BOLL(data: List[float], period: int = 20, width: float = 2.0) -> Dict:
    """
    布林带 (Bollinger Bands)
    
    组成：
    - 中轨：MA(period)
    - 上轨：中轨 + width * 标准差
    - 下轨：中轨 - width * 标准差
    
    用法：
    - 价格触及上轨：可能超买
    - 价格触及下轨：可能超卖
    - 带宽收窄：变盘前兆
    
    Args:
        data: 价格数据列表
        period: 周期，默认 20
        width: 标准差倍数，默认 2
    
    Returns:
        字典包含 upper, middle, lower 列表
    """
    if len(data) < period:
        return {'upper': [], 'middle': [], 'lower': []}
    
    middle = MA(data, period)
    upper = []
    lower = []
    
    for i in range(len(middle)):
        window = data[i:i+period]
        std = np.std(window)
        upper.append(middle[i] + width * std)
        lower.append(middle[i] - width * std)
    
    return {
        'upper': upper,
        'middle': middle,
        'lower': lower
    }


def ATR(high: List[float], low: List[float], close: List[float], period: int = 14) -> List[float]:
    """
    平均真实波幅 (Average True Range)
    
    衡量波动性，值越大波动越剧烈
    
    Args:
        high: 最高价列表
        low: 最低价列表
        close: 收盘价列表
        period: 周期，默认 14
    
    Returns:
        ATR 值列表
    """
    if len(close) < period + 1:
        return []
    
    tr = []
    for i in range(1, len(close)):
        tr1 = high[i] - low[i]
        tr2 = abs(high[i] - close[i-1])
        tr3 = abs(low[i] - close[i-1])
        tr.append(max(tr1, tr2, tr3))
    
    # 初始 ATR
    atr = [sum(tr[:period]) / period]
    
    # 后续使用平滑移动平均
    for i in range(period, len(tr)):
        atr.append((atr[-1] * (period - 1) + tr[i]) / period)
    
    return atr


# ============== 趋势指标 ==============

def DMI(high: List[float], low: List[float], close: List[float], 
        period: int = 14) -> Dict:
    """
    趋向指标 (Directional Movement Index)
    
    组成：
    - PDI: 上升方向线
    - MDI: 下降方向线
    - ADX: 平均趋向指数（趋势强度）
    - ADXR: ADX 的评估
    
    用法：
    - PDI 上穿 MDI: 买入信号
    - ADX > 25: 趋势明显
    - ADX < 20: 震荡行情
    
    Args:
        high: 最高价列表
        low: 最低价列表
        close: 收盘价列表
        period: 周期，默认 14
    
    Returns:
        字典包含 pdi, mdi, adx, adxr 列表
    """
    if len(close) < period * 2 + 1:
        return {'pdi': [], 'mdi': [], 'adx': [], 'adxr': []}
    
    n = len(close)
    
    # 计算 DM 和 TR
    plus_dm = [0]
    minus_dm = [0]
    tr = [0]
    
    for i in range(1, n):
        # +DM
        up_move = high[i] - high[i-1]
        down_move = low[i-1] - low[i]
        
        if up_move > down_move and up_move > 0:
            plus_dm.append(up_move)
        else:
            plus_dm.append(0)
        
        # -DM
        if down_move > up_move and down_move > 0:
            minus_dm.append(down_move)
        else:
            minus_dm.append(0)
        
        # TR
        tr1 = high[i] - low[i]
        tr2 = abs(high[i] - close[i-1])
        tr3 = abs(low[i] - close[i-1])
        tr.append(max(tr1, tr2, tr3))
    
    # 平滑处理
    plus_di = []
    minus_di = []
    
    # 初始值
    sum_plus = sum(plus_dm[1:period+1])
    sum_minus = sum(minus_dm[1:period+1])
    sum_tr = sum(tr[1:period+1])
    
    if sum_tr > 0:
        plus_di.append(sum_plus / sum_tr * 100)
        minus_di.append(sum_minus / sum_tr * 100)
    else:
        plus_di.append(0)
        minus_di.append(0)
    
    # 后续平滑
    for i in range(period, n-1):
        sum_plus = sum_plus - sum_plus / period + plus_dm[i+1]
        sum_minus = sum_minus - sum_minus / period + minus_dm[i+1]
        sum_tr = sum_tr - sum_tr / period + tr[i+1]
        
        if sum_tr > 0:
            plus_di.append(sum_plus / sum_tr * 100)
            minus_di.append(sum_minus / sum_tr * 100)
        else:
            plus_di.append(0)
            minus_di.append(0)
    
    # 计算 DX 和 ADX
    dx = []
    for p, m in zip(plus_di, minus_di):
        if p + m > 0:
            dx.append(abs(p - m) / (p + m) * 100)
        else:
            dx.append(0)
    
    adx = MA(dx, period)
    
    # ADXR
    adxr = []
    if len(adx) >= period:
        for i in range(len(adx) - period + 1):
            adxr.append((adx[i] + adx[i + period - 1]) / 2)
    
    return {
        'pdi': plus_di,
        'mdi': minus_di,
        'adx': adx,
        'adxr': adxr
    }


# ============== 其他常用指标 ==============

def CCI(high: List[float], low: List[float], close: List[float], period: int = 20) -> List[float]:
    """
    顺势指标 (Commodity Channel Index)
    
    用法：
    - CCI > 100: 超买
    - CCI < -100: 超卖
    
    Args:
        high: 最高价列表
        low: 最低价列表
        close: 收盘价列表
        period: 周期，默认 20
    
    Returns:
        CCI 值列表
    """
    if len(close) < period:
        return []
    
    result = []
    
    for i in range(len(close) - period + 1):
        # 计算典型价
        tp = [(high[i+j] + low[i+j] + close[i+j]) / 3 for j in range(period)]
        
        # 平均典型价
        ma_tp = sum(tp) / period
        
        # 平均偏差
        mean_dev = sum(abs(t - ma_tp) for t in tp) / period
        
        if mean_dev == 0:
            result.append(0)
        else:
            cci = (tp[-1] - ma_tp) / (0.015 * mean_dev)
            result.append(cci)
    
    return result


def WR(high: List[float], low: List[float], close: List[float], period: int = 14) -> List[float]:
    """
    威廉指标 (Williams %R)
    
    用法：
    - WR > -20: 超买
    - WR < -80: 超卖
    
    Args:
        high: 最高价列表
        low: 最低价列表
        close: 收盘价列表
        period: 周期，默认 14
    
    Returns:
        WR 值列表 (-100 到 0)
    """
    if len(close) < period:
        return []
    
    result = []
    
    for i in range(len(close) - period + 1):
        highest = max(high[i:i+period])
        lowest = min(low[i:i+period])
        
        if highest == lowest:
            result.append(-50)
        else:
            wr = (highest - close[i+period-1]) / (highest - lowest) * -100
            result.append(wr)
    
    return result


def ROC(close: List[float], period: int = 12) -> List[float]:
    """
    变动率指标 (Rate of Change)
    
    衡量价格变动速度
    
    Args:
        close: 收盘价列表
        period: 周期，默认 12
    
    Returns:
        ROC 值列表 (%)
    """
    if len(close) <= period:
        return []
    
    result = []
    
    for i in range(period, len(close)):
        roc = (close[i] - close[i-period]) / close[i-period] * 100
        result.append(roc)
    
    return result


def OBV(close: List[float], volume: List[int]) -> List[float]:
    """
    能量潮指标 (On Balance Volume)
    
    通过成交量推测资金流向
    
    Args:
        close: 收盘价列表
        volume: 成交量列表
    
    Returns:
        OBV 值列表
    """
    if len(close) != len(volume) or len(close) < 2:
        return []
    
    obv = [volume[0]]
    
    for i in range(1, len(close)):
        if close[i] > close[i-1]:
            obv.append(obv[-1] + volume[i])
        elif close[i] < close[i-1]:
            obv.append(obv[-1] - volume[i])
        else:
            obv.append(obv[-1])
    
    return obv


# ============== 综合分析 ==============

def analyze_technical(high: List[float], low: List[float], close: List[float], 
                      volume: List[int] = None) -> Dict:
    """
    综合技术分析
    
    Args:
        high: 最高价列表
        low: 最低价列表
        close: 收盘价列表
        volume: 成交量列表 (可选)
    
    Returns:
        包含各项指标最新值的字典
    """
    result = {}
    
    # 趋势指标
    ma5 = MA(close, 5)[-1] if len(close) >= 5 else None
    ma10 = MA(close, 10)[-1] if len(close) >= 10 else None
    ma20 = MA(close, 20)[-1] if len(close) >= 20 else None
    ma60 = MA(close, 60)[-1] if len(close) >= 60 else None
    
    result['trend'] = {
        'ma5': ma5,
        'ma10': ma10,
        'ma20': ma20,
        'ma60': ma60,
        'price_vs_ma5': 'above' if close[-1] > ma5 else 'below' if ma5 else None,
        'price_vs_ma20': 'above' if close[-1] > ma20 else 'below' if ma20 else None,
    }
    
    # 动量指标
    rsi6 = RSI(close, 6)[-1] if len(close) >= 7 else None
    rsi12 = RSI(close, 12)[-1] if len(close) >= 13 else None
    rsi14 = RSI(close, 14)[-1] if len(close) >= 15 else None
    
    result['momentum'] = {
        'rsi6': rsi6,
        'rsi12': rsi12,
        'rsi14': rsi14,
        'rsi_signal': 'overbought' if rsi14 and rsi14 > 70 else 'oversold' if rsi14 and rsi14 < 30 else 'neutral'
    }
    
    # MACD
    macd = MACD(close)
    if macd['dif'] and macd['dea']:
        result['macd'] = {
            'dif': macd['dif'][-1],
            'dea': macd['dea'][-1],
            'hist': macd['macd_hist'][-1] if macd['macd_hist'] else None,
            'signal': 'bullish' if macd['dif'][-1] > macd['dea'][-1] else 'bearish'
        }
    
    # 布林带
    boll = BOLL(close, 20)
    if boll['upper']:
        result['bollinger'] = {
            'upper': boll['upper'][-1],
            'middle': boll['middle'][-1],
            'lower': boll['lower'][-1],
            'position': 'upper' if close[-1] > boll['upper'][-1] else 'lower' if close[-1] < boll['lower'][-1] else 'middle'
        }
    
    # KDJ
    kdj = KDJ(high, low, close)
    if kdj['k']:
        result['kdj'] = {
            'k': kdj['k'][-1],
            'd': kdj['d'][-1],
            'j': kdj['j'][-1],
            'signal': 'overbought' if kdj['k'][-1] > 80 else 'oversold' if kdj['k'][-1] < 20 else 'neutral'
        }
    
    # 成交量分析
    if volume:
        result['volume'] = {
            'current': volume[-1],
            'ma5_vol': sum(volume[-5:]) / 5 if len(volume) >= 5 else volume[-1],
            'signal': 'high' if volume[-1] > sum(volume[-5:]) / 5 * 1.5 else 'low' if volume[-1] < sum(volume[-5:]) / 5 * 0.5 else 'normal'
        }
    
    return result


def format_analysis_report(stock_code: str, stock_name: str, current_price: float, 
                           analysis: Dict) -> str:
    """
    格式化分析报告
    
    Args:
        stock_code: 股票代码
        stock_name: 股票名称
        current_price: 当前价格
        analysis: 技术分析结果
    
    Returns:
        格式化的报告字符串
    """
    report = f"""
📊 {stock_name} ({stock_code}) 技术分析报告
━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 当前价格：¥{current_price:.2f}

📈 趋势指标:
"""
    
    # 趋势
    trend = analysis.get('trend', {})
    if trend.get('ma5'):
        report += f"  MA5:  ¥{trend['ma5']:.2f} | 价格{'站上' if trend.get('price_vs_ma5') == 'above' else '跌破'}5 日线\n"
    if trend.get('ma20'):
        report += f"  MA20: ¥{trend['ma20']:.2f} | 价格{'站上' if trend.get('price_vs_ma20') == 'above' else '跌破'}20 日线\n"
    
    # 动量
    momentum = analysis.get('momentum', {})
    if momentum.get('rsi14'):
        rsi_status = {
            'overbought': '⚠️ 超买区',
            'oversold': '💪 超卖区',
            'neutral': '➖ 中性区'
        }
        report += f"\n📊 动量指标:\n"
        report += f"  RSI(14): {momentum['rsi14']:.2f} | {rsi_status.get(momentum.get('rsi_signal', 'neutral'), '')}\n"
    
    # MACD
    macd = analysis.get('macd', {})
    if macd:
        report += f"\n📉 MACD:\n"
        report += f"  DIF: {macd['dif']:.4f} | DEA: {macd['dea']:.4f}\n"
        report += f"  信号：{'🐂 多头' if macd.get('signal') == 'bullish' else '🐻 空头'}\n"
    
    # 布林带
    boll = analysis.get('bollinger', {})
    if boll:
        report += f"\n📊 布林带:\n"
        report += f"  上轨：¥{boll['upper']:.2f} | 中轨：¥{boll['middle']:.2f} | 下轨：¥{boll['lower']:.2f}\n"
        pos_text = {
            'upper': '⚠️ 触及上轨',
            'lower': '💪 触及下轨',
            'middle': '➖ 中轨附近'
        }
        report += f"  位置：{pos_text.get(boll.get('position', 'middle'), '')}\n"
    
    # KDJ
    kdj = analysis.get('kdj', {})
    if kdj:
        report += f"\n📊 KDJ:\n"
        report += f"  K: {kdj['k']:.2f} | D: {kdj['d']:.2f} | J: {kdj['j']:.2f}\n"
        report += f"  信号：{'⚠️ 超买' if kdj.get('signal') == 'overbought' else '💪 超卖' if kdj.get('signal') == 'oversold' else '➖ 中性'}\n"
    
    # 成交量
    vol = analysis.get('volume', {})
    if vol:
        report += f"\n📦 成交量:\n"
        report += f"  当前：{vol['current']:,}手 | 5 日均：{vol['ma5_vol']:,.0f}手\n"
        vol_status = {
            'high': '🔥 放量',
            'low': '❄️ 缩量',
            'normal': '➖ 正常'
        }
        report += f"  状态：{vol_status.get(vol.get('signal', 'normal'), '')}\n"
    
    report += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    report += "⚠️ 风险提示：技术分析仅供参考，不构成投资建议\n"
    
    return report


# ============== 测试 ==============
if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    # 测试数据（模拟 60 天数据）
    np.random.seed(42)
    base_price = 100
    
    # 生成随机走势
    changes = np.random.randn(100) * 2
    close = [base_price]
    for c in changes:
        close.append(close[-1] + c)
    
    # 生成高低点
    high = [c + abs(np.random.randn() * 1.5) for c in close]
    low = [c - abs(np.random.randn() * 1.5) for c in close]
    volume = [int(np.random.randint(10000, 100000) * 100) for _ in close]
    
    print("=" * 60)
    print("技术分析模块测试")
    print("=" * 60)
    
    # 测试各项指标
    print(f"\n收盘价序列：{len(close)}天")
    print(f"最新价：{close[-1]:.2f}")
    
    print(f"\nMA5: {MA(close, 5)[-1]:.2f}")
    print(f"MA20: {MA(close, 20)[-1]:.2f}")
    
    rsi = RSI(close, 14)
    print(f"RSI(14): {rsi[-1]:.2f}")
    
    macd = MACD(close)
    print(f"MACD DIF: {macd['dif'][-1]:.4f}")
    print(f"MACD DEA: {macd['dea'][-1]:.4f}")
    
    kdj = KDJ(high, low, close)
    print(f"KDJ K: {kdj['k'][-1]:.2f}")
    print(f"KDJ D: {kdj['d'][-1]:.2f}")
    print(f"KDJ J: {kdj['j'][-1]:.2f}")
    
    boll = BOLL(close, 20)
    print(f"BOLL 上轨：{boll['upper'][-1]:.2f}")
    print(f"BOLL 中轨：{boll['middle'][-1]:.2f}")
    print(f"BOLL 下轨：{boll['lower'][-1]:.2f}")
    
    # 综合分析
    print("\n" + "=" * 60)
    print("综合分析报告")
    print("=" * 60)
    
    analysis = analyze_technical(high, low, close, volume)
    report = format_analysis_report("000001", "测试股票", close[-1], analysis)
    print(report)
