# Import, Export, and Backup

Moving mail in or out. Long-running, partially-failing, and impossible to verify by feel — every step here exists to make the counts checkable.

**Before starting**, read `## Mailbox Map`, `## Account Map` and any prior migration plan in `artifacts/` (`~/Clawic/data/fastmail-api/memory.md`, or the files `## Boxes` names). **Write the plan to `artifacts/<name>.md` before the first batch**, and append each batch to `operations/<year>.md` as it completes — a migration interrupted at 60% with no record is restarted from zero, and restarting an import from zero duplicates everything already moved (`memory-template.md`).

**Contents:** [Plan First](#plan-first) · [Exporting Messages](#exporting-messages) · [Importing Messages](#importing-messages) · [Copying Between Accounts](#copying-between-accounts) · [Resumability](#resumability) · [Verification](#verification) · [What Does Not Survive](#what-does-not-survive) · [Backup Versus Archive](#backup-versus-archive)

## Plan First

Write these down before any bytes move; they are the artifact:

1. **Scope**: which mailboxes, which date range, how many messages, how many bytes. `Mailbox/get` gives `totalEmails` per mailbox for free (`search.md`).
2. **Destination mapping**: source mailbox → destination mailbox id, resolved by role where a role exists, decided explicitly where it does not.
3. **Order**: mailbox structure first, then messages, then keywords. Importing into a mailbox that does not exist yet fails per message.
4. **Batch size and expected batch count**: `min(max_batch_size, maxObjectsInSet)`, and the byte budget against `maxSizeRequest` (`requests.md`).
5. **Quota headroom**: destination account free space versus total bytes. `overQuota` mid-import leaves a half-migrated mailbox and is the single most common way this goes wrong.
6. **Verification method and the number it must produce** — decided now, not after.
7. **What happens to the source**: kept, marked, or deleted. Deleting the source is a separate, later, confirmed operation, never part of the migration run.

## Exporting Messages

Raw messages come out as blobs through the session's `downloadUrl` template (`{accountId}`, `{blobId}`, `{type}`, `{name}`).

- `Email/get` with `properties: ["blobId", "id", "subject", "receivedAt", "mailboxIds", "keywords"]` gives the download handle plus the metadata that would otherwise be lost.
- The blob is the full RFC 5322 message, headers included. That is the portable unit — anything reconstructed from parsed fields is a different message.
- **Metadata does not travel inside the blob.** Mailbox membership and keywords are JMAP-side; export them alongside as a manifest, or the import lands everything flat and unread.
- Rate the downloads; a tight loop over thousands of blobs hits `maxConcurrentRequests` and the connection limits before it hits anything else.
- Where the exported files go is the user's decision and they leave the Clawic data area entirely. Never write mailbox contents under `~/Clawic/data/` (`memory-template.md`).

## Importing Messages

Two steps per message: upload the raw bytes as a blob, then `Email/import`.

```json
["Email/import", {"accountId": "u1a2b3c4", "emails": {
  "i1": {"blobId": "<uploaded>", "mailboxIds": {"<destination>": true},
         "keywords": {"$seen": true}, "receivedAt": "2024-03-11T09:14:00Z"}
}}, "c0"]
```

- **`receivedAt` is settable on import and nowhere else.** Omit it and every imported message is dated today, which destroys chronological order permanently and cannot be fixed afterwards.
- `mailboxIds` and `keywords` are set at import time. Setting them in a second pass doubles the work and leaves a window where everything is unread in the wrong place.
- Per-message failures come back in `notCreated` with a `SetError` each — `alreadyExists` (with the existing id), `invalidEmail` for an unparseable blob, `overQuota`, `tooLarge`. Collect them; do not stop the run for `alreadyExists`.
- **`alreadyExists` is the resume signal, not an error.** It means that message is already there, which is exactly what a re-run of an interrupted import should produce.

## Copying Between Accounts

`Email/copy` moves messages between accounts of the same token without a download round trip:

- Takes `fromAccountId`, `accountId` (destination), a `create` map with source ids and destination `mailboxIds`/`keywords`, and optionally `onSuccessDestroyOriginal`.
- The copy is a **new message with a new id** in the destination. Nothing links it back to the original afterwards; the manifest is the only record of the pairing.
- `onSuccessDestroyOriginal` is a destroy, with everything that implies (SKILL.md Rule 6). Default to leaving the original and deleting later, deliberately, once verification has passed.
- Both accounts must be reachable by the same token and the destination must not be `isReadOnly` (`session.md`).

## Resumability

A migration is a sequence of batches, and any of them can be the last one before the process dies.

- **Checkpoint after every batch**, into `operations/<year>.md`: batch number, source id range, destination, counts, and the timestamp. That row is the resume point.
- Order batches deterministically — sorted by `receivedAt` ascending, never by an unsorted query — so "resume after the last checkpoint" has an unambiguous meaning (`search.md`).
- On resume, re-run the last checkpointed batch. `alreadyExists` makes it idempotent for imports; for copies, check the destination count first.
- Never resume from a memory of what happened. Resume from the log.

## Verification

Counting the destination is not verification, because a mailbox with the right number of wrong messages passes.

| Check | How |
|---|---|
| Count per mailbox | `Mailbox/get` `totalEmails` on both sides; they should match per mapped pair |
| Date range | Oldest and newest `receivedAt` per mailbox on both sides — catches the "everything dated today" failure |
| Unread counts | `unreadEmails` per mailbox; a mismatch means keywords were lost |
| Sampling | Fetch five messages spread across the range on both sides and compare subject, sender, date, and attachment count |
| Attachments | `{"hasAttachment": true}` count on both sides — attachments are what silently fail on size limits |
| Total bytes | Sum of `size` per mailbox; a large gap means truncated blobs |

Run the checks before proposing anything be deleted from the source, and record the numbers in the migration artifact. "It looked right" is not a number.

## What Does Not Survive

Say these out loud before the migration, not after:

- **Message ids and blob ids.** Anything referencing them — saved filters with hardcoded ids, external links — breaks.
- **Thread grouping** is recomputed by the destination server from headers. Threads that were grouped by client-side heuristics may split.
- **Read/flag state**, unless carried in the manifest and set at import.
- **Server-side rules and filters.** They are account configuration, not mail; they are recreated by hand.
- **Masked email addresses.** They belong to the provider account and cannot move (`masked-email.md`).
- **Custom mailbox order and colours**, subscription state, and per-mailbox settings.
- **Calendar invitations already responded to** — the responses live in other people's calendars.

## Backup Versus Archive

Different jobs, and conflating them produces something that is neither:

| | Backup | Archive |
|---|---|---|
| Purpose | Recover from loss or account compromise | Get old mail out of the working mailbox |
| Contents | Everything, raw blobs, restorable | A selected set, possibly reformatted |
| Verified by | A test restore | A count |
| Where | Off the provider entirely | Often still on the provider |

A backup that has never been restored is a hypothesis. If the user's goal is "not lose my mail", the deliverable includes one restore of a sample into a scratch mailbox, timed, with the procedure written to `artifacts/` — and a `## Due` row so it happens again next year.
