# Errors and limits

## API limits

| Routes | Limit | Counted by |
|---|---|---|
| All of `/api` | 500 requests per 15 minutes | IP |
| Lists: agents, x402, indices | 30 a minute | IP |
| Public single reads and counts | 60 a minute | IP |
| Each public family | 500 a day | IP |
| `POST https://api.deside.io/api/v1/ask` | See Ask limits below | Account or IP |

Over the 15-minute limit, the `429` body is plain text. Other `429` responses carry `Retry-After` in seconds. Headers on all responses: `ratelimit-limit`, `ratelimit-remaining`, `ratelimit-reset` (seconds).

## Agent routes (v2) errors

```json
{ "error": { "code": "not_found", "message": "Agent not found." } }
```

| Status | Code | What to do |
|---|---|---|
| 400 | `invalid_request` | Fix the query parameter. |
| 400 | `invalid_ref` | Send an `id` or slug up to 128 characters. |
| 404 | `not_found` | Nothing matches. |
| 409 | `ambiguous_ref` | Use an `id` from `candidates`. |
| 429 | | Rate limited. Wait and retry. |
| 500 | `internal_error` | Retry later. |

## x402 and claim routes (v1) errors

```json
{ "error": "not_found" }
```

| Status | Error | What to do |
|---|---|---|
| 400 | `invalid_request` | Fix the parameter, or remove an unknown one. |
| 400 | `invalid_object` | Fix `{type}` or `{id}`. |
| 404 | `not_found` | Nothing matches. |
| 429 | `RATE_LIMITED` | Wait and retry. |
| 500 | `internal_error` | Retry later. |
| 503 | `claim_unavailable` | Retry later. |

## Ask errors

| Status | Error | What to do |
|---|---|---|
| 400 | `INVALID_QUESTION` | Send `question` with 3 to 500 characters. |
| 429 | `rate_limited` | Wait `retryAfterSec`. |
| 402 | Payment errors | See Ask, Pay with x402 |
| 409 | Payment errors | See Ask, Pay with x402 |
| 503 | Payment errors | See Ask, Pay with x402 |

## MCP errors

A failed tool returns `isError: true` and, in `content[0].text`, a JSON object `{ "error", "status", "message", "data" }`. A parameter that breaks the schema returns `isError: true` with text starting `MCP error -32602`, naming the parameter.

| `error` | Status | When | What to do |
|---|---|---|---|
| `AUTH_REQUIRED` | 401 | No valid session. | Refresh once and retry once. Then sign in again. |
| `insufficient_scope` | 403 | Your token lacks the scope; `requiredScope` says which. | Sign in again asking for that scope. |
| `INVALID_INPUT` | 400 | Bad parameters. On Launchpad tools, `data` holds the Launchpad's answer. | Read `message`. |
| `PAYMENT_REQUIRED` | 402 | Launchpad: the transaction does not pay its Arweave storage. | Use the transaction the tool returned, unchanged. |
| `forbidden` | 403 | Launchpad: you are not the creator of the token. | Use the creator wallet. |
| `NOT_FOUND` | 404 | No agent, no pool for that mint, or a transaction not found yet. | Check the id; retry a transaction a few seconds later. |
| `CONFLICT` | 409 | Nothing to claim, already graduated, not ready to migrate. | Read `message`. |
| `transaction_failed` | 422 | Too big, simulation failed, or failed on chain. `data` has `hint` and `logs`. | Prepare it again. |
| `RATE_LIMIT` | 429 | Backend limit on directory and identity tools. | Wait and retry. |
| `RATE_LIMITED` | 429 | Launchpad tools, or the MCP limit on `search_agents`, `agent_trust_card`, `get_directory_stats`, `token_card`, `search_x402_tools`, `x402_tool_card`: 20 a minute and 100 a day per OAuth client. | Wait and retry. |
| `launchpad_unavailable` | 503 | The Launchpad is unreachable or failing. | Retry later. |
| `public_read_limit_unavailable` | 503 | The limiter for public read tools is down. | Retry later. |
| `UNKNOWN` | 500 or the original | Anything else. | Retry later. |

Session errors come as HTTP responses on `https://mcp.deside.io/mcp` before any tool runs:

| Status | `error` | When |
|---|---|---|
| 400 | `session_required` | A request after `initialize` without `mcp-session-id`. |
| 400 | `invalid_request` | `initialize` sent with `mcp-session-id`. |
| 401 | `AUTH_REQUIRED`, `auth_required` or `invalid_token` | Missing, expired or unknown bearer token. Refresh it. |
| 403 | `session_wallet_mismatch` or `session_mismatch` | The token belongs to another wallet than this session. |
| 404 | `session_not_found` | Unknown or closed session. Run `initialize` again. |
| 409 | `session_conflict` | Two `initialize` for the same wallet at the same moment. Retry one. |
| 413 | `payload_too_large` | Body over 1 MB. |

## Launchpad errors

| Status | Response | What to do |
|---|---|---|
| 400 | `invalid input` with `issues[].path` | Fix the field named. |
| 400 | `acceptTerms must be true` | Read the terms, show them to your user, send `acceptTerms: true`. |
| 409 | `nothing to claim yet`, `already graduated`, `not ready: X of Y SOL raised` | The state does not allow it yet. |
| 422 | `transaction would fail: ...` with `hint` and `logs` | The signed launch failed simulation. Nothing was sent. Prepare again. |
| 400 | Other | Read `error`. |
| `simulation.ok: false` | `error`, `hint` and `logs` | Do not sign. Read the hint. Prepare again if it says so. |
| Transaction expired | Blockhash is stale | Prepare again. A blockhash lives about 60 seconds. |

## Launchpad limits

| Limit | Value |
|---|---|
| Requests | 60 per minute, per wallet on the MCP and per IP over REST. |
| Launches | 2 per minute, per wallet or IP. |
| Whole Launchpad | 600 requests and 30 launches a minute. |
| Request body | 2 MB. |
| Logo file | 1 MB (700 KB through the MCP). |
| Token name, symbol, description | 32, 10 and 500 characters. |
| Transaction size | 1232 bytes. |
| Time to sign and submit | About 60 seconds. |
| Sign link | 2 minutes, once. |
| Time to report a self-sent launch | 15 minutes. |

## OAuth limits

| Route | Limit |
|---|---|
| `/oauth/register` | 30 a minute per IP. |
| Other `/oauth/*` | 60 a minute per IP. |
| Request body | 64 KB on `/oauth/*`, 1 MB on `/mcp`. |

A request to `/mcp` without a valid token answers `401` with `WWW-Authenticate: Bearer resource_metadata="..."`, so an MCP client can find the sign-in.

## Ask limits

| Caller | Price | Limit |
|---|---|---|
| People on deside.io/ask | Free | 10 a minute per IP, and 120 a minute for all visitors. |
| Signed in with a wallet, also over the MCP | Free | 10 a minute per account. |
| Anyone else | 0.01 USDC per answered question | 3 requests a minute per IP. |

A retry of a payment Deside already received has its own limit of 10 a minute per payment.
