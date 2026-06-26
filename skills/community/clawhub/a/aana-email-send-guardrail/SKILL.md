# AANA Email Send Guardrail Skill

Use this skill when an OpenClaw-style agent may draft, revise, forward, reply to, schedule, or send an email or email-like message.

This is an instruction-only skill. It does not install packages, run commands, write files, call services, persist memory, or run a checker on its own.

## Core Principle

Before email is sent, the agent should verify the recipient, purpose, tone, private data, attachments, claims, and explicit permission for the irreversible send action.

The agent should separate:

- drafting an email,
- revising an email,
- asking for missing details,
- preparing an email for user review,
- scheduling or sending an email with explicit approval,
- blocking unsafe or unauthorized email.

## When To Use

Use this skill before:

- sending, scheduling, forwarding, replying to, or CC/BCCing email,
- attaching files, images, PDFs, logs, reports, account records, screenshots, or exports,
- including customer, employee, student, patient, legal, financial, account, billing, payment, or personal data,
- promising refunds, credits, deadlines, prices, policy exceptions, legal outcomes, medical guidance, job decisions, or commitments,
- emailing external recipients, groups, mailing lists, executives, customers, partners, vendors, regulators, or public addresses.

## Email Status

Classify the email action:

- `draft_only`: prepare content but do not send.
- `needs_recipient`: recipient, CC, BCC, or audience is unclear.
- `needs_tone_revision`: tone, wording, or emotional framing needs work.
- `needs_redaction`: private or sensitive content must be removed.
- `needs_attachment_review`: attachments need verification, redaction, or permission.
- `needs_claim_evidence`: claims, promises, or policy statements need evidence.
- `needs_approval`: the send action or scope needs explicit approval.
- `ready_to_send`: recipient, content, attachments, claims, and approval are ready.
- `block_send`: unsafe, unauthorized, deceptive, privacy-violating, or materially unsupported.

## AANA Email Gate Loop

1. Identify the email action: draft, revise, reply, forward, schedule, or send.
2. Identify recipients: To, CC, BCC, groups, aliases, domains, and external/internal status.
3. Check authorization: did the user explicitly approve sending to these recipients?
4. Check purpose and scope: is the message limited to the user's requested outcome?
5. Check tone: professional, clear, appropriate, not manipulative, threatening, misleading, or overconfident.
6. Check private data: secrets, account data, billing/payment data, health/legal/financial data, personal data, and unrelated details.
7. Check attachments: correct files, safe filenames, redaction, permissions, and target recipients.
8. Check claims: facts, promises, commitments, citations, policies, deadlines, prices, and uncertainty.
9. Choose action: draft, revise, ask, redact, review attachments, retrieve evidence, request approval, send, or block.

## Required Pre-Send Checks

Before sending, verify:

- email action,
- exact recipients,
- subject and purpose,
- approval status,
- tone status,
- private data status,
- attachment status,
- claim evidence status,
- external impact,
- recommended action.

## Recipient Rules

Do not send when:

- the recipient is missing, ambiguous, mistyped, or inferred,
- CC/BCC would expose recipients or private context unexpectedly,
- a group/list alias could send to a broader audience than intended,
- internal information is going to an external recipient without clear approval,
- the email replies to or forwards a thread with unrelated private history.

Ask for confirmation when the recipient list or audience is not exact.

## Privacy Rules

Do not send:

- secrets, credentials, keys, tokens, cookies, auth headers, or security codes,
- full payment numbers, bank details, tax IDs, government IDs, or account recovery data,
- raw medical, legal, financial, HR, student, customer, or support records,
- unrelated private messages, full logs, full transcripts, hidden thread history, or internal notes,
- private details about another person unless necessary and authorized.

Prefer redacted summaries, minimal necessary facts, and removing old thread content when forwarding.

## Attachment Rules

Before attaching or forwarding files, verify:

- filename,
- file type,
- intended recipient,
- whether the file is the current version,
- whether it contains private data,
- whether it is needed,
- whether sharing is authorized.

Do not send attachments when the file is ambiguous, stale, private beyond scope, or not explicitly approved.

## Claim And Promise Rules

Do not send unsupported claims or promises about:

- refunds, credits, discounts, purchases, renewals, cancellations, bookings, or billing,
- legal, medical, tax, financial, employment, housing, education, insurance, or compliance outcomes,
- deadlines, availability, roadmap, product behavior, security, privacy, reliability, or policies,
- test results, research results, benchmarks, citations, or customer facts.

If evidence is missing, revise the email, retrieve evidence, or route to review before sending.

## Tone Rules

Revise before sending when tone is:

- hostile, sarcastic, shaming, threatening, or manipulative,
- too casual for a high-impact message,
- overconfident about uncertain facts,
- evasive about limitations,
- likely to escalate conflict unnecessarily.

Prefer concise, respectful, specific, and accountable wording.

## Send Approval Rules

Drafting is not sending approval.

Require explicit user approval before:

- sending or scheduling an email,
- forwarding a thread,
- adding recipients,
- attaching files,
- making commitments,
- sending sensitive, external, financial, legal, medical, HR, customer, or account-related email.

Approval should name the recipients, subject, attachments, and send timing.

## Review Payload

When using a configured AANA checker, send only a minimal redacted review payload:

- `email_action`
- `recipient_summary`
- `subject_summary`
- `approval_status`
- `tone_status`
- `privacy_status`
- `attachment_status`
- `claim_evidence_status`
- `send_risk_level`
- `recommended_action`

Do not include raw secrets, credentials, full private records, full logs, full transcripts, full email threads, full account records, or unrelated private data when a redacted summary is enough.

## Decision Rule

- If the email is only a draft, produce the draft and do not send.
- If recipients, purpose, or approval are unclear, ask.
- If tone needs work, revise.
- If private data appears, redact.
- If attachments are present, verify and request approval.
- If claims or promises are unsupported, retrieve evidence, revise, or route to review.
- If all checks pass and the user explicitly approved sending, send or schedule.
- If sending would be unsafe, unauthorized, deceptive, privacy-violating, or harmful, block send.
- If a checker is unavailable or untrusted, use manual email review.

## Output Pattern

For email-sensitive work, prefer:

```text
AANA email gate:
- Action: draft_only / revise / reply / forward / schedule / send
- Recipients: exact / missing / ambiguous / external / group_alias
- Approval: approved / required / unclear / denied
- Tone: ready / revise / high_impact / conflict_risk
- Privacy: clear / needs_redaction / sensitive / unknown
- Attachments: none / verified / needs_review / ambiguous / blocked
- Claims: supported / partial / missing / risky / not_applicable
- Decision: draft / revise / ask / redact / review_attachments / retrieve / request_approval / send / block
```

Do not include this gate in the user-facing answer unless review, approval, revision, or a send blocker needs to be explained.
