---
name: email-newsletter-digest
description: Summarizes recent newsletter emails received in Gmail into a single newsletter digest. This skill identifies newsletter emails using configured labels or sender addresses. Use for requests like "send me the newsletter digest email", "email the newsletter digest to me and my friends", "schedule my newsletter digest every morning", or "update my newsletter digest recipients".
version: 1.0.1
metadata:
  openclaw:
    always: false
    emoji: "📰"
    primaryEnv: OPENAI_API_KEY
    requires:
      bins:
        - python3
        - gog
        - summarize
      env:
        - OPENAI_API_KEY
---

# Email Newsletter Digest

Use this skill to send a digest of newsletter emails received within the last 1 day.

Read `settings.json` at the start of every invocation. For settings structure and maintainer notes, see [REFERENCE.md](REFERENCE.md).

## When To Use

Use this skill when the user wants to:
- send a newsletter digest email
- send the newsletter digest to multiple people
- schedule the digest every morning or on another cadence
- update which labels count as newsletters
- update which senders count as newsletters
- update who receives the digest

## Settings

Read `settings.json` at the start of every invocation.

The settings file contains:
- `newsletter_labels_csv`
- `newsletter_senders_csv`
- `digest_recipient_emails_csv`
- `recipient_delivery_mode`

Rules:
- `newsletter_labels_csv` may be null or empty if `newsletter_senders_csv` is populated
- `newsletter_senders_csv` may be null or empty if `newsletter_labels_csv` is populated
- both cannot be null or empty at the same time
- if both are populated, the Gmail search must use OR semantics across both groups
- `digest_recipient_emails_csv` may contain one or more comma-separated email addresses
- `recipient_delivery_mode` controls how emails are sent to multiple recipients
- supported values:
  - `individual` to send one email per recipient
  - `group` to send one email with all recipients in `To`
- if `recipient_delivery_mode` is omitted, default to `group`

## Agent Workflow

1. Immediately send a short acknowledgement such as: "I'm preparing the email newsletter digest now."
2. Read `settings.json`.
3. Validate that at least one newsletter filter is populated and at least one recipient email is configured.
4. Run the bundled runner at `~/.openclaw/skills/email-newsletter-digest/scripts/newsletter-digest.py` in a single blocking command with a generous timeout so you can wait for its stdout result. Do not background it and do not rely on follow-up polling for this skill.
5. Summarize each matching newsletter, build the digest, and send it using the configured `recipient_delivery_mode`.
6. When the run finishes, send a short completion message naming the recipients and the newsletter count.

If the user asks to update labels, senders, recipients, or recipient delivery mode:
- edit `settings.json`
- preserve the comma-separated format
- remove duplicates and empty entries

If the user asks to schedule it:
- use OpenClaw's normal scheduling or cron mechanism
- do not ask the user to write shell commands
- if the user says "every morning" and does not specify a time, use a reasonable morning time in the system timezone

## Core Rules

- Use `gog gmail messages search` to fetch individual newsletter emails.
- Use `gog gmail thread get --full` first for body extraction.
- If the body looks like a placeholder, fall back to `gog gmail get --json` and extract the best MIME part.
- Use `summarize` to turn each newsletter into bullet points.
- Unless the user explicitly asks for a different summarizer model, let `summarize` use its own configured/default model.
- Deduplicate by Gmail message id so each newsletter is summarized once per run.
- Only include matching emails from the last 1 day.
- If no newsletters are found, report that plainly and do not send anything.
- If the run fails or all summaries fail, send a failure email to the configured recipients with the likely cause when possible.
- If only some newsletters fail to summarize, still send the digest and then send a warning email describing the failures.
- Keep user interaction natural-language-first. Do not tell the user to run Python or shell commands themselves.

## Query Construction

Construct the Gmail search from the settings file:

- labels only:
  - `label:Newsletters newer_than:1d`
- senders only:
  - `(from:a@example.com OR from:b@example.com) newer_than:1d`
- both populated:
  - `(label:Newsletters OR label:finance OR from:a@example.com OR from:b@example.com) newer_than:1d`

## Reporting Back

- Always acknowledge the request before starting work.
- For a successful run, report which recipients were sent the digest and how many newsletters were included.
- For settings changes, summarize exactly what changed.
- For scheduled runs, confirm the cadence in plain language.
- If `gog` or `summarize` fails, surface the error instead of hiding it.
- Never fail silently. If the digest cannot be sent, tell the user plainly what went wrong.
