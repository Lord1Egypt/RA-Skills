#!/usr/bin/env python3
"""
关心记忆系统 v2.0
- 智能任务提醒（按优先级 + 艾宾浩斯曲线）
- 活跃时间学习
- 游戏化激励
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).parent
TASKS_FILE = BASE_DIR / "tasks.json"
CONFIG_FILE = BASE_DIR / "config.json"
ACTIVITY_FILE = BASE_DIR / "activity_log.json"
STATS_FILE = BASE_DIR / "stats.json"

PRIORITY_ORDER = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
STATUS_ACTIVE = {"pending", "reminded"}
EBBINGHAUS_LABELS = ["1小时后", "第2天", "第4天", "第7天", "第15天"]


def _load(path: Path, default=None):
    if path.exists():
        return json.loads(path.read_text("utf-8"))
    return default or {}


def _save(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")


def load_tasks():
    return _load(TASKS_FILE, {"tasks": [], "next_id": 1})


def save_tasks(data):
    _save(TASKS_FILE, data)


def load_config():
    return _load(CONFIG_FILE)


def load_stats():
    return _load(STATS_FILE, {
        "xp": 0, "level": "虾苗", "streak_days": 0,
        "last_chat_date": None, "tasks_completed_today": 0,
        "total_tasks_completed": 0, "achievements": [],
        "daily_reset_date": None
    })


def save_stats(data):
    _save(STATS_FILE, data)


def load_activity():
    return _load(ACTIVITY_FILE, {"activity_buckets": {}, "reminder_adjustments": {}, "learned": False})


def save_activity(data):
    _save(ACTIVITY_FILE, data)


# ── 任务管理 ──

def add_task(title: str, priority: str = "medium", deadline: Optional[str] = None,
             category: str = "general", description: str = "", recurring: Optional[str] = None) -> dict:
    """添加任务。priority: urgent/high/medium/low"""
    data = load_tasks()
    now = datetime.now().isoformat()
    task = {
        "id": data["next_id"],
        "title": title,
        "description": description,
        "priority": priority,
        "category": category,
        "status": "pending",
        "deadline": deadline,
        "recurring": recurring,
        "created_at": now,
        "reminded_at": [],
        "completed_at": None,
        "ebbinghaus_step": 0,
        "next_remind": now  # 立即提醒一次
    }
    data["tasks"].append(task)
    data["next_id"] += 1
    save_tasks(data)
    return task


def complete_task(task_id: int) -> Optional[dict]:
    data = load_tasks()
    for t in data["tasks"]:
        if t["id"] == task_id and t["status"] in STATUS_ACTIVE:
            t["status"] = "done"
            t["completed_at"] = datetime.now().isoformat()
            save_tasks(data)
            _add_xp("complete_task")
            _check_daily_reset()
            stats = load_stats()
            stats["tasks_completed_today"] += 1
            stats["total_tasks_completed"] += 1
            save_stats(stats)
            _check_achievements()
            return t
    return None


def cancel_task(task_id: int) -> Optional[dict]:
    data = load_tasks()
    for t in data["tasks"]:
        if t["id"] == task_id and t["status"] in STATUS_ACTIVE:
            t["status"] = "cancelled"
            save_tasks(data)
            return t
    return None


def list_tasks(status_filter: Optional[str] = None, priority_filter: Optional[str] = None) -> list:
    data = load_tasks()
    tasks = data["tasks"]
    if status_filter:
        tasks = [t for t in tasks if t["status"] == status_filter]
    elif status_filter is None:
        tasks = [t for t in tasks if t["status"] in STATUS_ACTIVE]
    if priority_filter:
        tasks = [t for t in tasks if t["priority"] == priority_filter]
    tasks.sort(key=lambda t: PRIORITY_ORDER.get(t.get("priority", "low"), 3))
    return tasks


# ── 优先级自动升级 ──

def auto_upgrade_priority():
    """接近截止日的任务自动升级优先级"""
    config = load_config()
    data = load_tasks()
    now = datetime.now()
    rules = config.get("priority_upgrade", {}).get("hours_before_deadline", {})
    changed = False

    for t in data["tasks"]:
        if t["status"] not in STATUS_ACTIVE or not t.get("deadline"):
            continue
        try:
            dl = datetime.fromisoformat(t["deadline"])
        except (ValueError, TypeError):
            continue
        hours_left = (dl - now).total_seconds() / 3600

        if t["priority"] == "high" and hours_left <= rules.get("high_to_urgent", 24):
            t["priority"] = "urgent"
            changed = True
        elif t["priority"] == "medium" and hours_left <= rules.get("medium_to_high", 48):
            t["priority"] = "high"
            changed = True
        elif t["priority"] == "low" and hours_left <= rules.get("low_to_medium", 96):
            t["priority"] = "medium"
            changed = True

    if changed:
        save_tasks(data)


# ── 艾宾浩斯提醒 ──

def get_ebbinghaus_reminders() -> list:
    """返回需要艾宾浩斯提醒的任务"""
    config = load_config()
    intervals = config.get("ebbinghaus_intervals_hours", [1, 24, 96, 168, 360])
    data = load_tasks()
    now = datetime.now()
    reminders = []

    for t in data["tasks"]:
        if t["status"] not in STATUS_ACTIVE:
            continue
        created = datetime.fromisoformat(t["created_at"])
        step = t.get("ebbinghaus_step", 0)
        if step >= len(intervals):
            continue
        next_time = created + timedelta(hours=intervals[step])
        if now >= next_time:
            label = EBBINGHAUS_LABELS[step] if step < len(EBBINGHAUS_LABELS) else f"第{step+1}次"
            reminders.append({
                "task": t,
                "step": step,
                "label": label
            })

    return reminders


def mark_ebbinghaus_reminded(task_id: int, step: int):
    data = load_tasks()
    for t in data["tasks"]:
        if t["id"] == task_id:
            t["ebbinghaus_step"] = step + 1
            t["reminded_at"].append(datetime.now().isoformat())
            save_tasks(data)
            return


# ── 生成提醒摘要 ──

def generate_reminder_summary() -> str:
    """生成当前时段的提醒摘要"""
    auto_upgrade_priority()

    tasks = list_tasks()
    if not tasks:
        return ""

    # 按优先级分组
    groups = {}
    for t in tasks:
        p = t.get("priority", "medium")
        groups.setdefault(p, []).append(t)

    lines = ["📋 **今日待办提醒**\n"]
    priority_emoji = {"urgent": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
    priority_label = {"urgent": "紧急", "high": "高", "medium": "中", "low": "低"}

    for p in ["urgent", "high", "medium", "low"]:
        if p not in groups:
            continue
        emoji = priority_emoji.get(p, "⚪")
        label = priority_label.get(p, p)
        lines.append(f"{emoji} **{label}优先级**")
        for t in groups[p]:
            deadline_str = ""
            if t.get("deadline"):
                try:
                    dl = datetime.fromisoformat(t["deadline"])
                    deadline_str = f" | 截止: {dl.strftime('%m/%d %H:%M')}"
                except:
                    pass
            recurring_str = f" | 🔄 {t['recurring']}" if t.get("recurring") else ""
            lines.append(f"  • #{t['id']} {t['title']}{deadline_str}{recurring_str}")
        lines.append("")

    # 艾宾浩斯提醒
    eb_reminders = get_ebbinghaus_reminders()
    if eb_reminders:
        lines.append("🧠 **复习提醒**")
        for r in eb_reminders:
            t = r["task"]
            lines.append(f"  • #{t['id']} {t['title']} — {r['label']}")
        lines.append("")

    return "\n".join(lines)


# ── 活跃时间学习 ──

def record_activity():
    """记录当前活跃时间"""
    data = load_activity()
    now = datetime.now()
    bucket = f"{now.hour:02d}"  # 按小时分桶
    date_key = now.strftime("%Y-%m-%d")

    if date_key not in data["activity_buckets"]:
        data["activity_buckets"][date_key] = {}
    data["activity_buckets"][date_key][bucket] = data["activity_buckets"][date_key].get(bucket, 0) + 1

    # 只保留最近30天
    cutoff = (now - timedelta(days=30)).strftime("%Y-%m-%d")
    data["activity_buckets"] = {k: v for k, v in data["activity_buckets"].items() if k >= cutoff}

    # 如果有7天以上数据，计算最佳提醒时间
    if len(data["activity_buckets"]) >= 7:
        _learn_best_times(data)

    save_activity(data)


def _learn_best_times(data):
    """从历史数据学习最佳提醒时间"""
    hour_counts = {}
    for date_buckets in data["activity_buckets"].values():
        for hour, count in date_buckets.items():
            hour_counts[hour] = hour_counts.get(hour, 0) + count

    # 找出活跃度最高的时段
    sorted_hours = sorted(hour_counts.items(), key=lambda x: -x[1])
    top_hours = [h for h, c in sorted_hours[:5]]

    data["reminder_adjustments"] = {
        "learned_hours": top_hours,
        "learned_at": datetime.now().isoformat()
    }
    data["learned"] = True


def get_learned_active_hours() -> list:
    data = load_activity()
    return data.get("reminder_adjustments", {}).get("learned_hours", [])


# ── 游戏化 ──

def _add_xp(action: str):
    config = load_config()
    stats = load_stats()
    xp_rules = config.get("gamification", {}).get("xp_rules", {})
    gain = xp_rules.get(action, 0)
    stats["xp"] += gain
    _update_level(stats)
    save_stats(stats)


def _update_level(stats):
    config = load_config()
    levels = config.get("gamification", {}).get("levels", [])
    current_level = "虾苗"
    for lvl in levels:
        if stats["xp"] >= lvl["xp"]:
            current_level = lvl["name"]
    stats["level"] = current_level


def _check_daily_reset():
    stats = load_stats()
    today = datetime.now().strftime("%Y-%m-%d")
    if stats.get("daily_reset_date") != today:
        stats["tasks_completed_today"] = 0
        stats["daily_reset_date"] = today

        # 连续天数
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        if stats.get("last_chat_date") == yesterday:
            stats["streak_days"] += 1
            _add_xp("daily_chat")
            if stats["streak_days"] > 1:
                # 连续奖励
                config = load_config()
                streak_xp = config.get("gamification", {}).get("xp_rules", {}).get("streak_bonus_per_day", 5)
                stats["xp"] += streak_xp * min(stats["streak_days"], 7)
        elif stats.get("last_chat_date") != today:
            stats["streak_days"] = 1

        stats["last_chat_date"] = today
        save_stats(stats)


def record_chat_activity():
    """每次对话时调用"""
    _check_daily_reset()
    record_activity()
    _check_achievements()


def _check_achievements():
    stats = load_stats()
    new_achievements = []

    if "连续7天" not in stats["achievements"] and stats["streak_days"] >= 7:
        new_achievements.append("连续7天")
    if "效率王者" not in stats["achievements"] and stats["tasks_completed_today"] >= 5:
        new_achievements.append("效率王者")
    if "早起鸟" not in stats["achievements"] and datetime.now().hour < 8:
        # 简化：8点前对话
        if stats["streak_days"] >= 7:
            new_achievements.append("早起鸟")

    if new_achievements:
        stats["achievements"].extend(new_achievements)
        save_stats(stats)


def get_stats_summary() -> str:
    stats = load_stats()
    lines = [
        f"🎮 **等级**: {stats['level']} | **XP**: {stats['xp']}",
        f"🔥 **连续**: {stats['streak_days']}天 | **今日完成**: {stats['tasks_completed_today']}个",
        f"📊 **累计完成**: {stats['total_tasks_completed']}个任务",
    ]
    if stats["achievements"]:
        lines.append(f"🏆 **成就**: {', '.join(stats['achievements'])}")
    active_hours = get_learned_active_hours()
    if active_hours:
        lines.append(f"⏰ **你的活跃时段**: {', '.join(active_hours[:3])}点")
    return "\n".join(lines)


# ── 过期任务处理 ──

def expire_overdue_tasks():
    data = load_tasks()
    now = datetime.now()
    changed = False
    for t in data["tasks"]:
        if t["status"] not in STATUS_ACTIVE or not t.get("deadline"):
            continue
        try:
            dl = datetime.fromisoformat(t["deadline"])
            if now > dl + timedelta(hours=24):  # 宽限24小时
                t["status"] = "expired"
                changed = True
        except:
            pass
    if changed:
        save_tasks(data)


# ── CLI ──

def main():
    if len(sys.argv) < 2:
        print("用法: caring_memory.py <command> [args]")
        print("命令: add/complete/cancel/list/summary/remind/stats/expire")
        return

    cmd = sys.argv[1]

    if cmd == "add":
        title = sys.argv[2] if len(sys.argv) > 2 else "未命名任务"
        priority = sys.argv[3] if len(sys.argv) > 3 else "medium"
        deadline = sys.argv[4] if len(sys.argv) > 4 else None
        t = add_task(title, priority, deadline)
        print(f"✅ 任务已添加: #{t['id']} {t['title']} [{t['priority']}]")

    elif cmd == "complete":
        tid = int(sys.argv[2])
        t = complete_task(tid)
        if t:
            print(f"🎉 完成: #{t['id']} {t['title']}")
        else:
            print("❌ 任务不存在或已完成")

    elif cmd == "cancel":
        tid = int(sys.argv[2])
        t = cancel_task(tid)
        if t:
            print(f"🗑️ 取消: #{t['id']} {t['title']}")
        else:
            print("❌ 任务不存在")

    elif cmd == "list":
        tasks = list_tasks()
        if not tasks:
            print("📭 没有待办任务")
        for t in tasks:
            dl = f" | 截止: {t['deadline'][:10]}" if t.get("deadline") else ""
            print(f"  #{t['id']} [{t['priority']}] {t['title']}{dl}")

    elif cmd == "summary":
        print(generate_reminder_summary())

    elif cmd == "remind":
        # 供 cron 调用，输出提醒内容
        expire_overdue_tasks()
        summary = generate_reminder_summary()
        if summary:
            print(summary)

    elif cmd == "stats":
        print(get_stats_summary())

    elif cmd == "expire":
        expire_overdue_tasks()
        print("✅ 过期任务已标记")

    elif cmd == "chat":
        # 每次对话时调用
        record_chat_activity()
        print(f"✅ 活跃记录已更新 | 等级: {load_stats()['level']}")

    else:
        print(f"未知命令: {cmd}")


if __name__ == "__main__":
    main()
