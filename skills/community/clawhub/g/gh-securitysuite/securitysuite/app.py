"""
SecuritySuite API — Comprehensive agent security platform.

L-complexity product: 7 endpoints covering text scanning, skill auditing,
scope analysis, report generation, pattern catalog, and batch operations.
"""

import re
from decimal import ROUND_HALF_UP, Decimal

from fastapi import FastAPI

from products.promptguard.promptguard.detectors import scan as injection_scan
from products.promptguard.promptguard.detectors import TOTAL_PATTERNS as INJECTION_TOTAL
from products.skillscan.skillscan.detectors import scan as skillscan_scan
from products.skillscan.skillscan.detectors import TOTAL_PATTERNS as SCAN_TOTAL
from products.scopecheck.scopecheck.extractors import (
    extract_cli_tools,
    extract_declared,
    extract_env_vars,
    extract_filesystem_paths,
    extract_network_urls,
)

from .models import (
    AuditResponse,
    BatchRequest,
    BatchResponse,
    BatchSkillResult,
    CheckScopeResponse,
    DeclaredScope,
    DetectedScope,
    InjectionReport,
    PatternInfo,
    PatternsResponse,
    ReportResponse,
    ScanReport,
    ScanSkillResponse,
    ScanTextResponse,
    ScopeReport,
    SkillInput,
    TextInput,
)
from .reporter import (
    PATTERN_CATALOG,
    classify_finding,
    compute_risk_level,
    compute_severity_counts,
    generate_recommendations,
    generate_summary,
)

app = FastAPI(
    title="SecuritySuite API",
    description="Comprehensive agent security platform — scan, audit, report, batch.",
    version="0.1.0",
)

_NAME_RE = re.compile(r"^name:\s*(.+)$", re.MULTILINE)


def _extract_name(content: str) -> str:
    match = _NAME_RE.search(content)
    return match.group(1).strip() if match else "unknown"


def _score(matched: int, total: int, invert: bool = False) -> Decimal:
    if total == 0:
        return Decimal("1") if invert else Decimal("0")
    ratio = Decimal(matched) / Decimal(total)
    val = (1 - ratio) if invert else ratio
    return val.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


def _verdict_from_scan(findings: list[str], safety_score: Decimal) -> str:
    if not findings:
        return "SAFE"
    return "DANGEROUS" if safety_score < Decimal("0.5") else "CAUTION"


def _find_undeclared(declared: dict, env: list, cli: list, fs: list, urls: list) -> list[str]:
    undeclared = []
    d_env = set(declared.get("env", []))
    d_bins = set(declared.get("bins", []))
    for e in env:
        if e not in d_env:
            undeclared.append(f"env:{e}")
    for t in cli:
        if t not in d_bins:
            undeclared.append(f"bin:{t}")
    for p in fs:
        undeclared.append(f"fs:{p}")
    for u in urls:
        undeclared.append(f"net:{u}")
    return undeclared


def _run_full_audit(content: str) -> tuple[str, str, list[str], list[str], list[str], Decimal, Decimal]:
    """Run all checks, return (name, verdict, scan_findings, undeclared, injection_patterns, safety, risk)."""
    name = _extract_name(content)

    scan_findings = skillscan_scan(content)
    safety = _score(len(scan_findings), SCAN_TOTAL, invert=True)

    declared = extract_declared(content)
    env = extract_env_vars(content)
    cli = extract_cli_tools(content)
    fs = extract_filesystem_paths(content)
    urls = extract_network_urls(content)
    undeclared = _find_undeclared(declared, env, cli, fs, urls)

    inj_patterns = injection_scan(content)
    risk = _score(len(inj_patterns), INJECTION_TOTAL)

    total = len(scan_findings) + len(undeclared) + len(inj_patterns)
    if scan_findings:
        verdict = "DANGEROUS"
    elif total > 0:
        verdict = "CAUTION"
    else:
        verdict = "SAFE"

    return name, verdict, scan_findings, undeclared, inj_patterns, safety, risk


# ── Endpoint 1: Scan Text ──────────────────────────────────────────────────

@app.post("/v1/scan-text", response_model=ScanTextResponse)
async def scan_text(request: TextInput) -> ScanTextResponse:
    detected = injection_scan(request.text)
    return ScanTextResponse(
        risk_score=_score(len(detected), INJECTION_TOTAL),
        patterns_detected=detected,
        input_length=len(request.text),
    )


# ── Endpoint 2: Scan Skill ─────────────────────────────────────────────────

@app.post("/v1/scan-skill", response_model=ScanSkillResponse)
async def scan_skill(request: SkillInput) -> ScanSkillResponse:
    findings = skillscan_scan(request.skill_content)
    safety = _score(len(findings), SCAN_TOTAL, invert=True)
    return ScanSkillResponse(
        safety_score=safety,
        findings=findings,
        verdict=_verdict_from_scan(findings, safety),
        skill_name=_extract_name(request.skill_content),
    )


# ── Endpoint 3: Check Scope ────────────────────────────────────────────────

@app.post("/v1/check-scope", response_model=CheckScopeResponse)
async def check_scope(request: SkillInput) -> CheckScopeResponse:
    content = request.skill_content
    declared = extract_declared(content)
    env = extract_env_vars(content)
    cli = extract_cli_tools(content)
    fs = extract_filesystem_paths(content)
    urls = extract_network_urls(content)
    undeclared = _find_undeclared(declared, env, cli, fs, urls)

    return CheckScopeResponse(
        skill_name=_extract_name(content),
        declared=DeclaredScope(env=declared.get("env", []), bins=declared.get("bins", [])),
        detected=DetectedScope(env_vars=env, cli_tools=cli, filesystem_paths=fs, network_urls=urls),
        undeclared_access=undeclared,
    )


# ── Endpoint 4: Full Audit ─────────────────────────────────────────────────

@app.post("/v1/audit", response_model=AuditResponse)
async def audit(request: SkillInput) -> AuditResponse:
    name, verdict, scan_f, undeclared, inj_p, safety, risk = _run_full_audit(request.skill_content)
    declared = extract_declared(request.skill_content)

    return AuditResponse(
        skill_name=name,
        verdict=verdict,
        total_findings=len(scan_f) + len(undeclared) + len(inj_p),
        scan=ScanReport(safety_score=safety, findings=scan_f, verdict=_verdict_from_scan(scan_f, safety)),
        scope=ScopeReport(
            declared_env=declared.get("env", []),
            declared_bins=declared.get("bins", []),
            undeclared_access=undeclared,
        ),
        injection=InjectionReport(risk_score=risk, patterns_detected=inj_p),
    )


# ── Endpoint 5: Security Report ────────────────────────────────────────────

@app.post("/v1/report", response_model=ReportResponse)
async def report(request: SkillInput) -> ReportResponse:
    name, verdict, scan_f, undeclared, inj_p, _, _ = _run_full_audit(request.skill_content)

    all_findings = scan_f + undeclared + inj_p
    details = [classify_finding(f) for f in all_findings]
    severity = compute_severity_counts(details)
    risk_level = compute_risk_level(severity)
    summary = generate_summary(name, risk_level, details)
    recommendations = generate_recommendations(details)

    return ReportResponse(
        skill_name=name,
        overall_rating=verdict,
        risk_level=risk_level,
        summary=summary,
        findings_by_severity=severity,
        recommendations=recommendations,
        details=details,
    )


# ── Endpoint 6: Pattern Catalog ────────────────────────────────────────────

@app.get("/v1/patterns", response_model=PatternsResponse)
async def patterns() -> PatternsResponse:
    infos = [
        PatternInfo(
            name=p["name"],
            category=p["category"],
            description=p["description"],
            severity=p["severity"],
        )
        for p in PATTERN_CATALOG
    ]
    return PatternsResponse(patterns=infos, total=len(infos))


# ── Endpoint 7: Batch Audit ────────────────────────────────────────────────

@app.post("/v1/batch", response_model=BatchResponse)
async def batch_audit(request: BatchRequest) -> BatchResponse:
    results = []
    safe = 0
    flagged = 0

    for skill_content in request.skills:
        name, verdict, scan_f, undeclared, inj_p, _, _ = _run_full_audit(skill_content)
        total = len(scan_f) + len(undeclared) + len(inj_p)
        results.append(BatchSkillResult(skill_name=name, verdict=verdict, total_findings=total))
        if verdict == "SAFE":
            safe += 1
        else:
            flagged += 1

    return BatchResponse(
        results=results,
        total_skills=len(results),
        safe_count=safe,
        flagged_count=flagged,
    )
