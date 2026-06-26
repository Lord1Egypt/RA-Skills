# Deep Validator

Email and URL deep validation micro-service — A2A-compatible, x402 payment protocol.

**Hosted endpoint:** `https://deep-validator-production.up.railway.app`
**Operator:** novlease.contact@gmail.com
**License:** MIT-0

---

## What it does

Performs real network checks that a language model cannot do natively:

- **Email:** RFC 5322 syntax → DNS MX (parking detection) → DNSBL reputation → disposable domain → WHOIS age
- **URL:** DNS resolution + SSRF protection → HTTP reachability → redirect chain (up to 5 hops) → heuristic risk scoring
- **Domain:** MX + SSL certificate → WHOIS age → registrar → disposable/parked detection
- **Batch classify:** free heuristic pre-filter (no auth, no credits, up to 10 000 items)

Every response includes `recommended_action` — agents use this field directly without re-interpreting raw checks.

---

## Endpoints

| Method | Path | Description | Credits |
|--------|------|-------------|---------|
| POST | `/validate/email` | Single email, full checks | 1 |
| POST | `/validate/emails/bulk` | Up to 500 emails | 1 each |
| POST | `/validate/emails/file` | CSV/XLSX/TSV/TXT, up to 1 000 000 rows | 1 each |
| POST | `/validate/url` | Single URL, full checks | 1 |
| POST | `/validate/urls/bulk` | Up to 500 URLs | 1 each |
| POST | `/validate/urls/file` | CSV/XLSX/TSV/TXT, up to 1 000 000 rows | 1 each |
| POST | `/validate/domain` | Domain enrichment (MX, SSL, WHOIS) | 1 |
| POST | `/batch/classify/emails` | Free heuristic pre-filter | Free |
| POST | `/batch/classify/urls` | Free heuristic pre-filter | Free |
| GET | `/jobs/{job_id}` | Poll async job status | Free |
| GET | `/jobs/{job_id}/result` | Download async job result | Free |
| GET | `/health` | Health check | Free |
| GET | `/.well-known/agent.json` | Nevermined Agent Card | Free |
| GET | `/.well-known/ai-plugin.json` | OpenAI plugin manifest | Free |

---

## Authentication

**For agents calling the hosted endpoint:** no configuration needed. The service uses the **x402 Nevermined payment protocol** — the agent pays automatically from its wallet.

**Payment flow:**
1. Call any `/validate/*` endpoint with `confirmed=true`
2. Server returns `HTTP 402` with payment requirements
3. Agent pays from its Nevermined wallet and retries with `Authorization: Bearer <token>`
4. Validation runs

**Consent gate:** Call with `confirmed=false` (default) to get a free cost quote first. The server charges nothing until `confirmed=true` is sent.

1 credit = 1 validation = **$0.0001**. Free trial: 10 credits per plan.

---

## Email validation checks

| Check | Library | Fallback |
|-------|---------|---------|
| RFC 5322 syntax | `email-validator` | Blocking — returns `is_valid: false` |
| DNS MX (parking detection) | `dnspython` | Returns `is_valid: false` |
| DNSBL reputation (Spamhaus ZEN) | `dnspython` | Skipped gracefully, score not penalised |
| Disposable domain detection | Static list | Always applied |
| WHOIS domain age | `python-whois` | Skipped if unavailable |

---

## URL validation checks

| Check | Fallback |
|-------|---------|
| RFC 3986 format | Blocking |
| DNS resolution + SSRF protection (private IP block) | Returns `is_alive: false` |
| HTTP HEAD reachability | Returns `is_alive: false` + error |
| Redirect chain tracking (max 5 hops) | Truncated with warning |
| Heuristic risk scoring | Always applied, no extra I/O |

---

## Self-hosting

### Environment variables

Credentials are loaded in `app/dependencies.py`, not `app/config.py`. `app/config.py` contains only operational settings (timeouts, limits, base URL).

| Variable | Required | Description |
|----------|----------|-------------|
| `NVM_API_KEY` | Yes | Nevermined API key — verifies and settles x402 payments server-side. |
| `NVM_PLAN_ID_EMAIL` | Yes | Nevermined plan ID for email/domain validation. |
| `NVM_PLAN_ID_URL` | Yes | Nevermined plan ID for URL validation. |
| `NVM_ENVIRONMENT` | No | `live` (default) or `testing`. |
| `DEEP_VALIDATOR_API_KEY` | No | Optional admin bypass key. If set, the operator can call the API directly without x402. Leave empty to enforce the Nevermined flow for all requests. |

```bash
cp .env.example .env
# Set all four variables above in .env

pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Rate limiting

The built-in rate limiter (`slowapi`) is **single-instance and in-memory**. Deploy with exactly **1 replica**. For horizontal scaling, replace with a Redis-backed limiter.

### Docker

```bash
docker compose up
```

### Tests

```bash
pytest tests/ -v
```

### Nevermined registration

```bash
NVM_API_KEY=your_key SERVICE_URL=https://your-url.com python scripts/register_on_nevermined.py
```

---

## Agent integration

See `SKILL.md` for full agent instructions, curl examples, response schemas, and usage rules.
