"""根据任务特征推荐工作法。"""

from __future__ import annotations

from typing import Dict

TASK_TYPE_MAPPING = {
    "编程": "long_pomodoro",
    "代码": "long_pomodoro",
    "写作": "long_pomodoro",
    "设计": "long_pomodoro",
    "论文": "ultradian",
    "报告": "flexible_pomodoro",
    "邮件": "flexible_pomodoro",
    "回复": "flexible_pomodoro",
    "沟通": "flexible_pomodoro",
    "会议": "flexible_pomodoro",
    "学习": "flexible_pomodoro",
    "阅读": "flexible_pomodoro",
    "笔记": "flexible_pomodoro",
    "头脑风暴": "ultradian",
    "创意": "ultradian",
    "策划": "long_pomodoro",
    "整理": "classic_pomodoro",
    "归档": "classic_pomodoro",
    "数据": "flexible_pomodoro",
}

METHOD_REASONING = {
    "flexible_pomodoro": "这个任务适合 30 分钟的节奏，既能保持专注，也方便中途调整。",
    "classic_pomodoro": "这个任务偏碎片化，经典番茄更利于快速迭代和清空收尾工作。",
    "long_pomodoro": "这是深度工作类型，建议用 50 分钟长番茄，减少上下文切换。",
    "ultradian": "这个任务需要长时间沉浸，90 分钟深度模式更容易进入状态。",
}


def recommend_work_method(task_description: str) -> str:
    """按关键字返回推荐工作法。"""

    for keyword, method in TASK_TYPE_MAPPING.items():
        if keyword in task_description:
            return method
    return "flexible_pomodoro"


def get_work_method_reasoning(task_description: str, method: str) -> str:
    """返回推荐理由；若方法与任务不匹配也给出通用解释。"""

    if not task_description:
        return METHOD_REASONING.get(method, METHOD_REASONING["flexible_pomodoro"])
    return METHOD_REASONING.get(method, METHOD_REASONING["flexible_pomodoro"])


def explain_work_method(method: str, config: Dict[str, object]) -> str:
    """把工作法配置格式化成简洁说明。"""

    methods = config.get("work_method", {}).get("methods", {})
    if not isinstance(methods, dict):
        return "使用默认配置。"

    method_config = methods.get(method, {})
    if not isinstance(method_config, dict) or not method_config:
        return "使用默认配置。"

    name = method_config.get("name", method)
    focus = method_config.get("focus", 30)
    short_break = method_config.get("short_break", 5)
    long_break = method_config.get("long_break", 15)
    boxes_before_long = method_config.get("boxes_before_long", 4)
    return (
        f"**{name}**：专注 {focus} 分钟，短休息 {short_break} 分钟，"
        f"每 {boxes_before_long} 个盒子后长休息 {long_break} 分钟。"
    )
