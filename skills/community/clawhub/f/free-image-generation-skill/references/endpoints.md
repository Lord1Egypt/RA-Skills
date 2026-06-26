# Endpoint Notes (Implementation)

This skill uses a 3-step generation pattern:

1. session verification endpoint
2. image generation endpoint
3. temporary image download endpoint

Request behavior:
- random cache-bust params
- request id per generation
- JSON payload with prompt, negative prompt, resolution, guidance

Operational guidance:
- keep request rates moderate
- use retries + backoff for transient errors
- fail clearly with structured error output
