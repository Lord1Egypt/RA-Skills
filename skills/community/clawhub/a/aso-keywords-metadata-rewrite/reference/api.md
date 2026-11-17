# REST fallback

Without the AppGoat MCP server, call the API directly. Base URL `https://api.appgoat.ai/v1`,
header `x-api-key: $APPGOAT_API_KEY` (create a key at https://dash.appgoat.ai). Responses are
`{ "data": …, "meta": { "credits_used", "credits_remaining", … } }`; errors carry `error.hint`.

| MCP tool | REST call |
|---|---|
| `get_app` | `GET /apps/{app}?country=us` |
| `get_app_keywords` | `GET /apps/{app}/keywords?country=us&limit=200` (competitors: `&max_rank=20`) |
| `get_competitors` | `GET /apps/{app}/competitors?country=us&limit=8` |
| `keyword_research` (expand) | `GET /keywords?qs=seed1,seed2&store=apple&country=us&include=related` (≤ 5 seeds) |
| `keyword_research` (score) | `GET /keywords?qs=t1,t2,…&store=apple&country=us&app={app}` (≤ 25 terms) |
| `track_keywords` | `POST /tracked-keywords` `{"terms":[…],"store":"apple","countries":["us"]}` (0 credits) |
| `list_tracked_keywords` | `GET /tracked-keywords?store=apple&country=us` |
| `get_keyword_ranks` | `GET /tracked-keywords/{id}/ranks?app={app_id}` |

```bash
curl -s -G -H "x-api-key: $APPGOAT_API_KEY" https://api.appgoat.ai/v1/keywords \
  --data-urlencode "qs=habit tracker,daily routine" -d store=apple -d country=us -d app=284882215
```
