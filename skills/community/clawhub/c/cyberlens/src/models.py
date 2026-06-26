"""Pydantic models for CyberLens skill inputs and outputs."""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, HttpUrl


class Finding(BaseModel):
    """A security finding from a scan."""
    type: str = Field(..., description="Type of finding")
    severity: str = Field(..., description="Severity level: critical, high, medium, low, info")
    description: str = Field(..., description="Human-readable description")
    remediation: str = Field(..., description="How to fix the issue")
    url: Optional[str] = Field(None, description="URL where finding was detected")
    evidence: Optional[str] = Field(None, description="Evidence supporting the finding")
    references: List[str] = Field(default_factory=list, description="Reference URLs")


class ScanResult(BaseModel):
    """Complete result from a security scan."""
    url: str = Field(..., description="Scanned URL")
    score: int = Field(..., ge=0, le=100, description="Security score 0-100")
    grade: str = Field(..., pattern="^[A-F]$", description="Letter grade A-F")
    findings: List[Finding] = Field(default_factory=list, description="List of findings")
    headers: Dict[str, str] = Field(default_factory=dict, description="Response headers")
    technologies: List[str] = Field(default_factory=list, description="Detected technologies")
    scan_time_ms: int = Field(default=0, description="Scan duration in milliseconds")
    error: Optional[str] = Field(None, description="Error message if scan failed")


class SecurityScore(BaseModel):
    """Quick security score result."""
    url: str = Field(..., description="Scanned URL")
    score: int = Field(..., ge=0, le=100, description="Security score 0-100")
    grade: str = Field(..., pattern="^[A-F]$", description="Letter grade A-F")
    assessment: str = Field(..., description="Human-readable assessment")


class FindingExplanation(BaseModel):
    """Explanation of a security finding."""
    finding_type: str = Field(..., description="Type of finding")
    explanation: str = Field(..., description="Plain-English explanation")
    severity: str = Field(..., description="Severity level")
    remediation: str = Field(..., description="How to fix")
    references: List[str] = Field(default_factory=list, description="Reference URLs")
    context: Optional[str] = Field(None, description="Optional context")


class ScanRule(BaseModel):
    """Definition of a scan rule."""
    name: str = Field(..., description="Rule name")
    category: str = Field(..., description="Rule category")
    severity: str = Field(..., description="Default severity")
    description: str = Field(..., description="What the rule checks for")


class ScanWebsiteInput(BaseModel):
    """Input for scan_website tool."""
    url: str = Field(..., description="The website URL to scan (must include https://)")
    scan_depth: str = Field(default="standard", pattern="^(quick|standard|deep)$")
    timeout: float = Field(default=30.0, gt=0, description="Request timeout in seconds")


class ScanWebsiteOutput(BaseModel):
    """Output from scan_website tool."""
    success: bool
    url: str
    score: Optional[int] = None
    grade: Optional[str] = None
    scan_time_ms: Optional[int] = None
    technologies: Optional[List[str]] = None
    findings_count: Optional[int] = None
    findings: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None


class GetSecurityScoreInput(BaseModel):
    """Input for get_security_score tool."""
    url: str = Field(..., description="The website URL to check")
    timeout: float = Field(default=30.0, gt=0)


class GetSecurityScoreOutput(BaseModel):
    """Output from get_security_score tool."""
    success: bool
    url: str
    score: Optional[int] = None
    grade: Optional[str] = None
    assessment: Optional[str] = None
    error: Optional[str] = None


class ExplainFindingInput(BaseModel):
    """Input for explain_finding tool."""
    finding_type: str = Field(..., description="Type of finding to explain")
    context: Optional[str] = Field(None, description="Optional context")


class ExplainFindingOutput(BaseModel):
    """Output from explain_finding tool."""
    success: bool
    finding_type: Optional[str] = None
    explanation: Optional[str] = None
    severity: Optional[str] = None
    remediation: Optional[str] = None
    references: Optional[List[str]] = None
    context: Optional[str] = None
    error: Optional[str] = None
    known_types: Optional[List[str]] = None


class ListScanRulesOutput(BaseModel):
    """Output from list_scan_rules tool."""
    success: bool
    total_rules: int
    categories: Dict[str, Any]
