---
name: avito-outreach-manager
description: Review Avito message drafts for clarity, consent, respectful tone, one clear next step, and safe checkout wording before a human decides what to send.
---

# Avito Message QA Reviewer

Use this skill to review Avito message drafts before a human decides what to
send. Keep the work to copy QA, safety wording, and a short human-send
checklist.

## Inputs

Collect:

- item or service context,
- seller-facing draft message,
- intended package or offer,
- allowed contact method,
- checkout boundary.

Do not request phone numbers, bank card numbers, payment account details,
session cookies, private chat exports, or personal identifiers that are not
needed for message review.

## Review Workflow

1. Check the message for:
   - respectful tone,
   - specific context,
   - one clear next step,
   - no pressure tactics,
   - no private payment details,
   - no workflow notes or scoring language.
2. Rewrite the message if needed.
3. Add a short human-send checklist.

## Output

Return:

- revised Avito message,
- what changed,
- human-send checklist,
- payment-safety reminder.

## Guardrails

- Keep all Avito account activity outside this skill.
- Keep checkout wording inside Avito-supported safe flows.
- Keep outbound text limited to what the recipient should see.
- Do not advise off-platform payments.
