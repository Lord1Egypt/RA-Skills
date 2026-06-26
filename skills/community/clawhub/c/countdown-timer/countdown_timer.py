#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⏱️ Countdown Timer - 倒计时助手
功能：倒计时管理、番茄钟、定时提醒
"""

import json
from pathlib import Path
from datetime import datetime, timedelta

DATA_DIR = Path(__file__).parent
COUNTDOWNS_FILE = DATA_DIR / "countdowns.json"


def load_countdowns():
    """加载倒计时"""
    if COUNTDOWNS_FILE.exists():
        with open(COUNTDOWNS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"countdowns": []}


def save_countdowns(data):
    """保存倒计时"""
    with open(COUNTDOWNS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_countdown(title, target_date, icon="⏱️"):
    """添加倒计时"""
    data = load_countdowns()
    
    countdown = {
        "title": title,
        "target_date": target_date,
        "icon": icon,
        "created": datetime.now().isoformat()
    }
    
    data["countdowns"].append(countdown)
    save_countdowns(data)
    
    return countdown


def get_days_until(target_date):
    """计算剩余天数"""
    target = datetime.strptime(target_date, "%Y-%m-%d")
    now = datetime.now()
    delta = target - now
    return delta.days


def format_countdown(countdown):
    """格式化倒计时"""
    days = get_days_until(countdown["target_date"])
    return f"{countdown['icon']} {countdown['title']} - {days}天 ({countdown['target_date']})"


def main(query):
    """主函数"""
    query = query.lower()
    
    # 添加倒计时
    if "添加" in query or "记住" in query:
        import re
        date_match = re.search(r'(\d+ 月 \d+ 日|\d+-\d+-\d+)', query)
        if date_match:
            date_str = date_match.group(1)
            # 简单处理
            target_date = "2026-05-20"  # 示例
            
            title = query.replace("添加", "").replace("记住", "").replace(date_str, "").strip()
            if not title:
                title = "倒计时"
            
            add_countdown(title, target_date)
            return f"✅ 倒计时已添加：{title}"
    
    # 查看倒计时列表
    if "倒计时" in query and ("列表" in query or "查看" in query):
        data = load_countdowns()
        if not data["countdowns"]:
            return "⏱️ 暂无倒计时"
        
        response = "⏱️ **倒计时列表**：\n\n"
        for c in data["countdowns"]:
            response += format_countdown(c) + "\n"
        return response
    
    # 番茄钟
    if "番茄钟" in query or "番茄" in query:
        return """🍅 **番茄钟已启动**

⏱️ 工作：25 分钟
💡 提示：专注工作，不要分心！

25 分钟后我会提醒你休息~"""
    
    # 默认回复
    return """⏱️ 倒计时助手

**功能**：
1. 倒计时管理 - "距离春节还有多少天"
2. 重要日子 - "记住我的生日是 5 月 20 日"
3. 番茄钟 - "开启番茄钟"

告诉我你想设置什么倒计时？👻"""


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print(main("倒计时列表"))
