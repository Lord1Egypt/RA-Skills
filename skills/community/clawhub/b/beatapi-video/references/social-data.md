# Social Data actions

Use the public BeatAPI action catalog. Never guess a provider path or expose a
provider name to the user.

## Discover and inspect

Prefer the unified MCP tools when available:

```text
capabilities_search({"query":"小红书 搜索笔记"})
capabilities_inspect({"reference":"data:xiaohongshu.app_v2.search_notes"})
```

Copy the `reference` from the Search result; Inspect returns the input schema,
price, `readiness` and a ready-to-fill `next` Run call. A query naming only a
platform (`"小红书"`) returns an overview of what the platform offers. The catalog is also available as
`https://beatapi.io/social-data-catalog.json`.

## Run an action

```text
capabilities_run({
  "reference":"data:xiaohongshu.app_v2.search_notes",
  "input":{"keyword":"AI 视频"},
  "view":"preview",
  "idempotency_key":"social-data-run-001"
})
```

For a synchronous Social Data result, the public response has this shape:

```json
{
  "object":"social_data.call",
  "status":"succeeded",
  "request_id":"req_...",
  "action":"douyin.web.fetch_one_video",
  "data":{}
}
```

BeatAPI removes provider names, provider request IDs, cache URLs, routing
fields, and raw provider errors. Do not rely on those fields or ask the user
to configure an upstream account.

Failed calls do not consume credits. Use the same idempotency key only when
retrying the same request. Stable error codes include `bad_request`,
`processing_unavailable`, `insufficient_credits`, `not_found`,
`idempotency_conflict`, and `rate_limit_exceeded`.

The direct REST form is:

```bash
curl https://api.beatapi.io/v1/social-data/call \
  -H "Authorization: Bearer $BEATAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"action":"douyin.web.fetch_one_video","params":{"aweme_id":"7364837462110"}}'
```

The action catalog's `input_schema` defines required fields and types. GET
actions use scalar parameters; POST actions use a JSON object. The request body
limit is 512 KiB.
