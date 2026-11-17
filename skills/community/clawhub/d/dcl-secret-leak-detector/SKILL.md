---
name: dcl-secret-leak-detector
description: >
  Scan AI agent outputs, tool results, and pipeline data for exposed secrets
  and credentials — API keys, tokens, private keys, database URLs, .env values
  — before they reach users, logs, or downstream systems. Runs as a free
  instruction-only checklist, or as a real, paid regex scan via the live DCL
  Trust Oracle MCP server (Leibniz Layer™ protocol) with an on-chain audit
  proof settled via x402 (USDC on Base). The specialist companion to DCL
  Sentinel Trace — for secrets, not just PII. Part of the DCL Skills security
  suite by Fronesis Labs.
tags: [secret-detection, credential-leak, api-key, token-leak, devsecops, runtime-security, x402, mcp, audit-trail]
---

# DCL Secret Leak Detector — Leibniz Layer™

**Publisher:** @daririnch · Fronesis Labs
**Version:** 2.0.0
**Part of:** DCL Skills · Leibniz Layer™ Security Suite
**MCP endpoint:** `https://mcp.fronesislabs.com/mcp` (DCL Trust Oracle)

---

## ⚠️ Now backed by a live, paid regex scan — same checklist, real server

Starting with v2.0.0, the categories below can be run two ways:

1. **Free, instruction-only** — the agent works through the checklist itself, entirely inside
   its own context. No network call, no charge.
2. **Paid, live** — the same eight categories, run as real regex against the live **DCL Trust
   Oracle** MCP server, settled on-chain via **x402 in USDC on the Base network**, returning a
   cryptographic `tx_hash` seal. No subscription, no account — pay per call.

Unlike some other DCL skills, this one is a close one-to-one match: the live tool implements
the same S1-S8 categories documented here, so the two modes should agree. Use the free mode for
manual review or offline work; use the live mode when you want an independently verifiable,
on-chain-anchored proof of the scan.

---

## What this skill does

Scans AI agent outputs, tool results, and pipeline data for exposed secrets and credentials —
before they reach users, logs, or downstream systems.

### What gets detected

| Category | Pattern class |
|----------|--------------|
| `api_key` | Provider-prefixed keys: OpenAI, Anthropic, Stripe, GitHub, Slack, SendGrid, Twilio patterns |
| `cloud_credential` | AWS access key IDs, AWS secret access keys, GCP service account fragments |
| `token` | JWTs, Bearer tokens |
| `private_key_pem` | PEM header/footer blocks for any private key type |
| `database_url` | Connection strings with embedded credentials: `proto://user:pass@host` |
| `connection_string` | ADO.NET / ODBC style strings with `User ID=`/`Password=` fields |
| `env_assignment` | `.env`-style lines where the variable name matches known secret patterns |
| `webhook_secret` | Signed secrets for platforms like Stripe |
| `internal_endpoint` | URLs containing API keys or tokens as query parameters |

---

## Live tool (paid, USDC on Base via x402)

| MCP tool | Price | What it runs |
|---|---|---|
| `dcl_evaluate_secrets` | **$0.02** | Regex scan across all 8 categories above; any finding → `NO_COMMIT` |

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
result = dcl_evaluate_secrets(
    response=agent_output,
    agent_id="my-agent-01",
)

if result["verdict"] == "NO_COMMIT":
    block_and_alert(result["findings"])
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
      "type": "api_key",
      "provider": "openai",
      "position": 87,
      "redacted_sample": "sk****************3456",
      "severity": "critical",
      "category": "S1"
    }
  ],
  "detection_count": 0,
  "categories_checked": ["S1","S2","S3","S4","S5","S6","S7","S8"],
  "categories_clear": ["S1","S2","S3","S4","S5","S6","S7","S8"],
  "tx_hash": "string",
  "chain_index": 0,
  "input_hash": "string",
  "timestamp": 0.0,
  "seal_text": "🔒 Verified by Leibniz Layer | Fronesis Labs\nHash: ...\nIntent: ...\nSealed: ... — Base Mainnet\nVerify: https://x402.fronesislabs.com/verify/...",
  "verify_url": "https://x402.fronesislabs.com/verify/<hash>"
}
```

Only `input_hash` (a hash of the scanned text) and finding metadata are written to the audit
chain — the raw text and any real secret values are never stored. `redacted_sample` shows only
the first 2 and last 4 characters of any match.

---

## Free instruction-only checklist (no network call, no charge)

Paste the text to scan into the conversation and work through the checklist below entirely
inside the agent's own context. Nothing here contacts any server.

### Step 1 — Confirm content is in context

Verify the text to scan is present in the conversation. If not provided, ask the user to paste it.

### Step 2 — Compute content fingerprint

```
content_hash = SHA-256(raw text submitted for scanning)
```

### Step 3 — Run the detection checklist

Work through every category below. For each match found, record `type`, `provider` (if
identifiable), `position`, a `redacted_sample` (first 2 and last 4 chars only), and `severity`.
If no patterns match a category, mark it `CLEAR`.

### Step 4 — Apply verdict logic

| Condition | Verdict |
|---|---|
| Any finding at any severity | `NO_COMMIT` |
| No findings | `COMMIT` |

Secrets have no safe threshold — any detected secret results in `NO_COMMIT`.

### Step 5 — Compute DCL fingerprint

```
analysis_content  = verdict + all findings serialized + timestamp
analysis_hash     = SHA-256(analysis_content)
dcl_fingerprint   = "DCL-SLD-" + date + "-" + content_hash[:8] + "-" + analysis_hash[:8]
```

### Detection Checklist

**S1 — API Keys (Critical)**
- [ ] Short prefix followed by 20+ alphanumeric chars matching known provider key formats
- [ ] Live payment key prefixes (distinct from test/publishable key prefixes)
- [ ] Version control platform personal access token prefixes
- [ ] Messaging platform bot/user token prefixes

**S2 — Cloud Credentials (Critical)**
- [ ] Cloud provider access key ID patterns
- [ ] Cloud provider secret key context: high-entropy string near credential field names
- [ ] Service account JSON fragments: private key fields, client email fields

**S3 — Tokens & JWTs (Critical)**
- [ ] JWT pattern: three base64url segments separated by dots
- [ ] Bearer token context: authorization header values with high-entropy content

**S4 — Private Keys (Critical)**
- [ ] PEM block opening/closing markers for any private key type

**S5 — Database & Connection Strings (Critical)**
- [ ] URI with embedded credentials: protocol + `://` + username + `:` + password + `@` + host
- [ ] ORM/driver connection strings containing password parameter fields

**S6 — Environment Variable Assignments (Major)**
- [ ] Variable assignments where the name contains `KEY`, `SECRET`, `TOKEN`, `PASS`, `PWD`, `CREDENTIAL`, `AUTH`

**S7 — Webhook & Signed URL Secrets (Major)**
- [ ] Webhook secret prefixes for known payment/developer platforms
- [ ] Signed URL patterns where a signature or secret appears as a query parameter

**S8 — Internal Endpoints with Auth (Minor → Major)**
- [ ] Internal hostnames with auth query parameters
- [ ] Any URL where `api_key=`, `token=`, `secret=`, or `access_token=` appears with a non-trivial value

---

## Secret Leak Detector vs DCL Sentinel Trace

These two skills are **complementary, not competing**. Run both.

| | DCL Sentinel Trace | DCL Secret Leak Detector |
|---|---|---|
| **Focus** | Personal identity data | Technical credentials |
| **Catches** | Emails, phones, national IDs, IBANs, card PANs | API keys, tokens, private keys, DB URLs |
| **Primary risk** | Privacy breach | Security breach / credential compromise |
| **Live tool** | `dcl_evaluate_pii` ($0.02) | `dcl_evaluate_secrets` ($0.02) |

A response can be PII-clean and still contain a live credential. Both checks are necessary for
complete output coverage.

---

## Where Secret Leak Detector fits in the DCL pipeline

```
Untrusted input
        │
        ▼
DCL Prompt Firewall          ← blocks malicious input
        │ COMMIT
        ▼
      LLM call
        │
        ▼
DCL Policy Enforcer          ← policy & jailbreak check
        │ COMMIT
        ▼
DCL Sentinel Trace           ← PII redaction
        │ COMMIT
        ▼
DCL Secret Leak Detector     ← this skill — credential & secret scan
        │ COMMIT
        ▼
DCL Semantic Drift Guard     ← hallucination & grounding check
        │ IN_COMMIT
        ▼
Safe to deliver
```

---

## High-risk agent patterns

**Coding agents** — generate shell scripts, Dockerfiles, CI configs, Terraform. Common vector for hardcoded credentials appearing in generated output.

**DevOps / infrastructure agents** — read deployment configs, env files, Kubernetes secrets. May quote them verbatim in responses.

**RAG pipelines over internal docs** — internal wikis and runbooks routinely contain credentials left by engineers. Retrieved chunks can carry them into LLM context and outputs.

**Tool-calling agents** — an agent that calls an API internally may reproduce the key in its reasoning trace or final response.

---

## Privacy & Data Policy

Operated by **Fronesis Labs**. The free checklist runs 100% instruction-only — no network
requests, no content transmitted anywhere. For the live tool: only a hash of the scanned text
(`input_hash`) and finding metadata are written to the on-chain audit trail; raw text and
detected secret values are never stored server-side. Only redacted samples ever appear in output.

Full policy: **https://fronesislabs.com/#privacy** · Questions: support@fronesislabs.com

---

## Related skills

- `dcl-sentinel-trace` — PII redaction and identity exposure detection
- `dcl-prompt-firewall` — Input-layer injection and jailbreak detection
- `dcl-policy-enforcer` — Policy and jailbreak detection for AI outputs
- `dcl-semantic-drift-guard` — Hallucination and grounding check

**Leibniz Layer™ · Fronesis Labs · fronesislabs.com**
