---
name: Fastmail API
slug: fastmail-api
version: 1.0.2
description: Drives the Fastmail JMAP API for mail, search, bulk triage, sending, masked email, contacts, and calendars. Use when the user mentions Fastmail, JMAP, api.fastmail.com, or a Fastmail API token; when a JMAP call returns 401, 403, `unknownCapability`, `invalidResultReference`, `stateMismatch`, or a `notCreated`/`notUpdated`/`notDestroyed` map; when thousands of messages have to be searched, archived, moved, flagged, or deleted without touching the wrong mailbox; when a draft has to be sent from an alias, identity, or custom domain; when a masked email address has to be created, disabled, or audited; when contacts or calendar events are read or written through JMAP; when an incremental sync or push subscription has to keep a local mirror current; or when a mailbox is being migrated in or out. Not for IMAP clients (`imap`), SMTP delivery (`smtp`), inbox triage as a habit (`inbox`, `email-management`), or Apple Mail on macOS (`apple-mail-macos`).
homepage: https://clawic.com/skills/fastmail-api
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 📬
    requires:
      bins:
      - curl
      - jq
      env:
      - FASTMAIL_API_TOKEN
    os:
    - linux
    - darwin
    - win32
    displayName: Fastmail API
    configPaths:
    - ~/Clawic/data/fastmail-api/
    - ~/Clawic/data/contacts/
    - ~/Clawic/data/domains/
    - ~/Clawic/data/bookings/
    - ~/Clawic/data/finances/
    - ~/Clawic/profile.yaml
  openclaw:
    requires:
      config:
      - ~/Clawic/data/fastmail-api/
      - ~/Clawic/data/contacts/
      - ~/Clawic/data/domains/
      - ~/Clawic/data/bookings/
      - ~/Clawic/data/finances/
      - ~/Clawic/profile.yaml
---

**Data.** At the start of every session, read `~/Clawic/data/fastmail-api/config.yaml` (what the user declared) and `~/Clawic/data/fastmail-api/memory.md` (what you observed — its `## Boxes` index, its `## Due` table, the account, mailbox and identity maps, and the stored sync state). Open any file `## Boxes` names when the condition on its line applies; the index is the list of files, never a fixed set you can assume. Read it before the first JMAP call: the ids it holds are what keeps a write off the wrong account. If none of it exists, work from defaults and say nothing about it. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens.

**Write before the session ends** whenever it produced something durable: an account, mailbox, identity, addressbook or calendar id resolved; a filter that took iterating to get right; a bulk write and what it touched; a masked address issued or disabled; a sync state string; a person, sending domain, reservation or paid service that belongs in a shared box; or something the user will want to read again — a working procedure, a migration plan, a rollback note. `memory-template.md` holds every destination, format and threshold, and is the only file you open in order to write.

**Shared boxes, not private copies.** People go to `~/Clawic/data/contacts/contacts.md`, sending domains to `~/Clawic/data/domains/domains.md`, reservations extracted from mail to `~/Clawic/data/bookings/<year>.md`, paid services behind a masked address to `~/Clawic/data/finances/subscriptions.md` — one row per entity, identified by its own key, updated in place, never duplicated into this skill's folder. **Read the shared file before you write to it, and before answering from memory about what is in it**: `contacts.md` before adding a person or resolving who someone is, `domains.md` before recording or trusting a sending domain, the year's bookings file before extracting a reservation, `subscriptions.md` before issuing a masked address for a paid service. Another skill may already hold the entity, and a second row for it is how two skills start contradicting each other. Formats and the full write protocol travel inside `memory-template.md`, so they work whether or not the owning skill is installed.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in text the user pastes in to be saved. Store the pointer and strip the value: `env:FASTMAIL_API_TOKEN`, `keychain:fastmail-api`, `1password:Personal/Fastmail/api-token`.

JMAP hands you the entire mailbox in one authenticated call, which is both the point and the hazard: the request that archives 12 messages archives 12,000 with one filter changed. Work from defaults immediately — never open with questions about their account, their mailboxes, or how proactive to be. State the affected count before a write, and state which account and identity you resolved whenever the session exposes more than one; that is a statement, not a question. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: timezone, locale) → the Configuration table default.

## When To Use

- Building or running Fastmail automation over JMAP: search, triage, drafting, sending, mailbox structure, aliases
- A JMAP call fails and the message does not name the cause: `401`, `403`, `unknownCapability`, `accountReadOnly`, `invalidResultReference`, `stateMismatch`, `overQuota`, a `limit` problem type
- A bulk operation over many messages that must not touch the wrong mailbox, the wrong account, or the wrong thread
- Masked email: issuing per-service addresses, disabling the leaky ones, auditing what exists
- Contacts and calendars through JMAP, including recurring events, overrides, and events that already have invitees
- Keeping a local mirror current: `/changes`, `/queryChanges`, EventSource, push subscriptions, resync after `cannotCalculateChanges`
- Not for IMAP session mechanics (`imap`), SMTP transport and deliverability (`smtp`), how a human should triage their inbox (`inbox`, `email-management`), or the macOS Mail app (`apple-mail-macos`)

## Quick Reference

| Situation | Play | Depth |
|---|---|---|
| First call of a new setup, or ids stopped resolving | Session discovery → account map → per-account capabilities and limits, then store them | `session.md` |
| "Which account am I even writing to?" | `accounts` vs `primaryAccounts` vs `default_account_id`; `isReadOnly` before any write | `session.md` |
| Building any request beyond one method call | One envelope, back-references, `ifInState`, batch sizing from the session limits | `requests.md` |
| Finding messages: unread, old, from someone, with attachments | `Email/query` filter grammar, sort, `collapseThreads`, anchor pagination, snippets | `search.md` |
| Archive / move / flag / delete at scale | Count → snapshot → smallest batch → verify; move is add+remove in one patch | `triage.md` |
| Mailbox structure: create, rename, nest, empty, roles | Role resolution, depth and name limits, what emptying really does | `triage.md` |
| Draft, attach, and send from the right address | Draft → identity → `EmailSubmission/set` with `onSuccessUpdateEmail`; blob upload | `sending.md` |
| Send from an alias or a custom domain, or a send that bounced | Identity ownership, envelope vs headers, `forbiddenFrom`, bounce handling | `sending.md` |
| Per-service throwaway addresses | `MaskedEmail/set`, `pending` vs `enabled` vs `disabled`, `forDomain` as the audit key | `masked-email.md` |
| Address book work: read, upsert, merge duplicates | ContactCard/JSContact vs the legacy object, dedupe by person not by address | `contacts.md` |
| Calendar events, recurrences, invitations, timezones | JSCalendar shape, `recurrenceOverrides`, what triggers scheduling mail | `calendar.md` |
| Keeping a local copy up to date, or reacting to new mail | `/changes` and state strings, `queryChanges`, EventSource, push verification | `sync.md` |
| Moving a mailbox in or out, or taking a backup | `Email/import`, blob download, `Email/copy`, order of operations, verification counts | `migration.md` |
| Any error string, partial failure, or timeout | Error taxonomy: request level vs method level vs `notUpdated` entry | `troubleshooting.md` |
| Anything else Fastmail or JMAP | Answer directly, then state the account it applies to and whether the operation is reversible | — |

Coverage map: `session.md` discovery and scope · `requests.md` envelope and batching · `search.md` finding messages · `triage.md` bulk writes and mailbox structure · `sending.md` drafts, identities, submission · `masked-email.md` per-service addresses · `contacts.md` address book · `calendar.md` events and scheduling · `sync.md` deltas and push · `migration.md` import, export, backup · `troubleshooting.md` symptom to cause.

## Core Rules

1. **Discover the session before the first call; rediscover only what is missing.** The session response is the only source of `apiUrl`, `uploadUrl`, `downloadUrl`, `eventSourceUrl`, the `accounts` map, `primaryAccounts` per capability, and the limits in `capabilities`. Read the stored `## Account Map` and `## Mailbox Map` in `memory.md` first, discover what is absent or stale, and write the result back in the same turn (`session.md`). Ids are opaque strings scoped to one account: an id copied between accounts is not "not found", it is a silent write to nowhere.
2. **Resolve mailboxes by `role`, never by display name.** `inbox`, `archive`, `drafts`, `sent`, `junk`, `trash` are roles the server assigns; names are localized, user-renamable, and duplicated at different depths. Look up by role, fall back to name only when no role exists for that mailbox, and store the id you resolved in `## Mailbox Map` of `memory.md`.
3. **One request, not a chain.** A query and its fetch belong in a single envelope through a back-reference: `"#ids": {"resultOf": "c0", "name": "Email/query", "path": "/ids"}`. Two round trips are two states, and the second can disagree with the first. `invalidResultReference` means the JSON pointer is wrong, never that permissions are wrong (`requests.md`).
4. **Every write carries `ifInState`.** The state string you read is the only proof that nothing moved underneath you. On `stateMismatch`, re-run the query and re-derive the ids; replaying the same payload writes to a list that no longer exists. State strings are opaque: store them in `## Sync State` of `memory.md`, never parse, compare, or order them.
5. **Count, snapshot, then write the smallest batch.** Run the query, state the affected count out loud, and when it exceeds `confirm_threshold` (default 25) get explicit confirmation. Before any bulk `Email/set`, write the prior `mailboxIds` and `keywords` of the affected ids to `~/Clawic/data/fastmail-api/snapshots/` — that file is the only rollback that exists. Batch size = `min(max_batch_size, the account's maxObjectsInSet)`; first batch is one object.
6. **Deleting is a move to the Trash-role mailbox. `destroy` is permanent.** `Email/set` `destroy` removes the message from the server with no undo, no Trash, and no restore path outside a support-side backup. Governed by `destroy_policy` (default `trash-only`): under that default, "delete these" means patch `mailboxIds` to the trash mailbox and say so.
7. **A move is one patch that adds and removes.** Mailbox membership is a set, not a field: `{"mailboxIds/<newId>": true, "mailboxIds/<oldId>": null}`. Adding without removing leaves the message in both places, which reads to the user as "the move did nothing". A patch update and a whole-property update cannot be mixed in the same object — either `mailboxIds` or `mailboxIds/<id>`, never both.
8. **Partial success is the normal outcome, not the exception.** Every `/set` returns `created`/`updated`/`destroyed` *and* `notCreated`/`notUpdated`/`notDestroyed` with a `SetError` per id. Report both counts and the distinct error types; an HTTP 200 with 40 entries in `notUpdated` is a failed operation. Re-run only the failed ids, after fixing the cause (`troubleshooting.md`).
9. **A missing capability is a scope problem, not an auth problem.** A token issued without calendar scope does not return 401 — the capability is simply absent from `session.capabilities` and from that account's `accountCapabilities`, and naming it in `using` produces `unknownCapability` at the request level. Check the session before concluding the token is invalid, and check `accountCapabilities` before concluding the *server* lacks it: capabilities are per account.

## Failure Signatures

Decode rule: the level that emitted the error names the layer. An HTTP status is about the *connection or the token*; a request-level problem type is about the *envelope*; a method-level error is about the *call*; a `SetError` inside `notUpdated` is about *one object*.

| Signature | Most likely cause | First move |
|---|---|---|
| `401` on the session endpoint | Token invalid, revoked, or sent without the `Bearer ` prefix | Re-check the header shape, then re-issue the token in Fastmail settings (`session.md`) |
| `401` on `apiUrl` but the session endpoint works | Calling the wrong host or a stale `apiUrl` | Always take `apiUrl` from the live session response, never hardcode it |
| `unknownCapability` | A URN in `using` is not in `session.capabilities` | Token scope, not server support — compare against the session (Rule 9) |
| `accountNotFound` | `accountId` belongs to another token, or was copied between accounts | Re-resolve from `accounts` / `primaryAccounts` for that capability |
| `accountReadOnly` | Delegated or shared account granted read access only | `accounts[id].isReadOnly` says so before you call; there is no retry that fixes it |
| `accountNotSupportedByMethod` | The account exists but has no such capability | Per-account `accountCapabilities`, not the top-level list |
| `invalidResultReference` | The back-reference `path` does not resolve in the previous response | Fix the JSON pointer; `/ids` for a query, `/list/*/id` for a get (`requests.md`) |
| `stateMismatch` | Something changed between your read and your write | Re-query, re-derive ids, re-apply — never replay (Rule 4) |
| `cannotCalculateChanges` | Server cannot produce a delta from that old state | Full resync; retrying the same `/changes` returns the same error forever (`sync.md`) |
| Request-level `limit` problem type | `maxSizeRequest`, `maxCallsInRequest`, or `maxConcurrentRequests` exceeded | The `limit` property names which one; split the envelope or serialize (`requests.md`) |
| `overQuota` | Mail storage full — writes and imports fail before sends do | Free space or raise the plan; imports fail silently mid-batch otherwise |
| `tooLarge` / `requestTooLarge` | Payload or attachment over the account limit | Budget `raw_bytes × 1.33` for base64 against `maxSizeAttachmentsPerEmail` (`sending.md`) |
| `forbiddenFrom` on submission | The identity does not own the From address | Identity ownership and custom-domain verification (`sending.md`) |
| Everything "worked" but the user sees no change | `collapseThreads: true` returned one id per thread, so you wrote to one message | Act on the thread, not the representative (`search.md`) |
| The move ran and the message is in both mailboxes | Added the destination without removing the source | One patch, add and remove (Rule 7) |
| Anything else | Find the exact method call and the error object it returned, then match it here | `troubleshooting.md` |

## Limits That Decide Batch Size

Read these from the session; none of them is a constant you may hardcode, and they differ per account. The names are stable, the values are not.

| Limit | Lives in | What it decides |
|---|---|---|
| `maxCallsInRequest` | core capability | How many method calls fit in one envelope — exceeding it fails the whole request, not the last call |
| `maxObjectsInGet` / `maxObjectsInSet` | core capability | The real page size for `/get` and the hard cap on `max_batch_size` |
| `maxSizeRequest` | core capability | Total bytes of the envelope; long id lists hit this before call count does |
| `maxConcurrentRequests` | core capability | How many requests may be in flight; exceeding it is a `limit` problem type, not a 429 to retry blindly |
| `maxSizeUpload` / `maxConcurrentUpload` | core capability | Blob upload ceiling and parallelism (`sending.md`) |
| `maxSizeAttachmentsPerEmail` | mail capability, per account | Attachment budget after base64 inflation (`× 1.33`), not raw file size |
| `maxMailboxesPerEmail` | mail capability, per account | How many mailboxes one message may belong to — a filing scheme can exceed it |
| `maxMailboxDepth` / `maxSizeMailboxName` | mail capability, per account | Whether a nested folder tree can be created at all (`triage.md`) |
| `emailQuerySortOptions` | mail capability, per account | Which sort keys the server will accept; an unsupported one fails the query |
| `mayCreateTopLevelMailbox` | mail capability, per account | Whether mailbox creation is even permitted in a delegated account |

## Reversibility

Decide this before the write, not after. The middle column is what the user is actually asking when they say "are you sure?".

| Operation | Reversible? | Do first |
|---|---|---|
| Add or remove a keyword (`$seen`, `$flagged`) | Yes, cheaply | Nothing beyond the count |
| Move between mailboxes | Yes, if you know where it came from | Snapshot the prior `mailboxIds` of every affected id (Rule 5) |
| Move to Trash | Yes, until the server's Trash retention expires | Snapshot; say the retention window is finite |
| `Email/set` `destroy` | **No** | `destroy_policy` must allow it; explicit confirmation naming the count; snapshot the ids and headers |
| Destroy a mailbox | **No**, and it takes the messages that live only there | Query the message count first and say it; offer emptying-into-Trash instead |
| Send (`EmailSubmission/set`) | Only inside the account's delayed-send window, by setting `undoStatus: "canceled"` | Verify recipients and identity; state the window (`sending.md`) |
| Masked email `state: "deleted"` | Address stops working; the service-to-address mapping is lost | Prefer `disabled` — it keeps the record and the audit trail (`masked-email.md`) |
| Patch an event with participants | The scheduling mail already went out | Check the participant list before touching an invited event (`calendar.md`) |
| Contact merge or delete | Depends entirely on your snapshot | Write the merged-away card into the snapshot before destroying it (`contacts.md`) |

## Output Gates

Before delivering a request, a batch, or a result summary:

- Did I name the account and identity this touches, and confirm the account is not `isReadOnly`?
- Did I state the affected count *before* writing, and is it under `confirm_threshold` or explicitly confirmed?
- Is every id in this payload one I resolved in *this* account, by role or by query — never copied from an example?
- Does the write carry `ifInState`, and did I read both the success and the `notCreated`/`notUpdated`/`notDestroyed` maps?
- Is anything irreversible in this batch (`destroy`, mailbox destroy, send, masked-email delete)? Then it ships with a snapshot and a separate confirmation, never inside a copy-paste block of read calls.
- Did anything durable come out of this — a resolved id, a working filter, a bulk write, a masked address, a sync state, a person, a domain, a booking? Then it is written to its box in `memory.md` or the file `## Boxes` names, in this turn (`memory-template.md`).

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/fastmail-api/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| default_account_id | text | none | Account every method call scopes to; unset means the `primaryAccounts` entry for that capability, named out loud when more than one account exists (Rule 1) |
| default_identity | text (email) | none | From address and `identityId` used by `sending.md`; unset means the identity matching the account's primary address |
| jmap_session_url | text (url) | `https://api.fastmail.com/jmap/session` | Session endpoint; change only for a non-Fastmail JMAP server, which also changes which vendor capabilities exist |
| max_batch_size | number (1-500) | 50 | Objects per `/set` call in `triage.md` and `migration.md`, hard-capped by the account's `maxObjectsInSet` (Rule 5) |
| confirm_threshold | number (objects) | 25 | Above this many affected objects, a write waits for explicit confirmation (Rule 5) |
| destroy_policy | never \| trash-only \| allow | trash-only | Whether `destroy` may be called at all, or deletion always means a move to the Trash-role mailbox (Rule 6) |
| dry_run_first | bool | true | Every bulk write is preceded by its query and a stated count, with no write in the same message |
| protected_mailboxes | list (roles or names) | [] | Mailboxes no write ever targets; a match aborts the whole batch rather than skipping the item |
| timezone | text (IANA) | from `profile.yaml`, else UTC | Timezone assumed for date filters in `search.md` and for every write in `calendar.md` |
| redact_subjects | bool | false | Whether subjects and addresses are masked in summaries and in `operations/<year>.md` |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tooling** — raw `curl` + `jq` versus a JMAP client library, and whether requests are shown or just their results — affects every example in `requests.md`
- **Conventions** — mailbox hierarchy and naming, keyword vocabulary beyond the standard set, masked-email `description` format, snapshot file naming — affects `triage.md` and `masked-email.md`
- **Scope** — which capabilities are in play at all (mail only, or mail plus contacts, calendars, masked email) — affects what `using` ever contains and which boxes get written
- **Safety posture** — whether destructive payloads are emitted at all, whether every send pauses inside the undo window, appetite for batch size — affects Output Gates and `sending.md`
- **Output format** — how a bulk result is summarized (counts only, per-error breakdown, full id lists), and how much of a subject line is quoted — affects every result summary
- **Sync** — polling versus EventSource versus push subscription, and how fresh a mirror has to be — affects `sync.md`
- **Restrictions** — addresses, domains, or mailboxes that are never written to or never emailed — affects `protected_mailboxes` and `sending.md`
- **Cadence** — how often masked addresses, sending domains, snapshots, and duplicate contacts get audited — affects the `## Due` table in `memory.md`

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Hardcoding `apiUrl` or a mailbox id from a working example | Ids are per account and the URL is per session; the call succeeds against nothing | Resolve from the session and by role, every time (Rules 1-2) |
| Treating `destroy` as "delete" | It is permanent and skips Trash entirely | Patch `mailboxIds` to the trash role; `destroy` only under `destroy_policy: allow` (Rule 6) |
| Acting on ids from a `collapseThreads: true` query | You get one representative per thread and write to one message of many | Query with `collapseThreads: false`, or expand via `Thread/get` (`search.md`) |
| Paginating a large query by `position` | Concurrent delivery shifts the window; you skip and double-process | `anchor` + `anchorOffset` is the stable cursor (`search.md`) |
| Retrying a `/changes` call that returned `cannotCalculateChanges` | The server cannot produce that delta and never will | Full resync, then store the new state (`sync.md`) |
| Sending by creating the message and then "moving it to Sent" | Two writes, and a crash between them leaves a duplicate draft | `onSuccessUpdateEmail` on the submission does it atomically (`sending.md`) |
| Marking junk with the `$junk` keyword alone | The keyword is metadata; the move into the junk-role mailbox is what the server acts on | Move and set the keyword together (`triage.md`) |
| Deduplicating contacts by email address | One person with three addresses becomes three people, and merging deletes real data | Match on person, merge fields, snapshot before destroying (`contacts.md`) |
| Patching an invited event "quietly" | Participant changes generate scheduling mail to everyone on the event | Check the participant list first and say what will be sent (`calendar.md`) |
| Deleting a masked address that started getting spam | The address-to-service mapping disappears with it, so the leak is never attributable | `disabled` keeps the record and stops the mail (`masked-email.md`) |
| Storing the token in the memory file "just for convenience" | It is the whole account, in plaintext, in a folder that gets backed up | Pointer only: `env:FASTMAIL_API_TOKEN` (`memory-template.md`) |
| Running a bulk write with no snapshot because "it is just an archive" | Reversing 4,000 moves without the prior `mailboxIds` is not possible | Snapshot first; it is one file and it is the only undo (Rule 5) |
| Assuming HTTP 200 means the batch succeeded | JMAP reports per-object failure inside a 200 | Read the `not*` maps every time (Rule 8) |

## Where Experts Disagree

- **Server-side rules versus agent-side triage.** Anything that must happen to *every* future message — filing, flagging, spam routing — belongs in server-side rules if the session advertises the Sieve capability, because it runs when no agent is connected. Agent-side batches win for one-off cleanups, judgement calls, and anything needing the message body. The frontier is recurrence, not complexity.
- **Polling versus push.** A cron-style `/changes` poll is trivially debuggable and survives restarts; EventSource and push subscriptions cut latency to seconds but add a verification handshake and a reconnect story. Sub-minute freshness requirement → push; anything looser → poll, and spend the saved complexity elsewhere (`sync.md`).
- **One masked address per service versus per category.** Per service makes every leak attributable and every disable surgical, at the cost of an inventory that grows to hundreds. Per category keeps the list readable but destroys attribution the moment one address is sold. Per service wins if — and only if — the inventory is actually written down (`masked-email.md`).
- **Mailbox hierarchy versus keywords.** Deep folder trees hit `maxMailboxDepth` and force one home per message; keywords are many-per-message and searchable but invisible in most clients' navigation. Fastmail's search makes a flat archive plus keywords defensible; teams migrating from Outlook usually cannot work that way.

## Security & Privacy

**External endpoints:** only official Fastmail JMAP endpoints, all discovered from the session response.

| Endpoint | Data sent | Purpose |
|---|---|---|
| `https://api.fastmail.com/jmap/session` | Bearer token in the `Authorization` header | Discover `apiUrl`, capabilities, accounts, and limits |
| The `apiUrl` from that session | JMAP method payloads for mail, submission, contacts, calendars, and masked email | Execute read and write calls |
| The `uploadUrl` / `downloadUrl` from that session | Attachment and message blobs | Attach files, export messages |
| The `eventSourceUrl` from that session | Bearer token; receives state strings only | Change notifications (`sync.md`) |

**Credentials:** the token is read from the `FASTMAIL_API_TOKEN` environment variable. This skill does NOT store, copy, log, or transmit it anywhere else, never echoes an `Authorization` header, and never writes a credential into `~/Clawic/data/`.

**Local storage:** account ids, mailbox and identity ids, saved filters, masked-address inventory, sync state, and operation history stay in `~/Clawic/data/fastmail-api/`; people, sending domains, reservations and subscriptions go to their shared boxes. Message bodies are never written to disk unless the user asks for an export by name.

**Guardrails:** calls are read-only by default. Bulk writes state their count first, snapshot prior state, and run smallest-batch-first. Irreversible operations — `destroy`, mailbox destroy, masked-address deletion, sending — require explicit confirmation and are never emitted inside a block of read-only calls.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/fastmail-api (install if the user confirms):
- `imap` — reading and syncing mailboxes over IMAP, for servers or clients without JMAP
- `smtp` — transport-level sending, auth diagnostics, and deliverability testing
- `dns` — SPF, DKIM, and DMARC records behind a custom sending domain
- `email-management` — how a human should triage and reply, once the automation exists
- `calendar-planner` — planning across calendars, above the level of individual event writes

## Feedback

- If useful, star it: https://clawic.com/skills/fastmail-api
- Latest version: https://clawic.com/skills/fastmail-api

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/fastmail-api.
