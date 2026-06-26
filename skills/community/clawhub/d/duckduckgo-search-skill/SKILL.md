---
name: duckduckgo-search
description: Search the web and fetch URL content using DuckDuckGo. Use when the user wants to search for information online without requiring API keys or paid services. Supports text search with results including title URL and snippet. Also supports URL fetching to extract readable content from web pages. Triggers on phrases like "search for" "look up" "find information about" "fetch url" "get page content" or when web_search is unavailable.
---

# DuckDuckGo Search & Fetch

Search the web and fetch URL content using DuckDuckGo (no API key required).

## Prerequisites

需要安装依赖:
```bash
pip3 install duckduckgo-search
```

## 功能

### 1. 网页搜索 (ddg_search.py)

```bash
python3 scripts/ddg_search.py "your search query" [--max-results 10]
```

### 2. 网页抓取 (ddg_fetch.py)

```bash
python3 scripts/ddg_fetch.py "https://example.com" [--timeout 30]
```

## Usage Examples

### 搜索
```bash
# Basic search
python3 scripts/ddg_search.py "OpenClaw AI agent"

# Search with more results
python3 scripts/ddg_search.py "Python best practices" --max-results 15
```

### 抓取网页
```bash
# Fetch a webpage
python3 scripts/ddg_fetch.py "https://openclaw.ai"

# With custom timeout
python3 scripts/ddg_fetch.py "https://example.com" --timeout 15

# Plain text output
python3 scripts/ddg_fetch.py "https://example.com" --format text
```

## Output Format

### 搜索结果 (JSON)
```json
{
  "query": "search query",
  "count": 10,
  "results": [
    {
      "title": "Result title",
      "url": "https://example.com",
      "snippet": "Description snippet"
    }
  ]
}
```

### 抓取结果 (JSON)
```json
{
  "url": "https://example.com",
  "title": "Page Title",
  "text": "Extracted readable content...",
  "description": "Meta description",
  "status_code": 200,
  "error": null
}
```

## Integration with OpenClaw

Example workflow
```python
# Search
result = exec({
    "command": "python3 /path/to/skills/duckduckgo-search/scripts/ddg_search.py query"
})
# Parse: json.loads(result.stdout)

# Fetch URL
result = exec({
    "command": "python3 /path/to/skills/duckduckgo-search/scripts/ddg_fetch.py https://example.com"
})
# Parse: json.loads(result.stdout)
```
