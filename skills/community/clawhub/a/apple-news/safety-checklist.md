# Safety Checklist - Apple News (MacOS)

Apply this checklist before link opens and shortcut execution.

## Pre-Action Checks

1. Confirm exact intent (open app, open one link, open queue, or run shortcut).
2. Validate each target link format before launch.
3. Confirm whether links include sensitive context.
4. For shortcut execution, confirm shortcut name and expected side effects.
5. For multiple opens, show link count and collect explicit confirmation.
6. For more than one link, require second explicit confirmation.

## Post-Action Checks

1. Confirm app opened successfully.
2. Confirm target link or workflow executed as requested.
3. If mismatch occurs, stop and present corrected options.

## Bulk Action Guardrails

- Default to opening one link at a time.
- Require second confirmation before opening more than one link.
- Record high-impact confirmations in local safety notes.
