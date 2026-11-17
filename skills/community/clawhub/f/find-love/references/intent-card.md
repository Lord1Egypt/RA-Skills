# Intent Card

`showme/v1` remains the common profile envelope. Add `intents` only when a person wants to publish a searchable request. Old readers can safely ignore it.

```json
{
  "schema": "showme/v1",
  "id": "github:example",
  "name": "小林",
  "github": "example",
  "city": "深圳",
  "bio": "做产品和 AI 工具，周末喜欢徒步和看展。",
  "contact": { "email": "hello@example.com" },
  "intents": [
    {
      "kind": "dating",
      "title": "寻找长期、认真相处的伴侣",
      "looking_for": "愿意沟通、在深圳或能稳定见面的人。",
      "topics": ["AI", "徒步", "看展"],
      "cities": ["深圳"],
      "status": "open",
      "updated_at": "2026-09-16T00:00:00.000Z"
    }
  ]
}
```

## Fields

- `kind`: one of `dating`, `activity`, `business`, `supplier`, `collaboration`, `hiring`.
- `title`: a human-readable request, not a slogan.
- `looking_for`: the fit and boundaries the user wants public.
- `topics`: 2-5 searchable hooks.
- `cities`: relevant city names, or an empty array for remote/online.
- `status`: `open`, `paused`, or `closed`. Do not index closed requests in a later registry version.
- `updated_at`: ISO-8601 timestamp. Refresh this when materially changing the request.

## Dating Guidance

Keep it adult-only, mutual, and specific. A useful card says what daily life or values the person hopes to share, not a long checklist of demands. Do not publish an exact home/work location, private photos, government IDs, financial details, or contact data that should not be searchable.
