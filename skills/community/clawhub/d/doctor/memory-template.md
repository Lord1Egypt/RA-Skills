# Working File Templates — Doctor

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md`, the shared health box and everything they index is what you **observed** or produced. An observation never overwrites a declaration.

Everything here obeys `health_logging`: `full` writes all of it, `minimal` writes only allergies, conditions and current medicines in the shared profile, `off` writes nothing at all and says so once.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — table keys and preference areas alike | `~/Clawic/data/doctor/config.yaml` | Key by key, read-modify-write |
| Session state, current concerns, how they work, due dates, box index | `~/Clawic/data/doctor/memory.md` | Rewritten in place; stays small |
| Conditions, allergies, medicines, vaccines, screenings, measured values | `~/Clawic/data/health/profile.md` (**shared**) | One entry per condition, drug, allergy or vaccine; measurements append |
| A single metric measured in series once it passes ~15 entries | `~/Clawic/data/health/<metric>.md` (**shared**) | Append-only rows: date, value with unit, note |
| A dependent's or relative's health record | `~/Clawic/data/health/<kebab-name>.md` (**shared**) | Same headings as `profile.md`, one file per person |
| Clinicians, pharmacy, dentist, emergency contact | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, every source in one list |
| Appointments, procedures, scans | `~/Clawic/data/bookings/<year>.md` (**shared**) | One row per booking, cut by year |
| Health-insurance premium or plan | `~/Clawic/data/finances/subscriptions.md` (**shared**) | One row per subscription, amount with currency |
| A course of treatment the user runs as a project, with a goal and an end | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project; summary and milestones only, clinical detail stays here |
| Symptom episodes, injuries, falls, consultations and what came of them | `~/Clawic/data/doctor/episodes/<year>.md` | Append-only, cut by year |
| Things you produced that get re-read — action plans, sick-day plans, visit-prep sheets, safety plans, an emergency summary, a decision with its reasoning | `~/Clawic/data/doctor/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| **Anything durable this table does not name** | `~/Clawic/data/doctor/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

Three questions decide anything not listed: would another skill want to read it (→ a shared box) · is it a text read whole when its subject comes up (→ `artifacts/`) · is it one more row of something accumulating (→ a section of `memory.md` until the split threshold).

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A symptom was triaged, an injury assessed, a fall happened | A row in `episodes/<year>.md`, plus `## Current Concerns` while it is live |
| A diagnosis was given, or one was excluded | `## Conditions` in the shared profile, with the date |
| A medicine started, stopped, or changed dose | Its row in `## Medications`, updated in place |
| A reaction or allergy appeared | `## Allergies`, with the reaction described and the year |
| A result, reading or score was produced | `## Measurements`, or `health/<metric>.md` past the threshold |
| A screening or vaccine was done | `## Screenings` / `## Vaccines`, plus a `## Due` row for the next |
| An appointment was made, moved or cancelled | `~/Clawic/data/bookings/<year>.md` |
| A clinician was named for the first time | `~/Clawic/data/contacts/contacts.md` |
| A treatment course got a goal and an end date, or one of its milestones landed | `~/Clawic/data/projects/<project>.md` |
| A written plan came out of the session | `artifacts/` |
| A repeat date, review, refill or expiry was set | `## Due` |
| The user declared a preference | Its key in `config.yaml` |

## Start flat, split only when it hurts

Everything except artifacts, episode logs and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file, move the whole section into it, **delete the section from its origin**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the original copy is deleted.

The same procedure governs the shared health box: `## Measurements` in `profile.md` holds every metric until one of them passes ~15 entries, at which point that metric alone moves to `~/Clawic/data/health/<metric>.md` and `profile.md` keeps one index line.

Artifacts are the exception: an action plan, a safety plan or a decision is born as its own file whatever its size, because it is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. A pasted discharge letter, insurance document or portal export gets every secret value replaced **before** writing, and you say in one line that you did it. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`keychain:patient-portal` · `1password:Personal/Insurer` · `bitwarden:Health/Portal` · `env:HEALTH_API_TOKEN` · `file:~/Documents/insurance-card.pdf`

In this domain — **not secrets, keep them**: conditions and diagnoses, medicine names and doses, allergy names and reactions, test results with their units, clinician and clinic names, insurance plan name and member ID, appointment references, vaccine batch dates. **Secrets, strip them**: patient-portal and insurer logins and passwords, health-app API tokens, one-time codes, national identity or social-security numbers, full payment card numbers, and any password inside a pasted document.

Health data that is not a secret is still the most sensitive category this catalog stores. It stays on this machine, it is never copied into another skill's box, and nothing is deleted from it without saying which entry and why.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [shared health box](#shared-health-box) · [shared contacts](#shared-contacts) · [shared bookings](#shared-bookings) · [shared finances](#shared-finances) · [shared projects](#shared-projects) · [episodes/](#episodes) · [artifacts/](#artifacts) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/doctor/` if it does not exist.

```yaml
guideline_body: nice-uk
units: metric
glucose_units: mmol/L
lipid_units: mmol/L
emergency_number: "112"
care_context: gp-registered
detail_level: clinical
health_logging: full
screening_reminders: true

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
coverage:
  also_tracks: [mia, dad]        # each has a file in ~/Clawic/data/health/
restrictions:
  declines: [blood products]
  pregnancy_status: none
output_register: numbers-first
cadence:
  annual_review_month: 3
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Doctor Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Health profile (shared: conditions, allergies, 6 medicines) → `~/Clawic/data/health/profile.md`; read before naming any drug, dose or threshold
- Home blood pressure (34 entries) → `~/Clawic/data/health/blood-pressure.md`; read before any blood-pressure question
- Mia, 3 years (dependent) → `~/Clawic/data/health/mia.md`; read before any question about Mia
- Asthma action plan → `artifacts/action-plan-asthma.md`; read at the first sign of a flare
- Sick-day plan → `artifacts/sick-day-plan.md`; read during any illness with vomiting, diarrhoea or fever
- Emergency summary → `artifacts/emergency-summary.md`; read out to responders, and before travel
- Episodes 2026 (11) → `episodes/2026.md`; read when a symptom recurs or a timeline is needed

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| HbA1c | 6 months | 2026-04-02 | 2026-10-02 |
| Blood pressure review | 12 months | 2025-11-14 | 2026-11-14 |
| Cervical screening | 5 years | 2023-05-09 | 2028-05-09 |
| Flu vaccine | year, autumn | 2025-10-06 | 2026-10-05 |
| Adrenaline autoinjector expiry | — | — | 2027-01-31 |
| Medication review | 12 months | 2026-03-11 | 2027-03-11 |

## Current Concerns
Right calf ache since 2026-07-22, no swelling, walking normally — tripwire: swelling, warmth, or breathlessness → same day.

## How They Work
Wants the number and the mechanism, not reassurance. Health-anxious about cardiac symptoms after a family event in 2024 — name what has been excluded and how. Reads results before appointments.

## Care Team
GP: Dr Alvarez (see contacts) · Respiratory: Dr Kim (see contacts) · Pharmacy: High Street (see contacts)

---
*Updated: 2026-07-26*
```

Rules that keep this useful next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Screenings, vaccines, monitoring intervals, medication reviews, repeat tests, refills and rescue-medicine expiry dates all belong here. Only create rows when `screening_reminders` is true.
- **`## Current Concerns`**: what is live right now, with its tripwire. Cleared the moment it resolves, and the resolution goes into the episode row — a concerns list that only grows stops being read.
- **`## Care Team`**: names only, pointing at `contacts.md`. Never duplicate a clinician's contact details here.
- **`## How They Work`** is about communication, not clinical content: health literacy, what they want from an answer, known anxieties. Clinical facts belong in the shared profile.
- These headings are exactly the ones a split-out file inherits, so any future split stays a copy-paste.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still learning their history and how they want answers |
| `complete` | History, medicines and preferences are known |

## Shared health box

Lives at `~/Clawic/data/health/` and is shared with every other health-adjacent skill — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Health Profile

## Conditions
| Condition | Since | Status | Target / notes |
|---|---|---|---|
| Asthma | 2011 | active | Reliever ≤2 days/week; preventer daily |
| Hypertension | 2024-03 | active | Home average target <135/85 mmHg |

## Allergies
| Substance | Reaction | Year | Type |
|---|---|---|---|
| Penicillin | Widespread urticaria within 1 h | 2009 | allergy |
| Metformin | Diarrhoea | 2024 | intolerance |

## Medications
| Drug | Dose | Frequency | For | Prescriber | Since |
|---|---|---|---|---|---|
| Ramipril | 5 mg | daily | hypertension | Dr Alvarez | 2024-04 |
| Beclometasone inhaler | 200 µg | twice daily | asthma | Dr Kim | 2011 |

## Vaccines
| Vaccine | Date | Valid until |
|---|---|---|
| Tetanus/diphtheria | 2019-06-02 | 2029-06-02 |
| Influenza | 2025-10-06 | season |

## Screenings
| Screen | Date | Result | Next due |
|---|---|---|---|
| Cervical (HPV) | 2023-05-09 | negative | 2028-05-09 |

## Measurements
| Date | Metric | Value | Reference / target |
|---|---|---|---|
| 2026-07-14 | HbA1c | 41 mmol/mol (5.9%) | <42 |
| 2026-07-20 | Weight | 78.4 kg | — |
```

- **Identity is the entry name** — the condition, the drug, the allergen, the vaccine, the metric. Read the file before adding. If the entry is already there, **update the row in place**; only its absence justifies a new row. Two rows for the same drug is how a dose gets read wrong.
- **A stopped medicine keeps its row** with `stopped <date> — <reason>` until the next medication review, then moves to a `## Past Medications` heading. Deleting it loses the reason.
- **Every value carries its unit inside the value** (`78.4 kg`, `41 mmol/mol`, `132/84 mmHg`), because another skill will read this file and no unit can be assumed. Amounts of money carry their currency the same way.
- **Scale cut**: `## Measurements` holds every metric until one metric alone passes ~15 entries; that metric moves to `~/Clawic/data/health/<metric>.md` with the columns `Date | Value | Note`, the section keeps one index line, and the moved rows are deleted here. If you arrive and the folder already has per-metric files, follow that — do not start a parallel list.
- **Dependents**: one file per person at `~/Clawic/data/health/<kebab-name>.md`, opening with `# Health — <Name>` and carrying the same headings as `profile.md`. The person also gets a row in `contacts.md`. Never merge two people's data into one file.
- **The folder is flat, so two naming conventions share it**: `<metric>.md` (a series, `| Date | Value | Note |`, split out of `## Measurements`) and `<kebab-name>.md` (a person, `# Health — <Name>` plus the profile headings). The first line of the file says which it is — read it before writing, and follow what is already there. Never convert one kind into the other. When a person's name would collide with a metric name, or when a dependent's own metric splits out, the file is `<kebab-name>-<metric>.md`; the person file keeps the index line. The user's own record is always `profile.md`, never a name file.
- **Foreign columns win.** If a file already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- **Retirement**: a condition that was excluded or resolved gets `resolved <date>` rather than deletion — "we already ruled that out" is the most useful sentence in a future consultation.

## Shared contacts

```markdown
# Contacts

| Name | Key | Role | Preferred channel | Context | Last contact | File |
|------|-----|------|-------------------|---------|--------------|------|
| Dr Alvarez | dr-alvarez-southside | GP | phone | Registered practice, hypertension and asthma | 2026-06-12 | — |
```

- **Identity is `Key`**: lowercase email if there is one, else a handle, else `<kebab-name>` plus a stable disambiguator. It is a column of the row, never implicit.
- Read before adding; if the key exists, update in place. `Role` carries the specialty — GP, cardiologist, pharmacy, dentist, emergency contact.
- **Scale cut**: past 15 people, or as soon as one no longer fits its row, each gets `~/Clawic/data/contacts/<name>.md` and `contacts.md` becomes the index with the `File` pointer.
- **Retirement**: only rows this skill created are edited or removed. A clinician no longer involved has their row updated, not deleted, unless the user asks; when the user does ask, the row goes and the date is noted in `memory.md`.
- **Foreign columns win.** If `contacts.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.

## Shared bookings

```markdown
# Bookings — 2026

| Date | Type | Locator | Provider | Status | Notes |
|------|------|---------|----------|--------|-------|
| 2026-08-04 09:20 | medical | southside-2026-08-04 | Southside Clinic | confirmed | Asthma review, bring peak-flow diary |
```

- **Identity is the locator.** When the clinic gives none, use `<provider-kebab>-<date>` so the same appointment is never entered twice.
- Cut by year. Past ~60 rows in a year, split by quarter into `bookings/<year>-q<n>.md` and leave `<year>.md` as the index table.
- A cancelled appointment keeps `status: cancelled` with its reason until the end of the following year.
- Foreign columns win, exactly as above.

## Shared finances

Only one thing from this domain belongs here: the health-insurance premium or plan, as a row in `~/Clawic/data/finances/subscriptions.md` — `Name | Amount with currency | Cycle | Renewal | Notes`.

- **Identity is the subscription name.** Read the file before adding; if the name is already there, update the row in place. Two rows for one policy is how a premium gets counted twice.
- **Retirement**: when the policy ends, the row is deleted and the date noted in `memory.md` — this table is a live list of what is being paid, not a history.
- **Scale cut**: none. `subscriptions.md` stays a single table precisely because retirement deletes rows; never split it by year or provider.
- **Every amount carries its currency inside the value** (`64 EUR`, not `€64`), because other skills sum this file and no currency can be assumed. An estimate carries the date it was estimated.
- **Foreign columns win.** If the file already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- The member ID may live in the notes as working data; the portal login never does.

## Shared projects

Only when the user is already running a course of treatment as a project — a fertility cycle, a transplant workup, a rehab programme, a weight-loss or smoking-cessation course with a target date. A one-off appointment or a chronic condition is not a project; it stays in the health box.

```markdown
# Knee rehab after ACL repair
status: active
started: 2026-06-02
goal: Return to running by 2026-12, full pivot sport by 2027-03
owner: self

## Milestones
| Date | Milestone | Done |
|---|---|---|
| 2026-07-15 | Full passive extension | yes |
| 2026-09-01 | Single-leg hop symmetry >90% | — |

## Decisions
- 2026-06-10 — physio-led over surgeon-led protocol; both offered, physio has weekly slots.

Clinical detail: `~/Clawic/data/doctor/episodes/2026.md`, `artifacts/rehab-plan-acl.md`.
Clinicians: `~/Clawic/data/contacts/contacts.md` — keys `dr-kim`, `physio-nuria`.
```

- **Identity is the project name**, which is the filename slug — one `.md` per project at `~/Clawic/data/projects/<project>.md`, from the first one. Read the folder before creating: if a file for this project already exists, **update it in place**; a second file for the same project is how two skills end up describing different states of one thing.
- **Only the summary lives here.** Symptoms, results, doses and episodes stay in the health box and in `~/Clawic/data/doctor/`, and the project file points at them by path. Duplicating the clinical detail is how the two copies start disagreeing; people are named by their `contacts.md` key, never re-described here.
- **Retirement**: a finished or abandoned project gets `status: done | cancelled — <date>` inside the file and is never deleted — the record of what was done is the whole point.
- **Scale cut**: past ~20 closed projects, move them to `~/Clawic/data/projects/archive/<project>.md` without renaming the file.
- **Foreign columns win.** If the project file or folder already follows another shape — different headings, a different milestone table — match what is there and add anything missing at the end. Never rewrite its structure.
- Its `## Boxes` line goes in `memory.md` in the same turn, with the read condition "read before any question about <project>".

## episodes/

```markdown
# Episodes — 2026

| Date | Who | Complaint | Findings / discriminators | Rung | Tripwire | Outcome |
|------|-----|-----------|---------------------------|------|----------|---------|
| 2026-07-22 | self | Right calf ache | No swelling, no warmth, walked 5 km day before | self-care | swelling, warmth, breathlessness → same day | resolved 2026-07-25 |
| 2026-06-03 | Mia | Fever 39.1 °C, 3 y | Alert, drinking, no rash, RR 28 | same day | — | Viral, settled day 4 |
```

- One row per episode. `Who` is `self` or the dependent's name, matching their health file.
- The `Outcome` column is filled in later — an episode with no outcome is the one that teaches nothing.
- Append-only, cut by calendar year. Never delete an old year: recurrence patterns are the whole value.

## artifacts/

One file per thing, at `~/Clawic/data/doctor/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **action plan** (asthma, COPD, migraine, allergy), **sick-day plan**, **safety plan**, **emergency summary**, **visit-prep sheet**, **a decision with its reasoning**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Asthma action plan
*Read at the first sign of a flare. Agreed with Dr Kim, 2026-05-18.*

Green — peak flow above 420, reliever ≤2 days/week: preventer twice daily, no change.
Amber — peak flow 300-420, or reliever needed daily: <the step-up agreed with the clinician>, review within 48 h.
Red — peak flow below 300, cannot speak a full sentence, reliever not lasting 4 h: emergency now.
```

```markdown
# Emergency summary
*Read out to responders, and before travel. Updated 2026-07-26.*

Conditions: asthma, hypertension.
Medicines: ramipril 5 mg daily; beclometasone 200 µg twice daily; adrenaline autoinjector 0.3 mg (expires 2027-01).
Allergies: penicillin — urticaria within 1 h, 2009.
Emergency contact: see `~/Clawic/data/contacts/contacts.md`, key `marta-ruiz`.
```

```markdown
# Decision — declined statin for now
*Read before any lipid discussion. 2026-02-09.*

Decision: lifestyle first, recheck in 6 months.
Numbers at the time: LDL 3.4 mmol/L, 10-year risk 6%.
Rejected: immediate statin — risk below the treatment threshold in use, and the user wanted a trial period.
Review: 2026-08-09 (row in `## Due`).
```

If the user tracks a course of treatment as a project, the summary also belongs in the shared projects box — protocol under [shared projects](#shared-projects) above; the clinical detail stays here and is referenced by path.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside its origin.

`~/Clawic/data/health/<metric>.md` — `| Date | Value | Note |`, one metric per file, values carrying their unit. This is the usual first split, because home blood pressure and weight cross 15 entries quickly.

`~/Clawic/data/doctor/concerns.md` — only if `## Current Concerns` ever holds more than about 15 live items, which for most people means never. Same heading, same shape.
