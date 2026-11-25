# Error Codes

## Error Code Table

| Code | HTTP | Description | Action |
|------|------|-------------|--------|
| 40001 | 400 | Invalid parameters | Check JSON format, field names, value ranges |
| 40101 | 401 | Invalid API Key | Verify `CV_API_KEY` environment variable |
| 40102 | 401 | API Key expired | Contact admin to renew or regenerate |
| 40103 | 401 | API Key revoked | Contact admin |
| 40104 | 401 | Missing X-User-Identity | Verify `CV_USER_IDENTITY` environment variable |
| 40201 | 402 | Insufficient credits | Top up or upgrade plan |
| 40301 | 403 | No permission for endpoint | Check API Key scopes |
| 42901 | 429 | Rate limit exceeded | Script auto-retries; wait for Retry-After header |
| 42902 | 402 | Daily quota exhausted | Wait until UTC 00:00 reset or upgrade plan |
| 50001 | 500 | Server error | Record request_id, contact support |

## Video Script Audit Errors

The same code carries different meanings per endpoint — always resolve it against the endpoint you called.

| code | Endpoint | HTTP | Description | Action |
|------|----------|------|-------------|--------|
| 40004 | `/tasks/submit` | 400 | Video URL not in the platform whitelist (TikTok / YouTube Shorts / Instagram Reels only) | Do not retry. Report the reason plus the accepted formats to the user and ask for a new link. No credits are charged |
| 40001 | `/tasks/submit` | 400 | Invalid request parameters (e.g. `video_url` / `oss_url` not mutually exclusive) | Caller-side parameter bug; fix the payload and retry |
| 40001 | `/tasks/status`, `/tasks/result` | 200 | Audit task not found (invalid `task_id`) | Verify the task UUID; ensure it was submitted by the same tenant |
| 40002 | `/tasks/result` | 200 | Audit task not completed yet (`status ≠ completed`) | Continue polling via `/tasks/status`; do not retry `result` immediately |
| 40003 | `/tasks/result` | 200 | A completed task has no stored result | Report the missing result and keep the task ID for support |

### Task-Level Failures (no error code)

When `/tasks/status` returns `success: true` with `data.status = "failed"`, the failure happened inside the
worker and is reported only through `data.error_message`. There is no error code for these.

| `error_message` keyword | Meaning | Action |
|------------------------|---------|--------|
| 不支持的视频 URL | URL outside the whitelist | Ask for a whitelisted link |
| 视频时长 … 超过限制 | The processing service rejected this video's duration | Ask for a shorter video |
| 视频文件大小 … 超过限制 | The processing service rejected this file size | Use a smaller asset, or upload a compressed video of up to 500 MB |
| 下载失败 / not_found / invalid | Video deleted, private, or download service error | Confirm the link is still publicly reachable; retry later |

> `data.error_message` MUST be surfaced verbatim to the user. `success: true` only means the status query
> itself succeeded — it says nothing about whether the audit task succeeded.

## Media Upload Errors

| code | HTTP | Description | Action |
|------|------|-------------|--------|
| 40001 | 200 | Unsupported file format or file too large | Check extension (mp4/mov/avi/mkv/webm) and size (≤ 500MB) |

> 40002 is a business state, not a hard failure. Treat it as "keep polling" rather than triggering retry/backoff.
> Submit-time `40201` (insufficient credits) follows the global rule — only this code confirms a credits shortage.

## Troubleshooting

### Environment variables not set

```
Error: CV_API_KEY environment variable is not set
```

**Fix**: Set environment variables and restart terminal/IDE.

### API Key format

Valid format: `cv_live_` prefix + random string, e.g., `cv_live_Y8nil_BsKAbITdqj...`

### Rate limiting

- Default limit: 60 requests/minute (per tenant)
- Script auto-retries up to 3 times on 429
- `Retry-After` response header indicates wait time in seconds

### Daily quota

- Resets at UTC 00:00 daily
- `meta.quota_remaining` shows remaining daily API request count, not credits
- `-1` means unlimited
- Do not display a credits warning based on `quota_remaining`

### Insufficient credits

- Only error code `40201` confirms insufficient credits
- `meta.credits_remaining` is the actual OpenAPI credits balance when present
- A successful response must never be converted into an insufficient-credits warning

### Permission denied

API Key scopes control endpoint access. For example, structured TikTok search uses
`creator:tiktok:search`, natural-language creator search uses `creator:nl_search`, and video search uses `video:search`.
