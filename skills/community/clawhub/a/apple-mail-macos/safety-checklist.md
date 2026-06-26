# Safety Checklist - Apple Mail (MacOS)

Apply this checklist before any write action.

## Pre-Write Checks

1. Confirm account and mailbox scope exactly.
2. Resolve target message using at least two identity fields.
3. Generate operation ID and show dry-run preview.
4. Validate recipients and detect reply-all expansion.
5. If subject or body mentions attachment, verify attachment presence.
6. Show impacted message count for move, archive, or delete actions.
7. Collect explicit confirmation in clear text.

## High-Risk Send Gates

1. Require second confirmation when external recipients are added.
2. Block send when recipient identity is ambiguous.
3. Block send when attachment intent is detected but files are missing.
4. Check for duplicate send risk using operation ID and recent sent history.

## High-Risk Delete and Bulk Gates

1. Force dry-run count and sample preview before execution.
2. Require second confirmation for any bulk delete or bulk archive.
3. Prefer archive over permanent delete unless user explicitly requests hard delete.
4. Capture rollback notes in local safety log.

## Post-Write Checks

1. Re-read target mailbox window.
2. Verify expected state change for each target item.
3. Report success only after read-back matches request.
4. If mismatch occurs, stop and propose rollback options.
