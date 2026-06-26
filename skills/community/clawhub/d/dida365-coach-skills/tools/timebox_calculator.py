"""时间盒计算、格式化与改排程。"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta
from typing import Dict, List, Optional


def _truncate_title(task_description: str, limit: int = 20) -> str:
    if len(task_description) <= limit:
        return task_description
    return f"{task_description[:limit]}..."


def generate_deliverable(task: str, box_num: int, total_boxes: int) -> str:
    """按任务类型和时间盒序号生成预期成果。"""

    templates = {
        "报告": {
            1: "完成背景介绍和现状概述",
            2: "梳理问题清单",
            3: "给出解决方案",
            4: "整合完整报告",
        },
        "写作": {
            1: "完成大纲和开头",
            2: "完成主体第一部分",
            3: "完成主体第二部分",
            4: "完成结尾和润色",
        },
        "代码": {
            1: "完成核心逻辑框架",
            2: "实现主要功能",
            3: "处理边界情况",
            4: "补测试并优化",
        },
        "学习": {
            1: "通读材料并标记重点",
            2: "整理笔记和知识框架",
            3: "攻克难点并形成总结",
            4: "完成回顾和应用练习",
        },
    }

    for keyword, template in templates.items():
        if keyword in task:
            return template.get(box_num, f"完成第 {box_num}/{total_boxes} 部分")

    if total_boxes == 1:
        return f"完成{task}"
    if box_num == 1:
        return "完成框架和第一部分"
    if box_num == total_boxes:
        return "完成最后部分和整理"
    return f"完成第 {box_num}/{total_boxes} 部分"


def calculate_timeboxes(
    task_description: str,
    estimated_minutes: int,
    start_time: datetime,
    work_method: Dict[str, int],
) -> List[Dict[str, object]]:
    """根据任务时长和工作法配置生成时间盒列表。"""

    focus_time = int(work_method.get("focus", 30))
    short_break = int(work_method.get("short_break", 5))
    long_break = int(work_method.get("long_break", 15))
    boxes_before_long = int(work_method.get("boxes_before_long", 4))

    num_boxes = max(1, (estimated_minutes + focus_time - 1) // focus_time)
    boxes: List[Dict[str, object]] = []
    current_time = start_time
    remaining_minutes = max(estimated_minutes, focus_time)

    for index in range(num_boxes):
        box_num = index + 1
        current_focus = min(focus_time, remaining_minutes) if index == num_boxes - 1 else focus_time
        box_start = current_time
        box_end = box_start + timedelta(minutes=current_focus)
        deliverable = generate_deliverable(task_description, box_num, num_boxes)

        boxes.append(
            {
                "number": box_num,
                "start_time": box_start,
                "end_time": box_end,
                "focus_minutes": current_focus,
                "deliverable": deliverable,
                "task_title": f"📦 盒子 {box_num}: {_truncate_title(task_description)}",
            }
        )

        remaining_minutes -= current_focus
        if index == num_boxes - 1:
            continue

        break_minutes = long_break if box_num % boxes_before_long == 0 else short_break
        current_time = box_end + timedelta(minutes=break_minutes)

    return boxes


def format_timebox_schedule(boxes: List[Dict[str, object]]) -> str:
    """将时间盒格式化为人类可读文本。"""

    lines: List[str] = []
    for box in boxes:
        start = box["start_time"].strftime("%H:%M")
        end = box["end_time"].strftime("%H:%M")
        lines.append(
            f"📦 盒子 {box['number']} | {start}-{end} | 成果：{box['deliverable']} ✓"
        )
        lines.append(f"   └─ {box['task_title']}")
        lines.append("")
    return "\n".join(lines).strip()


def reschedule_boxes(
    boxes: List[Dict[str, object]],
    box_number: Optional[int] = None,
    new_start_time: Optional[datetime] = None,
    adjustment_minutes: Optional[int] = None,
) -> List[Dict[str, object]]:
    """返回重新排程后的时间盒列表。"""

    if not boxes:
        return []

    updated = deepcopy(boxes)
    start_index = max(0, (box_number - 1) if box_number else 0)

    if adjustment_minutes is not None:
        offset = timedelta(minutes=adjustment_minutes)
    elif new_start_time is not None:
        original_start = updated[start_index]["start_time"]
        offset = new_start_time - original_start
    else:
        return updated

    for index in range(start_index, len(updated)):
        updated[index]["start_time"] += offset
        updated[index]["end_time"] += offset

    return updated


def extend_box_duration(
    boxes: List[Dict[str, object]],
    box_number: int,
    new_focus_minutes: int,
) -> List[Dict[str, object]]:
    """调整指定时间盒时长，并顺延后续盒子。"""

    if not boxes or box_number < 1 or box_number > len(boxes):
        return deepcopy(boxes)

    updated = deepcopy(boxes)
    index = box_number - 1
    box = updated[index]
    original_minutes = int(box["focus_minutes"])
    delta_minutes = new_focus_minutes - original_minutes
    if delta_minutes == 0:
        return updated

    box["focus_minutes"] = new_focus_minutes
    box["end_time"] = box["start_time"] + timedelta(minutes=new_focus_minutes)

    offset = timedelta(minutes=delta_minutes)
    for follower in updated[index + 1 :]:
        follower["start_time"] += offset
        follower["end_time"] += offset

    return updated
