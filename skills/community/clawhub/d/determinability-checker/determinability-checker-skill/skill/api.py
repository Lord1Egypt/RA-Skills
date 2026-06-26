"""
Determinability Checker Skill API
Exposed as FastAPI HTTP service, compatible with MCP Skill calling conventions.
"""
from typing import Any, Dict, List, Optional
from fastapi import FastAPI
from pydantic import BaseModel

from .core import DeterminabilityCore
from .types import Config, DeterminabilityResult


class CheckRequest(BaseModel):
    """Agent request payload."""
    session_id: str
    question: str
    configs: List[Dict[str, Any]]
    omega_field: str
    target_field: str
    evidence_fields: Optional[List[str]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "audit-001",
                "question": "Does the final output have a valid verification event?",
                "configs": [
                    {"config_id": "C1", "tool": "code", "has_verif": True, "verif_hash": "valid", "output": "correct", "target": 1},
                    {"config_id": "C2", "tool": "code", "has_verif": False, "verif_hash": "none", "output": "correct", "target": 0}
                ],
                "omega_field": "output",
                "target_field": "target",
                "evidence_fields": ["tool", "has_verif", "verif_hash"]
            }
        }


class DeterminabilityResponse(BaseModel):
    """Structured response to Agent."""
    session_id: str
    question: str
    determinability: str
    can_proceed: bool
    decision_table: Optional[Dict[str, Any]] = None
    counterexample: Optional[Dict[str, Any]] = None
    missing_evidence: Optional[List[str]] = None
    next_skill_suggestion: Optional[str] = None
    message: str


app = FastAPI(
    title="Determinability-Checker Skill",
    description="Causal Sufficiency Determinability Checker — Meta-Skill Gatekeeper based on JEP Paper",
    version="1.0.2"
)

core = DeterminabilityCore()


@app.post("/check", response_model=DeterminabilityResponse)
async def check(request: CheckRequest):
    configs = [Config(config_id=c["config_id"], data=c) for c in request.configs]
    omega = lambda C: C.data.get(request.omega_field)
    target = lambda C: C.data.get(request.target_field)

    evidences = None
    if request.evidence_fields:
        evidences = [
            (field, lambda C, f=field: C.data.get(f))
            for field in request.evidence_fields
        ]

    result = core.check(configs, omega, target, evidences)

    response = DeterminabilityResponse(
        session_id=request.session_id,
        question=request.question,
        determinability=result.result.value,
        can_proceed=(result.result == DeterminabilityResult.DETERMINED),
        message=result.message
    )

    if result.result == DeterminabilityResult.DETERMINED and result.decision_table:
        response.decision_table = result.decision_table.mapping

    if result.result == DeterminabilityResult.NOT_DETERMINED:
        if result.counterexample:
            response.counterexample = {
                "config1": result.counterexample.config1.config_id,
                "config2": result.counterexample.config2.config_id,
                "observation": result.counterexample.observation_value,
                "target1": result.counterexample.target1,
                "target2": result.counterexample.target2
            }

        if result.conflict_graph and evidences:
            minimal_cover = core.find_minimal_evidence_cover(result.conflict_graph, evidences)
            if minimal_cover:
                response.missing_evidence = minimal_cover
                response.next_skill_suggestion = f"Supplement the following evidence items: {', '.join(minimal_cover)}"
            else:
                response.next_skill_suggestion = "Current evidence family cannot cover all conflicts. Expand evidence sources or relax the target."
        else:
            response.next_skill_suggestion = "Observation function is too coarse. Refine observation granularity."

    return response


@app.get("/health")
async def health():
    return {"status": "ok", "skill": "determinability-checker", "version": "1.0.2"}


@app.get("/")
async def root():
    return {
        "name": "Determinability-Checker Skill",
        "version": "1.0.2",
        "description": "Causal Sufficiency Determinability Checker based on JEP Paper CheckDeterminability Algorithm",
        "endpoints": ["/check", "/health"]
    }
