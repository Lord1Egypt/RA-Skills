# -*- coding: utf-8 -*-
"""流体网络求解器的异常层级。

所有对外异常都继承自 :class:`FluidNetworkError`，调用方可以只捕获这一层，
也可以用更具体的子类做精细处理。

错误信息统一采用 ``<类别>: <对象> - <说明>`` 的格式，方便直接展示给用户。

:class:`ValidationError` 额外携带**结构化诊断**（:class:`~fluid_network.diagnostics.Diagnostic`），
供 Skill / Agent 精确定位与自我修复 —— 只给一句中文，Agent 没法知道该改哪个字段。
"""

from __future__ import annotations

from typing import Iterable

from .diagnostics import Diagnostic, DiagnosticCollector


class FluidNetworkError(Exception):
    """所有流体网络错误的基类。

    ``diagnostic`` 是可选的结构化诊断。任何异常都可以带一条 ——
    这样 Skill 层不必区分"哪类错误带结构、哪类不带"，统一读它就好。
    """

    def __init__(self, message: str = "", diagnostic: Diagnostic | None = None) -> None:
        self.diagnostic = diagnostic
        super().__init__(message)


# --------------------------------------------------------------------------- #
# 配置 / 解析阶段
# --------------------------------------------------------------------------- #
class ConfigError(FluidNetworkError):
    """TOML 配置在语法或结构层面无法使用。"""


class ParseError(ConfigError):
    """配置能读出来，但不符合 Schema 约定（如缺少必需字段）。"""


class ValidationError(ConfigError):
    """配置结构正确，但取值不合法（id 重复、引用不存在、数值越界等）。

    可以带一组结构化诊断。``errors`` 保留为字符串列表以兼容既有调用方，
    ``diagnostics`` 才是给 Skill / Agent 用的结构。
    """

    def __init__(
        self,
        message: str,
        errors: Iterable[str] | None = None,
        diagnostics: Iterable[Diagnostic] | None = None,
    ) -> None:
        self.diagnostics: tuple[Diagnostic, ...] = tuple(diagnostics or ())

        if errors is not None:
            self.errors = list(errors)
        else:
            self.errors = [str(d) for d in self.diagnostics]

        if self.errors:
            detail = "\n".join(f"  [{i}] {e}" for i, e in enumerate(self.errors, 1))
            message = f"{message}\n{detail}"
        super().__init__(message)

    @classmethod
    def from_collector(cls, message: str, collector: DiagnosticCollector) -> "ValidationError":
        """从诊断收集器构造 —— 一次带上全部问题。"""
        return cls(message, errors=collector.messages(), diagnostics=collector.items)


# --------------------------------------------------------------------------- #
# 求解阶段
# --------------------------------------------------------------------------- #
class SolverError(FluidNetworkError):
    """求解过程中的通用错误。"""


class TopologyError(SolverError):
    """网络拓扑无法按一阶段模型求解（环路、无泵、方向矛盾等）。"""


class NotFoundError(FluidNetworkError):
    """按 id 查找对象失败。"""


__all__ = [
    "FluidNetworkError",
    "ConfigError",
    "ParseError",
    "ValidationError",
    "SolverError",
    "TopologyError",
    "NotFoundError",
]