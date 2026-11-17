---
name: aotrust-notarize
description: >
  Issue a cryptographic proof (PDR) that a digital artifact existed at a specific time.
  Pay $0.01 USDC on Base or Solana via x402 (MCP); optional evidence bundle $0.02 and
  signed time attestation $0.002. Receipts are leaves in an append-only Merkle log
  anchored hourly to NEAR blockchain; inclusion and consistency proofs are public.
  ONLY invoke when the user explicitly requests notarization or proof-of-existence for a
  specific artifact. This skill performs a paid external API call ($0.01 USDC, irreversible).
  Do NOT invoke proactively or as part of unrelated workflows.
license: MIT
metadata:
  author: aotrust
  version: "3.10.1"
  mcp-endpoint: https://api.aotrust.link/mcp
  http-endpoint: https://api.aotrust.link/notarize
  verification-endpoint: https://api.aotrust.link/v1/pdr/verify
  near-handle: aotrust
---

# AOTrust — Cryptographic Proof of Existence

## ⚠ Before You Start — Security & Consent

This skill interacts with an **external paid API**. Read this before invoking.

| What leaves your machine | Where it goes | Reversible? |
|--------------------------|---------------|-------------|
| `work_hash` (SHA-256 of your artifact) | api.aotrust.link | No — hash is public in the PDR |
| `agent_sig` + `agent_pubkey` (optional, bilateral) | api.aotrust.link | No — stored in notary ledger |
| EIP-3009 payment signature | Base Mainnet (on-chain) | No — $0.01 USDC, irreversible |

**Rules:**
- **Confirm with the user** before notarizing. Show the artifact hash and ask: "Notarize this for $0.01 USDC?"
- **Never use an unattended wallet.** Payment requires manual approval for every transaction.
- **Do not let the agent manage private keys.** The user signs EIP-3009 manually or via a wallet that requires confirmation.
- The artifact itself is never uploaded — only its hash. But the hash is public in the PDR and on NEAR blockchain.

---

A PDR (Provenance Data Record) is a 239-byte cryptographic receipt proving
that a digital artifact existed at a specific point in time.

Works with any digital artifact:
emails, documents, contracts, source code, AI outputs,
research notes, datasets, photos, logs, sensor readings.

The artifact itself is never uploaded — only its SHA-256 hash.

Receipts are anchored hourly to NEAR blockchain (cumulative Merkle log, RFC 9162 inclusion/consistency
proofs). $0.01 per proof. No account needed.

## Two Ways to Connect

| Interface | Best for | How |
|-----------|----------|-----|
| **MCP** (recommended for AI agents) | AI agents with MCP support | tools/list → notary_notarize_paid (x402 in-band micropayment) |
| **HTTP API** (for developers) | Direct integration, scripts, CI/CD | POST /notarize → 402 → pay → 200 |

Both interfaces produce the same PDR. Pick one.

---

## Interface 1: MCP (for AI Agents)

### Endpoint

```
https://api.aotrust.link/mcp
```

### Authentication

**None required.** The MCP endpoint works without any token or OAuth flow —
connect and call `tools/list` directly. Free-tier tools (`notary_free`,
`notary_quote`, `notary_verify`) are keyless; paid notarization uses in-band
x402 micropayments (no API key either).

OAuth 2.1 endpoints exist as optional discovery stubs (used by the
agents.near.ai integration path):

- Resource: `https://api.aotrust.link/.well-known/oauth-protected-resource/mcp`
- Authorization server: `https://api.aotrust.link/.well-known/oauth-authorization-server`
- Register client: `POST https://api.aotrust.link/oauth/register`
- Authorize: `GET https://api.aotrust.link/oauth/authorize`
- Token: `POST https://api.aotrust.link/oauth/token`

### Available Tools (9)

| Tool | Purpose | Payment? |
|------|---------|----------|
| `notary_free` | Create instant free cryptographic proof (UNPAID PDR), rate limited (5 per 24 h per IP, 1000/day global) | Free |
| `notary_quote` | Get price + payment details for a work_hash | Free |
| `notary_notarize` | NEAR_DIRECT payment (not available on mainnet) | — |
| `notary_notarize_paid` | Notarize artifact, on-chain settlement — x402-over-MCP (in-band; Base or Solana USDC) or HTTP fallback (Base-only) | $0.01 USDC |
| `notary_bundle` | Read-only evidence pack for an existing hash: **earliest** issuance + anchor + inclusion path + verify recipe (never creates a PDR) | $0.02 USDC |
| `notary_time_attest` | Signed timestamp (AOT-TS1) bound to a payload hash, leaf in the same cumulative log | $0.002 USDC |
| `notary_pdr_by_tx` | Look up a receipt by payment tx (full 64-hex payment hash) | Free |
| `notary_anchor` | Anchor status / proof / logproof / consistency (RFC 9162) | Free |
| `notary_verify` | Verify a notarization by job_id or pdr_b64 | Free |

Live price list in one request: `GET https://api.aotrust.link/menu`.

### MCP Flow — Free Tier (no wallet, 1 step)

For instant free proof without payment:

1. **MCP:** Call `notary_free` with `work_hash` (64 hex) → get `shield_id`, `pdr_b64`, `verify_url`
2. Done. No wallet, no payment. Rate limited: 5 per 24 h per IP (IPv6 counted per /64), 1000/day global.

> For on-chain settlement proof (payment-bound PDR with tx_hash on Base), use the paid flow below.

### MCP Flow (x402 USDC — paid, in-band settlement)

Paid notarization works **natively over MCP** (x402-over-MCP transport):

1. **MCP:** Call `notary_notarize_paid` with `work_hash` (see "Step 1: Compute the Work Hash" below)
2. **MCP:** Server returns the 402 challenge: `isError: true` + `PaymentRequired` in `structuredContent` (and `content[0].text` as the same JSON)
3. **MCP:** x402-capable agents sign the payment and retry the same call with the signed payload in `params._meta["x402/payment"]` → receive the PDR; the settlement receipt comes in `_meta["x402/payment-response"]`. Two rails are accepted (choose by the `network` field of the challenge entry your wallet supports):
   - **Base (EVM):** EIP-3009 `transferWithAuthorization`, USDC on Base (`eip155:8453`)
   - **Solana (SVM):** USDC-SPL transfer with PayAI as feePayer (`solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp`) — payload field is `{"transaction": "<base64 signed tx>"}`; x402 SVM client libraries handle this automatically
4. **MCP:** Call `notary_verify` with the `job_id` from the PDR → confirm `anchored`

x402-unaware MCP clients should read `content[1]` of the 402 result (human-readable fallback) — direct HTTP clients can still `POST https://api.aotrust.link/notarize` with the `x-payment` header (see Step 3 below for format).

> **Note:** `notary_notarize_paid` is a full paid tool: call it without payment to receive the challenge, then retry with payment attached. No HTTP round-trip is required for x402-capable MCP clients.

---

## Interface 2: HTTP API (for Developers)

> **Prices without a round-trip:** `GET https://api.aotrust.link/menu` returns the live tool list with costs and payment rails in one request (no 402 cycle needed).

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

> **Solana payments are MCP-only.** The HTTP endpoint (`/notarize`) accepts Base (EVM) payments only. Solana (SVM) wallets pay via the MCP flow above (`notary_notarize_paid`).

```bash
curl -X POST https://api.aotrust.link/notarize \
  -H "Content-Type: application/json" \
  -d '{"work_hash":"YOUR_SHA256_HEX","agent_sig":"","agent_pubkey":""}'
  # agent_sig/agent_pubkey optional — include for Bilateral Signature (v0x04)
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

### Bilateral Signature (optional, v0x04)

If you want the PDR to cryptographically bind the agent's signature into the record:

1. Sign your `work_hash` with your Ed25519 private key using NEP-413 (same as Full Chain)
2. Include `agent_sig` (base64) and `agent_pubkey` (hex) in the POST `/notarize` body
3. The notary will produce a v0x04 PDR with a **Binding Hash**: `payload_hash = sha256(work_hash + sig_A + agent_pubkey)`
4. The PDR is still 239 bytes, same price ($0.01), same verification flow

Without `agent_sig` → ordinary v0x03 PDR (`payload_hash = work_hash`).

**Verify response** now includes `binding_hash` (boolean) and `payload_hash` (replaces `work_hash`):
- v0x03: `binding_hash=false`, `payload_hash=work_hash`
- v0x04: `binding_hash=true`, `payload_hash=binding_hash`

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

## Paid Read Products (no new PDR created)

Two read-only products sit on top of an existing receipt — useful when you need *proof about a proof*:

| Product | Price | Endpoint | What you get |
|---|---|---|---|
| **Evidence bundle** | $0.02 | `POST /v1/attestation/bundle` | For a `work_hash` already notarized: the **earliest** issuance (`picked:"earliest"`), all issuances (`issuances[]`), the covering anchor (`anchor.mode/anchor_seq/size/root/index/path`), and a verify recipe. Unknown hash → `404`, nothing charged. Optional `seq` pin → rejected **before** payment (`400 INVALID_SEQ` / `400 SEQ_HASH_MISMATCH`). |
| **Signed time attestation** | $0.002 | `POST /v1/attest/time` | Ed25519 timestamp (`AOT-TS1`) over `payload_hash` + nonce, its leaf (`log_index`) in the same cumulative log, and anchor status. |

```bash
# bundle: 402 first, then pay and repeat
curl -X POST https://api.aotrust.link/v1/attestation/bundle \
  -H "Content-Type: application/json" \
  -d '{"work_hash":"YOUR_SHA256_HEX"}'
```

## Anchor & Transparency (free)

Every receipt is a leaf in an append-only cumulative Merkle tree; the root is committed to NEAR hourly
when new leaves exist. All endpoints are free and need no key:

| Endpoint | Purpose |
|---|---|
| `GET /v1/anchor/status` | latest anchor (seq, size, root, NEAR tx) |
| `GET /v1/anchor/proof/{seq}` | RFC 9162 inclusion path for a leaf (`404` + `latest_seq` if not yet anchored, `409 NOT_YET_ANCHORED` + `Retry-After` when pending) |
| `GET /v1/anchor/logproof/{log_index}` | inclusion by log index (covers time attestations) |
| `GET /v1/anchor/consistency?from=&to=` | proof the log only grew between two anchors |
| `GET /v1/pdr/by-tx/{tx}` | receipt lookup by payment tx (full 64-hex payment hash) |
| `https://docs.aotrust.link/transparency.html` | in-browser verification, protocol epochs, daily network snapshot |

## What a PDR Proves

- ✅ Your artifact (identified by its SHA-256 hash) existed at a specific time
- ✅ Payment was settled on Base Mainnet (tx_hash verifiable on-chain)
- ✅ The notary (notary-node.near) signed the record
- ✅ The record is a leaf in an append-only Merkle log; the root is committed to NEAR hourly and
  inclusion/consistency proofs (RFC 9162) can be checked without trusting AOTrust

A PDR does NOT reveal your artifact content — only its hash.

## PDR Binary Format (v2.3 / v2.4)

| Format | Size | Payload | Signature |
|--------|------|---------|-----------|
| Internal (server storage) | 193 bytes | 129 bytes | 64 bytes Ed25519 |
| External (client receipt) | 239 bytes | 175 bytes | 64 bytes Ed25519 |

Version byte: `0x03` ordinary, `0x04` bilateral. Signature: NEP-413 Ed25519 over
`pack("<II", 2147484061, len(payload)) + payload` — the envelope, **not** the bare payload.

Payment field (bytes 143–175): new paid receipts carry the **full 32-byte** payment identifier;
early legacy receipts carry a 4-byte key padded with zeros (verify via `/v1/pdr/by-tx`); free
receipts carry zeros. Field `semantic_anchor` is deprecated (reserved, zero-filled).

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

## Proof of Authorship (Bilateral Signature, v0x04)

By default, AOTrust proves that a hash existed at a specific time.
For stronger provenance, clients can sign the artifact hash with their own Ed25519 key before notarization — this produces a **bilateral PDR (v0x04)** with a binding hash.

This creates a non-repudiable provenance chain:
Client Key → Artifact Hash → Binding Hash → AOTrust PDR → Blockchain Anchor

See the **Bilateral Signature** section under Step 3 above for implementation details.

Useful for: agent reputation, creator attribution, audit trails, dispute resolution, multi-agent pipelines.

The standard PDR workflow (v0x03) remains available and does not require client signatures.

---

## Error Reference

| Response | Meaning | Action |
|----------|---------|--------|
| HTTP 402 | Expected — payment required | Proceed to Step 3 |
| HTTP 400 | Invalid `work_hash` / `seq` (`INVALID_SEQ`, `SEQ_HASH_MISMATCH`) | hash must be 64 lowercase hex; omit `seq` or pass one that belongs to the hash |
| HTTP 404 | No receipt for this hash / tx / anchor yet (`NOT_FOUND`, `NOT_YET_ANCHORED` on old SDKs) | issue a PDR first; for anchors use `/v1/anchor/status` |
| HTTP 409 | `NOT_YET_ANCHORED` — leaf exists, anchor pending | retry after `Retry-After` (≤ 1 anchor interval) |
| HTTP 410 | `/v1/shield/direct` retired | use `POST https://shield.aotrust.link/shield` ($0.10) |
| HTTP 502 | `PAYMENT_UNCONFIRMED` — facilitator said ok, chain says no | do not retry blindly; contact support with `tx_hash` |
| HTTP 429 | Rate limited | Wait 60 seconds, retry once |

---

## Notes

- Price: **$0.01 USDC** per PDR (bundle $0.02, signed time attestation $0.002). No tiers, no subscriptions.
- PDRs are **immutable**. Once issued, they cannot be modified.
- Payment is **non-refundable** after PDR issuance.
- AOTrust supports continuous provenance: re-notarizing the same work_hash is valid and produces a new timestamped PDR. Responses include a `provenance` block (first_seen, total notarizations) linking the new receipt to the original observation; the evidence bundle returns the **earliest** issuance.
- Idempotency: replaying the same payment tx returns the original receipt (`Idempotency-Replayed: true`), never a second ledger row.
- Merkle root committed to NEAR **hourly** (skip-empty) by `notary-node.near`; cumulative tree since 22.10.2026, legacy per-batch anchors before that.
- Rate limit: 60 requests/minute per IP.
- PDR spec: https://github.com/GitSerge-crypto/aotrust-skills/blob/main/pdr-spec.md
- PDR parser (standalone, offline): https://github.com/GitSerge-crypto/aotrust-skills/blob/main/pdr_parser.py

---

## Changelog

- v3.10.1 — republish to clear a stuck 3.10.0 publication (content identical to 3.10.0).
- v3.10.0 — hourly cumulative anchoring (RFC 9162 proofs public), tools 5→9 (`notary_bundle` $0.02, `notary_time_attest` $0.002, `notary_pdr_by_tx`, `notary_anchor`), free tier wording (5 per 24 h per IP / IPv6 /64), paid read products + anchor/transparency sections, payment-field semantics by version, error table (404/409/410/502), idempotency note.
- v3.9.1 — frontmatter version bump (3.8.0 → 3.9.0 missed in v3.9 commit); added /menu pointer to HTTP interface (live price list, one request, no 402 cycle).
- v3.9.0 — Solana rail (X402_SOLANA, pat 0x0A): dual-402 MCP accepts Base (EIP-3009) and Solana (USDC-SPL, PayAI feePayer) payments; HTTP /notarize remains Base-only (documented). PDR verify: payment_anchor_type surfaced; on-chain reveal for Solana via recomputed payment_hash.
- v3.8.0 — Added notary_free tool for instant free-tier notarization via MCP without wallet. Updated tools table (4→5), added Free Tier MCP Flow section.
- v3.7.0 — ClawHub security audit fixes: explicit trigger boundaries in description, Security & Consent section (external transmission warnings, user confirmation rules, wallet safety), updated Proof of Authorship from "Planned" to implemented (Bilateral Signature v0x04).
- v3.6.2 — Bilateral Signature (v0x04): agent_sig + agent_pubkey → binding hash PDR. Verify response: payload_hash + binding_hash fields.
- v3.6.1 — Added "What to Hash" examples (Step 1), common mistakes section