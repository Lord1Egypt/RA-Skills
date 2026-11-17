# REST fallback

Without the AppGoat MCP server, call the API directly. Base URL `https://api.appgoat.ai/v1`,
header `x-api-key: $APPGOAT_API_KEY` (create a key at https://dash.appgoat.ai). Responses are
`{ "data": …, "meta": { "credits_used", "credits_remaining", … } }`; errors are
`{ "error": { "code", "message", "hint", "approve_url"? } }` - read `hint`.

| MCP tool | REST call |
|---|---|
| `list_connections` | `GET /connections?provider=apple_ads` (free) |
| `read_connection` view=campaigns | `GET /connections/{id}/ads?view=campaigns` |
| `read_connection` view=ad_groups | `GET /connections/{id}/ads?view=ad_groups&campaign_id=…` |
| `read_connection` view=keywords | `GET /connections/{id}/ads?view=keywords&campaign_id=…&ad_group_id=…` |
| `read_connection` view=negatives | `GET /connections/{id}/ads?view=negatives&campaign_id=…` |
| `read_connection` view=report | `GET /connections/{id}/ads?view=report&level=keywords\|searchterms&campaign_id=…&start=YYYY-MM-DD&end=YYYY-MM-DD` |
| `keyword_research` | `GET /keywords?qs=term1,term2&store=apple&country=us` |
| `propose_action` | `POST /actions` with `"dry_run": true, "source": "playbook:apple-ads-optimizer"` (free) |
| `apply_action` | `POST /actions/{id}/approve` (1 credit when applied) |
| `reject_action` | `POST /actions/{id}/reject` (free) |

Report rows: `{ dims, impressions, taps, installs, spend, currency, avg_cpt, avg_cpa, ttr,
conversion_rate }`; `dims` holds Apple's row metadata (Apple Ads Platform API: keyword id, text
and match type, ad group id and bid for keywords; the search term, its source and the matched
keyword for search terms). Keyword `status` is `ENABLED` or `PAUSED` (`ACTIVE` is accepted as an
alias). The connection's `account` shows the `ad_account_id` it acts on.

```bash
CON=con_… CAMPAIGN=123456
curl -s -G -H "x-api-key: $APPGOAT_API_KEY" "https://api.appgoat.ai/v1/connections/$CON/ads" \
  -d view=report -d level=searchterms -d campaign_id=$CAMPAIGN -d start=2026-10-08 -d end=2026-10-21 \
  | jq -r '.data.rows[] | "\(.dims.searchTerm // .dims.searchTermText)\t\(.taps)\t\(.installs)\t\(.spend)"'

# Bids for one ad group, as a dry run
curl -s -H "x-api-key: $APPGOAT_API_KEY" -H "content-type: application/json" https://api.appgoat.ai/v1/actions \
  -d '{"type":"ads.keyword.bid","connection":"'$CON'","dry_run":true,"source":"playbook:apple-ads-optimizer",
       "params":{"campaign_id":"'$CAMPAIGN'","ad_group_id":"789","max_increase":0.3,
                 "keywords":[{"id":"111","bid":1.3},{"id":"112","status":"PAUSED"}]}}' | jq '.data | {id, diff, guardrail}'
```
