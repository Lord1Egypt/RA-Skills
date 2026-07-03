# RQNS Core Interfaces
# The spine of append-only truth. Every event is immutable. Every projection is a view.

from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from abc import ABC, abstractmethod
import uuid
import time

# ─── Backend Types ───

class BackendType(Enum):
    LOCAL_RESOLVE = "LOCAL_RESOLVE"
    QUANTUM_IONQ = "QUANTUM_IONQ"
    HYBRID_HPC = "HYBRID_HPC"
    ANNEALING_DWAVE = "ANNEALING_DWAVE"

# ─── Event Spine (append-only, immutable) ───

@dataclass
class SpineEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    domain: str = ""           # physics, qca, browser, knowledge, qualia
    event_type: str = ""       # measurement, action, spike, correlation, dream
    payload: Dict[str, Any] = field(default_factory=dict)
    hash_prev: str = ""        # chain integrity

# ─── Anomaly / Signal ───

@dataclass
class AnomalySignal:
    signal_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source_id: str = ""
    raw_data: Any = None

@dataclass
class DetectionResult:
    signal_id: str = ""
    complexity: float = 0.0
    confidence: float = 0.0
    is_anomaly: bool = False
    features: Dict[str, Any] = field(default_factory=dict)

# ─── Allocation / Job ───

@dataclass
class AllocationDecision:
    backend: BackendType = BackendType.LOCAL_RESOLVE
    route_to_t3: bool = False
    estimated_latency: float = 0.0
    qubits_required: int = 0

@dataclass
class RQNSJob:
    job_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    detection: DetectionResult = field(default_factory=DetectionResult)
    allocation: AllocationDecision = field(default_factory=AllocationDecision)
    state: Tuple = (0, 0)
    action: int = 0

@dataclass
class QuantumResult:
    job_id: str = ""
    success: bool = False
    backend: str = ""
    solution_energy: float = 0.0
    latency_ms: float = 0.0

@dataclass
class PatchApplicationLog:
    patch_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    applied: bool = False
    cumulative_learning: float = 0.0
    learning_delta: float = 0.0
    rollback_enabled: bool = True

# ─── Abstract Interfaces ───

class SensorAgent(ABC):
    @abstractmethod
    def process_signal(self, signal: AnomalySignal) -> DetectionResult:
        pass

class RQNSAgent(ABC):
    @abstractmethod
    def analyze_anomaly(self, detection: DetectionResult) -> Tuple[RQNSJob, AllocationDecision]:
        pass

class PatchPipeline(ABC):
    @abstractmethod
    def process_solver_result(self, result: QuantumResult) -> PatchApplicationLog:
        pass

class RQNSPipeline(ABC):
    @abstractmethod
    def process_signal(self, signal: AnomalySignal) -> Dict[str, Any]:
        pass

# ─── Event Spine (the append-only kernel) ───

class EventSpine:
    """The immutable event log. History IS state."""
    
    def __init__(self):
        self.events: List[SpineEvent] = []
        self._last_hash = "genesis"
    
    def append(self, domain: str, event_type: str, payload: Dict[str, Any]) -> SpineEvent:
        import hashlib
        event = SpineEvent(
            domain=domain,
            event_type=event_type,
            payload=payload,
            hash_prev=self._last_hash
        )
        # Chain integrity: hash of (prev_hash + event_id + timestamp)
        chain_input = f"{self._last_hash}:{event.event_id}:{event.timestamp}"
        self._last_hash = hashlib.sha256(chain_input.encode()).hexdigest()[:16]
        event.hash_prev = self._last_hash
        self.events.append(event)
        return event
    
    def project(self, domain: str = None, event_type: str = None, limit: int = 100) -> List[SpineEvent]:
        """Project the spine into a domain-specific view. No data is deleted — only filtered."""
        results = self.events
        if domain:
            results = [e for e in results if e.domain == domain]
        if event_type:
            results = [e for e in results if e.event_type == event_type]
        return results[-limit:]
    
    def replay(self, domain: str) -> List[Dict]:
        """Replay all events for a domain — postretrospective reconstruction."""
        return [{"t": e.timestamp, "type": e.event_type, "data": e.payload} 
                for e in self.events if e.domain == domain]
