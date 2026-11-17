# Production checklist

- Token comes only from `DATAIFY_API_TOKEN` and never appears in output.
- URLs and required business inputs are validated before any paid call.
- Every request has a deadline; safe retries are bounded and jittered.
- Builder submission is separated from status reads and result download.
- Final output is validated for type, record count and required fields.
- Windows/macOS/Linux text output is UTF-8 safe.
- Logs contain request IDs and error categories, not credentials or full sensitive payloads.
- Tests cover missing/invalid credentials, 402, 429, 5xx, timeout, malformed JSON and resume.
