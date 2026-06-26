---
name: daum-toy-search
description: High-performance, multi-source Korean search API aggregating Daum/Kakao News, Encyclopedia, and Web results in a Perplexity-compatible format.
metadata: {"openclaw":{"emoji":"⚡","requires":{"bins":["node"],"env":["DAUM_TOY_SEARCH_API_KEY"]},"primaryEnv":"DAUM_TOY_SEARCH_API_KEY"}}
---

# Daum Toy Search

The `daum-toy-search` skill enables high-performance, multi-source Korean web search powered by the Daum/Kakao index. It is fully compatible with the Perplexity Search API format and includes intelligent 3x Jaccard reranking by default.

## Search

```bash
node {baseDir}/scripts/search.mjs "query"
node {baseDir}/scripts/search.mjs "query" -n 5
node {baseDir}/scripts/search.mjs "query" --sources news,web
```

## Options

- `-n <count>`: Target number of results (default: 10, max: 50).
- `--sources <sources>`: Comma-separated list of sources to include (`news`, `dic`, `web`). Default is all three.
- `--no-reranking`: Disable Jaccard keyword overlap reranker.

## Setup

```bash
openclaw config set skills.entries.daum-toy-search.apiKey "your-api-key"
```

Notes:
- Requires `DAUM_TOY_SEARCH_API_KEY` from your environment.
- Sub-400ms average latency powered by Go concurrency.
- Intelligent reranking automatically fetches 3x results and uses keyword overlap scoring.
- Returns clean, fully structured JSON hits ready for AI agents.

You can use `curl` to query the API from your OpenClaw agents:

```bash
curl -s -X POST "https://daum-perplexity-search-adapter.toy.x.upstage.ai/search" \
     -H "Authorization: Bearer $DAUM_TOY_SEARCH_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "인공지능 트렌드",
       "max_results": 5,
       "search_sources": ["news", "dic", "web"],
       "reranking": "on"
     }'
```

The response is a JSON object containing a `results` array with the search hits.
   
## Output Format

The `search.mjs` script outputs concise, formatted Markdown suitable for direct ingestion by AI agents:

```markdown
## Search Results for "인공지능 트렌드"

### 1. [업스테이지, '솔라' 한국형 LLM 성능 입증](https://news.daum.net/...)
**Source:** news | **Date:** 2026-03-09
업스테이지의 솔라 모델이 벤치마크 테스트에서...
```
