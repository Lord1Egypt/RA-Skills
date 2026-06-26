"""
COE Consensus Skill API
FastAPI HTTP service compatible with MCP Skill conventions.
"""
from typing import Any, Dict, List, Optional
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel, Field

from .core import ConsensusEngine
from .types import (
    COEEvent, Primitive, ConsensusPolicy, VerificationResult,
    ConsensusResult, SharedWorldState
)


class EventInput(BaseModel):
    """Input COE event payload."""
    event_id: str
    primitive: str = Field(..., pattern="^[JDTV]$")
    issuer: str
    timestamp: str
    target: str
    assertion: Optional[Dict[str, Any]] = None
    delegate_to: Optional[str] = None
    terminate_of: Optional[str] = None
    verify_of: Optional[List[str]] = None
    verification_result: Optional[str] = None
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    prev_event_id: Optional[str] = None
    hash: Optional[str] = None
    signature: Optional[str] = None


class ConsensusRequest(BaseModel):
    """Request to run consensus engine."""
    session_id: str
    target: Optional[str] = None
    policy: str = "simple_majority"
    events: List[EventInput]
    trust_weights: Optional[Dict[str, float]] = None
    bft_fault_tolerance: Optional[int] = None
    weighted_threshold: Optional[float] = None

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "warehouse-001",
                "target": "warehouse-zone-3",
                "policy": "weighted_trust",
                "events": [
                    {
                        "event_id": "evt-1",
                        "primitive": "J",
                        "issuer": "robot-A",
                        "timestamp": "2026-04-19T10:30:00Z",
                        "target": "warehouse-zone-3",
                        "assertion": {"subject": "door_01", "predicate": "status", "value": "open"},
                        "confidence": 0.95
                    },
                    {
                        "event_id": "evt-2",
                        "primitive": "V",
                        "issuer": "robot-B",
                        "timestamp": "2026-04-19T10:30:05Z",
                        "target": "warehouse-zone-3",
                        "verify_of": ["evt-1"],
                        "verification_result": "confirmed",
                        "confidence": 0.9
                    }
                ],
                "trust_weights": {"robot-A": 0.9, "robot-B": 0.8, "human-1": 1.0}
            }
        }


class SWSOutput(BaseModel):
    """Shared World State output."""
    sws_id: str
    target: str
    timestamp: str
    assertions: List[Dict[str, Any]]
    previous_sws_id: Optional[str] = None
    hash: Optional[str] = None


class ConsensusResponse(BaseModel):
    """Structured consensus response."""
    session_id: str
    resolved: bool
    policy: str
    sws: Optional[SWSOutput] = None
    conflicts: List[Dict[str, Any]]
    message: str
    events_processed: int
    events_by_issuer: Dict[str, int]


app = FastAPI(
    title="COE Consensus Skill",
    description="Cross-Model Consensus Engine for Shared World State Formation",
    version="1.0.0"
)


def _to_coe_event(inp: EventInput) -> COEEvent:
    """Convert API input to internal COEEvent."""
    return COEEvent(
        event_id=inp.event_id,
        primitive=Primitive(inp.primitive),
        issuer=inp.issuer,
        timestamp=datetime.fromisoformat(inp.timestamp.replace("Z", "+00:00")),
        target=inp.target,
        assertion=inp.assertion,
        delegate_to=inp.delegate_to,
        terminate_of=inp.terminate_of,
        verify_of=inp.verify_of,
        verification_result=VerificationResult(inp.verification_result) if inp.verification_result else None,
        confidence=inp.confidence,
        prev_event_id=inp.prev_event_id,
        hash=inp.hash,
        signature=inp.signature
    )


@app.post("/consensus", response_model=ConsensusResponse)
async def consensus(request: ConsensusRequest):
    policy = ConsensusPolicy(request.policy)
    engine = ConsensusEngine(policy=policy)

    if request.trust_weights:
        for issuer, weight in request.trust_weights.items():
            engine.set_trust_weight(issuer, weight)

    if request.bft_fault_tolerance is not None:
        engine.set_bft_params(request.bft_fault_tolerance)

    if request.weighted_threshold is not None:
        engine.set_weighted_threshold(request.weighted_threshold)

    for evt_in in request.events:
        engine.add_event(_to_coe_event(evt_in))

    result = engine.run(target=request.target)

    sws_out = None
    if result.sws:
        sws_out = SWSOutput(
            sws_id=result.sws.sws_id,
            target=result.sws.target,
            timestamp=result.sws.timestamp.isoformat(),
            assertions=result.sws.assertions,
            previous_sws_id=result.sws.previous_sws_id,
            hash=result.sws.hash
        )

    return ConsensusResponse(
        session_id=request.session_id,
        resolved=result.resolved,
        policy=result.policy.value,
        sws=sws_out,
        conflicts=result.conflicts,
        message=result.message,
        events_processed=result.events_processed,
        events_by_issuer=result.events_by_issuer
    )


@app.get("/health")
async def health():
    return {"status": "ok", "skill": "coe-consensus", "version": "1.0.0"}


@app.get("/")
async def root():
    return {
        "name": "COE Consensus Skill",
        "version": "1.0.0",
        "description": "Cross-Model Consensus Engine for Shared World State Formation",
        "endpoints": ["/consensus", "/health"],
        "policies": ["simple_majority", "weighted_trust", "bft"]
    }
