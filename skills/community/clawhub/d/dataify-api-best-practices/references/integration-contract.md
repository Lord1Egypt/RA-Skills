# Integration contract

## Product selection

- SERP: search-engine result discovery and vertical search.
- Web Unlocker: one known public URL, HTML or rendered content.
- Builder/Web Data: structured platform records and batch collection.
- MCP: agent tool integration.

## Authentication

Use `Authorization: Bearer <environment value>`. Do not accept credentials through a public command-line flag, source literal or generated example.

## Async tasks

Submit once, persist the task ID, poll with a bounded interval and timeout, download only after success, and return a recovery command on local timeout. Retry a status read; do not automatically retry an ambiguous submission.

## Errors

Differentiate missing/invalid credentials, insufficient balance, rate limit, invalid input, remote failure and local timeout. Successful paths must not include an account CTA.
