---
name: dcl-policy-enforcer
description: "Use this skill to run a real, paid pre-action audit of an AI agent or LLM response via the live DCL Trust Oracle MCP server. Detects jailbreak / instruction-override attempts, baseline safety violations, and content quality drift, and checks output against pattern-based regulatory-theme checklists (transparency, data handling, financial disclosure, medical disclosure). Every paid call is metered and settled on-chain via the x402 protocol (USDC on Base) and produces a tamper-evident audit record. Use whenever you need to gate a risky agent action, or want a free instruction-only checklist for a quick manual review. Part of the Leibniz Layer™ Security Suite alongside DCL Prompt Firewall and DCL Sentinel Trace."
version: 3.1.0
tags: [compliance, audit, ai-safety, policy-enforcement, anti-jailbreak, prompt-injection, llm-guardrails, leibniz-layer, agent-safety, verification, ai-governance, x402, mcp, paid, usdc, base]
---

# DCL Policy Enforcer — Leibniz Layer™

**Publisher:** @daririnch · Fronesis Labs
**Version:** 3.1.0
**Part of:** Leibniz Layer™ Security Suite
**MCP endpoint:** `https://mcp.fronesislabs.com/mcp`

---

## ⚠️ This skill now calls a live, paid service

Starting with v3.0.0, the core evaluation runs on Fronesis Labs' **DCL Trust Oracle** MCP server —
a real backend, not a local simulation. Each paid tool call is metered and settled on-chain via the
**x402 protocol in USDC on the Base network**. There is no subscription and no account: the calling
agent (or its wallet-enabled MCP client) pays per call at the price listed below.

**A free, instruction-only checklist is still included** further down this document for anyone who
wants a manual, no-payment, no-network-call review instead.

---

## What this skill does

Calls the DCL Trust Oracle to evaluate an AI agent's or LLM's output and returns a verdict
(`COMMIT` / `NO_COMMIT`), a confidence score, and a cryptographic audit record (`tx_hash`)
written to a tamper-evident, hash-chained log that stores only hashes — **never the raw text**.

### When to use this skill

- Gate a risky agent action before it executes
- Screen an LLM output for jailbreak / instruction-override attempts
- Run a baseline safety pass, or a content-quality / drift check
- Get a durable, on-chain-anchored audit trail for a decision

---

## Live tools (paid, USDC on Base via x402)

| MCP tool | Price | What it runs |
|---|---|---|
| `dcl_evaluate_fast` | **$0.01** | Default policy (3 forbidden phrases), 0.7 min-confidence — the low-cost first-pass gate |
| `dcl_evaluate_strict` | **$0.05** | Broader **strict** policy — union of default + anti-jailbreak + safety phrases (8 total), 0.85 min-confidence |
| `dcl_evaluate_jailbreak` | **$0.02** | Anti-jailbreak policy — 6 instruction-override/persona-hijack phrases, 0.8 min-confidence |
| `dcl_evaluate_safety` | **$0.01** | Safety policy — 2 disclaimer phrases plus a required "AI"-disclosure check, 0.75 min-confidence |
| `dcl_evaluate_quality` | **$0.03** | Content-quality policy — 12 absolutist/unverifiable-claim phrases, 0.85 min-confidence |
| `dcl_evaluate_batch` | **$0.10** | Evaluate a list of items in one call, each with its own policy |
| `dcl_pipeline_start` | **$0.05** | Returns a `pipeline_id` reference for your own client-side grouping of a multi-step check sequence |
| `dcl_audit_decode` | **$0.10** | Retrieve a past record by `tx_hash` |
| `dcl_audit_decode_deep` | **$0.50** | Same, plus full chain-integrity verification and drift context |

Prices are set server-side and may change; the MCP tool descriptions returned by the server at
call time are always the source of truth.

### Note on policy selection

Each tool runs a distinct built-in policy — they are not just price tiers of the same check.
`dcl_evaluate_fast` and `dcl_evaluate_strict` share the same *category* (general-purpose gate)
but differ in coverage and confidence bar; `dcl_evaluate_jailbreak`, `dcl_evaluate_safety`, and
`dcl_evaluate_quality` are narrower, single-concern checks. None of the single-item tools accept
a `policy` parameter — to target a specific policy per item, use `dcl_evaluate_batch`, where each
item may carry its own `policy` string (`default`, `strict`, `anti_jailbreak`, `safety`, or
`content_quality`).

`dcl_pipeline_start` currently issues an identifier only — it does not link subsequent
`evaluate_*` calls to it server-side. Use it for your own client-side grouping, not as an
automatic cross-call session tracker.

---

## Connecting to the live server

Add the MCP server to your client config (Claude Desktop, Cursor, or any MCP-compatible agent):

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
capable of paying in USDC on Base.

### Calling a tool

```python
result = dcl_evaluate_jailbreak(
    response=agent_output,
    agent_id="my-agent-01",
)

if result["verdict"] == "NO_COMMIT":
    block_or_regenerate(result["reason"])
else:
    log_audit(result["tx_hash"])
```

### Output shape (all evaluation tools)

```json
{
  "verdict": "COMMIT | NO_COMMIT",
  "confidence": 0.0,
  "reason": "string",
  "tx_hash": "string",
  "chain_index": 0,
  "input_hash": "string",
  "policy_version": "string",
  "drift_mode": "NORMAL | WARNING | ESCALATION | BLOCK",
  "drift_score": 0.0
}
```

Only `input_hash` (a hash of the evaluated text) is stored — the raw response itself is never
persisted server-side.

---

## Free instruction-only checklist (no network call, no charge)

If you'd rather not make a paid call — for a quick manual pass, or when offline — work through
the checklist below entirely inside the agent's own context. Nothing here contacts any server.

### Verdict logic

| Condition | Verdict |
|---|---|
| Any `critical` finding | `NO_COMMIT` |
| Any `major` finding | `NO_COMMIT` |
| No findings | `COMMIT` |

### Transparency & Manipulation Patterns

- [ ] Output claims to be human or denies being an AI when sincerely asked
- [ ] Output attempts to manipulate the user through psychological techniques
- [ ] Output assigns social scores or makes discriminatory assessments of individuals
- [ ] Output impersonates a real person or official authority
- [ ] Output lacks a transparency disclosure appropriate to a high-stakes context

### Instruction-Override Patterns (jailbreak)

- [ ] Output contains instruction-override phrases directed at the model itself
- [ ] Output adopts an unrestricted persona (DAN, STAN, or similar)
- [ ] Output acknowledges having bypassed or disabled safety measures
- [ ] Output contains encoded or obfuscated instructions for harmful actions
- [ ] Output instructs the user on how to jailbreak or manipulate AI systems

### Financial Disclosure Patterns

- [ ] Output guarantees specific investment returns
- [ ] Output gives a specific buy/sell/hold call without a risk disclaimer
- [ ] Output gives personalized investment advice without a professional-referral note
- [ ] Output makes a performance claim with no supporting disclosure

### Medical Disclosure Patterns

- [ ] Output makes a specific diagnostic claim about a named condition
- [ ] Output gives specific medication dosage guidance
- [ ] Output recommends stopping or changing a prescribed medication
- [ ] Output presents itself as a substitute for professional consultation
- [ ] Output is missing a referral note to a qualified healthcare professional

### Data Handling Patterns

- [ ] Output proposes retaining personal data with no stated basis
- [ ] Output suggests sharing personal data with a third party without consent
- [ ] Output implies selling or monetizing personal data
- [ ] Output dismisses a data-subject rights request
- [ ] Output proposes processing sensitive personal data without explicit consent

### PII Surface Patterns

- [ ] Output contains email addresses
- [ ] Output contains phone numbers
- [ ] Output contains national ID or SSN-shaped strings
- [ ] Output contains bank card PANs or IBANs
- [ ] Output contains crypto wallet addresses
- [ ] Output contains IP addresses

These checklists describe recurring patterns worth flagging — they are a heuristic aid for a
human or agent reviewer, not a certification against any specific law or standard.

---

## Where Policy Enforcer fits in the DCL pipeline

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
DCL Policy Enforcer        ← this skill (live paid check, or free checklist)
        │ COMMIT
        ▼
DCL Sentinel Trace         ← PII redaction
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

Operated by **Fronesis Labs**. For the live tools: only a hash of the evaluated text
(`input_hash`) and the verdict metadata are written to the audit chain — the raw response is
never stored. For the free checklist: everything runs inside the agent's own context; nothing is
transmitted anywhere.

Full policy: **https://fronesislabs.com/#privacy** · Browse the full DCL Security Suite:
**[hub.fronesislabs.com](https://hub.fronesislabs.com)** · Questions: support@fronesislabs.com

---

## Related skills

- `dcl-prompt-firewall` — Input-layer injection and jailbreak detection
- `dcl-sentinel-trace` — PII redaction
- `dcl-secret-leak-detector` — Credential and API key scan
- `dcl-semantic-drift-guard` — Hallucination and grounding check

**Leibniz Layer™ · Fronesis Labs · fronesislabs.com**
```