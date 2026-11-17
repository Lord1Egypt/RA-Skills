---
name: api-gateway
description: Smart proxy for external API calls with retry, caching, rate limiting, and fallback providers. PERSISTS: API keys (chmod 0600 plaintext in keys.json), request/response cache metadata, and request logs. Network: outbound HTTPS only, with a strict provider-domain allowlist. Caches metadata by default; full response bodies are opt-in per provider.
---

# API Gateway ⚡

> **Read this first.** This skill makes outbound HTTPS calls and writes plaintext API keys to disk. By installing or running it, you accept responsibility for the security of the keys you provide and the endpoints you target.

**Stop duplicating API logic. Start routing through one smart gateway.**

## What This Skill Does

API Gateway is a local Node.js HTTP client wrapper that gives one call:

- **Retry with exponential backoff** (3 attempts, 1s/2s/4s)
- **Response caching** (default 5 min TTL, metadata-only)
- **Rate-limit handling** (parses `x-ratelimit-remaining`, auto-fallback)
- **Circuit breaker** (5-failure open, 30s cooldown, auto-recover)
- **API key management** (masked display, chmod 0600 storage, env-var override)
- **Fallback providers** (configurable per-provider chain)

## ⚠️ Important Warnings

### Outbound HTTPS Requests to Whitelisted Provider Domains
`--call <provider> <endpoint>` sends HTTPS requests and, for configured providers, attaches a `Authorization: Bearer <key>` header. **The provider allowlist is strict: it is a domain-match check, not a `string.includes()` check.** A URL like `https://attacker.com/api?provider=openai` will NOT receive the key because the hostname must match the provider's registered allowlist entry. Review the allowlist in `--keys` output before adding sensitive keys.

### API Keys Stored in Plaintext on Disk
API keys saved via `--keys add` are written to `memory/api-gateway/keys.json` in plaintext, with file permissions set to `0600` (owner read/write only). The key is NEVER echoed back. Anyone with shell access to the workspace as the same user can still read it. For higher assurance, prefer environment variables: `OPENAI_API_KEY=sk-...` — API Gateway auto-detects any `PROVIDER_API_KEY` variable (e.g. `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`) and uses it without disk storage. It does NOT read arbitrary `env:NAME` references — only the `PROVIDER_API_KEY` pattern — so unrelated secrets are never pulled in.

### Persistent Data Files (Disclosed Up Front)
The following files persist in `memory/api-gateway/` after any operation:
- `keys.json` — API key storage, chmod 0600
- `cache.json` — **Metadata-only by default** (status code, timestamp, response headers, response body *length*). The full response **body** is NOT stored unless you explicitly enable it per provider via `--cache-full <provider>`.
- `request-log.json` — Provider name, status class (2xx/4xx/5xx), timestamp. Endpoint URLs, query strings, and request/response **bodies are NOT written here.** (Note: if *you* pass a URL or prompt inside a request body to `--call`, that body travels to the provider but is never persisted to the log or cache by this skill.)
- `rate-limits.json` — Per-provider rate-limit state
- `circuit-state.json` — Per-provider circuit-breaker state
- `fallbacks.json` — Fallback provider mappings

All of these are intended, documented, and necessary for the skill's features. Default retention is unlimited unless cleared with `--cache --clear` and `--log --clear`.

### Zero External Dependencies
This skill uses only Node.js built-ins (`http`, `https`, `fs`, `path`). There is no `package.json` to install, no transitive dependencies, no `npm install` step. The code you read is the code that runs.

## Quick Start

### Make an API call

```bash
node skills/api-gateway/api-gateway.js --call openai https://api.openai.com/v1/chat/completions '{"model":"gpt-4","messages":[{"role":"user","content":"hello"}]}'
```

Retries up to 3 times with exponential backoff. Caches response **metadata** for 5 minutes.

### Dry run (preview without executing)

```bash
node skills/api-gateway/api-gateway.js --call --dry-run openai https://api.openai.com/v1/chat/completions
```

### Manage API keys

```bash
# List configured keys (masked, shows allowlist domains)
node skills/api-gateway/api-gateway.js --keys

# Add a key (with provider allowlist)
node skills/api-gateway/api-gateway.js --keys add openai sk-abc123 --allow-domain api.openai.com

# Remove a key
node skills/api-gateway/api-gateway.js --keys remove openai
```

### Use environment variables instead of stored keys (recommended for CI/ephemeral)

```bash
export OPENAI_API_KEY=sk-abc123
node skills/api-gateway/api-gateway.js --call openai https://api.openai.com/v1/chat/completions '{"model":"gpt-4","messages":[]}'
```

The skill auto-detects `PROVIDER_API_KEY` env vars and uses them without disk storage. Stored keys take precedence if both are configured.

### Cache, log, and rate status

```bash
node skills/api-gateway/api-gateway.js --cache          # Show cache entries (metadata only)
node skills/api-gateway/api-gateway.js --cache --clear  # Clear cache
node skills/api-gateway/api-gateway.js --log            # Show request log (coarse: provider, status class, time)
node skills/api-gateway/api-gateway.js --log --clear    # Clear request log
node skills/api-gateway/api-gateway.js --rate openai    # Rate limit status
```

### Fallback providers and circuit breaker

```bash
node skills/api-gateway/api-gateway.js --fallback openai anthropic
node skills/api-gateway/api-gateway.js --circuit --status
node skills/api-gateway/api-gateway.js --circuit openai --reset
```

### Status overview

```bash
node skills/api-gateway/api-gateway.js --status
```

## Provider Allowlist (Security Boundary)

This is the most important section. The skill uses a **domain allowlist** to decide whether to inject the `Authorization: Bearer` header:

- When you add a key with `--keys add <provider> <key> --allow-domain <domain>`, that domain is stored alongside the key.
- On every call, the request URL's hostname is extracted and compared against the allowlist (exact match or `*.example.com` wildcard).
- If the hostname does NOT match, the bearer token is omitted — the request still goes out, just without the key.
- This means a malicious or mistyped endpoint URL cannot exfiltrate your key.

**Example allowlist configurations:**

```bash
# Strict: only api.openai.com gets the OpenAI key
--keys add openai sk-... --allow-domain api.openai.com

# Wildcard: any *.anthropic.com endpoint
--keys add anthropic sk-ant-... --allow-domain "*.anthropic.com"

# Multi-domain (repeat flag)
--keys add custom TOKEN --allow-domain api.example.com --allow-domain api-staging.example.com
```

If you add a key WITHOUT `--allow-domain`, the key is still saved but the skill will **refuse to attach it to any request** until you add at least one allowlist entry. (You can edit `keys.json` to add `allowDomains: ["api.openai.com"]` directly.)

## Features

### Retry with Exponential Backoff
- 3 retry attempts by default
- Exponential backoff (1s, 2s, 4s)
- All failures logged with attempt count

### Response Caching (Metadata-Only by Default)
- 5-minute TTL
- Cache key = provider + endpoint + body hash
- **Default behavior**: caches `{status, headers (redacted), timestamp, bodyLength}`. Body content is NOT stored.
- **Opt-in full caching**: `--cache-full <provider>` enables full response body caching for that provider.
- Auto-evicts expired entries
- Cache hit detection prevents redundant calls

### Rate Limit Handling
- Tracks remaining requests from `x-ratelimit-remaining` headers
- Auto-fallback when rate limited (if configured)
- Status check via `--rate`

### Key Management
- Masked display (first 4 + last 4 chars)
- Per-provider key storage in `memory/api-gateway/keys.json`
- **chmod 0600** on the file (POSIX only; best-effort on Windows)
- Environment-variable auto-detection (PROVIDER_API_KEY)
- Allowlist attached to each key
- Add/remove keys without exposing full values

### Fallback Providers
- Configurable per-provider fallback chain
- Automatic failover on rate limit or error
- No manual intervention needed

### Circuit Breaker
- Tracks failure rates per provider
- Opens circuit after 5 consecutive failures
- Auto-recovers after 30s cooldown (HALF-OPEN state)
- Prevents cascading failures and saves API costs
- CLI visibility: `--circuit --status` + `--circuit <name> --reset`

## Configuration

Data files stored in: `memory/api-gateway/`

- `keys.json` — API key storage (chmod 0600)
- `fallbacks.json` — Fallback provider mappings
- `cache.json` — Response cache (metadata-only by default)
- `rate-limits.json` — Rate limit tracking
- `request-log.json` — Request history (coarse: provider, status class, timestamp, NOT endpoints)
- `circuit-state.json` — Circuit breaker state per provider

Override data directory:
```bash
--dir /path/to/data
# or env var
API_GATEWAY_DIR=/path/to/data node api-gateway.js --status
```

## Agent Protocol

When making API calls:

1. **Use the gateway** — `--call <provider> <endpoint> [body]` instead of direct fetch
2. **Add keys with allowlist** — `--keys add <provider> <key> --allow-domain <domain>` before first use
- **Prefer env vars in CI** — `PROVIDER_API_KEY` env vars bypass disk storage entirely. API Gateway auto-detects any `PROVIDER_API_KEY` environment variable (e.g. `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`) and uses it without disk storage. It does NOT read arbitrary environment variables — only the documented `PROVIDER_API_KEY` pattern — so unrelated secrets are never exposed to requests or local processing.
4. **Set fallbacks** — `--fallback primary secondary` for critical providers
5. **Check cache/log** — `--cache` / `--log` during heartbeats to monitor usage
6. **Dry run** — `--call --dry-run` before executing important calls

## Security Notes
- Keys stored as plain text in JSON with chmod 0600 (POSIX)
- For higher assurance, use environment variables (`PROVIDER_API_KEY`)
- For production, integrate with a secrets manager
- Masked output prevents accidental exposure in logs
- Request log stores only provider + status class + timestamp (no endpoints)
- Allowlist is a strict domain match, not a string contains
- Code has zero external dependencies (no npm install)
- ⚠️ **DATA LEAVES TO A THIRD PARTY:** every `--call` sends your request (URL, headers, body, prompts) to the provider endpoint YOU specify — a separate external service. Responses come back from that provider and may be retained by them per their own policy. This skill is NOT a transparent pass-through; it centralizes collection, storage, and forwarding of potentially sensitive data. Only call endpoints you trust.
- ⚠️ **SENSITIVE DATA IN LOGS/CACHE:** request bodies, response headers, and endpoints you pass may themselves contain API keys, tokens, or prompts. The request log, `cache.json` (especially with `--cache-full`), and `request-log.json` persist this data to disk. Clear them after sensitive work (`--log --clear`, `--cache --clear`) and never call `--cache-full` for sensitive providers.
- ⚠️ **FULL-BODY CACHING WRITES COMPLETE RESPONSES TO DISK:** `--cache-full <provider>` stores the ENTIRE response body (which may contain secrets, tokens, personal data, or proprietary content) in `cache.json`. This is a local data-exposure risk if the host/workspace is shared or later exfiltrated. Never use `--cache-full` with sensitive providers; prefer the default metadata-only cache.
- ⚠️ **HTTPS ONLY:** API Gateway refuses to send any request over plain HTTP (it would expose bearer credentials on the wire). Set `API_GATEWAY_ALLOW_HTTP=1` only for non-credential plaintext endpoints.

## What This Skill Does NOT Do

- Does NOT install npm packages
- Does NOT auto-update or phone home
- Does NOT read environment variables silently — only the documented `PROVIDER_API_KEY` pattern
- Does NOT send Authorization headers to URLs outside the allowlist
- Does NOT cache full response bodies unless explicitly opted in per provider
- Does NOT log full endpoint URLs or query strings

## Design Principles

1. **Zero setup** — Works immediately, no config needed
2. **No dependencies** — Pure Node.js http/https, no npm packages
3. **Resilient** — Retry, fallback, and rate limit handling built in
4. **Transparent** — Masked keys, cache status, request logging
5. **Composable** — Works with any HTTP API, not just specific providers
6. **Fail-closed on security boundaries** — If the allowlist doesn't match, the key is not sent. If a file permission can't be set, the call still proceeds but a warning is logged.
