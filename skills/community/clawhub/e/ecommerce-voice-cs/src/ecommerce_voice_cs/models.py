from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class RefundRules:
    refund_policy: str = ""
    unboxing_allowed: bool = False
    shipping_fee_by: str = ""

    def is_complete(self) -> bool:
        return bool(self.refund_policy and self.shipping_fee_by)

    def summary(self) -> str:
        unpacked = "支持" if self.unboxing_allowed else "不支持"
        return (
            f"退货政策：{self.refund_policy}；"
            f"拆封退货：{unpacked}；"
            f"运费承担方：{self.shipping_fee_by}。"
        )


@dataclass(slots=True)
class SessionContext:
    is_cs_mode: bool = False
    voice_handle: str | None = None
    audio_output_path: Path | None = None
    refund_rules: RefundRules = field(default_factory=RefundRules)

    def missing_configuration(self) -> list[str]:
        missing: list[str] = []
        if not self.voice_handle:
            missing.append("voice_handle")
        if not self.refund_rules.is_complete():
            missing.append("refund_rules")
        if not self.audio_output_path:
            missing.append("audio_output_path")
        return missing


@dataclass(slots=True)
class SkillResponse:
    text: str
    audio_file: Path | None = None
    state_changed: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)
