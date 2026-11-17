# Working File Templates — CRM

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

If data sits at an old location (`~/crm/` or `~/Clawic/crm/`), move it to `~/Clawic/data/crm/` and say so in one line.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — table keys and preference areas alike | `~/Clawic/data/crm/config.yaml` | Key by key, read-modify-write |
| System of record, pipeline, organizations, ICP, data health, metrics, due dates, box index | `~/Clawic/data/crm/memory.md` | Rewritten in place; stays small |
| People — name, role, channel, context | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, every skill reading the same file |
| Commercial state of a person — tier, owner, source, referrer | `## People` in `memory.md` up to ~15, then `~/Clawic/data/crm/people.md` | One row per person, keyed by the same lowercased email |
| Open deals | `## Pipeline` in `memory.md` up to ~15, then `~/Clawic/data/crm/deals.md` | One row per deal |
| Closed deals, won and lost, with their reason | `~/Clawic/data/crm/closed-deals.md` | Append-only from the first close; cut by year past ~200 rows |
| Calls, meetings, emails, notes — anything with a date | `~/Clawic/data/crm/interactions/<year>.md` | Append-only, cut by year, never inside `memory.md` |
| Opt-outs, erasure requests, bounced-and-retired addresses | `~/Clawic/data/crm/do-not-contact.md` | Append-only from the first entry; entries are never deleted |
| Companies and their segment | `## Organizations` in `memory.md` up to ~15, then `~/Clawic/data/crm/organizations.md` | One row per company |
| Things you produced that get re-read — ICP definition, qualification scorecard, win/loss teardown, field dictionary, import mapping, migration plan, message templates, discovery question set | `~/Clawic/data/crm/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| A self-built CRM's actual data files (`crm_tool: files` or `sqlite`) | `~/Clawic/data/crm/db/` — plus dated exports in `db/backups/` | Per the schema in `files-and-sqlite.md` |
| Delivery work that starts after a deal is won | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project; the deal row keeps only its name |
| **Anything durable this table does not name** | `~/Clawic/data/crm/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A person was met, named, or their role or channel changed | Their row in the shared `contacts.md` |
| A tier was set, promoted or demoted; an owner, source or referrer was assigned | Their row in `## People` (or `people.md`), keyed by the same email |
| A deal opened, changed value, changed stage, or slipped its close date | Its row in `## Pipeline` (or `deals.md`) |
| A deal was won or lost | Move the row to `closed-deals.md` with its reason code, and delete it from the pipeline |
| A call, meeting, email or note happened | A line in `interactions/<year>.md`, ending in the next step |
| A next step was agreed, or an overdue sweep ran | The deal's next-step field, and `## Due` for the sweep |
| Someone opted out, asked for deletion, or hard-bounced once | `do-not-contact.md` — before touching anything else |
| A dedupe, bounce, import or export pass ran | `## Data Health`, with counts |
| A tool was chosen, migrated, or a schema decision was made | `## System` |
| Monthly numbers were read (conversion, cycle length, win rate) | `## Metrics` |
| An ICP, scorecard, teardown, field dictionary, mapping or template came out of the session | `artifacts/` |
| A won deal became delivery work | `~/Clawic/data/projects/<project>.md`, and the project name on the closed-deal row |
| The user declared a preference | Its key in `config.yaml` |
| Recurring work was scheduled or run | `## Due` |

## Start flat, split only when it hurts

Everything except interactions, closed deals, the suppression list, artifacts, `db/` and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/crm/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Three things are exceptions and are born as their own file whatever their size: **interactions**, because a log grows without end and would swallow the file that has to stay readable; **the suppression list**, because it is read before every outreach and must never depend on `memory.md` being current; and **artifacts**, because a teardown or an ICP is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`env:HUBSPOT_TOKEN` · `env:PIPEDRIVE_API_TOKEN` · `keychain:attio-api` · `1password:Work/Salesforce/api` · `bitwarden:CRM/airtable` · `file:~/.config/crm/token`

When the user pastes something to save — an export URL, an API snippet, an integration setup, a `.env` — replace each secret value before writing and leave the pointer visible: `token: <keychain:attio-api>`. Say in one line that you did it. Watch for the two that hide inside otherwise harmless text: an **API token embedded in a request URL** (`?api_token=…`, the classic Pipedrive shape) and a **signed export or webhook URL**, which is a bearer credential with an expiry.

In this domain — **not secrets, keep them**: names, work email addresses, company domains, job titles, CRM record and object ids, portal/workspace ids, pipeline and stage names, source labels, deal values and dates, owner names, public profile handles. **Secrets, strip them**: API tokens and keys, OAuth access and refresh tokens, webhook signing secrets, SMTP/IMAP passwords, session cookies, signed export URLs, and the **BCC-to-CRM logging address**, which lets anyone who has it write records into the database. Never write at all, secret or not: payment card numbers, bank details, national id numbers, or health information a contact mentioned in passing — a CRM is not the place for them and no follow-up needs them.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [shared contacts box](#shared-contacts-box) · [interactions/](#interactions) · [closed-deals.md](#closed-dealsmd) · [do-not-contact.md](#do-not-contactmd) · [artifacts/](#artifacts) · [shared projects box](#shared-projects-box) · [db/](#db) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/crm/` if it does not exist.

```yaml
crm_tool: sqlite
pipeline_stages: [Lead, Qualified, Proposal, Negotiation, Closed]
stale_days: 90
stall_days: 21
email_logging: bcc
privacy_regime: gdpr
review_day: Monday

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
conventions:
  required_fields: [email, source, owner, next_step]
  tag_vocabulary: [design, agency, referral, conference-2026]
reporting:
  forecast_style: commit          # commit | weighted
  round_to: 100
safety_posture:
  bulk_edits: confirm-each
  hard_delete: never              # archive instead
  enrichment: company-level-only
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# CRM Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Interactions (2026, 140 entries) → `interactions/2026.md`; read before any "when did we last talk" or pre-call prep
- Suppression list (11) → `do-not-contact.md`; read before naming anyone to contact — every time
- Closed deals (34) → `closed-deals.md`; read before any win-rate, cycle-length or forecast question
- ICP definition → `artifacts/icp.md`; read before qualifying a new lead or judging a list
- Win/loss teardown, Northwind → `artifacts/win-loss-northwind.md`; read before the next deal in that segment
- Self-built database → `db/`; read when a record has to be queried or edited directly

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Pipeline review | week, Monday | 2026-07-20 | 2026-07-27 |
| Dedupe + bounce sweep | month | 2026-07-02 | 2026-08-02 |
| Stale-contact reconnect (tier B) | quarter | 2026-04-14 | 2026-07-14 |
| Full export to `db/backups/` | quarter | 2026-07-01 | 2026-10-01 |
| Retention purge (gdpr) | year | 2026-01-08 | 2027-01-08 |

## System
Record of truth: SQLite at `db/crm.db`, one table per entity, UUID ids. Notion board is a read-only view, rebuilt on export.
Field decisions: no `lifecycle_stage` — deal stage owns status. `source` is a closed list of six values.

## People
| Email | Tier | Owner | Source | Referred by | Since |
|-------|------|-------|--------|-------------|-------|
| ana@northwind.com | A | me | referral | luis@contoso.es | 2026-05-11 |
| luis@contoso.es | A | me | inbound | — | 2025-11-02 |
| pau@studioline.io | B | me | conference-2026 | — | 2026-03-08 |

## Pipeline
| Deal | Org | Contact (email) | Value | Stage | Since | Close (as of) | Next step | Date |
|------|-----|-----------------|-------|-------|-------|---------------|-----------|------|
| Website rebuild | Northwind | ana@northwind.com | 18000 EUR | Proposal | 2026-07-09 | 2026-08-15 (2026-07-24, was 2026-07-31) | They review scope with CFO | 2026-07-29 |
| Retainer renewal | Contoso | luis@contoso.es | 2400 EUR/mo | Negotiation | 2026-07-18 | 2026-08-01 (2026-07-18) | Send redlined terms | 2026-07-28 |

## Organizations
| Org | Domain | Segment | Size | Primary contact |
|-----|--------|---------|------|-----------------|
| Northwind | northwind.com | e-commerce | 50-200 | ana@northwind.com |

## Segments & ICP
Best-fit: 20-100 person e-commerce with an in-house designer. Worst: pre-seed startups — three deals, all lost on price.

## Data Health
2026-07-02 dedupe: 412 records, 18 merged, 6 hard bounces retired. Fields under 70% filled: `phone` (41%) — candidate for deletion.

## Metrics
| Month | Open pipeline | Won | Lost | Win rate | Median cycle | As of |
|-------|---------------|-----|------|----------|--------------|-------|
| 2026-06 | 46000 EUR | 2 | 5 | 29% | 38 d | 2026-06-30 |
| 2026-07 | 52000 EUR | 1 | 1 | — | — | 2026-07-24 (month-to-date) |

## How They Work
Solo designer. Hates data entry; will type one line after a call and nothing more. Wants the overdue list, not a dashboard.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Every recurring thing this skill schedules belongs here, and the review day comes from `review_day`.
- **`## People`**: the commercial state of a person — tier, owner, source, referrer — keyed by the lowercased email, which is the join to the shared `contacts.md`. Name, role, channel and context are not repeated here; a person with no row is unassigned, and the stale sweep treats unassigned as tier B (SKILL.md Follow-Up Cadence). Tier is a stored decision, never recomputed at read time: a promotion or demotion **overwrites the cell** and sets `Since` to that day, so a tier that has not moved in a year is visible (`followup.md`). A row survives its deals — that is the point of keeping it out of `## Pipeline`.
- **`## Pipeline`**: open deals only. A won or lost deal is *moved* to `closed-deals.md` in the same turn, never left with a "Closed" stage — a pipeline that only grows stops forecasting. `Since` is the date the deal entered its current stage, which is what makes `stall_days` computable. Close date carries its as-of date and the previous value in parentheses; keep only the most recent previous one, the full history belongs on the closed row. Values carry their currency.
- **`## Metrics`**: `As of` is the day the number was read. A row whose `As of` is not the last day of the month is month-to-date and must never be compared against a closed month. Re-checking the current month **overwrites** its row; never a second row for the same month.
- **`## Data Health`**: last pass date, record count, merges, retirements, and any field below the 70% fill bar (SKILL.md Rule 6). Without the count, "we cleaned it up" is unverifiable next quarter.
- `people.md`, `deals.md`, `organizations.md` and `metrics-log.md` carry over the heading of the section they came from — `## People`, `## Pipeline`, `## Organizations`, `## Metrics` — unchanged, so each split stays a copy-paste. A split-out file may **add** headings later as it grows (below); it never renames the one it was born with.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still learning their process and their data |
| `complete` | Know the system, the stages and the people well |

## Shared contacts box

Lives at `~/Clawic/data/contacts/contacts.md` and is shared with every other skill that knows people — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Contacts

| Name | Role | Preferred channel | Context |
|------|------|-------------------|---------|
| Ana Ruiz | Head of Ops, Northwind | email ana@northwind.com | Met at Shoptalk 2026; owns the rebuild budget |
```

- **Identity is the email, lowercased.** Read the file before adding. If that address is already there, update the row in place — never append a second one. Rows written by another source are still updatable when the person's facts changed, but never rewritten wholesale.
- **This box holds the person, not the deal.** Role, channel and one line of context. Commercial state stays in this skill's boxes and points here by the same email: stage, value and next step in `## Pipeline`, tier, owner, source and referrer in `## People`. Duplicating the person is the fastest way to make two skills contradict each other.
- **Retirement is part of the inventory.** When someone asks to be removed, or the address hard-bounces (one is enough — it is permanent), delete the row, add the entry to `do-not-contact.md`, and note the date in `## Data Health`. A contact list that only grows stops being a contact list.
- **Scale cut**: one row per person while there are ≤15. Past that, one file per person at `~/Clawic/data/contacts/<name-kebab>.md` with the same fields, and `contacts.md` becomes the index (`Name | Role | → file`). If you arrive and the folder already looks like that, follow it — do not start a parallel `contacts.md`.
- **Foreign columns win.** If `contacts.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- Channel is a pointer to how to reach them, never a password, a portal login, or a private note about them.

## interactions/

One file per year at `~/Clawic/data/crm/interactions/<year>.md`, append-only, newest at the bottom. This is the file that makes "when did we last talk, and about what" answerable, and the only one worth having when everything else is skipped.

```markdown
# Interactions — 2026

| Date | Contact | Deal | Type | Dir | What happened | Next step |
|------|---------|------|------|-----|---------------|-----------|
| 2026-07-24 | ana@northwind.com | Website rebuild | call | in | Scope fine, CFO wants phased billing | Send phased option by 2026-07-29 |
| 2026-07-18 | luis@contoso.es | Retainer renewal | meeting | out | Wants 3-month notice clause | Redlines to their legal |
```

- One line per interaction, written at the end of the conversation (SKILL.md Rule 5). `Dir` is `in` or `out` — who initiated, which is the only reliable signal of whether a relationship is warm.
- The `What happened` cell holds substance, not sentiment: what they said, what changed, what it means. "Good call" is a wasted row.
- Every row ends in a next step, or in `—` plus one word saying why there is none (`closed`, `their move`, `no fit`).
- Past ~500 rows in a year, cut by half-year (`2026-h1.md`, `2026-h2.md`) and update the `## Boxes` line. Never merge years into one file.

## closed-deals.md

The archive that makes every metric computable. A deal moves here the moment it is won or lost, and leaves the pipeline in the same turn.

```markdown
# Closed Deals

| Closed | Deal | Org | Value | Result | Reason | Cycle | Slips | Project |
|--------|------|-----|-------|--------|--------|-------|-------|---------|
| 2026-06-30 | Brand refresh | Fabrikam | 9000 EUR | won | referral, no competitor | 22 d | 0 | fabrikam-brand |
| 2026-06-12 | Shop migration | Tailwind | 14000 EUR | lost | price — chose in-house | 61 d | 2 | — |
```

- `Reason` comes from a closed list agreed once and recorded in `## System` (won: referral / inbound / displaced incumbent / price; lost: price / timing / no decision / chose competitor / disqualified). Free-text reasons cannot be counted, and counting them is the entire point.
- `Cycle` is days from creation to close; `Slips` is how many times the close date moved. Those two columns are what turn a forecast from a guess into an adjustment (`pipeline.md`).
- `Project` is the name of the file in `~/Clawic/data/projects/`, when a won deal became delivery work. The project's content lives there, never here.
- Past ~200 rows, cut by year (`closed-deals-2026.md`) and leave `closed-deals.md` as the index by year.

## do-not-contact.md

Created the first time anyone opts out. Read before every outreach, list, or suggestion of who to contact — this file is the reason it exists, so it is never folded into `memory.md`.

```markdown
# Do Not Contact

| Added | Identifier | Scope | Source of request | Notes |
|-------|-----------|-------|-------------------|-------|
| 2026-05-04 | pedro@example.com | all | reply "remove me" | record deleted 2026-05-04 |
| 2026-06-21 | @example-corp.com | marketing only | procurement policy | sales replies still allowed |
| 2026-07-02 | maria@example.org | all | hard bounce | address retired, person kept |
```

- **Entries are never deleted**, even when the underlying record is. The suppression outlives the contact: an erasure request that removes the row and the suppression entry together guarantees the person is re-imported next quarter (`privacy.md`).
- `Scope` is `all`, `marketing only`, or a named channel. A domain-level entry starts with `@`.
- Where the regime requires proving suppression without keeping the address in the clear, store a one-way hash of the lowercased email and note the algorithm in the row.

## artifacts/

One file per thing, at `~/Clawic/data/crm/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **ICP definition**, **qualification scorecard**, **win/loss teardown**, **field dictionary**, **import mapping**, **migration plan**, **message templates**, **discovery question set**, **stage exit criteria** once they diverge from the default. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# ICP — who this actually works for
*Read before qualifying a lead or judging a purchased list. Written 2026-07-26, from 34 closed deals.*

Fits: ...observable attributes, with the evidence from closed-deals...
Does not fit: ...with the losses that proved it...
Disqualifying signals: ...
```

```markdown
# Win/loss — Northwind
*Read before the next deal in e-commerce, and before quoting phased billing. 2026-07-26.*

Result: won, 18000 EUR, 34 days, 1 slip.
Turned on: the phased-billing option, offered after the CFO appeared in week three.
Nearly lost it: two weeks with no next step while waiting on "their internal chat".
Repeatable: name the CFO in call one; every deal here has one.
```

```markdown
# Field dictionary
*Read before adding, renaming or deleting a field, and before any import mapping. 2026-07-26.*

| Field | Type | Required | Who fills it | What it is for | Fill rate (as of) |
|-------|------|----------|--------------|----------------|-------------------|
| source | enum(6) | yes | whoever creates the record | Channel report, ICP review | 100% (2026-07-02) |
```

## Shared projects box

When a won deal becomes delivery work, the project goes to the shared `~/Clawic/data/projects/<project-kebab>.md` — one file per project from the first, identified by the project name — and the closed-deal row keeps only that name. The file holds objective, status, milestones and decisions taken; the deal's commercial history stays in `closed-deals.md`. The user may not have any project skill installed, so the rules travel with this one:

- **Read before writing.** If the file already exists, update it in place; never create a second file for the same project and never rewrite sections another skill wrote — append yours under your own heading.
- **Foreign structure wins.** If the file, or the folder, already uses other headings, another status vocabulary, or a different filename convention (`2026-northwind.md`, `northwind/README.md`), match what is there and add anything missing as your own trailing section. Never rewrite another skill's headings and never rename its files — a renamed file is a project two skills each think they own.
- **Closing is part of the inventory.** When the work ships, is cancelled, or the client stops, write `status: done — <date>` (or `cancelled — <date>`) at the top of the file plus one line of outcome, in the same turn you learn it. The file stays: it is what makes the next deal in that segment quotable, and it is the input to `artifacts/win-loss-<org>.md`. Past ~20 closed projects, move them to `~/Clawic/data/projects/archive/<project-kebab>.md` keeping the filename, so the folder still reads as the list of live work; the closed-deal row's project name does not change. Never delete a project file — an open-ended folder of finished work is still an inventory, an emptied one is a gap nobody can reconstruct.
- Money inside it carries its currency in the value (`18000 EUR`), the same as everywhere else.
- People named in it are pointers to the shared contacts box, never duplicated records.
- Never copy the project's content back into this skill's boxes.

## db/

Only when `crm_tool` is `files` or `sqlite`: this is the user's actual database, not this skill's notes. Schema, ids, and the query and migration mechanics are in `files-and-sqlite.md`.

```
~/Clawic/data/crm/db/
├── crm.db                     # or contacts.json + interactions.json + deals.json
└── backups/
    └── 2026-07-01-crm.db      # dated copy, written before every bulk operation
```

- A dated backup is written before every import, merge, mass edit or migration (SKILL.md Rule 9), and the quarterly export row in `## Due` keeps one even when nothing bulk happened.
- Backups are pruned on the same schedule as the retention policy in `privacy.md` — a deletion request that leaves the address in a backup has not been honored.

## Split-out files

Created only by the split procedure above, never on day one. Each opens with the exact heading its section had inside `memory.md`, and the rows move across untouched — a rename at split time is a rewrite and loses data. Extra headings below are ones the file **gains later**, never replacements.

`people.md` — `## People`, same columns. Once it exists it is the tier list, and the overdue sweep reads it instead of `memory.md` (`followup.md`). It gains `## Retired` for people whose row left the shared `contacts.md` but whose history still explains a closed deal.

`deals.md` — `## Pipeline`, same columns. One pipeline stays one `## Pipeline` heading forever. Only a genuine second pipeline (new business, renewals, partnerships) adds one `## <pipeline name>` heading per pipeline, and that restructure happens in one turn on whichever file currently holds the deals — never as part of a split.

`organizations.md` — `## Organizations`, same columns. It gains `## Dormant` for companies with no contact in a year. Splitting this one usually means the user needs company-level segments; that is the moment to write `artifacts/icp.md` if it does not exist.

`metrics-log.md` — `## Metrics`, same columns, one row per month. It gains `## Conversion By Stage` and `## By Source` once there are enough closed deals to compute them (`metrics.md`). The reason this file exists is comparison: a month's numbers mean nothing without the twelve before them.
