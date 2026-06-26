# AANA Tool Use Gate Skill

Use this skill when an OpenClaw-style agent may call a tool, connector, API, browser action, shell, file operation, email/calendar action, repository action, database action, payment action, deployment action, or any capability that can read, write, send, publish, delete, modify, or affect external state.

This is an instruction-only skill. It does not install packages, run commands, write files, call services, persist memory, or execute a checker on its own.

## Core Principle

Tool calls should be necessary, scoped, authorized, data-minimized, and safe before use.

The agent should separate:

- actions that can be answered without tools,
- read-only tools,
- write or state-changing tools,
- external-send or publishing tools,
- destructive or irreversible tools,
- tools that expose private data,
- tools that require explicit approval,
- tools that should be refused or deferred.

## When To Use

Use this skill before:

- reading private files, inboxes, calendars, drives, tickets, databases, repositories, logs, accounts, or records,
- writing, editing, deleting, moving, publishing, sending, booking, buying, subscribing, renewing, deploying, committing, pushing, or opening pull requests,
- using browser automation, API connectors, local shell, local scripts, external services, cloud resources, or third-party apps,
- using tools that could reveal secrets, personal data, customer data, medical data, legal data, financial data, or private messages,
- expanding from a narrow user request into broad search, bulk action, or cross-system action.

## Tool Risk Classes

Treat these as higher risk:

- destructive actions: delete, overwrite, reset, drop, revoke, cancel, terminate,
- external actions: send, publish, post, upload, share, invite, email, message,
- financial actions: purchase, book, reserve, renew, subscribe, refund, transfer,
- code/repo actions: commit, push, merge, tag, release, deploy, change CI/CD,
- private-data actions: read mail, files, chats, calendars, account records, customer records, health, legal, financial, HR, student, or personal data,
- broad actions: recursive, bulk, wildcard, all records, all files, whole inbox, whole database,
- privileged actions: permissions, credentials, production systems, admin settings, cloud resources.

## AANA Tool Gate Loop

1. Identify the proposed tool and the exact operation.
2. Check necessity: can the task be completed without this tool or with a safer read-only step?
3. Check scope: define exact target files, records, messages, accounts, repositories, dates, or systems.
4. Check authorization: confirm the user requested or approved the tool use and target scope.
5. Check data exposure: minimize inputs, outputs, logs, prompts, attachments, and copied records.
6. Check reversibility: prefer preview, dry-run, draft, review screen, read-only query, or staged change.
7. Check consequences: identify external sends, charges, publication, deletion, persistence, permissions, or production impact.
8. Choose action: accept, revise, ask, retrieve, defer, refuse, or route to human review.

## Required Pre-Tool Checks

Before using a tool, verify:

- tool name or capability,
- intended operation,
- exact target scope,
- why the tool is necessary,
- whether the tool is read-only or state-changing,
- whether the user explicitly authorized the action,
- what private data may be read, sent, logged, or exposed,
- whether a safer alternative exists,
- whether the action is reversible,
- whether the action affects external systems or other people.

## Necessity Rules

Do not use a tool when:

- the answer can be given from already available evidence,
- the tool would collect private data not needed for the task,
- the user asked for a conceptual explanation only,
- the tool would expand scope beyond the user request,
- a lower-risk tool or read-only step is enough.

Prefer:

- read before write,
- preview before submit,
- draft before send,
- list before bulk action,
- diff before overwrite,
- narrow query before broad search,
- user confirmation before irreversible state change.

## Authorization Rules

Ask for explicit approval before:

- sending messages, emails, posts, invites, or external notifications,
- deleting, overwriting, moving, or bulk-editing files or records,
- committing, pushing, merging, releasing, deploying, or changing production state,
- buying, booking, subscribing, renewing, transferring, refunding, or charging money,
- reading private accounts, inboxes, health/legal/financial/customer records when not clearly needed,
- changing permissions, credentials, settings, policies, or access.

Approval should name the tool, operation, and target scope:

```text
Please confirm: use the calendar tool to create one event titled "Project review" on May 6 at 2 PM for the listed attendees.
```

## Data Minimization Rules

Do not pass unnecessary private data into tool inputs or logs.

Minimize:

- secrets, tokens, passwords, keys, cookies, auth headers,
- payment data, bank details, account IDs, tax IDs, government IDs,
- health, legal, financial, HR, student, customer, or personal records,
- full logs, full transcripts, full directory dumps, full inbox exports,
- unrelated files, messages, records, or attachments.

Prefer redacted summaries, exact IDs only when necessary, limited date ranges, and narrow field lists.

## Refusal And Deferral Rules

Refuse or defer tool use when:

- the user did not authorize a risky action,
- the target scope is ambiguous,
- the tool could harm unrelated files, accounts, systems, or people,
- the action would bypass consent, policy, review, or safety boundaries,
- the request involves credential theft, fraud, evasion, harassment, exfiltration, or unauthorized access,
- a qualified professional, administrator, or verified system must review the action first.

## Review Payload

When using a configured AANA checker, send only a minimal redacted review payload:

- `task_summary`
- `tool_name`
- `operation_summary`
- `target_scope`
- `necessity_status`
- `authorization_status`
- `data_exposure_status`
- `reversibility_status`
- `risk_classes`
- `recommended_action`

Do not include raw secrets, credentials, full private records, full logs, full transcripts, full directory dumps, or unrelated private data when a redacted summary is enough.

## Decision Rule

- If the tool is necessary, narrow, authorized, data-minimized, and reversible or low-risk, accept.
- If the tool is useful but too broad, revise to a narrower read-only or preview step.
- If authorization, target scope, or data exposure is unclear, ask.
- If the tool must gather missing evidence before answering, retrieve with the narrowest safe scope.
- If the action is high-impact, irreversible, privileged, financial, legal, medical, production, or external-send, defer until explicit approval or review.
- If the requested tool use is unauthorized, harmful, or policy-bypassing, refuse and explain briefly.
- If a checker is unavailable or untrusted, use manual tool-use review.

## Output Pattern

For tool-sensitive work, prefer:

```text
Tool gate:
- Tool: ...
- Operation: ...
- Target scope: ...
- Necessity: ...
- Authorization: ...
- Data exposure: ...
- Reversibility: ...
- Decision: accept / revise / ask / retrieve / defer / refuse
```

Do not include this gate in the user-facing answer unless the workflow requires it or approval is needed.
