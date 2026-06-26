"""
SessionInfo — openclaw session 信息的数据类。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SessionInfo:
    key: str
    session_id: str
    updated_at: int                     # epoch ms
    age_ms: int | None
    agent_id: str
    kind: str
    model: str
    model_provider: str
    context_tokens: int | None
    input_tokens: int | None
    output_tokens: int | None
    total_tokens: int | None
    total_tokens_fresh: bool
    system_sent: bool
    aborted_last_run: bool

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "SessionInfo":
        return cls(
            key=d.get("key", ""),
            session_id=d.get("sessionId", ""),
            updated_at=d.get("updatedAt", 0),
            age_ms=d.get("ageMs"),
            agent_id=d.get("agentId", ""),
            kind=d.get("kind", ""),
            model=d.get("model", ""),
            model_provider=d.get("modelProvider", ""),
            context_tokens=d.get("contextTokens"),
            input_tokens=d.get("inputTokens"),
            output_tokens=d.get("outputTokens"),
            total_tokens=d.get("totalTokens"),
            total_tokens_fresh=d.get("totalTokensFresh", False),
            system_sent=d.get("systemSent", False),
            aborted_last_run=d.get("abortedLastRun", False),
        )
