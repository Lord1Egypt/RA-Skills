# Working File Templates — Clients

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — table keys and preference areas alike | `~/Clawic/data/clients/config.yaml` | Key by key, read-modify-write |
| Roster, pipeline, receivables, portfolio snapshots, practice notes, due dates, box index | `~/Clawic/data/clients/memory.md` | Rewritten in place; stays small |
| People at any client — names, roles, channels | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, identified by email or handle |
| Engagements with a start, an end and milestones | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project from the first; client referenced by name only |
| Clients and their terms | `## Roster` in `memory.md`; `~/Clawic/data/clients/clients.md` past the split | One row per client |
| One client whose context outgrows its row — working agreement, approval chain, quirks | `~/Clawic/data/clients/roster/<client-slug>.md` | Its own dossier; the roster row keeps `→ file` |
| Access held at a client — system, account name, granter, date, credential pointer | `~/Clawic/data/clients/roster/<client-slug>.md` | One line per system; pointers only, never values; the line is deleted when the access is revoked |
| Leads and the ones you declined | `## Pipeline` and `## Declined Leads` in `memory.md`; `~/Clawic/data/clients/leads.md` past the split | One row per lead |
| Money owed right now | `## Receivables` in `memory.md`; `receivables.md` past the split | One row per unpaid invoice; the row is deleted when it is paid |
| Invoices actually paid | `~/Clawic/data/clients/revenue/<year>.md` | Append-only, cut by year; this is what the concentration math reads |
| Meetings, calls, decisions and promises, per client | `~/Clawic/data/clients/contact-log/<client-slug>.md` | Append-only, newest first, one file per client |
| Things you produced that get re-read — winning proposals, onboarding checklists, rescue plans, scripts, handovers, post-mortems, case studies, procurement answers | `~/Clawic/data/clients/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| **Anything durable this table does not name** | `~/Clawic/data/clients/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind, including the ones a client hands over | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A lead arrived, moved stage, was won, or was declined | `## Pipeline` / `## Declined Leads` |
| A client was won, paused, retired, or fired | Its row in `## Roster`, with the date |
| Terms changed — rate, model, payment days, deposit | The roster row, in place |
| You learned who someone is at a client | Their row in `~/Clawic/data/contacts/contacts.md` |
| A meeting, call, decision, or promise happened | `contact-log/<client-slug>.md` |
| An engagement started, hit a milestone, or closed | `~/Clawic/data/projects/<project>.md` |
| A change order was requested — priced, free, or refused | The project's change log, with estimated hours either way |
| An invoice was sent or a chase rung was run | `## Receivables` |
| An invoice was paid | Delete its receivables row, append the line to `revenue/<year>.md` |
| A concentration or capacity review ran | `## Portfolio` and `## Due` |
| A proposal won, a script worked, a rescue was planned, an engagement was handed over or post-mortemed | `artifacts/` |
| Anything recurring was scheduled or run | `## Due` |
| The user declared a preference | Its key in `config.yaml` |

## Start flat, split only when it hurts

Everything except artifacts, the contact log, the revenue log and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/clients/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Artifacts are the exception: a proposal, a rescue plan or a handover is born as its own file whatever its size, because it is read whole and only when its subject comes up. The contact log and the revenue log are the other exception: both are append-only records that would otherwise swell `memory.md` until nobody reads it.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. Onboarding is where this bites: clients hand over CMS logins, ad-account access, SFTP details and API tokens in a single email. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`1password:Clients/Acme/wp-admin` · `bitwarden:Acme/sftp` · `keychain:acme-sftp` · `env:ACME_API_TOKEN` · `vault:clients/acme/analytics` · `file:~/.ssh/acme_ed25519`

When the user pastes something to save, replace each secret value before writing and leave the pointer visible: `password: <1password:Clients/Acme/wp-admin>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: company legal name, VAT or company registration number, billing address, invoice and PO numbers, contract reference numbers, project codes, names, roles and work emails of stakeholders, rates and amounts with their currency, portal and ticket URLs, the last four digits of a payment method. **Secrets, strip them**: any login the client handed over (CMS, hosting, SFTP, ad accounts, analytics, e-signature), API keys and tokens for their systems, VPN configs and shared secrets, private keys and passphrases, staging basic-auth passwords, two-factor recovery codes, and full bank account, IBAN or card numbers.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [shared contacts](#shared-contacts) · [shared projects](#shared-projects) · [roster/](#roster) · [contact-log/](#contact-log) · [revenue/](#revenue) · [artifacts/](#artifacts) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/clients/` if it does not exist.

```yaml
engagement_default: retainer
payment_terms_days: 14
deposit_pct: 50
status_cadence: weekly
invoicing_day: 1
concentration_limit_pct: 30
contract_required: true
no_go_list: [gambling, crypto-token-launches]
rate_card_file: rate-card.md
voice_file: client-voice.md

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
communication:
  response_promise: "same business day, not evenings or weekends"
  meeting_day: tuesday
commercial:
  rate_floor: "800 EUR/day"
  rush_surcharge_pct: 25
  retainer_rollover: "one month, then expires"
risk_posture:
  unsigned_start: never
  missed_payments_before_exit: 2
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Clients Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Acme dossier (approval chain, quirks) → `roster/acme.md`; read before anything involving Acme
- Contact log, Acme (2 years) → `contact-log/acme.md`; read before any Acme meeting or when history is disputed
- Winning proposal, retainer shape → `artifacts/proposal-retainer.md`; read when pricing a retainer
- Rate-rise script → `artifacts/script-rate-rise.md`; read before announcing any price change
- Paid invoices 2026 → `revenue/2026.md`; read for any concentration, forecast or best-client question

## Due
| What | Every | Last run | Next due |
|---|---|---|---|
| Send invoices | month, day 1 | 2026-07-01 | 2026-08-01 |
| Receivables sweep | week | 2026-07-20 | 2026-07-27 |
| Portfolio and concentration review | quarter | 2026-04-05 | 2026-07-05 |
| Rate review | year, September | 2025-09-10 | 2026-09-10 |
| Acme contract renewal | — | — | 2026-11-30 |
| Re-contact dormant clients | quarter | 2026-05-02 | 2026-08-02 |

## Roster
| Client | Status | Model | Rate | Terms | Main contact | Channel | Health | Since | Notes |
|---|---|---|---|---|---|---|---|---|---|
| Acme Corp | active | retainer | 4,000 EUR/mo | net 14 | sarah@acme.com | Slack | green | 2024-02 | approvals need CEO above 5,000 EUR → `roster/acme.md` |
| Northwind | paused | project | 850 EUR/day | net 30 | jo@northwind.io | email | amber | 2025-11 | budget frozen until Q4, re-contact 2026-10 |
| Belltower | past | project | 12,000 EUR fixed | net 30 | — | — | — | 2023-2024 | ended well, gave a testimonial, referred Acme |

## Pipeline
| Lead | Source | Stage | Est. value | Next step | Next date |
|---|---|---|---|---|---|
| Kestrel Labs | Belltower referral | proposal sent | 18,000 EUR | chase decision | 2026-07-29 |
| Orbit Health | inbound, website | discovery booked | ~9,000 EUR est. 2026-07-20 | run discovery call | 2026-07-28 |

## Declined Leads
| Lead | Date | Why | Re-open if |
|---|---|---|---|
| BetVista | 2026-06-11 | gambling, on the no-go list | never |
| Tiny Studio | 2026-05-02 | budget 1,200 EUR against a 9,000 EUR scope | they come back with budget, not with scope cuts |

## Receivables
| Invoice | Client | Amount | Issued | Due | Status | Last chase |
|---|---|---|---|---|---|---|
| 2026-041 | Acme Corp | 4,000 EUR | 2026-07-01 | 2026-07-15 | overdue | +7 notice sent 2026-07-22 |
| 2026-042 | Kestrel Labs | 6,000 EUR | 2026-07-20 | 2026-08-19 | sent | — |

## Portfolio
| Quarter | Revenue | Active clients | Largest client share | Notes |
|---|---|---|---|---|
| 2026-Q2 | 34,500 EUR | 4 | Acme 41% | over the 30% limit two quarters running |

## Practice Notes
Deposits stopped being argued once they moved into the proposal as a line item rather than a clause.
Clients who ask for the rate before the scope have never converted above 6,000 EUR.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Renewal dates, invoicing day, receivables sweeps, rate reviews and dormant re-contacts all live here; a date held only in a contract PDF is a date nobody will meet.
- **`## Roster`**: one row per client, identified by client name. `Health` is `green | amber | red` from the Warning Signals table, with the date of the last change in `Notes` when it moves. Amounts carry their currency. Status values: `lead-won | active | paused | past | fired`. A client that ends keeps its row — the history is what makes a win-back or a reference possible.
- **`## Receivables`** holds only what is unpaid. The moment an invoice clears, delete its row and append the line to `revenue/<year>.md`; a receivables table that keeps paid rows stops being a to-do list within a month.
- **`## Portfolio`**: one row per quarter, computed from `revenue/<year>.md`, never estimated from memory. Largest client share = that client's trailing-12-month revenue ÷ total over the same window (SKILL.md Rule 5).
- **`## Practice Notes`** is about the user's own practice across clients — what works in their market. Anything true of one client belongs in that client's row or dossier instead.
- These headings are exactly the ones the split-out files get, so every split stays a copy-paste.

| Status | Meaning |
|---|---|
| `ongoing` | Still learning their clients and how they work |
| `complete` | Roster, terms and cadences are known and current |

## Shared contacts

Lives at `~/Clawic/data/contacts/contacts.md` and is shared with every other skill that touches people — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Contacts

| Name | Role | Preferred channel | Context |
|---|---|---|---|
| Sarah Chen | VP Product, Acme Corp | Slack | client sponsor; approves under 5,000 EUR, CEO above |
```

- **Identity is the email address or handle.** Read the file before adding. If that person is already there, update the row in place — never a second row for the same address. Rows this skill did not write belong to another source; leave them alone.
- **Departure is part of the record.** When someone leaves the client, delete their row and note the date and the replacement in `memory.md`. A contact list that only grows stops being one.
- **Scale cut**: one row per person while there are ≤15. Past that, one file per person at `~/Clawic/data/contacts/<name>.md` with the same fields, and `contacts.md` becomes the index (`Name | Role | → file`). If you arrive and the folder already looks like that, follow it — do not start a parallel `contacts.md`.
- **Foreign columns win.** If `contacts.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- Personal details beyond what the work needs do not belong here, and no credential ever does.

## Shared projects

Lives at `~/Clawic/data/projects/<project>.md`, one file per engagement from the first, identified by the project name that names the file. Also written by planning and delivery skills.

```markdown
# Acme — 2026 rebrand

status: active            # active | paused | closed | cancelled
client: Acme Corp         # name only — the terms live in the clients roster
started: 2026-02-03
budget: 25,000 EUR fixed

## Milestones
- [x] Discovery — 2026-02-14
- [ ] Visual identity — due 2026-08-20

## Decisions
| Date | Decision | Who decided | Written back |
|---|---|---|---|
| 2026-07-14 | Motion graphics in scope, +5,000 EUR, launch moves to 2026-09-04 | Sarah Chen | email 2026-07-14 |

## Change Log
| Date | Request | Est. hours | Outcome |
|---|---|---|---|
| 2026-06-02 | extra social crops | 3 | done free, logged |
| 2026-07-14 | motion graphics | 22 | change order, +5,000 EUR |
```

- **The client is a pointer, never a copy.** Terms, rate and health stay in the roster; people stay in `contacts/`. If a project file already carries client detail written by another skill, leave it and do not duplicate it here.
- **Closing is a status, not a deletion.** A finished engagement keeps its file with `status: closed` and the close date — it is the evidence behind the case study, the reference and the next quote. Only a project that never started is deleted.
- **Foreign structure wins.** If the file already exists with different headings, add your rows under the closest existing heading rather than imposing this shape.
- The change log is the single most valuable thing in this file at renewal time (SKILL.md Rule 3). Free work is logged with its hours exactly like billed work.

## roster/

One file per client, at `~/Clawic/data/clients/roster/<client-slug>.md`, created only when that client's context stops fitting a roster row — an approval chain worth writing down, a working agreement, recurring quirks, or any access they granted. The roster row stays and gains `→ roster/<client-slug>.md`.

```markdown
# Acme Corp
*Read before anything involving Acme. Row lives in the clients roster.*

## Working Agreement
Requests in the Slack channel only; anything by DM gets moved there before it is actioned.
Status every Monday. Two rounds of revisions per deliverable, a third is a change order.

## Approval Chain
Sarah Chen approves under 5,000 EUR. Above that: CEO, who reviews on Thursdays only — anything
landing Friday costs a week.

## Quirks
Prefers a walkthrough over a document. Invoices must carry PO number and project code ACM24.
Closes the last week of December.
```

## contact-log/

One file per client at `~/Clawic/data/clients/contact-log/<client-slug>.md`, newest entry first, created the first time anything is worth remembering. Append; never rewrite an old entry, because its value is that it was written at the time.

```markdown
# Contact log — Acme Corp

## 2026-07-14 — call, Sarah
Approved motion graphics at +5,000 EUR; launch moves to 2026-09-04. Written back same day by email.
Mentioned a budget review in October — renewal conversation should start September.

## 2026-06-02 — Slack
Asked for extra social crops. Done free, 3h, logged in the project change log.
```

Cut only if one client's log passes ~300 lines: move closed years to `contact-log/<client-slug>-<year>.md` and keep the current year in the main file, updating the `## Boxes` line in the same turn.

## revenue/

```markdown
# Revenue — 2026

| Paid | Client | Invoice | Amount | Engagement |
|---|---|---|---|---|
| 2026-07-18 | Acme Corp | 2026-041 | 4,000 EUR | retainer, July |
| 2026-06-30 | Northwind | 2026-038 | 5,100 EUR | discovery |
```

Append-only, cut by year. Amounts carry their currency; if the user bills in more than one, record what was actually received and never sum across currencies without stating the conversion date. This file, not memory, is the source for every concentration, best-client and forecast answer (SKILL.md Rule 5).

## artifacts/

One file per thing, at `~/Clawic/data/clients/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **a proposal that won**, **an onboarding checklist**, **a script that worked** (rate rise, late payment, saying no, firing), **a rescue plan**, **a handover pack**, **an engagement post-mortem**, **a case study or testimonial**, **a completed security questionnaire or procurement answer set**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Script — announcing a rate rise
*Read before any price change on an existing client. Written 2026-07-26, worked on two clients.*

...the actual wording, with the notice period and the effective date as blanks...
```

```markdown
# Post-mortem — Northwind, paused 2026-07
*Read before quoting anything like this again, and before any win-back attempt.*

What was sold: ...
What actually happened: ...
The signal that came first, and how early: approvals doubled in week 3.
What it was worth: 15,300 EUR over 5 months, ~40 unbilled hours.
Do differently: cap revisions in the scope document; deposit per phase, not per project.
```

A security questionnaire or a procurement answer set is worth keeping precisely because it is reused: strip every credential and endpoint secret from it before it lands here, leaving pointers.

If the user tracks the engagement as a project, the decision summary also belongs in `~/Clawic/data/projects/<project>.md`, with the long text staying here and referenced by name.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`clients.md` — `## Roster`. The moment the roster leaves `memory.md`, the `## Boxes` line has to say "read before anything about a named client", because that is now the only thing making it get opened.

`leads.md` — `## Pipeline` and `## Declined Leads`. Declined leads are the reason this file exists: without them, the same unqualified prospect gets re-litigated every year and the same discount gets re-offered. Named `leads.md` and not `pipeline.md` so that nothing in the user's data folder shares a filename with a guide in the skill.

`receivables.md` — `## Receivables`. Rarely needed; a receivables table past 15 open invoices usually means the ladder is not being run rather than that the business grew.
