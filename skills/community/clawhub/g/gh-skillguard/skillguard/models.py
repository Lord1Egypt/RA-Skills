"""
Pydantic models for SkillGuard unified audit API.
"""

from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class AuditSkillRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    skill_content: str = Field(
        ..., min_length=1, max_length=500_000,
        description="Raw SKILL.md content to audit.",
    )


class ScanReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    safety_score: Decimal
    findings: list[str]
    verdict: str


class ScopeReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    declared_env: list[str]
    declared_bins: list[str]
    undeclared_access: list[str]


class InjectionReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    risk_score: Decimal
    patterns_detected: list[str]


class AuditSkillResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    skill_name: str
    verdict: Literal["SAFE", "CAUTION", "DANGEROUS"]
    total_findings: int = Field(..., ge=0)
    scan: ScanReport
    scope: ScopeReport
    injection: InjectionReport
