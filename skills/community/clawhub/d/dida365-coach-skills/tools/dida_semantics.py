"""滴答清单字段语义与保守判定规则。"""

from __future__ import annotations

from typing import Any, Dict, Optional

PRIORITY_NAME_TO_NUMERIC = {
    "none": 0,
    "low": 1,
    "medium": 3,
    "high": 5,
}

PRIORITY_TOKEN_TO_NAME = {
    "!1": "low",
    "!2": "medium",
    "!3": "high",
}

PRIORITY_LABELS = {
    "none": "无优先级",
    "low": "低优先级",
    "medium": "中优先级",
    "high": "高优先级",
}

COMPLETED_STATUS_STRINGS = {
    "completed",
    "complete",
    "done",
    "closed",
    "finished",
}

PENDING_STATUS_STRINGS = {
    "pending",
    "todo",
    "open",
    "normal",
    "incomplete",
}


def normalize_priority_name(value: Optional[str]) -> Optional[str]:
    """把口语化或符号化优先级归一为 low/medium/high/none。"""

    if value is None:
        return None

    normalized = str(value).strip().lower()
    if not normalized:
        return None

    if normalized in PRIORITY_NAME_TO_NUMERIC:
        return normalized
    if normalized in PRIORITY_TOKEN_TO_NAME:
        return PRIORITY_TOKEN_TO_NAME[normalized]
    if normalized in {"低", "低优先级", "low priority"}:
        return "low"
    if normalized in {"中", "中优先级", "medium priority"}:
        return "medium"
    if normalized in {"高", "高优先级", "important", "urgent", "high priority"}:
        return "high"
    return None


def priority_to_numeric(value: Optional[str]) -> int:
    """将优先级名称转为滴答/TickTick 常见数值。"""

    name = normalize_priority_name(value) or "none"
    return PRIORITY_NAME_TO_NUMERIC[name]


def priority_label(value: Optional[str]) -> str:
    """返回人类可读优先级。"""

    name = normalize_priority_name(value) or "none"
    return PRIORITY_LABELS[name]


def is_current_task_completed(task: Dict[str, Any]) -> bool:
    """
    保守判断当前任务是否已完成。

    规则：
    - 优先信任显式布尔字段 `isCompleted` / `completed`
    - 其次信任明确的状态字符串
    - 数字状态仅在常见 completed 值 `2` 时视为完成
    - 不根据 `completedTime` 单独推断，避免把历史实例误判为当前已完成
    """

    for key in ("isCompleted", "completed"):
        value = task.get(key)
        if isinstance(value, bool):
            return value

    status = task.get("status")
    if isinstance(status, str):
        normalized = status.strip().lower()
        if normalized in COMPLETED_STATUS_STRINGS:
            return True
        if normalized in PENDING_STATUS_STRINGS:
            return False

    if isinstance(status, (int, float)):
        return int(status) == 2

    return False
