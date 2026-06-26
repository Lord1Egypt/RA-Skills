"""
Demo Data Validator - 演示数据安全验证层

职责：
1. 检测当前是否运行在演示模式
2. 验证数据是否为演示数据，拒绝误用于真实决策
3. 在关键决策节点抛出警告，防止演示数据被滥用

使用方式：
    from safety.demo_validator import validate_not_demo_data, is_demo_mode

    data = query_inventory()
    validate_not_demo_data(data)  # 演示模式下抛出 DemoDataWarning
"""

from __future__ import annotations

import os
from typing import Any

# =============================================================================
# 异常定义
# =============================================================================

class DemoDataWarning(UserWarning):
    """
    演示数据警告

    当尝试在演示模式下使用数据进行真实决策时触发。
    继承自 UserWarning，允许被捕获但不应被静默忽略。
    """
    pass


class DemoDataError(Exception):
    """
    演示数据错误（严重）

    当检测到演示数据被用于需要真实数据的场景时触发。
    此异常不应被捕获，应立即终止操作。
    """
    pass


# =============================================================================
# 模式检测
# =============================================================================

def is_demo_mode() -> bool:
    """
    检测当前是否运行在演示模式

    判断优先级：
    1. 环境变量 SYSTEM_MODE == "demo"
    2. 环境变量 SYSTEM_MODE == "development"
    3. 未检测到真实 ERP 配置

    Returns:
        bool: True 表示当前为演示模式
    """
    mode = os.getenv("SYSTEM_MODE", "").lower()
    if mode in ("demo", "development"):
        return True

    # 检查是否配置了真实ERP（无ERP配置时默认demo）
    has_sap = bool(os.getenv("SAP_BASE_URL"))
    has_yonyou = bool(os.getenv("YONYOU_BASE_URL"))
    has_kingdee = bool(os.getenv("KINGDEE_BASE_URL"))

    if not (has_sap or has_yonyou or has_kingdee):
        return True  # 无真实ERP配置，强制为演示模式

    return False


def get_mode_label() -> str:
    """返回当前运行模式的标签"""
    if is_demo_mode():
        return "[⚠️ 演示模式]"
    return "[✅ 生产模式]"


# =============================================================================
# 数据验证
# =============================================================================

def _is_demo_data(data: Any) -> bool:
    """
    检测单条数据是否为演示数据

    通过 _demo 标记字段判断。
    支持 dict、list 包裹的结构。

    Args:
        data: 待检测的数据

    Returns:
        bool: True 表示为演示数据
    """
    if isinstance(data, dict):
        if data.get("_demo") is True:
            return True
        # 递归检查嵌套值（列表中的字典）
        return any(_is_demo_data(v) for v in data.values() if isinstance(v, (dict, list)))

    if isinstance(data, list):
        return any(_is_demo_data(item) for item in data if isinstance(item, (dict, list)))

    return False


def validate_not_demo_data(data: Any, *, raise_on_demo: bool = True) -> bool:
    """
    验证数据不是演示数据

    在演示模式下，若数据携带 _demo 标记，
    根据 raise_on_demo 决定抛出警告或错误。

    Args:
        data: 待验证的数据（API 响应体、字典或列表）
        raise_on_demo: True 抛出 DemoDataError（严格模式），
                       False 仅发出 DemoDataWarning（宽松模式）

    Returns:
        bool: 验证通过返回 True（数据为真实数据）

    Raises:
        DemoDataError: 严格模式下，数据为演示数据时抛出
        DemoDataWarning: 宽松模式下，数据为演示数据时触发

    Example:
        >>> resp = mock_gen.query_inventory(sku="SKU001")
        >>> validate_not_demo_data(resp.data)
        DemoDataError: 当前为演示模式，数据不可用于真实决策
    """
    if not is_demo_mode():
        # 生产模式不需要验证，直接放行
        return True

    if _is_demo_data(data):
        warning_msg = (
            f"{get_mode_label()} 当前为演示模式，数据不可用于真实决策。"
            f"请切换至生产模式（配置真实ERP）后再执行。"
        )
        if raise_on_demo:
            raise DemoDataError(warning_msg)
        else:
            import warnings
            warnings.warn(DemoDataWarning(warning_msg))
            return False

    return True


def safe_extract(data: Any, key: str, default: Any = None) -> Any:
    """
    安全提取数据字段，自动检测演示数据陷阱

    在演示模式下，如果提取的值的原始对象是演示数据，
    在返回值中附加演示警告信息。

    Args:
        data: 数据源字典
        key: 要提取的字段名
        default: 不存在时返回的默认值

    Returns:
        提取的字段值，若数据为演示数据则附加警告信息
    """
    import warnings

    value = data.get(key, default) if isinstance(data, dict) else default

    if is_demo_mode() and _is_demo_data(data):
        warnings.warn(
            DemoDataWarning(
                f"{get_mode_label()} 您正在访问演示数据中的字段 '{key}'，"
                f"该数据不可用于真实决策。"
            )
        )

    return value


# =============================================================================
# 集成装饰器（保护关键函数）
# =============================================================================

from functools import wraps

def require_real_data(func):
    """
    装饰器：要求被装饰函数必须使用真实数据

    使用示例：
        @require_real_data
        def commit_order(order_data):
            '''提交真实订单（不允许演示数据）'''
            ...
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 如果传入了 data 参数，先验证
        data = kwargs.get("data") or (args[0] if args else None)
        if data is not None:
            validate_not_demo_data(data)
        return func(*args, **kwargs)
    return wrapper
