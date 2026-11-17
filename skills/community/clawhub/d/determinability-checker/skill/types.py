"""
Determinability Checker — Core Types
Based on: Target Determinability under Partial Causal Observation (Wang, 2026)
"""
from typing import Any, Callable, Dict, List, Tuple, Set, Optional, Union
from dataclasses import dataclass
from enum import Enum


class DeterminabilityResult(Enum):
    DETERMINED = "DETERMINED"
    NOT_DETERMINED = "NOT_DETERMINED"


@dataclass(frozen=True)
class Config:
    """A finite causal event configuration."""
    config_id: str
    data: Any

    def __hash__(self):
        return hash(self.config_id)


@dataclass
class DecisionTable:
    """Observation -> Target mapping when determined."""
    mapping: Dict[Any, Any]
    observation_count: int
    config_count: int


@dataclass
class CounterExample:
    """Certificate of non-determinability."""
    config1: Config
    config2: Config
    observation_value: Any
    target1: Any
    target2: Any


@dataclass
class ConflictEdge:
    """An edge in the conflict graph."""
    config1: Config
    config2: Config
    observation_class: Any


@dataclass
class EvidenceGap:
    """Missing evidence items needed to resolve a conflict."""
    conflict_edge: ConflictEdge
    required_evidence: List[str]


@dataclass
class CheckResult:
    """Complete check result."""
    result: DeterminabilityResult
    decision_table: Optional[DecisionTable] = None
    counterexample: Optional[CounterExample] = None
    conflict_graph: Optional[List[ConflictEdge]] = None
    evidence_gaps: Optional[List[EvidenceGap]] = None
    message: str = ""


OmegaFunc = Callable[[Config], Any]
TargetFunc = Callable[[Config], Any]
EvidenceFunc = Callable[[Config], Any]
