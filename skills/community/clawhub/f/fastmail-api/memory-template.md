# Working File Templates — Fastmail API

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — Configuration table keys and preference areas alike | `~/Clawic/data/fastmail-api/config.yaml` | Key by key, read-modify-write |
| Account ids, capability scope, session limits, identities, sync state, box index, due dates | `~/Clawic/data/fastmail-api/memory.md` | Rewritten in place; stays small |
| Calendar and address book ids: name, id, whether writable | `## Account Map` in `memory.md`, resources sub-table | One row per calendar or address book, a handful per account |
| Mailbox id ↔ role ↔ name, per account | `## Mailbox Map` in `memory.md`; `~/Clawic/data/fastmail-api/mailboxes.md` once it outgrows it | One row per mailbox |
| Filters that took iterating to get right | `## Saved Queries` in `memory.md`; `~/Clawic/data/fastmail-api/queries.md` once it outgrows it | One entry per named query |
| Masked email addresses and what each one is for | `## Masked Emails` in `memory.md`; `~/Clawic/data/fastmail-api/masked-emails.md` once it outgrows it | One row per address |
| High-impact writes: what ran, on how many objects, with what result | `~/Clawic/data/fastmail-api/operations/<year>.md` | Append-only, cut by year |
| Prior state of objects a bulk write is about to change | `~/Clawic/data/fastmail-api/snapshots/<date>-<what>.md` | Its own file per operation, from the first one |
| Things you produced that get re-read — working procedures, migration plans, rollback notes, mailbox-structure decisions | `~/Clawic/data/fastmail-api/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| People the user actually corresponds with | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, every skill in one address list |
| Domains used for sending | `~/Clawic/data/domains/domains.md` (**shared**) | One row per domain |
| Reservations and tickets found in mail or turned into events | `~/Clawic/data/bookings/<year>.md` (**shared**) | One row per booking, cut by year |
| Paid services behind a masked address or a receipt | `~/Clawic/data/finances/subscriptions.md` (**shared**) | One row per subscription, amount with currency |
| **Anything durable this table does not name** | `~/Clawic/data/fastmail-api/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Tokens, app passwords, push keys, anything that authenticates | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

Deciding where something new goes, in order: **would another skill want to read it?** → shared box above. **Is it a text read whole when its subject comes up?** → `artifacts/`. **Is it one more row of something accumulating?** → a section of `memory.md` until the split threshold, then its own file.

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A session was discovered, or the account/capability picture changed | `## Account Map` |
| A calendar or address book was listed, or its `myRights` read | `## Account Map`, resources sub-table |
| A mailbox id was resolved by role or query | `## Mailbox Map` |
| An identity was found, created, or changed its address | `## Identities` |
| A filter took more than one attempt to get right | `## Saved Queries` |
| A `/changes` or `/queryChanges` cycle completed | `## Sync State` |
| A bulk write ran (move, flag, delete, import, export) | `operations/<year>.md`, plus its snapshot before the write |
| A masked address was created, disabled, or deleted | `## Masked Emails` |
| A masked address was issued for a paid service, or a receipt named a subscription | `~/Clawic/data/finances/subscriptions.md` |
| A person came up who the user will deal with again | `~/Clawic/data/contacts/contacts.md` |
| A custom sending domain was configured or verified | `~/Clawic/data/domains/domains.md` |
| A confirmation email was turned into a calendar event | `~/Clawic/data/bookings/<year>.md` |
| A procedure, migration plan, or rollback note came out of the session | `artifacts/` |
| A non-obvious failure was diagnosed | `## Pain Points` |
| The user declared a preference | Its key in `config.yaml` |
| Recurring work was scheduled or run | `## Due` |

## Start flat, split only when it hurts

Everything except artifacts, snapshots, operation logs and the shared boxes begins inside `memory.md`. Splitting is a procedure carried out by whichever agent is about to write the entry that crosses the threshold — never deferred, never proposed to the user:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/fastmail-api/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Artifacts, snapshots and operation logs are the exception: each is born as its own file whatever its size, because it is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`env:FASTMAIL_API_TOKEN` · `keychain:fastmail-api` · `1password:Personal/Fastmail/api-token` · `bitwarden:Fastmail/api` · `vault:secret/fastmail/token` · `file:~/.config/fastmail/token`

When the user pastes something to save — a curl command, a `.env`, a script, a support transcript — replace each secret value before writing and leave the pointer visible: `Authorization: Bearer <env:FASTMAIL_API_TOKEN>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: account ids (`u1a2b3c4`), mailbox ids and roles, identity ids, thread and email ids, blob ids, addressbook and calendar ids, state strings, the user's own email addresses and aliases, masked addresses and their `forDomain`, the session URL, capability URNs, quota numbers, the *name* of the environment variable holding the token.

**Secrets, strip them**: the API token value itself, any `Authorization:` header with a literal value, Fastmail app passwords, OAuth access and refresh tokens, push subscription `keys.p256dh` / `keys.auth` and the verification code, DKIM private keys, anything inside a message body that is a one-time code, password reset link, or invitation token — those expire but they are live while you are writing them down.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [mailboxes.md](#mailboxesmd) · [queries.md](#queriesmd) · [masked-emails.md](#masked-emailsmd) · [operations/](#operations) · [snapshots/](#snapshots) · [artifacts/](#artifacts) · [shared contacts](#shared-contacts) · [shared domains](#shared-domains) · [shared bookings](#shared-bookings) · [shared subscriptions](#shared-subscriptions)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/fastmail-api/` if it does not exist.

```yaml
default_account_id: u1a2b3c4
default_identity: me@example.com
max_batch_size: 50
confirm_threshold: 25
destroy_policy: trash-only
dry_run_first: true
protected_mailboxes: [archive, "Legal hold"]
timezone: Europe/Madrid
redact_subjects: false

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
scope:
  capabilities: [mail, submission, maskedemail]   # contacts and calendars out of scope for now
conventions:
  masked_description: "<service> — signed up <date>"
sync:
  mode: poll            # poll | eventsource | push
  interval_minutes: 15
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Fastmail API Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Masked addresses (34) → `masked-emails.md`; read before issuing a new one or investigating spam on an alias
- Saved queries (19) → `queries.md`; read before writing any Email/query filter from scratch
- Bulk write history → `operations/2026.md`; read when asked what a past batch did, or before repeating one
- Pre-change snapshots → `snapshots/`; read only to undo a specific operation, named in operations/
- Newsletter purge procedure → `artifacts/newsletter-purge.md`; read when a recurring bulk cleanup is requested
- Gmail import plan → `artifacts/gmail-import.md`; read if the migration resumes or is questioned

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Masked-address audit (disable unused) | quarter | 2026-04-14 | 2026-07-14 |
| Sending domain check: SPF/DKIM/DMARC + expiry | quarter | 2026-05-02 | 2026-08-02 |
| Snapshot prune (older than 90 days) | month | 2026-07-01 | 2026-08-01 |
| Contacts duplicate pass | half-year | 2026-02-20 | 2026-08-20 |

## Account Map
| Account id | Kind | Capabilities in scope | Read only | Primary address |
|---|---|---|---|---|
| u1a2b3c4 | personal | mail, submission, maskedemail, contacts, calendars | no | me@example.com |
| u9z8y7x6 | shared (team@) | mail | yes | team@example.com |

Session limits observed 2026-07-26: maxCallsInRequest 64 · maxObjectsInGet 4096 · maxObjectsInSet 4096 · maxConcurrentRequests 10.
Values are read from the session, not assumed; re-read them when a `limit` error appears.

### Calendars and address books
| Account | Kind | Name | Id | Writable |
|---|---|---|---|---|
| u1a2b3c4 | calendar | Personal | Cal19f | yes |
| u1a2b3c4 | calendar | Holidays (subscribed) | Cal4b2 | no — `myRights` read only |
| u1a2b3c4 | addressbook | Default | Ab01 | yes |

## Mailbox Map
| Account | Role | Name | Id | Parent | Notes |
|---|---|---|---|---|---|
| u1a2b3c4 | inbox | Inbox | Mb1001 | — | — |
| u1a2b3c4 | archive | Archive | Mb1002 | — | — |
| u1a2b3c4 | trash | Trash | Mb1004 | — | — |
| u1a2b3c4 | — | Clients/Acme | Mb2210 | Mb2200 | protected: never bulk-write |

## Identities
| Identity id | Address | Domain | Default | Notes |
|---|---|---|---|---|
| I77a | me@example.com | example.com (own, see domains box) | yes | — |
| I92c | hello@acmestudio.dev | acmestudio.dev | no | custom domain, DKIM verified 2026-05-02 |

## Sync State
| Account | Type | State | As of |
|---|---|---|---|
| u1a2b3c4 | Email | `s-4f21c9` | 2026-07-26 |
| u1a2b3c4 | Mailbox | `s-11ab04` | 2026-07-26 |

## Saved Queries
- **vendor-noise** — unread, older than 90 days, in Inbox, from a list address: `{"inMailbox":"Mb1001","notKeyword":"$seen","before":"2026-04-27","header":["List-Unsubscribe"]}`. Used by the quarterly purge.
- **acme-thread-search** — everything from the Acme domain, threads collapsed off: `{"from":"@acme.example","inMailboxOtherThan":["Mb1004"]}`.

## Masked Emails
| Address | For | State | Created | Notes |
|---|---|---|---|---|
| a1b2c3@fastmail.example | shop.example | enabled | 2026-03-11 | paid, see subscriptions box |
| d4e5f6@fastmail.example | forum.example | disabled | 2025-11-02 | started receiving spam 2026-06 |

## Pain Points
2026-06-18: an archive batch used ids from a `collapseThreads: true` query — 340 threads reported, 340 messages actually moved. Threads now queried uncollapsed by default.

## How They Work
Wants counts before writes, not explanations. Reads the JSON. Never asks for the curl, only the result.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Every recurring thing this skill schedules belongs here.
- **`## Account Map`** is the section that pays for this whole file: it is what stops a write landing in a shared or read-only account. Update it the moment a session is discovered, and record `isReadOnly` even when it is `no`.
- **The calendars-and-address-books sub-table** holds container ids only — one row per calendar or address book, with the `myRights` verdict in `Writable`, because a subscribed calendar accepts the call and drops the event. Individual contact card and event ids are *not* stored: they are re-resolved by query each time, since a card deleted and recreated keeps the name and changes the id. If an account ever grows past ~15 containers, this sub-table splits out under the same rules as any other section.
- **`## Mailbox Map`** stores the id you resolved *and* the role you resolved it by. A row without a role is only usable by name, which is exactly the fragile path. Ids from different accounts never share a table without the account column.
- **`## Sync State`**: state strings are opaque. Store them verbatim, never parse, compare, or sort them. Replace the row, never append a second one for the same account and type. A state older than the server's change window returns `cannotCalculateChanges` — record the resync date when that happens.
- **`## Masked Emails`**: `For` is the service the address was issued to and it is the only reason this table exists — an address with no `For` cannot be audited. Disabled rows stay; deleted rows get a date and a reason, then move to the bottom.
- These headings are exactly the ones `mailboxes.md`, `queries.md` and `masked-emails.md` get when they split out, so each split stays a copy-paste.

| Status | Meaning |
|---|---|
| `ongoing` | Still resolving their accounts, mailboxes, and habits |
| `complete` | Account map is stable; act directly |

## mailboxes.md

Created by the split procedure when `## Mailbox Map` outgrows `memory.md` — common on any account with a real folder tree. The table moves across unchanged: same columns, same order, `Account` included, no per-account headings. The split is a copy-paste, never a rewrite.

```markdown
# Mailboxes

| Account | Role | Name | Id | Parent | Notes |
|---|---|---|---|---|---|
| u1a2b3c4 | inbox | Inbox | Mb1001 | — | — |
| u1a2b3c4 | — | Clients/Acme | Mb2210 | Mb2200 | protected: never bulk-write |
| u9z8y7x6 | inbox | Inbox | Mb7001 | — | shared account, read only |
```

Re-verify an id before a destructive write if the row is older than the last mailbox state change; mailboxes can be deleted and recreated with a new id under the same name.

## queries.md

Same shape as `## Saved Queries`. One entry per named filter: the name, the JSON, what it is for, and the trap it encodes. A query nobody can explain gets deleted, not kept.

```markdown
# Saved Queries

- **vendor-noise** — unread, older than 90 days, in Inbox, from a list address.
  `{"inMailbox":"Mb1001","notKeyword":"$seen","before":"2026-04-27","header":["List-Unsubscribe"]}`
  Run uncollapsed. Feeds the quarterly purge; always paired with a snapshot.
```

Dates inside a stored filter go stale — a hardcoded `before` is a point in time, not a rolling window. Note which fields are recomputed at run time.

## masked-emails.md

Same headings as `## Masked Emails`. This is an inventory, so it obeys the inventory rules: read it before issuing a new address (the service may already have one), update the row in place when a state changes, and never let it only grow.

```markdown
# Masked Emails

| Address | For | State | Created | Notes |
|---|---|---|---|---|
| a1b2c3@fastmail.example | shop.example | enabled | 2026-03-11 | paid, see subscriptions box |
```

When the address belongs to a paid service, the money side goes to `~/Clawic/data/finances/subscriptions.md` and this row just names the service. Never copy the price here.

## operations/

One file per year, append-only. This is the answer to "what did that batch actually do", asked three months later.

```markdown
# Operations — 2026

| Date | Account | Operation | Filter / target | Objects | Result | Snapshot |
|---|---|---|---|---|---|---|
| 2026-07-14 | u1a2b3c4 | move → Archive | saved query `vendor-noise` | 1,842 | 1,840 updated, 2 notUpdated (`notFound`) | `snapshots/2026-07-14-vendor-noise.md` |
| 2026-07-20 | u1a2b3c4 | destroy | Trash older than 1 year | 3,110 | confirmed by user, irreversible | `snapshots/2026-07-20-trash-purge.md` |
```

Subjects and addresses are summarized, never pasted in bulk; with `redact_subjects: true` they are omitted entirely. Every irreversible row names the confirmation.

## snapshots/

One file per operation, written **before** the write, at `~/Clawic/data/fastmail-api/snapshots/<date>-<what>.md`. It exists to be replayed backwards, so it holds ids and prior values, nothing else.

```markdown
# Snapshot — vendor-noise archive, 2026-07-14
*Read only to reverse this operation. Account u1a2b3c4. Referenced from operations/2026.md.*

Reverse by patching each id back to its prior mailboxIds and keywords.

| Email id | Prior mailboxIds | Prior keywords |
|---|---|---|
| M8f21 | Mb1001 | — |
| M8f2a | Mb1001, Mb2210 | $flagged |
```

Prune per the `## Due` row. A snapshot whose operation can no longer be reversed — because the messages were later destroyed — is deleted along with its `## Boxes` mention.

## artifacts/

One file per thing, at `~/Clawic/data/fastmail-api/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **a recurring procedure that finally worked**, **a migration plan**, **a mailbox-structure decision and why**, **a rollback note for something already reversed**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Procedure — quarterly newsletter purge
*Read when a recurring bulk cleanup is requested. Written 2026-07-14.*

1. Run saved query `vendor-noise` with the `before` date recomputed to today − 90 days.
2. State the count. Above confirm_threshold, wait.
3. Snapshot prior mailboxIds and keywords.
4. Move in batches of 50 with ifInState; on stateMismatch, re-query.
5. Log the row in operations/<year>.md.
```

```markdown
# Decision — flat archive plus keywords, not a folder tree
*Read before proposing any mailbox restructure. 2026-07-26.*

Decision: one Archive mailbox, filing by keyword.
Why: maxMailboxDepth would cap the client tree they wanted, and one message often belongs to two clients.
Rejected: Clients/<name> hierarchy — forces one home per message.
Migration cost if reversed: one bulk move per keyword, snapshot per batch.
```

If the work is tracked as a project, the summary also belongs in the shared `~/Clawic/data/projects/<project>.md`, with the detail staying here and referenced by name.

## Shared contacts

Lives at `~/Clawic/data/contacts/contacts.md` and is shared with every other skill that deals with people — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Contacts

| Name | Email or handle | Role | Preferred channel | Context |
|------|-----------------|------|-------------------|---------|
| Marta Ruiz | marta@acme.example | Acme ops lead | email | invoicing thread, replies within a day |
```

- **Identity is the email or handle.** Read the file before adding. If that address is already there, update the row in place; only its absence justifies a new row. A person with several addresses is one row — extra addresses go in `Context`, never a second row.
- **Write the people who matter, not the address book.** This box holds people the user will deal with again. Never mirror a Fastmail address book into it; a bulk import destroys a curated file and cannot be undone from the JMAP side.
- **Retirement is part of the box.** When a relationship ends and the user says so, delete the row and note the date in `memory.md`. A list that only grows stops being useful.
- **Foreign columns win.** If `contacts.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- **Scale cut**: one row per person while there are ≤15. Past that, one file per person at `~/Clawic/data/contacts/<name>.md` with the same fields, and `contacts.md` becomes the index (`Name | Email | Role | → file`). If the folder already looks like that, follow it — never start a parallel `contacts.md`.
- Never a password, a security answer, or a one-time code. Contact records are exactly where those get pasted by accident.

## Shared domains

Lives at `~/Clawic/data/domains/domains.md`. A custom sending identity is a domain fact before it is a mail fact: SPF, DKIM and DMARC live in DNS, and the expiry date kills the mail flow when it passes.

```markdown
# Domains

| Domain | Registrar | Expires | Used for | Mail records | Notes |
|--------|-----------|---------|----------|--------------|-------|
| acmestudio.dev | (registrar name) | 2027-02-14 | Fastmail sending identity I92c | SPF ok, DKIM verified 2026-05-02, DMARC p=none | — |
```

- **Identity is the domain name.** Read before adding; update in place if it is there. Add your `Used for` and `Mail records` notes to the existing row instead of creating a second one.
- Record the DKIM *selector and verification date*, never a private key.
- **Retirement is part of the inventory.** When a domain lapses, is sold, or stops being used for sending, delete its row and note the date against the identity it served in `## Identities` of `memory.md` — a dead domain still listed is what makes the next `forbiddenFrom` unexplainable. If the domain is still owned and only the sending stopped, keep the row and empty `Used for` instead of deleting it; a row that is not yours to delete stays.
- **Scale cut**: one `domains.md` table up to ~40 hostnames. Past that, group by apex domain into `~/Clawic/data/domains/<apex>.md` with the same fields, and `domains.md` becomes the index (`Domain | Registrar | Expires | → file`). If the folder already looks like that, follow it — never start a parallel table.
- **Foreign columns win**: match the header you find.
- Expiry belongs in `## Due` of whichever skill noticed it, so it gets checked; here it is a value, not a reminder.

## Shared bookings

Lives at `~/Clawic/data/bookings/<year>.md`, cut by year. Written only when a confirmation email is turned into a calendar event or a reservation is extracted on purpose — never as a side effect of a search.

```markdown
# Bookings — 2026

| Locator | Provider | What | Dates | Status | Source |
|---------|----------|------|-------|--------|--------|
| XK4T2P | (airline) | MAD → LHR | 2026-09-03 | confirmed | mail 2026-07-20, event created |
```

- **Identity is the locator.** Read the year file before adding; a re-sent confirmation updates the existing row rather than creating a duplicate.
- Amounts, if recorded, carry their currency inside the value (`184 EUR`).
- Cancellation is an update to `Status` plus the date, not a deleted row — the cancelled booking is what explains the refund later.
- **Foreign columns win**: match the header you find.

## Shared subscriptions

Lives at `~/Clawic/data/finances/subscriptions.md`. Written when a masked address is issued for a paid service, or when a receipt or renewal notice is what the user was searching for.

```markdown
# Subscriptions

| Service | Amount | Cycle | Next charge | Paid from | Contact address |
|---------|--------|-------|-------------|-----------|-----------------|
| shop.example Pro | 9 USD | monthly | 2026-08-11 | (card reference, last four only) | a1b2c3@fastmail.example |
```

- **Identity is the service name.** Read before adding; update in place, including when the price changes — a second row for the same service hides the increase, which is the one thing this file exists to reveal.
- **Amounts carry their currency inside the value** (`9 USD`), because rows from other skills will be in other currencies and someone will add the column up.
- Cancelled means a row update with the end date, then removal once the final charge has cleared.
- Never a card number beyond the last four, never a login, never a billing portal password.
- **Foreign columns win**: match the header you find.
