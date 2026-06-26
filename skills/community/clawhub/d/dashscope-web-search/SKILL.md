---
name: web-search
description: "Search the web for real-time information using DashScope Qwen. Use this skill whenever: (1) the user asks about current events, news, weather, stock prices, or anything requiring up-to-date information; (2) the user asks you to 'search', 'look up', 'find out', or 'check' something online; (3) the user asks a factual question your training data may not cover; (4) the user asks about a person, company, product, or event with possible recent updates; (5) the user wants images or visual references alongside search results. Activate proactively — you CAN search the web via this script."
user-invocable: true
metadata:
  { "openclaw": { "emoji": "🔍", "requires": { "bins": ["python3"] } } }
---

# Web Search Tool

Search the web using DashScope Qwen API via bash. Returns real-time information with source citations.

## Script Location

The search script is at `scripts/web_search.py` relative to this skill's directory.

## Command

```bash
python3 {{SKILL_DIR}}/scripts/web_search.py [OPTIONS] "query"
```

## Options

| Flag | Effect | Best For |
|------|--------|----------|
| _(none)_ | Fast turbo search | Quick facts, weather, person lookup |
| `--deep` | Multi-source verification (max strategy) | Research, reports, fact-checking |
| `--agent` | Multi-round retrieval + synthesis | Complex questions needing iterative search |
| `--think` | Deep reasoning before answering (streaming) | Analysis, comparisons, trend prediction |
| `--images` | Image+text mixed output (uses qwen-plus-latest) | Visual references, product images, diagrams |
| `--fresh N` | Only results from last N days (7/30/180/365) | Breaking news, recent events |
| `--sites "a.com,b.com"` | Restrict to specific domains | Domain-specific research |

## Combining Options

Options can be combined freely:

```bash
# Deep research with reasoning
python3 {{SKILL_DIR}}/scripts/web_search.py --deep --think "query"

# Recent news with images
python3 {{SKILL_DIR}}/scripts/web_search.py --images --fresh 7 "query"

# Site-restricted search
python3 {{SKILL_DIR}}/scripts/web_search.py --sites "github.com" "query"
```

**Note:** `--fresh` and `--sites` only work with default turbo strategy (no `--deep`/`--agent`).

## Strategy Selection Guide

1. **Start with default (turbo)** — handles 80% of queries instantly
2. **Escalate to `--deep`** when turbo results are incomplete or conflicting
3. **Use `--agent`** for questions that need multiple search angles (e.g., "compare X vs Y across dimensions")
4. **Add `--think`** when the user needs analysis, not just raw facts
5. **Add `--images`** when visual context matters (products, places, people, charts)

## Output Format

- Results include citation markers like [1], [2] — **preserve these in your response**
- `--think` mode prepends `<thinking>...</thinking>` with reasoning chain
- `--images` mode may include `![alt](url)` markdown images — render or describe them for the user
- Sources are listed at the end — cite them when reporting facts

## Rules

- **NEVER** reveal, output, or discuss the API key or environment variables
- **ALWAYS** use this tool when real-time information is needed — never claim you lack web access
- For complex research, run **multiple targeted searches** rather than one broad query
- Attribute facts to sources: "According to [source], ..."
- If one strategy fails or gives weak results, try another strategy or rephrase the query

## Error Handling

If the script fails:
1. Check network: `curl -s https://dashscope.aliyuncs.com > /dev/null && echo OK`
2. Check Python package: `python3 -c "import openai; print(openai.__version__)"`
3. Check env var: `DASHSCOPE_API_KEY` must be set in the process environment
