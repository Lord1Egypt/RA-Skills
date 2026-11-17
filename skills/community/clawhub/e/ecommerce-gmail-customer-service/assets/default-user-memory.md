# User customer service memory

> This file saves the email writing preferences confirmed by the user, as well as the classification processing practices summarized from historical customer service responses and manual modifications to the Draft. It is not a source of fact for orders, policies, laws or Platform rules. Current evidence and mandatory rules always take precedence.

## Instructions for use

- One-time historical email import happens only during onboarding after the user explicitly agrees. It is independent of ongoing draft-edit learning.
- `learning.enabled` controls whether later owner-edited AI drafts are automatically compared and summarized into new memory.
- `memory.usage_enabled` controls whether this existing long-term memory may guide new drafts. It is enabled by default; turning it off does not delete the memory or change separately approved automatic-send categories.
- Only desensitized, generalizable summaries are saved, and original emails, attachments or customer personal information are not saved.
- View this file read-only with `python3 scripts/configure.py show user-memory`, or display its local path with `python3 scripts/configure.py path user-memory`. Do not manually edit individual classification playbooks; controlled onboarding, sent-Draft, or Draft-edit merges add or update memory.
- You can run `python3 scripts/configure.py set learning off --confirm-owner-request` to stop ongoing draft-edit learning without changing historical memory or its use setting.
- Long-term memory has no automatic expiry. The owner may clear all of it with `python3 scripts/user_memory.py clear --confirm-owner-request --confirm-delete-all`. This does not change any independent category automatic-reply permission.
- `status=approved` means a playbook may guide a reply; it never by itself permits automatic sending.
- Automatic-reply permissions are stored separately in `auto_reply_permissions.json`. A known sent AI Draft creates a short-lived confirmation event; only after the owner confirms that a category's handling logic is reusable does that category's independent switch turn on. Turning off one or all category switches never changes this memory file.

## Current status

- History learning: not started yet
- Historical range: past 30 days
- Tone plan: to be summarized and confirmed
- Classification solutions: 0 items
- Last updated: None

## Confirmed tone and diction

Not yet.

## Treatment plans organized according to three levels of classification

Not yet.

<!-- ECS_MEMORY_JSON_BEGIN -->
```json
{
  "schema_version": 5,
  "history_learning": {
    "status": "not_started",
    "window_days": 30,
    "approved_at": null,
    "last_scan_at": null,
    "source_threads": 0
  },
  "style_profile": {
    "status": "not_reviewed",
    "items": []
  },
  "handling_playbooks": [],
  "updated_at": null
}
```
<!-- ECS_MEMORY_JSON_END -->
