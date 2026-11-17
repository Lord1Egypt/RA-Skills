---
name: dach-x402-compliance
version: 1.0.0
description: "DACH compliance layer for x402 agents — Impressum, DSGVO, BFSG, cookie banner, Preisangaben checks via x402 on Base USDC. Deterministic single-response compliance signals for German/Austrian/Swiss URLs."
metadata:
  openclaw:
    emoji: "🦞"
    requires:
      bins: ["curl"]
    homepage: "https://agent.kihustle.tech"
---

# DACH x402 Compliance

Deterministic DACH compliance signals for agents, paid via x402 on Base USDC.

## Base URL

`https://agent.kihustle.tech`

## Network

- **Chain:** `eip155:8453` (Base mainnet)
- **Asset:** USDC
- **Pay-to:** `0x1c8b3C34Dca2Ba2A71598f1F9E0BC2a04A0Bea36`

## Available Services

| Service | Price | Description |
|---------|-------|-------------|
| **impressum-check** | $0.05 | Impressum/imprint signals for DE/AT/CH (DDG/ECG/OR groups) |
| **dsgvo-site-signals** | $0.08 | DSGVO/Datenschutz privacy page and tracker heuristics |
| **bfsg-signals** | $0.08 | BFSG/accessibility signals (lang, title, alt, landmarks) |
| **cookie-banner-signals** | $0.05 | Cookie banner / CMP detection |
| **preisangaben-signals** | $0.05 | Preisangaben / pricing display signals (MwSt, Versand) |
| **widerruf-signals** | $0.05 | Widerruf / cancellation policy signals |
| **dach-site-pack** | $0.15 | Bundle: URL preflight + Impressum + DSGVO + next_jobs |
| **url-preflight** | $0.01 | Fast check: is the URL alive? Status, redirects, title |
| **url-preflight-batch** | $0.10 | Preflight 2-20 URLs in one payment |
| **aeo-dach** | $0.50 | DACH AEO/agent-readiness: llms.txt, agent.json, x402 surfaces |
| **site-watch** | $0.08 | Compare 1-10 URLs against last snapshot (change detection) |
| **json-schema-repair** | $0.01 | Deterministic JSON repair with optional schema validation (demo tier) |

## How to Pay (x402 Flow)

Every paid endpoint follows the same flow:

### Step 1: POST without payment → HTTP 402

```bash
curl -s -X POST https://agent.kihustle.tech/services/impressum-check/jobs \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.de", "country": "DE"}'
```

Response: `HTTP 402 PAYMENT-REQUIRED`

```json
{
  "statusCode": 402,
  "payment": {
    "network": "eip155:8453",
    "asset": "USDC",
    "amount": "0.05",
    "payTo": "0x1c8b3C34Dca2Ba2A71598f1F9E0BC2a04A0Bea36",
    "quoteId": "qt_abc123",
    "expiresAt": "2026-01-01T00:05:00.000Z"
  }
}
```

### Step 2: Pay the exact amount to `payTo` on Base USDC

Use your agent wallet (CDP, Permit2, or any x402-capable wallet). Save the transaction hash.

### Step 3: Retry with PAYMENT-SIGNATURE

```bash
curl -s -X POST https://agent.kihustle.tech/services/impressum-check/jobs \
  -H "Content-Type: application/json" \
  -H "PAYMENT-SIGNATURE: 0x<tx_hash>" \
  -d '{"url": "https://example.de", "country": "DE"}'
```

### Step 4: GET the result

```bash
curl -s https://agent.kihustle.tech/services/impressum-check/jobs/<job_id>/result
```

## Example Response (impressum-check)

```json
{
  "job_id": "job_uuid",
  "service": "impressum-check",
  "status": "completed",
  "country": "DE",
  "present": true,
  "impressum_url": "https://example.de/impressum/",
  "score": 86,
  "issue_codes": [],
  "limitations": ["Heuristic only — not legal advice."]
}
```

## Free Discovery Surfaces

| URL | Content |
|-----|---------|
| `https://agent.kihustle.tech/promo/catalog.json` | Full service catalog with prices and schemas |
| `https://agent.kihustle.tech/promo/demo.json` | Step-by-step settle demo (~60 seconds) |
| `https://agent.kihustle.tech/promo/share.json` | Share/promo text |
| `https://agent.kihustle.tech/docs/how-to-pay` | Payment documentation |
| `https://agent.kihustle.tech/llms.txt` | Agent discovery index |
| `https://agent.kihustle.tech/llms.de.txt` | German llms.txt |
| `https://agent.kihustle.tech/promo/paste-kit.json` | Paste kit for catalogs/discovery |

## Disclaimer

Machine heuristics only — not legal advice. Not a substitute for qualified legal counsel.