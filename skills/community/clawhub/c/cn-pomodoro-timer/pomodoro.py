#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
番茄专注计时工具 - 中文番茄钟
功能：开始/暂停/继续/查看状态/统计
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 配置
POMODORO_MINUTES = 25  # 专注时长（分钟）
DATA_DIR = Path.home() / ".qclaw" / "data"
DATA_FILE = DATA_DIR / "pomodoro.json"

def ensure_data_dir():
    """确保数据目录存在"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_data():
    """加载数据"""
    if not DATA_FILE.exists():
        return {
            "current": None,  # 当前进行中的番茄钟
            "history": []     # 历史记录
        }
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"current": None, "history": []}

def save_data(data):
    """保存数据"""
    ensure_data_dir()
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def start_pomodoro():
    """开始新的番茄钟"""
    data = load_data()
    
    # 检查是否已有进行中的番茄钟
    if data.get("current") and data["current"].get("status") == "active":
        return "❌ 已有番茄钟在进行中！使用'查看专注状态'查看详情"
    
    # 创建新的番茄钟
    now = datetime.now()
    pomodoro = {
        "start_time": now.isoformat(),
        "status": "active",
        "paused_duration": 0,  # 累计暂停时长（秒）
        "pause_start": None    # 暂停开始时间
    }
    
    data["current"] = pomodoro
    save_data(data)
    
    end_time = now + timedelta(minutes=POMODORO_MINUTES)
    return f"🍅 番茄钟已开始！\n⏰ 预计结束时间：{end_time.strftime('%H:%M')}\n💪 专注25分钟，加油！"

def pause_pomodoro():
    """暂停番茄钟"""
    data = load_data()
    
    if not data.get("current"):
        return "❌ 当前没有进行中的番茄钟"
    
    current = data["current"]
    if current["status"] != "active":
        return "❌ 番茄钟未在运行中"
    
    # 记录暂停开始时间
    current["status"] = "paused"
    current["pause_start"] = datetime.now().isoformat()
    save_data(data)
    
    return "⏸️ 番茄钟已暂停\n使用'继续专注'恢复计时"

def resume_pomodoro():
    """继续番茄钟"""
    data = load_data()
    
    if not data.get("current"):
        return "❌ 当前没有进行中的番茄钟"
    
    current = data["current"]
    if current["status"] != "paused":
        return "❌ 番茄钟未在暂停状态"
    
    # 计算暂停时长
    pause_start = datetime.fromisoformat(current["pause_start"])
    pause_duration = (datetime.now() - pause_start).seconds
    current["paused_duration"] += pause_duration
    current["status"] = "active"
    current["pause_start"] = None
    
    save_data(data)
    
    return "▶️ 番茄钟已继续\n专注继续，保持状态！"

def get_status():
    """查看当前番茄钟状态"""
    data = load_data()
    
    if not data.get("current"):
        return "📭 当前没有进行中的番茄钟\n使用'开始专注'启动新的番茄钟"
    
    current = data["current"]
    start_time = datetime.fromisoformat(current["start_time"])
    
    if current["status"] == "paused":
        pause_start = datetime.fromisoformat(current["pause_start"])
        pause_duration = current["paused_duration"] + (datetime.now() - pause_start).seconds
        elapsed = (datetime.now() - start_time).seconds - pause_duration
        remaining = POMODORO_MINUTES * 60 - elapsed
        return f"⏸️ 番茄钟已暂停\n已专注：{elapsed // 60}分{elapsed % 60}秒\n剩余：{remaining // 60}分{remaining % 60}秒\n使用'继续专注'恢复"
    
    # 计算已用时间和剩余时间
    elapsed = (datetime.now() - start_time).seconds - current["paused_duration"]
    remaining = POMODORO_MINUTES * 60 - elapsed
    
    if remaining <= 0:
        # 番茄钟已完成
        return finish_pomodoro()
    
    minutes = remaining // 60
    seconds = remaining % 60
    
    end_time = start_time + timedelta(minutes=POMODORO_MINUTES, seconds=current["paused_duration"])
    
    return f"🍅 番茄钟进行中\n⏰ 剩余时间：{minutes}分{seconds}秒\n预计结束：{end_time.strftime('%H:%M')}\n专注中..."

def finish_pomodoro():
    """完成番茄钟"""
    data = load_data()
    
    if not data.get("current"):
        return "❌ 当前没有进行中的番茄钟"
    
    current = data["current"]
    start_time = datetime.fromisoformat(current["start_time"])
    
    # 记录到历史
    record = {
        "start_time": current["start_time"],
        "end_time": datetime.now().isoformat(),
        "completed": True,
        "paused_duration": current["paused_duration"]
    }
    
    data["history"].append(record)
    data["current"] = None
    save_data(data)
    
    # 计算实际专注时长
    actual_duration = POMODORO_MINUTES + current["paused_duration"] // 60
    
    return f"🎉 番茄钟完成！\n⏱️ 专注时长：{actual_duration}分钟\n🧘 记得休息5分钟\n💪 已完成今日 {len([h for h in data['history'] if h['start_time'][:10] == datetime.now().strftime('%Y-%m-%d')])} 个番茄钟"

def get_stats():
    """查看今日统计"""
    data = load_data()
    
    today = datetime.now().strftime('%Y-%m-%d')
    today_records = [h for h in data["history"] if h["start_time"][:10] == today]
    
    total_minutes = len(today_records) * POMODORO_MINUTES
    
    stats = f"📊 今日专注统计\n\n"
    stats += f"🍅 完成番茄钟：{len(today_records)} 个\n"
    stats += f"⏱️ 专注时长：{total_minutes} 分钟\n"
    
    if len(today_records) > 0:
        stats += f"\n记录：\n"
        for i, record in enumerate(today_records, 1):
            start = datetime.fromisoformat(record["start_time"]).strftime('%H:%M')
            end = datetime.fromisoformat(record["end_time"]).strftime('%H:%M')
            stats += f"{i}. {start} - {end}\n"
    
    return stats

def main():
    """主函数"""
    if len(sys.argv) < 2:
        # 默认行为：查看状态
        print(get_status())
        return
    
    command = sys.argv[1].lower()
    
    # 命令映射
    commands = {
        "start": start_pomodoro,
        "开始": start_pomodoro,
        "开始专注": start_pomodoro,
        "pause": pause_pomodoro,
        "暂停": pause_pomodoro,
        "暂停专注": pause_pomodoro,
        "resume": resume_pomodoro,
        "继续": resume_pomodoro,
        "继续专注": resume_pomodoro,
        "status": get_status,
        "状态": get_status,
        "查看状态": get_status,
        "专注状态": get_status,
        "stats": get_stats,
        "统计": get_stats,
        "今日专注": get_stats,
        "finish": finish_pomodoro,
        "完成": finish_pomodoro,
    }
    
    # 查找命令
    handler = None
    for key in commands:
        if key in command or command in key:
            handler = commands[key]
            break
    
    if handler:
        print(handler())
    else:
        print("❌ 未知命令")
        print("可用命令：开始专注、暂停专注、继续专注、查看状态、今日专注")

if __name__ == "__main__":
    main()
