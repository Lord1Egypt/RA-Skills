"""任务数据验证器 — 自动检测 API/Base 返回格式异常。

当前检测项：
  - 状态字段是否为字符串（曾变为 list 导致 status 崩溃）
  - API任务ID 是否为字符串
  - 必要字段是否存在
  - 字段值异常（空/过长/类型不符）

自动修复常见问题并记录警告，方便快速定位 API 升级后的兼容问题。
"""
from typing import Any

# 验证规则：字段名 → (类型, 是否必填, 说明)
# 支持别名：记录中只要任一别名有值即视为存在，用第一个找到的别名取值。
_FIELD_RULES: dict[str, tuple[type, bool, str, list[str]]] = {
    "状态": (str, True, "任务状态（queued/completed/failed/pending）", ["status"]),
    "API任务ID": (str, False, "Agnes API 任务 ID", ["task_id"]),
    "镜头ID": (str, False, "镜头标识（shot_01）", []),
    "对应视频任务ID": (str, False, "飞书文档 ID", []),
}

_WARNED_ISSUES: set[str] = set()


def _warn_once(key: str, msg: str) -> None:
    """同 session 同 warning 只打一次。"""
    if key not in _WARNED_ISSUES:
        _WARNED_ISSUES.add(key)
        print(f"  [validator] ⚠️ {msg}", flush=True)


def validate_task(data: dict[str, Any]) -> dict[str, Any]:
    """验证并修复单条任务数据，返回修复后的副本。

    自动修复：
      - 状态字段是 list → 取第一个元素
      - API任务ID 是数字 → 转字符串
      - 缺失必填字段 → 补充默认值
    """
    fixed = dict(data)

    for field, (expected_type, required, desc, aliases) in _FIELD_RULES.items():
        val = fixed.get(field)
        # 若主要字段为空，尝试别名（如 "status" 对应 "状态"）
        if val is None or val == "" or val == []:
            for alias in aliases:
                alias_val = fixed.get(alias)
                if alias_val is not None and alias_val != "" and alias_val != []:
                    val = alias_val
                    break

        if val is None or val == "" or val == []:
            if required:
                _warn_once(f"missing_{field}",
                           f"字段 '{field}' 缺失（{desc}），自动补充 'pending'")
                fixed[field] = "pending"
            continue

        # 类型修正
        if isinstance(val, list):
            _warn_once(f"type_list_{field}",
                       f"字段 '{field}' 是 list={val}，应是 {expected_type.__name__}。"
                       f"可能原因：API/Base 表格式变更。已取第一个值修复")
            fixed[field] = str(val[0]) if val else "pending"

        elif not isinstance(val, expected_type):
            try:
                fixed_val = expected_type(val)
                _warn_once(f"type_cast_{field}",
                           f"字段 '{field}' 类型是 {type(val).__name__}，"
                           f"期望 {expected_type.__name__}。已自动转换")
                fixed[field] = fixed_val
            except (ValueError, TypeError):
                _warn_once(f"type_err_{field}",
                           f"字段 '{field}' 类型 {type(val).__name__} 无法转为 "
                           f"{expected_type.__name__}（{desc}），值={repr(val)[:100]}")
                if required:
                    fixed[field] = "pending"

    return fixed


def validate_task_list(shots: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """验证并修复整批任务数据。每个 shot 独立修复。"""
    return [validate_task(s) for s in shots]


def reset_warnings() -> None:
    """清空警告缓存（测试用）。"""
    _WARNED_ISSUES.clear()
