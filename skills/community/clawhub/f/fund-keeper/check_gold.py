#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
黄金基金快速查询 - 000218
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

import requests

def get_gold_fund_data():
    """获取黄金基金实时数据"""
    fund_code = "000218"
    
    # 从天天基金网获取
    try:
        url = f"http://fundgz.1234567.com.cn/js/{fund_code}.js"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": f"http://fund.eastmoney.com/{fund_code}.html"
        }
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            content = response.text
            if content.startswith("jsonpgz(") and content.endswith(");"):
                data = json.loads(content[8:-2])
                return {
                    "code": data.get("fundcode"),
                    "name": data.get("name"),
                    "current_nav": float(data.get("gsz", 0)),
                    "last_nav": float(data.get("dwjz", 0)),
                    "estimate_growth": float(data.get("gszzl", 0)),
                    "update_time": data.get("gztime", "")
                }
    except Exception as e:
        return None
    return None

def analyze_gold_fund(data):
    """分析黄金基金，给出操作建议"""
    if not data:
        return None
    
    growth = data["estimate_growth"]
    current_nav = data["current_nav"]
    
    # 判断信号
    signal = "HOLD"
    action = "观望"
    reason = []
    
    if growth < -3:
        signal = "STRONG_BUY"
        action = "强烈建议补仓"
        reason.append(f"今日大跌 {growth}%，黄金坑机会")
    elif growth < -2:
        signal = "BUY"
        action = "建议补仓"
        reason.append(f"今日跌幅 {growth}%，达到补仓阈值")
    elif growth < 0:
        reason.append(f"今日下跌 {growth}%，未达补仓线")
    
    if growth > 3:
        signal = "STRONG_SELL"
        action = "强烈建议止盈"
        reason.append(f"今日大涨 +{growth}%，考虑止盈")
    elif growth > 2:
        signal = "SELL"
        action = "建议部分止盈"
        reason.append(f"今日涨幅 +{growth}%，达到止盈阈值")
    elif growth > 0:
        reason.append(f"今日上涨 +{growth}%，继续持有")
    
    return {
        "signal": signal,
        "action": action,
        "reasons": reason,
        "data": data
    }

def main():
    """主函数"""
    print("\n[Gold Fund 000218] Real-time Query\n")
    
    data = get_gold_fund_data()
    if not data:
        print("[ERROR] Failed to get data, please try again later")
        return
    
    analysis = analyze_gold_fund(data)
    if not analysis:
        print("[ERROR] Analysis failed")
        return
    
    # 显示结果
    print(f"Update: {analysis['data']['update_time']}")
    print(f"Current NAV: {analysis['data']['current_nav']:.4f}")
    print(f"Last NAV: {analysis['data']['last_nav']:.4f}")
    print(f"Change: {analysis['data']['estimate_growth']:+.2f}%")
    print()
    print(f"Action: {analysis['action']}")
    print(f"Signal: {analysis['signal']}")
    print()
    print("Reasons:")
    for r in analysis["reasons"]:
        print(f"  - {r}")
    print()

if __name__ == "__main__":
    main()
