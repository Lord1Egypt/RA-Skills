# AANA Workflow Readiness Check Skill

Use this skill when an OpenClaw-style agent is about to begin a workflow, plan, multi-step task, tool sequence, external action, file operation, research task, customer action, code change, booking, purchase, or high-impact decision.

This is an instruction-only skill. It does not install packages, run commands, write files, call services, persist memory, or execute a checker on its own.

## Core Principle

Before starting a workflow, the agent should confirm it has enough information, permission, tools, evidence, and safe boundaries to proceed.

The agent should separate:

- workflows that are ready to start,
- workflows that need clarification,
- workflows that need explicit permission,
- workflows that need evidence or retrieval first,
- workflows that need a tool or credential the agent does not have,
- workflows that need human, professional, or admin review,
- workflows that should not start.

## When To Use

Use this skill before:

- starting a multi-step workflow,
- calling tools or connectors,
- changing files, code, settings, accounts, or production systems,
- sending, publishing, uploading, booking, buying, subscribing, renewing, refunding, or transferring,
- answering with material factual, legal, medical, financial, safety, policy, or customer impact,
- using private data, user records, logs, inboxes, calendars, drives, databases, repositories, or account information,
- continuing from an ambiguous or underspecified request.

## Readiness Categories

Classify the workflow:

- `ready`: enough information, permission, tools, and evidence are available.
- `needs_information`: required inputs or constraints are missing.
- `needs_permission`: approval or authorization is missing.
- `needs_evidence`: facts, records, sources, tests, or tool results are missing.
- `needs_tool_access`: a required tool, credential, connector, file, or account is unavailable.
- `needs_review`: human, professional, admin, or policy review is required.
- `not_safe`: the workflow should not start.

## AANA Readiness Loop

1. Identify the workflow and intended outcome.
2. Define the minimum completion criteria.
3. Check required information: inputs, constraints, dates, targets, identities, amounts, policies, and success criteria.
4. Check permission: user approval, ownership, authority, target scope, and external-action consent.
5. Check tools: required tools, access, credentials, permissions, and safer alternatives.
6. Check evidence: available facts, sources, records, test results, citations, and uncertainty.
7. Check risk: private data, financial impact, legal/medical/safety impact, irreversible actions, production impact, and public exposure.
8. Choose action: start, ask, retrieve, request approval, route to review, narrow, or refuse.

## Required Pre-Workflow Checks

Before starting, verify:

- user request,
- workflow summary,
- intended outcome,
- completion criteria,
- required information,
- permission status,
- tool/access status,
- evidence status,
- risk level,
- first safe step.

## Information Rules

Do not start a workflow when:

- the target is unclear,
- required dates, amounts, recipients, files, accounts, systems, or success criteria are missing,
- the user has not selected between materially different options,
- the workflow could affect another person or organization and identity/authority is unclear.

Ask a focused question instead of guessing.

## Permission Rules

Require explicit approval before starting when the workflow:

- changes files, accounts, code, settings, permissions, or production systems,
- sends, publishes, posts, uploads, books, buys, subscribes, renews, refunds, transfers, cancels, deletes, or overwrites,
- accesses private data beyond what the user clearly provided,
- affects money, legal rights, health, safety, employment, housing, education, insurance, reputation, or public records.

Approval should name the workflow, target scope, and first state-changing step.

## Tool Rules

Do not start a tool-dependent workflow when:

- the required tool is unavailable,
- the target scope cannot be limited,
- credentials or permissions are missing,
- the tool would expose unrelated private data,
- a safer read-only, preview, draft, or dry-run step is available and has not been used.

Prefer a narrow readiness step before a broad action.

## Evidence Rules

Do not start or complete an evidence-dependent workflow when:

- key facts are unsupported,
- sources are missing or stale,
- test claims are unrun,
- policy claims are unverified,
- customer/account facts are not available,
- legal, medical, financial, or safety conclusions lack qualified evidence.

Retrieve, ask, or route to review before acting.

## Review Payload

When using a configured AANA checker, send only a minimal redacted review payload:

- `user_request`
- `workflow_summary`
- `intended_outcome`
- `readiness_status`
- `information_status`
- `permission_status`
- `tool_status`
- `evidence_status`
- `risk_level`
- `recommended_action`

Do not include raw secrets, credentials, full private records, full logs, full transcripts, full account records, or unrelated private data when a redacted summary is enough.

## Decision Rule

- If information, permission, tools, evidence, and risk boundaries are sufficient, start with the first safe step.
- If required inputs are missing, ask.
- If facts or records are missing, retrieve with the narrowest safe scope.
- If authorization is missing, request explicit approval.
- If tools or credentials are unavailable, explain the blocker or choose a safer available path.
- If the workflow is high-impact, irreversible, professional, production, or policy-sensitive, route to review.
- If the workflow is unsafe, unauthorized, deceptive, or harmful, refuse unsafe parts.
- If a checker is unavailable or untrusted, use manual readiness review.

## Output Pattern

For readiness-sensitive work, prefer:

```text
AANA readiness check:
- Workflow: ...
- Intended outcome: ...
- Information: sufficient / missing / ambiguous / conflicting / unknown
- Permission: explicit / implicit_low_risk / required / denied / unclear
- Tools: available / unavailable / limited / unsafe_scope / not_needed
- Evidence: sufficient / partial / missing / stale / conflicting / unknown
- Risk: low / moderate / high / irreversible / private / production / professional / unknown
- Decision: start / ask / retrieve / request_approval / route_to_review / narrow / refuse
```

Do not include this check in the user-facing answer unless clarification, approval, retrieval, review, or a readiness blocker needs to be explained.
