# Baidu AI Search API Notes

Use this reference before changing request/auth behavior.

## Endpoint

```text
POST https://qianfan.baidubce.com/v2/ai_search/web_search
```

This skill targets the web search endpoint because it returns raw-ish `references` suitable for downstream AI analysis. Do not replace it with generated answer endpoints when the user asks for original information.

## Request Shape

The current script builds this payload:

```json
{
  "messages": [{"role": "user", "content": "新能源汽车 口碑"}],
  "search_source": "baidu_search_v2",
  "resource_type_filter": [{"type": "web", "top_k": 50}]
}
```

For low-latency discovery, `fast` mode may add:

```json
{
  "edition": "lite"
}
```

`lite` reduces recall/reranking depth for better latency. Use `standard` for normal and deep research.

Optional filters:

```json
{
  "search_filter": {
    "match": {
      "site": ["example.com"]
    },
    "items": {
      "block_websites": ["spam.example"]
    }
  },
  "search_recency_filter": "year"
}
```

`search_recency_filter` accepts `week`, `month`, `semiyear`, or `year`. The exact advanced filter grammar should be verified with live API testing before relying on site or block filters. Basic `messages`, `search_source`, `resource_type_filter`, and optional `edition` are the core contract.

## Authentication

Do not hardcode keys. Use:

```text
BAIDU_AI_SEARCH_API_KEYS=key1,key2,key3
```

The script can send both:

```text
Authorization: Bearer <key>
X-Appbuilder-Authorization: Bearer <key>
```

If live testing shows only one header is accepted, use `--auth-header authorization` or `--auth-header x-appbuilder`.

## Limits

- `top_k` is clamped to 50.
- `edition` can be `standard` or `lite`; `standard` remains the default for research.
- There is no known offset/page/next-token for `web_search`.
- Multiple keys should not be treated as pagination for the same query.
- Repeated identical calls should use the local query cache unless the task requires current/latest results.

## Expected Response

The response should expose `references` either at the top level or under `data.references`. The scripts accept both.

Useful fields:

```text
title
url
date
content
snippet
website
type
markdown_text
rerank_score
authority_score
```

## Live Testing Checklist

When an API key is available:

1. Run `baidu_web_search.py --query "新能源汽车 口碑" --top-k 10 --output smoke.json`.
2. Confirm the response contains `references`.
3. Run `run_search_plan.py` with a tiny 2-query plan.
4. Confirm `raw_results.jsonl` has one reference per line.
5. Confirm no key is printed in logs.

## Cache Safety

The cache stores endpoint, payload, raw API response, and timestamp. It must not store API keys, Authorization headers, or full key identifiers. Cached responses should use `key_id: "cache"` in downstream raw results.
