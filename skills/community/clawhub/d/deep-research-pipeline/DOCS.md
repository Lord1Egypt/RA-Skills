# Deep Research v2 — Documentation

Comprehensive multi-stage research pipeline with reflection loops, multi-query retrieval, LLM chunk selection, and citation integrity.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR (you)                           │
│                                                                 │
│  1. PLAN ─── Decompose question into research dimensions       │
│              Save plan to memory/research/<slug>/plan.md        │
│                                                                 │
│  2. RESEARCH LOOP (0-8 cycles)                                 │
│     ┌──────────────────────────────────────────────────────┐   │
│     │  ┌─────────────┐    ┌─────────────┐    ┌──────────┐  │   │
│     │  │ RESEARCHER   │───▶│  ANALYST    │───▶│ REFLECT  │  │   │
│     │  │ (parallel)   │    │  (dedup +   │    │ (gap     │  │   │
│     │  │              │    │   themes +   │    │  check + │  │   │
│     │  │ query_gen    │    │   contrad.) │    │  budget) │  │   │
│     │  │ web_search   │    │             │    │          │  │   │
│     │  │ chunk_select │    │             │    │ continue?│  │   │
│     │  │ context_exp  │    │             │    │   │      │  │   │
│     │  └─────────────┘    └─────────────┘    │───┘      │  │   │
│     │                                            │      │  │   │
│     │              ◀─────────────────────────────┘      │  │   │
│     └──────────────────────────────────────────────────────┘   │
│                                                                 │
│  3. WRITE ─── WriterAgent produces publication-quality report   │
│              Multiple formats: report, summary, brief, json     │
│              Inline citations, confidence indicators             │
│                                                                 │
│  4. VERIFY ─── Adversarial fact-check (optional)                │
│                                                                 │
│  5. DELIVER ── Final report + provenance                        │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### 1. Query Generator (`query_generator.py`)

Generates 3-5 diverse search query variants for a research question using LLM + rule-based fallback.

**API:**
```python
from query_generator import generate_queries

queries = generate_queries("How does RAG work?", max_queries=5)
# Returns: [{"type": "semantic", "query": "...", "rationale": "..."}, ...]
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `question` | str | required | Research question |
| `max_queries` | int | 5 | Max query variants |
| `api_key` | str | None | ZAI_API_KEY override |

**Query types:** semantic, keyword, broad, specific, comparative

### 2. Research Sources (`research_sources.py`)

Multi-source search adapters:
- `WebSearchSource` — DuckDuckGo HTML/Lite + content fetching
- `GitHubSource` — GitHub REST API (repos + code search)
- `DocSource` — Documentation URL fetching + discovery

**API:**
```python
from research_sources import WebSearchSource, GitHubSource, DocSource, score_results, deduplicate_results

web = WebSearchSource()
results = web.search("OpenClaw skills", limit=5)

scored = score_results(results, topic="OpenClaw", use_llm=True)
unique = deduplicate_results(scored)
```

**Also provides:** `score_results()` (LLM + keyword fallback), `deduplicate_results()` (URL + content hash)

### 3. Chunk Selector (`chunk_selector.py`)

LLM scores each chunk for relevance, filters by threshold. The "hallucination killer."

**API:**
```python
from chunk_selector import select_relevant_chunks

selected = select_relevant_chunks(
    question="How does RAG work?",
    content=chunks,          # list of {content, url, title}
    min_score=0.7,           # threshold (0.0-1.0)
    max_context_tokens=8000, # batch size limit
)
```

**Batching:** Chunks are batched to fit within token limits. Each chunk scored 0.0-1.0.

### 4. Context Expander (`context_expander.py`)

Decides if selected chunks need surrounding context, fetches it from source URLs.

**API:**
```python
from context_expander import expand_context

expanded = expand_context(
    selected_chunks=selected,
    question="How does RAG work?",
    max_expansions=5,  # max URLs to re-fetch
)
```

### 5. Researcher Agent (`researcher.py`)

Orchestrates multi-source searches: query generation → parallel search → dedup → scoring → chunk selection → context expansion → finding extraction.

**API:**
```python
from researcher import research, research_dimension

# Full research on a topic
result = research("OpenClaw skills system", sources=["web", "github"])

# Dimension-based research (for subagents)
result = research_dimension(
    dimension="architecture",
    questions=["How does X work?", "What are the components?"],
    sources=["web", "github"],
)
```

**`research()` returns:**
```json
{
  "status": "complete|partial|no_results",
  "topic": "string",
  "findings": [{"claim": "...", "source_url": "...", "confidence": 0.9, "category": "..."}],
  "sources": [{"title": "...", "url": "...", "relevance_score": 0.8}],
  "gaps": [{"question": "...", "reason": "...", "importance": "high|medium|low"}],
  "metadata": {"queries_generated": 5, "raw_results": 20, "elapsed_seconds": 12.3}
}
```

**`research_dimension()` returns:**
```json
{
  "dimension": "architecture",
  "questions": ["..."],
  "findings": [...],
  "sources": [...],
  "coverage": 0.8,
  "question_coverage": {"q1": {"covered": true, "findings_count": 3}},
  "metadata": {...}
}
```

### 6. Analyst (`analyst.py`)

Local, deterministic analysis. No API calls needed.

**API:**
```python
from analyst import analyze_findings, AnalysisResult

result: AnalysisResult = analyze_findings(
    findings=[{"claim": "...", "source_url": "...", "confidence": 0.9}],
    dimensions=["architecture", "performance"],
)
```

**Returns `AnalysisResult` (frozen dataclass):**
| Field | Type | Description |
|-------|------|-------------|
| `themes` | list[dict] | 3-7 thematic clusters with keyword co-occurrence |
| `contradictions` | list[dict] | Opposing claims detected via polarity heuristics |
| `gaps` | list[dict] | Dimensions with insufficient coverage |
| `confidence_map` | dict[str, float] | Reliability scores per finding (0.0-1.0) |
| `coverage_score` | float | Overall dimension coverage (0.0-1.0) |

**Features:**
- Deduplication by hash + Jaccard similarity (≥0.6 threshold)
- Theme extraction via keyword co-occurrence clusters
- Contradiction detection via polarity heuristics (up/down/affirm/negate)
- Confidence scoring: source quality × extractor confidence + corroboration bonus

### 7. Reflection (`reflection.py`)

Coverage check + gap analysis + continue decision. Runs after every research cycle.

**API:**
```python
from reflection import ResearchPlan, reflect, ReflectionResult

plan = ResearchPlan(
    question="What is RAG?",
    dimensions=["architecture", "benchmarks", "limitations"],
    dimension_questions={"architecture": ["What is RAG?"]},
    budget_seconds=900,
    budget_tokens=60000,
)

result: ReflectionResult = reflect(plan, findings, cycle=1, max_cycles=8)
```

**Returns `ReflectionResult` (frozen dataclass):**
| Field | Type | Description |
|-------|------|-------------|
| `should_continue` | bool | Whether to run another research cycle |
| `gaps` | list[str] | Dimensions needing more research |
| `coverage_score` | float | Fraction of dimensions covered (0.0-1.0) |
| `next_dimensions` | list[str] | Suggested dimensions for next cycle |
| `summary` | str | Human-readable progress summary |

**Stop conditions:**
- Cycle ≥ max_cycles (hard stop at 8)
- Coverage ≥ 0.8 with no significant gaps
- Time budget ≥ 90% used
- Token budget ≥ 90% used
- Empty findings after cycle ≥ 1

### 8. Writer Agent (`writer.py`)

Publication-quality report generation with multiple output formats.

**API:**
```python
from writer import WriterAgent, write_report, OutputFormat, save_report

# Using the agent class
agent = WriterAgent(use_llm=True)
result = agent.write_report(
    analyst_output,           # from analyst or run_analyst()
    question="What is RAG?",
    fmt=OutputFormat.REPORT,  # REPORT, SUMMARY, BRIEF, JSON
    metadata={"cycles": 3},
)

# Using the convenience function
result = write_report(analyst_output, question, fmt="report", use_llm=True)

# Save to file
save_report(result, "output/report.md")
```

**Output formats:**

| Format | Description |
|--------|-------------|
| `report` | Full markdown with all sections (default) |
| `summary` | Executive summary + top 5 findings |
| `brief` | Bullet-point format for quick scanning |
| `json` | Structured JSON with annotated findings |

**Report sections:**
1. Title + metadata
2. Executive Summary (2-3 paragraphs)
3. Key Findings (numbered, with confidence badges 🟢🟡🟠🔴)
4. Detailed Analysis (one section per theme)
5. Contradictions (callout boxes for source disagreements)
6. Knowledge Gaps (prioritized by importance)
7. Sources (numbered reference list)
8. Methodology (research process description)

**Confidence indicators:**
- 🟢 High (≥0.8) — directly stated in sources
- 🟡 Medium (≥0.6) — strongly implied
- 🟠 Low (≥0.4) — inferred
- 🔴 Uncertain (<0.4) — weak support

### 9. Research Pipeline (`research_pipeline.py`)

Full orchestration with CLI, progress reporting, checkpoints, and budget awareness.

**CLI Usage:**
```bash
# Full pipeline
python3 research_pipeline.py "What is quantum computing?" \
    --max-cycles 3 \
    --output report.md \
    --format report

# Mock mode (no API calls)
python3 research_pipeline.py "test question" --mock --output report.md

# With budget limits
python3 research_pipeline.py "question" \
    --max-cycles 3 \
    --time-limit 300 \
    --token-limit 40000

# Resume from checkpoint
python3 research_pipeline.py "question" \
    --resume checkpoint.json \
    --output report.md

# Explicit dimensions
python3 research_pipeline.py "question" \
    --dimensions architecture benchmarks limitations \
    --output report.md

# Subcommand mode (backward compatible)
python3 research_pipeline.py researcher --question "..." --dimension "..."
python3 research_pipeline.py analyst --input researcher_output.json
python3 research_pipeline.py writer --input analyst_output.json --question "..."
```

**Python API:**
```python
from research_pipeline import (
    run_enhanced_pipeline, run_looping_pipeline,
    run_researcher, run_analyst, run_writer,
)

# Enhanced pipeline with all features
result = run_enhanced_pipeline(
    question="What is quantum computing?",
    max_cycles=3,
    dimensions=["hardware", "applications", "theory"],
    mock_mode=False,
    output_format="report",
    time_limit=900,
    token_limit=60000,
    checkpoint_path="checkpoint.json",
    resume_from=None,
    parallel_dimensions=True,
)

# Backward-compatible wrapper
result = run_looping_pipeline(question="...", max_cycles=3, mock_mode=True)
```

**CLI Flags:**
| Flag | Default | Description |
|------|---------|-------------|
| `--max-cycles` | 3 | Max research cycles (1-8) |
| `--mock` | false | Use mock data, no API calls |
| `--output` / `-o` | stdout | Output file path |
| `--format` / `-f` | report | Output format (report/summary/brief/json) |
| `--time-limit` | 900 | Max seconds |
| `--token-limit` | 60000 | Max estimated tokens |
| `--checkpoint` | none | Save checkpoints to path |
| `--resume` | none | Resume from checkpoint file |
| `--dimensions` | auto | Explicit research dimensions |
| `--no-parallel` | false | Research dimensions sequentially |

### 10. Fact Checker (`fact-checker.py`)

Simple claim extraction and source ranking.

```bash
python3 fact-checker.py "Text with claims" --sources '["url1", "url2"]'
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_API_KEY` | (none) | Universal provider API key, highest priority |
| `LLM_API_BASE` | (none) | Universal OpenAI-compatible base URL, highest priority |
| `LLM_MODEL` | provider default | Universal model name override |
| `OPENAI_API_KEY` | (none) | OpenAI or OpenAI-compatible API key |
| `OPENAI_API_BASE` / `OPENAI_BASE_URL` | OpenAI default | OpenAI-compatible endpoint |
| `OPENAI_MODEL` | provider default | OpenAI-compatible model override |
| `ZAI_API_KEY` | (none) | Z.AI GLM API key, still supported for local OpenClaw setups |
| `ZAI_API_ENDPOINT` | `https://api.z.ai/api/coding/paas/v4` | Z.AI GLM endpoint |
| `GLM_MODEL` | `glm-5-turbo` | Z.AI model override |
| `GITHUB_TOKEN` | (none) | GitHub API token (higher rate limits) |
| `DEEP_RESEARCH_TIME_BUDGET_SECONDS` | 900 | Default time budget |
| `DEEP_RESEARCH_TOKEN_BUDGET` | 60000 | Default token budget |

### Key Parameters

| Parameter | Recommended Range | Description |
|-----------|------------------|-------------|
| `max_cycles` | 2-5 | More cycles = deeper research, longer time |
| `max_queries` | 3-5 | Query variants per question |
| `min_relevance` | 0.4-0.6 | Relevance filter threshold |
| `chunk_selector_threshold` | 0.7 | Min chunk score to keep |
| `max_context_tokens` | 8000-12000 | Context window per LLM call |

## Example Workflows

### Quick Research (single fact)
```python
# No subagents, direct pipeline
result = run_enhanced_pipeline(
    question="What is the current price of Bitcoin?",
    max_cycles=1,
    mock_mode=False,
    output_format="summary",
)
```

### Multi-Dimension Deep Dive
```python
result = run_enhanced_pipeline(
    question="What is the state of quantum computing in 2026?",
    max_cycles=4,
    dimensions=["hardware", "algorithms", "applications", "challenges", "investment"],
    time_limit=600,
    token_limit=80000,
    checkpoint_path="/tmp/quantum-checkpoint.json",
    parallel_dimensions=True,
)
```

### Resume Interrupted Research
```bash
# First run (gets interrupted)
python3 research_pipeline.py "Complex topic" \
    --max-cycles 5 \
    --checkpoint /tmp/checkpoint.json \
    --output report.md

# Resume
python3 research_pipeline.py "Complex topic" \
    --resume /tmp/checkpoint.json \
    --output report.md
```

### Generate Multiple Formats
```python
from writer import WriterAgent, OutputFormat

agent = WriterAgent(use_llm=True)

# Full report
report = agent.write_report(analyst_output, question, OutputFormat.REPORT)

# Executive summary
summary = agent.write_report(analyst_output, question, OutputFormat.SUMMARY)

# Quick brief
brief = agent.write_report(analyst_output, question, OutputFormat.BRIEF)

# Structured JSON
json_out = agent.write_report(analyst_output, question, OutputFormat.JSON)
```

## Troubleshooting

### "LLM_API_KEY, OPENAI_API_KEY, or ZAI_API_KEY not set"
Set any supported provider configuration:
```bash
# Universal OpenAI-compatible provider
export LLM_API_KEY="your-key-here"
export LLM_API_BASE="https://api.example.com/v1"
export LLM_MODEL="your-model"

# Or OpenAI-compatible env names
export OPENAI_API_KEY="your-key-here"
export OPENAI_BASE_URL="https://api.example.com/v1"

# Or Z.AI GLM
export ZAI_API_KEY="your-key-here"
```
Or use `--mock` mode for testing without API access.

### Pipeline hangs
- Check network connectivity to your configured provider endpoint
- Reduce `--max-cycles` (try 1-2)
- Set explicit `--dimensions` to skip query generation
- Use `--time-limit` to enforce a timeout

### Empty results
- Try broader search queries
- Check if DuckDuckGo is accessible from your network
- Use `--dimensions` with explicit terms
- Try adding more source types

### Low quality findings
- Increase `max_queries` (5-7)
- Lower `min_relevance` threshold (0.3-0.4)
- Run more cycles (3-5)
- Add GitHub/docs sources

### Tests failing
```bash
# Run all tests
cd skills/deep-research/scripts
python3 -m pytest test_analyst.py test_pipeline.py test_integration.py -v

# Run specific test class
python3 -m pytest test_integration.py::TestWriterAgentReport -v
```

### Checkpoint file format
```json
{
  "plan": {
    "question": "...",
    "dimensions": ["dim1", "dim2"],
    "dimension_questions": {"dim1": ["q1"]},
    "budget_seconds": 900,
    "budget_tokens": 60000,
    "created_at_unix": 1714022400.0
  },
  "cycle_history": [...],
  "all_researcher_outputs": [...]
}
```

## Design Principles

1. **Pure Python 3, stdlib only** — no external dependencies
2. **Stage separation** — orchestrator never searches, researchers never see full plan
3. **Citation integrity** — every claim traces to a source URL
4. **Reflection is mandatory** — run after every cycle
5. **Graceful degradation** — LLM failures fall back to rule-based methods
6. **Budget awareness** — time and token limits prevent runaway research
