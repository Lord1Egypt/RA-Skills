#!/usr/bin/env python3
"""DNFM 周本进度追踪 - 快速更新工具"""
import json
import sys
import os
from datetime import datetime

PROGRESS_FILE = "/root/.openclaw/workspace/dnfm-tracker/progress.json"
CONFIG_FILE = "/root/.openclaw/workspace/dnfm-tracker/config.json"

# 默认事件配置
DEFAULT_EVENTS = {
    "新超越本": {"key": "new_transcend", "total": 5, "refresh_day": 5, "enabled": True},
    "老超越本": {"key": "old_transcend", "total": 10, "refresh_day": 3, "enabled": True},
    "周本": {"key": "weekly", "total": 10, "refresh_day": 3, "enabled": True},
    "雷龙": {"key": "thunder_dragon", "total": 18, "refresh_day": 1, "enabled": True},
    "团本": {"key": "raid", "total": 16, "refresh_day": 1, "enabled": True},
}

def load_config():
    """加载用户配置"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"events": {}}

def save_config(config):
    """保存用户配置"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def get_events():
    """获取事件配置（合并默认配置和用户配置）"""
    config = load_config()
    user_events = config.get("events", {})
    
    events = {}
    for name, default_cfg in DEFAULT_EVENTS.items():
        if name in user_events:
            # 合并用户配置
            cfg = default_cfg.copy()
            cfg.update(user_events[name])
            events[name] = cfg
        else:
            events[name] = default_cfg.copy()
    
    return events

def load_progress():
    """加载进度"""
    try:
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"progress": {}}

def save_progress(data):
    """保存进度"""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def check_reset():
    """检查是否需要自动重置（刷新日早上6点后重置）"""
    now = datetime.now()
    today = now.date()
    weekday = now.weekday() + 1  # 周1-7
    
    data = load_progress()
    events = get_events()
    
    # 刷新时间：早上6点
    refresh_hour = 6
    
    for name, config in events.items():
        if not config.get("enabled", True):
            continue
            
        key = config["key"]
        refresh_day = config["refresh_day"]
        
        # 判断今天是否是刷新日，且当前时间超过6点
        if weekday == refresh_day and now.hour >= refresh_hour:
            # 重置进度
            data["progress"][key] = {"done": 0, "total": config["total"]}
            data["last_reset"] = data.get("last_reset", {})
            data["last_reset"][key] = now.strftime("%Y-%m-%d")
            save_progress(data)
    
    return data

def status():
    """显示当前进度"""
    check_reset()  # 每次调用都自动检查重置
    data = load_progress()
    events = get_events()
    progress = data.get("progress", {})
    
    lines = []
    for name, config in events.items():
        if not config.get("enabled", True):
            continue
            
        key = config["key"]
        prog = progress.get(key, {})
        done = prog.get("done", 0)
        total = config["total"]
        remaining = total - done
        
        if remaining <= 0:
            lines.append(f"✅ {name}: {done}/{total} ✓")
        else:
            lines.append(f"⏳ {name}: {done}/{total} (剩{remaining})")
    
    return "\n".join(lines) if lines else "没有启用的副本"

def update(event_name, done_count):
    """更新进度"""
    events = get_events()
    if event_name not in events:
        return f"未知事件: {event_name}"
    
    config = events[event_name]
    key = config["key"]
    total = config["total"]
    
    data = check_reset()
    data["progress"] = data.get("progress", {})
    data["progress"][key] = {
        "done": done_count,
        "total": total,
        "updated": datetime.now().isoformat()
    }
    
    save_progress(data)
    
    remaining = total - done_count
    if remaining <= 0:
        return f"✅ {event_name}: {done_count}/{total} ✓ 全部完成！"
    return f"✅ {event_name}: {done_count}/{total}，剩 {remaining} 个"

def set_total(event_name, new_total):
    """设置事件总量"""
    events = get_events()
    if event_name not in events:
        return f"未知事件: {event_name}"
    
    config = events[event_name]
    old_total = config["total"]
    config["total"] = int(new_total)
    
    # 保存到用户配置
    cfg = load_config()
    cfg["events"] = cfg.get("events", {})
    cfg["events"][event_name] = config
    save_config(cfg)
    
    # 同时更新数据文件
    data = load_progress()
    key = config["key"]
    if key in data.get("progress", {}):
        data["progress"][key]["total"] = int(new_total)
        save_progress(data)
    
    return f"✅ {event_name} 总量: {old_total} → {new_total}"

def enable_event(event_name):
    """启用事件"""
    events = get_events()
    if event_name not in events:
        return f"未知事件: {event_name}"
    
    cfg = load_config()
    cfg["events"] = cfg.get("events", {})
    cfg["events"][event_name] = cfg["events"].get(event_name, {})
    cfg["events"][event_name]["enabled"] = True
    save_config(cfg)
    
    return f"✅ 已启用 {event_name}"

def disable_event(event_name):
    """禁用事件"""
    events = get_events()
    if event_name not in events:
        return f"未知事件: {event_name}"
    
    cfg = load_config()
    cfg["events"] = cfg.get("events", {})
    cfg["events"][event_name] = cfg["events"].get(event_name, {})
    cfg["events"][event_name]["enabled"] = False
    save_config(cfg)
    
    return f"✅ 已禁用 {event_name}"

def show_config():
    """显示当前配置"""
    events = get_events()
    lines = ["⚙️ 当前配置："]
    for name, config in events.items():
        status = "✓" if config.get("enabled", True) else "✗"
        lines.append(f"  {status} {name}: {config['total']}个 (刷新日: 周{config['refresh_day']})")
    return "\n".join(lines)

def show_events():
    """显示所有可用事件"""
    lines = ["📋 可用事件列表："]
    for name, config in DEFAULT_EVENTS.items():
        lines.append(f"  - {name}")
    return "\n".join(lines)

if __name__ == "__main__":
    # 任何调用都先检查重置
    check_reset()
    
    if len(sys.argv) < 2:
        print(status())
    elif sys.argv[1] == "--status":
        print(status())
    elif sys.argv[1] == "--config":
        print(show_config())
    elif sys.argv[1] == "--events":
        print(show_events())
    elif sys.argv[1] == "--update" and len(sys.argv) >= 4:
        event = sys.argv[2]
        try:
            count = int(sys.argv[3])
            print(update(event, count))
        except:
            print(f"无效数字: {sys.argv[3]}")
    elif sys.argv[1] == "--set-total" and len(sys.argv) >= 4:
        event = sys.argv[2]
        try:
            total = int(sys.argv[3])
            print(set_total(event, total))
        except:
            print(f"无效数字: {sys.argv[3]}")
    elif sys.argv[1] == "--enable" and len(sys.argv) >= 3:
        print(enable_event(sys.argv[2]))
    elif sys.argv[1] == "--disable" and len(sys.argv) >= 3:
        print(disable_event(sys.argv[2]))
    else:
        print("用法:")
        print("  tracker.py              # 显示进度")
        print("  tracker.py --status     # 显示进度")
        print("  tracker.py --config     # 显示配置")
        print("  tracker.py --events     # 显示可用事件")
        print("  tracker.py --update <事件> <数量>  # 更新进度")
        print("  tracker.py --set-total <事件> <总量>  # 设置总量")
        print("  tracker.py --enable <事件>   # 启用事件")
        print("  tracker.py --disable <事件>  # 禁用事件")
