"""Researcher Agent — Orchestrates multi-source searches for deep research.

Takes a topic, generates search queries, searches across multiple sources
(web, GitHub, docs) in parallel, collects and deduplicates results, scores
by relevance, and returns structured research output.

This is Phase 2 of Deep Research v2. Integrates with Phase 1 scripts:
- query_generator.py for query expansion (3-5 variants per dimension)
- chunk_selector.py for relevance filtering (threshold >= 0.7)
- context_expander.py for context enrichment

Usage:
    # Full research on a topic
    python researcher.py "OpenClaw skills system"

    # Single dimension research (importable)
    from researcher import research_dimension
    findings = research_dimension("architecture", ["How does X work?", "What are the components?"])

    # CLI with options
    python researcher.py "OpenClaw skills system" --sources web github --limit 5

Output: JSON with findings, sources, gaps, and metadata.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError as FuturesTimeout
from typing import Optional

from llm_client import call_llm as _call_glm

# Reuse existing Phase 1 scripts
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from query_generator import generate_queries
from chunk_selector import select_relevant_chunks
from context_expander import expand_context
from research_sources import (
    WebSearchSource,
    GitHubSource,
    DocSource,
    score_results,
    deduplicate_results,
)

# ─── Config ───────────────────────────────────────────────────────────────────

SEARCH_TIMEOUT = 30       # seconds per individual search call
FETCH_TIMEOUT = 30        # seconds per URL fetch
MAX_PARALLEL_SEARCHES = 3 # concurrent search workers
CHUNK_SELECTOR_THRESHOLD = 0.7  # minimum score to keep a chunk


def _has_llm_config() -> bool:
    return bool(
        os.environ.get("LLM_API_KEY")
        or os.environ.get("OPENAI_API_KEY")
        or os.environ.get("ZAI_API_KEY")
    )


def _parse_json_response(text: str):
    """Parse JSON from LLM, stripping markdown fences."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(text)


# ─── Source registry ──────────────────────────────────────────────────────────

SOURCE_REGISTRY = {
    "web": WebSearchSource,
    "github": GitHubSource,
    "docs": DocSource,
}


# ─── Parallel search helpers ──────────────────────────────────────────────────


def _search_one(source_instance, query_text: str, limit: int) -> tuple[str, list[dict]]:
    """Execute a single search call. Returns (query, results).

    Designed to run in a thread — catches all exceptions and returns
    empty results instead of raising.
    """
    try:
        results = source_instance.search(query_text, limit=limit)
        return query_text, results
    except Exception as e:
        print(f"[timeout/error] search '{query_text[:60]}' failed: {e}", file=sys.stderr)
        return query_text, []


def _parallel_search(
    source_instance,
    queries: list[dict],
    max_results_per_source: int = 5,
    max_workers: int = MAX_PARALLEL_SEARCHES,
    timeout: int = SEARCH_TIMEOUT,
) -> list[dict]:
    """Run multiple search queries in parallel, return combined results.

    Args:
        source_instance: A source adapter (WebSearchSource, GitHubSource, etc.)
        queries: List of query dicts with 'query' key
        max_results_per_source: Max results per query
        max_workers: Max parallel search threads
        timeout: Timeout per search call (seconds)

    Returns:
        Combined list of result dicts from all queries.
    """
    all_results = []
    futures = {}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for q in queries:
            query_text = q["query"]
            future = executor.submit(
                _search_one, source_instance, query_text, max_results_per_source
            )
            futures[future] = query_text

        for future in as_completed(futures, timeout=timeout + 5):
            try:
                query_text, results = future.result(timeout=timeout)
                all_results.extend(results)
            except FuturesTimeout:
                query_text = futures[future]
                print(f"[timeout] search '{query_text[:60]}' exceeded {timeout}s", file=sys.stderr)
            except Exception as e:
                query_text = futures[future]
                print(f"[error] search '{query_text[:60]}': {e}", file=sys.stderr)

    return all_results


# ─── Query adaptation ─────────────────────────────────────────────────────────


def _adapt_queries_for_source(queries: list[dict], source_type: str, topic: str) -> list[dict]:
    """Adapt search queries for specific source types.

    GitHub search works better with short keyword queries.
    Web search handles longer natural language queries.
    Docs search benefits from including 'docs' or 'documentation'.
    """
    if source_type == "github":
        adapted = []
        adapted.append({"type": "keyword", "query": topic, "rationale": "Direct topic"})
        for q in queries[:3]:
            query_text = q["query"]
            simplified = re.sub(
                r"\b(how|what|when|where|which|who|why|does|is|are|the|a|an)\b",
                "", query_text, flags=re.IGNORECASE,
            )
            simplified = re.sub(r"\s+", " ", simplified).strip()
            words = simplified.split()
            if len(words) > 6:
                simplified = " ".join(words[:6])
            if simplified and simplified != topic:
                adapted.append({**q, "query": simplified})
        return adapted[:3]

    elif source_type == "docs":
        adapted = []
        for q in queries[:3]:
            adapted.append({**q, "query": f"{q['query']} documentation"})
        return adapted

    else:
        return queries


# ─── Main researcher ──────────────────────────────────────────────────────────


def research(
    topic: str,
    sources: Optional[list[str]] = None,
    max_queries: int = 5,
    max_results_per_source: int = 5,
    min_relevance: float = 0.4,
    use_chunk_selector: bool = True,
    use_context_expander: bool = True,
    api_key: Optional[str] = None,
) -> dict:
    """Run the full researcher pipeline.

    Args:
        topic: Research topic or question.
        sources: List of source types to search (default: ["web", "github", "docs"]).
        max_queries: Max search queries to generate (3-5 recommended).
        max_results_per_source: Max results per source per query.
        min_relevance: Minimum relevance score to include in output.
        use_chunk_selector: Run Phase 1 chunk_selector for LLM-based filtering.
        use_context_expander: Run Phase 1 context_expander for enrichment.
        api_key: Optional ZAI_API_KEY override.

    Returns:
        Dict with:
            - status: "complete" | "partial" | "no_results"
            - topic: str
            - findings: list of structured findings
            - sources: list of source metadata
            - gaps: list of identified gaps
            - metadata: pipeline stats
    """
    if api_key:
        os.environ["ZAI_API_KEY"] = api_key

    start_time = time.time()
    sources = sources or ["web", "github", "docs"]

    # ── Step 1: Generate search queries (3-5 variants) ─────────────────────
    queries = []
    try:
        queries = generate_queries(topic, max_queries=max(3, min(5, max_queries)))
    except Exception as e:
        print(f"Warning: query generation failed ({e}), using topic directly", file=sys.stderr)
        queries = [{"type": "direct", "query": topic, "rationale": "Fallback"}]

    query_texts = [q["query"] for q in queries]
    print(f"Generated {len(query_texts)} queries: {query_texts[:3]}...", file=sys.stderr)

    # ── Step 2: Parallel search across all sources ─────────────────────────
    all_raw_results = []
    source_stats = {}

    for source_type in sources:
        source_class = SOURCE_REGISTRY.get(source_type)
        if not source_class:
            print(f"Warning: unknown source type '{source_type}'", file=sys.stderr)
            continue

        source = source_class()
        source_queries = _adapt_queries_for_source(queries, source_type, topic)

        # Run queries in parallel (up to 3 concurrent)
        source_results = _parallel_search(
            source,
            source_queries,
            max_results_per_source=max_results_per_source,
            max_workers=MAX_PARALLEL_SEARCHES,
            timeout=SEARCH_TIMEOUT,
        )

        source_stats[source_type] = {
            "queries_run": len(source_queries),
            "results_found": len(source_results),
        }
        all_raw_results.extend(source_results)

    print(f"Collected {len(all_raw_results)} raw results from {len(sources)} sources", file=sys.stderr)

    if not all_raw_results:
        return {
            "status": "no_results",
            "topic": topic,
            "findings": [],
            "sources": [],
            "gaps": [{"question": topic, "reason": "No results found from any source"}],
            "metadata": {
                "queries": query_texts,
                "source_stats": source_stats,
                "elapsed_seconds": round(time.time() - start_time, 1),
            },
        }

    # ── Step 3: Deduplicate by URL ─────────────────────────────────────────
    deduped = deduplicate_results(all_raw_results)
    print(f"After dedup: {len(deduped)} unique results", file=sys.stderr)

    # ── Step 4: Score by relevance ────────────────────────────────────────
    scored = score_results(deduped, topic, use_llm=_has_llm_config())

    relevant = [r for r in scored if r.get("relevance_score", 0) >= min_relevance]
    print(f"After relevance filter (>= {min_relevance}): {len(relevant)} results", file=sys.stderr)

    if not relevant:
        relevant = sorted(scored, key=lambda x: x.get("relevance_score", 0), reverse=True)[:5]
        print(f"Relaxed to top {len(relevant)} results", file=sys.stderr)

    # ── Step 5: LLM chunk selection (threshold >= 0.7) ─────────────────────
    if use_chunk_selector and len(relevant) > 3:
        try:
            selected = select_relevant_chunks(
                topic, relevant,
                min_score=CHUNK_SELECTOR_THRESHOLD,
                max_context_tokens=12000,
            )
            print(f"Chunk selector (>= {CHUNK_SELECTOR_THRESHOLD}): {len(selected)} of {len(relevant)} passed", file=sys.stderr)
        except Exception as e:
            print(f"Warning: chunk selection failed ({e}), using all relevant", file=sys.stderr)
            selected = relevant
    else:
        selected = relevant

    if not selected and relevant:
        # If all were filtered out, keep the top 3
        selected = sorted(relevant, key=lambda x: x.get("relevance_score", 0), reverse=True)[:3]
        print(f"Chunk selector filtered everything, kept top {len(selected)} by relevance", file=sys.stderr)

    # ── Step 6: Context expansion for incomplete chunks ────────────────────
    if use_context_expander and len(selected) > 0:
        try:
            expanded = expand_context(selected, topic, max_expansions=5)
            print(f"Context expansion: {sum(1 for c in expanded if c.get('expanded'))} expanded", file=sys.stderr)
        except Exception as e:
            print(f"Warning: context expansion failed ({e})", file=sys.stderr)
            expanded = selected
    else:
        expanded = selected

    # ── Step 7: Extract structured findings ───────────────────────────────
    findings = _extract_findings(expanded, topic)
    gaps = _identify_gaps(expanded, topic, findings)

    # ── Step 8: Build output ──────────────────────────────────────────────
    sources_output = []
    seen_source_urls = set()
    for r in expanded:
        url = r.get("url", "")
        if url and url not in seen_source_urls:
            seen_source_urls.add(url)
            sources_output.append({
                "title": r.get("title", ""),
                "url": url,
                "source_type": r.get("source_type", "unknown"),
                "relevance_score": r.get("relevance_score", 0),
                "relevance_reason": r.get("relevance_reason", ""),
                "expanded": r.get("expanded", False),
            })

    elapsed = round(time.time() - start_time, 1)

    return {
        "status": "complete" if findings else "partial",
        "topic": topic,
        "findings": findings,
        "sources": sources_output,
        "gaps": gaps,
        "metadata": {
            "queries_generated": len(queries),
            "queries": query_texts,
            "raw_results": len(all_raw_results),
            "after_dedup": len(deduped),
            "after_scoring": len(relevant),
            "after_chunk_selection": len(selected),
            "after_expansion": len(expanded),
            "source_stats": source_stats,
            "elapsed_seconds": elapsed,
        },
    }


# ─── Dimension-based research ─────────────────────────────────────────────────


def research_dimension(
    dimension: str,
    questions: list[str],
    sources: Optional[list[str]] = None,
    max_queries_per_question: int = 3,
    max_results_per_source: int = 5,
    min_relevance: float = 0.4,
    use_chunk_selector: bool = True,
    use_context_expander: bool = True,
    api_key: Optional[str] = None,
) -> dict:
    """Research a specific dimension of a topic with multiple questions.

    This is the key function for sessions_spawn subagents. Each subagent
    gets a dimension (e.g., "architecture", "market_analysis", "risks") and
    a list of questions to answer. Returns structured findings.

    Args:
        dimension: The research dimension name (e.g., "architecture", "market", "risks").
        questions: List of specific questions to research within this dimension.
        sources: Source types to search (default: ["web", "github", "docs"]).
        max_queries_per_question: Search variants per question (3-5 recommended).
        max_results_per_source: Max results per source per query.
        min_relevance: Minimum relevance score for results.
        use_chunk_selector: Run LLM-based chunk filtering.
        use_context_expander: Expand context for incomplete chunks.
        api_key: Optional ZAI_API_KEY override.

    Returns:
        Dict with:
            - dimension: str
            - questions: list[str]
            - findings: list[dict] with claim, source_url, source_title,
                        confidence, category, supporting_question
            - sources: list[dict] with url, title, relevance_score
            - coverage: float (0.0-1.0, how well questions were answered)
            - metadata: pipeline stats
    """
    if api_key:
        os.environ["ZAI_API_KEY"] = api_key

    start_time = time.time()
    sources = sources or ["web", "github", "docs"]
    all_findings = []
    all_sources = []
    seen_urls = set()
    question_coverage = {}
    total_queries = 0
    total_raw = 0

    for question in questions:
        q_start = time.time()
        print(f"\n── Researching: [{dimension}] {question[:80]} ──", file=sys.stderr)

        # 1. Generate 3-5 query variants for this question
        try:
            queries = generate_queries(question, max_queries=max_queries_per_question)
        except Exception as e:
            print(f"  Warning: query gen failed ({e})", file=sys.stderr)
            queries = [{"type": "direct", "query": question, "rationale": "Fallback"}]

        total_queries += len(queries)

        # 2. Parallel search across sources
        question_results = []
        for source_type in sources:
            source_class = SOURCE_REGISTRY.get(source_type)
            if not source_class:
                continue
            source = source_class()
            source_queries = _adapt_queries_for_source(queries, source_type, question)

            results = _parallel_search(
                source,
                source_queries,
                max_results_per_source=max_results_per_source,
                max_workers=MAX_PARALLEL_SEARCHES,
                timeout=SEARCH_TIMEOUT,
            )
            question_results.extend(results)

        total_raw += len(question_results)

        if not question_results:
            question_coverage[question] = {"covered": False, "reason": "No results"}
            continue

        # 3. Deduplicate by URL
        deduped = deduplicate_results(question_results)

        # 4. Score and filter
        scored = score_results(deduped, question, use_llm=_has_llm_config())
        relevant = [r for r in scored if r.get("relevance_score", 0) >= min_relevance]
        if not relevant:
            relevant = sorted(scored, key=lambda x: x.get("relevance_score", 0), reverse=True)[:3]

        # 5. LLM chunk selection (threshold >= 0.7)
        if use_chunk_selector and len(relevant) > 2:
            try:
                selected = select_relevant_chunks(
                    question, relevant,
                    min_score=CHUNK_SELECTOR_THRESHOLD,
                    max_context_tokens=10000,
                )
            except Exception:
                selected = relevant
        else:
            selected = relevant

        if not selected and relevant:
            selected = sorted(relevant, key=lambda x: x.get("relevance_score", 0), reverse=True)[:2]

        # 6. Context expansion
        if use_context_expander and len(selected) > 0:
            try:
                expanded = expand_context(selected, question, max_expansions=3)
            except Exception:
                expanded = selected
        else:
            expanded = selected

        # 7. Extract findings for this question
        findings = _extract_findings(expanded, question)

        # Tag each finding with the dimension and question
        for f in findings:
            f["dimension"] = dimension
            f["supporting_question"] = question

        all_findings.extend(findings)

        # Collect unique sources
        for r in expanded:
            url = r.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                all_sources.append({
                    "title": r.get("title", ""),
                    "url": url,
                    "source_type": r.get("source_type", "unknown"),
                    "relevance_score": r.get("relevance_score", 0),
                    "relevance_reason": r.get("relevance_reason", ""),
                })

        question_coverage[question] = {
            "covered": len(findings) > 0,
            "findings_count": len(findings),
            "elapsed": round(time.time() - q_start, 1),
        }

        print(f"  → {len(findings)} findings in {round(time.time() - q_start, 1)}s", file=sys.stderr)

    # Calculate coverage score
    covered = sum(1 for v in question_coverage.values() if v.get("covered", False))
    coverage = round(covered / max(1, len(questions)), 2)

    elapsed = round(time.time() - start_time, 1)

    return {
        "dimension": dimension,
        "questions": questions,
        "findings": all_findings,
        "sources": all_sources,
        "coverage": coverage,
        "question_coverage": question_coverage,
        "metadata": {
            "total_queries": total_queries,
            "total_raw_results": total_raw,
            "total_findings": len(all_findings),
            "unique_sources": len(all_sources),
            "elapsed_seconds": elapsed,
        },
    }


# ─── Finding extraction ──────────────────────────────────────────────────────


def _extract_findings(chunks: list[dict], topic: str) -> list[dict]:
    """Use LLM to extract structured findings from processed chunks."""
    if not chunks:
        return []

    if not _has_llm_config():
        return _extract_findings_simple(chunks, topic)

    system = (
        "You are a research analyst. Extract key findings from the provided source chunks. "
        "Each finding must be directly supported by the source text.\n\n"
        "Output ONLY a JSON array. Each finding:\n"
        '{"claim": "...", "source_url": "...", "source_title": "...", '
        '"confidence": 0.0-1.0, "category": "technical|concept|comparison|data|opinion"}\n\n'
        "Rules:\n"
        "- Only include claims directly supported by source text\n"
        "- Never fabricate or extrapolate beyond what's stated\n"
        "- confidence 1.0 = directly stated, 0.8 = strongly implied, 0.6 = inferred\n"
        "- Group similar findings into single claims with multiple sources\n"
        "- Maximum 15 findings"
    )

    chunks_text = []
    total_chars = 0
    MAX_CHARS = 20000

    for c in chunks:
        content = c.get("content", "")[:2000]
        chunk_str = f"[{c.get('url', 'unknown')}] {c.get('title', 'Untitled')}\n{content}"
        if total_chars + len(chunk_str) > MAX_CHARS:
            break
        chunks_text.append(chunk_str)
        total_chars += len(chunk_str)

    prompt = (
        f"Research topic: {topic}\n\n"
        f"Source chunks:\n{chr(10).join(chunks_text)}\n\n"
        "Extract findings. Output JSON array only."
    )

    try:
        response = _call_glm(prompt, system, max_tokens=4096, temperature=0.2)
        findings = _parse_json_response(response)
        if not isinstance(findings, list):
            findings = [findings]
        return findings[:20]
    except Exception as e:
        print(f"Warning: finding extraction failed ({e})", file=sys.stderr)
        return _extract_findings_simple(chunks, topic)


def _extract_findings_simple(chunks: list[dict], topic: str) -> list[dict]:
    """Simple rule-based finding extraction (fallback when no API key)."""
    findings = []
    for c in chunks:
        content = c.get("content", "")
        if not content or len(content) < 50:
            continue

        sentences = [s.strip() for s in content.replace("\n", ".").split(".") if len(s.strip()) > 20]
        for sentence in sentences[:2]:
            findings.append({
                "claim": sentence,
                "source_url": c.get("url", ""),
                "source_title": c.get("title", ""),
                "confidence": 0.5,
                "category": "extracted",
            })

    return findings[:15]


# ─── Gap identification ──────────────────────────────────────────────────────


def _identify_gaps(
    chunks: list[dict], topic: str, findings: list[dict]
) -> list[dict]:
    """Identify research gaps based on what was found vs. what the topic needs."""
    if not _has_llm_config() or not findings:
        return _identify_gaps_simple(topic, chunks, findings)

    system = (
        "You are a research gap analyzer. Given a research topic and the findings "
        "so far, identify what important aspects are missing or under-explored.\n\n"
        "Output ONLY a JSON array:\n"
        '[{"question": "...", "reason": "...", "importance": "high|medium|low"}]\n\n'
        "Rules:\n"
        "- Focus on gaps that would significantly improve understanding of the topic\n"
        "- Don't list things that are adequately covered by findings\n"
        "- Maximum 5 gaps\n"
        "- If findings are comprehensive, return empty array"
    )

    findings_summary = json.dumps(
        [{"claim": f.get("claim", "")[:200]} for f in findings[:10]],
        ensure_ascii=False,
    )

    prompt = (
        f"Research topic: {topic}\n\n"
        f"Findings so far ({len(findings)}):\n{findings_summary}\n\n"
        "What important aspects are still missing?"
    )

    try:
        response = _call_glm(prompt, system, max_tokens=2048, temperature=0.3)
        gaps = _parse_json_response(response)
        if not isinstance(gaps, list):
            gaps = [gaps]
        return gaps[:5]
    except Exception:
        return _identify_gaps_simple(topic, chunks, findings)


def _identify_gaps_simple(
    topic: str, chunks: list[dict], findings: list[dict]
) -> list[dict]:
    """Simple gap identification based on coverage heuristics."""
    gaps = []
    topic_lower = topic.lower()

    source_types = set(c.get("source_type", "") for c in chunks)
    if len(source_types) < 2:
        gaps.append({
            "question": f"Diversify sources for: {topic}",
            "reason": f"Only {len(source_types)} source type(s) used ({', '.join(source_types)})",
            "importance": "medium",
        })

    if len(findings) < 3:
        gaps.append({
            "question": f"More information needed on: {topic}",
            "reason": f"Only {len(findings)} finding(s) extracted",
            "importance": "high",
        })

    aspects = {
        "comparison": any(w in topic_lower for w in ["vs", "compare", "alternative", "difference"]),
        "how_to": any(w in topic_lower for w in ["how", "guide", "tutorial", "setup", "install"]),
        "technical": any(w in topic_lower for w in ["architecture", "implementation", "code", "api"]),
    }

    if aspects["comparison"] and len(findings) < 5:
        gaps.append({
            "question": f"Detailed comparison analysis for: {topic}",
            "reason": "Comparison topic but limited findings",
            "importance": "high",
        })

    if not aspects["comparison"] and not any("overview" in f.get("claim", "").lower() for f in findings):
        gaps.append({
            "question": f"High-level overview of: {topic}",
            "reason": "No overview/broad-context finding identified",
            "importance": "medium",
        })

    return gaps


# ─── Save helpers ─────────────────────────────────────────────────────────────


def save_research(output: dict, output_dir: str) -> str:
    """Save research output to files."""
    import os
    os.makedirs(output_dir, exist_ok=True)

    json_path = os.path.join(output_dir, "researcher-output.json")
    with open(json_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    md_path = os.path.join(output_dir, "research-summary.md")
    md = f"# Research: {output.get('topic', output.get('dimension', 'Unknown'))}\n\n"
    md += f"**Status:** {output.get('status', output.get('coverage', 'N/A'))}\n"
    md += f"**Findings:** {len(output.get('findings', []))}\n"
    md += f"**Sources:** {len(output.get('sources', []))}\n"
    md += f"**Gaps:** {len(output.get('gaps', []))}\n"

    meta = output.get("metadata", {})
    md += f"\n## Metadata\n"
    md += f"- Queries: {meta.get('queries_generated', meta.get('total_queries', 0))}\n"
    md += f"- Raw results: {meta.get('raw_results', meta.get('total_raw_results', 0))}\n"
    md += f"- After dedup: {meta.get('after_dedup', 'N/A')}\n"
    md += f"- After scoring: {meta.get('after_scoring', 'N/A')}\n"
    md += f"- Elapsed: {meta.get('elapsed_seconds', 0)}s\n"

    if output.get("findings"):
        md += "\n## Findings\n\n"
        for i, f in enumerate(output["findings"], 1):
            md += f"### {i}. {f.get('claim', '?')[:100]}\n\n"
            md += f"- **Source:** [{f.get('source_title', '?')}]({f.get('source_url', '#')})\n"
            md += f"- **Confidence:** {f.get('confidence', '?')}\n"
            md += f"- **Category:** {f.get('category', '?')}\n"
            dim = f.get("dimension", "")
            if dim:
                md += f"- **Dimension:** {dim}\n"
            sq = f.get("supporting_question", "")
            if sq:
                md += f"- **Question:** {sq}\n"
            md += "\n"

    if output.get("sources"):
        md += "## Sources\n\n"
        for s in output["sources"]:
            md += f"- [{s.get('title', '?')}]({s.get('url', '#')}) "
            md += f"(score: {s.get('relevance_score', '?')}, type: {s.get('source_type', '?')})\n"

    if output.get("gaps"):
        md += "\n## Gaps\n\n"
        for g in output["gaps"]:
            md += f"- **{g.get('question', '?')}** ({g.get('importance', '?')}): {g.get('reason', '')}\n"

    if output.get("question_coverage"):
        md += "\n## Question Coverage\n\n"
        for q, cov in output["question_coverage"].items():
            status = "✅" if cov.get("covered") else "❌"
            md += f"- {status} {q} ({cov.get('findings_count', 0)} findings, {cov.get('elapsed', '?')}s)\n"

    with open(md_path, "w") as f:
        f.write(md)

    return json_path


# ─── CLI ──────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Researcher Agent — multi-source research orchestration"
    )
    parser.add_argument("topic", nargs="?", help="Research topic or question")
    parser.add_argument("--stdin", action="store_true", help="Read topic from stdin JSON")
    parser.add_argument(
        "--sources", "-s",
        nargs="+",
        choices=["web", "github", "docs"],
        default=["web", "github", "docs"],
        help="Source types to search (default: all)",
    )
    parser.add_argument("--limit", "-n", type=int, default=5, help="Max results per source")
    parser.add_argument("--max-queries", type=int, default=5)
    parser.add_argument("--min-relevance", type=float, default=0.4)
    parser.add_argument("--no-chunk-selector", action="store_true", help="Skip chunk selection")
    parser.add_argument("--no-context-expander", action="store_true", help="Skip context expansion")
    parser.add_argument("--output-dir", "-o", help="Directory to save results")
    args = parser.parse_args()

    # Get topic
    if args.stdin:
        data = json.load(sys.stdin)
        topic = data.get("topic", data.get("question", data.get("q", "")))
    elif args.topic:
        topic = args.topic
    else:
        print("Error: provide a topic or use --stdin", file=sys.stderr)
        sys.exit(1)

    if not topic:
        print("Error: empty topic", file=sys.stderr)
        sys.exit(1)

    # Run research
    output = research(
        topic=topic,
        sources=args.sources,
        max_queries=args.max_queries,
        max_results_per_source=args.limit,
        min_relevance=args.min_relevance,
        use_chunk_selector=not args.no_chunk_selector,
        use_context_expander=not args.no_context_expander,
    )

    # Save if output dir specified
    if args.output_dir:
        path = save_research(output, args.output_dir)
        print(f"Saved to {path}", file=sys.stderr)

    # Print JSON output
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
