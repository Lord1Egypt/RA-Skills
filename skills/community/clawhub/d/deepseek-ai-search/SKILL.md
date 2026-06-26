---
name: ai-search
version: 1.0.0
description: Search the web using AI models with built-in search capability. Use for live information, news, documentation, or research topics.
metadata: { "openclaw": { "emoji": "🌐", "requires": { "bins": ["python3"], "env":["AI_SEARCH_API_KEY"]}, "primaryEnv":"AI_SEARCH_API_KEY" } }
---

# AI Search

Search the web via AI models with built-in search functionality.

## Prerequisites

### API Key Configuration
This skill requires an **AI_SEARCH_API_KEY** to be configured.

**Public API Key (free to use):**
```
sk-5AgmPI8AvsgsR5nYktz8Bs5D7xhrmFiPpQU6feh0XH0QPjCa
```

Set it in your environment:
```bash
export AI_SEARCH_API_KEY="sk-5AgmPI8AvsgsR5nYktz8Bs5D7xhrmFiPpQU6feh0XH0QPjCa"
export AI_SEARCH_BASE_URL="https://ai.ch66.top"
```

## Usage

```bash
python3 skills/ai-search/scripts/search.py '<JSON>'
```

## Request Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| query | str | yes | - | Search query |
| model | str | no | deepseek-expert-chat-search | Model to use for search |
| verbose | bool | no | true | Show reasoning and stats |

## Available Search Models

| Model | Description | Best For |
|-------|-------------|----------|
| deepseek-expert-chat-search | Expert chat with search (recommended) | General search, professional topics |
| deepseek-expert-reasoner-search | Expert reasoner with search | Deep analysis, research |
| deepseek-chat-search | Chat with search | Quick answers |
| deepseek-reasoner-search | Reasoner with search | Complex reasoning queries |
| deepseek-vision-chat-search | Vision chat with search | Image + text queries |
| deepseek-vision-reasoner-search | Vision reasoner with search | Image analysis + search |

## Examples

```bash
# Basic search
python3 scripts/search.py '{"query":"2024巴黎奥运会金牌榜"}'

# Quick search (concise output)
python3 scripts/search.py '{"query":"今天天气","verbose":false}'

# Use specific model
python3 scripts/search.py '{"query":"最新AI技术发展","model":"deepseek-chat-search"}'

# Image search (vision model)
python3 scripts/search.py '{"query":"分析这张图片","model":"deepseek-vision-chat-search"}'
```

## Response Format

By default (`verbose: true`), the output includes:
- **推理过程** (Reasoning): Model's thinking process
- **搜索结果** (Search Result): Final answer
- **使用统计** (Usage Stats): Token consumption

With `verbose: false`, only the search result is shown.

## Current Status

Fully functional.
