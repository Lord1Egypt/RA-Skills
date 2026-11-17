# Search: find a capability

Read this when a search returns nothing useful, or you want filters, platform
overviews or paging. Step 1 of the Search → Inspect → Run loop in the main Skill
(<https://beatapi.io/skill.md>). Search needs no key.

```sh
curl -sS -X POST https://api.beatapi.io/v1/capabilities/search \
  -H 'Content-Type: application/json' -d '{"query":"小红书 搜索笔记"}'
```

Over MCP, pass the same JSON to `capabilities_search`.

- Write the query the way the user would: platform + action, in Chinese or
  English. Examples: `"小红书 搜索笔记"`, `"抖音 用户作品"`, `"tiktok user profile"`,
  `"B站 视频评论"`, `"video model"`, `"文本模型"`, `"决策"`, `"联网搜索"`.
- A query naming only a platform (`"小红书"`) returns an **overview**: `groups` of
  what the platform offers (search, content, comments, users, trends, …), each
  with example references and the `search` arguments that list the rest.
  An empty query returns the whole catalogue map.
- Each card has `reference`, `summary`, `price`, `readiness` and an input `signature`.
- The search payload (the REST reply's `data` object) carries `understood`
  (matched words), `hints` (rephrasing advice), and, for specific queries, `recommended`.
  `recommended` contains the top `reference`, `why_match` and `missing_inputs`.
  When `readiness` is `ready` and inputs are obvious, you can go straight to Run.
- Optional: `platform` (slug/name), `kind` (`model` | `data` | `workflow`),
  `limit` (1-50, default 5), `cursor`, `view` (`compact` default or `full` with
  `input_schema` and `schema_hash`, skipping Inspect), and `group_by: "function"`
  (an explicit `groups` overview).
- Copy a `reference` exactly as returned; never invent one. The reply's `next`
  field is the exact call to make next.
