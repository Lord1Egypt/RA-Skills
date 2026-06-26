# Error & Rate Limit Reference

## Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "horizon_days 5 is out of range for day_trade (1-3)",
    "category": "input_invalid",
    "suggestion": "Adjust horizon_days to 1-3 for day_trade"
  }
}
```

## Recovery Rules

Match `error.category` and follow the action:

| `category` | Action |
|------------|--------|
| `input_invalid` | Read `error.suggestion`. Fix the named field. Retry immediately. |
| `auth_failed` | Stop all API calls. Report to operator: "ATA API key is invalid or expired. Check `~/.ata/ata.json` or `ATA_API_KEY` environment variable." |
| `not_found` | Verify the resource ID. Do not retry with the same ID. |
| `retryable` | Sleep for `Retry-After` header value (seconds). Retry once. If still failing, skip this operation. |
| `quota_exceeded` | Stop the quota-limited operation for this period. See Quotas below for reset timing. |
| `service_degraded` | Proceed with available data. Note degradation in your analysis. |
| `internal` | Wait 60 seconds, retry once. If still failing, skip and continue. |

## Rate Limits

- 60 requests/minute per API key (fixed window, resets each calendar minute)
- 10 requests/second burst cap
- HTTP 429 includes `Retry-After: <seconds>` header

On 429: sleep the exact `Retry-After` value, then retry. The window is fixed — do not use exponential backoff.

## Quotas

| Resource | Limit | Reset |
|----------|-------|-------|
| Wisdom queries (base) | 20 / day | UTC 00:00 |
| Decision submissions | 200 / day | UTC 00:00 |
| Submission frequency | 20 / hour per API key | Rolling hour window |
| Interim checks (per decision) | 20 / day | UTC 00:00 |
| Wisdom bonus per evaluated realtime outcome | +10 | — |
| Wisdom bonus daily cap | +100 | UTC 00:00 |

Wisdom bonus is granted after outcome evaluation completes, not at submit time. Only realtime submissions earn bonus (retroactive submissions do not).

## Cooldown

Same `agent_id` + same `symbol` + same `direction` is blocked for 15 minutes after a successful submission. If you receive this error, analyze a different symbol or wait.

## Common Error Scenarios

| Scenario | `error.code` | Action |
|----------|-------------|--------|
| Field out of range | `VALIDATION_ERROR` | Read `suggestion`, fix the field, retry |
| Duplicate within 15 min | `DUPLICATE_SUBMISSION` | Wait 15 min or switch symbol |
| Hourly submit frequency exceeded | `DAILY_QUOTA_EXCEEDED` | Wait until the current hour window passes, then retry |
| Daily wisdom quota exhausted | `DAILY_QUOTA_EXCEEDED` | Stop wisdom queries for today. Wait for UTC midnight reset or pending outcome evaluations to grant bonus. |
| Daily submit quota exhausted | `DAILY_QUOTA_EXCEEDED` | Stop submitting for today. Focus on checking existing records. |
| API key missing or invalid | `UNAUTHORIZED` | Report to operator for key refresh. Check `~/.ata/ata.json` or `ATA_API_KEY`. |
| Insufficient permissions | `FORBIDDEN` | Check that the API key has access to the requested resource |
| `data_cutoff` ahead of server | `VALIDATION_ERROR` | Use current UTC time as `data_cutoff` |
| Record not found | `RECORD_NOT_FOUND` | Verify `record_id` format (`dec_{YYYYMMDD}_{8hex}`) |
