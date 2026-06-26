# AANA Private Data Guardrail Skill

Use this skill when an OpenClaw-style agent may draft, summarize, send, display, transform, or act on private account, billing, payment, health, legal, personal, or sensitive business data.

This is an instruction-only skill. It does not install packages, run commands, write files, call services, persist memory, or execute a checker on its own.

## Core Principle

Private data should be used only when it is necessary, authorized, minimized, and safe for the current user-visible task.

The agent should separate:

- data the user explicitly provided,
- data available from authorized tools,
- data that is private and should not be repeated,
- data that is missing and must be requested or verified,
- data that should be redacted, summarized, deferred, or refused.

## When To Use

Use this skill before:

- sending emails, chats, tickets, or support replies,
- summarizing account, billing, payment, legal, health, HR, student, customer, or personal records,
- sharing screenshots, logs, exports, attachments, or reports,
- making account, refund, eligibility, diagnosis, legal, financial, or policy claims,
- using private records to personalize an answer,
- copying data from one system or context into another,
- storing memories or notes about a person,
- publishing or forwarding anything containing private details.

## Private Data Classes

Treat these as sensitive:

- account identifiers, order IDs, customer IDs, addresses, phone numbers, emails,
- payment methods, card numbers, bank details, invoices, balances, subscriptions,
- health symptoms, diagnoses, medications, insurance details, appointments,
- legal facts, case details, contracts, immigration, disputes, compliance records,
- employment, payroll, performance, school, family, or relationship records,
- API keys, tokens, passwords, credentials, auth headers, recovery codes,
- private messages, attachments, images, transcripts, logs, or internal notes.

## AANA Privacy Loop

1. Identify the action: what the agent is about to reveal, send, summarize, store, or decide.
2. Classify the data: public, user-provided, authorized private, restricted, secret, or unrelated.
3. Check necessity: remove anything not required for the current user request.
4. Check authorization: verify that the user has asked for this use and the context permits it.
5. Minimize: replace raw values with redacted summaries when possible.
6. Verify claims: do not invent account facts, eligibility, balances, policy outcomes, diagnoses, or legal conclusions.
7. Choose action: accept, revise, ask, defer, refuse, or route to human review.

## Redaction Rules

Prefer:

- "payment method on file" instead of a card number,
- "order ID unavailable" instead of invented order IDs,
- "refund eligibility unknown" instead of a refund promise,
- "health detail redacted" instead of symptoms unless needed,
- "legal status requires review" instead of legal conclusions,
- "account identifier present" instead of copying the identifier.

Do not expose:

- API keys or bearer tokens,
- passwords or recovery codes,
- full payment numbers,
- private account records unrelated to the task,
- health, legal, or financial details not needed for the answer,
- private messages or attachments unrelated to the current request.

## Allowed Actions

- Accept: the content contains only necessary, authorized, minimized data.
- Revise: the answer is useful but includes unnecessary private data or unsupported account claims.
- Ask: required permission, identity, context, or missing facts must be clarified.
- Defer: the action needs a verified system, stronger tool, human review, or compliance boundary.
- Refuse: the request asks to expose secrets, unrelated private data, or unauthorized records.

## High-Risk Cases

Pause and ask for review before:

- sending private data to a third party,
- posting private data publicly,
- revealing another person's data,
- making refund, billing, health, legal, financial, employment, or eligibility decisions,
- storing memory about a person,
- using sensitive data outside the original purpose,
- combining private records from multiple contexts.

## Review Payload

When using a configured AANA checker, send only a minimal redacted review payload:

- `task_summary`
- `data_classes`
- `candidate_disclosure_summary`
- `authorization_status`
- `minimization_status`
- `unsupported_private_claims`
- `recommended_action`

Do not include raw secrets, tokens, full payment data, private messages, health records, legal records, or full account files when a redacted summary is enough.

## Decision Rule

- If private data is unnecessary, remove it.
- If authorization is unclear, ask.
- If facts are missing, ask or defer.
- If the content invents account, billing, payment, health, legal, or personal facts, revise.
- If the request seeks unauthorized disclosure, refuse and explain briefly.
- If the action is high-impact or irreversible, defer to human review or a verified system.
- If a checker is unavailable or untrusted, use manual privacy review.

## Output Pattern

For privacy-sensitive replies, prefer:

```text
Safe response:
- ...

Privacy handling:
- Used only necessary details.
- Redacted sensitive fields.
- Did not verify or invent missing private facts.

Next step:
- Ask / verify / defer if needed.
```

Do not include the privacy-handling note unless useful to the user or needed for review.
