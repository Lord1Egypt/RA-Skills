# When something fails

Read this on any error, a 429 or a timeout, from Search, Inspect or Run. The
main Skill is <https://beatapi.io/skill.md>.

Every error is `{"error":{"code","message","retryable","request_id"}}`. Branch on
`error.retryable`: when it is `false`, do not retry — fix the request or tell the
user; when `true`, the same call may succeed later. A failed task carries the same
`retryable`. Never loop a call whose `retryable` is `false`.

| Status / code | Do this |
| --- | --- |
| 401 `missing_api_key` | The request had no key: add the `Authorization` header. |
| 401 `invalid_api_key` | The key was rejected: ask the user to check it in their secure settings. Do not retry. |
| 402 / `insufficient_credits` | Balance too low: send the user to <https://beatapi.io/dashboard/billing>. |
| 400 `bad_request` | Inspect again and fix the named field. Not retryable. |
| 404 `not_found` | Use `suggestions`, or `GET /v1/models` for text models. Not retryable; do not loop. |
| 429 | Wait `error.retry_after_seconds` (or `Retry-After`; MCP sees only the body). Free keys are rate limited before first top-up; batch calls. |
| 5xx on a sync call (`retryable:true`) | It failed and was not charged. Retry once, then tell the user or try another capability. |
| 5xx / timeout on an async start | Retry with the same `idempotency_key`; if you have a task id, poll its status instead. |
| 403 `error code: 1010` | The edge refused Python's default User-Agent: send an explicit one. |

A 429 on a free model: <https://beatapi.io/skill-refs/free-models.md>.
