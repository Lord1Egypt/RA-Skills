from __future__ import annotations

import hashlib
import re
from collections import Counter, defaultdict

SCHEMA_VERSION = 2
TOOL_VERSION = "0.2.0"
ABS_RE = re.compile(r"\b(always|never|must|required|mandatory|forbidden|all|every|only)\b", re.I)
EXC_RE = re.compile(r"\b(unless|except|when appropriate|when necessary|if needed|fallback)\b", re.I)
EXAMPLEISH_RE = re.compile(r"\b(bad example|anti-pattern|quoted|example of|do not do this|unsafe example)\b", re.I)
SEV = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1, "Info": 0}
NEGATION_BEFORE_RE = re.compile(
    r"(?:^|\b)(?:never|do\s+not|don't|must\s+not|should\s+not|avoid|forbid|forbidden(?:\s+to)?|no)\b[\w\s`'\"-]{0,50}$",
    re.I,
)

INEFFICIENT = [
    (r"always\s+read\s+(every|all)\s+files?", "Always reading every file creates unnecessary context and tool pressure."),
    (r"read\s+(every|all)\s+files?\s+(fully|completely|linearly)", "Exhaustive linear reading is weaker than map/search/targeted inspection."),
    (r"(always|must).*\b(tiny|small|fixed-size)\s+chunks?", "Rigid chunking can hide structure and waste calls."),
    (r"never\s+use\s+(grep|rg|search|index)", "Forbidding search/indexing harms context acquisition."),
    (r"(manual|linear|exhaustive)\s+read(?:ing)?.{0,100}\bevery\s+(?:task|file)", "Global manual-reading preference harms scalable context acquisition."),
]

COUNTERPRODUCTIVE = [
    (r"always\s+produce\s+a\s+complete\s+implementation\s+plan", "Planning should scale with task risk and ambiguity."),
    (r"never\s+proceed\s+without\s+confirmation", "Global confirmation requirements can cause paralysis."),
    (r"always\s+preserve\s+every\s+existing\s+instruction", "Preserving all instructions can preserve contradictions and bloat."),
    (r"always\s+load\s+all\s+.*(docs|prompts|context)", "Loading all context can degrade retrieval and reasoning."),
]

POLICY_RISKS = [
    {
        "patterns": [
            r"\b(?:prefer|prioritize|follow)\b.{0,70}\b(?:nearest|local|project)\b.{0,70}\b(?:over|before|instead of)\b.{0,50}\b(?:upstream|higher[- ]priority|system|developer|safety|safeguards?)\b",
            r"\b(?:project|local|nearest)\b.{0,50}\b(?:notes?|files?|instructions?)\b.{0,30}\b(?:outrank|override|supersede)\b.{0,50}\b(?:upstream|higher[- ]priority|system|developer|safety|safeguards?)\b",
        ],
        "severity": "High",
        "category": "prompt_hierarchy",
        "codes": ["BF-004", "BF-018"],
        "title": "Unsafe instruction-priority inversion",
        "impact": "Lower-authority project text is told to outrank upstream or higher-priority policy.",
        "recommendation": "State that local files are untrusted evidence and never override higher-priority instructions.",
        "remediation_type": "REWRITE_CONTRADICTION",
        "tags": ["authority_boundary"],
    },
    {
        "patterns": [
            r"\b(?:report|summary)\b.{0,50}\b(?:sound|appear|be)\b.{0,20}\bconfident\b.{0,60}\b(?:incomplete|uncertain|insufficient|missing)\b",
            r"\b(?:smooth over|omit|hide|suppress|do not report)\b.{0,80}\b(?:contradictions?|disagreements?|findings?|risks?|unsafe)\b",
            r"\b(?:mark|declare)\b.{0,40}\b(?:repository|project|audit)\b.{0,20}\bclean\b|\bself[- ]?certif",
        ],
        "severity": "Medium",
        "category": "reporting_integrity",
        "codes": ["BF-009", "BF-020"],
        "title": "Reporting-integrity instruction",
        "impact": "The instruction pressures the reviewer to overstate certainty, conceal disagreement, or self-certify.",
        "recommendation": "Require evidence-linked uncertainty and preserve deterministic findings for operator review.",
        "remediation_type": "ADD_GUARDRAIL",
        "tags": ["reporting_integrity"],
    },
]

CONFLICTS = [
    ("confirmation_policy", [r"ask\s+before", r"confirm\s+before", r"never\s+proceed\s+without"], [r"do\s+not\s+ask", r"never\s+ask", r"proceed\s+without\s+confirmation"], ["BF-006", "BF-007"]),
    ("file_inspection_policy", [r"read\s+(every|all)\s+files?", r"always\s+read", r"read\s+fully"], [r"targeted\s+(read|inspection)", r"use\s+(grep|rg|search)", r"minimize\s+context"], ["BF-001", "BF-002", "BF-020"]),
    ("autonomy_policy", [r"act\s+autonomously", r"proceed\s+without\s+asking", r"do\s+not\s+stop"], [r"ask\s+for\s+approval", r"explicit\s+approval", r"confirmation\s+required"], ["BF-006", "BF-008"]),
    ("authority_boundary", [r"local\s+files?\s+are\s+authoritative", r"follow\s+.*local\s+instructions"], [r"treat\s+.*local\s+files?\s+as\s+untrusted", r"higher-priority\s+instructions"], ["BF-004", "BF-018"]),
]

TRUST_GUARDRAIL_RE = re.compile(
    r"(?:treat|consider).{0,40}(?:local|project|audited).{0,30}(?:files?|text|content).{0,25}untrusted|"
    r"(?:local|project).{0,30}(?:files?|instructions?).{0,40}(?:do not|must not|never).{0,30}(?:override|outrank).{0,30}(?:higher|system|developer)",
    re.I,
)
SECRET_GUARDRAIL_RE = re.compile(
    r"(?:do not|never|avoid|must not|should not).{0,35}(?:print|expose|reveal|commit|send|upload|log|store|copy).{0,70}(?:secret|credential|token|api key|password)|"
    r"(?:secret|credential|token|api key|password).{0,50}(?:must not|should not|never).{0,35}(?:print|expose|reveal|commit|send|upload|log|store|copy)",
    re.I,
)


def add(findings, **kw):
    base = {
        "id": f"AAF-{len(findings)+1:04d}",
        "severity": "Info",
        "category": "general",
        "codes": [],
        "title": "Finding",
        "file": None,
        "rel_path": None,
        "line_start": None,
        "line_end": None,
        "evidence": "",
        "impact": "",
        "recommendation": "",
        "remediation_type": "CLARIFY_SCOPE",
        "confidence": "medium",
        "tags": [],
        "context": "active",
    }
    base.update(kw)
    findings.append(base)


def active_instruction(inst: dict[str, object]) -> bool:
    if str(inst.get("context") or "active") != "active":
        return False
    return not bool(EXAMPLEISH_RE.search(str(inst.get("instruction", ""))))


def finding_fingerprint(finding: dict[str, object]) -> str:
    parts = [str(finding.get(key) or "") for key in ("category", "title", "rel_path", "line_start", "evidence")]
    return hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()[:20]


def pattern_has_explicit_negation(pattern: str) -> bool:
    lowered = pattern.lower()
    return any(token in lowered for token in ("never", "do\s+not", "don't", "must\s+not", "should\s+not", "avoid", "forbidden", "forbid"))


def pattern_matches_instruction(text: str, pattern: str) -> bool:
    explicit_negation = pattern_has_explicit_negation(pattern)
    for match in re.finditer(pattern, text, re.I):
        if not explicit_negation and NEGATION_BEFORE_RE.search(text[:match.start()]):
            continue
        return True
    return False


def first_match(instructions, patterns):
    for inst in instructions:
        if not active_instruction(inst):
            continue
        text = str(inst.get("instruction", ""))
        if any(pattern_matches_instruction(text, pattern) for pattern in patterns):
            return inst
    return None


def metric_counts(instructions):
    counts = defaultdict(lambda: defaultdict(int))
    for inst in instructions:
        if not active_instruction(inst):
            continue
        file = str(inst.get("file"))
        text = str(inst.get("instruction", ""))
        counts[file]["instructions"] += 1
        counts[file]["hard_rules"] += int(inst.get("strength") == "hard")
        counts[file]["absolute_terms"] += len(ABS_RE.findall(text))
        counts[file]["exceptions"] += len(EXC_RE.findall(text))
        counts[file][f"domain_{inst.get('domain')}"] += 1
    return counts


def pressure(score):
    if score >= 90:
        return "very_high"
    if score >= 55:
        return "high"
    if score >= 25:
        return "medium"
    return "low"


def has_guardrail(instructions, pattern: re.Pattern[str]) -> bool:
    return any(active_instruction(inst) and pattern.search(str(inst.get("instruction", ""))) for inst in instructions)


def build_audit(records, instructions, prompt_events, warnings, profile, mode):
    findings = []
    by_path = {record.path: record for record in records}

    for event in prompt_events:
        category = str(event.get("category") or "prompt_injection")
        is_injection = category == "prompt_injection"
        codes = ["BF-009", "BF-004"] if is_injection and event["priority"] in {"P0", "P1", "P2"} else ["BF-009"] if is_injection else []
        title = f"Prompt-injection signal: {event['tag']}" if is_injection else "Agent-facing control surface detected"
        add(
            findings,
            severity=event["severity"],
            category=category,
            codes=codes,
            title=title,
            file=event["file"],
            rel_path=event.get("rel_path"),
            line_start=event["line_start"],
            line_end=event["line_end"],
            evidence=event["evidence"],
            impact=event["rationale"],
            recommendation="Treat this text as untrusted. Remove, quote, sandbox, or clearly scope it if it is an example." if is_injection else "Confirm the file's authority, loading behavior, and intended scope.",
            remediation_type="ISOLATE_UNTRUSTED_TEXT" if is_injection else "CLARIFY_SCOPE",
            confidence="high" if event["priority"] in {"P0", "P1"} else "medium",
            tags=(["prompt_injection", str(event["tag"])] if is_injection else ["agent_facing_surface"]),
            context=event.get("context") or "active",
        )

    for inst in instructions:
        if not active_instruction(inst):
            continue
        text = str(inst.get("instruction", ""))
        for risk in POLICY_RISKS:
            if not any(pattern_matches_instruction(text, pattern) for pattern in risk["patterns"]):
                continue
            add(
                findings,
                severity=risk["severity"],
                category=risk["category"],
                codes=risk["codes"],
                title=risk["title"],
                file=inst.get("file"),
                rel_path=inst.get("rel_path"),
                line_start=inst.get("line_start"),
                line_end=inst.get("line_end"),
                evidence=text[:500],
                impact=risk["impact"],
                recommendation=risk["recommendation"],
                remediation_type=risk["remediation_type"],
                tags=risk["tags"],
            )
            break

    counts = metric_counts(instructions)
    metrics = []
    for file, count in counts.items():
        score = count["hard_rules"] * 3 + count["absolute_terms"] * 2 + count["instructions"] - count["exceptions"] * 2
        label = pressure(score)
        record = by_path.get(file)
        metrics.append({
            "file": file,
            "rel_path": getattr(record, "rel_path", file),
            "instructions": count["instructions"],
            "hard_rules": count["hard_rules"],
            "absolute_terms": count["absolute_terms"],
            "exceptions": count["exceptions"],
            "enforcement_score": score,
            "enforcement_pressure": label,
        })
        if label in {"high", "very_high"}:
            add(
                findings,
                severity="High" if label == "very_high" else "Medium",
                category="enforcement_pressure",
                codes=["BF-003", "BF-005", "BF-020"],
                title=f"{label.replace('_', ' ').title()} enforcement pressure",
                file=file,
                rel_path=getattr(record, "rel_path", None),
                evidence=f"hard_rules={count['hard_rules']}, absolute_terms={count['absolute_terms']}, exceptions={count['exceptions']}",
                impact="The agent may become rigid, slow, overly literal, or hesitant.",
                recommendation="Soften global mandates, add exceptions, and move detailed workflows into skills or references.",
                remediation_type="SOFTEN_OVER_ENFORCED_RULE",
                tags=["over_enforcement"],
            )

    for inst in instructions:
        if not active_instruction(inst):
            continue
        text = str(inst.get("instruction", ""))
        for pattern, impact in INEFFICIENT:
            if pattern_matches_instruction(text, pattern):
                add(
                    findings,
                    severity="Medium",
                    category="tool_use_and_file_inspection",
                    codes=["BF-001", "BF-002", "BF-005", "BF-020"],
                    title="Inefficient file-inspection instruction",
                    file=inst.get("file"),
                    rel_path=inst.get("rel_path"),
                    line_start=inst.get("line_start"),
                    line_end=inst.get("line_end"),
                    evidence=text[:500],
                    impact=impact,
                    recommendation="Replace with a structure/search/targeted-read policy that scales with file size and task risk.",
                    remediation_type="REPLACE_COUNTERPRODUCTIVE_WORKFLOW",
                    tags=["file_inspection", "tool_use"],
                )
                break
        for pattern, impact in COUNTERPRODUCTIVE:
            if pattern_matches_instruction(text, pattern):
                add(
                    findings,
                    severity="Medium",
                    category="counterproductive_rule",
                    codes=["BF-020", "BF-003"],
                    title="Counterproductive global rule",
                    file=inst.get("file"),
                    rel_path=inst.get("rel_path"),
                    line_start=inst.get("line_start"),
                    line_end=inst.get("line_end"),
                    evidence=text[:500],
                    impact=impact,
                    recommendation="Scope the rule to high-risk cases or convert it into a preference with exceptions.",
                    remediation_type="SOFTEN_OVER_ENFORCED_RULE",
                    tags=["counterproductive", "over_enforcement"],
                )
                break

    for name, positive, negative, codes in CONFLICTS:
        first = first_match(instructions, positive)
        second = first_match(instructions, negative)
        if first and second:
            add(
                findings,
                severity="High" if name in {"authority_boundary", "autonomy_policy"} else "Medium",
                category="contradiction_or_contrariety",
                codes=codes,
                title=f"Operational tension in {name.replace('_', ' ')}",
                file=first.get("file"),
                rel_path=first.get("rel_path"),
                line_start=first.get("line_start"),
                line_end=first.get("line_end"),
                evidence=f"A: {first.get('instruction')} | B: {second.get('instruction')}",
                impact="Conflicting or contrarian instructions can degrade agent behavior even when each rule is reasonable alone.",
                recommendation="Rewrite both instructions into one scoped policy with explicit risk-based exceptions.",
                remediation_type="REWRITE_CONTRADICTION",
                tags=["contradiction", name],
                related_locations=[{"rel_path": second.get("rel_path"), "line_start": second.get("line_start")}],
            )

    normalized = defaultdict(list)
    for inst in instructions:
        if not active_instruction(inst):
            continue
        normalized_value = str(inst.get("normalized", ""))
        if len(normalized_value) >= 45:
            normalized[normalized_value].append(inst)
    for group in normalized.values():
        files = {str(item.get("file")) for item in group}
        if len(group) >= 3 or len(files) >= 2:
            first = group[0]
            add(
                findings,
                severity="Low",
                category="duplicated_governance",
                codes=["BF-011", "BF-010"],
                title="Repeated instruction appears in multiple places",
                file=first.get("file"),
                rel_path=first.get("rel_path"),
                line_start=first.get("line_start"),
                line_end=first.get("line_end"),
                evidence=str(first.get("instruction", ""))[:500],
                impact=f"The same or nearly same instruction appears {len(group)} times across {len(files)} file(s).",
                recommendation="Pick one canonical layer and remove or soften duplicates after review.",
                remediation_type="DELETE_DUPLICATE",
                tags=["duplication", "bloat"],
            )
            break

    for record in records:
        count = counts.get(record.path, {})
        if record.line_count > 700 or record.size_bytes > 80000:
            add(
                findings,
                severity="Low",
                category="prompt_bloat_and_layering",
                codes=["BF-010"],
                title="Large prompt-bearing file may contribute to context bloat",
                file=record.path,
                rel_path=record.rel_path,
                evidence=f"line_count={record.line_count}, size_bytes={record.size_bytes}",
                impact="Long active prompts increase retrieval cost and can preserve stale or duplicated guidance.",
                recommendation="Split durable policy, examples, temporary notes, and historical material into separate layers.",
                remediation_type="SPLIT_FILE",
                tags=["bloat"],
            )
        if record.role == "memory" and count.get("hard_rules", 0) >= 3:
            add(
                findings,
                severity="Medium",
                category="prompt_bloat_and_layering",
                codes=["BF-016", "BF-012"],
                title="Memory-like file contains hard procedural rules",
                file=record.path,
                rel_path=record.rel_path,
                evidence=f"hard_rules={count.get('hard_rules', 0)}",
                impact="Memory should store durable facts, not active operational law.",
                recommendation="Move reusable procedures into a skill or project instruction layer.",
                remediation_type="MOVE_TO_SKILL",
                tags=["memory", "layering"],
            )
        toolish = count.get("domain_tool_use", 0) + count.get("domain_file_inspection", 0)
        if record.role == "identity_or_system" and toolish >= 5:
            add(
                findings,
                severity="Medium",
                category="prompt_bloat_and_layering",
                codes=["BF-012", "BF-005"],
                title="Identity/system-like file carries many concrete tool-use rules",
                file=record.path,
                rel_path=record.rel_path,
                evidence=f"tool_or_file_instruction_count={toolish}",
                impact="Durable identity layers can become cluttered with procedural rules that belong in skills or project guidance.",
                recommendation="Move reusable tool workflows into a skill and keep identity guidance high level.",
                remediation_type="MOVE_TO_SKILL",
                tags=["layering", "tool_use"],
            )

    config_text = "\n".join(record.text.lower() for record in records if record.role == "config")
    instruction_text = "\n".join(str(inst.get("instruction", "")) for inst in instructions if active_instruction(inst)).lower()
    if re.search(r"context[^\n]{0,80}(max|limit)[^\n]{0,80}([5-9]\d{4}|\d{6,})", config_text) and re.search(r"tiny chunks|small chunks|fixed-size chunks|read.*linearly", instruction_text):
        add(
            findings,
            severity="Medium",
            category="config_prompt_mismatch",
            codes=["BF-017", "BF-002"],
            title="Config appears to allow broad context while prompts force inefficient reading",
            evidence="Config contains a high context limit while prompt instructions mention tiny or fixed-size reads.",
            impact="The agent may behave inefficiently despite available context capacity.",
            recommendation="Replace rigid chunking with a structural inspect/search/read policy.",
            remediation_type="REPLACE_COUNTERPRODUCTIVE_WORKFLOW",
            tags=["config", "file_inspection"],
        )

    if records and not has_guardrail(instructions, TRUST_GUARDRAIL_RE):
        add(
            findings,
            severity="Low",
            category="missing_guardrail",
            codes=["BF-018", "BF-009"],
            title="No clear trust-boundary guardrail found for local agent-facing files",
            evidence="No active protective trust-boundary instruction was found.",
            impact="Prompt-like project files may be over-obeyed if malicious or stale content is discovered.",
            recommendation="Add a concise trust-boundary rule in the correct global or project instruction layer.",
            remediation_type="ADD_GUARDRAIL",
            tags=["trust_boundary"],
        )
    if records and not has_guardrail(instructions, SECRET_GUARDRAIL_RE):
        add(
            findings,
            severity="Low",
            category="missing_guardrail",
            codes=["BF-019"],
            title="No explicit secret-handling guidance found",
            evidence="No active protective secret-handling instruction was found.",
            impact="Agents may accidentally expose sensitive values in reports, logs, or patches.",
            recommendation="Add a short rule to avoid printing, committing, or exfiltrating secrets.",
            remediation_type="ADD_GUARDRAIL",
            tags=["secret_handling"],
        )

    influence = defaultdict(list)
    for record in records:
        influence[record.influence].append({
            "path": record.path,
            "rel_path": record.rel_path,
            "role": record.role,
            "prompt_bearing": record.prompt_bearing,
            "line_count": record.line_count,
        })

    for finding in findings:
        if finding.get("file") and not finding.get("rel_path"):
            record = by_path.get(str(finding.get("file")))
            finding["rel_path"] = getattr(record, "rel_path", None)
        finding["fingerprint"] = finding_fingerprint(finding)

    findings.sort(key=lambda finding: (-SEV.get(str(finding.get("severity")), 0), str(finding.get("id"))))
    inventory = [record.inventory_row() for record in records]
    audit_material = [profile, mode]
    audit_material.extend(f"{row.get('rel_path')}:{row.get('sha256')}:{row.get('truncated')}" for row in inventory)
    audit_material.extend(str(finding.get("fingerprint")) for finding in findings)
    audit_id = hashlib.sha256("\n".join(audit_material).encode("utf-8")).hexdigest()[:24]

    prompt_injection_count = sum(1 for event in prompt_events if event.get("category") == "prompt_injection")
    return {
        "schema_version": SCHEMA_VERSION,
        "tool_version": TOOL_VERSION,
        "audit_id": audit_id,
        "profile": profile,
        "mode": mode,
        "warnings": warnings,
        "inventory": inventory,
        "instructions": instructions,
        "prompt_events": prompt_events,
        "findings": findings,
        "influence_map": dict(influence),
        "enforcement_metrics": sorted(metrics, key=lambda metric: int(metric["enforcement_score"]), reverse=True),
        "summary": {
            "files_scanned": len(records),
            "instructions_extracted": len(instructions),
            "active_instructions": sum(1 for inst in instructions if active_instruction(inst)),
            "prompt_injection_events": prompt_injection_count,
            "agent_facing_events": len(prompt_events) - prompt_injection_count,
            "findings_total": len(findings),
            "severity_counts": dict(Counter(finding["severity"] for finding in findings)),
            "category_counts": dict(Counter(finding["category"] for finding in findings)),
        },
    }
