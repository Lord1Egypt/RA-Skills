"""
BiliYouTik2Brain — CLI 交互层 (v4.0)

对话式交互 + 快捷指令 + 定时任务
支持全渠道：命令行 / 聊天窗口 / 定时任务
"""

import os
import json
import time
from typing import Dict, List, Optional


# ═══════════════════════════════════════════════════════════
#  对话式交互
# ═══════════════════════════════════════════════════════════

def cost_confirmation_dialog(estimate: Dict) -> str:
    """成本确认对话

    Args:
        estimate: {time_min, cost_cny, asr_engine, llm_backend}

    Returns:
        格式化确认提示
    """
    time_min = estimate.get("time_min", 0)
    cost = estimate.get("cost_cny", 0)

    if time_min < 1:
        time_str = f"{int(time_min * 60)}秒"
    else:
        time_str = f"{time_min:.0f}分钟"

    if cost < 0.01:
        cost_str = "几乎不花钱"
    elif cost < 0.1:
        cost_str = f"约 {int(cost * 10)} 毛"
    else:
        cost_str = f"约 {cost:.2f} 元"

    return (
        f"┌─────────────────────────────────┐\n"
        f"│  处理预估                        │\n"
        f"├─────────────────────────────────┤\n"
        f"│  预计时间: {time_str}\n"
        f"│  预计费用: {cost_str}\n"
        f"│  ASR: {estimate.get('asr_engine', 'auto')}\n"
        f"│  LLM: {estimate.get('llm_backend', 'auto')}\n"
        f"└─────────────────────────────────┘\n"
        f"\n确认开始？[Y/n]: "
    )


def output_format_selection_dialog(formats: List[str], auto_format: str) -> str:
    """输出格式选择对话"""
    lines = [
        "┌─────────────────────────────────┐",
        "│  输出格式选择                    │",
        "├─────────────────────────────────┤",
    ]

    format_names = {
        "note": "纯文本笔记",
        "rich": "图文并茂",
        "data": "结构化数据",
        "obsidian": "Obsidian 卡片",
    }

    for fmt in formats:
        name = format_names.get(fmt, fmt)
        auto_marker = " ← 推荐" if fmt == auto_format else ""
        lines.append(f"│  {fmt}: {name}{auto_marker}")

    lines.extend([
        "└─────────────────────────────────┘",
        "",
        "回复格式名切换，回车确认推荐格式",
    ])

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════
#  快捷指令
# ═══════════════════════════════════════════════════════════

QUICK_COMMANDS = {
    "/bili": {"desc": "处理 B站视频", "platform": "bilibili"},
    "/youte": {"desc": "处理 YouTube 视频", "platform": "youtube"},
    "/douyin": {"desc": "处理抖音视频", "platform": "douyin"},
    "/xhs": {"desc": "处理小红书视频", "platform": "xiaohongshu"},
    "/status": {"desc": "查看系统状态"},
    "/queue": {"desc": "查看任务队列"},
    "/env": {"desc": "环境诊断"},
    "/private": {"desc": "开启隐私模式"},
    "/channel": {"desc": "切换更新通道"},
}


def parse_quick_command(text: str) -> Optional[Dict]:
    """解析快捷指令

    Returns:
        {command, args} 或 None
    """
    text = text.strip()
    if not text.startswith("/"):
        return None

    parts = text.split(None, 1)
    cmd = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    if cmd in QUICK_COMMANDS:
        return {"command": cmd, "args": args, **QUICK_COMMANDS[cmd]}

    return None


# ═══════════════════════════════════════════════════════════
#  定时任务
# ═══════════════════════════════════════════════════════════

_SCHEDULE_FILE = os.path.expanduser("~/.biliyoutik2brain/schedule.json")


def add_schedule(
    url: str,
    schedule: str,  # cron 表达式或 "daily"/"weekly"
    output_format: str = "note",
) -> str:
    """添加定时任务

    Args:
        url: 视频链接或 UP 主页链接
        schedule: cron 表达式或预设
        output_format: 输出格式

    Returns:
        schedule_id
    """
    import uuid

    schedules = []
    if os.path.exists(_SCHEDULE_FILE):
        with open(_SCHEDULE_FILE, encoding="utf-8") as f:
            schedules = json.load(f)

    schedule_id = f"sch_{uuid.uuid4().hex[:8]}"
    schedules.append({
        "id": schedule_id,
        "url": url,
        "schedule": schedule,
        "output_format": output_format,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "enabled": True,
    })

    with open(_SCHEDULE_FILE, "w", encoding="utf-8") as f:
        json.dump(schedules, f, ensure_ascii=False, indent=2)

    return schedule_id


def list_schedules() -> List[Dict]:
    """列出定时任务"""
    if not os.path.exists(_SCHEDULE_FILE):
        return []
    with open(_SCHEDULE_FILE, encoding="utf-8") as f:
        return json.load(f)


def remove_schedule(schedule_id: str) -> bool:
    """删除定时任务"""
    if not os.path.exists(_SCHEDULE_FILE):
        return False

    with open(_SCHEDULE_FILE, encoding="utf-8") as f:
        schedules = json.load(f)

    filtered = [s for s in schedules if s.get("id") != schedule_id]
    if len(filtered) == len(schedules):
        return False

    with open(_SCHEDULE_FILE, "w", encoding="utf-8") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)

    return True
