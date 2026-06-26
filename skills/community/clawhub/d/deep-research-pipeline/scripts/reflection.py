"""Reflection — Coverage/gap check between research cycles.

After every researcher → analyst cycle, the orchestrator runs reflection to decide
whether to continue researching or proceed to writing.

Usage:
    python reflection.py --question "..." --findings <json_file_or_stdin> --cycle 1 --original-plan <json_file>

Input findings: JSON array of analyst output
    [{"theme": "...", "claims": [...], "sources": [...], "confidence": 0.8}]

Output: JSON with coverage assessment, gaps, and continue decision.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import sys
import time
import urllib.request
from typing import Any, Optional

from llm_client import call_llm as _call_glm

MAX_CYCLES = 8
DEFAULT_TIME_BUDGET_SECONDS = int(os.environ.get("DEEP_RESEARCH_TIME_BUDGET_SECONDS", "900"))
DEFAULT_TOKEN_BUDGET = int(os.environ.get("DEEP_RESEARCH_TOKEN_BUDGET", "60000"))


@dataclasses.dataclass(frozen=True)
class ResearchPlan:
    question: str
    dimensions: list[str]
    dimension_questions: dict[str, list[str]]
    created_at_unix: float = dataclasses.field(default_factory=lambda: time.time())
    budget_seconds: int = DEFAULT_TIME_BUDGET_SECONDS
    budget_tokens: int = DEFAULT_TOKEN_BUDGET


@dataclasses.dataclass(frozen=True)
class ReflectionResult:
    should_continue: bool
    gaps: list[str]
    coverage_score: float
    next_dimensions: list[str]
    summary: str


def _normalize_findings(findings_input) -> list[dict]:
    """Convert analyst output formats into the themed format reflection expects.

    Handles:
    - Flat list: [{"claim": "...", "dimension": "...", ...}]
    - Wrapped: {"merged_findings": [...]}
    - Already themed: [{"theme": "...", "claims": [...], "sources": [...]}]
    - Researcher format: [{"dimension": "...", "findings": [...]}]
    """
    # Unwrap if dict with merged_findings key
    if isinstance(findings_input, dict):
        if "merged_findings" in findings_input:
            findings_input = findings_input["merged_findings"]
        elif "findings" in findings_input and "dimension" in findings_input:
            # Single researcher output
            findings_input = [findings_input]
        else:
            findings_input = [findings_input]

    if not isinstance(findings_input, list):
        return []

    # Check if already in themed format
    if (
        findings_input
        and "theme" in findings_input[0]
        and "claims" in findings_input[0]
    ):
        return findings_input

    # Check if researcher format: [{dimension, findings: [...]}]
    if (
        findings_input
        and isinstance(findings_input[0], dict)
        and "findings" in findings_input[0]
    ):
        groups = {}
        for item in findings_input:
            dim = item.get("dimension", "Unknown")
            if dim not in groups:
                groups[dim] = {
                    "theme": dim,
                    "claims": [],
                    "sources": [],
                    "confidence": 0,
                }
            for f in item.get("findings", []):
                groups[dim]["claims"].append(f.get("claim", str(f)))
                src = f.get("source", f.get("source_url", ""))
                if src and src not in groups[dim]["sources"]:
                    groups[dim]["sources"].append(src)
                conf = f.get("confidence", 0)
                groups[dim]["confidence"] = max(groups[dim]["confidence"], conf)
        return list(groups.values())

    # Flat list of findings — group by dimension/theme
    groups = {}
    for f in findings_input:
        theme = f.get("dimension", f.get("theme", "General"))
        if theme not in groups:
            groups[theme] = {
                "theme": theme,
                "claims": [],
                "sources": [],
                "confidence": 0,
            }
        groups[theme]["claims"].append(f.get("claim", str(f)))
        src = f.get("source", f.get("source_url", f.get("sources", "")))
        if isinstance(src, list):
            for s in src:
                if s and s not in groups[theme]["sources"]:
                    groups[theme]["sources"].append(s)
        elif src and src not in groups[theme]["sources"]:
            groups[theme]["sources"].append(src)
        conf = f.get("confidence", 0)
        groups[theme]["confidence"] = max(groups[theme]["confidence"], conf)
    return list(groups.values())


def reflect_llm(
    question: str,
    findings: list[dict],
    cycle: int,
    original_plan: Optional[dict] = None,
    max_cycles: int = MAX_CYCLES,
    api_key: Optional[str] = None,
) -> dict:
    """Legacy LLM-based reflection (kept for backwards compatibility)."""

    system = (
        "You are a research reflection analyzer. After a research cycle, you assess "
        "what's been found, what's missing, and whether more research would help.\n\n"
        "Be rigorous and honest.\n\n"
        "Output ONLY valid JSON with this schema:\n"
        "{\n"
        '  "covered": [{"theme": "...", "confidence": 0.9, "source_count": N}],\n'
        '  "gaps": [{"question": "...", "why_important": "..."}],\n'
        '  "coverage_score": 0.0,\n'
        '  "should_continue": true,\n'
        '  "continue_reason": "...",\n'
        '  "next_cycle_plan": {"dimensions": ["..."], "specific_questions": ["..."]}\n'
        "}\n\n"
        f"Rules:\n- Hard stop at cycle {max_cycles}\n"
    )

    findings = _normalize_findings(findings)
    findings_text = []
    for f in findings:
        theme = f.get("theme", "Unknown")
        claims = f.get("claims", [])
        confidence = f.get("confidence", "?")
        sources = f.get("sources", [])
        findings_text.append(
            f"Theme: {theme} (confidence: {confidence}, sources: {len(sources)})\n"
            f"Claims: {json.dumps(claims[:5], ensure_ascii=False)[:500]}"
        )

    plan_text = ""
    if original_plan:
        dims = original_plan.get("dimensions", [])
        plan_text = f"\nOriginal plan dimensions: {json.dumps(dims)}"

    prompt = (
        f"Research question: {question}\n"
        f"Cycle: {cycle}/{max_cycles}{plan_text}\n\n"
        f"Findings this cycle:\n{chr(10).join(findings_text)}\n\n"
        "Run reflection. Output JSON only."
    )

    response = _call_glm(prompt, system, max_tokens=4096, temperature=0.3, api_key=api_key).strip()
    if response.startswith("```"):
        response = response.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    reflection = json.loads(response)
    if cycle >= max_cycles:
        reflection["should_continue"] = False
        reflection["continue_reason"] = f"Hard stop at max cycles ({max_cycles})"
    reflection["cycle"] = cycle
    return reflection


def _estimate_tokens(obj: Any) -> int:
    """Cheap token proxy: ~4 chars/token."""
    try:
        s = json.dumps(obj, ensure_ascii=False)
    except Exception:
        s = str(obj)
    return max(1, len(s) // 4)


def _dimension_hits(plan_dimensions: list[str], findings: list[dict]) -> dict[str, int]:
    dims_norm = {d.strip().lower(): d for d in plan_dimensions if d and d.strip()}
    hits: dict[str, int] = {d: 0 for d in dims_norm.values()}

    for f in findings:
        dim = (f.get("dimension") or f.get("theme") or "").strip()
        if not dim:
            continue
        dim_key = dim.lower()
        if dim_key in dims_norm:
            hits[dims_norm[dim_key]] += 1
            continue
        for k_norm, original in dims_norm.items():
            if k_norm and (k_norm in dim_key or dim_key in k_norm):
                hits[original] += 1
                break

    return hits


def _gap_score(hit_count: int, avg_confidence: float, target_hits: int = 2) -> float:
    """0.0 = no gap, 1.0 = major gap."""
    coverage_component = 1.0 - min(1.0, hit_count / max(1, target_hits))
    confidence_component = 1.0 - max(0.0, min(1.0, avg_confidence))
    return max(0.0, min(1.0, coverage_component * 0.75 + confidence_component * 0.25))


def _progress_summary(plan: ResearchPlan, findings: list[dict], cycle: int, max_cycles: int) -> str:
    hits = _dimension_hits(plan.dimensions, findings)
    covered = [d for d, c in hits.items() if c > 0]
    missing = [d for d, c in hits.items() if c == 0]

    top_claims: list[str] = []
    for f in findings[:10]:
        claim = (f.get("claim") or "").strip()
        if claim:
            top_claims.append(claim[:160])

    lines = [
        f"Cycle {cycle}/{max_cycles}",
        f"Covered dimensions: {', '.join(covered) if covered else 'none'}",
        f"Missing dimensions: {', '.join(missing) if missing else 'none'}",
    ]
    if top_claims:
        lines.append("Top findings:")
        lines.extend([f"- {c}" for c in top_claims[:5]])
    return "\n".join(lines).strip()


def reflect(
    plan: ResearchPlan,
    findings: list[dict],
    cycle: int,
    max_cycles: int,
) -> ReflectionResult:
    """Coverage check + gap analysis + continue decision (max 8 cycles + budgets)."""
    normalized_findings = findings if isinstance(findings, list) else []
    max_cycles = min(int(max_cycles), MAX_CYCLES)
    cycle = int(cycle)

    plan_dimensions = [d for d in (plan.dimensions or []) if isinstance(d, str) and d.strip()]
    if not plan_dimensions:
        plan_dimensions = ["overview"]

    hits = _dimension_hits(plan_dimensions, normalized_findings)

    dim_conf_values: dict[str, list[float]] = {d: [] for d in plan_dimensions}
    for f in normalized_findings:
        dim_raw = (f.get("dimension") or f.get("theme") or "").strip().lower()
        conf = f.get("confidence", None)
        if conf is None:
            continue
        try:
            conf_f = float(conf)
        except Exception:
            continue
        for d in plan_dimensions:
            d_key = d.strip().lower()
            if not d_key:
                continue
            if dim_raw == d_key or d_key in dim_raw or dim_raw in d_key:
                dim_conf_values[d].append(conf_f)

    gap_scores: dict[str, float] = {}
    for d in plan_dimensions:
        avg_conf = (
            sum(dim_conf_values[d]) / len(dim_conf_values[d]) if dim_conf_values.get(d) else 0.0
        )
        gap_scores[d] = _gap_score(hits.get(d, 0), avg_conf)

    covered_count = sum(1 for d in plan_dimensions if hits.get(d, 0) > 0)
    coverage_score = covered_count / max(1, len(plan_dimensions))

    gap_ranked = sorted(gap_scores.items(), key=lambda kv: kv[1], reverse=True)
    gaps = [d for d, score in gap_ranked if score >= 0.45]
    next_dimensions = [d for d, score in gap_ranked if score >= 0.35][:3]

    now = time.time()
    elapsed = max(0.0, now - float(plan.created_at_unix))
    tokens_est = _estimate_tokens(normalized_findings)
    time_budget_hit = elapsed >= float(plan.budget_seconds) * 0.9
    token_budget_hit = tokens_est >= int(plan.budget_tokens) * 0.9

    should_continue = True
    if cycle >= max_cycles:
        should_continue = False
    elif time_budget_hit or token_budget_hit:
        should_continue = False
    elif coverage_score >= 0.8 and not gaps:
        should_continue = False
    elif not normalized_findings and cycle >= 1:
        should_continue = False

    summary = _progress_summary(plan, normalized_findings, cycle, max_cycles)
    if time_budget_hit or token_budget_hit:
        summary += (
            "\n\nBudget warning:"
            f"\n- elapsed_seconds={round(elapsed, 1)} / {plan.budget_seconds}"
            f"\n- est_tokens={tokens_est} / {plan.budget_tokens}"
        )

    return ReflectionResult(
        should_continue=should_continue,
        gaps=gaps,
        coverage_score=round(float(coverage_score), 3),
        next_dimensions=next_dimensions,
        summary=summary,
    )


def save_reflection(reflection: dict, output_dir: str) -> str:
    """Save reflection to a markdown file."""
    os.makedirs(output_dir, exist_ok=True)
    cycle = reflection.get("cycle", 0)
    filepath = os.path.join(output_dir, f"reflection-cycle-{cycle}.md")

    md = f"# Reflection Cycle {cycle}\n\n"
    md += f"**Coverage Score:** {reflection.get('coverage_score', '?')}\n"
    md += (
        f"**Should Continue:** {'Yes' if reflection.get('should_continue') else 'No'}\n"
    )
    if reflection.get("continue_reason"):
        md += f"**Reason:** {reflection['continue_reason']}\n"

    if reflection.get("covered"):
        md += "\n## Covered\n"
        for c in reflection["covered"]:
            md += f"- {c.get('theme', '?')} (confidence: {c.get('confidence', '?')}, sources: {c.get('source_count', '?')})\n"

    if reflection.get("gaps"):
        md += "\n## Gaps\n"
        for g in reflection["gaps"]:
            md += f"- {g.get('question', '?')}: {g.get('why_important', '')}\n"

    if reflection.get("contradictions"):
        md += "\n## Contradictions\n"
        for c in reflection["contradictions"]:
            md += f"- **A:** {c.get('claim_a', '')} ({c.get('source_a', '')})\n"
            md += f"  **B:** {c.get('claim_b', '')} ({c.get('source_b', '')})\n"
            md += f"  Resolution: {c.get('resolution', '?')}\n"

    if reflection.get("new_directions"):
        md += "\n## New Directions\n"
        for d in reflection["new_directions"]:
            md += f"- {d.get('topic', '?')}: {d.get('why_relevant', '')}\n"

    next_plan = reflection.get("next_cycle_plan", {})
    if next_plan.get("dimensions"):
        md += "\n## Next Cycle Plan\n"
        md += f"Dimensions: {json.dumps(next_plan['dimensions'])}\n"
        if next_plan.get("specific_questions"):
            md += f"Questions: {json.dumps(next_plan['specific_questions'], ensure_ascii=False)}\n"

    with open(filepath, "w") as f:
        f.write(md)

    return filepath


def main():
    parser = argparse.ArgumentParser(description="Research cycle reflection")
    parser.add_argument("--question", "-q", required=True)
    parser.add_argument("--findings", "-f", help="JSON file with analyst findings")
    parser.add_argument("--cycle", "-c", type=int, required=True)
    parser.add_argument(
        "--original-plan", "-p", help="JSON file with original research plan"
    )
    parser.add_argument("--max-cycles", type=int, default=MAX_CYCLES)
    parser.add_argument(
        "--output-dir", "-o", help="Directory to save reflection markdown"
    )
    parser.add_argument("--stdin", action="store_true")
    args = parser.parse_args()

    if args.stdin or not args.findings:
        findings = json.load(sys.stdin)
    else:
        with open(args.findings) as f:
            findings = json.load(f)

    original_plan_data = None
    if args.original_plan:
        with open(args.original_plan) as f:
            original_plan_data = json.load(f)

    # Build a ResearchPlan from the question and optional plan file
    if original_plan_data:
        plan = ResearchPlan(
            question=args.question,
            dimensions=original_plan_data.get("dimensions", ["overview"]),
            dimension_questions=original_plan_data.get("dimension_questions", {}),
            budget_seconds=original_plan_data.get("budget_seconds", DEFAULT_TIME_BUDGET_SECONDS),
            budget_tokens=original_plan_data.get("budget_tokens", DEFAULT_TOKEN_BUDGET),
        )
    else:
        plan = ResearchPlan(question=args.question, dimensions=["overview"])

    result = reflect(plan, findings, args.cycle, args.max_cycles)

    reflection_out = {
        "should_continue": result.should_continue,
        "gaps": result.gaps,
        "coverage_score": result.coverage_score,
        "next_dimensions": result.next_dimensions,
        "summary": result.summary,
        "cycle": args.cycle,
    }

    if args.output_dir:
        path = save_reflection(reflection_out, args.output_dir)
        print(f"Saved reflection to {path}", file=sys.stderr)

    print(json.dumps(reflection_out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
