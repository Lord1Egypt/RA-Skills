---
name: dcl-semantic-drift-guard
description: >
  Use this skill to detect semantic hallucinations and context drift in LLM outputs.
  Triggers when an agent or pipeline needs to verify that a generated response is
  faithfully grounded in a source document or knowledge base — and has not fabricated,
  contradicted, or materially distorted any claims. Use whenever you need to validate
  AI output against a contract, policy document, RAG-retrieved context, or any
  authoritative source of truth. Returns a tamper-evident DCL audit record with
  verdict IN_COMMIT or HALLUCINATION_DRIFT. Part of the Fronesis Labs / Leibniz Layer™
  verification suite alongside DCL Policy Enforcer and DCL Sentinel Trace.
---

# DCL Semantic Drift Guard

**Publisher:** @daririnch · Fronesis Labs  
**Version:** 1.0.0  
**Part of:** Leibniz Layer™ Verification Suite

---

## What this skill does

Semantic Drift Guard compares an LLM-generated response against a trusted source of truth and detects:

- **Hallucinated facts** — claims not present in the source
- **Logical contradictions** — statements that directly conflict with the source
- **Omission drift** — critical information from the source that was silently dropped
- **Fabricated specifics** — invented numbers, dates, names, clauses, or identifiers

It supports two source modes:
- **`context` mode** — inline document or contract passed directly in the request
- **`kb_query` mode** — knowledge base lookup via RAG endpoint

Every verification produces a cryptographic audit record compatible with the DCL Evaluator tamper-evident chain.

---

## Verdicts

| Verdict | Meaning |
|---|---|
| `IN_COMMIT` | Response is faithfully grounded in the source. No hallucinations detected. Safe to proceed. |
| `HALLUCINATION_DRIFT` | Response contains fabricated, contradicted, or unsupported claims. Do not commit. Review `drift_items`. |

---

## Input schema

```json
{
  "source_mode": "context" | "kb_query",

  // For source_mode = "context":
  "source_document": "<full text of the authoritative document>",

  // For source_mode = "kb_query":
  "kb_endpoint": "<RAG endpoint URL>",
  "kb_query": "<query string to retrieve relevant chunks>",

  // Always required:
  "llm_output": "<the LLM-generated response to verify>",
  "strictness": "strict" | "balanced" | "lenient",  // default: "balanced"
  "policy": "eu_ai_act" | "gdpr" | "fstek" | "internal" | "none"  // optional
}
```

### Strictness levels

- **`strict`** — any unverifiable claim triggers HALLUCINATION_DRIFT. Use for contracts, medical, legal, financial outputs.
- **`balanced`** — minor paraphrasing and reasonable inferences are tolerated. Use for customer support, summaries.
- **`lenient`** — only direct factual contradictions trigger HALLUCINATION_DRIFT. Use for creative or exploratory outputs.

---

## Output schema

```json
{
  "status": "success" | "error",
  "data": {
    "verdict": "IN_COMMIT" | "HALLUCINATION_DRIFT",
    "confidence": 0.0–1.0,
    "source_mode": "context" | "kb_query",
    "strictness": "strict" | "balanced" | "lenient",
    "policy": "eu_ai_act" | "none" | "...",
    "drift_items": [
      {
        "type": "hallucination" | "contradiction" | "omission" | "fabricated_specific",
        "claim": "<the problematic claim in the LLM output>",
        "source_reference": "<relevant excerpt from source, or null if absent>",
        "severity": "critical" | "major" | "minor"
      }
    ],
    "tx_hash": "<SHA-256 of input+output payload>",
    "timestamp": "ISO-8601",
    "audit_chain_id": "<Merkle leaf ID for DCL Evaluator chain>"
  }
}
```

`drift_items` is an empty array `[]` when verdict is `IN_COMMIT`.

---

## Verification workflow

When this skill is invoked, follow these steps:

### Step 1 — Retrieve source of truth

**If `source_mode = "context"`:**  
Use `source_document` directly. Chunk it into logical sections for comparison.

**If `source_mode = "kb_query"`:**  
Query the `kb_endpoint` with `kb_query`. Retrieve top-k relevant chunks. Treat the union of retrieved chunks as the authoritative source. If the endpoint is unreachable, return `status: "error"` with `reason: "kb_unavailable"`.

### Step 2 — Decompose LLM output into claims

Parse the `llm_output` into atomic, verifiable claims:
- Factual assertions ("The contract states X")
- Numerical values ("The penalty is €10,000")
- Named entities ("The responsible party is Company A")
- Temporal claims ("The deadline is March 15")
- Logical conclusions ("Therefore, clause 4.2 applies")

### Step 3 — Cross-reference each claim against source

For each claim, determine:

| Finding | Classification |
|---|---|
| Claim is explicitly supported by source | ✅ Grounded |
| Claim is a reasonable paraphrase (strictness: lenient/balanced) | ✅ Grounded |
| Claim introduces information absent from source | ⚠️ `hallucination` |
| Claim directly contradicts source | 🚨 `contradiction` |
| Critical source information was omitted from output | ⚠️ `omission` |
| Specific value (number, date, name) was invented | 🚨 `fabricated_specific` |

### Step 4 — Apply strictness filter

- `strict`: any ⚠️ or 🚨 → HALLUCINATION_DRIFT
- `balanced`: any 🚨, or multiple ⚠️ → HALLUCINATION_DRIFT
- `lenient`: only 🚨 contradiction or fabricated_specific → HALLUCINATION_DRIFT

### Step 5 — Compute audit record

Generate:
```
tx_hash = SHA-256(source_fingerprint + llm_output + verdict + timestamp)
audit_chain_id = Merkle leaf position in DCL Evaluator chain
```

Return the full output schema.

---

## Interpreting results

### IN_COMMIT — safe to proceed

```json
{
  "status": "success",
  "data": {
    "verdict": "IN_COMMIT",
    "confidence": 0.97,
    "drift_items": [],
    "tx_hash": "0xa3f1...c72e",
    "timestamp": "2026-04-09T14:22:00Z",
    "audit_chain_id": "dcl-leaf-0047"
  }
}
```

The LLM output is faithfully grounded in the source. Log `tx_hash` to your audit trail.

### HALLUCINATION_DRIFT — do not commit

```json
{
  "status": "success",
  "data": {
    "verdict": "HALLUCINATION_DRIFT",
    "confidence": 0.89,
    "drift_items": [
      {
        "type": "fabricated_specific",
        "claim": "The penalty for breach is €50,000.",
        "source_reference": "Section 8.3: The penalty shall not exceed €10,000.",
        "severity": "critical"
      },
      {
        "type": "hallucination",
        "claim": "The agreement includes a 90-day cooling-off period.",
        "source_reference": null,
        "severity": "major"
      }
    ],
    "tx_hash": "0xb8d2...4f91",
    "timestamp": "2026-04-09T14:22:00Z",
    "audit_chain_id": "dcl-leaf-0048"
  }
}
```

Block the output. Surface `drift_items` to the human reviewer or trigger a re-generation loop.

---

## Integration patterns

### With DCL Policy Enforcer (recommended pipeline)

Run Policy Enforcer first (jailbreak / compliance check), then Semantic Drift Guard (factual grounding):

```
LLM Output
    │
    ▼
DCL Policy Enforcer ──► REJECT? → Block immediately
    │ COMMIT
    ▼
DCL Semantic Drift Guard ──► HALLUCINATION_DRIFT? → Block / re-generate
    │ IN_COMMIT
    ▼
Safe to deliver
```

Both `tx_hash` values are logged to the same DCL Evaluator audit chain, giving end-to-end verifiability.

### With DCL Sentinel Trace (full Leibniz Layer™ stack)

```
Sentinel Trace → strip PII before source reaches LLM
Policy Enforcer → compliance check on output
Semantic Drift Guard → factual grounding check
```

### Standalone (quick RAG validation)

```python
result = dcl_semantic_drift_guard(
    source_mode="kb_query",
    kb_endpoint="https://kb.yourapp.com/query",
    kb_query="penalty clauses breach of contract",
    llm_output=agent_response,
    strictness="strict",
    policy="eu_ai_act"
)

if result["data"]["verdict"] == "HALLUCINATION_DRIFT":
    raise ValueError(f"Drift detected: {result['data']['drift_items']}")
```

---

## Use cases

| Domain | Source mode | Strictness | Why |
|---|---|---|---|
| Legal contract summarization | `context` | `strict` | Fabricated clauses = liability |
| RAG-based customer support | `kb_query` | `balanced` | Prevent wrong product info |
| Medical documentation | `context` | `strict` | Patient safety |
| Financial report generation | `context` | `strict` | Regulatory compliance |
| EU AI Act compliance auditing | `kb_query` | `strict` | FSTEK / AI Act article mapping |
| Internal knowledge assistant | `kb_query` | `lenient` | Lower stakes, exploratory |

---

## Compliance notes

- Audit records are compatible with **EU AI Act Article 12** (logging requirements for high-risk AI systems)
- `tx_hash` chain is admissible as tamper-evident evidence under **GDPR Article 5(2)** accountability principle
- All source documents processed in `context` mode are never stored — only their fingerprint is hashed
- Compatible with **FSTEK** audit trail requirements for AI systems in Russian regulated industries

---

## Privacy & Data Policy

This skill is operated by **Fronesis Labs** under a strict no-retention data policy.

**What is processed:** Only the text submitted for evaluation. No user identity, no API keys, no metadata beyond what is required to run the verification.

**Retention:** Evaluations are processed in-memory only. No text is written to disk, no logs are retained, no data is shared with third parties. The only persistent record is the cryptographic `tx_hash` and `chain_hash` — these contain no personal data.

**Source documents:** Content passed via `source_document` (context mode) is never stored or logged. Only a cryptographic fingerprint is included in the audit hash.

**Infrastructure:** Webhook hosted on a private VPS operated solely by Fronesis Labs. No cloud analytics, no third-party processors.

Full policy: **https://fronesislabs.com/#privacy** · Questions: support@fronesislabs.com

---

## Related skills

- `dcl-policy-enforcer` — Compliance and jailbreak detection (run before Drift Guard)
- `dcl-sentinel-trace` — PII redaction and identity exposure detection (run before source reaches LLM)

**Leibniz Layer™ · Fronesis Labs · fronesislabs.com**
