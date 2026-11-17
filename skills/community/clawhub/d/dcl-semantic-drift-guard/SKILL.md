---
name: dcl-semantic-drift-guard
description: >
  Use this skill to detect semantic hallucinations and context drift in LLM outputs.
  Triggers when an agent or pipeline needs to verify that a generated response is
  faithfully grounded in a source document that was already provided inline —
  and has not fabricated, contradicted, or materially distorted any claims.
  Default mode (source_document provided directly) runs entirely inside the
  agent's own context with no network calls. Two clearly-labeled optional modes
  exist that do transmit data externally: kb_query (queries a remote RAG
  endpoint you configure) and an optional paid heuristic pre-check via Fronesis
  Labs' live DCL Trust Oracle MCP server. Do not use either optional mode with
  confidential, regulated, or sensitive source material without explicit
  confirmation from the user. Returns a tamper-evident DCL audit record with
  verdict IN_COMMIT or HALLUCINATION_DRIFT. Part of the DCL Skills verification
  suite by Fronesis Labs alongside DCL Policy Enforcer and DCL Sentinel Trace.
---

# DCL Semantic Drift Guard — Leibniz Layer™

**Publisher:** @daririnch · Fronesis Labs
**Version:** 1.2.0
**Part of:** DCL Skills · Leibniz Layer™ Verification Suite

---

## ⚠️ Data flow — read this before using

This skill has **three distinct modes** with different network behavior. Know which one you're
invoking:

| Mode | Network calls? | What leaves the agent |
|---|---|---|
| `source_mode: "context"` (default) | **None** | Nothing. Everything runs inside the agent's own context. |
| `source_mode: "kb_query"` | **Yes** | Your `kb_query` string is sent to the `kb_endpoint` you configure. |
| Optional `dcl_evaluate_quality` pre-check | **Yes** | The `llm_output` text is sent to Fronesis Labs' MCP server over the network, and a hash of it is written to an on-chain audit trail. |

**Do not use `kb_query` mode or the optional pre-check with confidential, regulated, or
sensitive source material** unless the user has explicitly confirmed that's acceptable — these
are the only two paths in this skill where anything leaves the agent. When in doubt, use
`source_mode: "context"` with the document pasted directly; it is fully local.

---

## What this skill does

Semantic Drift Guard compares an LLM-generated response against a trusted source of truth and detects:

- **Hallucinated facts** — claims not present in the source
- **Logical contradictions** — statements that directly conflict with the source
- **Omission drift** — critical information from the source that was silently dropped
- **Fabricated specifics** — invented numbers, dates, names, clauses, or identifiers

It supports two source modes:
- **`context` mode (default, fully local)** — inline document or contract passed directly in the
  request. No network call is made in this mode.
- **`kb_query` mode (network call)** — knowledge base lookup via a RAG endpoint you configure.
  This sends your query text to that endpoint. See the data-flow warning above.

Every verification produces a cryptographic audit record computed locally — this record itself
is not submitted anywhere by default.

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
  "strictness": "strict" | "balanced" | "lenient"  // default: "balanced"
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
    "confidence": 0.0,
    "source_mode": "context" | "kb_query",
    "strictness": "strict" | "balanced" | "lenient",
    "drift_items": [
      {
        "type": "hallucination" | "contradiction" | "omission" | "fabricated_specific",
        "claim": "<the problematic claim in the LLM output>",
        "source_reference": "<relevant excerpt from source, or null if absent>",
        "severity": "critical" | "major" | "minor"
      }
    ],
    "tx_hash": "<SHA-256 of input+output payload>",
    "timestamp": "ISO-8601"
  }
}
```

`drift_items` is an empty array `[]` when verdict is `IN_COMMIT`.

---

## Verification workflow

When this skill is invoked, follow these steps:

### Step 1 — Retrieve source of truth

**If `source_mode = "context"`:**
Use `source_document` directly. Chunk it into logical sections for comparison. Fully local, no
network call.

**If `source_mode = "kb_query"`:**
⚠️ This sends `kb_query` to `kb_endpoint` over the network. Confirm with the user before using
this mode if the query or surrounding context could reveal anything confidential. Query the
`kb_endpoint` with `kb_query`. Retrieve top-k relevant chunks. Treat the union of retrieved
chunks as the authoritative source. If the endpoint is unreachable, return `status: "error"`
with `reason: "kb_unavailable"`.

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
    "timestamp": "2026-04-09T14:22:00Z"
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
    "timestamp": "2026-04-09T14:22:00Z"
  }
}
```

Block the output. Surface `drift_items` to the human reviewer or trigger a re-generation loop.

---

## Optional faster pre-check via live paid service

⚠️ **This sends data over the network.** Calling this tool transmits the `llm_output` text to
Fronesis Labs' MCP server and writes a hash of it plus verdict metadata to an on-chain audit
trail. Do not use this with confidential, regulated, or sensitive text unless the user has
confirmed that's acceptable. This is entirely optional — the free workflow above never leaves
the agent.

If you want a quick heuristic signal *before* running the full source-grounding workflow above
— or as a cheap secondary check for overconfidence and fabrication-prone language on its own,
without a source document — Fronesis Labs' live **DCL Trust Oracle** MCP server offers:

| MCP tool | Price | What it runs |
|---|---|---|
| `dcl_evaluate_quality` | **$0.03** | Flags overconfident/absolute-claim language patterns and produces an on-chain `tx_hash` |

This is a pattern-based heuristic on the output text alone — it does **not** take a source
document and does not perform the claim-by-claim grounding check this skill does. It's useful as
a fast first-pass filter or as an independent, cryptographically-anchored confirmation alongside
this skill's own `tx_hash`, not as a replacement for the full workflow above.

```json
{
  "mcpServers": {
    "dcl-trust-oracle": {
      "url": "https://mcp.fronesislabs.com/mcp"
    }
  }
}
```

No API key or account signup is required — only a wallet capable of paying in USDC on Base.
Prices are set server-side and may change; the MCP tool description returned by the server at
call time is the source of truth.

---

## Integration patterns

### With DCL Policy Enforcer (recommended pipeline)

Run Policy Enforcer first (jailbreak / policy check), then Semantic Drift Guard (factual grounding):

```
LLM Output
    │
    ▼
DCL Policy Enforcer ──► NO_COMMIT? → Block immediately
    │ COMMIT
    ▼
DCL Semantic Drift Guard ──► HALLUCINATION_DRIFT? → Block / re-generate
    │ IN_COMMIT
    ▼
Safe to deliver
```

### With DCL Sentinel Trace (full Leibniz Layer™ stack)

```
Sentinel Trace → strip PII before source reaches LLM
Policy Enforcer → policy check on output
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
| Financial report generation | `context` | `strict` | Accuracy of figures |
| Internal knowledge assistant | `kb_query` | `lenient` | Lower stakes, exploratory |

---

## Privacy & Data Policy

This skill is operated by **Fronesis Labs**. Data handling depends on which mode you use:

**`source_mode: "context"` (default):** Fully local. Only the text submitted for evaluation is
processed, entirely within the agent's own context window. Nothing is written to disk, no logs
are retained, no data is shared with third parties.

**`source_mode: "kb_query"`:** Your `kb_query` string, and the retrieved chunks, are handled by
whatever `kb_endpoint` you configure — that endpoint's own data policy applies, not this skill's.
Fronesis Labs has no visibility into that traffic.

**Optional live pre-check (`dcl_evaluate_quality`):** Only a hash of the evaluated text
(`input_hash`) and verdict metadata are written to Fronesis Labs' on-chain audit trail — the raw
text itself is not stored server-side. See the data-flow table at the top of this document.

Full policy: **https://fronesislabs.com/#privacy** · Questions: support@fronesislabs.com

---

## Related skills

- `dcl-policy-enforcer` — Policy and jailbreak detection (run before Drift Guard)
- `dcl-prompt-firewall` — Input-layer injection and jailbreak detection
- `dcl-sentinel-trace` — PII redaction and identity exposure detection (run before source reaches LLM)
- `dcl-skill-auditor` — Pre-install scanner for ClawHub skills

**Leibniz Layer™ · Fronesis Labs · fronesislabs.com**
