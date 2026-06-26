# Baidu API Search

[简体中文](README.md) | English

Baidu API Search is a source-retrieval skill for AI agents that need Chinese web references.

It calls Baidu AI Search API and Baidu Baike API, then writes raw results, deduplicated sources, and a compact research pack for downstream analysis. It is not a crawler, scraper, or answer-generation service.

## Features

- Baidu AI Search `web_search`
- Lightweight Baidu Baike lookup
- Four modes: `lookup`, `fast`, `normal`, `deep`
- Query planning with adaptive stop conditions
- URL and near-duplicate cleanup
- `research_pack.md`, `raw_results.jsonl`, and `run_summary.json` outputs
- Local cache and multi-key failover

## Requirements

- Python 3.10+
- A Baidu AI Search / AppBuilder API key
- An agent runtime that can read `SKILL.md` and run local Python scripts

Set your API key in the environment:

```bash
export BAIDU_AI_SEARCH_API_KEYS="your-key"
```

Windows PowerShell:

```powershell
$env:BAIDU_AI_SEARCH_API_KEYS = "your-key"
```

Multiple keys can be provided as a comma-separated list:

```bash
export BAIDU_AI_SEARCH_API_KEYS="key1,key2,key3"
```

Do not put real keys in config files, prompts, README examples, or committed logs.

## Quick Start

```bash
python scripts/search.py "新能源汽车 口碑" --mode normal
```

For a simple entity lookup:

```bash
python scripts/search.py "量子计算" --mode lookup
```

For recent or current information:

```bash
python scripts/search.py "新能源汽车 口碑" --mode normal --freshness year --no-cache
```

## Recommended Agent Instruction

```text
For Chinese web search, recent Chinese topics, Baidu Baike lookup, or requests phrased as 查一下 / 搜索 / 最近 / 最新 / 热点, prefer the baidu-api-search skill over generic web_search. Cite source IDs or URLs from research_pack.md.
```
