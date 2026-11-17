# Working File Templates — Coach

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — table keys and preference areas alike | `~/Clawic/data/coach/config.yaml` | Key by key, read-modify-write |
| Current focus, open commitments, patterns, boundaries, cadences, box index | `~/Clawic/data/coach/memory.md` | Rewritten in place; stays small |
| People — clients, sponsors, referral partners, the person's own coach | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, every context in one file |
| A coaching client's engagement: goal, contract, history, progress | `~/Clawic/data/coach/clients/<name>.md` | One file per client from the first; index at `clients/roster.md` past 5 |
| Session records | `~/Clawic/data/coach/sessions/<year>.md` | Append-only, cut by year, then by quarter past ~40 |
| Things the user re-reads whole — 90-day plan, values list, wheel-of-life baseline, coaching agreement, discovery-call script, a decision and its reasoning, a session-prep brief, a program outline | `~/Clawic/data/coach/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| The practice: rates, packages, capacity, pipeline, churn | `## Practice` in `memory.md` while it is short; `~/Clawic/data/coach/business.md` after | One block, rewritten in place |
| A paid engagement or a client initiative tracked as work | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project |
| A body metric the coaching goal is measured by | `~/Clawic/data/health/profile.md`, or `health/<metric>.md` in series (**shared**) | Metric + date |
| A coaching subscription or retainer the user **pays** | `~/Clawic/data/finances/subscriptions.md` (**shared**) | One row, amount with currency |
| **Anything durable this table does not name** | `~/Clawic/data/coach/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |
| What a client disclosed that triggered a referral | Nowhere | Record the fact and date of the referral, never the content |

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A commitment was made | `## Commitments`, with action, date, observable |
| A commitment was kept, missed, or renegotiated | Its row's verdict, and the resize if Rule 5 applied |
| A session was held | `sessions/<year>.md` at `notes_detail`, plus `## Status` |
| A goal was set, revised, split, or dropped | `## Focus` — and the 90-day plan to `artifacts/` |
| A recurring pattern or limiting belief was named across sessions | `## Patterns` |
| A new client, chemistry call, or engagement started | `clients/<name>.md` + the person's row in `contacts.md` |
| A contract term, rate, cadence, or renewal date was agreed | `clients/<name>.md`, and `## Due` for the date |
| A referral was made, or a boundary was drawn | `## Boundaries` — fact and date only |
| A progress marker or a mid-engagement review happened | `clients/<name>.md` (advise) or `## Focus` (act-as), plus `## Due` |
| Pricing, packages, capacity, or churn changed | `## Practice` |
| Supervision, a recorded-session review, or credential hours | `## Craft Log` + `## Due` |
| Recurring work was scheduled or run | `## Due` |
| The user declared a preference | Its key in `config.yaml` |

## Start flat, split only when it hurts

Everything except client files, session records, artifacts and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/coach/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Named splits, so two sessions crossing the threshold months apart produce the same file: `## Commitments` → `commitments.md` · `## Patterns` → `patterns.md` · `## Practice` → `business.md` · `## Craft Log` → `craft-log.md`. A closed commitment older than the current `horizon_days` is archived into the same file, never deleted — the kept/missed history is what makes Rule 5 possible.

Client files, session records and artifacts are the exception: each is born as its own file whatever its size, because it is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`env:CALENDLY_TOKEN` · `keychain:coaching-portal` · `1password:Work/Practice/stripe` · `bitwarden:Personal/Zoom` · `file:~/.config/invoicing/creds` · `profile:practice`

When the user pastes something to save — a client intake form, a portal export, an invoicing config — replace each secret value before writing and leave the pointer visible: `api_key: <env:CALENDLY_TOKEN>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: client names and the contact key, session dates and counts, goals and commitments, rates and package prices with their currency, cadences, credential hours, referral partner names, engagement start and end dates. **Secrets, strip them**: portal and calendar API tokens, video-call host keys and meeting passcodes, payment-processor keys, client passwords or logins shared "so you can check", anything from a client's `.env`, and recording-storage credentials.

**Sensitive but not secret, and still not stored**: what a client disclosed in distress. The Red Flags table produces one line — "referred to a clinician, 2026-07-26" — and nothing else. A coaching file is not a clinical record and must not read like one.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [shared contacts](#shared-contacts) · [clients/](#clients) · [sessions/](#sessions) · [artifacts/](#artifacts) · [shared projects](#shared-projects) · [shared health](#shared-health) · [shared finances](#shared-finances) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/coach/` if it does not exist.

```yaml
mode: advise
session_model: grow
session_length_min: 60
checkin_cadence: weekly
commitment_cap: 2
challenge_level: direct
advice_mode: hybrid
horizon_days: 90
notes_detail: full
niche: executive

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
tooling:
  commitments_live_in: "their task app; this file holds the verdict only"
  recording: "consented, deleted after review"
cadence:
  checkin_day: monday
  supervision: monthly
practice_model:
  pricing: package
  cancellation_window_hours: 24
ethics:
  sponsor_receives: "themes and attendance only, never content"
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Coach Memory

## Status
status: ongoing
mode: act-as
last session: 2026-07-24 (#11)

## Boxes
- Clients (7) → `clients/roster.md`; read before any client-specific question
- Sessions 2026 (23) → `sessions/2026.md`; read before a session, for the last two entries
- 90-day plan, Q3 → `artifacts/plan-q3-2026.md`; read at any goal or commitment review
- Values list → `artifacts/values-2026.md`; read when a decision or a goal feels borrowed
- Commitment history (41) → `commitments.md`; read before designing a new commitment

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Check-in on open commitments | week, Monday | 2026-07-20 | 2026-07-27 |
| Session | 2 weeks | 2026-07-24 | 2026-08-07 |
| 90-day review | quarter | 2026-04-15 | 2026-07-15 |
| Talk-ratio review on a recording | month | 2026-07-02 | 2026-08-02 |

## Focus
Goal (to 2026-10-15): ship the paid beta. Outcome they do not control: 20 paying users.
Process they do control: 4 customer conversations a week, one release every Friday.
Why, in their words: "I want to stop being someone who plans things."

## Commitments
| Made | Action | Due | Observable | Verdict | Size |
|------|--------|-----|-----------|---------|------|
| 2026-07-24 | 4 customer calls | 2026-07-31 | calls in the calendar | open | repeating |
| 2026-07-10 | Send the pricing email to Dana | 2026-07-12 | sent | kept | conversation |
| 2026-06-26 | Ship the onboarding fix | 2026-07-03 | merged | missed ×2 → halved to "open the PR" | mva |

## Patterns
Deadlines move after conversations with their manager (3rd time, 2026-07-24). Named, not interpreted.
Plans in detail when the next step is a conversation. Research is the avoidance tell.

## Boundaries
2026-05-12: referred to a clinician for sleep and mood; coaching continued on the work goal only.

## Practice
Packages: 3-month, 6 sessions, biweekly. Active clients 7, ceiling 12 (see business capacity formula).

## Craft Log
2026-07-02: recording review, talk ratio 38% — too high in Options. Watching for it.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Every cadence this skill agrees to belongs here: check-ins, sessions, reviews, re-contracting, renewal conversations, supervision, recording reviews.
- **`## Commitments`**: one row per commitment, never rewritten when it closes — the verdict column is the history Rule 5 needs. `Size` is the class from the Commitment Design table. A commitment with no `Observable` is an intention: write it with `Observable: none` so the pattern is visible, and do not count it in a streak.
- **`## Patterns`**: only what is observable and repeated, with the count and the date of the latest instance. A theory about *why* is marked as yours ("my read:") or not written.
- **`## Boundaries`**: fact and date. No content, ever.
- These headings are exactly the ones the split-out files get, so a split stays a copy-paste.

| Status | Meaning |
|-------|---------|
| `ongoing` | Engagement or self-coaching in progress |
| `paused` | Agreed break with a return date in `## Due` |
| `complete` | Exit condition met; the file stays as the record |

## Shared contacts

Lives at `~/Clawic/data/contacts/contacts.md` and is shared with every other skill that deals with people — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Contacts

| Name | Key | Role | Preferred channel | Context | Last contact | File |
|------|-----|------|-------------------|---------|--------------|------|
| Dana Ruiz | dana@acme.example | coaching client | email | exec coaching, sponsor is Acme L&D | 2026-07-24 | clients/dana-ruiz.md |
```

- **Identity is `Key`**, and it is a column of the row, never implicit: lowercased email first; no email → handle; neither → `<kebab-name>` plus a stable disambiguator (`ana-lopez-acme`). `Preferred channel` is the *type* of channel (email, phone, WhatsApp), not the address, so it can never serve as the key.
- Read the file before adding and search for the key. If it is there, **update that row in place** — one person is one row whether they arrived as a client, a friend, or a recruiter. Only absence justifies a new row.
- **You own only the rows you wrote.** Never rewrite a row another skill created; add what is missing to `Context` and leave the rest.
- **Ending a relationship is part of the record.** When an engagement ends, keep the row and update `Context` (`former client, ended 2026-09`); delete the row only when the person is gone from the user's life entirely, and note the deletion date in `## Boundaries`.
- **Scale cut**: one row per person while there are ≤15. Past that, one file per person at `~/Clawic/data/contacts/<name>.md` with the same fields, and `contacts.md` becomes the index with the `File` pointer. If you arrive and the folder already looks like that, follow it — do not start a parallel `contacts.md`.
- **Foreign columns win.** If `contacts.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- The `File` column points at the coaching file; the coaching material itself never goes in `contacts.md`.

## clients/

One file per coaching client, at `~/Clawic/data/coach/clients/<name>.md`, created at the chemistry call — before the first paid session, because the fit notes are what you re-read if it goes wrong.

```markdown
# Dana Ruiz — executive coaching
*Read before any session with Dana, and before any renewal or sponsor conversation.*

Contact: Dana Ruiz (see contacts). Sponsor: Acme L&D (see contacts). Started 2026-04-02.
Contract: 6 sessions, biweekly, 60 min. Ends 2026-09-30. Renewal decision 2026-09-16.
Fee: 2400 EUR for the package, invoiced monthly. Cancellation: 24h.
Sponsor receives: attendance and themes. Content stays private — stated at intake.

## Engagement goal
Delegate the technical review she still does herself. Baseline 2026-04-02: doing 100% of reviews.
Success as she defined it: "my team ships without me in the loop and I stop working Sundays."

## Baseline and markers
| Marker | Baseline | Now | Read on |
|--------|----------|-----|---------|
| Reviews she personally does | 100% | 40% | 2026-07-24 |
| Confidence delegating (0-10) | 3 | 6 | 2026-07-24 |

## Commitments
Same columns as `## Commitments` in memory.md.

## Patterns
Observable, counted, dated.

## Boundaries
Fact and date only.
```

- **Scale cut**: one file per client from the first. Past 5 active clients, add `~/Clawic/data/coach/clients/roster.md` — `Name | Focus | Cadence | Status | Next session | → file` — and collapse the per-client lines in `## Boxes` into one line pointing at the roster.
- A former client's file is never deleted: set `status: ended <date>` at the top. It is the record of what was delivered, and the source of a testimonial or a return engagement.
- The person's identity lives in `contacts.md`. Never duplicate their email, phone, or role here.

## sessions/

```markdown
# Sessions — 2026

| # | Date | Client | Min | Contracted outcome | What moved | Commitments set | Talk ratio |
|---|------|--------|-----|--------------------|-----------|-----------------|-----------|
| 23 | 2026-07-24 | Dana | 60 | "decide about the Friday review" | named the fear of being cut out | 1 (conversation) | 31% |
```

- Cut by year. Past ~40 rows in one year, split into `sessions/<year>-q<n>.md` and leave `<year>.md` as an index (`# | Date | Client | → file`).
- At `notes_detail: brief` the row is the whole record. At `full`, add a short block under the table with the client's own words for the outcome and the takeaway — their words, not your paraphrase. At `none`, still write the row: date, commitments set, verdict on the previous ones.
- `Talk ratio` only when the session was recorded or transcribed. Blank beats a guess.

## artifacts/

One file per thing, at `~/Clawic/data/coach/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **90-day plan**, **values list**, **wheel-of-life baseline**, **coaching agreement**, **discovery-call script**, **decision and its reasoning**, **session-prep brief**, **group or program outline**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# 90-day plan — Q3 2026
*Read at every commitment review, and before setting a new goal. Written 2026-07-15.*

Outcome (not controlled): 20 paying users by 2026-10-15.
Process (controlled): 4 customer calls/week, one release every Friday.
Identity: "someone who ships weekly".
Checkpoints: 2026-08-15, 2026-09-15. Review date is in `## Due`.
Abandon condition: if the process ran for 6 weeks and the outcome moved 0, the goal is wrong, not the effort.
```

```markdown
# Decision — end the Acme engagement at session 6
*Read before any renewal conversation with Acme. 2026-07-26.*

Decision: no renewal offered; recommend an internal mentor instead.
Why: the goal is capability, not action — training, not coaching (SKILL.md, Coaching Vs Adjacent Crafts).
Rejected: extending three sessions; it would have sold time against a gap coaching does not close.
```

If the engagement is tracked as paid work, the decision summary also belongs in the shared `~/Clawic/data/projects/<project>.md`, with the detail staying here and referenced by name.

## Shared projects

`~/Clawic/data/projects/<project>.md`, one file per project, shared with every skill that tracks work. Use it when a coaching engagement is a paid piece of work, or when the client's own initiative is what the sessions are steering.

- Identity is the project name (the file slug). Read the folder before creating; if the project is there, add to it rather than starting a second file.
- Retiring a project: `status: done | cancelled — <date>` inside the file. Never delete it — it is the record of what was delivered. Past ~20 closed, move to `projects/archive/<project>.md` without renaming.
- Keep it to objective, status, milestones and decisions. Session-level material stays in `clients/` and `sessions/`; duplicating it here is how two skills end up contradicting each other.
- Amounts carry their currency in the value (`2400 EUR`), never a bare number or a symbol.

## Shared health

`~/Clawic/data/health/`, shared with every health and fitness skill. Only when the coaching goal is measured by a body metric.

- Stable context — conditions, allergies, medication — goes in `profile.md`. A metric measured in series (weight, resting heart rate, sleep hours) goes in `profile.md` until ~15 entries, then to `health/<metric>.md` with `profile.md` keeping its index line.
- Identity is metric + date. Every value carries its unit (`78 kg`, `7.5 h`), because the file is shared with skills that assume the other system.
- Read before writing; if a fitness or nutrition skill already owns the series, append in its format and never rewrite its header.
- The commitment lives in `## Commitments` here; the measurement lives there. Do not copy the series into the coaching files.

## Shared finances

`~/Clawic/data/finances/`, shared with every money skill. One direction only: money the user **pays**.

- A coaching retainer or subscription the user pays is a row in `subscriptions.md`: `Name | Amount with currency | Cycle | Started | Renews | Notes`. Identity is the subscription name; update in place, and delete the row when it ends.
- Fees the user **charges** are not a subscription: they live in `clients/<name>.md` and, in aggregate, in `## Practice`.
- Amounts always carry the currency inside the value (`300 EUR/month`), never `€300`. Estimated figures carry the date of the estimate.
- Foreign columns win: match the file's existing header, add anything missing as a trailing note.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`commitments.md` — `## Commitments`, the full history including closed rows. This file is the reason Rule 5 works: without the kept/missed record, every miss looks like the first one.

`patterns.md` — `## Patterns`, one block per pattern with its count and latest date.

`business.md` — `## Practice`: rates and packages with currency, active clients, capacity, pipeline, churn, and the capacity arithmetic from `practice.md`.

`craft-log.md` — `## Craft Log`: recording reviews with the measured talk ratio, supervision dates and what came out of them, credential hours as a running total with the date each block was added.
