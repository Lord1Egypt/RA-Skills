"""Consensus Hardening Protocol — lock state machine and validation checks.

The CHP ensures that decision rooms in Consensus Commons cannot reach a
LOCKED state without passing through adversarial review and validation.
It mirrors the cognitive mesh engine's consensus validation layer.
"""

from __future__ import annotations

from enum import Enum
from typing import Any


class CHPGate(str, Enum):
    """Individual validation gates in the consensus hardening protocol."""

    MULTIPLE_PERSPECTIVES = "multiple_perspectives"
    ADVERSARIAL_CHALLENGE = "adversarial_challenge"
    CHALLENGE_ADDRESSED = "challenge_addressed"
    EVIDENCE_PROVIDED = "evidence_provided"
    NO_FALLACIES = "no_fallacies"
    TRACE_CONSISTENCY = "trace_consistency"
    METADATA_COMPLETE = "metadata_complete"
    HUMAN_REVIEW = "human_review"  # optional, for high-value decisions


class CHPResult:
    """Result of running the CHP validation checks."""

    def __init__(self) -> None:
        self.gates: dict[CHPGate, bool] = {}
        self.failures: list[str] = []
        self.warnings: list[str] = []

    def pass_gate(self, gate: CHPGate) -> None:
        self.gates[gate] = True

    def fail_gate(self, gate: CHPGate, reason: str) -> None:
        self.gates[gate] = False
        self.failures.append(f"{gate.value}: {reason}")

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    @property
    def is_valid(self) -> bool:
        """All required gates passed (warnings are non-blocking)."""
        required = {g for g in CHPGate if g != CHPGate.HUMAN_REVIEW}
        return all(self.gates.get(g, False) for g in required)

    @property
    def is_locked(self) -> bool:
        """Valid and no warnings (strict mode)."""
        return self.is_valid and len(self.warnings) == 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "is_locked": self.is_locked,
            "gates": {g.value: v for g, v in self.gates.items()},
            "failures": self.failures,
            "warnings": self.warnings,
        }
