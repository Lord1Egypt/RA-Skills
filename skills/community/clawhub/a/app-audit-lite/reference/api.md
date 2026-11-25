# REST fallback

Without the AppGoat MCP server, call the API directly. Base URL `https://api.appgoat.ai/v1`,
header `x-api-key: $APPGOAT_API_KEY` (create a key at https://dash.appgoat.ai). Responses are
`{ "data": …, "meta": { "credits_used", "credits_remaining", "freshness", "next_cursor", "warnings" } }`;
errors are `{ "error": { "code", "message", "hint" } }` - read `hint`. `{app}` must be URL-encoded.

| MCP tool | REST call |
|---|---|
| `get_app` | `GET /apps/{app}?country=us&include=versions,charts` |
| `get_app_history` | `GET /apps/{app}/history?country=us&from=YYYY-MM-DD` |
| `get_reviews` | `GET /apps/{app}/reviews?country=us&rating=1-2&limit=100` |
| `get_app_keywords` | `GET /apps/{app}/keywords?country=us&limit=100` |
| `get_competitors` | `GET /apps/{app}/competitors?country=us&limit=5` |
| `get_app_changes` | `GET /apps/{app}/changes?field=title,subtitle&since=YYYY-MM-DD` |
| `keyword_research` | `GET /keywords?qs=term1,term2&store=apple&country=us&app={app}` |
| `get_job` | `GET /jobs/{id}` (free) |
| `audit_app` (full audit) | `POST /apps/{app}/audit` with body `{"country": "us"}` (100 credits, first one free; 202 while running) |
| `get_audit` | `GET /audits/{id}` (free) |

```bash
curl -s -H "x-api-key: $APPGOAT_API_KEY" \
  "https://api.appgoat.ai/v1/apps/$(python3 -c 'import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1],safe=""))' 'https://apps.apple.com/us/app/id284882215')?country=us"
```
