# Safety Policy

## Principle

**Fail closed.** Free/API-key reads are fine. Paid reads, writes, and live sends need clear intent.

## Action Classification

### No confirmation needed

- `GET /health`
- `GET /stats`, `GET /stats/public`
- `GET /agents/top`
- `GET /agents/search`
- `GET /agents/{id}/card`
- `GET /agents/{id}/score`
- `GET /agents/{id}/score/explain`
- `GET /agents/{id}/metadata.json`
- `GET /metadata/{chain}/{agent_id}.json`
- `GET /keys/info`

### Confirmation required before paid reads

These may trigger x402 payment:

- `GET /agents/{id}/validations`
- `GET /wallet/{wallet}/agents`
- `GET /wallet/{wallet}/score`
- `GET /identity/{global_id}`

Do not auto-pay without the user clearly wanting the paid read.

### Live by default

- `POST /agents/{id}/contact` — sends live by default
- `POST /agents/dispatch` — sends live by default

Use `dry_run=true` only if the user explicitly asks to preview first.

### Explicit approval required

- `POST /metadata/nonce` — only when the user is actively registering metadata
- `POST /agents/{id}/metadata` — requires user confirmation of the payload before submission
- `POST /keys/generate` — only on explicit user request

## Cost Awareness

When an endpoint returns `402 Payment Required`:
1. Inform the user that this is a paid request
2. Explain the x402 flow if they want to proceed
3. Do not auto-pay without confirmation

## API Key Handling

- Never print or log the API key value
- Use `$EIGHTK4_API_KEY` env var in curl commands
- If no key is set, inform the user and offer to generate one with confirmation

## Rate Limits

- Free IP tier: 100 req/day for search + card
- API key tier: 1,000 req/day for key-backed reads
- x402: pay per request

If rate-limited, inform the user and suggest the next appropriate auth tier.
