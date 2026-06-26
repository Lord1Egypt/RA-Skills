# AANA Message Send Guardrail Skill

Use this skill before an OpenClaw-style agent sends, posts, replies, forwards, or schedules a Slack, Teams, Discord, SMS, DM, or public channel message.

This is an instruction-only skill. It does not install packages, run commands, write files, call services, persist memory, or send messages on its own.

## Core Principle

Message sending is an external action. Verify channel, recipients, tone, private data, attachments, claims, and explicit send approval before posting.

## Required Checks

- destination: DM, group DM, private channel, public channel, SMS, or external workspace
- recipients, mentions, broadcast tags, and channel visibility
- tone, urgency, and conflict risk
- private data, secrets, customer data, internal links, and hidden thread context
- attachments, screenshots, links, files, and quoted content
- factual claims, commitments, deadlines, or policy statements
- explicit approval for sending or posting

## Message Risk Classes

Treat these as higher risk:

- public channels, external workspaces, SMS, group DMs, broadcast tags, and large channels,
- `@channel`, `@here`, role mentions, customer channels, executive channels, and incident channels,
- screenshots, logs, file attachments, account details, customer details, or private thread context,
- promises about refunds, deadlines, policy exceptions, security, incidents, legal/medical/financial matters, or roadmap commitments,
- tense, emotional, disciplinary, urgent, or conflict-prone messages.

## Destination Rules

Do not send when:

- the destination is inferred, ambiguous, or broader than the user requested,
- a public channel or broadcast mention would expose private content,
- a thread reply includes hidden context that new recipients should not see,
- the message is intended for one person but would notify a group.

Ask for confirmation when the destination or audience is not exact.

## Tone And Claim Rules

Revise before sending if tone is hostile, manipulative, too casual for a high-impact context, or overconfident about uncertain facts.

Do not send unsupported promises, policy claims, customer facts, incident updates, deadlines, or commitments. Retrieve evidence, revise, or route to review first.

## Review Payload

When using a configured AANA checker, send only a minimal redacted review payload:

- `destination_status`
- `audience_status`
- `tone_status`
- `privacy_status`
- `approval_status`
- `message_risks`
- `blocker_reason`
- `safe_alternative`
- `recommended_action`

Do not include raw private messages, screenshots, logs, secrets, customer records, or unrelated thread history when a redacted summary is enough.

## Decision Rule

- If this is a draft only, draft and stop.
- If channel, recipients, or approval are unclear, ask.
- If private data or unsupported claims appear, redact or revise.
- If sending is external, public, high-impact, or irreversible, require approval.
- If the send is unsafe, unauthorized, deceptive, or privacy-violating, block.

## Output Pattern

```text
AANA message gate:
- Destination: dm / group / private_channel / public_channel / sms / external
- Audience: exact / ambiguous / broad / public
- Tone: ready / revise / conflict_risk
- Privacy: clear / needs_redaction / sensitive / unknown
- Approval: approved / required / unclear / denied
- Decision: draft / revise / ask / redact / request_approval / send / block
```
