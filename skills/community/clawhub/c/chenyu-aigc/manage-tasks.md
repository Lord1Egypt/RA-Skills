# Manage Tasks

## Poll Task Status

```bash
curl -s "$CHENYU_BASE_URL/api/v1/aigc/executions/{task_id}" \
  -H "Authorization: Bearer $CHENYU_API_KEY" | jq '.data | {status, progress, progress_message, outputs, error}'
```

**Task statuses:** `queued` → `running` → `succeeded` / `failed` / `canceled` / `expired`

- `succeeded` — check `outputs` for result (`video_url`, `image_url`, etc.)
- `failed` — check `error.code` and `error.message`

**Polling strategy:** wait 3-5 seconds between polls. Most video tasks complete in 30-120 seconds.

## Cancel a Task

```bash
curl -s -X POST "$CHENYU_BASE_URL/api/v1/aigc/executions/{task_id}/cancel" \
  -H "Authorization: Bearer $CHENYU_API_KEY"
```

Only `queued` or `running` tasks can be canceled.

## List Tasks

```bash
curl -s "$CHENYU_BASE_URL/api/v1/aigc/executions?status=running&page=1&page_size=10" \
  -H "Authorization: Bearer $CHENYU_API_KEY"
```

Query parameters: `status`, `recipe_slug`, `page`, `page_size` (max 100).

## Delete a Completed Task

```bash
curl -s -X DELETE "$CHENYU_BASE_URL/api/v1/aigc/executions/{task_id}" \
  -H "Authorization: Bearer $CHENYU_API_KEY"
```

Only terminal-state tasks (`succeeded`, `failed`, `canceled`, `expired`) can be deleted.

## Error Reference

| HTTP Status | Meaning | Action |
|-------------|---------|--------|
| 400 | Invalid inputs or parameters | Check request body against recipe schema |
| 402 | Insufficient credits | Top up account balance |
| 404 | Recipe or task not found | Verify the ID |
| 409 | Idempotency conflict | Use a different Idempotency-Key |

Task-level error codes (in `error.code` field):
- `MODEL_ERROR` — AI model failed, retry with different inputs
- `TASK_TIMEOUT` — task exceeded timeout, retry
- `QUEUE_EXPIRED` — task expired in queue before processing
