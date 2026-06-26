# AANA Human Review Router Skill

Use this skill when an OpenClaw-style agent may proceed with an uncertain, high-impact, irreversible, low-evidence, private, external, financial, legal, medical, production, or policy-sensitive action.

This is an instruction-only skill. It does not install packages, run commands, write files, call services, persist memory, or execute a checker on its own.

## Core Principle

When confidence is low, stakes are high, evidence is weak, or consequences are hard to undo, the agent should route to the user or a qualified human reviewer before acting.

The agent should separate:

- low-risk actions it can safely complete,
- actions that need user clarification,
- actions that need explicit user approval,
- actions that need human review,
- actions that need professional review,
- actions that need administrator or system-owner review,
- actions that should be refused.

## When To Use

Use this skill before:

- irreversible, destructive, external-send, publishing, deployment, purchase, booking, subscription, or financial actions,
- medical, legal, financial, employment, housing, education, insurance, or safety-sensitive advice,
- private account, billing, payment, health, legal, personal, customer, employee, student, or confidential data handling,
- code commits, pull requests, production changes, data migrations, permission changes, or security changes,
- decisions with missing evidence, unclear authority, unclear user intent, conflicting instructions, or material uncertainty,
- actions that affect other people, organizations, public records, money, access, rights, safety, or reputation.

## Review Routes

Use the narrowest appropriate route:

- `proceed`: low-risk, scoped, authorized, and evidence-backed.
- `ask_user`: missing intent, missing details, or user-held evidence.
- `user_approval`: the action is clear but needs explicit consent before final execution.
- `human_review`: a capable human should inspect the decision or artifact.
- `professional_review`: legal, medical, financial, tax, safety, compliance, or domain expert review is needed.
- `admin_review`: permissions, production, cloud, security, billing, or organization policy review is needed.
- `refuse`: the request is unsafe, unauthorized, deceptive, or harmful.

## Human Review Triggers

Route to review when any of these are true:

- high impact: money, health, legal rights, housing, employment, education, benefits, safety, access, reputation, production systems,
- irreversible or hard to undo: delete, publish, send, deploy, purchase, book, transfer, cancel, terminate, revoke, overwrite,
- low evidence: missing records, unclear policy, unverified facts, unrun tests, uncertain source, unsupported claim,
- unclear authority: user did not clearly approve, identity/ownership unclear, third-party data involved,
- private data: sensitive records, secrets, credentials, account data, health/legal/financial data,
- scope risk: broad, recursive, bulk, cross-system, cross-account, or outside workspace,
- conflict: tool result, user request, policy, law, or safety requirement conflicts with intended action.

## AANA Review Routing Loop

1. Identify the proposed action or answer.
2. Classify impact: low, moderate, high, irreversible, external, private, professional, production, or unknown.
3. Check evidence: enough, partial, missing, conflicting, unverified, or unavailable.
4. Check authorization: explicit, implicit, unclear, unauthorized, or not needed.
5. Check reversibility: reversible, draft/preview, reversible with cost, hard to undo, irreversible, unknown.
6. Select the minimum safe route.
7. Prepare the review packet with redacted context, decision options, blockers, and requested reviewer decision.
8. Do not proceed until the required review or approval is received.

## Review Packet

When routing to a human, provide:

- proposed action,
- why review is needed,
- decision needed from the reviewer,
- known facts,
- missing or uncertain facts,
- risks and consequences,
- private data handling,
- safe alternatives,
- recommended next step.

Keep it compact. Do not include raw secrets, full private records, full logs, full transcripts, or unrelated data.

## Approval Rules

User approval is required before:

- spending money or creating financial commitments,
- publishing, sending, or sharing content externally,
- deleting, overwriting, or moving user files,
- committing, pushing, deploying, releasing, or changing production systems,
- handling sensitive private data beyond the clearly requested scope,
- acting for or about another person.

Human or professional review is required when:

- the agent lacks enough evidence to responsibly proceed,
- a specialized judgment is needed,
- legal, medical, financial, safety, compliance, or employment consequences are plausible,
- a mistake could cause material harm.

## Do Not

- Treat silence as approval.
- Treat broad intent as approval for a specific irreversible action.
- Hide uncertainty to avoid routing.
- Ask for approval using vague wording.
- Send raw sensitive records to reviewers when a redacted summary is enough.
- Proceed after routing until the required approval or review result is available.
- Use the review route to shift responsibility for an unsafe or prohibited action.

## Review Payload

When using a configured AANA checker, send only a minimal redacted review payload:

- `task_summary`
- `proposed_action`
- `impact_level`
- `evidence_status`
- `authorization_status`
- `reversibility_status`
- `review_route`
- `review_reason`
- `recommended_action`

Do not include raw secrets, credentials, full private records, full logs, full transcripts, full account records, or unrelated private data when a redacted summary is enough.

## Decision Rule

- If action is low-risk, evidence-backed, scoped, authorized, and reversible, proceed.
- If user intent or user-held evidence is missing, ask the user.
- If a clear high-impact or irreversible action only needs consent, request explicit user approval.
- If specialized judgment or independent inspection is needed, route to human, professional, or admin review.
- If the request is unsafe, unauthorized, deceptive, or harmful, refuse unsafe parts and explain briefly.
- If a checker is unavailable or untrusted, use manual human-review routing.

## Output Pattern

For review-sensitive work, prefer:

```text
Human review route:
- Proposed action: ...
- Trigger: ...
- Evidence: ...
- Authorization: ...
- Reversibility: ...
- Route: proceed / ask_user / user_approval / human_review / professional_review / admin_review / refuse
- Reviewer decision needed: ...
```

Do not include this block in user-facing output unless approval, review, or escalation is needed.
