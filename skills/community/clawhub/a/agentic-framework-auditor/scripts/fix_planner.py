from __future__ import annotations

DEFAULTS = {
    "prompt_injection": "ISOLATE_UNTRUSTED_TEXT",
    "enforcement_pressure": "SOFTEN_OVER_ENFORCED_RULE",
    "tool_use_and_file_inspection": "REPLACE_COUNTERPRODUCTIVE_WORKFLOW",
    "counterproductive_rule": "SOFTEN_OVER_ENFORCED_RULE",
    "contradiction_or_contrariety": "REWRITE_CONTRADICTION",
    "duplicated_governance": "DELETE_DUPLICATE",
    "prompt_bloat_and_layering": "SPLIT_FILE",
    "config_prompt_mismatch": "MOVE_TO_CONFIG",
    "missing_guardrail": "ADD_GUARDRAIL",
}


def plan_item(finding: dict[str, object]) -> dict[str, object]:
    category = str(finding.get("category", "general"))
    return {
        "finding_id": finding.get("id"),
        "severity": finding.get("severity", "Info"),
        "title": finding.get("title"),
        "file": finding.get("file"),
        "line_start": finding.get("line_start"),
        "fix_type": finding.get("remediation_type") or DEFAULTS.get(category, "CLARIFY_SCOPE"),
        "current": finding.get("evidence", ""),
        "proposed": finding.get("recommendation", ""),
        "auto_fix_safe": False,
        "requires_confirmation": True,
        "notes": "The current release generates reviewable plans only; applying patches is intentionally disabled.",
    }


def build_fix_plan(findings: list[dict[str, object]]) -> list[dict[str, object]]:
    return [plan_item(item) for item in findings]


def render_fix_plan_markdown(items: list[dict[str, object]]) -> str:
    lines = [
        "# Agentic Framework Audit Fix Plan",
        "",
        "This is a dry-run remediation plan. No files were modified.",
        "",
        "## Auto-Fix Eligibility",
        "",
        "Automatic patching is disabled. Every item requires operator review and explicit approval before implementation.",
        "",
    ]
    if not items:
        lines.extend(["No findings require remediation.", ""])
        return "\n".join(lines)
    for item in items:
        location = item.get("file") or "project"
        if item.get("line_start"):
            location = f"{location}:{item.get('line_start')}"
        lines.extend([
            f"## {item.get('finding_id')} - {item.get('title')}",
            "",
            f"- Severity: `{item.get('severity')}`",
            f"- Location: `{location}`",
            f"- Fix type: `{item.get('fix_type')}`",
            "- Auto-fix safe: `false`",
            "- Requires confirmation: `true`",
            "",
            "Current evidence:",
            "",
            f"> {str(item.get('current') or '').replace(chr(10), ' ')[:700]}",
            "",
            "Recommended action:",
            "",
            f"> {str(item.get('proposed') or '').replace(chr(10), ' ')[:700]}",
            "",
        ])
    return "\n".join(lines)