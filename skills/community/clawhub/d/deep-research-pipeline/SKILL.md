---
name: deep-research
version: 2.0.1
description: "Multi-stage deep research with reflection loops, multi-query retrieval, LLM chunk selection, and citation integrity. Use when: deep research, literature review, topic investigation, multi-source analysis, fact-checking, competitive analysis, technology deep-dives."
---

# Deep Research Pipeline

Deep Research Pipeline turns broad questions into cited, publication-quality reports through a staged research workflow: planning, multi-query retrieval, chunk selection, analysis, reflection, writing, and optional verification.

It is designed for research that should not be answered from memory or a single search result. The pipeline keeps claims tied to sources, surfaces contradictions, tracks gaps, and can resume from checkpoints.

## Why Use It

- **Multi-stage research, not one-shot summarization** — separate researcher, analyst, reflection, and writer stages.
- **Citation integrity** — findings and final claims trace back to URLs/sources.
- **Reflection loops** — the pipeline checks coverage and decides whether another cycle is needed.
- **Portable LLM config** — supports `LLM_API_KEY`/`LLM_API_BASE`, OpenAI-compatible endpoints, or Z.AI GLM.
- **Operational controls** — checkpoint/resume, time limits, token budgets, output formats, and mock mode.

## When to Use
Deep research, comprehensive analysis, literature reviews, competitive analysis, fact-checking, technology deep-dives — anything needing multiple sources, synthesis, and verified citations.

## Quick Start

```bash
cd skills/deep-research

# Optional: configure any OpenAI-compatible provider
export LLM_API_KEY="your-key"
export LLM_API_BASE="https://api.example.com/v1"
export LLM_MODEL="your-model"

# Or use OpenAI-compatible env names
export OPENAI_API_KEY="your-key"
export OPENAI_BASE_URL="https://api.example.com/v1"

# Run a report
python3 scripts/research_pipeline.py \
  "Compare Vercel, Netlify, and Cloudflare Pages in 2026" \
  --max-cycles 2 \
  --format report \
  --output report.md

# Test without API calls
python3 scripts/research_pipeline.py "test question" --mock --output report.md
```

If no universal/OpenAI-compatible variables are set, the skill still supports Z.AI via `ZAI_API_KEY` and `ZAI_API_ENDPOINT`.

## Architecture

```
ORCHESTRATOR (you)
    │
    ├── Plan → Decompose question into research dimensions
    │
    ├── REFLECTION LOOP (0-8 cycles)
    │   ├── Researcher Agent (parallel) → multi-query search + chunk selection
    │   ├── Analyst Agent → dedupe + themes + contradictions
    │   └── Reflection → coverage check, gap analysis, continue decision
    │
    ├── Writer Agent → polished report (report/summary/brief/json)
    │
    └── Verify (optional) → adversarial fact-check
```

**Key principle:** Orchestrator NEVER searches directly. Clean output flows between stages only.

## Two Modes

### Mode 1: Full Pipeline CLI (Recommended)
Use the enhanced `research_pipeline.py` for automated end-to-end research:

```bash
# Full research with all features
python3 scripts/research_pipeline.py "What is the state of quantum computing in 2026?" \
    --max-cycles 3 \
    --output report.md \
    --format report

# Mock mode (no API calls, for testing)
python3 scripts/research_pipeline.py "test question" --mock --output report.md

# With budget limits
python3 scripts/research_pipeline.py "question" \
    --max-cycles 3 --time-limit 300 --token-limit 40000

# Resume from checkpoint
python3 scripts/research_pipeline.py "question" \
    --resume checkpoint.json --output report.md

# Explicit dimensions
python3 scripts/research_pipeline.py "question" \
    --dimensions architecture benchmarks limitations \
    --output report.md --format summary
```

**CLI Flags:**
| Flag | Default | Description |
|------|---------|-------------|
| `--max-cycles` | 3 | Max research cycles (1-8) |
| `--mock` | false | Use mock data, no API calls |
| `--output` / `-o` | stdout | Output file path |
| `--format` / `-f` | report | Output format: `report`, `summary`, `brief`, `json` |
| `--time-limit` | 900 | Max seconds for entire pipeline |
| `--token-limit` | 60000 | Max estimated tokens |
| `--checkpoint` | none | Save checkpoints to path |
| `--resume` | none | Resume from checkpoint file |
| `--dimensions` | auto | Explicit research dimensions |
| `--no-parallel` | false | Research dimensions sequentially |

**Output formats:**
- `report` — Full markdown: Executive Summary → Key Findings → Detailed Analysis → Contradictions → Gaps → Sources → Methodology
- `summary` — Executive summary + top 5 findings + sources
- `brief` — Bullet-point format for quick scanning
- `json` — Structured JSON with annotated findings and metadata

### Mode 2: Orchestrated Sub-Agents (For complex research)
Use when you need fine-grained control over each stage or parallel dimension research with sub-agents.

## Workflow (Orchestrated Mode)

### Phase 1: Planning
- Analyze question, create slug, make `memory/research/<slug>/` directory
- Generate research plan with dimensions and questions
- Save to `plan.md`

### Phase 2: Research Cycle (repeat up to 8 times)

#### Step A: Spawn Researcher Agent(s)
Use `sessions_spawn` with a **task brief** (NOT the full query):
```json
{
  "dimension": "technical architecture",
  "specific_questions": ["How does X work?", "What are Y's components?"],
  "context_limit": 5000,
  "max_sources": 10
}
```

Researcher agent does:
1. **Multi-query generation** — `scripts/query_generator.py` produces 3-5 variants
2. **Parallel search** — `web_search` for each variant
3. **Content fetching** — `web_fetch` for top results
4. **LLM chunk selection** — `scripts/chunk_selector.py` scores each chunk (≥0.7)
5. **Context expansion** — `scripts/context_expander.py` fetches surrounding content
6. Output: JSON findings with citations

**Can spawn 2-3 researcher agents in parallel for different dimensions.**

#### Step B: Spawn Analyst Agent
After researcher(s) complete, spawn analyst with their combined output:
1. Deduplicate overlapping findings
2. Flag contradictions (explicit + implicit)
3. Group into thematic clusters
4. Identify gaps
5. Output: Cleaned JSON + gap list

#### Step C: Run Reflection
After analyst completes, run `scripts/reflection.py`:
1. What's covered? (themes + confidence scores)
2. What gaps remain? (unanswered questions)
3. What contradictions emerged?
4. New directions discovered?
5. **Should continue?** (coverage ≥ 0.8 + minor gaps → stop)

Save reflection to `memory/research/<slug>/reflection-cycle-N.md`

#### Continue Decision
- Coverage ≥ 0.8 AND gaps minor → proceed to Phase 3
- Major contradictions → spawn targeted researcher
- Significant gaps → another researcher cycle
- Hard stop at cycle 8

### Phase 3: Write Report
Use the **Writer Agent** (`scripts/writer.py`) for publication-quality output:

```python
# From Python
from writer import WriterAgent, OutputFormat, write_report

# Generate report using WriterAgent
agent = WriterAgent(use_llm=True)
result = agent.write_report(
    analyst_output,           # from analyst or run_analyst()
    question="What is RAG?",
    fmt=OutputFormat.REPORT,
)

# Or use convenience function
result = write_report(analyst_output, question, fmt="report")

# Save to file
from writer import save_report
save_report(result, "output/report.md")
```

**Report features:**
- 🟢🟡🟠🔴 Confidence indicators on every finding
- `[source_url]` inline citations throughout
- ⚠️ Contradiction callout boxes where sources disagree
- Structured sections: Summary → Findings → Analysis → Contradictions → Gaps → Sources → Methodology
- Template-based fallback when no LLM available

### Phase 4: Verify (optional sub-agent)
Spawn adversarial verifier:
- Anchor every claim to source
- Verify URLs with `web_fetch`
- Remove unsourced claims
- Save to `review.md`

### Phase 5: Deliver
- Fix any FATAL issues from review
- Copy to `final.md`
- Write `provenance.md` (date, cycles, sources, verification status)
- Send summary to user

## Python API

```python
import sys, os
sys.path.insert(0, os.path.expanduser("~/.openclaw/workspace/skills/deep-research/scripts"))

from research_pipeline import run_enhanced_pipeline

result = run_enhanced_pipeline(
    question="What is the state of quantum computing in 2026?",
    max_cycles=3,
    dimensions=["hardware", "algorithms", "applications", "challenges"],
    mock_mode=False,
    output_format="report",
    time_limit=900,
    token_limit=60000,
    checkpoint_path="checkpoint.json",    # auto-saves progress
    parallel_dimensions=True,             # parallel research per dimension
)

# result["report"] = markdown string
# result["cycles_completed"] = int
# result["final_coverage"] = float (0.0-1.0)
# result["metadata"] = dict with timing, findings count, etc.
```

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `research_pipeline.py` | **Full pipeline orchestration** | `python3 scripts/research_pipeline.py "question" --max-cycles 3` |
| `query_generator.py` | Generate 3-5 search query variants | `python3 scripts/query_generator.py -q "..."` |
| `chunk_selector.py` | LLM scores chunks, filters by threshold | `python3 scripts/chunk_selector.py -q "..." -c chunks.json` |
| `context_expander.py` | Fetch surrounding context for incomplete chunks | `python3 scripts/context_expander.py -s selected.json -q "..."` |
| `reflection.py` | Mandatory gap/contradiction check | `python3 scripts/reflection.py -q "..." -f findings.json -c 1` |
| `writer.py` | Publication-quality report generation | `from writer import WriterAgent, write_report` |
| `analyst.py` | Dedup + themes + contradictions (no API needed) | `from analyst import analyze_findings` |
| `researcher.py` | Multi-source research orchestration | `from researcher import research, research_dimension` |
| `research_sources.py` | Search adapters (web, GitHub, docs) | `from research_sources import WebSearchSource` |
| `fact-checker.py` | Claim extraction + source ranking | `python3 scripts/fact-checker.py "text" --sources '["url1"]'` |

All LLM-enabled scripts use the shared provider-agnostic `llm_client.py`.

Provider resolution order:
1. `LLM_API_KEY` + `LLM_API_BASE` + optional `LLM_MODEL`
2. `OPENAI_API_KEY` + `OPENAI_API_BASE` / `OPENAI_BASE_URL` + optional `OPENAI_MODEL`
3. `ZAI_API_KEY` + optional `ZAI_API_ENDPOINT` / `GLM_MODEL`

If no key is configured, use `--mock` for local pipeline testing or rely on scripts with rule-based fallbacks where available.

## Examples

### Example 1: Quick Competitive Analysis
```bash
python3 scripts/research_pipeline.py \
    "Compare Vercel vs Netlify vs Cloudflare Pages features and pricing 2026" \
    --max-cycles 2 \
    --dimensions features pricing performance ecosystem \
    --format summary \
    --output competitive-analysis.md
```

### Example 2: Deep Technology Research
```bash
python3 scripts/research_pipeline.py \
    "What is the current state of AI agent frameworks?" \
    --max-cycles 4 \
    --time-limit 600 \
    --token-limit 80000 \
    --checkpoint /tmp/ai-agents-checkpoint.json \
    --format report \
    --output ai-agents-research.md
```

### Example 3: Literature Review (mock mode for testing)
```bash
python3 scripts/research_pipeline.py \
    "What does the research say about transformer architecture efficiency?" \
    --mock \
    --max-cycles 3 \
    --format report \
    --output literature-review.md
```

### Example 4: Bullet Brief for Quick Scanning
```bash
python3 scripts/research_pipeline.py \
    "What are the latest developments in Rust web frameworks?" \
    --max-cycles 2 \
    --format brief \
    --output rust-web-brief.md
```

### Example 5: JSON Output for Programmatic Use
```bash
python3 scripts/research_pipeline.py \
    "What is the market size of edge computing?" \
    --max-cycles 2 \
    --format json \
    --output edge-computing-data.json
```

## Integration with Night Shift

To queue research plans for Night Shift execution:

1. **Create a research plan file:**
```json
// memory/research/queued/<slug>.json
{
  "question": "What is the state of quantum computing in 2026?",
  "max_cycles": 3,
  "dimensions": ["hardware", "algorithms", "applications"],
  "output_format": "report",
  "output_path": "memory/research/quantum-2026/final.md",
  "time_limit": 600,
  "created_at": "2026-04-25T06:00:00Z"
}
```

2. **Night Shift picks up queued plans** and runs them via:
```bash
python3 scripts/research_pipeline.py "$QUESTION" \
    --max-cycles $MAX_CYCLES \
    --dimensions $DIMENSIONS \
    --format $FORMAT \
    --output $OUTPUT_PATH \
    --time-limit $TIME_LIMIT
```

3. **Results are saved** to `memory/research/<slug>/final.md` with provenance metadata.

## File Layout
```
memory/research/<slug>/
├── plan.md                    # Research plan with dimensions
├── reflection-cycle-1.md      # Reflection after each cycle
├── reflection-cycle-2.md
├── researcher-output-*.json   # Raw researcher findings
├── analyst-output.json        # Merged/deduped findings
├── draft.md                   # First draft
├── brief.md                   # Verified brief
├── review.md                  # Adversarial review (optional)
├── final.md                   # Final report
├── provenance.md              # Metadata + source verification status
└── checkpoint.json            # Pipeline checkpoint (auto-saved)
```

## Quick Mode
Skip sub-agents and the full pipeline. Do 5-10 searches yourself. Still use evidence tables, verify URLs, cite sources. Shorter, inline in chat.

## Integrity Commandments
1. Never fabricate a source — no URL = don't mention it
2. Never claim existence without checking
3. Never extrapolate unread details
4. Read before summarizing
5. No fake certainty — never say "verified" unless checked
6. Never invent numbers/benchmarks/comparisons
7. Separate observations from inferences
8. **Every claim traces to a source** — citation integrity is mandatory
9. **Reflection is not optional** — run it after every cycle
10. **Stage separation** — orchestrator never searches, researchers never see full plan

## Scale Decision
- Single fact → Quick Mode (3-10 tool calls, no sub-agents)
- 2-3 item comparison → 2 parallel researcher sub-agents, 2-3 cycles
- Broad/multi-faceted → 3-4 researcher sub-agents, 3-5 cycles
- PhD-level deep dive → 4+ researchers, 5-8 cycles

## See Also
- **DOCS.md** — Full API reference, architecture diagrams, troubleshooting
- **test_integration.py** — 29 integration tests covering the full pipeline
- **test_pipeline.py** — 26 unit tests for individual components
