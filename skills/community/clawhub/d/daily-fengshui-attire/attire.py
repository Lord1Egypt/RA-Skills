#!/usr/bin/env python3
"""
每日穿衣指南 - 基于地支五行生克
"""

import sys
from datetime import datetime, timedelta

# 地支顺序
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 地支五行映射
DIZHI_WUXING = {
    "子": "水",
    "丑": "土",
    "寅": "木",
    "卯": "木",
    "辰": "土",
    "巳": "火",
    "午": "火",
    "未": "土",
    "申": "金",
    "酉": "金",
    "戌": "土",
    "亥": "水",
}

# 五行颜色映射
WUXING_COLORS = {
    "木": {"colors": ["绿色", "青色"], "emoji": "🟢", "direction": "东"},
    "火": {"colors": ["红色", "紫色"], "emoji": "🔴", "direction": "南"},
    "土": {"colors": ["黄色", "棕色"], "emoji": "🟡", "direction": "中"},
    "金": {"colors": ["白色", "金色"], "emoji": "⚪", "direction": "西"},
    "水": {"colors": ["黑色", "蓝色"], "emoji": "🔵", "direction": "北"},
}

# 五行相生顺序
SHENG = ["木", "火", "土", "金", "水"]

# 五行相克顺序
KE = ["木", "土", "水", "火", "金"]


def get_dizhi(date: datetime) -> str:
    """根据日期计算地支"""
    # 基准日期：2024-01-01 是甲子日
    base = datetime(2024, 1, 1)
    days_diff = (date - base).days
    # 甲子是第0个地支
    index = days_diff % 12
    return DIZHI[index]


def get_wuxing(dizhi: str) -> str:
    """获取地支对应的五行"""
    return DIZHI_WUXING[dizhi]


def get_sheng(wuxing: str) -> str:
    """获取相生的五行"""
    idx = SHENG.index(wuxing)
    return SHENG[(idx + 1) % 5]


def get_ke(wuxing: str) -> str:
    """获取相克的五行"""
    idx = KE.index(wuxing)
    return KE[(idx + 1) % 5]


def analyze_relationship(today_wuxing: str, tomorrow_wuxing: str) -> dict:
    """分析今日与明日的五行关系"""
    result = {"type": "unknown", "advice": ""}
    
    if get_sheng(today_wuxing) == tomorrow_wuxing:
        result["type"] = "相生"
        result["advice"] = f"今日五行{today_wuxing}生明日五行{tomorrow_wuxing}，明日气场处于上升期"
    elif get_ke(today_wuxing) == tomorrow_wuxing:
        result["type"] = "相克"
        result["advice"] = f"今日五行{today_wuxing}克明日五行{tomorrow_wuxing}，明日需要化解"
    elif today_wuxing == tomorrow_wuxing:
        result["type"] = "同气"
        result["advice"] = f"今日与明日同为{today_wuxing}气，能量持续稳定"
    else:
        result["type"] = "泄气"
        result["advice"] = f"今日{today_wuxing}泄明日{tomorrow_wuxing}，明日气场较弱"
    
    return result


def generate_advice(today_dizhi: str, tomorrow_dizhi: str) -> str:
    """生成穿衣建议 - 核心原则：穿当日所生的颜色"""
    today_wuxing = get_wuxing(today_dizhi)
    tomorrow_wuxing = get_wuxing(tomorrow_dizhi)
    
    # 核心逻辑：当日五行生什么，就穿什么颜色
    sheng_wuxing = get_sheng(today_wuxing)  # 今日所生的五行
    color_info = WUXING_COLORS[sheng_wuxing]
    
    suggestions = []
    
    # 最佳推荐：穿当日所生的颜色
    suggestions.append(
        f"🧧 最佳推荐：{color_info['colors'][0]}/{color_info['colors'][1]}（{sheng_wuxing}）\n"
        f"   今日{today_dizhi}（{today_wuxing}）生{sheng_wuxing}，穿此颜色助长今日气场"
    )
    
    # 次选：穿当日同属性颜色
    today_color = WUXING_COLORS[today_wuxing]
    suggestions.append(
        f"📘 次选：{today_color['colors'][0]}/{today_color['colors'][1]}（{today_wuxing}）\n"
        f"   保持与今日五行同气，能量稳定"
    )
    
    return "\n\n".join(suggestions)


def cmd_today():
    """输出今日地支"""
    today = datetime.now()
    dizhi = get_dizhi(today)
    wuxing = get_wuxing(dizhi)
    print(f"{today.strftime('%Y-%m-%d')}|{dizhi}|{wuxing}")


def cmd_tomorrow():
    """输出明日地支"""
    tomorrow = datetime.now() + timedelta(days=1)
    dizhi = get_dizhi(tomorrow)
    wuxing = get_wuxing(dizhi)
    print(f"{tomorrow.strftime('%Y-%m-%d')}|{dizhi}|{wuxing}")


def cmd_advice():
    """输出完整穿衣建议"""
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    
    today_dizhi = get_dizhi(today)
    tomorrow_dizhi = get_dizhi(tomorrow)
    
    today_wuxing = get_wuxing(today_dizhi)
    tomorrow_wuxing = get_wuxing(tomorrow_dizhi)
    
    relation = analyze_relationship(today_wuxing, tomorrow_wuxing)
    suggestions = generate_advice(today_dizhi, tomorrow_dizhi)
    
    print("=" * 50)
    print(f"📅 今日（{today.strftime('%m月%d日')}）：{today_dizhi}日 | {today_wuxing}气")
    print(f"🎯 明日（{tomorrow.strftime('%m月%d日')}）：{tomorrow_dizhi}日 | {tomorrow_wuxing}气")
    print("=" * 50)
    print()
    print("【五行分析】")
    print(relation["advice"])
    print()
    print("【穿衣建议】")
    print(suggestions)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        cmd_advice()
    elif sys.argv[1] == "today":
        cmd_today()
    elif sys.argv[1] == "tomorrow":
        cmd_tomorrow()
    elif sys.argv[1] == "advice":
        cmd_advice()
    else:
        print(f"用法: {sys.argv[0]} [today|tomorrow|advice]")
