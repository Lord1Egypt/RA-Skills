"""统一 Skill 返回结构"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class ErrorCode(str, Enum):
    MISSING_PARAM = "MISSING_PARAM"
    INVALID_PARAM = "INVALID_PARAM"
    CRAWL_FAILED = "CRAWL_FAILED"
    NO_BASELINE = "NO_BASELINE"
    NOTIFY_FAILED = "NOTIFY_FAILED"
    UNKNOWN = "UNKNOWN"


@dataclass
class SkillResponse:
    """所有 skill 的统一返回结构。

    machine: 供 OpenClaw 程序读取的结构化数据
    human:   供人类阅读的 Markdown/文本摘要
    error:   出错时填充，正常时为 None
    """

    machine: Dict[str, Any] = field(default_factory=dict)
    human: Dict[str, Any] = field(default_factory=dict)
    error: Optional[Dict[str, Any]] = None

    @classmethod
    def ok(cls, machine: Dict[str, Any], human: Dict[str, Any]) -> "SkillResponse":
        return cls(machine=machine, human=human, error=None)

    @classmethod
    def fail(cls, code: ErrorCode, message: str, detail: Any = None) -> "SkillResponse":
        return cls(
            machine={},
            human={"error_text": message},
            error={"code": code.value, "message": message, "detail": detail},
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {"machine": self.machine, "human": self.human}
        if self.error is not None:
            result["error"] = self.error
        return result

    @property
    def success(self) -> bool:
        return self.error is None
