"""
Pydantic models for SecuritySuite API.
All models use extra="forbid". Decimal for scores.
"""

from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


# ── Shared ──────────────────────────────────────────────────────────────────

class SkillInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    skill_content: str = Field(..., min_length=1, max_length=500_000)


class TextInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(..., min_length=1, max_length=100_000)


# ── Scan Text ───────────────────────────────────────────────────────────────

class ScanTextResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    risk_score: Decimal = Field(..., ge=Decimal("0"), le=Decimal("1"))
    patterns_detected: list[str]
    input_length: int = Field(..., ge=0)


# ── Scan Skill ──────────────────────────────────────────────────────────────

class ScanSkillResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    safety_score: Decimal = Field(..., ge=Decimal("0"), le=Decimal("1"))
    findings: list[str]
    verdict: Literal["SAFE", "CAUTION", "DANGEROUS"]
    skill_name: str


# ── Check Scope ─────────────────────────────────────────────────────────────

class DeclaredScope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    env: list[str] = Field(default_factory=list)
    bins: list[str] = Field(default_factory=list)


class DetectedScope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    env_vars: list[str] = Field(default_factory=list)
    cli_tools: list[str] = Field(default_factory=list)
    filesystem_paths: list[str] = Field(default_factory=list)
    network_urls: list[str] = Field(default_factory=list)


class CheckScopeResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    skill_name: str
    declared: DeclaredScope
    detected: DetectedScope
    undeclared_access: list[str]


# ── Audit ───────────────────────────────────────────────────────────────────

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


class AuditResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    skill_name: str
    verdict: Literal["SAFE", "CAUTION", "DANGEROUS"]
    total_findings: int = Field(..., ge=0)
    scan: ScanReport
    scope: ScopeReport
    injection: InjectionReport


# ── Report ──────────────────────────────────────────────────────────────────

class FindingDetail(BaseModel):
    model_config = ConfigDict(extra="forbid")
    category: str
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    finding: str
    recommendation: str


class FindingsBySeverity(BaseModel):
    model_config = ConfigDict(extra="forbid")
    critical: int = Field(default=0, ge=0)
    high: int = Field(default=0, ge=0)
    medium: int = Field(default=0, ge=0)
    low: int = Field(default=0, ge=0)


class ReportResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    skill_name: str
    overall_rating: Literal["SAFE", "CAUTION", "DANGEROUS"]
    risk_level: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    summary: str
    findings_by_severity: FindingsBySeverity
    recommendations: list[str]
    details: list[FindingDetail]


# ── Patterns ────────────────────────────────────────────────────────────────

class PatternInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    category: str
    description: str
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]


class PatternsResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    patterns: list[PatternInfo]
    total: int = Field(..., ge=0)


# ── Batch ───────────────────────────────────────────────────────────────────

class BatchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    skills: list[str] = Field(..., min_length=1, max_length=100)


class BatchSkillResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    skill_name: str
    verdict: Literal["SAFE", "CAUTION", "DANGEROUS"]
    total_findings: int = Field(..., ge=0)


class BatchResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    results: list[BatchSkillResult]
    total_skills: int = Field(..., ge=0)
    safe_count: int = Field(..., ge=0)
    flagged_count: int = Field(..., ge=0)
