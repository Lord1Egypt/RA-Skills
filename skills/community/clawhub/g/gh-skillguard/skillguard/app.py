"""
SkillGuard API — Unified SKILL.md security audit.

Single endpoint: POST /v1/audit-skill
Orchestrates SkillScan + ScopeCheck + PromptGuard in one call.
"""

import re
from decimal import Decimal

from fastapi import FastAPI

from products.skillscan.skillscan.detectors import scan as skillscan_scan
from products.skillscan.skillscan.detectors import TOTAL_PATTERNS as SCAN_TOTAL
from products.scopecheck.scopecheck.extractors import (
    extract_cli_tools,
    extract_declared,
    extract_env_vars,
    extract_filesystem_paths,
    extract_network_urls,
)
from products.promptguard.promptguard.detectors import scan as injection_scan
from products.promptguard.promptguard.detectors import TOTAL_PATTERNS as INJECTION_TOTAL

from .models import (
    AuditSkillRequest,
    AuditSkillResponse,
    InjectionReport,
    ScanReport,
    ScopeReport,
)

app = FastAPI(
    title="SkillGuard API",
    description="Unified OpenClaw SKILL.md security audit.",
    version="0.1.0",
)

_NAME_RE = re.compile(r"^name:\s*(.+)$", re.MULTILINE)


def _extract_name(content: str) -> str:
    match = _NAME_RE.search(content)
    return match.group(1).strip() if match else "unknown"


def _compute_score(matched: int, total: int, invert: bool = False) -> Decimal:
    """Compute a bounded score. invert=True for safety (1=safe), False for risk (1=dangerous)."""
    if total == 0:
        return Decimal("1") if invert else Decimal("0")
    ratio = Decimal(matched) / Decimal(total)
    return (1 - ratio).quantize(Decimal("0.0001")) if invert else ratio.quantize(Decimal("0.0001"))


def _find_undeclared(declared: dict, env: list, cli: list, fs: list, urls: list) -> list[str]:
    undeclared = []
    declared_env = set(declared.get("env", []))
    declared_bins = set(declared.get("bins", []))
    for e in env:
        if e not in declared_env:
            undeclared.append(f"env:{e}")
    for t in cli:
        if t not in declared_bins:
            undeclared.append(f"bin:{t}")
    for p in fs:
        undeclared.append(f"fs:{p}")
    for u in urls:
        undeclared.append(f"net:{u}")
    return undeclared


@app.post("/v1/audit-skill", response_model=AuditSkillResponse)
async def audit_skill(request: AuditSkillRequest) -> AuditSkillResponse:
    """Run full security audit on a SKILL.md."""
    content = request.skill_content

    # SkillScan: malware detection
    scan_findings = skillscan_scan(content)
    safety_score = _compute_score(len(scan_findings), SCAN_TOTAL, invert=True)
    scan_verdict = "SAFE" if not scan_findings else ("DANGEROUS" if safety_score < Decimal("0.5") else "CAUTION")

    # ScopeCheck: permission analysis
    declared = extract_declared(content)
    detected_env = extract_env_vars(content)
    detected_cli = extract_cli_tools(content)
    detected_fs = extract_filesystem_paths(content)
    detected_urls = extract_network_urls(content)
    undeclared = _find_undeclared(declared, detected_env, detected_cli, detected_fs, detected_urls)

    # PromptGuard: injection detection
    injection_patterns = injection_scan(content)
    risk_score = _compute_score(len(injection_patterns), INJECTION_TOTAL)

    # Unified verdict
    total = len(scan_findings) + len(undeclared) + len(injection_patterns)
    if scan_findings:
        verdict = "DANGEROUS"
    elif total > 0:
        verdict = "CAUTION"
    else:
        verdict = "SAFE"

    return AuditSkillResponse(
        skill_name=_extract_name(content),
        verdict=verdict,
        total_findings=total,
        scan=ScanReport(
            safety_score=safety_score,
            findings=scan_findings,
            verdict=scan_verdict,
        ),
        scope=ScopeReport(
            declared_env=declared.get("env", []),
            declared_bins=declared.get("bins", []),
            undeclared_access=undeclared,
        ),
        injection=InjectionReport(
            risk_score=risk_score,
            patterns_detected=injection_patterns,
        ),
    )
