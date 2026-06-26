#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📅 Calendar Manager - 日历管理助手（优化版）
功能：日程管理、提醒、节日、倒计时、时间统计
"""

import json
import re
from pathlib import Path
from datetime import datetime, timedelta

DATA_DIR = Path(__file__).parent
EVENTS_FILE = DATA_DIR / "events.json"
HOLIDAYS_FILE = DATA_DIR / "holidays.json"

# ========== 中国节日 ==========

CHINESE_HOLIDAYS = {
    "2026": {
        "01-01": "元旦",
        "01-22": "除夕",
        "01-23": "春节",
        "02-08": "元宵节",
        "04-04": "清明节",
        "05-01": "劳动节",
        "06-20": "端午节",
        "09-03": "中秋节",
        "10-01": "国庆节",
        "10-02": "国庆节",
        "10-03": "国庆节",
    }
}

# ========== 重要纪念日 ==========

MEMORABLE_DAYS = {
    "01-01": "元旦",
    "02-14": "情人节",
    "03-08": "妇女节",
    "03-12": "植树节",
    "04-04": "清明节",
    "05-01": "劳动节",
    "05-04": "青年节",
    "06-01": "儿童节",
    "07-01": "建党节",
    "08-01": "建军节",
    "09-10": "教师节",
    "10-01": "国庆节",
    "12-25": "圣诞节",
}


def load_json(filepath):
    """加载 JSON 文件"""
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"events": [], "memorable_days": []}


def save_json(filepath, data):
    """保存 JSON 文件"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def parse_time(time_str):
    """解析时间字符串"""
    now = datetime.now()
    
    # 今天下午 3 点
    if "今天" in time_str:
        match = re.search(r'(\d+) 点', time_str)
        if match:
            hour = int(match.group(1))
            return now.replace(hour=hour, minute=0, second=0)
    
    # 明天上午 10 点
    if "明天" in time_str:
        match = re.search(r'(\d+) 点', time_str)
        if match:
            hour = int(match.group(1))
            tomorrow = now + timedelta(days=1)
            return tomorrow.replace(hour=hour, minute=0, second=0)
    
    # 具体日期：2026-03-20 14:00
    match = re.search(r'(\d{4})-(\d{2})-(\d{2})\s*(\d{1,2}):?(\d{2})?', time_str)
    if match:
        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))
        hour = int(match.group(4)) if match.group(5) else 0
        minute = int(match.group(5)) if match.group(5) else 0
        return datetime(year, month, day, hour, minute)
    
    # 仅日期：2026-03-20
    match = re.search(r'(\d{4})-(\d{2})-(\d{2})', time_str)
    if match:
        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))
        return datetime(year, month, day, 9, 0)  # 默认上午 9 点
    
    return now


def add_event(title, start, end=None, reminder=True, location="", notes=""):
    """添加日程"""
    data = load_json(EVENTS_FILE)
    
    if isinstance(start, str):
        start = parse_time(start)
    
    if end is None:
        end = start + timedelta(hours=1)
    elif isinstance(end, str):
        end = parse_time(end)
    
    event = {
        "id": f"evt_{datetime.now().timestamp()}",
        "title": title,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "reminder": reminder,
        "location": location,
        "notes": notes,
        "created": datetime.now().isoformat(),
        "completed": False
    }
    
    data["events"].append(event)
    save_json(EVENTS_FILE, data)
    
    return event


def get_today_events():
    """获取今日日程"""
    data = load_json(EVENTS_FILE)
    today = datetime.now().strftime("%Y-%m-%d")
    
    events = [e for e in data["events"] if e["start"].startswith(today)]
    events.sort(key=lambda x: x["start"])
    
    return events


def get_upcoming_events(days=7):
    """获取未来 N 天日程"""
    data = load_json(EVENTS_FILE)
    now = datetime.now()
    future = now + timedelta(days=days)
    
    events = []
    for e in data["events"]:
        event_time = datetime.fromisoformat(e["start"])
        if now <= event_time <= future:
            events.append(e)
    
    events.sort(key=lambda x: x["start"])
    
    return events


def get_holiday(date=None):
    """获取节日信息"""
    if date is None:
        date = datetime.now()
    
    month_day = date.strftime("%m-%d")
    year = date.strftime("%Y")
    
    # 中国节日
    if year in CHINESE_HOLIDAYS:
        if month_day in CHINESE_HOLIDAYS[year]:
            return CHINESE_HOLIDAYS[year][month_day]
    
    # 常规节日
    if month_day in MEMORABLE_DAYS:
        return MEMORABLE_DAYS[month_day]
    
    return None


def get_next_holiday():
    """获取下一个节日"""
    now = datetime.now()
    
    for i in range(365):
        date = now + timedelta(days=i)
        holiday = get_holiday(date)
        if holiday:
            return {
                "name": holiday,
                "date": date.strftime("%Y-%m-%d"),
                "days_left": i
            }
    
    return None


def add_memorable_day(name, date_str):
    """添加纪念日"""
    data = load_json(EVENTS_FILE)
    
    if "memorable_days" not in data:
        data["memorable_days"] = []
    
    # 解析日期
    if "-" in date_str:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        date = datetime.now()
    
    data["memorable_days"].append({
        "name": name,
        "date": date.strftime("%Y-%m-%d"),
        "created": datetime.now().isoformat()
    })
    
    save_json(EVENTS_FILE, data)
    
    return data["memorable_days"][-1]


def get_countdown(target_date, name=""):
    """获取倒计时"""
    if isinstance(target_date, str):
        target_date = datetime.strptime(target_date, "%Y-%m-%d")
    
    now = datetime.now()
    delta = target_date - now
    
    if delta.days < 0:
        return f"❌ {name} 已经过去 {-delta.days} 天了"
    
    return f"⏳ 距离{name}{target_date.strftime('%Y-%m-%d')}还有 {delta.days} 天"


def get_time_stats():
    """获取时间统计"""
    data = load_json(EVENTS_FILE)
    events = data.get("events", [])
    
    # 按类型统计
    stats = {
        "total": len(events),
        "this_week": 0,
        "this_month": 0,
        "completed": 0,
        "pending": 0
    }
    
    now = datetime.now()
    week_start = now - timedelta(days=now.weekday())
    month_start = now.replace(day=1)
    
    for event in events:
        event_time = datetime.fromisoformat(event["start"])
        
        if event_time >= week_start:
            stats["this_week"] += 1
        if event_time >= month_start:
            stats["this_month"] += 1
        if event.get("completed"):
            stats["completed"] += 1
        else:
            stats["pending"] += 1
    
    return stats


def complete_event(event_id):
    """标记日程完成"""
    data = load_json(EVENTS_FILE)
    
    for event in data["events"]:
        if event["id"] == event_id:
            event["completed"] = True
            save_json(EVENTS_FILE, data)
            return True
    
    return False


def delete_event(event_id):
    """删除日程"""
    data = load_json(EVENTS_FILE)
    
    before = len(data["events"])
    data["events"] = [e for e in data["events"] if e["id"] != event_id]
    save_json(EVENTS_FILE, data)
    
    return len(data["events"]) < before


def format_event(event):
    """格式化单个日程"""
    start = datetime.fromisoformat(event["start"])
    end = datetime.fromisoformat(event["end"])
    
    status = "✅" if event.get("completed") else "⏳"
    
    info = f"{status} {event['title']}\n"
    info += f"   🕐 {start.strftime('%m-%d %H:%M')} - {end.strftime('%H:%M')}\n"
    
    if event.get("location"):
        info += f"   📍 {event['location']}\n"
    
    return info


def format_events(events, title="日程"):
    """格式化日程列表"""
    if not events:
        return f"📅 {title}：暂无安排"
    
    response = f"📅 **{title}** ({len(events)} 个)：\n\n"
    for event in events:
        response += format_event(event) + "\n"
    
    return response


def main(query):
    """主函数"""
    query_lower = query.lower()
    
    # ========== 添加日程 ==========
    
    if "添加" in query_lower or "安排" in query_lower or "约" in query_lower:
        # 提取时间
        time_match = re.search(r'(今天 | 明天|\d{4}-\d{2}-\d{2})\s*(\d+ 点|\d+:\d+)?', query)
        
        if time_match:
            time_str = time_match.group(0)
            start = parse_time(time_str)
            
            # 提取标题
            title = query.replace(time_str, "").replace("添加", "").replace("安排", "").replace("约", "").strip()
            if not title:
                title = "未命名日程"
            
            # 提取地点
            location = ""
            if "在" in title:
                match = re.search(r'在 (.+)', title)
                if match:
                    location = match.group(1)
                    title = title.replace(f"在 {location}", "").strip()
            
            event = add_event(title, start, location=location)
            return f"""✅ 日程已添加

📝 {event['title']}
🕐 {start.strftime('%m-%d %H:%M')}
📍 {location or '无地点'}

💡 说「完成 {event['id']}」标记完成"""
        
        return "❌ 请指定时间，例如：「明天下午 3 点开会」"
    
    # ========== 查看日程 ==========
    
    # 今日日程
    if "今天" in query_lower or "今日" in query_lower or "今天有什么安排" in query_lower:
        events = get_today_events()
        holiday = get_holiday()
        
        response = ""
        if holiday:
            response += f"🎉 今天是{holiday}！\n\n"
        
        response += format_events(events, "今日日程")
        return response
    
    # 明天日程
    if "明天" in query_lower:
        tomorrow = datetime.now() + timedelta(days=1)
        data = load_json(EVENTS_FILE)
        tomorrow_str = tomorrow.strftime("%Y-%m-%d")
        
        events = [e for e in data["events"] if e["start"].startswith(tomorrow_str)]
        return format_events(events, "明日日程")
    
    # 未来日程
    if "未来" in query_lower or "接下来" in query_lower:
        days = 7
        match = re.search(r'(\d+) 天', query)
        if match:
            days = int(match.group(1))
        
        events = get_upcoming_events(days)
        return format_events(events, f"未来{days}天日程")
    
    # 日程列表
    if "列表" in query_lower or "所有" in query_lower:
        data = load_json(EVENTS_FILE)
        return format_events(data["events"][-10:], "最近日程")
    
    # ========== 节日/纪念日 ==========
    
    # 今天是什么节日
    if "节日" in query_lower and ("今天" in query_lower or "什么" in query_lower):
        holiday = get_holiday()
        if holiday:
            return f"🎉 今天是{holiday}！"
        return "📅 今天没有特殊节日"
    
    # 下一个节日
    if "下一个节日" in query_lower or "最近节日" in query_lower:
        next_holiday = get_next_holiday()
        if next_holiday:
            return f"""🎉 下一个节日：{next_holiday['name']}
📅 日期：{next_holiday['date']}
⏳ 还有：{next_holiday['days_left']} 天"""
        return "📅 未找到节日信息"
    
    # 添加纪念日
    if "纪念日" in query_lower and "添加" in query_lower:
        match = re.search(r'(.+) 是 (.+)', query)
        if match:
            name = match.group(1).strip()
            date_str = match.group(2).strip()
            result = add_memorable_day(name, date_str)
            return f"✅ 纪念日已添加：{name}（{result['date']}）"
    
    # ========== 倒计时 ==========
    
    if "倒计时" in query_lower or "还有多久" in query_lower:
        # 简单实现
        next_holiday = get_next_holiday()
        if next_holiday:
            return get_countdown(next_holiday['date'], next_holiday['name'])
    
    # ========== 完成/删除日程 ==========
    
    if "完成" in query_lower or "做完" in query_lower:
        match = re.search(r'evt_\d+', query)
        if match:
            event_id = match.group(0)
            if complete_event(event_id):
                return f"✅ 日程已标记完成：{event_id}"
        return "❌ 未找到日程 ID"
    
    if "删除" in query_lower or "取消" in query_lower:
        match = re.search(r'evt_\d+', query)
        if match:
            event_id = match.group(0)
            if delete_event(event_id):
                return f"✅ 日程已删除：{event_id}"
        return "❌ 未找到日程 ID"
    
    # ========== 统计 ==========
    
    if "统计" in query_lower or "总结" in query_lower:
        stats = get_time_stats()
        return f"""📊 **时间统计**

总计：{stats['total']} 个日程
本周：{stats['this_week']} 个
本月：{stats['this_month']} 个
已完成：{stats['completed']} 个
待完成：{stats['pending']} 个"""
    
    # ========== 默认回复 ==========
    
    return """📅 日历管理助手（优化版）

**功能**：

📝 日程管理
1. 添加日程 - "明天下午 3 点开会"
2. 查看日程 - "今天有什么安排"
3. 日程列表 - "我的日程列表"
4. 完成日程 - "完成 evt_xxx"
5. 删除日程 - "删除 evt_xxx"

🎉 节日/纪念日
6. 今日节日 - "今天是什么节日"
7. 下一个节日 - "下一个节日"
8. 添加纪念日 - "生日是 1990-01-01"

⏳ 倒计时
9. 节日倒计时 - "距离春节还有多久"

📊 统计
10. 时间统计 - "本周日程统计"

告诉我你要添加什么日程？👻"""


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    print("=" * 60)
    print("📅 日历管理助手 - 测试")
    print("=" * 60)
    
    print("\n测试 1: 今日日程")
    print(main("今天有什么安排"))
    
    print("\n" + "=" * 60)
    print("测试 2: 添加日程")
    print(main("明天下午 3 点开会"))
    
    print("\n" + "=" * 60)
    print("测试 3: 节日查询")
    print(main("今天是什么节日"))
