---
name: deep-research-engine
description: Autonomous deep research agent with multi-step web search, sub-agent delegation, and structured report generation. Triggered by requests for deep research, 深度研究, literature review, or comprehensive topic analysis.
author: ClawX
version: 0.1.0
dependencies:
  - pip: deepagents
  - pip: tavily-python
  - pip: langchain-anthropic
  - pip: markdownify
---

# Deep Research Agent

## When to Use

Trigger this skill when the user asks for:
- 深度研究 / deep research on any topic
- Comprehensive topic analysis with citations
- Literature review or academic research
- "Research [X]" where a thorough, multi-source report is needed
- Comparison reports (products, technologies, methodologies)
- Market research or competitive analysis

**NOT** for quick lookups — use web_search for simple questions.

## Prerequisites

1. **Tavily API key** (free): https://tavily.com/
2. **LLM API key**: Anthropic, Google, or OpenAI

Set environment variables before first use:
```bash
export TAVILY_API_KEY="your_key"
export ANTHROPIC_API_KEY="your_key"  # or GOOGLE_API_KEY / OPENAI_API_KEY
```

## Workflow

When triggered, follow this deep research process:

### Phase 1: Plan 📋
1. Analyze the research question
2. Break it down into 2-5 focused sub-topics
3. Create a research plan with specific tasks

### Phase 2: Search 🔍
1. For each sub-topic, use `web_search` tool to discover key information
2. Use `web_fetch` to read important pages in full
3. Take notes on key findings from each source
4. If a sub-topic yields insufficient info, refine search queries

### Phase 3: Synthesize 📝
1. Consolidate findings from all sources
2. Identify contradictions or gaps
3. Form evidence-based conclusions
4. Generate inline citations for all claims

### Phase 4: Report 📄
Output a structured report with:
- **Executive Summary** — Key findings at a glance
- **Background** — Context and definitions
- **Detailed Analysis** — Evidence-backed exploration
- **Comparison/Insights** (if applicable)
- **Conclusion** — Actionable takeaways
- **Sources** — Numbered list of all references (inline `[1]`, `[2]`, etc.)

## Alternative: Python Backend

For truly deep research (autonomous multi-hour sessions with Tavily), use the bundled Python script:

```bash
cd deep-research-agent/backend
pip install -r requirements.txt
python agent.py "Research topic here"
```

This spawns sub-agents for parallel research and writes `/final_report.md`.

## Prompt Template (Substitute & Execute)

For quick in-session deep research (no backend needed), follow this prompt structure:

```
Perform deep research on: "{user_query}"

Research Guidelines:
1. Use web_search with at least 3 different query variations
2. Read at least 5 sources thoroughly via web_fetch
3. Cross-reference claims across sources
4. Cite inline with [1], [2], etc.
5. Note confidence levels for uncertain claims
6. Write a comprehensive report with sections
```
