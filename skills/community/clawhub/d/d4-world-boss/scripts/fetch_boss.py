#!/usr/bin/env python3
"""暗黑4世界BOSS刷新时间查询"""

import json, re, sys, subprocess

URL = "https://map.caimogu.cc/d4.html"

def fetch_data():
    try:
        r = subprocess.run(["curl", "-s", "-L", URL], capture_output=True, text=True, timeout=30)
        return r.stdout
    except:
        return None

def parse_boss_info(html):
    m = re.search(r'window\.d4WorldBoss=({[^}]+})', html)
    if not m:
        return None
    
    data = json.loads(m.group(1))
    status = data.get("status", "")
    name = data.get("name", "")
    countdown_sec = data.get("time", 0)
    next_time = data.get("tsn", 0)
    
    # 格式化倒计时
    hours = countdown_sec // 3600
    minutes = (countdown_sec % 3600) // 60
    seconds = countdown_sec % 60
    
    if hours > 0:
        countdown_str = f"{hours}小时{minutes}分{seconds}秒"
    elif minutes > 0:
        countdown_str = f"{minutes}分{seconds}秒"
    else:
        countdown_str = f"{seconds}秒"
    
    # 状态描述
    status_map = {
        "colddown": "🔄 刷新倒计时",
        "active": "⚔️ BOSS已出现，战斗中",
        "waiting": "⏳ 等待出现",
        "process": "⚔️ BOSS已出现，战斗中"  # process 表示boss已出现
    }
    status_desc = status_map.get(status, status)
    can_set_reminder = status in ["colddown", "waiting"]  # 只有冷却中/等待中才能设置提醒
    
    return {
        "name": name,
        "status": status_desc,
        "countdown": countdown_str,
        "countdown_sec": countdown_sec,
        "can_set_reminder": can_set_reminder
    }

def output(info, url):
    if not info:
        return "❌ 获取BOSS信息失败，请稍后再试"
    
    lines = []
    lines.append(f"🔥 暗黑4 世界BOSS")
    lines.append(f"")
    lines.append(f"【当前BOSS】{info['name']}")
    lines.append(f"【状态】{info['status']}")
    lines.append(f"【倒计时】{info['countdown']}")
    lines.append(f"")
    lines.append(f"📊 数据来源: {url}")
    
    # 添加提醒提示
    if info.get("can_set_reminder"):
        lines.append(f"")
        lines.append(f"💡 需要设置刷新提醒吗？")
    else:
        lines.append(f"")
        lines.append(f"⚠️ BOSS已出现，无需设置提醒")
    
    return "\n".join(lines)

def main():
    html = fetch_data()
    if not html:
        print("❌ 获取数据失败")
        sys.exit(1)
    
    info = parse_boss_info(html)
    print(output(info, URL))

main()
