# Errors and recovery

Keep the original `request_id` in diagnostics. Never include the API key,
webhook signing secret, or private media URL in logs or issue text.

| Condition | Action |
| --- | --- |
| `unauthorized` / HTTP 401 | Stop. Ask the user to run `beatapi auth login` or replace/revoke the key outside chat. |
| `insufficient_credits` / HTTP 402 | Stop. Report available balance and the relevant estimate; do not retry. |
| `bad_request` / HTTP 400 | Correct fields, enums, URLs, or media. Do not resubmit unchanged. |
| `not_found` / HTTP 404 | Verify task, shot, or webhook ID. |
| `user_concurrency_exceeded` | Stop creating tasks. Wait for active processing work to finish or ask the user to choose. |
| `rate_limit_exceeded` | Honor `retry_after_seconds` or `Retry-After`, then retry with a bound. |
| Network failure / HTTP 502, 503, 504 | Retry with bounded exponential backoff and jitter. |
| `processing_failed`, `processing_timeout`, `result_transfer_failed` | Read final task state, error fields, usage settlement/refund, and request ID before recommending a new paid task. |

Do not automatically create a replacement paid task after a failed task. Explain
the final state and ask only when a new charge or changed creative decision is
required.
