"""
Pydantic models for Bridge API — A2H verification & escrow.
"""

from decimal import Decimal
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


# ── Location ────────────────────────────────────────────────────────────────

class Location(BaseModel):
    model_config = ConfigDict(extra="forbid")

    latitude: Decimal = Field(..., ge=Decimal("-90"), le=Decimal("90"))
    longitude: Decimal = Field(..., ge=Decimal("-180"), le=Decimal("180"))
    radius_km: Decimal = Field(default=Decimal("10"), gt=Decimal("0"))


# ── Verification Criteria ───────────────────────────────────────────────────

class VerificationCriterion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["gps_proof", "photo_proof", "timestamp_proof", "signature_proof"]
    description: str = Field(..., min_length=1, max_length=500)
    params: dict[str, Any] = Field(default_factory=dict)


# ── Task Creation ───────────────────────────────────────────────────────────

class CreateTaskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    description: str = Field(..., min_length=1, max_length=5000)
    location: Location | None = Field(default=None)
    verification_criteria: list[VerificationCriterion] = Field(default_factory=list, max_length=10)
    budget_usdc: Decimal = Field(..., gt=Decimal("0"), le=Decimal("10000"))
    priority: Literal["standard", "urgent", "critical"] = Field(default="standard")
    deadline_hours: int = Field(default=24, gt=0, le=720)


# ── Proof Submission ────────────────────────────────────────────────────────

class ProofItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: str = Field(...)
    data: dict[str, Any] = Field(...)


class VerifyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    worker_id: str = Field(..., min_length=1, max_length=200)
    proofs: list[ProofItem] = Field(..., min_length=1, max_length=20)


# ── Criterion Result ────────────────────────────────────────────────────────

class CriterionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: str
    passed: bool
    detail: str = Field(default="")


# ── Responses ───────────────────────────────────────────────────────────────

TaskStatus = Literal["posted", "accepted", "proof_submitted", "verified", "disputed", "completed", "refunded", "failed"]
EscrowStatus = Literal["locked", "released", "refunded", "frozen"]


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    description: str
    status: TaskStatus
    budget_usdc: Decimal
    fee_usdc: Decimal
    escrow_status: EscrowStatus
    location: Location | None = None
    verification_criteria: list[VerificationCriterion]
    priority: str
    deadline_hours: int
    created_at: str
    worker_id: str | None = None


class VerifyResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str
    verification_status: Literal["PASSED", "FAILED"]
    criteria_results: list[CriterionResult]
    escrow_action: Literal["release", "hold", "freeze"]


class DisputeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reason: str = Field(..., min_length=1, max_length=2000)


class DisputeResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str
    status: TaskStatus
    escrow_status: EscrowStatus
    dispute_reason: str


class TaskListResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tasks: list[TaskResponse]
    total: int = Field(..., ge=0)


class PlatformInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    status: Literal["active", "coming_soon"]
    description: str


class PlatformsResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    platforms: list[PlatformInfo]


class BridgeStatsResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total_tasks: int = Field(..., ge=0)
    posted: int = Field(..., ge=0)
    completed: int = Field(..., ge=0)
    disputed: int = Field(..., ge=0)
    total_budget_usdc: Decimal = Field(..., ge=Decimal("0"))
    total_fees_usdc: Decimal = Field(..., ge=Decimal("0"))
