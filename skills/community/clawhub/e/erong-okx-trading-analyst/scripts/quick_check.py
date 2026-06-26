#!/usr/bin/env python3
"""
快速行情检查 - 每分钟运行
检测信号变化和关键价格突破，有重大变化才通知
"""

import sys
import os
import json
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from okx_analyst import OKXAnalyzer, normalize_symbol, extract_base_symbol

# 配置
CHECK_INTERVAL = 60  # 每分钟检查
SYMBOLS = [
    "BTC-USDT-SWAP",
    "CL-USDT-SWAP",
]
TIMEFRAME = "4H"  # 使用4H周期信号
SIGNAL_CHANGE_THRESHOLD = 2  # 信号变化超过这个值才通知
STATE_FILE = os.path.expanduser("~/.openclaw/skills/okx-trading-analyst/data/last_state.json")


def load_last_state():
    """加载上次检查的状态"""
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}


def save_last_state(state):
    """保存当前状态"""
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2)


def quick_analyze(symbol, analyzer):
    """快速分析一个币种，返回关键数据"""
    df = analyzer.get_klines(symbol, bar=TIMEFRAME, limit=200)
    if df is None or len(df) < 60:
        return None
    
    df, indicators = analyzer.calculate_indicators(df)
    result = analyzer.generate_signals(df, indicators)
    
    latest = df.iloc[-1]
    support = indicators['Support_Level']
    resistance = indicators['Resistance_Level']
    
    return {
        'symbol': symbol,
        'price': result['latest_price'],
        'strength': result['strength'],
        'recommendation': result['recommendation'],
        'support': support,
        'resistance': resistance,
        'timestamp': datetime.now().isoformat()
    }


def check_for_changes(current, last):
    """检查是否需要通知"""
    notifications = []
    
    for symbol in SYMBOLS:
        curr = current.get(symbol)
        prev = last.get(symbol)
        
        if not curr:
            continue
        
        # 第一次检查，只记录不通知
        if not prev:
            continue
        
        # 检查信号强度变化
        curr_strength = curr['strength']
        prev_strength = prev['strength']
        change = abs(curr_strength - prev_strength)
        
        if change >= SIGNAL_CHANGE_THRESHOLD:
            direction = "上涨" if curr_strength > prev_strength else "下跌"
            notifications.append({
                'type': 'signal_change',
                'symbol': symbol,
                'old_strength': prev_strength,
                'new_strength': curr_strength,
                'change': change,
                'direction': direction,
                'current': curr
            })
        
        # 检查价格突破支撑/阻力
        price = curr['price']
        support = curr['support']
        resistance = curr['resistance']
        
        # 跌破支撑
        if prev['price'] > support and price <= support:
            notifications.append({
                'type': 'break_support',
                'symbol': symbol,
                'support': support,
                'current_price': price,
                'current': curr
            })
        
        # 突破阻力
        if prev['price'] < resistance and price >= resistance:
            notifications.append({
                'type': 'break_resistance',
                'symbol': symbol,
                'resistance': resistance,
                'current_price': price,
                'current': curr
            })
    
    return notifications


def format_notification(n):
    """格式化通知消息"""
    if n['type'] == 'signal_change':
        rec = n['current']['recommendation']
        emoji = rec['emoji']
        signal = rec['signal']
        return (
            f"⚠️ **{n['symbol']} 信号变化 {n['direction']}**\n"
            f"强度: {n['old_strength']:+d} → {n['new_strength']:+d} (变化 {n['change']:+d})\n"
            f"{emoji} {signal}  \n"
            f"当前价格: `${n['current']['price']:.2f}`\n"
            f"建议操作: {rec['action']}"
        )
    
    elif n['type'] == 'break_support':
        return (
            f"🔴 **{n['symbol']} 跌破支撑**\n"
            f"支撑位: `${n['support']:.2f}`\n"
            f"当前价格: `${n['current_price']:.2f}`\n"
            f"信号强度: {n['current']['strength']:+d}"
        )
    
    elif n['type'] == 'break_resistance':
        return (
            f"🟢 **{n['symbol']} 突破阻力**\n"
            f"阻力位: `${n['resistance']:.2f}`\n"
            f"当前价格: `${n['current_price']:.2f}`\n"
            f"信号强度: {n['current']['strength']:+d}"
        )
    
    return str(n)


def main():
    analyzer = OKXAnalyzer()
    last_state = load_last_state()
    
    # 分析所有币种
    current_state = {}
    for symbol in SYMBOLS:
        data = quick_analyze(symbol, analyzer)
        if data:
            current_state[symbol] = data
    
    # 检查变化
    notifications = check_for_changes(current_state, last_state)
    
    # 保存新状态
    save_last_state(current_state)
    
    # 输出通知（OpenClaw会捕获这个输出发送给你）
    if notifications:
        print(f"🔔 检测到{len(notifications)}个重要变化:\n")
        for n in notifications:
            print("---")
            print(format_notification(n))
        print("---")
    else:
        # 无变化，完全静默 - 不输出任何内容到 stdout 或 stderr
        # 这样 agent 不会生成无意义的总结
        sys.exit(0)
    
    # 有通知就退出码非0？不，正常退出，输出即通知
    sys.exit(0)


if __name__ == "__main__":
    main()
