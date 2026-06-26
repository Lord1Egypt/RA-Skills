---
name: exa-search
description: Semantic search, web scraping, and content extraction optimized for AI Agents and LLMs. Use when you need highly relevant web search, clean Markdown extraction, extractive highlights, or similarity searches.
metadata:
  author: Simon-Pierre Boucher
---

# Exa Search Skill

This skill extends Manus's capabilities with a custom-built, semantic search engine optimized specifically for AI agents and LLMs. It enables neural search, clean Markdown extraction, extractive query highlights, and conceptual similarity searches.

## When to Use

Use this skill when:
1. You need to search the web using complex natural language prompts rather than raw keywords.
2. You need clean, boilerplate-free Markdown text from web pages for LLM context windows.
3. You need query-relevant extractive snippets (`highlights`) to reduce token consumption.
4. You need to perform similarity searches using an existing URL as a conceptual query.
5. You need to perform deep, multi-step web research or build structured lists using schema validation.

## Core Capabilities & Commands

### 1. Neural Search (`/search`)
Query Exa's index using semantic embeddings. Unlike keyword matching, this understands the conceptual meaning of your prompt.

```python
from exa_py import Exa
exa = Exa(api_key="YOUR_EXA_API_KEY")

results = exa.search(
    query="companies building innovative fusion energy reactors",
    type="auto",
    num_results=5,
    contents={"highlights": True}
)
```

### 2. Clean Web Extraction (`/contents`)
Retrieve webpage content stripped of navigation menus, sidebars, advertisements, and other boilerplate, returned as clean Markdown.

```python
contents = exa.get_contents(
    urls=["https://example.com/target-article"],
    text=True,
    max_age_hours=24
)
```

### 3. Similar Link Discovery (`/findSimilar`)
Find conceptually similar pages in Exa's index using a starting URL as your query.

```python
similar = exa.find_similar(
    url="https://arxiv.org/abs/2307.06435",
    num_results=5
)
```

## Advanced Workflows & Best Practices

### Cache Freshness & Live Crawling
By default, Exa serves cached pages to optimize speed. To control cache freshness, use `max_age_hours` instead of deprecated livecrawl parameters:
* `max_age_hours=0`: Forces a live crawl of the URL.
* `max_age_hours=1`: Uses cache if it's less than 1 hour old, otherwise performs a live crawl.
* `max_age_hours=-1`: Cache-only lookup (never crawl).

### Subpage Crawling
Automatically discover and extract content from linked subpages on a target site. Highly effective for documentation or news archives:
```python
results = exa.get_contents(
    ["https://docs.exa.ai"],
    subpages=10,
    subpage_target=["api", "reference"],
    max_age_hours=24
)
```

### RAG Integration Pattern
Always format extracted contents cleanly into XML blocks for downstream LLM generation:
```python
context = "\n".join([
    f"<source><url>{r.url}</url><highlights>{r.highlights}</highlights></source>"
    for r in results.results
])
```

## References & Resources

* Detailed API endpoints and SDK configurations: [API Reference](references/api_reference.md)
* Command-line search utility: Execute `/home/ubuntu/skills/exa-search/scripts/exa_search.py --help`
