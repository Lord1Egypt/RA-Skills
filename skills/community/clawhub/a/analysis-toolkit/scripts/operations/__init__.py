"""
细粒度算子层 — 统一入口

所有算子按分类模块导出，供上层（scenarios/、pipeline/）组合调用。
首次导入时自动注册到算子注册表。
"""
import importlib

# 动态导入所有算子模块并合并 __all__
_OPERATOR_MODULES = {}

for _mod_name in ["operators", "uncertainty", "total_error", "viz"]:
    try:
        _mod = importlib.import_module(f"scripts.operations.{_mod_name}")
        if hasattr(_mod, "__all__"):
            _all_names = getattr(_mod, "__all__")
            _OPERATOR_MODULES[_mod_name] = _all_names
            for _name in _all_names:
                globals()[_name] = getattr(_mod, _name)
    except ImportError:
        pass


def list_all_operators() -> list[dict]:
    """列出所有可用算子（从注册表读取）。"""
    from scripts.operations.registry import get_operator_registry
    return get_operator_registry().list_all()


def list_operators_by_category(category: str) -> list[dict]:
    """按分类列出算子。"""
    from scripts.operations.registry import get_operator_registry
    return get_operator_registry().list_by_category(category)


def find_operators(keyword: str) -> list[dict]:
    """模糊搜索算子。"""
    from scripts.operations.registry import get_operator_registry
    return get_operator_registry().find(keyword)


def check_operator_gaps(required: list[str]) -> dict:
    """
    检查所需的算子清单是否存在缺口。

    Parameters
    ----------
    required : list[str] — 所需算子名列表

    Returns
    -------
    dict — {"available": [...], "missing": [...], "all_available": bool}
    """
    from scripts.operations.registry import get_operator_registry
    return get_operator_registry().find_gaps(required)


# 构造合并后的 __all__
__all__ = []
for _mod_name, _names in _OPERATOR_MODULES.items():
    __all__.extend(_names)
__all__.extend([
    "list_all_operators", "list_operators_by_category",
    "find_operators", "check_operator_gaps",
])

# 触发首次注册表初始化
from scripts.operations.registry import get_operator_registry
get_operator_registry()
