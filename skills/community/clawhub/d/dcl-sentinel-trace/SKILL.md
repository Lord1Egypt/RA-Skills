---
name: dcl-sentinel-trace
description: >
  Detect and redact personally identifiable information in AI outputs before
  they reach users or downstream systems — emails, phones, national IDs, bank
  cards, IBANs, crypto addresses, IPs, passports. Runs as a free
  instruction-only checklist, or as a real, paid regex scan (with a Luhn
  checksum on card numbers) via the live DCL Trust Oracle MCP server
  (Leibniz Layer™ protocol), settled on-chain via x402 (USDC on Base). Part
  of the DCL Skills security suite by Fronesis Labs.
tags: [pii, redaction, privacy, data-protection, security, audit-trail, x402, mcp]
---

# DCL Sentinel Trace — Leibniz Layer™

**Publisher:** @daririnch · Fronesis Labs
**Version:** 3.0.0
**Part of:** DCL Skills · Leibniz Layer™ Security Suite
**MCP endpoint:** `https://mcp.fronesislabs.com/mcp` (DCL Trust Oracle)

---

## ⚠️ Now backed by a live, paid regex scan — same checklist, real server

Starting with v3.0.0, the categories below can be run two ways:

1. **Free, instruction-only** — the agent works through the checklist itself, entirely inside
   its own context. No network call, no charge.
2. **Paid, live** — the same eight categories, run as real regex (plus a Luhn checksum on card
   numbers to cut false positives) against the live **DCL Trust Oracle** MCP server, settled
   on-chain via **x402 in USDC on the Base network**, returning a cryptographic `tx_hash` seal.
   No subscription, no account — pay per call.

This is a close one-to-one match: the live tool implements the same T1-T8 categories documented
here. Use the free mode for manual review or offline work; use the live mode when you want an
independently verifiable, on-chain-anchored proof of the scan.

---

## What this skill does

Detects and redacts personally identifiable information in AI outputs before they reach users or
downstream systems.

### What gets detected

| Category | Examples |
|----------|---------|
| `email` | Any email address pattern |
| `phone` | International format numbers (with country code) |
| `national_id` | US-style SSN pattern (`###-##-####`) |
| `bank_card` | Card PANs, verified with a Luhn checksum to reduce false positives |
| `iban` | International bank account numbers |
| `crypto_address` | Bitcoin and Ethereum wallet address formats |
| `ip_address` | IPv4 and IPv6 addresses |
| `passport` | Passport/document numbers appearing in explicit passport context |

### When to use this skill

- AI output may contain **personal data** from user input, documents, or retrieved content
- A **coding or data agent** processes datasets that may contain real PII
- You need a **privacy checkpoint** before logging or storing AI outputs

---

## Live tool (paid, USDC on Base via x402)

| MCP tool | Price | What it runs |
|---|---|---|
| `dcl_evaluate_pii` | **$0.02** | Regex scan across all 8 categories above; any finding → `NO_COMMIT` |

### Connecting to the live server

```json
{
  "mcpServers": {
    "dcl-trust-oracle": {
      "url": "https://mcp.fronesislabs.com/mcp"
    }
  }
}
```

Payment is handled automatically for x402-capable clients; clients without native x402 support
fall back to a guided payment flow. No API key or account signup is required — only a wallet
capable of paying in USDC on Base. Prices are set server-side and may change; the MCP tool
description returned by the server at call time is the source of truth.

### Calling the tool

```python
result = dcl_evaluate_pii(
    response=agent_output,
    agent_id="my-agent-01",
)

if result["verdict"] == "NO_COMMIT":
    redact_and_reprocess(result["findings"])
else:
    log_audit(result["tx_hash"])
```

### Output shape

```json
{
  "verdict": "COMMIT | NO_COMMIT",
  "risk_score": 0.0,
  "findings": [
    {
      "type": "email",
      "position": 14,
      "redacted_sample": "jo****doe.com",
      "severity": "major",
      "category": "T1"
    }
  ],
  "detection_count": 0,
  "categories_checked": ["T1","T2","T3","T4","T5","T6","T7","T8"],
  "categories_clear": ["T1","T2","T3","T4","T5","T6","T7","T8"],
  "tx_hash": "string",
  "chain_index": 0,
  "input_hash": "string",
  "timestamp": 0.0,
  "seal_text": "🔒 Verified by Leibniz Layer | Fronesis Labs\nHash: ...\nIntent: ...\nSealed: ... — Base Mainnet\nVerify: https://x402.fronesislabs.com/verify/...",
  "verify_url": "https://x402.fronesislabs.com/verify/<hash>"
}
```

Only `input_hash` (a hash of the scanned text) and finding metadata are written to the audit
chain — the raw text and any real personal data are never stored. `redacted_sample` shows only
the first 2 and last 4 characters of any match.

---

## Free instruction-only checklist (no network call, no charge)

Paste the text to scan into the conversation and work through the checklist below entirely
inside the agent's own context. Nothing here contacts any server.

### Step 1 — Run the detection checklist

Work through each category. For each match found, record `type`, a `redacted_sample` (masked
version, e.g. `te****@****.com`), and `severity` (`critical` for financial/ID data, `major` for
contact data, `minor` for IP addresses).

### Step 2 — Apply verdict logic

| Condition | Verdict |
|---|---|
| Any finding | `NO_COMMIT` |
| No findings | `COMMIT` |

### Detection Checklist

**T1 — Email Addresses (Major)**
- [ ] Any string matching `[text]@[domain].[tld]` pattern

**T2 — Phone Numbers (Major)**
- [ ] International format: `+[country code][number]`

**T3 — National ID / SSN (Critical)**
- [ ] US SSN: three digits, two digits, four digits pattern
- [ ] National ID formats for other countries in ID context

**T4 — Bank Card PANs (Critical)**
- [ ] 13-19 digit sequences matching major card network prefixes, passing a Luhn checksum

**T5 — IBANs (Critical)**
- [ ] Two-letter country code + two check digits + up to 30 alphanumeric characters

**T6 — Crypto Wallet Addresses (Major)**
- [ ] Bitcoin: Base58 strings of 25-34 chars starting with `1`, `3`, or `bc1`
- [ ] Ethereum: 42-char hex strings starting with `0x`

**T7 — IP Addresses (Minor)**
- [ ] IPv4: four octets separated by dots
- [ ] IPv6: eight groups of hex digits separated by colons

**T8 — Passport / Document Numbers (Critical)**
- [ ] Alphanumeric strings of 6-9 characters in explicit passport/document-number context

---

## DCL Sentinel Trace vs DCL Secret Leak Detector

These two skills are **complementary, not competing**. Run both.

| | DCL Sentinel Trace | DCL Secret Leak Detector |
|---|---|---|
| **Focus** | Personal identity data | Technical credentials |
| **Catches** | Emails, phones, national IDs, IBANs, card PANs | API keys, tokens, private keys, DB URLs |
| **Primary risk** | Privacy breach | Security breach / credential compromise |
| **Live tool** | `dcl_evaluate_pii` ($0.02) | `dcl_evaluate_secrets` ($0.02) |

A response can be free of credentials and still expose personal data. Both checks are necessary
for complete output coverage.

---

## Where Sentinel Trace fits in the DCL pipeline

```
Untrusted input
        │
        ▼
DCL Prompt Firewall        ← blocks malicious input
        │ COMMIT
        ▼
      LLM
        │
        ▼
DCL Policy Enforcer        ← policy check on output
        │ COMMIT
        ▼
DCL Sentinel Trace         ← this skill — PII redaction
        │ COMMIT
        ▼
DCL Secret Leak Detector   ← credential scan
        │ COMMIT
        ▼
DCL Semantic Drift Guard   ← hallucination check
        │ IN_COMMIT
        ▼
Safe to deliver
```

---

## Privacy & Data Policy

Operated by **Fronesis Labs**. The free checklist runs 100% instruction-only — no network
requests, no content transmitted anywhere. For the live tool: only a hash of the scanned text
(`input_hash`) and finding metadata are written to the on-chain audit trail; raw text and
detected personal data are never stored server-side. Only redacted samples ever appear in output.

Full policy: **https://fronesislabs.com/#privacy** · Questions: support@fronesislabs.com

---

## Related skills

- `dcl-secret-leak-detector` — Credential and API key scan
- `dcl-prompt-firewall` — Input-layer injection and jailbreak detection
- `dcl-policy-enforcer` — Policy and jailbreak detection for AI outputs
- `dcl-semantic-drift-guard` — Hallucination and grounding check

**Leibniz Layer™ · Fronesis Labs · fronesislabs.com**
