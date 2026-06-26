"""分析任务完成情况并生成复盘文本。"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional

from .dida_semantics import is_current_task_completed


def _parse_iso_datetime(value: str) -> Optional[datetime]:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


def _is_completed(task: Dict[str, object]) -> bool:
    return is_current_task_completed(task)


def analyze_daily_tasks(tasks: List[Dict[str, object]]) -> Dict[str, object]:
    """分析当天任务完成率、高效时段与类型分布。"""

    if not tasks:
        return {
            "total": 0,
            "completed": 0,
            "completion_rate": 0.0,
            "peak_hours": [],
            "type_distribution": {},
        }

    total = len(tasks)
    completed = sum(1 for task in tasks if _is_completed(task))

    hour_distribution: Dict[int, Dict[str, int]] = defaultdict(
        lambda: {"completed": 0, "total": 0}
    )
    type_distribution: Dict[str, int] = defaultdict(int)

    for task in tasks:
        task_time = _parse_iso_datetime(
            str(task.get("due_date") or task.get("start_date") or "")
        )
        if task_time:
            hour_distribution[task_time.hour]["total"] += 1
            if _is_completed(task):
                hour_distribution[task_time.hour]["completed"] += 1

        tags = [str(tag).lower() for tag in task.get("tags", [])]
        if any(tag in {"工作", "work"} for tag in tags):
            type_distribution["work"] += 1
        elif any(tag in {"学习", "study"} for tag in tags):
            type_distribution["study"] += 1
        elif any(tag in {"生活", "life"} for tag in tags):
            type_distribution["life"] += 1
        else:
            type_distribution["other"] += 1

    ranked_hours = sorted(
        hour_distribution.items(),
        key=lambda item: item[1]["completed"] / max(item[1]["total"], 1),
        reverse=True,
    )[:2]

    return {
        "total": total,
        "completed": completed,
        "completion_rate": round(completed / total * 100, 1),
        "peak_hours": [
            f"{hour:02d}:00-{(hour + 1) % 24:02d}:00"
            for hour, stats in ranked_hours
            if stats["total"] > 0
        ],
        "type_distribution": dict(type_distribution),
    }


def analyze_weekly_trends(daily_stats: List[Dict[str, object]]) -> Dict[str, object]:
    """分析一周的完成率趋势。"""

    if not daily_stats:
        return {}

    completion_rates = [float(day.get("completion_rate", 0.0)) for day in daily_stats]
    avg_rate = sum(completion_rates) / len(completion_rates)
    best_day = max(daily_stats, key=lambda item: float(item.get("completion_rate", 0.0)))
    worst_day = min(daily_stats, key=lambda item: float(item.get("completion_rate", 0.0)))

    midpoint = len(completion_rates) // 2
    first_half = sum(completion_rates[:midpoint]) / max(midpoint, 1)
    second_half = sum(completion_rates[midpoint:]) / max(len(completion_rates) - midpoint, 1)

    if second_half > first_half + 10:
        trend = "上升"
    elif second_half < first_half - 10:
        trend = "下降"
    else:
        trend = "平稳"

    return {
        "average_completion_rate": round(avg_rate, 1),
        "best_day": best_day,
        "worst_day": worst_day,
        "trend": trend,
        "daily_rates": completion_rates,
    }


def identify_missed_patterns(missed_tasks: List[Dict[str, object]]) -> List[Dict[str, str]]:
    """识别重复未完成和晚间低效等模式。"""

    patterns: List[Dict[str, str]] = []
    if not missed_tasks:
        return patterns

    task_names: Dict[str, int] = defaultdict(int)
    evening_missed = 0

    for task in missed_tasks:
        name = str(task.get("title", "")).strip().split(" ")[0]
        if name:
            task_names[name] += 1

        task_time = _parse_iso_datetime(str(task.get("due_date") or ""))
        if task_time and task_time.hour >= 18:
            evening_missed += 1

    recurring = [f"{name}({count}次)" for name, count in task_names.items() if count >= 2]
    if recurring:
        patterns.append(
            {
                "type": "recurring_missed",
                "description": f"重复未完成：{', '.join(recurring)}",
                "suggestion": "建议进一步拆解任务，或把目标难度调低一档。",
            }
        )

    if evening_missed > len(missed_tasks) * 0.5:
        patterns.append(
            {
                "type": "evening_slump",
                "description": "晚上任务完成率较低",
                "suggestion": "把重要任务前移到上午或午后精力高点。",
            }
        )

    return patterns


def suggest_automation(tasks: List[Dict[str, object]]) -> List[str]:
    """识别高频重复任务并给出自动化建议。"""

    keywords = ["回复邮件", "查收邮件", "日报", "周报", "打卡", "备份"]
    task_patterns: Dict[str, int] = defaultdict(int)

    for task in tasks:
        title = str(task.get("title", ""))
        for keyword in keywords:
            if keyword in title:
                task_patterns[keyword] += 1

    return [
        f"“{pattern}”本周出现 {count} 次，建议设置循环任务或自动提醒。"
        for pattern, count in task_patterns.items()
        if count >= 3
    ]


def generate_daily_report(tasks: List[Dict[str, object]]) -> str:
    """生成紧凑版日复盘文本。"""

    stats = analyze_daily_tasks(tasks)
    lines = [
        "📊 今日概览",
        f"• 完成任务：{stats['completed']}/{stats['total']} ({stats['completion_rate']}%)",
    ]

    if stats["peak_hours"]:
        lines.append(f"• 高峰时段：{', '.join(stats['peak_hours'])}")

    type_dist = stats.get("type_distribution", {})
    if type_dist:
        distribution = " | ".join(f"{key} {value}个" for key, value in type_dist.items())
        lines.append(f"• 任务分布：{distribution}")

    return "\n".join(lines)


def generate_weekly_report(tasks_by_day: Dict[str, List[Dict[str, object]]]) -> str:
    """生成周复盘摘要。"""

    daily_stats = [analyze_daily_tasks(tasks) for tasks in tasks_by_day.values()]
    trends = analyze_weekly_trends(daily_stats)

    all_tasks: List[Dict[str, object]] = []
    for tasks in tasks_by_day.values():
        all_tasks.extend(tasks)

    missed_tasks = [task for task in all_tasks if not _is_completed(task)]
    patterns = identify_missed_patterns(missed_tasks)
    automation = suggest_automation(all_tasks)

    lines = [
        "📈 本周统计",
        f"• 平均完成率：{trends.get('average_completion_rate', 0)}%",
        f"• 趋势：{trends.get('trend', '未知')}",
        "",
        "🏆 本周亮点",
        f"• 最高完成率：{trends.get('best_day', {}).get('completion_rate', 0)}%",
    ]

    if patterns:
        lines.extend(["", "🔍 改进点"])
        for pattern in patterns:
            lines.append(f"• {pattern['description']}")
            lines.append(f"  建议：{pattern['suggestion']}")

    if automation:
        lines.extend(["", "🤖 自动化建议"])
        for item in automation:
            lines.append(f"• {item}")

    return "\n".join(lines)
