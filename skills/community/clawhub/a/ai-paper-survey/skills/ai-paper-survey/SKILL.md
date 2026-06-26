---
name: ai-paper-survey
description: "Conduct structured AI paper surveys using alphaXiv MCP tools. Reads user research interests from a keywords file, searches recent papers across multiple dimensions, classifies by innovation tier, runs impact analysis, and outputs a Markdown report. Use when the user asks to survey recent papers, do a literature review, find what's new in a research area, or track progress in AI subfields."
version: "1.0.0"
allowed-tools: "Bash Read Write Agent"
license: MIT-0
metadata:
  skill-author: haataa
  version: "1.0.0"
  openclaw:
    emoji: "🔬"
    requires:
      bins: ["python"]
---

# AI Paper Survey Skill

Structured, multi-phase paper survey workflow for AI research.

## When to Use

- "Survey recent papers in [topic]"
- "What's new in agent/LLM/multimodal research?"
- "Find the most important papers from the last N months"
- "Do a literature review on [topic]"
- "Track progress in [research area]"

## Prerequisites

- **alphaXiv MCP server** must be connected (provides `embedding_similarity_search`, `full_text_papers_search`, `get_paper_content`)
- **paper-impact-analyzer** skill installed (for impact assessment)
- **Research keywords file** (optional): a Markdown file listing the user's research interests and keywords

## Workflow: 5-Phase Pipeline

### Phase 0: Load Research Context

1. Check if a research keywords file exists. Look for files matching patterns:
   - `研究关键词*.md`
   - `research-keywords*.md`
   - `research-interests*.md`
   in the current working directory.

2. If found, read it and extract:
   - **Theme list**: the major research themes (e.g., "RL optimization", "Agent & Tool Calling")
   - **Keywords**: specific terms to search for (e.g., "GRPO", "Nested Learning", "VLA")
   - **Models of interest**: specific model names (e.g., "DeepSeek V4", "Qwen3.5")

3. If no keywords file, ask the user for:
   - Research topics (1-5 topics)
   - Time range (default: last 3 months)
   - Any specific papers or authors to track

4. Determine the **time range** (default: last 3 months from today).

5. Generate **search queries** using the template below. For each user theme T, generate:

```
Semantic query:  "Fundamental advances in {T}, paradigm shift, redefine {T}, {year}"
Keyword query:   "{specific_keywords_from_T} {year_range}"
Contrast query:  "Alternative to {current_paradigm_of_T}, beyond {T}, {year}"
```

### Phase 1: Broad Search (Parallel)

Execute search queries in parallel using alphaXiv MCP tools:
- Use `embedding_similarity_search` for semantic queries (captures conceptual matches)
- Use `full_text_papers_search` for keyword queries (captures exact term matches)

**Rules:**
- Launch 4-6 parallel searches covering different themes
- Each search returns up to 15 results
- Collect all results into a candidate pool
- Deduplicate by arXiv ID
- Filter by publication date (must be within the specified time range)

**Expected output:** 30-60 unique candidate papers with titles and abstracts.

### Phase 2: Initial Screening (LLM Judgment)

For each candidate paper, classify by the user's framework. Default framework (3-tier):

- **Tier 1 (Essence)**: "What IS X?" — Redefines the problem itself. Asks fundamental questions about the nature of learning, reasoning, action, perception, etc. These papers have lasting impact because they challenge assumptions.
- **Tier 2 (Engineering)**: "How to do X better?" — Optimizes within existing frameworks. Valuable but doesn't change paradigms. Examples: better MoE routing, improved training recipes, new benchmarks.
- **Tier 3 (Patch)**: "How to mitigate this symptom?" — Short-term fixes. Inference token pruning, fine-tuning tricks, quantization improvements.

**Rules:**
- Use ONLY title + abstract for screening (don't read full papers yet)
- Be selective: aim for 8-12 papers across all tiers
- Tier 1 should have 3-5 papers max
- Apply the user's specific keywords to boost relevance

**Expected output:** Classified paper list with tier assignments.

### Phase 3: Deep Reading (Parallel, Top Candidates Only)

For Tier 1 and top Tier 2 papers (4-6 papers max), use `get_paper_content` to retrieve full analysis.

**After reading each paper, immediately extract and cache:**
- Core contribution (1 sentence)
- Method keywords (3-5 terms)
- Best experimental result (1-2 numbers)
- Open-source links (GitHub URL if any)
- Venue acceptance status
- Key limitation

**Discard the raw full-text analysis after extraction** to manage context window.

### Phase 4: Impact Assessment

For each paper in the deep reading set, run the paper-impact-analyzer:

```bash
python path/to/paper-impact-analyzer/scripts/analyze.py {arxiv_id_1} {arxiv_id_2} ...
```

Merge impact data with the content analysis from Phase 3.

### Phase 5: Synthesize Report

Generate a structured Markdown report with the following sections:

```markdown
# {Topic} Paper Survey — {Date Range}

> Survey date: {today}
> Scope: {themes covered}
> Papers screened: {N candidates} → {M selected}

## Classification Framework
{Describe the tier system used}

## Tier 1 (Essence): Redefining the Problem
### Paper 1: {Title}
- **Essential question**: What fundamental assumption does this challenge?
- **Core contribution**: {1 sentence}
- **Key result**: {best number}
- **Impact**: {rating from analyzer} | {venue} | {github stars}
- **Links**: arXiv | GitHub
{... repeat for each Tier 1 paper}

## Tier 2 (Engineering): Doing It Better
| Paper | Contribution | Impact | Links |
|-------|-------------|--------|-------|
{table rows}

## Tier 3 (Patches): Symptom Relief
| Paper | What it fixes | Links |
|-------|--------------|-------|
{table rows}

## Top 3 Recommended Papers
{Ranked list with justification combining content depth + impact signals}

## Trends & Observations
{2-3 paragraphs on emerging patterns}
```

Save the report to `{working_directory}/{topic}-paper-survey-{date}.md`.

## Configuration

### Custom Classification Framework

Users can override the default 3-tier framework by specifying their own in the keywords file. The skill will use whatever framework the user provides.

### Search Depth Control

| Level | Searches | Deep reads | Best for |
|-------|----------|------------|----------|
| Quick | 4 | 2-3 | Weekly check-in |
| Standard | 6 | 4-6 | Monthly review |
| Thorough | 8-10 | 6-8 | Quarterly survey |

Default: Standard.

## Example Usage

```
Survey the last 3 months of papers in my research areas
```

```
Quick survey: what's new in LLM reasoning and agent tool-calling since January?
```

```
Thorough literature review on RL training methods for LLMs, classify by innovation tier
```
