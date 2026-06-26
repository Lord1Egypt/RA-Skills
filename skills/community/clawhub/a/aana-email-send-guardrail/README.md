# AANA Email Send Guardrail Skill

This OpenClaw-style skill verifies recipient, tone, private data, attachments, claims, and send approval before email is sent.

## Marketplace Slug

Recommended slug:

```text
aana-email-send-guardrail
```

## Contents

- `SKILL.md`: agent-facing instructions.
- `manifest.json`: review metadata and boundaries.
- `schemas/email-send-guardrail.schema.json`: optional email-gate payload shape.
- `examples/redacted-email-send-guardrail.json`: safe example payload.

## What It Does

The skill asks the agent to:

1. Identify whether the action is draft, reply, forward, schedule, or send.
2. Verify exact recipients, CC, BCC, and external audience.
3. Check tone before high-impact or sensitive email is sent.
4. Redact private or unrelated data.
5. Verify attachments are correct, necessary, safe, and approved.
6. Check factual claims and promises against evidence.
7. Require explicit approval before the irreversible send action.

## What It Does Not Do

This package does not:

- install dependencies,
- execute code,
- call remote services,
- write files,
- persist memory,
- inspect systems by itself,
- send email by itself.

## Safety Model

Email sending is an irreversible external action. Drafting an email is not permission to send it.

The agent should request explicit approval naming the recipients, subject, attachments, and timing before sending or scheduling any sensitive, external, financial, legal, medical, HR, customer, account, or commitment-bearing email.
