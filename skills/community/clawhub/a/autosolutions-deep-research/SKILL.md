---
name: deep-research
description: Conduct deep multi-phase research using parallel subagents and iterative search. Use for deep research requests, comprehensive analysis, competitive intelligence, market research, or thorough investigation of complex topics.
---

# Deep Research Skill

## Overview

This skill conducts thorough, multi-phase research using parallel subagents and iterative search methodology. It simulates ChatGPT Deep Research and Anthropic Deep Search by breaking complex topics into sub-questions, distributing work across 6-10 parallel research agents, and synthesizing findings into a structured report.

## When to Use

Use this skill when the user requests:
- Deep research on a topic
- Comprehensive analysis
- Competitive intelligence
- Market research
- Thorough investigation (not quick facts)
- Multi-angle exploration of complex subjects

## Research Methodology

### Core Principles

1. **Multi-pass queries** — Never one-and-done; iterate based on findings
2. **Source triangulation** — Verify claims across 3-5 independent sources
3. **Primary source hunting** — Find original studies, docs, not just blog posts
4. **Contradiction spotting** — Flag where sources disagree; don't hide uncertainty
5. **Synthesis over summary** — Connect dots, identify patterns, surface insights

### Parallel Agent Architecture

For deep research, spawn **6-10 subagents** to explore different angles simultaneously:

```
Research Lead (you)
├── Agent 1: Background & definitions
├── Agent 2: Market/industry landscape
├── Agent 3: Key players/competitors
├── Agent 4: Technology/trends
├── Agent 5: Challenges/risks
├── Agent 6: Opportunities/future outlook
├── Agent 7: Case studies/examples
├── Agent 8: Data/statistics
└── Agent 9-10: Specialized deep-dives (as needed)
```

### Search Tool Strategy

Use `web_search` with different modes per phase:

| Mode | Use Case |
|------|----------|
| `deep-reasoning` | Initial exploration, complex queries |
| `deep` | Broad topic coverage, 20-30 results |
| `neural` | Semantic matching, finding relevant pages |
| `fast` | Quick fact-checks, specific lookups |
| `instant` | Verifying names, dates, basic facts |

Use `web_fetch` to:
- Extract full article content from promising URLs
- Read primary sources, studies, documentation
- Get details that search snippets miss

## Workflow

### Phase 1: Scoping (5 min)

1. **Clarify the topic** — Ask user if the request is ambiguous
2. **Identify sub-questions** — Break the topic into 6-10 research angles
3. **Define success** — What does a good answer look like?

Example sub-question breakdown for "AI agent platforms":
- What are AI agent platforms and how do they work?
- What's the market size and growth trajectory?
- Who are the major players (established + startups)?
- What technologies power these platforms?
- What are the main use cases?
- What challenges/limitations exist?
- What's the competitive landscape?
- What trends are emerging?

### Phase 2: Parallel Research (15-25 min)

Spawn subagents with `sessions_spawn` for each research angle:

```bash
# Example subagent spawn
sessions_spawn(
  task="Research [specific angle]. Use web_search with mode=deep-reasoning, 20-30 results. Fetch full content from 5-10 key sources. Return: key findings, statistics, quotes with sources, contradictions spotted.",
  runtime="subagent",
  mode="run"
)
```

Each subagent should:
- Use appropriate `web_search` mode for their angle
- Fetch 5-10 full articles with `web_fetch`
- Return structured findings with source citations
- Flag uncertainties or conflicting information

### Phase 3: Synthesis (10-15 min)

As research lead, consolidate findings:

1. **Aggregate results** — Collect all subagent outputs
2. **Identify patterns** — What themes emerge across angles?
3. **Spot contradictions** — Where do sources disagree?
4. **Fill gaps** — Run targeted searches for missing pieces
5. **Verify claims** — Cross-check key statistics across sources

### Phase 4: Report Writing (10 min)

Structure the final report as follows:

## Output Format

```markdown
# [Research Topic]

## Executive Brief

[150-250 words: The 3-5 most important takeaways. Lead with the answer. What should the reader know after finishing this report?]

---

## 1. Background & Context

[Foundational information, definitions, why this matters]

## 2. [Key Theme 1]

[Deep dive with supporting evidence]

## 3. [Key Theme 2]

[Deep dive with supporting evidence]

## 4. [Key Theme 3]

[Deep dive with supporting evidence]

## 5. Challenges & Risks

[What could go wrong, limitations, open questions]

## 6. Opportunities & Outlook

[Future trends, emerging developments, what to watch]

## Key Takeaways

- [Bulleted summary of 5-7 most important points]

---

## Sources

[Numbered list with full URLs, titles, and 1-line context for each source]

1. [Title](URL) — [Brief context: what this source contributed]
2. [Title](URL) — [Brief context]
...
```

### Citation Guidelines

- **In-text** — Use numbered brackets: [1], [2-4], [5, 7]
- **Sources section** — Full URL, title, and 1-line context
- **Minimum sources** — 20-30 for deep research
- **Quality over quantity** — Prefer primary sources, industry reports, reputable publications

## Tool Usage

### web_search

```bash
# Broad exploration
web_search query="[topic]" type="deep-reasoning" count=30 freshness="year"

# Targeted lookup
web_search query="[specific fact]" type="fast" count=10

# Recent developments
web_search query="[topic]" type="neural" count=20 freshness="month"
```

### web_fetch

```bash
# Extract full content
web_fetch url="https://example.com/article" extractMode="markdown" maxChars=5000
```

### sessions_spawn (for parallel research)

```bash
# Spawn research subagent
sessions_spawn(
  task="Research [specific angle]. Search with mode=deep-reasoning, 25 results. Fetch 8-10 full articles. Return structured findings with citations.",
  runtime="subagent",
  mode="run"
)
```

## Quality Checks

Before delivering the report, verify:

- [ ] Executive brief captures the 3-5 most important takeaways
- [ ] All major claims have 2+ source citations
- [ ] Contradictions/uncertainties are flagged, not hidden
- [ ] Sources section has 20-30 entries with full URLs
- [ ] Report answers the original question thoroughly
- [ ] No obvious gaps in coverage

## Adaptation

### For Quick Research (<10 min)

- Skip subagent spawning
- Run 3-5 targeted searches yourself
- Aim for 10-15 sources
- Condense report structure

### For Ultra-Deep Research (60+ min)

- Spawn 10-15 subagents
- Include primary source documents, academic papers
- Add data tables, comparisons, timelines
- Include appendix with raw findings

## Notes

- **Context efficiency** — Subagents run in isolated sessions; only their findings load into your context
- **Parallelism** — Spawn all subagents at once, then `sessions_yield` to wait for completion
- **Iterative** — If initial findings reveal new angles, spawn follow-up agents
- **Time boxing** — Set `runTimeoutSeconds` on subagents to prevent runaway research
