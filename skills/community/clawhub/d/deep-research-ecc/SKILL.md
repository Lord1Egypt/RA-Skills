---
name: deep-research-agent
description: "Conduct multi-source research with synthesized reports and citations. Searches the web, reads full content from key sources, and produces structured reports. Use when thorough research is needed on any topic with evidence attribution. Trigger phrases: research, deep dive, investigate, what's the current state of. Adapted from everything-claude-code by @affaan-m (MIT)"
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":[],"env":[]},"os":["darwin","linux","win32"]}}
---

# Deep Research

Produce thorough, cited research reports from multiple web sources using search and fetch tools.

## When to Activate

- User asks to research any topic in depth
- Competitive analysis, technology evaluation, or market sizing
- Due diligence on companies, investors, or technologies
- User says "research", "deep dive", "investigate", or "what's the current state of"

## Quick Start

1. Clarify goal — "learning, decision, or writing?"
2. Plan 3-5 research sub-questions
3. Execute multi-source search using `web_search` (15-30 sources total)
4. Deep-read 3-5 key sources with `web_fetch`
5. Synthesize findings into structured report with citations

## Key Concepts

- **Multi-source synthesis** — Combine data from academic, official, reputable news sources
- **Citation discipline** — Every claim must have a source; cross-reference critical facts
- **Recency focus** — Prefer sources from the last 12 months
- **Separate fact from inference** — Label estimates, projections, and opinions clearly
- **Acknowledge gaps** — Say "insufficient data found" rather than hallucinate

## Common Usage

Most frequent patterns:
- Competitive landscapes and market sizing
- Technology evaluations ("Rust vs Go")
- Business strategy research ("bootstrapping SaaS")
- Current events and trends
- Due diligence on companies or products

## References

- `references/workflow.md` — Detailed 6-step workflow with report template
- `references/examples.md` — Example research queries and output formats
