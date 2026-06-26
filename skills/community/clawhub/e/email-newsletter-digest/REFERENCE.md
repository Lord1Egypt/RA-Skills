# Email Newsletter Digest Reference

This skill sends an email digest built from newsletter emails received within the last 1 day.

It is designed to be used through natural language. Users should be able to ask OpenClaw things like:
- "Please send me the newsletter digest email"
- "Email the newsletter digest to me and my friends"
- "Add this sender to the newsletter digest"
- "Schedule my newsletter digest every morning"

## Files

- `SKILL.md` — agent-facing instructions and trigger guidance
- `settings.json` — user-editable filters and recipients
- `scripts/newsletter-digest.py` — bundled runner used by the skill

## Settings Shape

```json
{
  "newsletter_labels_csv": "Newsletters, Finance",
  "newsletter_senders_csv": "daily@example.com, weekly@example.com",
  "digest_recipient_emails_csv": "reader@example.com, friend@example.com",
  "recipient_delivery_mode": "individual"
}
```

Rules:
- `newsletter_labels_csv` is a comma-separated list of Gmail labels
- `newsletter_senders_csv` is a comma-separated list of sender email addresses
- either labels or senders may be empty, but not both
- if both are populated, the search uses OR semantics across both groups
- `digest_recipient_emails_csv` accepts one or more comma-separated recipient email addresses
- `recipient_delivery_mode` controls how those recipients receive emails
- supported values are `individual` and `group`
- `individual` sends one email per recipient
- `group` sends one email with every recipient in the `To` field
- if omitted, `recipient_delivery_mode` defaults to `group`

## User Experience

OpenClaw should handle this skill through natural language, not by asking the user to run shell commands.

Expected behavior:
- If the user asks to send the digest, run it immediately.
- If the user asks to add or remove labels, senders, recipients, or recipient delivery mode, update `settings.json`.
- If the user asks to schedule it every morning or on another cadence, OpenClaw should use its normal scheduling mechanism.

## Scheduling Notes

This skill should be schedulable through OpenClaw in natural language.

When a user asks for a morning schedule:
- keep the digest scoped to the last 1 day
- preserve the configured labels, senders, and recipients
- use the platform's normal scheduler or cron integration behind the scenes

## Runtime Notes

The skill depends on:
- `gog` for Gmail search and send
- `summarize` for per-newsletter summarization
- a valid `OPENAI_API_KEY` for the configured summarization provider

The skill does not hardcode a personal Gmail account. If `GOG_ACCOUNT` is set in the environment, it will use that account. Otherwise it relies on gog's default configured account.

The skill intentionally defers summarization model choice to `summarize`. Users can control that through summarize's own normal environment or configuration.

## Output Behavior

- No matching newsletters: send nothing and report that none were found
- Successful run: send the digest using the configured `recipient_delivery_mode`
- Partial summarization failure: still send the digest, then send a warning email describing the failures
- Full summarization failure or runtime failure: send a failure email instead of a broken digest

## Matching Logic

The Gmail search always uses `newer_than:1d`.

Examples:
- labels only: `label:Newsletters newer_than:1d`
- senders only: `(from:daily@example.com OR from:weekly@example.com) newer_than:1d`
- both populated: `(label:Newsletters OR label:Finance OR from:daily@example.com OR from:weekly@example.com) newer_than:1d`

## Maintainer Notes

- The script includes a MIME-part fallback when thread output is incomplete.
- The digest uses deterministic overlap heuristics to create a "Mentioned in multiple newsletters" section.
- The runner supports both one-per-recipient delivery and one group email to all recipients.
