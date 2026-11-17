# Bulk Writes and Mailbox Structure

The point where a mistake stops being a bad answer and becomes a changed mailbox. Every procedure here is built around one order: count, snapshot, smallest batch, verify.

**Before any write**, read `## Mailbox Map` and `protected_mailboxes` from config, plus `## Saved Queries` if the target set comes from a stored filter (`~/Clawic/data/fastmail-api/memory.md`, or the files `## Boxes` names). **Before the write lands**, put the prior `mailboxIds` and `keywords` of every affected id into `~/Clawic/data/fastmail-api/snapshots/<date>-<what>.md`; **after it lands**, append the row to `~/Clawic/data/fastmail-api/operations/<year>.md` with the counts and the snapshot path (`memory-template.md`). A bulk write with no snapshot has no undo, and one with no log cannot be explained three months later.

**Contents:** [The Bulk Write Procedure](#the-bulk-write-procedure) · [Move, Copy, File](#move-copy-file) · [Keywords](#keywords) · [Junk and Not-Junk](#junk-and-not-junk) · [Deleting](#deleting) · [Mailbox Structure](#mailbox-structure) · [Emptying a Mailbox](#emptying-a-mailbox) · [Server-Side Rules](#server-side-rules) · [Undoing a Batch](#undoing-a-batch)

## The Bulk Write Procedure

1. **Query with `calculateTotal: true`** and `collapseThreads: false` unless the target genuinely is one message per thread (`search.md`).
2. **State two numbers**: how many matched, and how many will actually change. They differ whenever part of the set is already in the target state.
3. **Abort if any target or source mailbox is in `protected_mailboxes`.** Abort the batch, not the item — a partially-applied filing scheme is worse than none.
4. **Snapshot** prior `mailboxIds` and `keywords` for every id, before the first write.
5. **Write one object.** Verify it. Then batches of `min(max_batch_size, maxObjectsInSet)` with `ifInState`.
6. **Read both maps** on every batch (`requests.md`). Stop on the first batch with unexplained failures; a systematic error repeats 40 times if you let it.
7. **Verify by re-query**, not by trusting the counts: re-run the original filter and confirm it now returns what it should (usually zero).
8. **Log** the operation row in `~/Clawic/data/fastmail-api/operations/<year>.md`, with the counts and the snapshot path.

Above `confirm_threshold` (default 25) step 5 waits for explicit confirmation. With `dry_run_first: true` (the default), steps 1-3 are delivered as a message on their own, with no write attached.

## Move, Copy, File

Mailbox membership is a **set**. This shapes everything:

```json
"update": {"M8f21": {"mailboxIds/<destination>": true, "mailboxIds/<source>": null}}
```

| Intent | Patch |
|---|---|
| Move | Add destination, remove source, one update object |
| File in two places | Add destination only — the message is legitimately in both |
| Move out of everything into one place | `{"mailboxIds": {"<destination>": true}}` — whole-property replace, and it wipes every other membership |
| Remove from one mailbox, keep the rest | `{"mailboxIds/<source>": null}` — fails if it is the last membership |

- **A message must always be in at least one mailbox.** Removing the last one is rejected; that operation is `destroy`.
- **`maxMailboxesPerEmail`** (per account, `session.md`) caps multi-filing. A tagging scheme built on mailboxes hits it; one built on keywords does not.
- **Cross-account is `Email/copy`, not a move.** `Email/copy` takes `fromAccountId` and `accountId`, creates a new message in the destination account with a new id, and only removes the original if `onSuccessDestroyOriginal` is set. The source and destination ids have nothing to do with each other afterwards.

## Keywords

Free-form per message, many at once, and the natural way to tag without touching structure.

- Standard set: `$seen`, `$flagged`, `$draft`, `$answered`, `$forwarded`, `$junk`, `$notjunk`. Custom keywords are allowed and are lowercase-ASCII by convention; they show up in most clients as labels or flags.
- Patch shape: `{"keywords/$seen": true}` to add, `{"keywords/$seen": null}` to remove. Same no-mixing rule as `mailboxIds`.
- `{"keywords": {"$seen": true}}` replaces the whole set and silently drops `$flagged`, `$answered`, and every custom tag on that message. It is the most common accidental data loss in this domain because nothing errors.
- Marking a large set read is a keyword write, not a move, and it is fully reversible — snapshot is still worth it when the prior read state is information the user cares about (an "unread since" boundary is destroyed by a blanket mark-read).
- Thread-level intent needs thread-level filters: "mark this conversation read" is `Thread/get` then a keyword write on every `emailId` (`search.md`).

## Junk and Not-Junk

Two operations, and they are done together:

| Intent | Move | Keyword |
|---|---|---|
| This is spam | Into the `junk`-role mailbox | `$junk` set, `$notjunk` removed |
| This is not spam | Out of `junk` into `inbox` (or the intended mailbox) | `$notjunk` set, `$junk` removed |

The move is what the server acts on; the keyword is metadata that travels with the message. Setting `$junk` while leaving the message in the Inbox produces a message that claims to be spam and is sitting in the Inbox — no filter changes, and the user sees nothing happen.

## Deleting

Three different things wear the word "delete":

| Operation | Effect | Reversible |
|---|---|---|
| Move to the `trash`-role mailbox | Out of sight, still on the server, subject to the account's Trash retention | Yes, until retention expires |
| `Email/set` `destroy` | Removed from the server | **No** |
| Destroy a mailbox | Removed, and it takes every message that lived only there | **No** |

Under the default `destroy_policy: trash-only`, "delete these 400 emails" means a move to Trash and one line saying so. `destroy` requires `destroy_policy: allow`, an explicit confirmation naming the count, and a snapshot that at minimum holds the ids, senders, subjects and dates — because after the call, that snapshot is the only record the messages existed.

Emptying Trash is `destroy` on the contents of the Trash mailbox and obeys the same gate. "It is already in Trash" is not an argument for skipping confirmation; it is the last moment the messages exist.

## Mailbox Structure

`Mailbox/set` creates, renames, reparents, and destroys.

```json
"create": {"newbox": {"name": "Acme", "parentId": "Mb2200", "isSubscribed": true}}
```

| Constraint | Where it lives | Effect |
|---|---|---|
| `maxMailboxDepth` | mail capability, per account | A nested tree deeper than this cannot be created; check before designing the scheme |
| `maxSizeMailboxName` | mail capability, per account | Long descriptive names fail at creation, not at use |
| `mayCreateTopLevelMailbox` | mail capability, per account | Often false in a delegated account |
| `myRights.mayCreateChild` | per mailbox | Whether this specific parent accepts children |
| Sibling name uniqueness | server | Two mailboxes cannot share a name under one parent — a rename can collide |

- **Renaming keeps the id**; the message set is untouched. Renames are cheap and reversible.
- **Reparenting** (`parentId` patch) moves the whole subtree. Depth is recomputed — moving a three-level subtree under a two-level parent can exceed `maxMailboxDepth` and fail after you have already told the user it would work.
- **Role is server-assigned.** Do not attempt to set `role` when creating; resolve the existing role-holder instead (`session.md`).
- `Mailbox/set` `destroy` takes `onDestroyRemoveEmails`. Left false, the call fails if the mailbox has messages — which is the safe default and the one to rely on. Setting it true destroys messages that exist nowhere else.

Before proposing any restructure, write the decision and its rejected alternative to `artifacts/` (`memory-template.md`); a filing scheme is exactly the thing that gets re-litigated in six months.

## Server-Side Rules

Anything that must happen to *every future message* belongs on the server, not in a batch. If the session advertises a Sieve capability (`session.md`), rules can be managed through JMAP; if not, they are managed in the Fastmail web settings and this skill's role is to specify the rule precisely, not to pretend it can install it.

The dividing line: **recurrence, not complexity.** A one-time cleanup of 4,000 old newsletters is a batch. "Newsletters should always land in a folder" is a rule — it runs at delivery, when no agent is connected, and it stops the batch from ever being needed again. Proposing a batch for a recurring problem is treating the symptom every quarter.

## Undoing a Batch

1. Find the operation row in `operations/<year>.md` and open the snapshot it names.
2. Reverse per id: patch `mailboxIds` and `keywords` back to their recorded prior values, in batches, with `ifInState`.
3. Ids that now return `notFound` were destroyed or moved by something else after the batch — report them individually rather than skipping them silently.
4. Log the reversal as its own operation row, referencing the original.

There is no undo for `destroy`, for a destroyed mailbox, or for a sent message past its undo window. Those three are why the confirmation exists.
