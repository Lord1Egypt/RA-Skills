# -*- coding: utf-8 -*-
"""统一的 Skill 返回契约。

为什么要有这一层
----------------
Skill 的调用方是 Agent，不是人。它需要**稳定的机器可读结构**，
而不是 Python traceback：

* 成功 / 失败用 ``ok`` 一个布尔说清，不必去猜异常类型；
* 失败时 ``errors`` 是结构化诊断（code / location / suggestion），
  Agent 拿到就能决定"是重试、改参数，还是告诉用户"；
* ``warnings`` 与 ``errors`` 分开 —— 有警告不代表失败；
* ``data`` 始终存在（失败时为 ``None``），调用方不必做存在性判断。

**绝不把 traceback 透给 Agent。** 未预期的异常会被兜住并转成
``ok=false``，同时在 ``errors`` 里保留异常类型与消息，便于人排查。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from ..diagnostics import Diagnostic

__all__ = ["SkillResult"]


@dataclass(frozen=True)
class SkillResult:
    """所有 Skill 的统一返回结构。

    不论哪个工具、成功还是失败，形状都一样::

        {
          "ok": true,
          "tool": "analyze_scenario",
          "data": { ... },
          "errors": [],
          "warnings": []
        }
    """

    ok: bool
    tool: str
    data: Any = None
    errors: tuple[Diagnostic, ...] = ()
    warnings: tuple[Diagnostic, ...] = ()

    # ------------------------------------------------------------------ #
    # 构造
    # ------------------------------------------------------------------ #
    @classmethod
    def success(
        cls,
        tool: str,
        data: Any = None,
        warnings: Iterable[Diagnostic] = (),
    ) -> "SkillResult":
        return cls(ok=True, tool=tool, data=data, warnings=tuple(warnings))

    @classmethod
    def failure(
        cls,
        tool: str,
        errors: Iterable[Diagnostic],
        *,
        data: Any = None,
        warnings: Iterable[Diagnostic] = (),
    ) -> "SkillResult":
        errors = tuple(errors)
        if not errors:
            # 调用方必须给出原因 —— 一个"失败但没说为什么"的结果对 Agent 毫无用处
            errors = (
                Diagnostic(code="unknown_error", message="工具执行失败，但未提供具体原因"),
            )
        return cls(ok=False, tool=tool, data=data, errors=errors, warnings=tuple(warnings))

    @classmethod
    def from_exception(cls, tool: str, exc: Exception) -> "SkillResult":
        """把任意异常转成失败结果 —— 这是 traceback 的终点。

        优先取结构化诊断；取不到就退化成一条 ``internal_error``，
        并保留异常类型，方便人排查（但对 Agent 仍然只是普通错误）。
        """
        diagnostics = getattr(exc, "diagnostics", None)
        if diagnostics:
            return cls.failure(tool, diagnostics)

        diagnostic = getattr(exc, "diagnostic", None)
        if diagnostic is not None:
            return cls.failure(tool, [diagnostic])

        from ..exceptions import FluidNetworkError

        # 已知的领域错误：消息本身就是给用户看的，直接转述
        code = "domain_error" if isinstance(exc, FluidNetworkError) else "internal_error"
        return cls.failure(
            tool,
            [
                Diagnostic(
                    code=code,
                    message=str(exc) or exc.__class__.__name__,
                    context={"exception_type": exc.__class__.__name__},
                )
            ],
        )

    # ------------------------------------------------------------------ #
    # 便捷判断
    # ------------------------------------------------------------------ #
    @property
    def failed(self) -> bool:
        return not self.ok

    def error_codes(self) -> list[str]:
        return [d.code for d in self.errors]

    def error_messages(self) -> list[str]:
        return [d.message for d in self.errors]

    def warnings_as_dicts(self) -> list[dict]:
        return [d.to_dict() for d in self.warnings]

    # ------------------------------------------------------------------ #
    # 序列化
    # ------------------------------------------------------------------ #
    def to_dict(self) -> dict:
        """转成纯基本类型 —— 可直接 ``json.dumps`` 或作为 tool 返回值。"""
        return {
            "ok": self.ok,
            "tool": self.tool,
            "data": self.data,
            "errors": [d.to_dict() for d in self.errors],
            "warnings": [d.to_dict() for d in self.warnings],
        }

    def to_json(self, *, indent: int | None = 2, ensure_ascii: bool = False) -> str:
        import json

        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=ensure_ascii)
