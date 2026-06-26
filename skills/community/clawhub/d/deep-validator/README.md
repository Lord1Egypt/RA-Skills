# Deep Validator

[![smithery badge](https://smithery.ai/badge/Vannelier/deep-validator)](https://smithery.ai/servers/Vannelier/deep-validator)

Validates email addresses and URLs in real time using actual DNS, HTTP, and
DNSBL checks — something a native LLM cannot do. Returns a clear recommendation
(safe / review / block), a confidence score, and per-check details. Free tier:
10 validations/day and 1 000 classify items/day per IP. Beyond quota:
$0.0005/item (validate) or $0.00005/item (classify). Two payment rails: x402
(USDC on Base) or MPP (Tempo stablecoin). Free cost quote before any charge.

**Hosted endpoint:** `https://deep-validator-production.up.railway.app`
**Operator:** novlease.contact@gmail.com
**License:** MIT-0

---

## What it does

- **Email:** RFC 5322 syntax → DNS MX (parking detection) → DNSBL reputation → disposable domain → WHOIS age
- **URL:** DNS + SSRF protection → HTTP reachability → redirect chain (≤ 5 hops) → heuristic risk scoring
- **Domain:** MX + SSL certificate → WHOIS age → registrar → disposable/parked detection
- **Batch classify:** free heuristic pre-filter (no auth, no credits, up to 10 000 items)

Every response includes `recommended_action` — agents use that field directly.

---

## Endpoints

| Method | Path | Description | Price |
|--------|------|-------------|-------|
| POST | `/validate/email` | Single email, full checks | $0.0005 |
| POST | `/validate/emails/bulk` | Up to 500 emails | $0.0005/item |
| POST | `/validate/emails/file` | CSV/XLSX/TSV/TXT, ≤ 1 000 000 rows | $0.0005/item |
| POST | `/validate/url` | Single URL, full checks | $0.0005 |
| POST | `/validate/urls/bulk` | Up to 500 URLs | $0.0005/item |
| POST | `/validate/urls/file` | CSV/XLSX/TSV/TXT, ≤ 1 000 000 rows | $0.0005/item |
| POST | `/validate/domain` | Domain enrichment (MX, SSL, WHOIS) | $0.0005 |
| POST | `/validate/mixed/bulk` | Mixed email + URL list (type auto-detected) | $0.0005/item |
| POST | `/batch/classify/emails` | Heuristic pre-filter (local, no network) | $0.00005/item |
| POST | `/batch/classify/urls` | Heuristic pre-filter (local, no network) | $0.00005/item |
| GET  | `/jobs/{id}` / `/jobs/{id}/result` | Async job polling | Free |
| GET  | `/health` | Health check | Free |
| GET  | `/mcp` | MCP (Model Context Protocol) streamable HTTP endpoint | Free |
| GET  | `/.well-known/agent.json` | Agent Card (x402 + MPP extensions) | Free |
| GET  | `/.well-known/ai-plugin.json` | OpenAI plugin manifest | Free |
| GET  | `/llms.txt` | Machine-readable summary for LLM agents | Free |

---

## Free tier + paid access

**Free, no auth, per-IP daily quotas:**

- **10 full validations/day** (any `/validate/*` endpoint).
- **1 000 classify items/day** (across both `/batch/classify/*` endpoints).

Once the daily quota is exhausted, requests return **HTTP 402** with the
standard dual-rail challenge. Counters reset at UTC midnight. Quotas are
tunable via `FREE_VALIDATE_DAILY_QUOTA` and `FREE_CLASSIFY_DAILY_QUOTA`.

The service accepts two payment protocols at **every paid request**: an agent
calls, receives **HTTP 402** listing both rails, picks one, and retries.

### Rail 1 — x402 (USDC on Base)

```
POST /validate/email
  → 402 { payment_methods: { x402: { network, token: "USDC", amount, recipient, nonce } } }

Pay on Base (send USDC to `recipient`, amount ≥ quoted), then:

POST /validate/email
Headers:
  X-Payment-Proof: {"tx_hash": "0x…", "nonce": "<nonce-from-challenge>", "payer": "0x…"}
  → 200 <result>
```

Server verifies the tx on-chain via RPC (`eth_getTransactionByHash`, 3 s timeout).

### Rail 2 — MPP (Tempo stablecoin, pympp SDK)

```
POST /validate/email
  → 402 { payment_methods: { mpp: { www_authenticate, amount, currency: "USD", recipient } } }

Client pays via Tempo → receives a credential, then:

POST /validate/email
Headers:
  Authorization: Payment <credential>
  → 200 <result>
```

### Admin bypass (operator only)

If the server is configured with `DEEP_VALIDATOR_API_KEY`, the operator can call
with `X-API-Key: <key>` or `Authorization: Bearer <key>` to skip payment entirely.
This key **must not** be shared with end users — it bypasses billing.

### Consent gate

All paid endpoints accept `confirmed: false` (default) which returns a **free cost
quote** without touching the payment flow. Production validation requires
`confirmed: true`.

```bash
# Free quote (no auth, no charge)
curl -X POST https://.../validate/email \
  -H "Content-Type: application/json" \
  -d '{"email": "test@gmail.com", "confirmed": false}'
# → 200 { item_count: 1, total_cost: 0.0005, ... }
```

---

## MCP (Smithery / Claude Desktop / Copilot)

The service exposes a Model Context Protocol streamable-HTTP endpoint at
`/mcp`. It surfaces seven tools: `validate_email`, `validate_emails_bulk`,
`validate_url`, `validate_urls_bulk`, `validate_domain`, `classify_emails`,
`classify_urls`.

### Use it from Smithery
```yaml
# Already published at: https://smithery.ai/server/deep-validator
# Or point a custom client at:
url: https://deep-validator-production.up.railway.app/mcp
```

### Use it locally over stdio
```bash
pip install "mcp[cli]" httpx
DEEP_VALIDATOR_API_KEY=... python mcp_server.py
```

The MCP server accepts an optional `api_key` setting (Smithery config or
`DEEP_VALIDATOR_API_KEY` env var). If provided it's forwarded as `X-API-Key`
for admin-bypass billing. Without it, the underlying REST endpoints return
HTTP 402 and the MCP tool returns the payment challenge to the calling agent.

---

## Self-hosting

### Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `X402_WALLET_ADDRESS` | ✅ | EOA or smart-wallet that receives USDC on Base. |
| `X402_NETWORK` | ✅ | `base-mainnet` (default) or `base-sepolia`. |
| `BASE_RPC_URL` | ✅ | Alchemy / Infura / public Base RPC used to verify tx hashes. |
| `MPP_TEMPO_RECIPIENT` | ⚠️ | Tempo recipient address. Omit to disable the MPP rail. |
| `MPP_SECRET_KEY` | ⚠️ | pympp server secret key. Omit to disable the MPP rail. |
| `DEEP_VALIDATOR_API_KEY` | ❌ | Optional operator admin bypass (`openssl rand -hex 32`). |
| `FREE_TIER_ENABLED` | ❌ | Set to `true` to bypass payment globally — every `/validate/*` call succeeds without 402. Unset or `false` = dual-rail billing active. |
| `FREE_VALIDATE_DAILY_QUOTA` | ❌ | Per-IP free daily quota for `/validate/*` (default `10`). Set to `0` to disable the free tier for validation. |
| `FREE_CLASSIFY_DAILY_QUOTA` | ❌ | Per-IP free daily quota for `/batch/classify/*` items (default `1000`). Set to `0` to disable. |
| `DEEP_VALIDATOR_BASE_URL` | ❌ | Public URL of this deployment. |
| `WEBHOOK_SECRET` | ❌ | If set, webhook POSTs are HMAC-SHA256 signed in `X-Signature`. |

All operator secrets are loaded via `os.environ` directly in `app/dependencies.py`
and `app/payment/*` — **not** declared in `app/config.py`. Static analysis of
`app/config.py` reports zero agent-side env vars by design.

### Run

```bash
cp .env.example .env
# Fill X402_WALLET_ADDRESS, BASE_RPC_URL, MPP_TEMPO_RECIPIENT, MPP_SECRET_KEY

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Or with Docker:

```bash
docker compose up --build
```

### Rate limiting

`slowapi` is **single-instance in-memory**. Deploy with **1 replica only**.
For horizontal scaling, migrate to Redis-backed `fastapi-limiter`.
`Dockerfile` and `docker-compose.yml` enforce `--workers 1` / `replicas: 1`.

### Tests

```bash
pytest
```

All tests mock the network (respx + pytest-mock). Zero live DNS/HTTP/SMTP calls.

---

## Agent integration

See `SKILL.md` for the full OpenClaw skill definition — curl examples, response
schemas, and usage rules for AI agents.

See `llms.txt` for a machine-readable one-page summary.
