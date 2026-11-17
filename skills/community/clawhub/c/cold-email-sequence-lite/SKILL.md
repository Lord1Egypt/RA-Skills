---
name: cold-email-sequence-lite
description: Generate a minimal 2-touch cold outreach skeleton (opener + polite breakup) from an ICP + pain points input — subject-line options, skeleton copy, CTA, and spam-trigger/subject-length checks. Use when the user asks to write cold outreach or a simple drip email.
---

# Cold Email Sequence (Lite)

`scripts/sequence.mjs` turns a structured brief into a 2-touch skeleton (day 0 opener, day 7 breakup). You write the final copy — skeletons encode structure, not finished prose.

## Rules

- Cold outreach only to the user's own leads/prospects. No mass unsolicited spam — always include the graceful exit (touch 2 is a breakup).
- Keep subjects under ~60 chars and lowercase-casual.
- Personalization tokens `{{firstName}}`, `{{company}}` stay literal — the sending tool fills them.
- Every touch ends with ONE CTA.

## 1. Run

Requires Node 18+, zero dependencies. Fully offline.

```bash
node <skill-dir>/scripts/sequence.mjs brief.json
```

Brief: `{product, icp, painPoints[], cta, senderName, company}` — `product` and `icp` required. Exit `1` when required fields are missing or warnings exist.

## 2. Read the report

- `sequence[]`: per-touch `day`, `goal`, `subjectOptions[]`, `skeleton`.
- `checks[]`: pass/fail/warn on brief completeness.
- `warnings[]`: overlong subjects, spam words, missing personalization.

## 3. Write the final emails

1. Expand each skeleton to 3-5 sentences — plain text, no HTML.
2. Touch 1: pain + one-line relevance + question CTA. Touch 2: breakup with door open.
3. Resolve `{{painPoint}}` placeholders with the user before delivery.

## Lite vs full

The full `cold-email-sequence` builds the standard 4-touch cadence (days 0/3/7/14: opener → proof bump → reframe → breakup) with proof-point and tone handling.
