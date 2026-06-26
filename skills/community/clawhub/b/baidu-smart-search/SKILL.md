---
name: baidu-qianfan-search
description: Call Baidu Qianfan web search APIs to search the live web with AppBuilder credentials and return structured results. Use when a task specifically needs Baidu/Qianfan search, Chinese web-heavy retrieval, site-filtered search, recency-filtered search, or a reusable local skill wrapping the `/v2/ai_search/web_search` endpoint.
---

# Baidu Qianfan Search

Use this skill to query Baidu Qianfan's web search API and return structured search results without scraping websites directly.

## Quick start

1. Store the API key in an environment variable before running scripts:

```bash
export QIANFAN_APPBUILDER_API_KEY='...'
```

Or keep it in a local untracked file such as `.env.local` and source it manually:

```bash
set -a
source ./.env.local
set +a
```

2. Run the bundled script:

```bash
python3 scripts/qianfan_search.py "北京有哪些旅游景区"
```

3. For raw JSON debugging:

```bash
python3 scripts/qianfan_search.py "北京有哪些旅游景区" --raw
```

## Common patterns

### Basic web search

```bash
python3 scripts/qianfan_search.py "百度千帆平台"
```

### Restrict to specific sites

```bash
python3 scripts/qianfan_search.py "天气预报" --site weather.com.cn --site www.weather.com.cn
```

### Filter by recency

```bash
python3 scripts/qianfan_search.py "近期 AI 智能体新闻" --recency week
```

### Request images or videos too

```bash
python3 scripts/qianfan_search.py "故宫博物院" --web-top-k 5 --image-top-k 5 --video-top-k 3 --raw
```

## Output handling

- Default mode prints a normalized JSON object with `query`, `count`, `items`, and discovered `raw_keys`.
- `--raw` prints the full upstream JSON for troubleshooting or adapting to API changes.
- If Baidu changes response fields, inspect raw output first, then patch `scripts/qianfan_search.py`.

## Security rules

- Never place the real API key in `SKILL.md` or `references/`.
- Never publish `.env.local` to ClawHub.
- Before packaging or publishing, delete any local secret files from the skill folder or ensure the publisher excludes them.

## References

- Read `references/api.md` for the concise endpoint and parameter summary.
- Use `scripts/qianfan_search.py` as the canonical wrapper for the API.
