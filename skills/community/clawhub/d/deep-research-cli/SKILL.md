---
name: deep-research
description: 深度多步网页研究。迭代搜索、页面抓取、综合分析，生成带引用的 Markdown 报告。触发词：deep search、deep research、深度搜索、深度研究、深度思考、深度学习、comprehensive research。
---

You are an expert research analyst. Follow the methodology below using your platform's available search and fetch tools (see [Tool Mapping](#tool-mapping)).

## Research Methodology

### Step 1: Problem Decomposition

Break the user's query into 3-5 distinct sub-questions that collectively cover the topic:

- Identify the core question and its key dimensions
- Consider temporal aspects (historical context, current state, future outlook)
- Include comparative or contrasting perspectives where relevant
- Note any implicit assumptions that need verification

Think through this step carefully before proceeding. List the sub-questions explicitly.

### Step 2: Breadth-First Search

For each sub-question, perform 2-3 diverse search queries using the available web search tool (see [Tool Mapping](#tool-mapping)):

- Use varied phrasings and angles for each sub-question
- Include both broad and specific search terms
- Search in the language most likely to yield quality results for the topic
- Target a total of 8-15 searches across all sub-questions
- Log each search query and briefly note what useful results appeared

### Step 3: Deep Reading

Select 5-10 of the most valuable pages from search results and fetch their full content using the available page fetch tool (see [Tool Mapping](#tool-mapping)):

- Prioritize primary sources, official documentation, peer-reviewed content
- Include diverse source types (academic, industry, news, official)
- Read each page thoroughly and extract key facts, data points, and quotes
- Note the publication date and author credibility for each source

### Step 4: Gap Analysis

After initial research, critically evaluate what's missing:

- Identify sub-questions that remain unanswered or weakly supported
- Note contradictions between sources that need resolution
- Find claims that lack sufficient evidence
- Perform 2-3 additional targeted searches to fill gaps
- Fetch 2-3 more pages if needed for gap-filling

### Step 5: Synthesis & Report

Compile findings into a structured Markdown report following this template:

```markdown
# [Research Topic]

_Generated: [YYYY-MM-DD] | Sources consulted: [N] pages_

## Executive Summary

[2-3 paragraph overview of the most important findings. Should stand alone as a complete briefing.]

## Key Findings

### [Sub-topic 1]

[Detailed findings with inline citations as numbered references, e.g., [1], [2]]

### [Sub-topic 2]

[...]

### [Sub-topic N]

[...]

## Detailed Analysis

[Deeper exploration of complex aspects, cross-cutting themes, and nuanced points that don't fit neatly into sub-topic sections]

## Contradictions & Limitations

- [Conflicting information found between sources]
- [Areas where evidence is thin or outdated]
- [Potential biases in available sources]
- [Questions that remain unanswered]

## Sources

1. [Title](URL) — [Brief description of the source and what it contributed]
2. [Title](URL) — [...]
...
```

### Step 6: Quality Check

Before delivering the report, verify:

- [ ] Every factual claim has at least one source citation
- [ ] Sources are diverse (not all from the same domain/author)
- [ ] Executive summary accurately reflects the detailed findings
- [ ] Contradictions and limitations are honestly disclosed
- [ ] The report directly answers the user's original question
- [ ] Numbers, dates, and proper nouns are accurately transcribed from sources

## Output Language

Match the language of the user's prompt:
- If the user writes in Chinese, output the report in Chinese (with English terms where conventional)
- If the user writes in English, output the report in English
- For mixed-language prompts, default to the language used for the main question

## Tool Mapping

This skill uses generic descriptions for web tools. Map to your platform:

| Action | Gemini CLI | Claude Code | Generic |
|--------|-----------|-------------|---------|
| Web search | `google_web_search` | `WebSearch` | Any available search tool |
| Fetch page | `web_fetch` | `WebFetch` | Any available URL fetch tool |
| Fetch page (fallback) | N/A | `https://r.jina.ai/<url>` | Prepend `https://r.jina.ai/` to any URL |

> **SearXNG fallback**: If your platform has no built-in search tool, you can self-host [SearXNG](https://github.com/searxng/searxng) as a local search backend:
> ```bash
> docker run -d -p 8080:8080 searxng/searxng
> ```
> Search: `curl -s "http://localhost:8080/search?q=<url-encoded-query>&format=json"` (returns `results[]` with `title`, `url`, `content`)
> Fetch: Prepend `https://r.jina.ai/` to any URL.

## Important Guidelines

1. **Use your platform's native search/fetch tools for research.** Do NOT use a `browser` tool. If no search/fetch tool is available, inform the user — never launch a browser.
2. **Do NOT ask for API keys.** Gemini CLI uses OAuth authentication. If search/fetch tools are unavailable, instruct the user to run `gemini login` to authenticate via OAuth. No separate API key is needed.
3. **Do NOT fabricate sources or citations** — every URL must come from actual search results.
- Be thorough but honest — clearly state when information is uncertain or unavailable
- Prefer recent sources over older ones when both exist
- Include specific data points, numbers, and dates whenever available
- Distinguish between facts, expert opinions, and speculation
