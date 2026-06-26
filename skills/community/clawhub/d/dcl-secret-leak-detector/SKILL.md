---
description: "Instruction-only runtime secret and credential leak detector for AI agents and LLM pipelines. Catches API keys, tokens, private keys, database URLs, and .env values entirely within the agent context — no text ever leaves the agent. Every detection produces a deterministic DCL audit proof. The specialist companion to DCL Sentinel Trace — for secrets, not just PII."
tags: [secret-detection, credential-leak, api-key, token-leak, private-key, env-leak, database-credentials, runtime-security, llm-guardrails, agent-safety, compliance, audit, tamper-evident, cryptographic-proof, leibniz-layer, ai-safety, pipeline-security, devsecops, secrets-management, instruction-only, zero-trust]
---

# DCL Secret Leak Detector — Leibniz Layer™

**Publisher:** @daririnch · Fronesis Labs  
**Version:** 1.0.0  
**Part of:** Leibniz Layer™ Security Suite

---

## What this skill does

DCL Secret Leak Detector scans AI agent outputs, tool results, and pipeline data for exposed secrets and credentials — before they reach users, logs, or downstream systems.

**This skill is 100% instruction-only.** No text is sent to any external server. No webhook is called. The entire analysis runs inside the agent's context window using the detection checklist below. The scanned text never leaves the agent.

Every detection produces a deterministic `dcl_fingerprint` — a self-contained audit proof compatible with the Leibniz Layer™ chain.

### What gets detected

| Category | Pattern class |
|----------|--------------|
| `api_key` | Provider-prefixed keys: OpenAI, Anthropic, Stripe, GitHub, Slack patterns |
| `cloud_credential` | AWS access key IDs, GCP service account fragments, Azure client secrets |
| `token` | Bearer tokens, JWT strings, OAuth access tokens, high-entropy credential-context strings |
| `private_key_pem` | PEM header/footer blocks for any private key type |
| `database_url` | Connection strings with embedded credentials: `proto://user:pass@host` |
| `connection_string` | ADO.NET, ODBC, SQLAlchemy strings containing password fields |
| `env_assignment` | `.env`-style lines where variable name matches known secret patterns |
| `webhook_secret` | Signed secrets for Stripe, GitHub, Twilio webhook endpoints |
| `internal_endpoint` | URLs containing API keys or tokens as query parameters |

---

## How to run a scan

The user provides text to scan directly in the conversation — model output, tool result, generated code, retrieved document chunk, or any pipeline data. This skill makes **no network requests** and does not transmit content anywhere.

### Step 1 — Confirm content is in context

Verify the text to scan is present in the conversation. If not provided, ask the user to paste it.

### Step 2 — Compute content fingerprint

```
content_hash = SHA-256(raw text submitted for scanning)
```

Record this as the immutable identifier for this scan event.

### Step 3 — Run the detection checklist

Work through every category in the **Detection Checklist** below. For each match found, record:

- `type` — which category triggered
- `provider` — which service the credential belongs to (if identifiable)
- `position` — approximate character offset in the text
- `redacted_sample` — masked version showing only first 2 and last 4 chars
- `severity` — `critical`, `major`, or `minor`

If no patterns match a category, mark it `CLEAR`.

### Step 4 — Apply verdict logic

| Condition | Verdict |
|---|---|
| Any finding at any severity | `NO_COMMIT` |
| No findings | `COMMIT` |

Any detected secret, regardless of severity, results in `NO_COMMIT`. Secrets have no safe threshold.

### Step 5 — Compute DCL proof

```
analysis_content  = verdict + all findings serialized + timestamp
analysis_hash     = SHA-256(analysis_content)
dcl_fingerprint   = "DCL-SLD-" + date + "-" + content_hash[:8] + "-" + analysis_hash[:8]
```

---

## Detection Checklist

Work through each item. Mark CLEAR or record finding with redacted evidence.

### S1 — API Keys (Critical)
- [ ] Short prefix followed by 20+ alphanumeric chars matching known provider key formats
- [ ] Live payment key prefixes (distinct from test/publishable key prefixes)
- [ ] Version control platform personal access token prefixes
- [ ] Messaging platform bot/user token prefixes
- [ ] Email delivery platform key prefixes
- [ ] Communications platform account SID patterns

### S2 — Cloud Credentials (Critical)
- [ ] Cloud provider access key ID patterns (uppercase alpha + numeric, fixed length)
- [ ] Cloud provider secret key context: high-entropy base64 string near credential field names
- [ ] Service account JSON fragments: private key fields, client email fields
- [ ] Client secret values in tenant/application ID combinations

### S3 — Tokens & JWTs (Critical)
- [ ] JWT pattern: three base64url segments separated by dots, first segment decodes to JSON header
- [ ] Bearer token context: authorization header values or token field assignments with high-entropy values
- [ ] High-entropy strings (40+ chars) appearing in credential assignment context

### S4 — Private Keys (Critical)
- [ ] PEM block opening markers: `-----BEGIN` + key type descriptor + `-----`
- [ ] PEM block closing markers: `-----END` + key type descriptor + `-----`
- [ ] Base64-encoded content between PEM markers

### S5 — Database & Connection Strings (Critical)
- [ ] URI with embedded credentials: protocol + `://` + username + `:` + password + `@` + host
- [ ] Database protocols: postgres, mysql, mongodb, redis, amqp, and their variants
- [ ] ORM/driver connection strings containing password parameter fields
- [ ] Connection strings with `User ID=` and `Password=` or `Pwd=` fields

### S6 — Environment Variable Assignments (Major)
- [ ] Variable assignments where name contains: `KEY`, `SECRET`, `TOKEN`, `PASS`, `PWD`, `CREDENTIAL`, `AUTH`
- [ ] Assignment format: `VARNAME=value` where value is non-trivial (not placeholder, not empty)
- [ ] Shell export statements with credential variable names

### S7 — Webhook & Signed URL Secrets (Major)
- [ ] Webhook secret prefixes for known payment and developer platforms
- [ ] Signed URL patterns where the signature or secret appears as a query parameter

### S8 — Internal Endpoints with Auth (Minor → Major)
- [ ] Internal hostnames (`.internal`, `.local`, `.corp`, `.intra`) with auth query parameters
- [ ] Any URL where `api_key=`, `apikey=`, `token=`, `secret=`, or `access_token=` appears with a non-trivial value (Major)

---

## Output schema

```json
{
  "verdict": "COMMIT | NO_COMMIT",
  "risk_score": 0.0,
  "content_hash": "sha256:<64-char hex>",
  "analysis_hash": "sha256:<64-char hex>",
  "dcl_fingerprint": "DCL-SLD-2026-04-14-<content_hash[:8]>-<analysis_hash[:8]>",
  "detections": [
    {
      "type": "api_key",
      "provider": "identified provider name",
      "redacted_sample": "[PREFIX]-****...****[SUFFIX]",
      "position": 87,
      "severity": "critical"
    }
  ],
  "detection_count": 0,
  "categories_checked": ["S1","S2","S3","S4","S5","S6","S7","S8"],
  "categories_clear": ["S1","S2","S3","S4","S5","S6","S7","S8"],
  "timestamp": "2026-04-14T09:00:00Z",
  "powered_by": "DCL Secret Leak Detector · Leibniz Layer™ · Fronesis Labs"
}
```

`detections` is an empty array `[]` when verdict is `COMMIT`.

---

## Secret Leak Detector vs DCL Sentinel Trace

These two skills are **complementary, not competing**. Run both.

| | DCL Sentinel Trace | DCL Secret Leak Detector |
|---|---|---|
| **Focus** | Personal identity data | Technical credentials |
| **Catches** | Emails, phones, SSNs, IBANs, card PANs | API keys, tokens, private keys, DB URLs |
| **Regulation** | GDPR, HIPAA | SOC 2, ISO 27001, internal SecOps |
| **Primary risk** | Privacy breach | Security breach / credential compromise |
| **External calls** | Via webhook | None — instruction-only |

A response can be PII-clean and still contain a live credential. Both checks are necessary for complete output coverage.

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
DCL Policy Enforcer          ← compliance & jailbreak check
        │ COMMIT
        ▼
DCL Sentinel Trace           ← PII redaction
        │ COMMIT
        ▼
DCL Secret Leak Detector     ← credential & secret scan (instruction-only)
        │ COMMIT
        ▼
DCL Output Sanitizer         ← final sweep: toxic, unsafe commands
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

This skill is operated by **Fronesis Labs** and is **100% instruction-only**.

**No data leaves the agent.** The text submitted for scanning is analyzed entirely within the agent's context window. No content is transmitted to any server — including Fronesis Labs infrastructure.

**No retention.** Nothing is stored, logged, or transmitted. The only artifact produced is the structured JSON output and `dcl_fingerprint`, which remain within the agent's session unless the caller saves them.

**Detected secrets:** Only redacted samples are included in output. Raw credential values are never reproduced in the result.

Full policy: **https://fronesislabs.com/#privacy** · Browse the full DCL Security Suite: **[hub.fronesislabs.com](https://hub.fronesislabs.com)** · Questions: support@fronesislabs.com

---

## Related skills

- `dcl-sentinel-trace` — PII redaction and identity exposure detection
- `dcl-prompt-firewall` — Input-layer injection and jailbreak detection
- `dcl-output-sanitizer` — Final output sweep: toxic content, unsafe commands
- `dcl-secret-leak-detector-crypto` — Specialist version for wallet keys, seed phrases, exchange credentials

**Leibniz Layer™ · Fronesis Labs · fronesislabs.com**
