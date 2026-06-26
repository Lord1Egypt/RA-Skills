from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass
class UsageInfo:
    """
    Gateway sessions.usage 返回的 token 与费用信息（与 payload.totals / session.usage 结构一致）。
    """

    input: int = 0
    output: int = 0
    cacheRead: int = 0
    cacheWrite: int = 0
    totalTokens: int = 0
    totalCost: float = 0.0
    inputCost: float = 0.0
    outputCost: float = 0.0
    cacheReadCost: float = 0.0
    cacheWriteCost: float = 0.0
    missingCostEntries: int = 0

    @classmethod
    def from_totals(cls, raw: dict[str, Any] | None) -> UsageInfo:
        """从 payload.totals 或 session.usage 字典构建。"""
        if not raw or not isinstance(raw, dict):
            return cls()

        def _int(key: str) -> int:
            v = raw.get(key)
            if v is None:
                return 0
            try:
                return int(float(v))
            except (TypeError, ValueError):
                return 0

        def _float(key: str) -> float:
            v = raw.get(key)
            if v is None:
                return 0.0
            try:
                return float(v)
            except (TypeError, ValueError):
                return 0.0

        return cls(
            input=_int("input"),
            output=_int("output"),
            cacheRead=_int("cacheRead"),
            cacheWrite=_int("cacheWrite"),
            totalTokens=_int("totalTokens"),
            totalCost=_float("totalCost"),
            inputCost=_float("inputCost"),
            outputCost=_float("outputCost"),
            cacheReadCost=_float("cacheReadCost"),
            cacheWriteCost=_float("cacheWriteCost"),
            missingCostEntries=_int("missingCostEntries"),
        )

    def __sub__(self, other: UsageInfo) -> UsageInfo:
        """返回 self - other，用于计算任务前后用量差。"""
        if not isinstance(other, UsageInfo):
            return self
        return UsageInfo(
            input=self.input - other.input,
            output=self.output - other.output,
            cacheRead=self.cacheRead - other.cacheRead,
            cacheWrite=self.cacheWrite - other.cacheWrite,
            totalTokens=self.totalTokens - other.totalTokens,
            totalCost=round(self.totalCost - other.totalCost, 8),
            inputCost=round(self.inputCost - other.inputCost, 8),
            outputCost=round(self.outputCost - other.outputCost, 8),
            cacheReadCost=round(self.cacheReadCost - other.cacheReadCost, 8),
            cacheWriteCost=round(self.cacheWriteCost - other.cacheWriteCost, 8),
            missingCostEntries=self.missingCostEntries - other.missingCostEntries,
        )

    def to_dict(self) -> dict[str, Any]:
        """转为字典，字段名与 Gateway usage 一致。"""
        return {
            "input": self.input,
            "output": self.output,
            "cacheRead": self.cacheRead,
            "cacheWrite": self.cacheWrite,
            "totalTokens": self.totalTokens,
            "totalCost": self.totalCost,
            "inputCost": self.inputCost,
            "outputCost": self.outputCost,
            "cacheReadCost": self.cacheReadCost,
            "cacheWriteCost": self.cacheWriteCost,
            "missingCostEntries": self.missingCostEntries,
        }
