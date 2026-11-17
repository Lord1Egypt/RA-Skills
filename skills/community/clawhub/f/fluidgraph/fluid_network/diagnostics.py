# -*- coding: utf-8 -*-
"""结构化诊断。

为什么需要它
------------
原来的错误只是一条字符串：``"[[nodes]]: 负载节点 'L1' 的 min_pressure 必须为正数"``。
人能看懂，但 **Agent 没法用** —— 它无法回答"错在哪个元素的哪个字段"、
"该怎么改"。

:class:`Diagnostic` 把这些拆成结构化字段，让上层（Skill / Agent）可以：

* 精确定位到 ``[[nodes]][0].min_pressure`` 这样的坐标；
* 按 ``code`` 分类处理，而不是去正则匹配中文；
* 把 ``suggestion`` 直接反馈给用户或用来改配置。

同时它也是"一次性返回全部问题"的载体 —— 见 :class:`DiagnosticCollector`。
"""

from __future__ import annotations

from dataclasses import dataclass, field as _dc_field
from typing import Iterable

__all__ = [
    "Diagnostic",
    "DiagnosticCollector",
    "SEVERITY_ERROR",
    "SEVERITY_WARNING",
]

SEVERITY_ERROR = "error"
SEVERITY_WARNING = "warning"


@dataclass(frozen=True)
class Diagnostic:
    """一条结构化的配置/求解诊断。

    字段
    ----
    code
        机器可读的错误类型，如 ``"invalid_node_type"``。Agent 按它分类处理，
        不要去正则匹配 ``message``。
    location
        TOML 坐标，如 ``"[[nodes]][0]"``；能定位到字段时是
        ``"[[nodes]][0].min_pressure"``。
    message
        给人看的说明。
    field
        出问题的具体字段名（可能为空，例如整段缺失）。
    suggestion
        可操作的修复建议。**能给出的一定给出** —— 这是 Agent 自我修复的关键。
    severity
        ``"error"`` 或 ``"warning"``。
    context
        额外上下文（当前值、可用取值等），供高级调用方使用。
    """

    code: str
    message: str
    location: str = ""
    field: str = ""
    suggestion: str = ""
    severity: str = SEVERITY_ERROR
    context: dict = _dc_field(default_factory=dict)

    def to_dict(self) -> dict:
        payload = {
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
        }
        if self.location:
            payload["location"] = self.location
        if self.field:
            payload["field"] = self.field
        if self.suggestion:
            payload["suggestion"] = self.suggestion
        if self.context:
            payload["context"] = self.context
        return payload

    def __str__(self) -> str:
        """人类可读单行形式，兼容旧的 ``str(exc)`` 用法。"""
        where = self.location or ""
        head = f"{where}: " if where else ""
        tail = f"（建议：{self.suggestion}）" if self.suggestion else ""
        return f"{head}{self.message}{tail}"


class DiagnosticCollector:
    """收集诊断信息，支持**一次性返回全部问题**。

    为什么不是"遇到第一个错就抛"：配置错了就该一次看全，而不是改一个跑一次。
    这对 Agent 尤其重要 —— 它需要在一轮里拿到所有待修复项。
    """

    __slots__ = ("_items",)

    def __init__(self, items: Iterable[Diagnostic] = ()) -> None:
        self._items: list[Diagnostic] = list(items)

    def add(self, diagnostic: Diagnostic) -> None:
        self._items.append(diagnostic)

    def error(
        self,
        code: str,
        message: str,
        *,
        location: str = "",
        field: str = "",
        suggestion: str = "",
        **context,
    ) -> None:
        self._items.append(
            Diagnostic(
                code=code,
                message=message,
                location=location,
                field=field,
                suggestion=suggestion,
                severity=SEVERITY_ERROR,
                context=context,
            )
        )

    def warning(
        self,
        code: str,
        message: str,
        *,
        location: str = "",
        field: str = "",
        suggestion: str = "",
        **context,
    ) -> None:
        self._items.append(
            Diagnostic(
                code=code,
                message=message,
                location=location,
                field=field,
                suggestion=suggestion,
                severity=SEVERITY_WARNING,
                context=context,
            )
        )

    def extend(self, diagnostics: Iterable[Diagnostic]) -> None:
        self._items.extend(diagnostics)

    # -- 查询 ------------------------------------------------------------ #
    @property
    def items(self) -> tuple[Diagnostic, ...]:
        return tuple(self._items)

    @property
    def errors(self) -> tuple[Diagnostic, ...]:
        return tuple(d for d in self._items if d.severity == SEVERITY_ERROR)

    @property
    def warnings(self) -> tuple[Diagnostic, ...]:
        return tuple(d for d in self._items if d.severity == SEVERITY_WARNING)

    @property
    def has_errors(self) -> bool:
        return any(d.severity == SEVERITY_ERROR for d in self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    # -- 输出 ------------------------------------------------------------ #
    def to_dicts(self) -> list[dict]:
        return [d.to_dict() for d in self._items]

    def messages(self) -> list[str]:
        """扁平化成字符串列表（兼容旧的 ``ValidationError.errors``）。"""
        return [str(d) for d in self._items]

    def summary(self) -> str:
        """一句话概括，例如 ``"发现 3 处问题"``。"""
        errors, warnings = len(self.errors), len(self.warnings)
        parts = []
        if errors:
            parts.append(f"{errors} 处错误")
        if warnings:
            parts.append(f"{warnings} 处警告")
        return "发现 " + "、".join(parts) if parts else "没有问题"
