#!/usr/bin/env python3
"""Build a Markdown research pack from a Baidu search run directory."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def read_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def count_jsonl(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as fh:
        return sum(1 for line in fh if line.strip())


def csv_or_none(values) -> str:
    if not values:
        return "none"
    return ", ".join(str(value) for value in values)


def required_intents_for(mode: str, profile: str) -> set[str]:
    if mode == "fast":
        return {"overview"}
    required = {"overview", "official"}
    if profile == "product":
        required.update({"review", "complaint", "platform", "experience"})
    elif profile == "event":
        required.update({"freshness", "timeline", "platform"})
    elif profile == "project":
        required.update({"docs", "code"})
    else:
        required.update({"review", "platform"})
    return required


def coverage_summary(plan: dict, summary: dict, sources: list[dict]) -> dict:
    mode = summary.get("mode") or plan.get("mode") or "normal"
    profile = plan.get("profile") or "general"
    required = set(summary.get("required_intents") or required_intents_for(mode, profile))
    attempted = set(summary.get("attempted_intents") or [])
    if not attempted:
        attempted.update(
            intent
            for source in sources
            for intent in source.get("matched_intents", [])
            if intent
        )
    if not attempted:
        attempted.update(
            item.get("intent")
            for item in plan.get("queries", [])
            if item.get("intent") and item.get("stage") == "seed"
        )
    missing = set(summary.get("missing_required_intents") or (required - attempted))
    return {
        "required_intents": sorted(required),
        "attempted_intents": sorted(attempted),
        "missing_required_intents": sorted(missing),
    }


def next_steps(summary: dict, sources: list[dict], error_count: int) -> list[str]:
    steps = []
    missing = summary.get("missing_required_intents") or []
    if missing:
        steps.append(f"Run targeted follow-up queries for missing intents: {csv_or_none(missing)}.")
    if error_count:
        steps.append("Inspect `errors.jsonl` before trusting coverage; rerun failed queries if needed.")
    if summary.get("stop_reason") == "max_raw_results_reached":
        steps.append("Use `deep --fixed` or raise `--max-raw-results` only if broader coverage is still required.")
    if not sources:
        steps.append("No deduped sources were produced; verify API key, endpoint response shape, and raw results.")
    if not steps:
        steps.append("Coverage is adequate for first-pass AI analysis; inspect raw results only for evidence-level checks.")
    return steps


def render_pack(run_dir: Path) -> str:
    plan = read_json(run_dir / "query_plan.json", {})
    deduped = read_json(run_dir / "deduped_sources.json", {"summary": {}, "sources": [], "duplicates": []})
    summary = read_json(run_dir / "run_summary.json", {})
    sources = deduped.get("sources", [])
    duplicates = deduped.get("duplicates", [])
    raw_count = summary.get("raw_result_count") or count_jsonl(run_dir / "raw_results.jsonl")
    error_count = count_jsonl(run_dir / "errors.jsonl")
    domain_counts = Counter(source.get("domain", "") for source in sources if source.get("domain"))
    intent_counts = Counter(
        intent
        for source in sources
        for intent in source.get("matched_intents", [])
        if intent
    )
    flag_counts = Counter(
        flag
        for source in sources
        for flag in source.get("quality_flags", [])
        if flag
    )
    coverage = coverage_summary(plan, summary, sources)
    decision_summary = dict(summary)
    decision_summary.update(coverage)

    lines = []
    lines.append(f"# Baidu Search Research Pack: {plan.get('topic', run_dir.name)}")
    lines.append("")
    lines.append("## Search Coverage")
    lines.append("")
    lines.append(f"- Mode: `{plan.get('mode', 'unknown')}`")
    lines.append(f"- Queries planned: {len(plan.get('queries', []))}")
    if summary.get("query_count") is not None:
        lines.append(f"- Queries run: {summary.get('query_count')}")
    lines.append(f"- Raw results: {raw_count}")
    lines.append(f"- Deduped sources: {len(sources)}")
    lines.append(f"- Duplicate mappings: {len(duplicates)}")
    lines.append(f"- Errors: {error_count}")
    if summary.get("cache_enabled") is not None:
        lines.append(f"- Cache enabled: `{summary.get('cache_enabled')}`")
    if summary.get("cache_hit_count") is not None:
        lines.append(f"- Cache hits: {summary.get('cache_hit_count')}")
    if summary.get("stop_reason"):
        lines.append(f"- Stop reason: `{summary.get('stop_reason')}`")
    lines.append("")

    if plan or summary:
        lines.append("## Coverage Decision")
        lines.append("")
        lines.append(f"- Required intents: {csv_or_none(decision_summary.get('required_intents'))}")
        lines.append(f"- Attempted intents: {csv_or_none(decision_summary.get('attempted_intents'))}")
        lines.append(f"- Missing required intents: {csv_or_none(decision_summary.get('missing_required_intents'))}")
        lines.append("")
        lines.append("Recommended next steps:")
        lines.append("")
        for step in next_steps(decision_summary, sources, error_count):
            lines.append(f"- {step}")
        lines.append("")

    if plan.get("queries"):
        lines.append("## Query Plan")
        lines.append("")
        for item in plan["queries"]:
            lines.append(f"- `{item.get('query')}` [{item.get('intent')}, {item.get('source')}]")
        lines.append("")

    lines.append("## Major Domains")
    lines.append("")
    for domain, count in domain_counts.most_common(15):
        lines.append(f"- {domain}: {count}")
    lines.append("")

    if intent_counts:
        lines.append("## Intent Coverage")
        lines.append("")
        for intent, count in intent_counts.most_common():
            lines.append(f"- {intent}: {count}")
        lines.append("")

    if flag_counts:
        lines.append("## Quality Flags")
        lines.append("")
        for flag, count in flag_counts.most_common():
            lines.append(f"- {flag}: {count}")
        lines.append("")

    lines.append("## Selected Sources")
    lines.append("")
    for source in sources[:50]:
        flags = ", ".join(source.get("quality_flags", [])) or "none"
        queries = " | ".join(source.get("matched_queries", [])[:5])
        lines.append(f"### {source.get('source_id')} - {source.get('title')}")
        lines.append("")
        lines.append(f"- URL: {source.get('url')}")
        lines.append(f"- Domain: `{source.get('domain')}`")
        lines.append(f"- Best rank: {source.get('best_rank')}")
        lines.append(f"- Matched queries: {queries}")
        intents = ", ".join(source.get("matched_intents", [])) or "unknown"
        lines.append(f"- Matched intents: {intents}")
        lines.append(f"- Flags: {flags}")
        snippet = (source.get("snippet") or "").strip()
        if snippet:
            lines.append(f"- Snippet: {snippet[:500]}")
        lines.append("")

    lines.append("## Duplicate Notes")
    lines.append("")
    lines.append("Duplicates were not discarded from raw data. See `deduped_sources.json` for mappings.")
    lines.append("")
    lines.append("## Limitations")
    lines.append("")
    lines.append("- Baidu AI Search web search has a per-query top_k ceiling of 50.")
    lines.append("- This pack is based on search result metadata/snippets unless page fetching is added separately.")
    lines.append("- Multiple API keys improve reliability and quota isolation; they do not create pagination for one query.")
    lines.append("- Sensitive or overseas topics may require non-Baidu sources for coverage.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_pack(run_dir), encoding="utf-8")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
