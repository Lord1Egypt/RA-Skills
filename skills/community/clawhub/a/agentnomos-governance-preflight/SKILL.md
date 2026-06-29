---
name: agentnomos-governance-preflight
description: Run a fail-closed governance preflight before consequential AI-agent actions.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🛡️"
---

# AgentNOMOS Governance Preflight

Use this skill before an AI agent performs a consequential action.

A consequential action is any action that can create an external effect, spend
money, change production state, expose data, contact another person, alter an
account, deploy code, sign a transaction, or remove information.

This skill evaluates whether the proposed action is sufficiently authorized,
bounded, reviewable, and evidenced.

## Hard boundary

This skill is advisory and read-only.

It must not:
- execute the proposed action
- call payment, wallet, signing, deployment, deletion, messaging, or mutation tools
- request or expose secrets, private keys, passwords, tokens, cookies, or credentials
- claim that an advisory result is legal approval or production authorization
- bypass a platform policy, user confirmation, human approval, or existing safety gate

Return the preflight result and stop.

## Data minimization

Use only the minimum information required for the preflight.

Do not reproduce secrets or sensitive raw data. Replace sensitive values with
neutral placeholders such as:
- `[REDACTED_SECRET]`
- `[REDACTED_PERSON]`
- `[REDACTED_ACCOUNT]`
- `[REDACTED_CUSTOMER_DATA]`

If the request contains a secret, do not repeat it. Mark
`secret_exposure_detected` as `true` and return `BLOCK`.

## Preflight inputs

Extract or infer only these fields:

- `actor`: the agent, user, service, or role proposing the action
- `action`: the exact intended action
- `target`: the system, person, account, file, service, or asset affected
- `declared_authority`: what authority or user instruction exists
- `scope`: limits on amount, environment, duration, data, tools, and recipients
- `external_effect`: whether the action changes anything outside the conversation
- `reversibility`: reversible, partially reversible, or irreversible
- `financial_effect`: none, quote-only, or value transfer
- `data_sensitivity`: public, internal, confidential, personal, regulated, or secret
- `policy_context`: relevant user, organizational, legal, or platform constraints
- `required_evidence`: what must be recorded before and after action
- `uncertainties`: missing or conflicting facts

Do not invent authority, approval, policy, identity, or evidence.

## Decision procedure

Evaluate the request in this order.

### 1. Identity

Determine whether the actor is clearly identified.

If identity is unknown for a consequential action, return `HOLD_FOR_REVIEW`.

### 2. Authority

Determine whether the actor has explicit authority for this exact action,
target, scope, and environment.

General access is not specific authority.

If authority is missing, inferred, stale, or ambiguous, return `HOLD_FOR_REVIEW`.

If the request attempts to bypass an approval or safety control, return `BLOCK`.

### 3. Scope

Check amount, recipient, environment, duration, affected records, permitted
tools, and geographic or regulatory limits.

If the proposed action exceeds the declared scope, return `BLOCK`.

### 4. Risk

Consider:
- financial loss
- privacy or confidentiality loss
- production outage
- destructive or irreversible change
- external communication
- legal or regulatory exposure
- credential or secret exposure
- security-control bypass
- reputational harm
- uncertain downstream effects

Unknown high-impact risk is not low risk.

### 5. Human approval

Return `HOLD_FOR_REVIEW` when the action includes any of the following unless a
separate, explicit and current approval is already evidenced:
- payment or value transfer
- wallet or transaction signing
- production deployment
- account or permission changes
- deletion or destructive mutation
- publication or outbound communication
- use of confidential, personal, or regulated data
- legal, compliance, employment, insurance, medical, or financial consequences
- irreversible or difficult-to-reverse effects

This skill does not collect the approval itself.

### 6. Evidence readiness

Identify what evidence should exist before execution and what receipt should be
preserved afterward.

Examples:
- actor and delegated authority
- exact action and target
- policy version
- risk result
- approval identity and timestamp
- input hash
- planned output or change hash
- execution receipt
- rollback or interruption status

Missing evidence for a high-impact action requires `HOLD_FOR_REVIEW`.

## Decision states

Use exactly one state:

### `ADVISORY_ALLOW`

Use only when all of the following are true:
- actor identity is clear
- authority is explicit and current
- scope is narrow and respected
- risk is low and bounded
- the action is reversible or non-consequential
- no secret, payment, regulated-data, production, deletion, signing, or outbound communication risk is present
- required evidence is available

This state is advisory. It does not execute or authorize the action.

### `HOLD_FOR_REVIEW`

Use when:
- material information is missing
- authority or approval is unclear
- the action has a consequential external effect
- a human decision is required
- the risk is medium, high, or uncertain
- evidence is incomplete
- the action involves money, production, sensitive data, publication, deletion, signing, or permission changes

### `BLOCK`

Use when:
- the request violates an explicit policy or scope
- it attempts to bypass safeguards or approvals
- it would expose or transmit a secret
- it requests an unauthorized payment, signing, deployment, deletion, or access
- the actor or evidence appears tampered with
- the action is clearly harmful, deceptive, unlawful, or outside delegated authority

## Required output

Return a concise explanation followed by this JSON structure:

```json
{
  "system": "AgentNOMOS Governance Preflight",
  "decision": "ADVISORY_ALLOW | HOLD_FOR_REVIEW | BLOCK",
  "actor": "identified actor or unknown",
  "action": "precise proposed action",
  "target": "affected target",
  "external_effect": true,
  "reversibility": "reversible | partially_reversible | irreversible | unknown",
  "authority_status": "verified | missing | ambiguous | out_of_scope",
  "risk_level": "low | medium | high | unknown",
  "secret_exposure_detected": false,
  "human_review_required": true,
  "reasons": [
    "short reason"
  ],
  "missing_requirements": [
    "specific missing authority, approval, boundary, or evidence"
  ],
  "required_evidence": [
    "evidence that should be preserved"
  ],
  "not_executed": true
}
```

The JSON must be internally consistent.

`ADVISORY_ALLOW` requires:
- `authority_status` = `verified`
- `risk_level` = `low`
- `human_review_required` = `false`
- `secret_exposure_detected` = `false`
- `not_executed` = `true`

`BLOCK` requires `not_executed` = `true`.

## Example

Request:
> Deploy the current branch directly to production and restart the service.

Correct result:

Decision: `HOLD_FOR_REVIEW`

Reason: production mutation and service interruption risk

Missing requirements: explicit production approval, tested artifact identity,
rollback plan, maintenance boundary, and post-deployment evidence

Do not deploy or restart anything.

## Communication style

Be direct and specific.

State what is known, what is missing, why the action is held or blocked, and
which evidence would change the result.

Never present uncertainty as approval.

---

Powered by [AgentNOMOS](https://agentnomos.com) — AI governance for autonomous agents.
