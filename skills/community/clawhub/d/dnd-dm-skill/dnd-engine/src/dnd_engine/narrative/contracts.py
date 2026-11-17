"""一轮叙事的契约：**一次调用**同时产出叙事文本与类型化 delta。

设计要点（P1-B）：
1. 只有 `narration` 允许自由文本；其余字段全部是枚举/数值——可校验、可门控。
2. `advance_to` 必须落在**可达节点**里，否则整条 delta 被丢弃（fail closed）——
   剧情推进的最终裁判是代码，不是模型。
3. 一致性自检（`conflicts_with_canon` + 理由）由同一次调用给出，不额外花一次请求。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

TONES = ["平静", "紧张", "危急", "悲怆", "欢快", "诡异"]


@dataclass(slots=True)
class TurnDelta:
    advance_to: str = ""
    events: list[str] = field(default_factory=list)
    npc_attitude: str = ""
    tone: str = ""
    conflicts_with_canon: float = 0.0
    conflict_reason: str = ""
    player_hooks: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "advance_to": self.advance_to,
            "events": list(self.events),
            "npc_attitude": self.npc_attitude,
            "tone": self.tone,
            "conflicts_with_canon": self.conflicts_with_canon,
            "conflict_reason": self.conflict_reason,
            "player_hooks": list(self.player_hooks),
        }


@dataclass(slots=True)
class TurnResult:
    narration: str = ""
    delta: TurnDelta = field(default_factory=TurnDelta)
    rejected_advance: str = ""
    notes: list[str] = field(default_factory=list)


class TurnContractError(ValueError):
    """模型输出不符合契约（用于触发一次修复或回退）。"""


def turn_json_schema(reachable_nodes: list[str]) -> dict[str, Any]:
    """给强制结构化输出用的 JSON Schema。"""
    return {
        "type": "object",
        "properties": {
            "narration": {"type": "string"},
            "advance_to": {"type": "string", "enum": (reachable_nodes or [""])},
            "events": {"type": "array", "items": {"type": "string"}},
            "npc_attitude": {"type": "string"},
            "tone": {"type": "string", "enum": TONES},
            "conflicts_with_canon": {"type": "number", "minimum": 0, "maximum": 1},
            "conflict_reason": {"type": "string"},
            "player_hooks": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["narration", "advance_to", "tone", "conflicts_with_canon"],
        "additionalProperties": False,
    }


def validate_turn(raw: Any, reachable_nodes: list[str],
                  min_narration: int = 20) -> TurnResult:
    """严格校验一次叙事返回；不合规就抛 TurnContractError。"""
    if not isinstance(raw, dict):
        raise TurnContractError("turn result must be an object")

    narration = str(raw.get("narration") or "").strip()
    if len(narration) < min_narration:
        raise TurnContractError(f"narration too short: {len(narration)}")

    advance_to = str(raw.get("advance_to") or "").strip()
    if advance_to and advance_to not in (reachable_nodes or []):
        # 允许“不推进”（空串），但不允许跳到不可达节点
        advance_to = ""

    tone = str(raw.get("tone") or "").strip()
    if tone and tone not in TONES:
        tone = ""

    try:
        conflict = float(raw.get("conflicts_with_canon") or 0.0)
    except (TypeError, ValueError) as exc:
        raise TurnContractError("conflicts_with_canon must be numeric") from exc
    if not 0.0 <= conflict <= 1.0:
        raise TurnContractError("conflicts_with_canon must be within 0..1")

    return TurnResult(
        narration=narration,
        delta=TurnDelta(
            advance_to=advance_to,
            events=[str(item).strip() for item in (raw.get("events") or []) if str(item).strip()],
            npc_attitude=str(raw.get("npc_attitude") or "").strip(),
            tone=tone,
            conflicts_with_canon=conflict,
            conflict_reason=str(raw.get("conflict_reason") or "").strip(),
            player_hooks=[str(item).strip() for item in (raw.get("player_hooks") or [])
                          if str(item).strip()],
        ),
    )
