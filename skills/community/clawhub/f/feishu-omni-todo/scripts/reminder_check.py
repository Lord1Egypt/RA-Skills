#!/usr/bin/env python3
"""
待办提醒检查脚本，每分钟运行一次，检查即将到期的待办并发送飞书提醒
"""
import os
import sys
import json
from datetime import datetime, timedelta
from todo_utils import load_todos, list_todos

# 飞书消息发送工具
FEISHU_SCRIPT = os.path.expanduser("~/.openclaw/skills/feishu-todo-manager/scripts/send_feishu_message.py")
REMINDER_LOG = os.path.expanduser("~/.openclaw/workspace/reminder_log.json")

def load_reminder_log() -> Dict:
    """加载已发送的提醒日志"""
    if not os.path.exists(REMINDER_LOG):
        return {"sent_reminders": {}}
    with open(REMINDER_LOG, "r", encoding="utf-8") as f:
        return json.load(f)

def save_reminder_log(data: Dict):
    """保存提醒日志"""
    with open(REMINDER_LOG, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def has_reminded(todo_id: int, remind_type: str) -> bool:
    """检查是否已经发送过该类型的提醒"""
    log = load_reminder_log()
    todo_key = str(todo_id)
    return todo_key in log["sent_reminders"] and remind_type in log["sent_reminders"][todo_key]

def mark_reminded(todo_id: int, remind_type: str):
    """标记已发送提醒"""
    log = load_reminder_log()
    todo_key = str(todo_id)
    if todo_key not in log["sent_reminders"]:
        log["sent_reminders"][todo_key] = []
    log["sent_reminders"][todo_key].append(remind_type)
    save_reminder_log(log)

def send_feishu_message(content: str) -> bool:
    """发送飞书消息给用户"""
    # 这里调用飞书消息发送API
    # 暂时使用系统消息通知，后续替换为实际飞书API调用
    print(f"[提醒] {content}")
    
    # 调用message工具发送飞书消息
    try:
        import subprocess
        cmd = [
            "openclaw", "message", "send",
            "--channel", "feishu",
            "--to", "ou_fd95eeaa259733145362ac2207654aaf",
            "--message", f"⏰ 待办提醒：\n{content}"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"发送消息失败: {e}")
        return False

def check_reminders():
    """检查待办提醒"""
    now = datetime.now()
    todos = list_todos()
    
    for todo in todos:
        if not todo.get("due_time"):
            continue
            
        try:
            due_time = datetime.fromisoformat(todo["due_time"])
            time_diff = due_time - now
            
            # 提前30分钟提醒
            if timedelta(minutes=25) <= time_diff <= timedelta(minutes=35):
                if not has_reminded(todo["id"], "30min"):
                    msg = f"即将到期：{todo['content']}\n⏰ 截止时间：{due_time.strftime('%Y-%m-%d %H:%M')}"
                    send_feishu_message(msg)
                    mark_reminded(todo["id"], "30min")
            
            # 提前5分钟提醒
            elif timedelta(minutes=0) <= time_diff <= timedelta(minutes=10):
                if not has_reminded(todo["id"], "5min"):
                    msg = f"马上到期！：{todo['content']}\n⏰ 截止时间：{due_time.strftime('%Y-%m-%d %H:%M')}"
                    send_feishu_message(msg)
                    mark_reminded(todo["id"], "5min")
            
            # 已过期提醒
            elif time_diff < timedelta(minutes=0) and abs(time_diff) < timedelta(hours=1):
                if not has_reminded(todo["id"], "overdue"):
                    msg = f"⚠️ 已逾期：{todo['content']}\n⏰ 截止时间：{due_time.strftime('%Y-%m-%d %H:%M')}"
                    send_feishu_message(msg)
                    mark_reminded(todo["id"], "overdue")
                    
        except Exception as e:
            print(f"处理待办 {todo['id']} 出错: {e}")
            continue

if __name__ == "__main__":
    check_reminders()
