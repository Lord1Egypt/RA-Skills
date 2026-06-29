---
name: content-review-mode-identifier
description: Triage a workspace content item.
version: 1.0.0
metadata:
  openclaw:
    skillKey: content-review-mode-identifier
---

# Content Intake Triage

Use this skill for routine content operations work when the user
asks to triage a workspace content item.

This is a standalone identifier skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Input

Field: `content_note`

Workspace content note, planning draft, or internal checklist to triage.

## Output

Field: `review_mode`

Return a concise review mode for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
low sensitivity
```

## Validation Prompt

```text
Triage this workspace note for the content-operations review flow: "Draft checklist for an internal planning demo."
```
