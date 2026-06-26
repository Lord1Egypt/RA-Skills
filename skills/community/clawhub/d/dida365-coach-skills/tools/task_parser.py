"""解析目标、时间盒和改时间请求。"""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from .dida_semantics import normalize_priority_name

GOAL_TYPE_KEYWORDS = {
    "skill": ["学", "提高", "掌握", "练习", "提升", "熟悉"],
    "habit": ["养成", "每天", "坚持", "打卡", "习惯"],
    "project": ["完成", "准备", "项目", "报告", "论文", "方案"],
}

DOMAIN_KEYWORDS = {
    "language": ["英语", "日语", "法语", "语言", "口语", "听力", "词汇"],
    "fitness": ["健身", "跑步", "运动", "减肥", "锻炼", "增肌"],
    "career": ["工作", "职业", "升职", "面试", "汇报", "技能"],
    "study": ["学习", "考试", "考证", "读书", "刷题", "课程"],
}

TIME_PATTERNS = [
    r"今天",
    r"明天",
    r"后天",
    r"今晚",
    r"明早",
    r"下周[一二三四五六日天]?",
    r"[上下]午",
    r"晚上?",
    r"\d{1,2}[:点]\d{0,2}",
]

PREFIX_PATTERNS = [
    r"^(我想|我要|我得|我需要|帮我|请帮我)",
    r"^(想要|打算)",
    r"(完成|做完|安排|规划)一下",
]


def parse_goal_input(text: str) -> Dict[str, Optional[str]]:
    """从长期目标描述中提取目标类型、领域与时间投入。"""

    result: Dict[str, Optional[str]] = {
        "raw_input": text,
        "goal_type": None,
        "domain": None,
        "time_commitment": None,
    }

    for goal_type, keywords in GOAL_TYPE_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            result["goal_type"] = goal_type
            break

    for domain, keywords in DOMAIN_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            result["domain"] = domain
            break

    time_match = re.search(r"(每天|每周)\s*(\d+)\s*(分钟|小时)", text)
    if time_match:
        result["time_commitment"] = "".join(time_match.groups())

    return result


def _strip_time_tokens(text: str) -> str:
    cleaned = text
    for pattern in TIME_PATTERNS:
        cleaned = re.sub(pattern, " ", cleaned)
    for pattern in PREFIX_PATTERNS:
        cleaned = re.sub(pattern, "", cleaned)
    cleaned = re.sub(r"^(我|把)\s*", "", cleaned)
    cleaned = re.sub(r"^(要|要去|需要)\s*", "", cleaned)
    cleaned = re.sub(r"(要完成|完成|做完|安排|规划)", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = re.sub(r"[，。,.]+$", "", cleaned)
    return cleaned.strip()


def _extract_relative_deadline(text: str) -> Optional[str]:
    now = datetime.now()
    hour = 18
    minute = 0

    time_match = re.search(r"(\d{1,2})(?:[:点](\d{1,2}))?", text)
    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2) or 0)
        if "下午" in text or "晚上" in text:
            if hour < 12:
                hour += 12

    due_at = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if "明天" in text:
        due_at += timedelta(days=1)
    elif "后天" in text:
        due_at += timedelta(days=2)
    elif "下周" in text:
        due_at += timedelta(days=7)
    elif "今天" in text or "今晚" in text:
        pass
    else:
        return None
    return due_at.isoformat(timespec="minutes")


def _estimate_duration(text: str) -> int:
    explicit = re.search(r"(\d+)\s*(分钟|小时)", text)
    if explicit:
        amount = int(explicit.group(1))
        return amount * 60 if explicit.group(2) == "小时" else amount

    project_keywords = ["报告", "论文", "项目", "方案", "PPT", "文档", "代码", "开发"]
    quick_keywords = ["邮件", "电话", "回复", "确认", "打卡", "表单"]
    deep_keywords = ["学习", "复习", "写作", "设计", "调研"]

    if any(keyword in text for keyword in project_keywords):
        return 120
    if any(keyword in text for keyword in quick_keywords):
        return 30
    if any(keyword in text for keyword in deep_keywords):
        return 90
    return 60


def _extract_reminder_offset_minutes(text: str) -> Optional[int]:
    match = re.search(r"提前\s*(\d+)\s*(分钟|小时)\s*提醒", text)
    if not match:
        return None
    amount = int(match.group(1))
    if match.group(2) == "小时":
        return amount * 60
    return amount


def _extract_list_name(text: str) -> Optional[str]:
    match = re.search(r"([^\s，,。；;]+清单)", text)
    if not match:
        return None
    return match.group(1)


def _strip_execution_metadata(text: str) -> str:
    cleaned = re.sub(r"提前\s*\d+\s*(分钟|小时)\s*提醒", " ", text)
    cleaned = re.sub(r"[高中低]优先级", " ", cleaned)
    cleaned = re.sub(r"!([123])", " ", cleaned)
    cleaned = re.sub(r"[^\s，,。；;]+清单", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = re.sub(r"[，,\s]+", "，", cleaned)
    cleaned = cleaned.strip("，。,. ")
    return cleaned


def parse_timebox_input(text: str) -> Dict[str, Optional[object]]:
    """从执行型请求中提取任务描述、截止时间与估算时长。"""

    task_description = _strip_execution_metadata(_strip_time_tokens(text))
    result: Dict[str, Optional[object]] = {
        "raw_input": text,
        "task_description": task_description or text.strip(),
        "deadline": _extract_relative_deadline(text),
        "estimated_duration": _estimate_duration(text),
        "priority": extract_priority(text),
        "reminder_offset_minutes": _extract_reminder_offset_minutes(text),
        "list_name": _extract_list_name(text),
    }
    return result


def extract_priority(text: str) -> Optional[str]:
    """从文本中提取高/中/低优先级。"""

    if "!3" in text:
        return "high"
    if "!2" in text:
        return "medium"
    if "!1" in text:
        return "low"
    if "高优先级" in text or "重要且紧急" in text:
        return "high"
    if "中优先级" in text:
        return "medium"
    if "低优先级" in text:
        return "low"
    if "重要" in text:
        return normalize_priority_name("high")
    return None


def extract_tags(text: str) -> List[str]:
    """提取形如 #标签 的标签列表。"""

    return re.findall(r"#([^\s#]+)", text)


def parse_reschedule_request(text: str) -> Dict[str, Optional[object]]:
    """解析改时间指令，支持单盒子、整体顺延和显式时间。"""

    result: Dict[str, Optional[object]] = {
        "box_number": None,
        "new_time": None,
        "adjustment": None,
        "adjustment_minutes": None,
    }

    box_match = re.search(r"盒子\s*(\d+)", text)
    if box_match:
        result["box_number"] = int(box_match.group(1))

    if "延后" in text or "推迟" in text or "顺延" in text:
        delta = re.search(r"(\d+)\s*(小时|分钟)", text)
        if delta:
            amount = int(delta.group(1))
            minutes = amount * 60 if delta.group(2) == "小时" else amount
            result["adjustment"] = f"delay_{minutes}m"
            result["adjustment_minutes"] = minutes

    if "提前" in text:
        delta = re.search(r"(\d+)\s*(小时|分钟)", text)
        if delta:
            amount = int(delta.group(1))
            minutes = amount * 60 if delta.group(2) == "小时" else amount
            result["adjustment"] = f"advance_{minutes}m"
            result["adjustment_minutes"] = -minutes

    target_text = None
    target_match = re.search(r"(?:改到|挪到|调到)(.+)$", text)
    if target_match:
        target_text = target_match.group(1)

    explicit_time = (
        re.search(r"(?:(上午|下午|晚上))?\s*(\d{1,2})(?:[:点](\d{1,2}))?", target_text)
        if target_text
        else None
    )
    if explicit_time:
        period = explicit_time.group(1) or ""
        hour = int(explicit_time.group(2))
        minute = int(explicit_time.group(3) or 0)
        if period in {"下午", "晚上"} and hour < 12:
            hour += 12
        result["new_time"] = f"{hour:02d}:{minute:02d}"

    return result
