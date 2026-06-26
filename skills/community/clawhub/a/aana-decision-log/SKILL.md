# AANA Decision Log Skill

Use this skill when an OpenClaw-style agent needs to produce a compact audit record for an important decision, guardrail gate, user-facing action, tool action, refusal, escalation, correction, or changed plan.

This is an instruction-only skill. It does not install packages, run commands, write files, call services, persist memory, or execute a checker on its own.

## Core Principle

Important agent decisions should leave a compact, truthful, privacy-minimized record of what was checked, what failed, what changed, and what risk remains.

The agent should separate:

- the decision being logged,
- checks actually performed,
- checks not performed,
- failures or risks found,
- changes made because of review,
- final action taken,
- evidence used,
- sensitive details that should be summarized or redacted.

## When To Use

Use this skill after or during:

- guardrail decisions that accept, revise, ask, defer, refuse, route, or escalate,
- medical, legal, financial, privacy, file, code, purchase, booking, support, or research-sensitive actions,
- destructive, irreversible, publishing, external-send, or high-impact tool actions,
- decisions where the agent changed its answer because a check failed,
- decisions where tests, evidence, policy, scope, authorization, or private-data checks matter,
- user requests for an audit trail, review note, handoff note, or compact decision summary.

## What To Log

Capture:

- `decision`: what the agent decided to do,
- `trigger`: why this was important enough to log,
- `checks_performed`: concrete checks that actually happened,
- `failed_checks`: checks that failed or raised uncertainty,
- `changes_made`: what changed because of the review,
- `evidence_basis`: short source of evidence, not raw sensitive data,
- `unverified_items`: facts, claims, tests, or assumptions not verified,
- `final_action`: accept, revise, ask, retrieve, defer, refuse, route, escalate, or no_action,
- `residual_risk`: what remains uncertain or risky,
- `privacy_handling`: how secrets/private data were avoided or redacted.

## What Not To Log

Do not include:

- API keys, bearer tokens, passwords, security codes, private keys,
- full payment numbers, bank account numbers, identity documents,
- raw medical, legal, customer, account, billing, or personal records,
- full private messages, full logs, full transcripts, or full directory dumps,
- unrelated file paths, unrelated diffs, unrelated customer data,
- speculation framed as fact,
- tests, checks, or reviews that did not actually happen.

## AANA Decision Log Loop

1. Identify the decision and its risk class.
2. List only checks actually performed.
3. Mark missing checks explicitly instead of implying they passed.
4. Record failures, uncertainty, or boundary triggers.
5. Record the correction: what was removed, revised, asked, deferred, refused, or escalated.
6. Minimize sensitive data: use labels, hashes, short summaries, or redacted references when possible.
7. Produce a compact record that a reviewer can scan quickly.

## Logging Rules

Be precise:

- "Checked refund claim against available ticket text; no account system was available."
- "Removed payment detail from reply."
- "Did not run full tests."
- "Deferred booking because cancellation terms were unclear."

Do not inflate evidence:

- A source summary is not a full policy review.
- A targeted test is not a full suite.
- A user statement is not verified account evidence.
- A redacted path list is not proof every file was inspected.

## Recommended Compact Format

Use this shape by default:

```text
Decision log:
- Decision: ...
- Trigger: ...
- Checked: ...
- Failed/unclear: ...
- Changed: ...
- Evidence: ...
- Not verified: ...
- Privacy: ...
- Final action: ...
- Residual risk: ...
```

Keep each bullet short. Prefer one sentence per field.

## JSON Record Shape

When a structured record is needed, use:

```json
{
  "decision": "revise",
  "trigger": "support reply included an unverified refund promise",
  "checks_performed": ["refund promise check", "private data check"],
  "failed_checks": ["refund approval not verified"],
  "changes_made": ["replaced refund promise with review language"],
  "evidence_basis": ["redacted ticket summary"],
  "unverified_items": ["refund eligibility"],
  "privacy_handling": "payment detail redacted",
  "final_action": "revise",
  "residual_risk": "account system still needs review"
}
```

## Decision Rule

- If the record would expose sensitive data, revise it into a redacted summary.
- If the agent did not perform a check, list it under `unverified_items` or omit it from `checks_performed`.
- If nothing meaningful changed and the action is low risk, keep the log minimal or do not produce one.
- If a decision affected safety, privacy, money, files, code, publication, medical boundaries, or user trust, produce a compact log.
- If a checker is unavailable or untrusted, produce a manual decision log from observed facts only.

## Output Boundary

Decision logs are audit artifacts, not user persuasion. Do not use them to hide uncertainty, justify unsupported claims, or imply compliance certification.
