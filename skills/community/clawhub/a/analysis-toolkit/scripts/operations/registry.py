"""
算子注册表 — 所有算子的统一登记、查询和缺口发现机制。

每个算子记录以下元信息：
  - name: 函数名
  - signature: 参数签名（用于自动匹配和代码生成）
  - formula: 人可读的公式描述
  - description: 简短说明
  - module: 所在 Python 模块
  - category: 分类标签（statistics / uncertainty / regression / ...）
  - required_params: 必需参数列表
  - optional_params: 可选参数列表

使用示例：

    from scripts.operations.registry import get_operator_registry

    reg = get_operator_registry()
    reg.register("calc_mean", signature="(values)", formula="μ = Σ(xi)/n",
                 description="算术均值", module="scripts.operations.operators",
                 category="statistics")

    reg.find("mean")           # 模糊搜索
    reg.find_gaps(["calc_mean", "calc_ubias", "calc_te"])   # 缺口发现
"""
import os
import json
from typing import Optional


# 数据目录（R-12 合规）
_SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DATA_DIR = os.path.normpath(os.path.join(
    _SKILL_DIR, "..", ".standardization", "analysis-toolkit", "data"
))
_OPERATORS_FILE = os.path.join(_DATA_DIR, "operators_registry.json")


class OperatorDef:
    """算子定义"""
    REQUIRED_FIELDS = {"name", "signature", "description", "module", "category"}

    def __init__(self, data: dict):
        missing = self.REQUIRED_FIELDS - set(data.keys())
        if missing:
            raise ValueError(f"算子定义缺少必需字段: {missing}")
        self.data = data

    @property
    def name(self) -> str:
        return self.data["name"]

    def get(self, key, default=None):
        return self.data.get(key, default)

    def to_dict(self) -> dict:
        return dict(self.data)


class OperatorRegistry:
    """算子注册表 — 管理所有已注册算子"""

    def __init__(self, filepath: str = _OPERATORS_FILE):
        self._filepath = filepath
        self._operators: dict[str, OperatorDef] = {}
        self._load()
        # 自动加载 scripts/operations/ 下的所有模块
        self._auto_discover()

    # ── 持久化 ──

    def _load(self):
        """从 JSON 加载"""
        if not os.path.exists(self._filepath):
            self._operators = {}
            return
        try:
            with open(self._filepath, "r", encoding="utf-8") as f:
                raw_list = json.load(f)
            self._operators = {}
            for item in raw_list:
                try:
                    op = OperatorDef(item)
                    self._operators[op.name] = op
                except ValueError:
                    import warnings
                    warnings.warn(f"跳过无效算子定义: {item.get('name', 'unknown')}")
        except (json.JSONDecodeError, IOError):
            self._operators = {}

    def _save(self):
        """持久化到 JSON"""
        os.makedirs(os.path.dirname(self._filepath), exist_ok=True)
        raw_list = [op.to_dict() for op in self._operators.values()]
        with open(self._filepath, "w", encoding="utf-8") as f:
            json.dump(raw_list, f, ensure_ascii=False, indent=2)

    # ── 自动发现 ──

    def _auto_discover(self):
        """自动扫描 scripts.operations 模块，列出所有不在此目录但实际存在的模块函数

        策略：读 operators.py、uncertainty.py、total_error.py、viz.py 的 __all__，
        将尚未注册的条目加入注册表。
        同时从函数 docstring 中提取公式描述。
        """
        import importlib
        import inspect as _inspect

        from scripts.operations import _OPERATOR_MODULES
        for mod_name, func_list in _OPERATOR_MODULES.items():
            try:
                mod = importlib.import_module(f"scripts.operations.{mod_name}")
            except ImportError:
                continue
            for func_name in func_list:
                if func_name in self._operators:
                    continue
                # 提取 category
                cat_map = {
                    "operators": "statistics", "uncertainty": "uncertainty",
                    "total_error": "total_error", "viz": "viz",
                }
                category = cat_map.get(mod_name, "general")

                # 从函数签名和 docstring 提取信息
                func = getattr(mod, func_name, None)
                sig_str = ""
                formula_str = ""
                desc_str = func_name

                if func and callable(func):
                    try:
                        sig = _inspect.signature(func)
                        sig_str = str(sig)
                    except (ValueError, TypeError):
                        sig_str = "(...)"

                    doc = getattr(func, "__doc__", "") or ""
                    lines = doc.strip().split("\n")
                    # 首行作为描述
                    if lines:
                        desc_str = lines[0].strip()
                    # 查找公式行（以 = 或 → 开头，或含 "=" 的短行）
                    for line in lines:
                        line = line.strip()
                        if "=" in line and len(line) < 60 and ":" not in line[:3]:
                            formula_str = line
                            break

                self._operators[func_name] = OperatorDef({
                    "name": func_name,
                    "signature": sig_str,
                    "formula": formula_str,
                    "description": desc_str,
                    "module": f"scripts.operations.{mod_name}",
                    "category": category,
                })
        self._save()

    # ── 注册 ──

    def register(self, data: dict) -> dict:
        """注册一个新算子"""
        try:
            op = OperatorDef(data)
        except ValueError as e:
            return {"status": "error", "message": str(e)}

        existing = self._operators.get(op.name)
        self._operators[op.name] = op
        self._save()

        if existing:
            return {"status": "updated", "message": f"算子 '{op.name}' 已更新"}
        return {"status": "ok", "message": f"算子 '{op.name}' 注册成功"}

    def unregister(self, name: str) -> dict:
        """注销算子"""
        if name not in self._operators:
            return {"status": "error", "message": f"算子 '{name}' 不存在"}
        del self._operators[name]
        self._save()
        return {"status": "ok", "message": f"算子 '{name}' 已注销"}

    # ── 查询 ──

    def get(self, name: str) -> Optional[OperatorDef]:
        """按名称精确查询算子"""
        return self._operators.get(name)

    def list_all(self) -> list[dict]:
        """列出所有算子摘要"""
        return [
            {"name": op.name, "signature": op.get("signature"),
             "formula": op.get("formula", ""),
             "category": op.get("category", ""),
             "description": op.get("description", "")}
            for op in sorted(self._operators.values(), key=lambda x: x.name)
        ]

    def list_by_category(self, category: str) -> list[dict]:
        """按分类筛选"""
        return [r for r in self.list_all() if r["category"] == category]

    def find(self, keyword: str) -> list[dict]:
        """模糊搜索算子（匹配 name / description / formula）"""
        kw = keyword.lower()
        results = []
        for op in self._operators.values():
            if (kw in op.name.lower()
                    or kw in op.get("description", "").lower()
                    or kw in op.get("formula", "").lower()):
                results.append({
                    "name": op.name,
                    "signature": op.get("signature"),
                    "formula": op.get("formula", ""),
                    "category": op.get("category", ""),
                    "description": op.get("description", ""),
                })
        return results

    # ── 缺口发现 ──

    def find_gaps(self, required_ops: list[str]) -> dict:
        """
        给定一组需要的算子名列表，返回哪些存在、哪些不存在。

        Parameters
        ----------
        required_ops : list[str]
            所需的算子名列表，如 ["calc_mean", "calc_ubias", "calc_te"]

        Returns
        -------
        dict
            {"available": [已存在的算子信息],
             "missing": [不存在的算子名],
             "all_available": bool}
        """
        available = []
        missing = []
        for name in required_ops:
            op = self._operators.get(name)
            if op:
                available.append({
                    "name": op.name,
                    "module": op.get("module"),
                    "signature": op.get("signature"),
                })
            else:
                missing.append(name)
        return {
            "available": available,
            "missing": missing,
            "all_available": len(missing) == 0,
        }


# ── 单例 ──

_default_registry = None


def get_operator_registry() -> OperatorRegistry:
    global _default_registry
    if _default_registry is None:
        _default_registry = OperatorRegistry()
    return _default_registry


def reset_operator_registry():
    global _default_registry
    _default_registry = None
