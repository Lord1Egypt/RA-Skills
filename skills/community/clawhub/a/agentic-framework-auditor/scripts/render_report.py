from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from agent_review import public_gate_state, write_agent_review_artifacts
from fix_planner import build_fix_plan, render_fix_plan_markdown

SECTIONS = [
    ("prompt_hierarchy", "Prompt Hierarchy Findings"),
    ("reporting_integrity", "Reporting Integrity Findings"),
    ("contradiction_or_contrariety", "Contradictions and Contrarieties"),
    ("enforcement_pressure", "Enforcement Pressure Analysis"),
    ("prompt_injection", "Prompt Injection Findings"),
    ("prompt_bloat_and_layering", "Prompt Bloat and Layering Findings"),
    ("config_prompt_mismatch", "Config-Prompt Mismatches"),
    ("tool_use_and_file_inspection", "Tool-Use and File-Inspection Findings"),
    ("counterproductive_rule", "Counterproductive Rules"),
    ("duplicated_governance", "Duplicated Governance"),
    ("missing_guardrail", "Missing Guardrails"),
    ("agent_facing_surface", "Agent-Facing Surface Observations"),
]


def clean(value: Any) -> str:
    if value is None:
        return ""
    return str(value).replace("\n", " ").strip()


def location(finding: dict[str, Any]) -> str:
    loc = clean(finding.get("rel_path")) or clean(finding.get("file")) or "project"
    if finding.get("line_start"):
        loc += f":{finding.get('line_start')}"
    return loc


def one_line(finding: dict[str, Any]) -> str:
    codes = ", ".join(finding.get("codes") or [])
    return f"- **{finding.get('severity')}** `{finding.get('id')}` {finding.get('title')} ({codes}) - `{location(finding)}`"


def render_markdown_report(audit: dict[str, Any], args_info: dict[str, Any]) -> str:
    summary = audit["summary"]
    findings = audit.get("findings", [])
    lines = [
        "# Agentic Framework Audit Report",
        "",
        "## Executive Summary",
        "",
        f"- Audit ID: `{audit.get('audit_id')}`",
        f"- Tool version: `{audit.get('tool_version')}`",
        f"- Schema version: `{audit.get('schema_version')}`",
        f"- Profile: `{audit.get('profile')}`",
        f"- Mode: `{audit.get('mode')}`",
        f"- Files scanned: `{summary.get('files_scanned')}`",
        f"- Instructions extracted: `{summary.get('instructions_extracted')}`",
        f"- Findings: `{summary.get('findings_total')}`",
        f"- Severity counts: `{summary.get('severity_counts')}`",
        "",
    ]
    if audit.get("warnings"):
        lines.extend(["## Scan Warnings", ""])
        lines.extend(f"- `{warning}`" for warning in audit.get("warnings", []))
        lines.append("")

    review = audit.get("agent_review")
    if review:
        gate = public_gate_state(review)
        lines.extend([
            "## Agent Review Gate",
            "",
            f"- Requested: `{gate.get('requested')}`",
            f"- Status: `{gate.get('status')}`",
            f"- Reviewer identity: `{gate.get('reviewer_id')}`",
            f"- Review profile: `{gate.get('review_profile')}`",
            f"- Selected findings: `{gate.get('selected_finding_count')}`",
            f"- Responsibility: {gate.get('responsibility_statement')}",
            "",
        ])
        blockers = gate.get("blocked_reasons") or []
        if blockers:
            lines.append("Blocked reasons:")
            for item in blockers[:20]:
                lines.append(f"- `{item.get('severity')}` `{item.get('reason')}` - {item.get('detail')}")
                if item.get("operator_action"):
                    lines.append(f"  Action: {item.get('operator_action')}")
            if len(blockers) > 20:
                lines.append(f"- ... {len(blockers) - 20} more")
            lines.append("")

    lines.extend([
        "## Scan Mode and Scope",
        "",
        f"- Roots: `{args_info.get('roots')}`",
        f"- Includes: `{args_info.get('includes')}`",
        f"- Excludes: `{args_info.get('excludes')}`",
        f"- Profile home included: `{args_info.get('include_profile_home')}`",
        f"- Sensitive files included: `{args_info.get('include_sensitive_files')}`",
        f"- Operator-edited only: `{args_info.get('operator_edited_only')}`",
        f"- Operator-edited files: `{args_info.get('operator_edited_files')}`",
        f"- Role filter: `{args_info.get('only_roles')}`",
        f"- Prompt-bearing only: `{args_info.get('prompt_bearing_only')}`",
        "",
        "## Prompt Influence Map",
        "",
    ])
    influence = audit.get("influence_map", {})
    if not influence:
        lines.append("No prompt-bearing files were found.")
    for name, files in sorted(influence.items()):
        lines.extend([f"### {str(name).replace('_', ' ').title()}", ""])
        for item in files[:40]:
            lines.append(f"- `{item.get('rel_path')}` - {item.get('role')} ({item.get('line_count')} lines)")
        if len(files) > 40:
            lines.append(f"- ... {len(files) - 40} more")
        lines.append("")

    lines.extend(["## Behavioral Failure Findings", ""])
    if not findings:
        lines.append("No findings were produced by the deterministic scanner.")
    else:
        lines.extend(one_line(finding) for finding in findings[:25])
        if len(findings) > 25:
            lines.append(f"- ... {len(findings) - 25} more findings in JSON output")
    lines.append("")

    for category, title in SECTIONS:
        bucket = [f for f in findings if f.get("category") == category]
        lines.extend([f"## {title}", ""])
        if not bucket:
            lines.extend(["No findings in this category.", ""])
            continue
        for finding in bucket[:20]:
            lines.append(one_line(finding))
            evidence = clean(finding.get("evidence"))[:700]
            rec = clean(finding.get("recommendation"))[:700]
            if evidence:
                lines.append(f"  Evidence: {evidence}")
            if rec:
                lines.append(f"  Recommendation: {rec}")
        if len(bucket) > 20:
            lines.append(f"- ... {len(bucket) - 20} more")
        lines.append("")

    lines.extend(["## Skill Architecture Findings", ""])
    skill_files = [row for row in audit.get("inventory", []) if row.get("role") == "skill"]
    if skill_files:
        lines.append(f"Scanned `{len(skill_files)}` skill-related file(s). Review broad descriptions, hidden install steps, and duplicated procedure text.")
    else:
        lines.append("No skill files were detected in the selected scope.")
    lines.append("")

    lines.extend(["## Fix Recommendations", ""])
    fix_items = build_fix_plan(findings)
    if not fix_items:
        lines.append("No fix recommendations were generated.")
    else:
        for item in fix_items[:20]:
            lines.append(f"- `{item.get('finding_id')}` `{item.get('fix_type')}` - {item.get('proposed')}")
        if len(fix_items) > 20:
            lines.append(f"- ... {len(fix_items) - 20} more in the fix plan")
    lines.append("")

    lines.extend([
        "## Auto-Fix Eligibility",
        "",
        "Automatic patching is disabled. Use the generated fix plan for review, then apply edits only after explicit operator approval.",
        "",
        "## Evidence Appendix",
        "",
    ])
    for finding in findings[:100]:
        lines.extend([
            f"### {finding.get('id')} - {finding.get('title')}",
            "",
            f"- Severity: `{finding.get('severity')}`",
            f"- Category: `{finding.get('category')}`",
            f"- Codes: `{', '.join(finding.get('codes') or [])}`",
            f"- Location: `{location(finding)}`",
            f"- Impact: {finding.get('impact')}",
            f"- Recommendation: {finding.get('recommendation')}",
            "",
            f"Evidence: {clean(finding.get('evidence'))[:1000]}",
            "",
        ])
    return "\n".join(lines)


def render_all(audit: dict[str, Any], output_dir: str | Path, prefix: str, args_info: dict[str, Any]) -> dict[str, str]:
    output = Path(output_dir).expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    paths = {
        "report": output / f"{prefix}_report.md",
        "findings": output / f"{prefix}_findings.json",
        "inventory": output / f"{prefix}_inventory.csv",
        "instruction_graph": output / f"{prefix}_instruction_graph.json",
        "fix_plan": output / f"{prefix}_fix_plan.md",
    }

    paths["report"].write_text(render_markdown_report(audit, args_info), encoding="utf-8")
    payload = {k: audit.get(k) for k in ("schema_version", "tool_version", "audit_id", "summary", "profile", "mode", "warnings", "findings", "enforcement_metrics", "agent_review")}
    if payload.get("agent_review"):
        payload["agent_review"] = public_gate_state(payload["agent_review"])
    paths["findings"].write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    fields = ["path", "root", "rel_path", "size_bytes", "line_count", "sha256", "extension", "role", "influence", "prompt_bearing", "truncated", "warning"]
    with paths["inventory"].open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in audit.get("inventory", []):
            writer.writerow({field: row.get(field, "") for field in fields})

    graph = {"schema_version": audit.get("schema_version"), "audit_id": audit.get("audit_id"), "influence_map": audit.get("influence_map"), "instructions": audit.get("instructions"), "prompt_events": audit.get("prompt_events")}
    paths["instruction_graph"].write_text(json.dumps(graph, indent=2, ensure_ascii=False), encoding="utf-8")
    paths["fix_plan"].write_text(render_fix_plan_markdown(build_fix_plan(audit.get("findings", []))), encoding="utf-8")
    paths.update(write_agent_review_artifacts(audit, output, prefix))
    return {key: str(value) for key, value in paths.items()}