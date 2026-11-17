# REST fallback

Without the AppGoat MCP server, call the API directly. Base URL `https://api.appgoat.ai/v1`,
header `x-api-key: $APPGOAT_API_KEY` (create a key at https://dash.appgoat.ai). Responses are
`{ "data": …, "meta": { "credits_used", "credits_remaining", … } }`; errors carry `error.hint`.

| MCP tool | REST call |
|---|---|
| `get_charts` | `GET /charts?store=apple&country=us&chart=free&category=6013` |
| `keyword_research` (expand) | `GET /keywords?qs=habit tracker,adhd planner&store=apple&country=us&include=related,suggestions` |
| `keyword_research` (measure) | `GET /keywords?qs=term1,term2,…&store=apple&country=us&include=top_apps` (≤ 25 terms) |
| `get_app` | `GET /apps/{app}?store=apple&country=us` |
| `search_apps` | `GET /search?q=habit tracker&store=apple&limit=20` |
| `get_reviews` | `GET /apps/{app}/reviews?country=us&rating=1-2&limit=100` |
| `get_job` | `GET /jobs/{id}` (free) |

```bash
curl -s -G -H "x-api-key: $APPGOAT_API_KEY" https://api.appgoat.ai/v1/keywords \
  --data-urlencode "qs=habit tracker,adhd planner" -d store=apple -d country=us -d include=top_apps
```
