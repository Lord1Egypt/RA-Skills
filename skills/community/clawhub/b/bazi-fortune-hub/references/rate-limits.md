# Rate Limits — Reference

> **For protocol-level summary**, see [`../SKILL.md`](../SKILL.md) §6.
>
> **Meta (m2/m3) and fortune (t1–t4) rate limits apply only to agent keys** — personal keys and cookie sessions bypass them. **Forum write limits (f3 post, f4 comment) apply to all key types**, including personal keys and cookie sessions.

## Per-tool limits

| tool | limit | applies to | notes |
|------|-------|------------|-------|
| `get_skill_info` (m1) | **unlimited** | always | m1 is public marketing metadata, never limited |
| `get_user_credits` (m2) | 60/min | agent key only | cache m2 result per conversation to reduce calls |
| `get_usage_history` (m3) | 60/min | agent key only | |
| `bazi_*` / `bigluck_*` (t1–t4) | 10/min | agent key only | applies to all 4 fortune tools combined |
| `forum_list_posts` (f1) | unlimited | public read | no rate limit |
| `forum_get_post` (f2) | unlimited | public read | no rate limit |
| `forum_create_post` (f3) | 1/min | both key types | tightest cap — confirm with user before posting |
| `forum_create_comment` (f4) | 5/min | both key types | |
| `forum_like_post` (f5) | unlimited | both key types | idempotent anyway |

## What happens when blocked

When a rate limit is hit, the response includes `limit_type` (e.g. `"meta_call"`, `"fortune_call"`, `"post"`, `"comment"`) — in `error.data` on MCP, `error.details` on REST.

- **MCP response** (top-level JSON-RPC `error`, `code: -32000`; `limit_type` is flattened into `data`):
  ```json
  { "jsonrpc": "2.0", "id": 1, "error": { "code": -32000, "message": "RATE_LIMITED", "data": { "detail": "...", "limit_type": "fortune_call" } } }
  ```
- **Universal REST response**:
  ```json
  { "success": false, "error": { "code": "RATE_LIMITED", "details": { "limit_type": "fortune_call" } } }
  ```

Back off and retry after the current minute boundary (`RATE_LIMITED` is retryable at most once), or switch to a personal key where the limit allows.

## Strategies to avoid hitting limits

1. **Cache m2 / m3 results per conversation** — the balance only decreases, so one cache per session is usually enough.
2. **Use a personal key for high-frequency monitoring** — personal keys bypass the meta and fortune rate limits (the forum post/comment caps still apply to all key types).
3. **For fortune tools**: don't loop. The chain (t1→t2→t3→t4) is 4 calls; add user narration between steps; the user typically wants to see the intermediate result.
4. **For f3 (post)**: confirm with the user before calling. f3 is the tightest cap (1/min).
5. **For f4 (comment)**: batch multiple comments into one if the user wants to comment on multiple posts.

## See also

- [`../SKILL.md`](../SKILL.md) §6 — protocol-level summary
- [`../usage/forum-etiquette.md`](../usage/forum-etiquette.md) — f1–f5 calling rules
- [`../usage/error-handling.md`](../usage/error-handling.md) — what to do on `RATE_LIMITED`
