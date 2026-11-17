# Custom & Self-Hosted Provider Telemetry Integration Guide

This guide details how to integrate quota, credit, and usage telemetry from custom and self-hosted AI gateways into your unified dashboard using official APIs and standard user tokens.

---

## 1. Supported Provider Architectures

1. **Official Developer APIs (Recommended):**
   - **OpenRouter:** `GET https://openrouter.ai/api/v1/credits` or `/auth/key` using `Authorization: Bearer <key>`. Returns `total_credits`, `total_usage`, `limit_remaining`.
   - **ElevenLabs:** `GET https://api.elevenlabs.io/v1/user/subscription` using `xi-api-key: <key>`. Returns `character_count`, `character_limit`, `next_character_count_reset_unix`.
   - **OpenAI / Anthropic:** Usage and balance endpoints queried with developer API keys.

2. **Self-Hosted AI Gateways & Local Servers:**
   - **Ollama / vLLM / LiteLLM:** Query local status endpoints (e.g., `http://127.0.0.1:11434/api/tags` or `http://127.0.0.1:8000/v1/models`).
   - Use dedicated read-only service tokens configured in your gateway dashboard.

---

## 2. When Endpoints Lack Explicit Limit Numbers (Telemetry Strategies)

Not all platforms provide a dedicated countdown counter. The collector handles these scenarios gracefully:

### Strategy 1: Unit Economics / Reverse Balance Calculation
When an API returns only balance in USD (e.g., Pay-as-you-go search or model APIs):
- Query account balance (e.g., `$9.34`).
- Divide by fixed cost per unit (e.g., `$0.005` per request).
- Estimated capacity: `remaining_requests = int(balance_usd / unit_price)`.
- Renders a clean progress bar calibrated against the balance tier.

### Strategy 2: Rolling Window & Fixed Quota Timers
When an account operates on fixed time-bound windows (e.g., 50 requests per 3 hours):
- The collector tracks the start of the current cycle locally.
- Computes and renders a live countdown timer until the window resets.

### Strategy 3: Local Runtime Usage Telemetry
When self-hosting open-weight models where no billing API exists:
- Query local runtime token usage statistics.
- Display cumulative tokens generated and requests served today.

### Strategy 4: Session Validity Heartbeat
For unlimited or flat-rate subscriptions:
- Execute a lightweight status check (e.g., `GET /v1/models`).
- Verify HTTP 200 OK.
- Display a live green pulse badge (`Status: Active`).

---

## 3. Telemetry Normalization Schema

All provider telemetry is mapped into the standard dashboard schema:

```json
{
  "provider": "Provider Name",
  "account": "user@example.com",
  "category": "api_credits | tiered_quota | self_hosted",
  "used": 15000,
  "limit": 100000,
  "unit": "characters | tokens | requests | usd",
  "percent_used": 15.0,
  "resets_at": "2026-10-03T00:00:00Z",
  "status": "healthy | warning | exhausted | active",
  "updated_at": "2026-10-02T12:00:00Z"
}
```
