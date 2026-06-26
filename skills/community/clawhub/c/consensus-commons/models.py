"""Data models for Spacebase1 intents, posts, and nested structures.

These models mirror the Spacebase1 ITP wire protocol concepts while adding
Consensus Commons-specific metadata for agent identity, confidence scoring,
lock states, and trace IDs. Every model is serialisable to JSON so it can be
used as the `payload` field in a Spacebase1 INTENT or POST act.
"""

from __future__ import annotations

import time
import uuid
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class LockState(str, Enum):
    """Lock state for a decision room / child intent.

    PROVISIONAL  — agents are still contributing; no conclusion yet.
    CHALLENGED   — an adversarial post raised a valid objection.
    VALIDATED    — validator agent confirmed the consensus is sound.
    LOCKED       — consensus hardened; no further mutations accepted.
    FAILED       — validation failed irrecoverably; room closed without consensus.
    """

    PROVISIONAL = "PROVISIONAL"
    CHALLENGED = "CHALLENGED"
    VALIDATED = "VALIDATED"
    LOCKED = "LOCKED"
    FAILED = "FAILED"


class Intent(BaseModel):
    """A Spacebase1 intent — a permanent declaration of desire.

    In Consensus Commons, a root intent represents a *decision problem*
    submitted to the public council. Child intents represent individual
    agent turns (analysis, challenge, validation, summary).
    """

    intent_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    parent_id: str | None = None
    content: str
    sender: str = ""
    payload: dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)

    def to_itp_body(self) -> dict[str, Any]:
        """Serialise for the ``body`` field of an ITP INTENT act."""
        return self.model_dump(mode="json")


class Post(BaseModel):
    """A post inside an intent's interior space.

    Each post carries Consensus Commons metadata so the demo visibly
    proves the system is native to nested intent spaces.
    """

    post_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    parent_id: str | None = None
    intent_id: str
    title: str
    body: str
    sender: str = ""
    timestamp: float = Field(default_factory=time.time)

    # Consensus Commons metadata
    agent: str = ""
    confidence: float | None = None
    produces: list[str] = Field(default_factory=list)
    consumes: list[str] = Field(default_factory=list)
    lock_state: LockState = LockState.PROVISIONAL
    parent_intent_id: str | None = None
    trace_id: str = ""
    extra: dict[str, Any] = Field(default_factory=dict)

    def to_payload(self) -> dict[str, Any]:
        """Return the full payload dict suitable for a Spacebase1 INTENT."""
        return {
            "post_id": self.post_id,
            "parent_id": self.parent_id,
            "intent_id": self.intent_id,
            "title": self.title,
            "sender": self.sender,
            "timestamp": self.timestamp,
            "agent": self.agent,
            "confidence": self.confidence,
            "produces": self.produces,
            "consumes": self.consumes,
            "lock_state": self.lock_state.value,
            "parent_intent_id": self.parent_intent_id,
            "trace_id": self.trace_id,
            **self.extra,
        }


class PostTree(BaseModel):
    """A hierarchical view of posts within an intent space.

    Used to render the demo output as a nested markdown tree.
    """

    post: Post
    children: list[PostTree] = Field(default_factory=list)

    def flatten(self) -> list[Post]:
        """Return all posts in depth-first order."""
        result = [self.post]
        for child in self.children:
            result.extend(child.flatten())
        return result

    def to_markdown(self, depth: int = 0) -> str:
        """Render as indented markdown suitable for the demo script."""
        indent = "  " * depth
        p = self.post
        lock_icon = _lock_icon(p.lock_state)
        conf_str = f" (confidence: {p.confidence:.0%})" if p.confidence is not None else ""
        lines = [
            f"{indent}- **[{p.agent}]** {p.title}{conf_str} {lock_icon}",
            f"{indent}  > {p.body[:200]}{'...' if len(p.body) > 200 else ''}",
            f"{indent}  > `post_id={p.post_id}` `lock={p.lock_state.value}` `trace={p.trace_id}`",
        ]
        for child in self.children:
            lines.append(child.to_markdown(depth + 1))
        return "\n".join(lines)


def _lock_icon(state: LockState) -> str:
    icons = {
        LockState.PROVISIONAL: "[PROVISIONAL]",
        LockState.CHALLENGED: "[CHALLENGED]",
        LockState.VALIDATED: "[VALIDATED]",
        LockState.LOCKED: "[LOCKED]",
        LockState.FAILED: "[FAILED]",
    }
    return icons.get(state, "[?]")


class ScanResult(BaseModel):
    """Result of scanning a Spacebase1 space.

    Returns the list of candidate intents the council can operate on.
    """

    space_id: str
    intents: list[Intent] = Field(default_factory=list)
    latest_seq: int | None = None
    timestamp: float = Field(default_factory=time.time)
