---
name: bohrium-web-search
description: "Web search via Bohrium's open-platform proxy (backed by searchapi.io). Use when: user needs to search the open web for research papers, documentation, tutorials, news, or general information. NOT for: academic database search (use bohrium-paper-search / bohrium-scholar-search), Bohrium knowledge base search."
---

# SKILL: Bohrium Web Search

## Overview

Proxy to searchapi.io via `open.bohrium.com`'s `/v1/search/web` endpoint. Issues keyword queries against the **open internet** and returns a list of hits with title, URL, and snippet.

**Use when**: locating a software's homepage, a blog post, a quick fact check, a news article.

**Don't use for**:

- Academic paper search → use `bohrium-paper-search` or `bohrium-scholar-search`
- Bohrium knowledge-base search → use `bohrium-knowledge-base`

**No CLI support** — HTTP API only. The `bohr` CLI ships a built-in `BohrWebSearch` tool that calls this endpoint automatically.

## Auth configuration

ACCESS_KEY comes from the OpenClaw config file `~/.openclaw/openclaw.json`:

```json
"bohrium-web-search": {
  "enabled": true,
  "apiKey": "YOUR_ACCESS_KEY",
  "env": {
    "ACCESS_KEY": "YOUR_ACCESS_KEY"
  }
}
```

OpenClaw injects `env.ACCESS_KEY` into the runtime.

## API

```
GET https://open.bohrium.com/openapi/v1/search/web?q=QUERY&num=N
Header: accessKey: $ACCESS_KEY
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `q` | string | required | Search query |
| `num` | int | `3` | Number of results, range `1-10` |

## Python example

```python
import os, requests

AK = os.environ["ACCESS_KEY"]
BASE = "https://open.bohrium.com/openapi/v1/search/web"

r = requests.get(BASE,
    headers={"accessKey": AK},
    params={"q": "graphene synthesis CVD", "num": 5})
data = r.json()

for i, hit in enumerate(data.get("organic_results", []), 1):
    print(f"[{i}] {hit['title']}")
    print(f"    {hit['link']}")
    print(f"    {hit.get('snippet', '')[:200]}")
    print()
```

**Response fields:**

| Field | Description |
|-------|-------------|
| `organic_results` | Array of main results |
| `organic_results[].title` | Page title |
| `organic_results[].link` | Page URL |
| `organic_results[].snippet` | Excerpt |
| `organic_results[].position` | Result rank |

## curl example

```bash
AK="YOUR_ACCESS_KEY"
curl -s "https://open.bohrium.com/openapi/v1/search/web?q=deepmd-kit&num=5" \
  -H "accessKey: $AK" | jq '.organic_results[] | {title, link, snippet}'
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `No organic_results` | No matches for the query | Rephrase; English queries generally return more hits than Chinese |
| `401` | Bad ACCESS_KEY | Check `accessKey` header case; don't use `Authorization: Bearer` |
| `num` ignored | Out of range | Must be `1-10`; values outside the range may be clamped or ignored |

## Pairs well with

- **web-search** to find a software's homepage → then **bohrium-job** to submit a job using it
- **web-search** to sanity-check a method name → then **bohrium-paper-search** to locate the original paper
- **web-search** for recent arxiv preprint URLs → hand off to **bohrium-pdf-parser**
