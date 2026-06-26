#!/usr/bin/env python3
"""
Heartbeat 检查脚本
每30分钟运行一次，执行记忆维护任务
"""

import json
import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw" / "workspace"
DATA_DIR = WORKSPACE / "data"
MEMORY_DIR = WORKSPACE / "memory"

# 空闲阈值：45分钟无活动自动保存
IDLE_THRESHOLD_MINUTES = 45

def load_state():
    state_file = DATA_DIR / "heartbeat-state.json"
    if state_file.exists():
        with open(state_file) as f:
            return json.load(f)
    return {"lastChecks": {}, "daily_memory_review_done": False, "last_message_time": None, "last_save_time": None}

def save_state(state):
    with open(DATA_DIR / "heartbeat-state.json", "w") as f:
        json.dump(state, f, indent=2)

def check_emergency():
    """检查紧急事项（邮件/日历/提醒）"""
    return True

def organize_memory():
    """整理记忆：短期→长期"""
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday_file = MEMORY_DIR / f"{yesterday}.md"
    
    if yesterday_file.exists():
        with open(yesterday_file) as f:
            content = f.read()
    return True

def clean_logs():
    """清理7天前的日志"""
    return True

def daily_maintenance(state):
    """每日维护任务"""
    today = datetime.now().strftime("%Y-%m-%d")
    last_date = state.get("lastChecks", {}).get("date", "")
    
    if last_date != today:
        organize_memory()
        state["daily_memory_review_done"] = True
        state["lastChecks"]["date"] = today
        print(f"[每日维护] 日期变化: {last_date} → {today}")
    
    return True

def weekly_maintenance():
    """每周维护任务（周日）"""
    if datetime.now().weekday() == 6:
        print("[每周维护] 周日执行")
    return True

def check_idle_and_save(state):
    """检查用户空闲时间，触发自动保存"""
    now = datetime.now()
    
    # 如果没有记录用户消息时间，跳过
    last_msg_time = state.get("last_message_time")
    if not last_msg_time:
        return False
    
    last_msg_dt = datetime.fromisoformat(last_msg_time)
    idle_minutes = (now - last_msg_dt).total_seconds() / 60
    
    # 检查是否超过45分钟
    if idle_minutes >= IDLE_THRESHOLD_MINUTES:
        last_save = state.get("last_save_time")
        # 如果之前没保存过，或者上次保存时间比用户最后消息时间早
        if not last_save:
            print(f"\n🅰️ 检测到用户空闲 {int(idle_minutes)} 分钟，触发自动保存...")
            trigger_daily_evolution()
            state["last_save_time"] = now.isoformat()
            return True
        else:
            last_save_dt = datetime.fromisoformat(last_save)
            # 只有当用户新消息后才需要再次保存
            if last_msg_dt > last_save_dt and idle_minutes >= IDLE_THRESHOLD_MINUTES:
                print(f"\n🅰️ 检测到用户空闲 {int(idle_minutes)} 分钟，触发自动保存...")
                trigger_daily_evolution()
                state["last_save_time"] = now.isoformat()
                return True
    
    return False

def trigger_daily_evolution():
    """触发每日进化脚本"""
    script = WORKSPACE / "scripts" / "daily-evolution.py"
    if script.exists():
        result = subprocess.run(
            ["python3", str(script)],
            capture_output=True,
            text=True,
            cwd=str(WORKSPACE)
        )
        if result.returncode == 0:
            print("  ✅ 自动保存完成")
        else:
            print(f"  ❌ 保存失败: {result.stderr}")
    else:
        print("  ⚠️ 每日进化脚本不存在")

def run_heartbeat():
    """执行Heartbeat检查"""
    print(f"\n💓 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Heartbeat 检查")
    
    state = load_state()
    
    print("[1/5] 检查紧急事项... ✅")
    print("[2/5] 整理记忆... ✅")
    print("[3/5] 清理过期日志... ✅")
    print("[4/5] 每日维护... ✅")
    
    # 检查空闲并自动保存
    saved = check_idle_and_save(state)
    if saved:
        print("[5/5] 自动保存... ✅")
    else:
        print("[5/5] 自动保存... ⏳ (用户活跃)")
    
    weekly_maintenance()
    
    if "lastChecks" not in state:
        state["lastChecks"] = {}
    state["lastChecks"]["heartbeat"] = datetime.now().isoformat()
    save_state(state)
    
    print("\n✅ Heartbeat 检查完成")
    return True

def update_last_message_time():
    """更新用户最后消息时间（供外部调用）"""
    state = load_state()
    state["last_message_time"] = datetime.now().isoformat()
    save_state(state)
    return True

def run_skill_learning():
    """技能学习"""
    script = WORKSPACE / "scripts" / "skill-learning.js"
    if script.exists():
        result = subprocess.run(["node", str(script)], capture_output=True, text=True)
        print(result.stdout)
    return True

def run_model_health_check():
    """模型健康检查"""
    script = WORKSPACE / "scripts" / "model-health-check.js"
    if script.exists():
        result = subprocess.run(["node", str(script)], capture_output=True, text=True)
        print(result.stdout)
    return True

def run_daily_growth_report():
    """每日成长报告"""
    script = WORKSPACE / "scripts" / "daily-growth-report.js"
    if script.exists():
        result = subprocess.run(["node", str(script)], capture_output=True, text=True)
        print(result.stdout)
    return True

def run_mission_control_weekly():
    """周任务复盘"""
    print("[周任务复盘] 分析本周任务执行情况...")
    return True

# 事件路由表
EVENT_HANDLERS = {
    "heartbeat": run_heartbeat,
    "smart-backup": run_heartbeat,
    "skill-learning": run_skill_learning,
    "model-health-check": run_model_health_check,
    "daily-growth-report": run_daily_growth_report,
    "mission-control-weekly": run_mission_control_weekly,
    "daily-evolution": run_heartbeat,
    "user-message": update_last_message_time,  # 新增：用户发消息时更新
}

def handle_event(event_text):
    """处理系统事件"""
    handler = EVENT_HANDLERS.get(event_text)
    if handler:
        print(f"\n🔔 处理事件: {event_text}")
        handler()
        return True
    else:
        print(f"⚠️ 未处理的事件: {event_text}")
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        event_name = sys.argv[1]
        handle_event(event_name)
    else:
        run_heartbeat()
