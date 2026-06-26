#!/usr/bin/env python3
"""
BaoStock + MyTT 技术分析集成脚本
标准化输出：MA(5,10,20,30,60) + MACD + KDJ + RSI + BOLL
"""
import baostock as bs
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# 添加当前目录到路径以便导入 MyTT
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from MyTT import MA, EMA, MACD as MyMACD, KDJ as MyKDJ, RSI as MyRSI, BOLL as MyBOLL, REF, HHV, LLV

def get_stock_name(code):
    """获取股票名称"""
    lg = bs.login()
    rs = bs.query_stock_basic(code=code)
    name = code
    while rs.next():
        name = rs.get_row_data()[1]
    bs.logout()
    return name

def get_kline_data(code, days=120):
    """获取K线数据"""
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days+30)).strftime('%Y-%m-%d')
    
    lg = bs.login()
    
    rs = bs.query_history_k_data_plus(
        code,
        "date,open,high,low,close,volume",
        start_date=start_date,
        end_date=end_date,
        frequency="d",
        adjustflag="3"
    )
    
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    
    bs.logout()
    
    if not data_list:
        return None
    
    df = pd.DataFrame(data_list, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    
    # 转换为数值类型
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def calculate_ma(close):
    """计算均线"""
    ma5 = MA(close, 5)
    ma10 = MA(close, 10)
    ma20 = MA(close, 20)
    ma30 = MA(close, 30)
    ma60 = MA(close, 60)
    return {
        'MA5': ma5[-1] if not np.isnan(ma5[-1]) else None,
        'MA10': ma10[-1] if not np.isnan(ma10[-1]) else None,
        'MA20': ma20[-1] if not np.isnan(ma20[-1]) else None,
        'MA30': ma30[-1] if not np.isnan(ma30[-1]) else None,
        'MA60': ma60[-1] if not np.isnan(ma60[-1]) else None,
    }

def calculate_macd(close):
    """计算MACD"""
    dif, dea, macd = MyMACD(close)
    return {
        'DIF': dif[-1],
        'DEA': dea[-1],
        'MACD': macd[-1]
    }

def calculate_kdj(close, high, low):
    """计算KDJ"""
    k, d, j = MyKDJ(close, high, low)
    return {
        'K': k[-1],
        'D': d[-1],
        'J': j[-1]
    }

def calculate_rsi(close):
    """计算RSI"""
    rsi = MyRSI(close)
    return {
        'RSI6': rsi[-1] if not np.isnan(rsi[-1]) else None,
        'RSI12': rsi[-1] if not np.isnan(rsi[-1]) else None,  # MyTT RSI只有24周期
        'RSI24': rsi[-1] if not np.isnan(rsi[-1]) else None
    }

def calculate_boll(close):
    """计算BOLL"""
    upper, mid, lower = MyBOLL(close)
    return {
        'UPPER': upper[-1],
        'MID': mid[-1],
        'LOWER': lower[-1]
    }

def get_direction(current, previous):
    """判断均线方向"""
    if current is None or previous is None:
        return "→"
    if current > previous:
        return "↗"
    elif current < previous:
        return "↘"
    return "→"

def analyze(code):
    """技术分析主函数"""
    # 获取股票名称
    stock_name = get_stock_name(code)
    print(f"📈 {stock_name} ({code}) 技术分析报告")
    print(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 获取数据
    df = get_kline_data(code)
    if df is None or len(df) < 60:
        print("数据获取失败或数据不足")
        return
    
    close = df['close'].values
    high = df['high'].values
    low = df['low'].values
    
    # ===== 1. 均线系统 =====
    ma = calculate_ma(close)
    ma_prev = {
        'MA5': MA(close, 5)[-2],
        'MA10': MA(close, 10)[-2],
        'MA20': MA(close, 20)[-2],
        'MA30': MA(close, 30)[-2],
        'MA60': MA(close, 60)[-2],
    }
    
    print("\n【均线系统】")
    for key in ['MA5', 'MA10', 'MA20', 'MA30', 'MA60']:
        if ma[key]:
            direction = get_direction(ma[key], ma_prev.get(key))
            print(f"├── {key}: {ma[key]:.2f} 元 (方向: {direction})")
    
    # 均线信号判断
    latest_close = close[-1]
    ma_signals = []
    if ma['MA5'] and ma['MA10'] and ma['MA5'] > ma['MA10']:
        ma_signals.append("MA5>MA10 金叉")
    elif ma['MA5'] and ma['MA10'] and ma['MA5'] < ma['MA10']:
        ma_signals.append("MA5<MA10 死叉")
    if ma['MA20'] and ma['MA60'] and ma['MA20'] > ma['MA60']:
        ma_signals.append("MA20>MA60 多头")
    elif ma['MA20'] and ma['MA60'] and ma['MA20'] < ma['MA60']:
        ma_signals.append("MA20<MA60 空头")
    signal_text = ", ".join(ma_signals) if ma_signals else "震荡整理"
    print(f"└── 信号: {signal_text}")
    
    # ===== 2. MACD =====
    macd = calculate_macd(close)
    print("\n【MACD指标】")
    print(f"├── DIF: {macd['DIF']:.4f}")
    print(f"├── DEA: {macd['DEA']:.4f}")
    print(f"└── MACD: {macd['MACD']:.4f}")
    
    macd_signal = []
    if macd['MACD'] > 0:
        macd_signal.append("多头")
    else:
        macd_signal.append("空头")
    if macd['DIF'] > macd['DEA']:
        macd_signal.append("金叉")
    else:
        macd_signal.append("死叉")
    print(f"    信号: {' '.join(macd_signal)}")
    
    # ===== 3. KDJ =====
    kdj = calculate_kdj(close, high, low)
    print("\n【KDJ指标】")
    print(f"├── K: {kdj['K']:.2f}")
    print(f"├── D: {kdj['D']:.2f}")
    print(f"└── J: {kdj['J']:.2f}")
    
    kdj_signal = []
    if kdj['K'] > kdj['D']:
        kdj_signal.append("金叉")
    else:
        kdj_signal.append("死叉")
    if kdj['J'] > 80:
        kdj_signal.append("超买")
    elif kdj['J'] < 20:
        kdj_signal.append("超卖")
    print(f"    信号: {', '.join(kdj_signal)}")
    
    # ===== 4. RSI =====
    rsi = calculate_rsi(close)
    print("\n【RSI指标】")
    print(f"├── RSI(6): {rsi['RSI6']:.2f}")
    print(f"├── RSI(12): {rsi['RSI12']:.2f}")
    print(f"└── RSI(24): {rsi['RSI24']:.2f}")
    
    avg_rsi = (rsi['RSI6'] + rsi['RSI12'] + rsi['RSI24']) / 3
    if avg_rsi > 70:
        rsi_signal = "超买"
    elif avg_rsi < 30:
        rsi_signal = "超卖"
    elif avg_rsi > 50:
        rsi_signal = "偏强"
    else:
        rsi_signal = "偏弱"
    print(f"    信号: {rsi_signal}")
    
    # ===== 5. BOLL =====
    boll = calculate_boll(close)
    print("\n【BOLL布林带】")
    print(f"├── 上轨: {boll['UPPER']:.2f}")
    print(f"├── 中轨: {boll['MID']:.2f}")
    print(f"└── 下轨: {boll['LOWER']:.2f}")
    
    if latest_close > boll['UPPER']:
        boll_signal = "突破上轨"
    elif latest_close < boll['LOWER']:
        boll_signal = "跌破下轨"
    else:
        boll_signal = "在中轨附近"
    print(f"    信号: {boll_signal}")
    
    # ===== 6. 综合评分 =====
    print("\n【综合判断】")
    
    # 短期评分
    short_score = 0
    if ma['MA5'] and ma['MA10'] and ma['MA5'] > ma['MA10']:
        short_score += 1
    if macd['MACD'] > 0:
        short_score += 1
    if kdj['J'] < 20:
        short_score += 1
    elif kdj['J'] > 80:
        short_score -= 1
    if rsi['RSI6'] > 50:
        short_score += 1
    
    # 中期评分
    mid_score = 0
    if ma['MA20'] and ma['MA60'] and ma['MA20'] > ma['MA60']:
        mid_score += 2
    if macd['DIF'] > 0:
        mid_score += 1
    if avg_rsi > 50:
        mid_score += 1
    if latest_close > boll['MID']:
        mid_score += 1
    
    short_stars = "⭐" * max(1, min(5, short_score))
    mid_stars = "⭐" * max(1, min(5, mid_score))
    
    print(f"├── 短期: {short_stars} ({short_score}/5)")
    print(f"├── 中期: {mid_stars} ({mid_score}/5)")
    
    # 操作建议
    if short_score >= 4 and mid_score >= 4:
        advice = "积极看多"
    elif short_score >= 3 and mid_score >= 3:
        advice = "谨慎看多"
    elif short_score <= 1 and mid_score <= 2:
        advice = "观望为主，等待企稳"
    elif short_score >= 3 and mid_score <= 2:
        advice = "短期反弹，注意风险"
    else:
        advice = "中性震荡"
    
    print(f"└── 建议: {advice}")
    
    print("\n" + "=" * 60)
    print("数据来源: BaoStock + MyTT")

if __name__ == "__main__":
    # 默认分析中金黄金
    code = sys.argv[1] if len(sys.argv) > 1 else "sh.600489"
    analyze(code)
