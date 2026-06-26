"""Research Pipeline CLI — Enhanced with progress, checkpoints, budget, and parallel research.

Enhanced version of research_pipeline.py with:
- Progress reporting to stdout
- Resume from checkpoint if interrupted
- Budget awareness (token count, time limit)
- Parallel dimension research using ThreadPoolExecutor
- Output to file with --output flag

Usage:
    # Full pipeline with defaults
    python3 research_pipeline.py "What is quantum computing?" --max-cycles 3 --output report.md

    # Mock mode (no API calls)
    python3 research_pipeline.py "test question" --mock --output report.md

    # Resume from checkpoint
    python3 research_pipeline.py "test question" --resume checkpoint.json --output report.md

    # With budget limits
    python3 research_pipeline.py "question" --max-cycles 3 --time-limit 300 --token-limit 40000

    # Subcommand mode (backward compatible)
    python3 research_pipeline.py researcher --question "..." --dimension "..."
    python3 research_pipeline.py analyst --input researcher_output.json
    python3 research_pipeline.py writer --input analyst_output.json --question "..."
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

from llm_client import call_llm as _call_glm

# Reuse existing scripts
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from query_generator import generate_queries
from chunk_selector import select_relevant_chunks
from context_expander import expand_context
from reflection import ResearchPlan, ReflectionResult, reflect
from writer import WriterAgent, write_report, OutputFormat, save_report

def _parse_json_response(text: str) -> any:
    """Parse JSON from LLM, stripping markdown fences."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(text)


def _estimate_tokens(obj: any) -> int:
    """Cheap token proxy: ~4 chars/token."""
    try:
        s = json.dumps(obj, ensure_ascii=False)
    except Exception:
        s = str(obj)
    return max(1, len(s) // 4)


def _progress(message: str) -> None:
    """Print progress message to stdout."""
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)


def _save_checkpoint(data: dict, path: str) -> None:
    """Save pipeline state to a checkpoint file."""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    data["checkpoint_saved_at"] = time.time()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _load_checkpoint(path: str) -> Optional[dict]:
    """Load pipeline state from a checkpoint file."""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


# ─── RESEARCHER ───────────────────────────────────────────────────────────────


def _web_fetch(url: str) -> Optional[str]:
    """Fetch a URL and return text content."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)"},
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            content_type = resp.headers.get("Content-Type", "")
            if "text" not in content_type and "json" not in content_type:
                return None
            return resp.read(30000).decode(errors="replace")
    except Exception:
        return None


def run_researcher(
    question: str,
    dimension: str,
    specific_questions: list[str],
    max_sources: int = 10,
    search_results: Optional[list[dict]] = None,
) -> dict:
    """Orchestrate: query_generator → search → fetch → chunk_selector → context_expander."""
    combined_q = f"{question} — {dimension}: {', '.join(specific_questions)}"
    queries = generate_queries(combined_q, max_queries=5)

    if search_results is None:
        return {
            "status": "queries_ready",
            "dimension": dimension,
            "queries": queries,
            "specific_questions": specific_questions,
            "message": "Run searches with these queries, then call _run_researcher_with_results()",
        }

    chunks = []
    for result in search_results[:max_sources]:
        url = result.get("url", "")
        content = result.get("content") or _web_fetch(url)
        if content:
            chunks.append(
                {
                    "url": url,
                    "title": result.get("title", ""),
                    "content": content,
                }
            )

    if not chunks:
        return {
            "status": "no_content",
            "dimension": dimension,
            "queries": queries,
            "findings": [],
            "sources": [],
        }

    selected = select_relevant_chunks(question, chunks, min_score=0.7)
    expanded = expand_context(selected, question, max_expansions=5)
    findings = _extract_findings(expanded, question, dimension, specific_questions)

    return {
        "status": "complete",
        "dimension": dimension,
        "queries": [q["query"] for q in queries],
        "findings": findings,
        "sources": [
            {"url": c["url"], "title": c.get("title", ""), "score": c.get("score", 0)}
            for c in expanded
        ],
        "metadata": {
            "chunks_scanned": len(chunks),
            "chunks_selected": len(selected),
            "chunks_expanded": sum(1 for c in expanded if c.get("expanded")),
        },
    }


def _extract_findings(
    chunks: list[dict], question: str, dimension: str, specific_questions: list[str]
) -> list[dict]:
    """Use LLM to extract structured findings from selected chunks."""
    system = (
        "You are a research analyst. Extract key findings from the provided source chunks. "
        "Each finding must be directly supported by the source text.\n\n"
        "Output ONLY a JSON array. Each finding:\n"
        '{"claim": "...", "source_url": "...", "confidence": 0.0-1.0, '
        '"answers_question": "which question this addresses"}\n\n'
        "Rules:\n"
        "- Only include claims directly supported by source text\n"
        "- Never fabricate or extrapolate\n"
        "- confidence 1.0 = directly stated, 0.7 = strongly implied, 0.5 = inferred"
    )

    chunks_text = "\n\n---\n\n".join(
        f"[{c.get('url', 'unknown')}]\n{c.get('content', '')[:3000]}" for c in chunks
    )

    prompt = (
        f"Research question: {question}\n"
        f"Dimension: {dimension}\n"
        f"Target questions: {json.dumps(specific_questions)}\n\n"
        f"Source chunks:\n{chunks_text}\n\n"
        "Extract findings."
    )

    try:
        response = _call_glm(prompt, system, max_tokens=4096)
        findings = _parse_json_response(response)
        if not isinstance(findings, list):
            findings = [findings]
        return findings
    except Exception as e:
        print(f"Warning: finding extraction failed ({e})", file=sys.stderr)
        return []


# ─── ANALYST ──────────────────────────────────────────────────────────────────


def run_analyst(researcher_outputs: list[dict]) -> dict:
    """Deduplicate findings, flag contradictions, group into themes, identify gaps."""
    all_findings = []
    for output in researcher_outputs:
        all_findings.extend(output.get("findings", []))

    if not all_findings:
        return {
            "status": "no_findings",
            "themes": [],
            "contradictions": [],
            "gaps": [],
            "merged_findings": [],
        }

    system = (
        "You are a research synthesis analyst. Analyze the collected findings.\n\n"
        "Tasks:\n"
        "1. Deduplicate overlapping findings\n"
        "2. Flag contradictions (explicit disagreements between sources)\n"
        "3. Group findings into thematic clusters\n"
        "4. Identify knowledge gaps (important questions left unanswered)\n\n"
        "Output ONLY JSON:\n"
        "{\n"
        '  "themes": [{"name": "...", "findings": [...], "confidence": 0.0-1.0, '
        '"key_claims": ["..."]}],\n'
        '  "contradictions": [{"claim_a": "...", "claim_b": "...", '
        '"source_a": "...", "source_b": "...", "resolution": "..."}],\n'
        '  "gaps": [{"question": "...", "importance": "high|medium|low", '
        '"suggested_search": "..."}],\n'
        '  "merged_findings": [{"claim": "...", "sources": ["url1", "url2"], '
        '"confidence": 0.0-1.0, "theme": "...", "dimension": "..."}]\n'
        "}"
    )

    BATCH_SIZE = 15

    if len(all_findings) <= BATCH_SIZE:
        findings_text = json.dumps(all_findings, indent=2, ensure_ascii=False)
        prompt = f"Analyze these research findings:\n\n{findings_text}"
        try:
            response = _call_glm(prompt, system, max_tokens=8000)
            result = _parse_json_response(response)
            return {
                "status": "complete",
                **result,
                "input_dimensions": [
                    o.get("dimension", "unknown") for o in researcher_outputs
                ],
                "total_findings_input": len(all_findings),
            }
        except Exception as e:
            print(f"Warning: analysis failed ({e})", file=sys.stderr)
            return _analyst_fallback(all_findings)

    batch_results = []
    for i in range(0, len(all_findings), BATCH_SIZE):
        batch = all_findings[i : i + BATCH_SIZE]
        findings_text = json.dumps(batch, indent=2, ensure_ascii=False)
        prompt = f"Analyze these research findings (batch {i // BATCH_SIZE + 1}):\n\n{findings_text}"
        try:
            response = _call_glm(prompt, system, max_tokens=8000)
            batch_result = _parse_json_response(response)
            batch_results.append(batch_result)
        except Exception as e:
            print(f"Warning: batch {i // BATCH_SIZE + 1} failed ({e})", file=sys.stderr)
            batch_results.append(
                {
                    "merged_findings": batch,
                    "themes": [],
                    "contradictions": [],
                    "gaps": [],
                }
            )

    all_merged = []
    all_themes = []
    all_contradictions = []
    all_gaps = []
    for br in batch_results:
        all_merged.extend(br.get("merged_findings", []))
        all_themes.extend(br.get("themes", []))
        all_contradictions.extend(br.get("contradictions", []))
        all_gaps.extend(br.get("gaps", []))

    return {
        "status": "complete_batched",
        "themes": all_themes,
        "contradictions": all_contradictions,
        "gaps": all_gaps,
        "merged_findings": all_merged,
        "input_dimensions": [o.get("dimension", "unknown") for o in researcher_outputs],
        "total_findings_input": len(all_findings),
        "batches_processed": len(batch_results),
    }


def _analyst_fallback(all_findings: list[dict]) -> dict:
    """Simple dedup fallback when LLM analysis fails."""
    seen = set()
    merged = []
    for f in all_findings:
        key = f.get("claim", "")[:100].lower()
        if key not in seen:
            seen.add(key)
            merged.append(
                {**f, "sources": [f.get("source_url", "")], "theme": "unclassified"}
            )
    return {
        "status": "fallback",
        "themes": [],
        "contradictions": [],
        "gaps": [],
        "merged_findings": merged,
    }


# ─── Writer (using the new WriterAgent) ───────────────────────────────────────


def run_writer(analyst_output: dict, question: str) -> dict:
    """Generate polished markdown report using WriterAgent."""
    agent = WriterAgent(use_llm=True)
    result = agent.write_report(analyst_output, question, OutputFormat.REPORT)
    return result


# ─── Plan creation ────────────────────────────────────────────────────────────


def _create_plan(
    question: str,
    dimensions: Optional[list[str]] = None,
    budget_seconds: int = 900,
    budget_tokens: int = 60000,
) -> ResearchPlan:
    """Create a ResearchPlan from a question."""
    if not dimensions:
        try:
            queries = generate_queries(question, max_queries=5)
            dimensions = [q.get("query", f"dim_{i}") for i, q in enumerate(queries)]
        except Exception:
            dimensions = ["overview", "key findings", "evidence"]

    dim_questions = {d: [question] for d in dimensions}
    return ResearchPlan(
        question=question,
        dimensions=dimensions,
        dimension_questions=dim_questions,
        budget_seconds=budget_seconds,
        budget_tokens=budget_tokens,
    )


# ─── Parallel dimension research ──────────────────────────────────────────────


def _research_dimension_parallel(
    question: str,
    dimension: str,
    questions: list[str],
    search_results: Optional[dict[str, list[dict]]],
    mock_mode: bool,
) -> dict:
    """Research a single dimension (runs in a thread)."""
    if mock_mode:
        return {
            "status": "complete",
            "dimension": dimension,
            "queries": [f"mock query for {dimension}"],
            "findings": [
                {
                    "claim": f"Mock finding for {dimension}",
                    "source_url": "https://example.com/mock",
                    "confidence": 0.75,
                    "answers_question": question,
                    "dimension": dimension,
                }
            ],
            "sources": [{"url": "https://example.com/mock", "title": dimension, "score": 0.7}],
            "metadata": {"chunks_scanned": 1, "chunks_selected": 1, "chunks_expanded": 0},
        }

    sr = (search_results or {}).get(dimension)
    return run_researcher(question, dimension, questions, search_results=sr)


# ─── Enhanced looping pipeline ────────────────────────────────────────────────


def run_enhanced_pipeline(
    question: str,
    max_cycles: int = 3,
    dimensions: Optional[list[str]] = None,
    search_results: Optional[dict[str, list[dict]]] = None,
    mock_mode: bool = False,
    output_format: str = "report",
    time_limit: Optional[int] = None,
    token_limit: Optional[int] = None,
    checkpoint_path: Optional[str] = None,
    resume_from: Optional[str] = None,
    parallel_dimensions: bool = True,
) -> dict:
    """Run the full research pipeline with progress, checkpoints, and budget awareness.

    Pipeline: plan -> [research -> analyze -> reflect] x N -> write

    Args:
        question: The research question.
        max_cycles: Maximum research cycles (1-8).
        dimensions: Optional explicit dimensions.
        search_results: Dict mapping dimension -> search results.
        mock_mode: Use mock data instead of real API calls.
        output_format: Report format (report, summary, brief, json).
        time_limit: Max seconds for the entire pipeline (default: 900).
        token_limit: Max estimated tokens (default: 60000).
        checkpoint_path: Path to save checkpoints (default: no checkpointing).
        resume_from: Path to resume from a checkpoint file.
        parallel_dimensions: Research dimensions in parallel (default: True).

    Returns:
        Dict with final report, cycle history, and metadata.
    """
    max_cycles = min(max_cycles, 8)
    budget_seconds = time_limit or 900
    budget_tokens = token_limit or 60000
    start_time = time.time()

    # ── Resume from checkpoint ──
    if resume_from:
        checkpoint = _load_checkpoint(resume_from)
        if checkpoint:
            _progress(f"Resuming from checkpoint: {resume_from}")
            cycle_history = checkpoint.get("cycle_history", [])
            all_researcher_outputs = checkpoint.get("all_researcher_outputs", [])
            plan_data = checkpoint.get("plan", {})
            plan = ResearchPlan(
                question=plan_data.get("question", question),
                dimensions=plan_data.get("dimensions", dimensions or ["overview"]),
                dimension_questions=plan_data.get("dimension_questions", {}),
                budget_seconds=plan_data.get("budget_seconds", budget_seconds),
                budget_tokens=plan_data.get("budget_tokens", budget_tokens),
                created_at_unix=plan_data.get("created_at_unix", start_time),
            )
            start_cycle = len(cycle_history) + 1
            _progress(f"Resuming from cycle {start_cycle}, {len(cycle_history)} cycles completed")
        else:
            _progress(f"Checkpoint not found: {resume_from}, starting fresh")
            plan = _create_plan(question, dimensions, budget_seconds, budget_tokens)
            cycle_history = []
            all_researcher_outputs = []
            start_cycle = 1
    else:
        plan = _create_plan(question, dimensions, budget_seconds, budget_tokens)
        cycle_history = []
        all_researcher_outputs = []
        start_cycle = 1

    _progress(f"Research question: {question}")
    _progress(f"Dimensions: {plan.dimensions}")
    _progress(f"Budget: {budget_seconds}s / {budget_tokens} tokens")
    _progress(f"Max cycles: {max_cycles}")

    if checkpoint_path:
        _progress(f"Checkpoints: {checkpoint_path}")

    for cycle in range(start_cycle, max_cycles + 1):
        elapsed = time.time() - start_time
        if elapsed >= budget_seconds * 0.95:
            _progress(f"⚠️ Time budget reached ({elapsed:.0f}s / {budget_seconds}s), stopping")
            break

        cycle_data = {"cycle": cycle, "start_time": time.time()}
        _progress(f"━━━ Cycle {cycle}/{max_cycles} ━━━")

        # Determine target dimensions
        if cycle == 1:
            target_dims = plan.dimensions
        else:
            prev_reflection = cycle_history[-1].get("reflection", {})
            target_dims = prev_reflection.get("next_dimensions", [])
            if not target_dims:
                target_dims = plan.dimensions

        _progress(f"Researching dimensions: {target_dims}")

        # ── Research phase (parallel if enabled) ──
        cycle_researcher_outputs = []

        if parallel_dimensions and len(target_dims) > 1 and not mock_mode:
            _progress(f"Researching {len(target_dims)} dimensions in parallel...")
            with ThreadPoolExecutor(max_workers=min(3, len(target_dims))) as executor:
                futures = {}
                for dim in target_dims:
                    questions = plan.dimension_questions.get(dim, [question])
                    future = executor.submit(
                        _research_dimension_parallel,
                        question, dim, questions, search_results, mock_mode,
                    )
                    futures[future] = dim

                for future in as_completed(futures, timeout=120):
                    dim = futures[future]
                    try:
                        result = future.result(timeout=120)
                        cycle_researcher_outputs.append(result)
                        status = result.get("status", "?")
                        n_findings = len(result.get("findings", []))
                        _progress(f"  ✓ {dim}: {status} ({n_findings} findings)")
                    except Exception as e:
                        _progress(f"  ✗ {dim}: FAILED ({e})")
                        cycle_researcher_outputs.append({
                            "status": "error",
                            "dimension": dim,
                            "findings": [],
                            "error": str(e),
                        })
        else:
            for dim in target_dims:
                _progress(f"  Researching: {dim}...")
                try:
                    result = _research_dimension_parallel(
                        question, dim,
                        plan.dimension_questions.get(dim, [question]),
                        search_results, mock_mode,
                    )
                    cycle_researcher_outputs.append(result)
                    status = result.get("status", "?")
                    n_findings = len(result.get("findings", []))
                    _progress(f"  ✓ {dim}: {status} ({n_findings} findings)")
                except Exception as e:
                    _progress(f"  ✗ {dim}: FAILED ({e})")
                    cycle_researcher_outputs.append({
                        "status": "error",
                        "dimension": dim,
                        "findings": [],
                        "error": str(e),
                    })

        all_researcher_outputs.extend(cycle_researcher_outputs)
        cycle_data["researcher_outputs"] = cycle_researcher_outputs

        # ── Budget check after research ──
        all_tokens = _estimate_tokens(all_researcher_outputs)
        if all_tokens >= budget_tokens * 0.95:
            _progress(f"⚠️ Token budget reached ({all_tokens} / {budget_tokens}), stopping")
            break

        # ── Analyze phase ──
        _progress("  Analyzing findings...")
        if mock_mode:
            merged = []
            for ro in cycle_researcher_outputs:
                merged.extend(ro.get("findings", []))
            analyst_out = {
                "status": "complete",
                "themes": [{"name": d, "confidence": 0.75, "key_claims": []} for d in target_dims],
                "contradictions": [],
                "gaps": [],
                "merged_findings": merged,
            }
        else:
            analyst_out = run_analyst(cycle_researcher_outputs)

        n_themes = len(analyst_out.get("themes", []))
        n_merged = len(analyst_out.get("merged_findings", []))
        _progress(f"  Analysis: {n_themes} themes, {n_merged} merged findings")
        cycle_data["analyst_output"] = analyst_out

        # ── Reflect phase ──
        findings_for_reflection = analyst_out.get("merged_findings", [])
        reflection_result = reflect(plan, findings_for_reflection, cycle, max_cycles)
        cycle_data["reflection"] = {
            "should_continue": reflection_result.should_continue,
            "gaps": reflection_result.gaps,
            "coverage_score": reflection_result.coverage_score,
            "next_dimensions": reflection_result.next_dimensions,
            "summary": reflection_result.summary,
        }

        cycle_data["end_time"] = time.time()
        cycle_data["duration_seconds"] = round(cycle_data["end_time"] - cycle_data["start_time"], 2)
        cycle_history.append(cycle_data)

        _progress(
            f"  Cycle {cycle} complete: coverage={reflection_result.coverage_score:.0%} "
            f"findings={n_merged} duration={cycle_data['duration_seconds']}s"
        )

        if reflection_result.gaps:
            _progress(f"  Gaps: {', '.join(reflection_result.gaps[:3])}")

        # ── Save checkpoint ──
        if checkpoint_path:
            checkpoint_data = {
                "plan": {
                    "question": plan.question,
                    "dimensions": plan.dimensions,
                    "dimension_questions": plan.dimension_questions,
                    "budget_seconds": plan.budget_seconds,
                    "budget_tokens": plan.budget_tokens,
                    "created_at_unix": plan.created_at_unix,
                },
                "cycle_history": cycle_history,
                "all_researcher_outputs": all_researcher_outputs,
            }
            _save_checkpoint(checkpoint_data, checkpoint_path)
            _progress(f"  Checkpoint saved: {checkpoint_path}")

        if not reflection_result.should_continue:
            reason = reflection_result.summary.split("\n")[0] if reflection_result.summary else "coverage sufficient"
            _progress(f"  Stopping: {reason}")
            break

    # ── Write phase ──
    _progress("━━━ Writing Report ━━━")

    all_merged = []
    all_themes = []
    for ch in cycle_history:
        ao = ch.get("analyst_output", {})
        all_merged.extend(ao.get("merged_findings", []))
        all_themes.extend(ao.get("themes", []))

    final_analyst = {
        "themes": all_themes,
        "contradictions": [],
        "gaps": cycle_history[-1].get("reflection", {}).get("gaps", []) if cycle_history else [],
        "merged_findings": all_merged,
    }

    try:
        fmt = OutputFormat(output_format)
    except ValueError:
        fmt = OutputFormat.REPORT

    if mock_mode:
        report = f"# Mock Research Report: {question}\n\n## Executive Summary\n\n"
        report += f"Mock report generated in {len(cycle_history)} cycle(s).\n\n"
        for ch in cycle_history:
            refl = ch.get("reflection", {})
            report += f"### Cycle {ch['cycle']} (coverage: {refl.get('coverage_score', '?')})\n\n"
            report += f"{refl.get('summary', '')}\n\n"
        if refl.get("gaps"):
            report += "## Gaps Identified\n\n"
            for g in refl["gaps"]:
                report += f"- {g}\n"
        writer_out = {
            "status": "complete",
            "report": report.strip(),
            "question": question,
            "format": output_format,
            "metadata": {},
        }
    else:
        writer_agent = WriterAgent(use_llm=True)
        writer_out = writer_agent.write_report(final_analyst, question, fmt)

    total_duration = round(time.time() - start_time, 2)
    _progress(f"Report generated: {len(writer_out.get('report', ''))} chars in {total_duration}s")

    return {
        "status": "complete",
        "question": question,
        "cycles_completed": len(cycle_history),
        "final_coverage": cycle_history[-1]["reflection"]["coverage_score"] if cycle_history else 0.0,
        "report": writer_out.get("report", ""),
        "cycle_history": cycle_history,
        "metadata": {
            "total_duration_seconds": total_duration,
            "total_findings": len(all_merged),
            "max_cycles": max_cycles,
            "dimensions": plan.dimensions,
            "output_format": output_format,
        },
    }


# ─── Backward compatibility alias ──────────────────────────────────────────


def run_looping_pipeline(
    question: str,
    max_cycles: int = 3,
    dimensions: Optional[list[str]] = None,
    search_results: Optional[dict[str, list[dict]]] = None,
    mock_mode: bool = False,
) -> dict:
    """Backward-compatible wrapper for run_enhanced_pipeline."""
    return run_enhanced_pipeline(
        question=question,
        max_cycles=max_cycles,
        dimensions=dimensions,
        search_results=search_results,
        mock_mode=mock_mode,
    )


# ─── CLI ──────────────────────────────────────────────────────────────────────


def main():
    # Detect full pipeline mode (no subcommand, just a question)
    full_pipeline_args = [a for a in sys.argv[1:] if not a.startswith("-")]
    has_flags = any(a.startswith("-") for a in sys.argv[1:])

    is_full_pipeline = (
        full_pipeline_args
        and full_pipeline_args[0] not in ("researcher", "analyst", "writer", "-h", "--help")
        and "--help" not in sys.argv
        and "-h" not in sys.argv
    )

    if is_full_pipeline:
        parser = argparse.ArgumentParser(
            description="Deep Research Pipeline (full loop with progress, checkpoints, and budget)"
        )
        parser.add_argument("question", help="Research question")
        parser.add_argument("--max-cycles", type=int, default=3, help="Max research cycles (1-8)")
        parser.add_argument("--mock", action="store_true", help="Use mock data (no API calls)")
        parser.add_argument("--output", "-o", help="Output file path for the report")
        parser.add_argument("--format", "-f", choices=["report", "summary", "brief", "json"],
                            default="report", help="Output format (default: report)")
        parser.add_argument("--time-limit", type=int, default=900, help="Max seconds (default: 900)")
        parser.add_argument("--token-limit", type=int, default=60000, help="Max estimated tokens")
        parser.add_argument("--checkpoint", help="Save checkpoints to this path")
        parser.add_argument("--resume", help="Resume from checkpoint file")
        parser.add_argument("--dimensions", nargs="+", help="Explicit research dimensions")
        parser.add_argument("--no-parallel", action="store_true", help="Research dimensions sequentially")
        args = parser.parse_args()

        result = run_enhanced_pipeline(
            question=args.question,
            max_cycles=args.max_cycles,
            dimensions=args.dimensions,
            mock_mode=args.mock,
            output_format=args.format,
            time_limit=args.time_limit,
            token_limit=args.token_limit,
            checkpoint_path=args.checkpoint,
            resume_from=args.resume,
            parallel_dimensions=not args.no_parallel,
        )

        # Save to file if requested
        if args.output:
            try:
                save_report(result, args.output)
                _progress(f"Report saved to {args.output}")
            except Exception as e:
                _progress(f"Error saving report: {e}")
                print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            if args.format == "json":
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(result.get("report", ""))
        return

    # Subcommand mode (backward compatible)
    parser = argparse.ArgumentParser(description="Research pipeline orchestrator")
    sub = parser.add_subparsers(dest="command")

    rp = sub.add_parser("researcher")
    rp.add_argument("--question", "-q", required=True)
    rp.add_argument("--dimension", "-d", required=True)
    rp.add_argument("--questions", nargs="+", default=[])
    rp.add_argument("--max-sources", type=int, default=10)
    rp.add_argument("--search-results", help="JSON file with pre-fetched results")

    ap = sub.add_parser("analyst")
    ap.add_argument("--input", "-i", required=True, help="JSON file or stdin")

    wp = sub.add_parser("writer")
    wp.add_argument("--input", "-i", required=True, help="JSON file or stdin")
    wp.add_argument("--question", "-q", required=True)

    args = parser.parse_args()

    if args.command == "researcher":
        results = None
        if args.search_results:
            with open(args.search_results) as f:
                results = json.load(f)
        output = run_researcher(
            args.question, args.dimension, args.questions, args.max_sources, results
        )

    elif args.command == "analyst":
        if args.input == "-":
            data = json.load(sys.stdin)
        else:
            with open(args.input) as f:
                data = json.load(f)
        if isinstance(data, list):
            researcher_outputs = data
        else:
            researcher_outputs = [data]
        output = run_analyst(researcher_outputs)

    elif args.command == "writer":
        if args.input == "-":
            analyst_data = json.load(sys.stdin)
        else:
            with open(args.input) as f:
                analyst_data = json.load(f)
        output = run_writer(analyst_data, args.question)

    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
