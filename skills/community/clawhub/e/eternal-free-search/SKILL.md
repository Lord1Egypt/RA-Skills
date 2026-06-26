---
name: ddg-search
description: Free web search using DuckDuckGo (no API key needed). Use when you need to search the web for any information — news, facts, research, people, companies, products, or anything else. Triggers on any web search need. Provides web search, news search, image search, and Q&A capabilities. As an alternative to paid search APIs.
---

# DDG Search — Free Web Search

Web search via DuckDuckGo. No API key, no subscription, no limits.

## Usage

```bash
python3 scripts/search.py "your query"
python3 scripts/search.py --news "breaking news topic"
python3 scripts/search.py --qna "what is quantum computing"
python3 scripts/search.py --images "sunset photos"
python3 scripts/search.py --max 10 "detailed research query"
```

## Commands

| Mode | Flag | Description |
|------|------|-------------|
| Web | (default) | Standard web search results |
| News | `--news` | Recent news articles |
| Q&A | `--qna` | Instant answer from DuckDuckGo |
| Images | `--images` | Image search results |
| Suggestions | `--suggest` | Search suggestions/autocomplete |

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--max` | 5 | Number of results |
| `--region` | wt-wt | Region code (us-en, uk-en, etc) |
| `--time` | | Time filter: d/w/m/y (day/week/month/year) |
| `--json` | | Output as JSON |

## Examples

```bash
# Quick search
python3 scripts/search.py "Python 3.13 features"

# News from last week
python3 scripts/search.py --news --time w "AI regulation"

# Get instant answer
python3 scripts/search.py --qna "capital of France"
```
