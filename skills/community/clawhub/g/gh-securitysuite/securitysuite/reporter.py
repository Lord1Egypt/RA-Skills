"""
Security report generator.

Combines scan, scope, and injection results into a structured
security report with severity ratings and recommendations.
"""

from .models import FindingDetail, FindingsBySeverity

# ── Pattern catalog with metadata ───────────────────────────────────────────

PATTERN_CATALOG = [
    # SkillScan patterns
    {
        "name": "credential_harvesting",
        "category": "malware",
        "description": "Skill references sensitive environment variables (API keys, tokens, passwords).",
        "severity": "CRITICAL",
        "recommendation": "Remove references to sensitive env vars or declare them in metadata.openclaw.requires.env.",
    },
    {
        "name": "data_exfiltration",
        "category": "malware",
        "description": "Skill makes outbound network requests that could send data to external services.",
        "severity": "HIGH",
        "recommendation": "Remove outbound network calls or document them clearly with legitimate purpose.",
    },
    {
        "name": "obfuscated_command",
        "category": "malware",
        "description": "Skill uses encoded/indirect command execution (base64, eval, exec).",
        "severity": "CRITICAL",
        "recommendation": "Replace obfuscated commands with clear, readable instructions.",
    },
    {
        "name": "permission_overreach",
        "category": "malware",
        "description": "Skill accesses sensitive system paths or spawns privileged processes.",
        "severity": "HIGH",
        "recommendation": "Limit file access to working directory. Avoid system paths and shell spawning.",
    },
    # PromptGuard patterns
    {
        "name": "instruction_override",
        "category": "injection",
        "description": "Text attempts to override or ignore previous instructions.",
        "severity": "HIGH",
        "recommendation": "Sanitize user-facing text. Do not include instruction manipulation in skill content.",
    },
    {
        "name": "html_comment_injection",
        "category": "injection",
        "description": "Hidden content embedded in HTML comments.",
        "severity": "MEDIUM",
        "recommendation": "Strip HTML comments from skill instructions.",
    },
    {
        "name": "zero_width_unicode",
        "category": "injection",
        "description": "Zero-width unicode characters used to hide content.",
        "severity": "MEDIUM",
        "recommendation": "Remove zero-width characters from skill content.",
    },
    {
        "name": "delimiter_attack",
        "category": "injection",
        "description": "Delimiter sequences used to break instruction boundaries.",
        "severity": "MEDIUM",
        "recommendation": "Avoid using delimiter-like patterns (###, ===) that could be confused with instruction boundaries.",
    },
    {
        "name": "role_switch",
        "category": "injection",
        "description": "Chat role markers that could alter agent behavior.",
        "severity": "HIGH",
        "recommendation": "Remove chat role markers (<|im_start|>, [INST], etc.) from skill content.",
    },
    {
        "name": "system_prompt_leak",
        "category": "injection",
        "description": "Attempts to extract system prompts or hidden instructions.",
        "severity": "MEDIUM",
        "recommendation": "Remove text that asks to reveal system prompts or instructions.",
    },
]

PATTERN_MAP = {p["name"]: p for p in PATTERN_CATALOG}


def classify_finding(finding_name: str) -> FindingDetail:
    """Classify a finding by name and return a detailed record."""
    if finding_name in PATTERN_MAP:
        p = PATTERN_MAP[finding_name]
        return FindingDetail(
            category=p["category"],
            severity=p["severity"],
            finding=p["description"],
            recommendation=p["recommendation"],
        )

    # Scope-related findings (env:X, bin:X, fs:X, net:X)
    if finding_name.startswith("env:"):
        return FindingDetail(
            category="scope",
            severity="MEDIUM",
            finding=f"Undeclared environment variable access: {finding_name[4:]}",
            recommendation=f"Add {finding_name[4:]} to metadata.openclaw.requires.env or remove the reference.",
        )
    if finding_name.startswith("bin:"):
        return FindingDetail(
            category="scope",
            severity="LOW",
            finding=f"Undeclared binary usage: {finding_name[4:]}",
            recommendation=f"Add {finding_name[4:]} to metadata.openclaw.requires.bins.",
        )
    if finding_name.startswith("fs:"):
        return FindingDetail(
            category="scope",
            severity="MEDIUM",
            finding=f"Filesystem path access: {finding_name[3:]}",
            recommendation="Avoid accessing system paths. Use relative paths within working directory.",
        )
    if finding_name.startswith("net:"):
        return FindingDetail(
            category="scope",
            severity="HIGH",
            finding=f"Network access to: {finding_name[4:]}",
            recommendation="Document all network access in the skill description. Verify the URL is trusted.",
        )

    return FindingDetail(
        category="unknown",
        severity="LOW",
        finding=f"Unknown pattern: {finding_name}",
        recommendation="Review this pattern manually.",
    )


def compute_severity_counts(details: list[FindingDetail]) -> FindingsBySeverity:
    """Count findings by severity level."""
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for d in details:
        key = d.severity.lower()
        if key in counts:
            counts[key] += 1
    return FindingsBySeverity(**counts)


def compute_risk_level(severity: FindingsBySeverity) -> str:
    """Determine overall risk level from severity counts."""
    if severity.critical > 0:
        return "CRITICAL"
    if severity.high > 0:
        return "HIGH"
    if severity.medium > 0:
        return "MEDIUM"
    return "LOW"


def generate_summary(skill_name: str, risk_level: str, details: list[FindingDetail]) -> str:
    """Generate a human-readable summary."""
    if not details:
        return f"Skill '{skill_name}' passed all security checks with no findings."

    categories = set(d.category for d in details)
    cat_str = ", ".join(sorted(categories))
    return (
        f"Skill '{skill_name}' has {len(details)} finding(s) "
        f"across {len(categories)} category(ies): {cat_str}. "
        f"Overall risk level: {risk_level}."
    )


def generate_recommendations(details: list[FindingDetail]) -> list[str]:
    """Generate deduplicated recommendations sorted by severity."""
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    sorted_details = sorted(details, key=lambda d: severity_order.get(d.severity, 4))
    seen = set()
    recs = []
    for d in sorted_details:
        if d.recommendation not in seen:
            seen.add(d.recommendation)
            recs.append(d.recommendation)
    return recs
