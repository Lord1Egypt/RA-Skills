"""
COE Consensus Skill — Core Types
Based on: Cognition-Oriented Emergence (COE) Protocol (Wang, 2026)
"""
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class Primitive(Enum):
    JUDGE = "J"
    DELEGATE = "D"
    TERMINATE = "T"
    VERIFY = "V"


class ConsensusPolicy(Enum):
    SIMPLE_MAJORITY = "simple_majority"
    WEIGHTED_TRUST = "weighted_trust"
    BFT = "bft"


class VerificationResult(Enum):
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    PARTIAL = "partial"


@dataclass
class COEEvent:
    """Standard COE event structure."""
    event_id: str
    primitive: Primitive
    issuer: str
    timestamp: datetime
    target: str
    assertion: Optional[Dict[str, Any]] = None
    delegate_to: Optional[str] = None
    terminate_of: Optional[str] = None
    verify_of: Optional[List[str]] = None
    verification_result: Optional[VerificationResult] = None
    confidence: Optional[float] = None
    prev_event_id: Optional[str] = None
    hash: Optional[str] = None
    signature: Optional[str] = None


@dataclass
class AssertionKey:
    """Unique key for an assertion: target + subject + predicate."""
    target: str
    subject: str
    predicate: str

    def __hash__(self):
        return hash((self.target, self.subject, self.predicate))


@dataclass
class SharedWorldState:
    """Consensus output: Shared World State record."""
    sws_id: str
    target: str
    timestamp: datetime
    assertions: List[Dict[str, Any]]
    previous_sws_id: Optional[str] = None
    hash: Optional[str] = None


@dataclass
class ConsensusResult:
    """Result of running consensus engine."""
    sws: Optional[SharedWorldState]
    resolved: bool
    conflicts: List[Dict[str, Any]]
    policy: ConsensusPolicy
    message: str
    events_processed: int
    events_by_issuer: Dict[str, int]


@dataclass
class TrustWeight:
    """Trust weight configuration for a Cognitive Unit."""
    issuer: str
    weight: float
    source: str = "default"
