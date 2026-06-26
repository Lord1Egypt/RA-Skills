# Quarantine Policy

## Purpose
Quarantine is a containment action for unsafe installed skills.

## When quarantine is allowed
- High or Critical findings exist
- The skill is already inside the active user skill tree
- Policy explicitly allows auto-quarantine

## When quarantine is not allowed
- The candidate has not yet been installed
- The path is outside the OpenClaw skill tree
- The scan report is unreadable or untrusted
- Only Medium/Low/Info findings exist

## Action
Move the skill directory to:
`~/.openclaw/skills-quarantine/<skillname>-<timestamp>`

## Preserve evidence
Keep the scan report in the workspace scan directory and do not delete it.

## If parsing fails
Leave the skill in place, mark the result as blocked or failed to verify, and ask for manual review.

## No silent cleanup
Do not delete the skill automatically. Do not mutate unrelated directories.
