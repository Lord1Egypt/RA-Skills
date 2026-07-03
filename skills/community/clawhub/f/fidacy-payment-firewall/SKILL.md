---
name: fidacy-payment-firewall
description: Use BEFORE any payment or money-moving tool call. Gates the action against a signed mandate and returns a signed, verifiable verdict, so a prompt-injected or hallucinated payment (wrong/lookalike payee, over cap, duplicate invoice) is blocked before money moves. Non-custodial.
version: 1.0.2
license: Apache-2.0
---

# Fidacy — the payment firewall for agents

![An invoice is paid with a signed grant; the same invoice re-presented at a higher amount is denied as duplicate_invoice](https://raw.githubusercontent.com/lucaslubi/fidacy-mcp/main/assets/fidacy-skill-demo.svg)

An agent can be prompt-injected or hallucinate into a payment: wrong payee, an
inflated amount, or the same invoice paid twice. Your own log is not evidence.
Fidacy puts a **signed, independently-verifiable verdict on every money-moving
action** and blocks the bad one *before* it settles. It moves no money.

## When to use this skill

Invoke it the moment you are about to run a tool that **moves money or authorizes
a payment** (`pay`, `transfer`, `send_payment`, checkout, invoice settlement, a
Hermes/Lightning send, an AP2 mandate). Also use it to put a signed trust verdict
on any high-stakes action you want to be able to *prove* later.

## How to use it

This skill drives the **`@fidacy/mcp`** plugin's tools. Wire it into your
pre-action / tool-execution hook:

1. **Before paying — call `request_payment`** with `{ payee, amount, currency,
   purpose, category, idempotencyKey, invoiceRef? }`.
   - **ALLOW** → you get a short-lived **signed grant**. Only then run the real
     payment tool, passing that grant to the executor.
   - **DENY** → **do not pay.** The response names the violated rule
     (`payee_not_in_allowlist`, `per_tx_cap_exceeded`, `duplicate_invoice`…). Stop
     and report it.
   - Always set `invoiceRef` when you have one: Fidacy enforces **one payment per
     invoice**, so a re-presented invoice (even at a different amount, or with
     case/spacing tweaks) is blocked — the core BEC defense.

2. **To see the guardrails — call `verify_mandate`**: returns the active mandate
   (caps, allowed payees/categories, window) and Fidacy's public key.

3. **To prove what was blocked/allowed — call `get_audit_proof`** with the
   `decisionId`: returns the tamper-evident, hash-chained proof.

4. **For a signed verdict on any action — call `assess_action`**: returns a
   `riskPayloadJws` that **anyone** can re-verify against the public JWKS at
   `https://api.fidacy.com/.well-known/jwks.json`. Attach it to the action's
   audit trail; you don't have to trust Fidacy — you verify the signature.

## Rules

- **Never move money on a DENY.** No grant = the action is dead on arrival.
- **Never pay without first getting an ALLOW grant** and handing it to the executor.
- Treat the signed verdict as the record of what was authorized — it is
  non-repudiable and verifiable by a third party (auditor, insurer, counterparty).

## Setup (one line, free, local-first)

**On OpenClaw, prefer the native plugin** — same 5 tools, in-process, no MCP
subprocess:

```
openclaw plugins install @fidacy/openclaw-plugin
```

On any other MCP host (Claude Code, Claude Desktop, Hermes…), install the MCP
server — it runs locally, offline, deny-by-default, no account:

```json
{
  "mcpServers": {
    "fidacy": { "command": "npx", "args": ["-y", "@fidacy/mcp"] }
  }
}
```

Add trusted payees + caps in `~/.fidacy/config.json` (or set a full mandate via
`FIDACY_MANDATE_JSON`). Set `FIDACY_ENGINE_API_KEY` to enable `assess_action`
verdicts. Upgrade to the hosted core with `FIDACY_MODE=http`.

Pairs with the **fidacy-fraud-detector** skill: this firewall guards the payments
YOUR agent makes; the fraud detector catches the forged "this was approved" claims
OTHER agents hand you.
