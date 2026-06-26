"""Cognitive Mesh EnterpriseOrchestrator — stub for Consensus Commons integration.

This module provides the TurnResult and Workflow data classes that the
existing cognitive mesh engine produces. The Consensus Commons adapter
consumes these objects and maps them onto Spacebase1 nested intents.

In the full CME system, the EnterpriseOrchestrator (line 28 in the original
codebase) produces TurnResult objects for each agent turn. The Consensus
Commons adapter wraps this without rewriting the engine.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TurnPhase(str, Enum):
    """Phases of an agent turn within the cognitive mesh."""

    EXPANSION = "expansion"
    COMPRESSION = "compression"
    VALIDATION = "validation"
    SUMMARY = "summary"


class TurnStatus(str, Enum):
    """Status of a completed turn."""

    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class TurnResult:
    """Result of a single agent turn in the orchestrator.

    This is the core data object that flows from the cognitive mesh engine
    into the Consensus Commons adapter. Each TurnResult becomes a child
    intent in the Spacebase1 decision room.

    Attributes:
        agent: The agent role that produced this turn.
        phase: Which phase of the deliberation this turn represents.
        status: Whether the turn succeeded, partially succeeded, or failed.
        title: Short human-readable title for the turn.
        body: Full body text (expansion trace, compression summary, etc.).
        confidence: 0.0–1.0 confidence score.
        produces: Artifacts this turn produces.
        consumes: Artifacts this turn consumes.
        metadata: Additional key-value metadata.
        trace_id: Correlation ID linking this turn to the council run.
        duration: Wall-clock time for the turn.
        timestamp: When the turn completed.
    """

    agent: str = ""
    phase: TurnPhase = TurnPhase.EXPANSION
    status: TurnStatus = TurnStatus.SUCCESS
    title: str = ""
    body: str = ""
    confidence: float = 0.5
    produces: list[str] = field(default_factory=list)
    consumes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    trace_id: str = ""
    duration: float = 0.0
    timestamp: float = field(default_factory=time.time)
    turn_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])


@dataclass
class Workflow:
    """Aggregated workflow produced by the full orchestrator run.

    Represents the final output after all agents have completed their
    turns. In Consensus Commons, this becomes the summary child intent.
    """

    workflow_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    trace_id: str = ""
    turns: list[TurnResult] = field(default_factory=list)
    conclusion: str = ""
    lock_state: str = "PROVISIONAL"
    confidence: float = 0.0
    duration: float = 0.0
    timestamp: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_turn(self, turn: TurnResult) -> None:
        """Add a turn to the workflow and update aggregate metrics."""
        self.turns.append(turn)
        self._update_aggregates()

    def _update_aggregates(self) -> None:
        """Recalculate aggregate confidence and duration."""
        if self.turns:
            self.confidence = sum(t.confidence for t in self.turns) / len(self.turns)
            self.duration = sum(t.duration for t in self.turns)
        # Determine lock state from turn statuses
        statuses = {t.status for t in self.turns}
        if TurnStatus.FAILED in statuses:
            self.lock_state = "FAILED"
        elif all(t.status == TurnStatus.SUCCESS for t in self.turns):
            self.lock_state = "LOCKED"
        elif TurnStatus.PARTIAL in statuses:
            self.lock_state = "PROVISIONAL"
