# Operation Patterns - Apple Mail (MacOS)

Use these patterns to keep behavior deterministic and auditable.

## Lookup Pattern

1. Normalize account, mailbox, and time window.
2. Query narrowly first, then expand only if needed.
3. If duplicate matches exist, disambiguate before any write.

## Draft Pattern

1. Build draft with explicit recipients, subject, and body summary.
2. Attach operation ID to local operation log context.
3. Present draft preview and request approval before send.

## Send Pattern

1. Validate recipients, attachment expectations, and reply mode.
2. Confirm final intent in clear text.
3. Execute send using active command path.
4. Verify message appears in Sent mailbox.

## Reply Pattern

1. Resolve exact source message by ID and date scope.
2. Confirm reply vs reply-all before writing.
3. Preserve thread integrity using message identifiers when available.
4. Verify resulting reply in Sent mailbox.

## Move and Archive Pattern

1. Resolve target messages with explicit source mailbox scope.
2. Run dry-run with impacted count.
3. Execute write after confirmation.
4. Verify messages are absent from source and present in destination.

## Delete Pattern

1. Resolve exact targets and show preview snapshot.
2. Require explicit confirmation.
3. Execute delete path.
4. Verify target absence and log operation outcome.

## Bulk Operation Pattern

1. Show count, filters, and sample rows.
2. Require second confirmation.
3. Execute once with operation ID tracking.
4. Verify result counts and stop on mismatch.
