# Working File Templates — Freelance

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — Configuration table keys and preference areas alike | `~/Clawic/data/freelance/config.yaml` | Key by key, read-modify-write |
| Practice state: positioning, rates in force, capacity, insurance, platforms, pain points, due dates, box index | `~/Clawic/data/freelance/memory.md` | Rewritten in place; stays small |
| Clients, prospects, referrers, subcontractors, accountants — any person | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, every skill writing into one book |
| The delivery work of an engagement: goal, milestones, decisions, handover | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project, from the first |
| Business bank and tax accounts, tool subscriptions, budget | `~/Clawic/data/finances/accounts.md`, `subscriptions.md`, `budget.md` (**shared**) | One row per account or subscription, amounts with currency |
| Commercial terms of each engagement — rate, basis, committed hours, terms, notice, portfolio rights | `## Engagements` in `memory.md`; `~/Clawic/data/freelance/engagements.md` once it outgrows the section | One row per engagement, closed ones kept with an end date |
| Leads and live opportunities | `## Pipeline` in `memory.md`; `~/Clawic/data/freelance/pipeline.md` once it outgrows the section | One row per opportunity; dead ones move to the quote log |
| Every quote sent and how it ended, with the reason | `## Win/Loss` in `memory.md`; `~/Clawic/data/freelance/wins-losses.md` once it outgrows the section | One row per quote — this is the evidence for Rule 6 |
| Monthly billings, collections, billable hours, utilization | `~/Clawic/data/freelance/income/<year>.md` | Append-only, one row per month, cut by year |
| Days present per country, when the year is genuinely mobile | `~/Clawic/data/freelance/days/<year>.md` (`international.md`) | Append-only, one row per stay, cut by year; created only when there is a first stay to record |
| Things you produced that get re-read — rate card, proposal or quote template, an MSA or clause set that was accepted, redline notes, a case study, an outreach message that got replies, a dry-spell runbook, a dispute timeline and evidence index, a positioning or entity decision | `~/Clawic/data/freelance/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| **Anything durable this table does not name** | `~/Clawic/data/freelance/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials, tax identifiers, bank numbers, client confidential material | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

Deciding where something unnamed goes, in this order: (1) would another skill want to read it — a person, a project, an account, a subscription? Then the shared box, not here. (2) Is it a text read whole when its subject comes up — a template, a contract that was accepted, a decision with its reasoning, a case study? Then `artifacts/`, its own file from the first one. (3) Is it one more row of something that accumulates? Then a section of `memory.md` until the split threshold.

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A rate was derived, set, or raised | `## Rates`, with the inputs used (Rule 1) and the date |
| A quote or proposal went out | A row in `## Win/Loss` with the number, basis and scope size |
| A quote was won, lost, or ghosted | The same row: outcome, reason in the client's words, and the winner's price if known |
| An engagement started, was repriced, renewed, or ended | Its row in `## Engagements`; the delivery work in `~/Clawic/data/projects/<project>.md` |
| A month closed | A row in `income/<year>.md`: invoiced, collected, billable hours, top client share |
| Payment terms, a deposit, a notice period or portfolio rights were agreed | The engagement row — these are the fields nobody else stores |
| An invoice went overdue, or was collected after chasing | `## Engagements` notes plus the DSO column in `income/<year>.md` |
| A client, prospect, referrer, subcontractor or accountant was met or named | Their row in the shared `contacts.md` |
| A tool subscription, business account or tax account was opened or closed | The shared `finances/` file (`subscriptions.md` or `accounts.md`) |
| A tax, VAT, filing, insurance-renewal, contract-notice or review date was learned | `## Due` |
| Insurance was bought, renewed, or a client's cover requirement was learned | `## Insurance` |
| A marketplace account, level, rating or fee tier changed | `## Platforms` |
| A subcontractor was engaged, with their rate and margin | `## Bench`; the person in `contacts.md` |
| Review of a subcontractor's work found defects, or cost rework hours | The `Rework` column of their `## Bench` row (`scaling.md`) |
| A stay in another country began or ended, in a mobile year | A row in `days/<year>.md` (`international.md`) |
| A dispute produced a timeline and an evidence pack | `artifacts/dispute-<client>.md` (`disputes.md`) |
| Something cost effort to find out and would cost it again — a client's real procurement path, a jurisdiction rule, a platform limit | `## Pain Points` |
| A rate card, template, accepted contract, case study or working outreach message exists | `artifacts/` |
| A positioning, entity, channel or pricing-model decision was made | `artifacts/`, with what was rejected and why |
| The user declared a preference | Its key in `config.yaml` |

## Start flat, split only when it hurts

Everything except artifacts, income records and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/freelance/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Artifacts are the exception: a rate card, a template or a decision is born as its own file whatever its size, because it is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. A pasted contract, invoice, tax letter, bank statement or platform export is the densest source of them: strip each value **before** writing and leave its pointer in place, in this shape: `<kind>:<locator>`.

`1password:Work/Stripe/live` · `bitwarden:Business/Upwork` · `keychain:wise` · `env:INVOICE_API_KEY` · `vault:secret/freelance/portal` · `file:~/Documents/tax/utr.txt`

In a text, the pointer goes where the value was: `IBAN: <1password:Business/Bank/current>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: business and client names, rates and amounts with currency, payment terms in days, invoice numbers, project names, marketplace usernames and public profile URLs, job titles, jurisdictions, entity type, insurer name and policy type, renewal dates, contract clause text you wrote.

**Secrets, strip them**: bank account numbers, IBANs, sort codes and routing numbers, card numbers, tax identifiers (SSN, EIN, NIF, UTR, VAT number where the user treats it as private), portal and platform passwords, payment-processor API keys, 2FA recovery codes, e-sign account credentials, a client's confidential material pasted for reference (source code, customer lists, unreleased plans) — that last one gets summarized in a line, never stored.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [shared contacts book](#shared-contacts-book) · [shared projects](#shared-projects) · [shared finances](#shared-finances) · [income/](#income) · [days/](#days) · [artifacts/](#artifacts) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/freelance/` if it does not exist.

```yaml
trade: backend development
currency: EUR
target_income: 60000
billable_hours_per_year: 1150
business_costs_per_year: 9000
engagement_basis: daily
payment_terms_days: 14
deposit_pct: 40
tax_jurisdiction: ES / Madrid
business_entity: sole-trader
tax_setaside_pct: 32
runway_months_target: 6
client_concentration_cap_pct: 40
ai_disclosure: proactive
rate_card_file: artifacts/rate-card.md
tone_file: artifacts/voice.md

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
risk_posture:
  start_without_signature: false
  red_lines: [unlimited liability, IP over pre-existing tools, exclusivity without retainer]
conventions:
  revisions_included: 2
  rights_model: assignment on final payment, pre-existing libraries licensed
  minimum_engagement: 2 days
work_order:
  discovery_before_quote: true
  drafts_reviewed_before_sending: true
  paper_before_price: false
channels: [referral, ex-colleagues, one agency, no marketplaces]
exclusions: [gambling, unpaid spec work]
cadence:
  pipeline_review: weekly
  invoice_run: monthly, day 1
  rate_review: yearly, January
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Freelance Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Income by month, 2026 (6 months closed) → `income/2026.md`; read before any rate, buffer, concentration or utilization number
- Income by month, 2025 (12 months closed) → `income/2025.md`; read when comparing years or preparing a filing
- Rate card (1 page) → `artifacts/rate-card.md`; read before quoting anything
- Accepted MSA and the clauses that survived (1 page) → `artifacts/msa-standard.md`; read when a client sends their own paper
- Case study, Meridian reconciliation (1 page) → `artifacts/case-study-meridian.md`; read when proposing similar work
- Dry-spell runbook (1 page) → `artifacts/runbook-dry-spell.md`; read when pipeline coverage drops under 2×

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Quarterly tax payment | quarter | 2026-07-20 | 2026-10-20 |
| VAT return | quarter | 2026-07-20 | 2026-10-20 |
| Pipeline review | week | 2026-07-24 | 2026-07-31 |
| Invoice run | month, day 1 | 2026-07-01 | 2026-08-01 |
| Rate review | year | 2026-01-15 | 2027-01-15 |
| Professional indemnity renewal | year | 2025-11-04 | 2026-11-04 |
| Notice window, Meridian retainer (30 days) | — | — | 2026-08-31 |

## Practice
Backend development, fintech data pipelines. Sells "a payments reconciliation service that closes in a day".
Positioning decided 2026-02 after two years of generalist work — see `artifacts/decision-niche.md`.

## Rates
| Date | Basis | Rate | Floor at the time | Inputs used | Note |
|------|-------|------|-------------------|-------------|------|
| 2025-01-10 | daily | 480 EUR | 433 EUR | 55k take-home, 1200 h, 30%, 8k costs | first derived floor |
| 2026-01-15 | daily | 620 EUR | 507 EUR | 60k take-home, 1150 h, 32%, 9k costs | 8 of last 10 quotes won → raised 29% |

## Engagements
| Client | Project | Basis | Rate | Committed | Terms | Deposit | Notice | Portfolio rights | Status |
|---|---|---|---|---|---|---|---|---|---|
| Meridian | reconciliation-v2 | retainer | 4,800 EUR/mo | 2 d/week (8 d/mo) | 14 d | n/a | 30 d | logo + anonymized metrics | active since 2025-11 |
| Kessler | data-migration | fixed | 14,000 EUR | 3 milestones | 14 d | 40% cleared | — | none, NDA | active, m2 delivered |
| Aurelio | audit | daily | 620 EUR | ad hoc | 7 d | 50% | — | full case study agreed | ended 2026-05-19 |

## Pipeline
| Opportunity | Source | Est. value | Basis | Stage | Next step | Next step due |
|---|---|---|---|---|---|---|
| Norsk ledger review | referral (Meridian CTO) | 18,000 EUR | fixed | quoted 2026-07-18 | follow up | 2026-07-28 |
| Pallas retainer | ex-colleague | 5,000 EUR/mo | retainer | discovery call held | send scope | 2026-07-29 |

## Win/Loss
| Date | Client | Quoted | Basis | Outcome | Reason (their words) | Winner's price |
|---|---|---|---|---|---|---|
| 2026-06-02 | Kessler | 14,000 EUR | fixed | won | "only quote that said what done means" | — |
| 2026-05-11 | Brightside | 620 EUR/day | daily | lost | "over budget" | 430 EUR/day, agency |

## Capacity
Sells 3 days a week, reserves Monday for pipeline and admin. Trailing utilization 58%.
Holiday funded as a sinking line: 20 days at the day rate, 2026 taken 6.

## Insurance
| Cover | Insurer | Limit | Premium | Renewal | Required by |
|---|---|---|---|---|---|
| Professional indemnity | (broker name) | 1,000,000 EUR | 340 EUR/yr | 2026-11-04 | Meridian MSA clause 11 |

## Platforms
| Platform | Status | All-in commission observed | Note |
|---|---|---|---|
| Upwork | dormant since 2025-03 | ~10% fee + connects | exit clause served; two clients moved off-platform after the contracted period |

## Bench
| Subcontractor | Trade | Their rate | Charged to client | Margin | Rework | Used on |
|---|---|---|---|---|---|---|
| (see contacts) | frontend | 380 EUR/day | 560 EUR/day | 32% | 6 h over 2 engagements, 1 defect after handover | Kessler m3 |

## Pain Points
2025-09: Brightside paid at 71 days; no interest clause in the contract. Every contract since carries one.
2026-03: Kessler procurement required a supplier form and insurance certificate before PO — two weeks lost. Certificate now kept in artifacts.

## How They Work
Wants the number and the formula, then a draft they can edit. Will not chase a client without seeing the exact message first.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Tax and VAT dates, insurance renewals, contract notice windows, rate reviews and every accepted cadence from `config.yaml` live here. A notice window is a one-off row with a date and no cadence: missing it renews a contract nobody wanted.
- **`## Rates`**: never overwrite the previous rate — the history is what makes the next raise arguable. Every row records the inputs the floor was computed from, because a floor without its inputs cannot be rechecked when a term changes.
- **`## Engagements`**: amounts carry their currency. `Committed` is the capacity the engagement consumes (days per week, hours per month, or milestone count) — it is what makes utilization computable. `Portfolio rights` is written when the contract is signed, not remembered later. A finished engagement keeps its row with an end date; deleting it destroys the concentration history.
- **`## Pipeline`**: every row has a `Next step` and a date, or it is not an opportunity. When an opportunity dies, move it to `## Win/Loss` with the reason and delete the pipeline row — a pipeline that only grows stops being a forecast.
- **`## Win/Loss`**: the reason is recorded in the client's words, not paraphrased into "price". Ten rows is the minimum sample for Rule 6; without the log every rate rise is a feeling.
- **`## Bench`**: `Rework` is the hours spent fixing or re-reviewing their work; priced at your rate, it is what turns the headline margin into the real one (`scaling.md`). A subcontractor no longer used keeps the row with the date and the reason — the bench is a record of who worked out.
- **`## Platforms`**: `All-in commission observed` is the fee plus lead costs actually paid over a period, not the advertised take rate. Fee schedules change — record the date observed.
- These headings are exactly the ones `engagements.md`, `pipeline.md` and `wins-losses.md` get when their sections outgrow this file, so each split stays a copy-paste.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still learning their practice, rates and clients |
| `complete` | Know the rate basis, the book of business and how they sell |

## Shared contacts book

Lives at `~/Clawic/data/contacts/contacts.md` and is shared with every other skill that knows people — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Contacts

| Name | Key | Role | Preferred channel | Context | Last contact | File |
|------|-----|------|-------------------|---------|--------------|------|
| Ana Ruiz | ana@meridian.example | client, Meridian CTO | email | retainer since 2025-11; also the source of the Norsk referral | 2026-07-18 | — |
| Tomas Lind | tomas@lind.example | subcontractor, frontend | signal | 380 EUR/day, used on Kessler m3 | 2026-07-02 | — |
```

- **Identity is `Key`**: lowercase email, else handle, else `<kebab-name>` plus a stable disambiguator. The key is a column of the row, never implicit and never delegated to a per-person file. `Preferred channel` is the *type* of channel, not the address — it cannot serve as a key.
- **Read the file before adding.** If the key is already there, update the row in place; only its absence justifies a new row. Never rewrite or delete a row this skill did not write — another skill owns it.
- **Retirement**: when a person is no longer a contact of this practice, remove only what this skill added to their row and note the date in `## Pain Points` or the engagement row. Do not delete a person another skill may still be using.
- **Scale cut**: one row per person while there are ≤15. Past that, one file per person at `~/Clawic/data/contacts/<name>.md` with the same fields, and `contacts.md` becomes the index with the `File` pointer. If the folder already looks like that on arrival, follow it — never start a parallel `contacts.md`.
- **Foreign columns win.** If `contacts.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- Rates, terms and margins stay in this skill's `## Engagements` and `## Bench`, referenced from the contact by name. The person is written once, in one place.

## Shared projects

The delivery work of an engagement lives at `~/Clawic/data/projects/<project>.md`, one file per project from the first, shared with every skill that tracks work.

```markdown
# reconciliation-v2

client: Meridian (see contacts)
status: active
goal: close daily reconciliation in under one hour, from four.
milestones: m1 ingest ✔ 2026-03 · m2 matching engine ✔ 2026-06 · m3 reporting — due 2026-09
decisions: batch over streaming (cost, 2026-03) · Postgres over the warehouse (latency, 2026-04)
handover: runbook + two sessions, contracted
```

- **Identity is the file name** — the project's own name in kebab-case, chosen once and never renamed, because other skills link to it by path. **Read the folder before creating anything**: if a file for that project already exists, add to it; only its absence justifies a new file.
- **Never rewrite or delete what another skill wrote.** Add your lines under the structure that is already there, and if the folder uses a different layout (front-matter, per-client subfolders, a different field set), adapt to it rather than starting a parallel convention.
- Closing a project is `status: done | cancelled — <date>` inside the file, never deleting it: it is the record of what was delivered and the raw material of the next case study. Past ~20 closed, move them to `projects/archive/<project>.md` without renaming.
- Commercial terms do not go here — rate, deposit, notice and portfolio rights live in `## Engagements`. The project file names the client and the engagement by name only.

## Shared finances

Business accounts, the tax account and paid tools live at `~/Clawic/data/finances/`, shared with every money skill.

```markdown
| Account | Type | Purpose | Reference | Currency |
|---------|------|---------|-----------|----------|
| Business current | bank | operating account | 1password:Business/Bank/current | EUR |
| Tax set-aside | savings | Rule 3 transfers only | 1password:Business/Bank/tax | EUR |
```

- Identity is the account or subscription name. Read before adding; update in place; never touch a row another skill wrote.
- Amounts always carry their currency inside the value (`340 EUR/yr`), and an estimate carries the date it was estimated — the file mixes currencies and someone will sum the column.
- Tool subscriptions that are business costs (design suite, accounting, marketplace membership, e-sign) go to `subscriptions.md`; their total is what feeds `business_costs_per_year` in `config.yaml`, so a subscription added here means the rate floor is stale.
- **Retirement**: a closed account or a cancelled subscription has its row deleted and the date noted in `## Pain Points`. A list that only grows stops being the input to `business_costs_per_year`, and cancelling rather than pausing is the whole point of keeping it (`cashflow.md`).
- **Scale cut**: `subscriptions.md` is never split — it stays small precisely because cancellation deletes rows. Past 15 accounts, each moves to `~/Clawic/data/finances/accounts/<name>.md` with the same fields and `accounts.md` becomes the index (`Account | Type | Purpose | → file`). If the folder already looks like that on arrival, follow it; never start a parallel `accounts.md`.
- **Foreign columns win.** If the file already exists with a different column set, match its columns and put anything missing in a trailing note. Never rewrite its header.
- References only. Never an account number, IBAN, sort code or portal password.

## income/

The record every health number is computed from. One file per year, one row per month, append-only.

```markdown
# Income — 2026

| Month | Invoiced | Collected | Billable hours | Hours worked | Largest client share | DSO | Note |
|-------|----------|-----------|----------------|--------------|---------------------|-----|------|
| 2026-05 | 11,400 EUR | 9,200 EUR | 92 | 148 | 54% | 31 | Aurelio ended |
| 2026-06 | 13,000 EUR | 13,000 EUR | 104 | 160 | 48% | 19 | — |

## Year totals
| Metric | Value | As of |
|---|---|---|
| Collected | 68,400 EUR | 2026-06-30 |
| Billable hours | 561 | 2026-06-30 |
| Effective rate (collected ÷ hours worked) | 78 EUR | 2026-06-30 |
```

- **Invoiced and collected are different columns and both are needed**: invoiced measures selling, collected measures the business surviving, and the gap is DSO.
- `Hours worked` includes everything — selling, admin, unbilled fixes. Without it the effective rate cannot be computed, and the effective rate is the number that tells the truth about a practice.
- A month is written once, when it closes. Re-checking a closed month overwrites its row; never a second row for the same month.
- Three closed months replace the `billable_hours_per_year` default with the user's own annualized figure (SKILL.md Rule 2). Say so in one line when it happens.

## days/

Only for a mobile year, and only from the first stay worth recording. One file per year, one row per stay, append-only — a residency question is decided on days present, and nobody reconstructs them later (`international.md`).

```markdown
# Days present — 2026

| From | To | Country | Days | Purpose | Running total, country |
|------|----|---------|------|---------|------------------------|
| 2026-01-04 | 2026-03-28 | PT | 84 | working, client Meridian remote | PT 84 |
| 2026-04-02 | 2026-04-19 | ES | 18 | home | ES 18 |
```

- Count arrival and departure days the way the jurisdiction counts them, and write which rule you applied — several count any part-day of presence.
- The threshold itself (183 days or the local equivalent) goes in `## Due` as a dated row, so it is checked before a trip is booked rather than after.
- Visa or permit status per country belongs in the `Purpose` cell in words; permit numbers and passport data are never stored.

## artifacts/

One file per thing, at `~/Clawic/data/freelance/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **rate card**, **proposal or quote template**, **an MSA or clause set that was accepted**, **redline notes for a client's paper**, **case study**, **outreach message that got replies**, **dry-spell runbook**, **dispute timeline and evidence index** (`dispute-<client>.md`), **positioning, entity or channel decision**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn. Every secret inside is already a pointer.

```markdown
# Rate card — 2026
*Read before quoting anything. Derived 2026-01-15, floor 507 EUR/day.*

Day rate 620 EUR · half-day 380 EUR · retainer 2 d/week billed as 8 d/mo 4,800 EUR/mo (3% under 8 × 620, bought with 30 days notice)
Rush (under 5 working days notice) +30% · out-of-hours +50% · travel billed at half rate plus expenses
Minimum engagement: 2 days. Under that, a fixed 900 EUR audit.
```

```markdown
# Case study — Meridian reconciliation
*Read when proposing reconciliation, ledger or data-pipeline work. Approved for public use 2026-06-10, logo + anonymized metrics only.*

Problem → what was done → measured outcome (4 h → 35 min) → what the client said.
Portfolio rights: per MSA clause 14, metrics anonymized, no client data.
```

```markdown
# Decision — niche on payments reconciliation
*Read before changing what the practice sells, or when a wildly off-niche lead arrives. 2026-02-08.*

Decision: one sentence.
Rejected: staying generalist — sales cycle averaged 6 weeks against 2, and the win rate was half.
Cost: turns away roughly a third of inbound.
Revisit when: fewer than 3 qualified leads a quarter for two consecutive quarters.
```

If the engagement is tracked as a project, the one-line decision summary also belongs in `~/Clawic/data/projects/<project>.md`, with the full artifact staying here and referenced by name.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`engagements.md` — `## Engagements`, plus `## Ended` once closed rows outnumber active ones. This is the file that answers "what am I committed to, on what terms" without opening a contract.

`pipeline.md` — `## Pipeline`, plus `## Sources` (channel, opportunities produced, won, revenue). The source table is the reason this file exists: it is the only way to tell which channel deserves the next hour of selling.

`wins-losses.md` — `## Win/Loss`, plus `## Rate Ladder` (period, rate quoted, quotes sent, won, win rate). Without the ladder, every rate rise is relitigated from memory instead of from the last ten quotes.
