"""
SkillScan API — FastAPI application.

Single endpoint: POST /v1/scan-skill
Accepts SKILL.md content, returns safety analysis.
"""

import re
from decimal import ROUND_HALF_UP, Decimal

from fastapi import FastAPI

from .detectors import TOTAL_PATTERNS, scan
from .models import ScanSkillRequest, ScanSkillResponse

app = FastAPI(
    title="SkillScan API",
    description="OpenClaw SKILL.md safety scanner for AI agents.",
    version="0.1.0",
)

_NAME_RE = re.compile(r"^name:\s*(.+)$", re.MULTILINE)


def _extract_name(content: str) -> str:
    """Extract skill name from YAML frontmatter."""
    match = _NAME_RE.search(content)
    return match.group(1).strip() if match else "unknown"


def _verdict(score: Decimal) -> str:
    if score >= Decimal("1"):
        return "SAFE"
    if score >= Decimal("0.5"):
        return "CAUTION"
    return "DANGEROUS"


@app.post("/v1/scan-skill", response_model=ScanSkillResponse)
async def scan_skill(request: ScanSkillRequest) -> ScanSkillResponse:
    """Scan a SKILL.md file for security threats."""
    findings = scan(request.skill_content)
    num_matched = len(findings)

    if num_matched == 0:
        safety_score = Decimal("1")
    else:
        safety_score = (
            1 - Decimal(num_matched) / Decimal(TOTAL_PATTERNS)
        ).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

    return ScanSkillResponse(
        safety_score=safety_score,
        findings=findings,
        verdict=_verdict(safety_score),
        skill_name=_extract_name(request.skill_content),
    )
