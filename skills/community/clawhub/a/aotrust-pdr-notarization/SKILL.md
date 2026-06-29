> ⚠️ Canonical version: https://github.com/GitSerge-crypto/aotrust-skills/blob/main/aotrust-notarize/SKILL.md

---
name: aotrust-notarize
description: >
  Issue a cryptographic proof (PDR) that a digital artifact existed at a specific time.
  Pay $0.01 USDC on Base via x402. Anchored daily to NEAR blockchain. Publicly verifiable.
license: MIT
metadata:
  author: aotrust
  version: "3.6.1"
  mcp-endpoint: https://api.aotrust.link/mcp
  http-endpoint: https://api.aotrust.link/notarize
  verification-endpoint: https://api.aotrust.link/v1/pdr/verify
  near-handle: aotrust
---

# AOTrust — Cryptographic Proof of Existence

A PDR (Provenance Data Record) is a 239-byte cryptographic receipt proving
that a digital artifact existed at a specific point in time.

Works with any digital artifact:
emails, documents, contracts, source code, AI outputs,
research notes, datasets, photos, logs, sensor readings.

The artifact itself is never uploaded — only its SHA-256 hash.

Anchored daily to NEAR blockchain. $0.01 per proof. No account needed.

## Two Ways to Connect

| Interface | Best for | How |
|-----------|----------|-----|
| **MCP** (recommended for AI agents) | AI agents with MCP support | OAuth 2.1 → tools/list → notary_quote → HTTP /notarize (pay) → notary_verify |
| **HTTP API** (for developers) | Direct integration, scripts, CI/CD | POST /notarize → 402 → pay → 200 |

Both interfaces produce the same PDR. Pick one.

---

## Interface 1: MCP (for AI Agents)

### Endpoint

```
https://api.aotrust.link/mcp
```

### Authentication

OAuth 2.1 with PKCE (S256). Discovery:

- Resource: `https://api.aotrust.link/.well-known/oauth-protected-resource/mcp`
- Authorization server: `https://api.aotrust.link/.well-known/oauth-authorization-server`
- Register client: `POST https://api.aotrust.link/oauth/register`
- Authorize: `GET https://api.aotrust.link/oauth/authorize`
- Token: `POST https://api.aotrust.link/oauth/token`

### Available Tools (4)

| Tool | Purpose | Payment? |
|------|---------|----------|
| `notary_quote` | Get price + payment details for a work_hash | Free |
| `notary_notarize` | NEAR_DIRECT payment (not available on mainnet) | — |
| `notary_notarize_paid` | x402 USDC — discovery only, cannot be called via MCP (see flow below) | $0.01 USDC |
| `notary_verify` | Verify a notarization by job_id | Free |

### MCP Flow (x402 USDC — the only production path)

x402 payment requires HTTP calls — MCP tool calls alone cannot complete the flow:

1. **MCP:** Call `notary_quote` with `work_hash` (see "Step 1: Compute the Work Hash" below) → get price ($0.01 USDC) and quote details
2. **HTTP:** POST to `https://api.aotrust.link/notarize` with `{"work_hash": "..."}` → get 402 payment requirements (see Step 2 below for format)
3. **HTTP:** Sign EIP-3009 `transferWithAuthorization` with your Ethereum key, then POST to `https://api.aotrust.link/notarize` again with `x-payment` header → get 200 + PDR (see Step 3 below for format)
4. **MCP:** Call `notary_verify` with the `job_id` from step 3 → confirm `anchored`

> **Note:** `notary_notarize_paid` appears in `tools/list` for discovery but cannot be called via MCP — x402 payment headers are not supported in MCP tool calls. Use HTTP POST `/notarize` for the actual payment step.

---

## Interface 2: HTTP API (for Developers)

### Step 1: Compute the Work Hash

Hash your artifact with SHA-256. This is what gets notarized — not the artifact itself.

**Key principle:** The hash must be reproducible by a third party who has the same artifact. Hash the artifact content directly — not metadata about it, not the HTTP response, not the chat history.

#### What to hash (by artifact type)

| Artifact type | What to hash | Python example |
|---------------|-------------|-----------------|
| AI text output | The raw response text, UTF-8 encoded | `hashlib.sha256(response_text.encode('utf-8')).hexdigest()` |
| Source code file | The file content as bytes | `hashlib.sha256(open('main.py','rb').read()).hexdigest()` |
| JSON data | Canonical JSON (sorted keys, no whitespace) | `hashlib.sha256(json.dumps(data, sort_keys=True, separators=(',',':')).encode()).hexdigest()` |
| Binary file (image, PDF, etc.) | The file bytes directly | `hashlib.sha256(open('screenshot.png','rb').read()).hexdigest()` |
| Agent decision | The specific decision string, not the full log | `hashlib.sha256(decision_text.encode('utf-8')).hexdigest()` |
| Structured output | The serialized output string (deterministic format) | `hashlib.sha256(str(output).encode('utf-8')).hexdigest()` |

#### Common mistakes

- ❌ Hashing the HTTP response (includes headers, status code) — hash only the body
- ❌ Hashing the chat history (includes user messages) — hash only the AI output
- ❌ Hashing with different encoding each time — always use UTF-8 for text
- ❌ Hashing the file path string — hash the file content bytes
- ✅ Hash exactly the bytes that constitute the artifact, nothing more, nothing less

### Step 2: Request Notarization (expect HTTP 402)

```bash
curl -X POST https://api.aotrust.link/notarize \
  -H "Content-Type: application/json" \
  -d '{"work_hash":"YOUR_SHA256_HEX","agent_sig":"","agent_pubkey":""}'
```

**Response (HTTP 402):**
```json
{
  "x402Version": 1,
  "accepts": [{
    "scheme": "exact",
    "network": "base",
    "maxAmountRequired": "10000",
    "maxTimeoutSeconds": 300,
    "payTo": "0x97E9af6B4d8a49f509DA99afaB954429Ab8Cc800",
    "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "resource": "/notarize",
    "description": "Notarize agent payload. Returns signed PDR.",
    "extra": {"name": "USD Coin", "version": "2"}
  }],
  "error": "Payment required"
}
```

Payment details are in `accepts[0]`:
- `scheme`: `"exact"` — pay exactly the specified amount
- `network`: `"base"` — Base Mainnet (chain ID 8453)
- `maxAmountRequired`: `"10000"` — 10000 micro-USDC = $0.01 USDC
- `payTo`: where to send payment
- `asset`: USDC contract on Base (`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`)
- `maxTimeoutSeconds`: 300 — payment must be made within 5 minutes

### Step 3: Pay and Get Your PDR

Sign an EIP-3009 `transferWithAuthorization` with your Ethereum key:

- `from`: your wallet address
- `to`: the `payTo` address from `accepts[0]` in Step 2
- `value`: `maxAmountRequired` from Step 2 (10000 = $0.01)
- `validAfter`: current Unix timestamp
- `validBefore`: current time + `maxTimeoutSeconds`
- `nonce`: random 32-byte hex string

Encode the signature as base64url JSON. Send it with the `x-payment` header:

```bash
curl -X POST https://api.aotrust.link/notarize \
  -H "Content-Type: application/json" \
  -H "x-payment: YOUR_BASE64URL_ENCODED_SIGNATURE" \
  -d '{"work_hash":"YOUR_SHA256_HEX","agent_sig":"","agent_pubkey":""}'
```

**Response (HTTP 200):**
```json
{
  "status": "notarized",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "pdr_b64": "AwEFXRE3agAAAABub3...",
  "tx_hash": "0x3c7133009a74...",
  "payment_anchor_type": "X402_BASE",
  "network": "base"
}
```

`pdr_b64` is your 239-byte cryptographic proof (base64-encoded).

### Step 4: Verify Your PDR

Go to `https://verify.aotrust.link` and enter the `job_id`.

Or verify programmatically:

```bash
# By job_id
curl https://api.aotrust.link/v1/notarize/YOUR_JOB_ID/status
```

Response:
```json
{
  "status": "anchored",
  "result": {
    "pdr_b64": "AwEFA1kuagAAAABub3...",
    "payment_hash": "679e323c",
    "merkle_proof": [],
    "near_anchor_tx": "H4MaR5ctqKcPGV3A7DDjANskum8F7h4jjJtSvgM9ZAGp"
  }
}
```

Or verify the PDR directly (no job_id needed):
```bash
curl https://api.aotrust.link/v1/pdr/verify/YOUR_PDR_B64
```

Response:
```json
{
  "valid": true,
  "version": 3,
  "payment_anchor_type": "X402_BASE",
  "subject_hash": "0000000000000000000000000000000000000000000000000000000000000000",
  "work_hash": "d8cb8ce666bdc8053b79029116d937ba2c99640f037877fbafa6320092beef6a",
  "timestamp_utc": 1781993821,
  "issuer_id": "notary-node.near",
  "merkle_root": "e4e495d4216391f3f78332870d2c025c70a1dd0b63d24d059ce3ece9aabd5b14",
  "payment_hash": "cd87ee2300000000000000000000000000000000000000000000000000000000",
  "signature_valid": true,
  "tx_verified_on_chain": false,
  "error": null
}
```

Anyone can verify — no account, no key, no authentication required.

---

## What a PDR Proves

- ✅ Your artifact (identified by its SHA-256 hash) existed at a specific time
- ✅ Payment was settled on Base Mainnet (tx_hash verifiable on-chain)
- ✅ The notary (notary-node.near) signed the record
- ✅ The record is anchored to NEAR blockchain via daily Merkle root

A PDR does NOT reveal your artifact content — only its hash.

## PDR Binary Format (v2.3)

| Format | Size | Payload | Signature |
|--------|------|---------|-----------|
| Internal (server storage) | 193 bytes | 129 bytes | 64 bytes Ed25519 |
| External (client receipt) | 239 bytes | 175 bytes | 64 bytes Ed25519 |

Version byte: 0x03. Signature: NEP-413 Ed25519 over raw payload.

Full binary spec: https://github.com/GitSerge-crypto/aotrust-skills/blob/main/pdr-spec.md

## Example Uses

**Personal Records:** Email correspondence, family letters, personal notes, photographs.
Proves that a specific version of a file existed at a specific time.

**AI Outputs:** Agent reports, LLM responses, generated code, research summaries.
Creates independent evidence of when an AI-generated artifact was produced.

**Business Documents:** Contracts, proposals, specifications, financial reports.
Provides a timestamped provenance record for important documents.

**Technical Artifacts:** Source code, configuration files, datasets, log files.
Creates a verifiable audit trail for technical work.

**Compliance and Audit:** Regulatory evidence, internal approvals, process documentation.
Provides a cryptographically verifiable historical record.

## Privacy

AOTrust does not store or publish your artifact content.
Only the SHA-256 hash of the artifact is included in the PDR.
Anyone can verify the PDR, but the original artifact remains private unless you choose to share it.

## Optional: Proof of Authorship (Planned)

By default, AOTrust proves that a hash existed at a specific time.
Future versions may optionally allow clients to sign the artifact hash with their own cryptographic key before notarization.

This creates a stronger provenance chain:
Client Key → Artifact Hash → AOTrust PDR → Blockchain Anchor

Useful for: agent reputation, creator attribution, audit trails, dispute resolution.

The standard PDR workflow remains unchanged and does not require client signatures.

---

## Error Reference

| Response | Meaning | Action |
|----------|---------|--------|
| HTTP 402 | Expected — payment required | Proceed to Step 3 |
| HTTP 400 | Invalid work_hash format | Must be 64-char lowercase hex |
| HTTP 409 | Duplicate work_hash | Already notarized — use verify |
| HTTP 429 | Rate limited | Wait 60 seconds, retry once |

---

## Notes

- Price: **$0.01 USDC** flat per PDR. No tiers, no subscriptions.
- PDRs are **immutable**. Once issued, they cannot be modified.
- Payment is **non-refundable** after PDR issuance.
- Daily Merkle root anchored to NEAR by `notary-node.near`.
- Rate limit: 60 requests/minute per IP.
- PDR spec: https://github.com/GitSerge-crypto/aotrust-skills/blob/main/pdr-spec.md
- PDR parser (standalone, offline): https://github.com/GitSerge-crypto/aotrust-skills/blob/main/pdr_parser.py

---

## Changelog

- v3.6.1 — Added "What to Hash" examples (Step 1), common mistakes section
