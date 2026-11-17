# Run: execute a capability

Read this when you run a capability: input, previews and `items`, async tasks
and polling, idempotency, text models, JEV. Step 3 of the Search → Inspect → Run
loop in the main Skill (<https://beatapi.io/skill.md>). Run needs the key.

```sh
curl -sS -X POST https://api.beatapi.io/v1/capabilities/run \
  -H "Authorization: Bearer $BEATAPI_API_KEY" -H 'Content-Type: application/json' \
  -d '{"reference":"data:xiaohongshu.app_v2.search_notes","input":{"keyword":"AI 视频"},"view":"preview"}'
```

Over MCP, pass the same JSON to `capabilities_run`.

- `input` follows the inspected `input_schema`; unknown fields inside `input`
  are rejected, and a missing required field is refused with 400 naming it
  (`Missing required input: keyword`). The direct `/v1/chat/completions`,
  `/v1/responses` and `/v1/messages` endpoints ignore unknown fields instead, as
  OpenAI's API does. Send a unique `idempotency_key` per task as a top-level field of
  the Run body, next to `reference` and `input` (or as an `Idempotency-Key`
  header), and reuse it only to retry the same task.
- **Sync** capabilities (social data, web search/read/map, text models, JEV)
  return the result. Send `"view":"preview"` for data: when the result has a
  list, it is in `items` (the first `max_items`, default 10, up to 50, each
  trimmed), with `items_total` and `items_path` (where the list sits in the
  full result), so you never hunt for it. A trimmed result has `result_ref` and
  a `next`: for more, send
  `{"reference":"<same reference>","operation":"result","request_id":"<request_id>","fields":["items[].<key>"]}`
  with keys you saw in `items` (free within an hour). `items` comes with
  `"view":"preview"` or `items[]` fields; without a view the result is the
  platform's own shape. Array indexes such as `[0]` are refused: use `[]` and
  `max_items` (`items_path` itself may contain `[]` when the list sits inside
  another array). Sync data and web results carry `usage`
  (`billing_unit`, `quantity`, `price_usd`): that is what the call cost.
- **Async** capabilities (image, video, workflows and `data:web.research`)
  return a task `id` and a `next` status call,
  `{"reference":"<same reference>","operation":"status","task_id":"<id>"}`.
  Repeat it until `succeeded` or `failed`, waiting the task's
  `poll_after_seconds` between calls (5 s for images, 8 s for video, 10 s for
  workflows and research); the result is in `data.output` (`media[]`; read
  `media[0].url` — `r2_url` is the same value, now deprecated). A running task
  may also carry `typical_seconds` (`p50`, `p90`, `samples`, `window`): how long
  that model recently took from accepted to done. Past `p90` with no change,
  tell the user it is running long; there is no ETA beyond that, and `queued`
  can last several minutes on some models. Over MCP only research waits (up to
  45 s) before answering; an image or video task comes back at once. A music
  video can also stop at `requires_action` or `storyboard_ready`, which needs
  the user's choice.
- **Text models** run the same way: `{"reference":"model:<id>","input":{"input":"<prompt>"}}`
  returns `output_text`; `usage` token counts may include upstream system prompts
  and are not comparable across models. **Decision model** JEV:
  `{"reference":"model:jev-1.13-free","input":{"state":"…","questions":{…}}}` returns
  typed answers with probabilities (question types `noul`, `choice`, `score`;
  a `noul` needs `instructions`, the yes/no question; `score` takes
  at most 10 criteria). To rank many candidates use **one** call:
  a `choice` question listing all of them, or one question per candidate.
  Inspect either model for its full schema.
- A run spends the account balance. The user's explicit request authorizes that
  task; start small.
- If the user already has their own tool or key for the job, use theirs: offer
  BeatAPI, don't override it.

A failed call or task: <https://beatapi.io/skill-refs/errors.md>.
