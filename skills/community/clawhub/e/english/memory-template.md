# Working File Templates — English

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — Configuration table keys and preference areas alike | `~/Clawic/data/english/config.yaml` | Key by key, read-modify-write |
| The user's own long-form English sample (`voice_file`) | `~/Clawic/data/english/voice-sample.md`, its path recorded in `config.yaml` | Replaced whole, never appended to |
| Level, focus, registers in use, how they work, due dates, box index | `~/Clawic/data/english/memory.md` | Rewritten in place; stays small |
| Error classes and the one-line rule that fixes each | `## Recurring Errors` in `memory.md`; `~/Clawic/data/english/errors.md` once it outgrows the section | One row per class, never per sentence |
| Chunks: collocations, phrasal verbs, idioms, and words with a pronunciation target | `## Vocabulary` in `memory.md`; `~/Clawic/data/english/vocabulary.md` once it outgrows the section | One row per chunk |
| Phrasings the user approved, keyed by situation | `## Phrasebook` in `memory.md`; `~/Clawic/data/english/phrasebook.md` once it outgrows the section | One row per situation |
| Domain terms and their agreed English rendering | `## Glossary` in `memory.md`; `~/Clawic/data/english/glossary.md` once it outgrows the section | One row per term |
| People, and the register that works with each | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, every skill writing into one inventory |
| A tracked piece of work whose English decisions matter | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project; this skill adds one line to it |
| Things you produced that get re-read — the house style sheet, a speech or talk script, a template set, a level report | `~/Clawic/data/english/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| Practice sessions, call debriefs, batched spoken corrections | `~/Clawic/data/english/sessions/<year>.md` | Append-only, cut by year |
| **Anything durable this table does not name** | `~/Clawic/data/english/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials, and any secret inside a text the user pasted | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

Deciding where something unnamed goes, in this order: (1) would another skill want to read it — a person, a project, a booking, a contact's preferred channel? Then it belongs in the shared box, not here. (2) Is it a text read whole when its subject comes up — a style sheet, a speech, a set of templates, a written assessment? Then `artifacts/`, its own file from the first one. (3) Is it one more row of something that accumulates? Then a section of `memory.md` until the split threshold.

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| The same correction appeared a second time | Its class row in `## Recurring Errors` (SKILL.md Rule 8) |
| Three consecutive clean uses of a class in the journal | Strike that row and date the retirement |
| A chunk was taught, asked about, got wrong, or was rejected as "not me" | Its row in `## Vocabulary`, with the register tag |
| A word or a name got a pronunciation target | The `Say it` column of its `## Vocabulary` row |
| The user approved a phrasing they will reuse | Its row in `## Phrasebook`, keyed by situation, never by date |
| A domain term got an agreed rendering, or an alternative was rejected | Its row in `## Glossary`, with the rejected form beside it |
| The rung, greeting or bottom-line-first habit that works with a named person was learned | The `Context` column of their row in `contacts.md` (shared); the pattern across people in `## Registers In Use` |
| A variety, spelling-system, punctuation or house-style question was settled | `config.yaml` if it is a table key; otherwise `artifacts/style-sheet.md` |
| The user vetoed a word or phrase outright | `banned_words` in `config.yaml` |
| A practice session, a call debrief, or a batch of spoken corrections happened | A dated row in `sessions/<year>.md`, errors also fed to `## Recurring Errors` |
| A level was assessed, or the focus skill changed | `## Progress`, plus the written assessment in `artifacts/` if it runs long |
| A speech, a template set, or a style sheet was produced | `artifacts/`, with its `## Boxes` line in the same turn |
| A review or practice cadence was agreed or run | `## Due` |
| The user declared a preference | Its key in `config.yaml` |

## Start flat, split only when it hurts

Everything except artifacts, session records and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/english/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Artifacts are the exception: a style sheet, a speech or a template set is born as its own file whatever its size, because it is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. Language work is fed on pasted text, and an email thread, a support transcript, a CV, a contract clause or a `.env` in a code comment is where the secret arrives. Strip each value **before** writing and leave its pointer where the value was, in this shape: `<kind>:<locator>`.

`env:SMTP_PASSWORD` · `keychain:work-mail` · `1password:Work/Mail` · `bitwarden:Personal/Bank` · `vault:secret/team/mail` · `profile:work` · `file:~/.ssh/id_ed25519`

In a text, the pointer goes where the value was: `password: <keychain:work-mail>`. Say in one line that you did it. A password-reset link, a one-time code and a signed download URL are secrets even though they look like ordinary sentences — the pointer replaces the whole URL.

In this domain — **not secrets, keep them**: names, job titles, company and product names, email addresses used as contact keys, phone country codes, domain names, document titles, invoice and ticket numbers, dates, and the wording of anything the user wrote themselves.

**Secrets, strip them**: passwords and app passwords, password-reset and magic-sign-in links, one-time codes and 2FA seeds, API keys and tokens pasted inside a text being corrected, full card and IBAN numbers, national ID and passport numbers, home addresses when the text is a template rather than a real letter, and anything the user calls confidential.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [shared contacts inventory](#shared-contacts-inventory) · [shared projects](#shared-projects) · [artifacts/](#artifacts) · [sessions/](#sessions) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/english/` if it does not exist.

```yaml
variety: en-GB
spelling_system: oxford-ize
register_default: neutral
first_language: Spanish
oxford_comma: true
correction_mode: explained
max_sentence_words: 25
banned_words: ["reach out", "leverage", "utilize", "delve"]
voice_file: voice-sample.md
review_cadence: monthly

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
conventions:
  title_style: sentence-case
  dates: ISO            # 2026-07-26, whatever the variety
  lists: no-terminal-period
variety_detail:
  keep_american: [product UI strings]
output_register:
  show: corrected-text-then-rule
  emoji: none
learning_focus: [writing, speaking]
correction_posture:
  spoken: batch-after
  in_front_of_others: never
```

If you find a preference recorded in `memory.md`, move it here and note the move. Long texts never live in this file: `voice_file` holds a filename, and the sample itself is `~/Clawic/data/english/voice-sample.md`.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# English Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Chunks and pronunciation targets (23) → `vocabulary.md`; read before teaching a word, a collocation or a sound
- House style sheet → `artifacts/style-sheet.md`; read before settling any mechanics, variety or word-choice question
- Best-man speech → `artifacts/speech-best-man.md`; read whenever that speech comes up again
- Client email templates → `artifacts/templates-client-email.md`; read before writing to a client
- Practice and call debriefs (2026) → `sessions/2026.md`; read before a review session or a level check

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Error-journal review | month | 2026-06-28 | 2026-07-28 |
| Vocabulary review (chunks added since last) | week | 2026-07-20 | 2026-07-27 |
| Speaking session, corrections batched | week | 2026-07-19 | 2026-07-26 |

## Recurring Errors
| Class | Rule in one line | First seen | Count | Last |
|-------|------------------|------------|-------|------|
| Article before an abstract generalization (*the life is hard*) | No article when the noun means all of it: "life is hard" | 2026-05-02 | 7 | 2026-07-24 |
| *I am agree* | "agree" is the verb; no "be" — "I agree" | 2026-05-11 | 3 | 2026-06-30 |
| Present perfect with a closed time (*I have seen him yesterday*) | A finished time expression forces the past simple | 2026-06-14 | 2 | 2026-07-18 |
| Retired 2026-07-02: *make a photo* → *take a photo* (3 clean uses) | | | | |

## Vocabulary
| Chunk | Register | Say it | Status | Added |
|-------|----------|--------|--------|-------|
| reach a decision | neutral | — | acquired | 2026-05-20 |
| touch base | business, dated | — | rejected — "sounds corporate" | 2026-06-02 |
| thorough | any | THUR-uh (not "true") | drilling | 2026-07-10 |
| get round to it | casual, en-GB | — | new | 2026-07-24 |

## Phrasebook
| Situation | The line they approved | Notes |
|-----------|------------------------|-------|
| Decline a meeting | "Can't make this one — send me the notes?" | rung 2, internal only |
| Chase an invoice, second attempt | "Following up on invoice 118 — anything you need from me?" | rung 3, no apology |
| Interrupt in a call | "Sorry, can I jump in there?" | used successfully 2026-07-19 |

## Glossary
| Term (source) | Agreed English | Rejected | Why |
|---------------|----------------|----------|-----|
| pedido | order | request | "request" reads as a support ticket |
| responsable de zona | area manager | zone responsible | calque; nobody says it |

## Registers In Use
Writes at rung 3 by default, rung 2 in team chat, holds rung 4 with the Acme client. Cuts "I hope this email finds you well" on sight. Per-person detail lives in `contacts.md`, not here.

## Progress
Self-assessed B2, reads at C1, speaking lags writing by a level. Current focus: articles, /θ/ vs /s/, interrupting in meetings. Target: write client email with no review by end of year.

## How They Work
Spanish L1, en-GB for work and en-US for the product UI. Wants the corrected text first and the rule in one line, never a lesson. Will not accept idioms they consider "TV English".

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Every cadence this skill schedules belongs here, and the cadences come from `review_cadence` and the `cadence` area of `config.yaml` when the user has declared them.
- **`## Recurring Errors`**: a row is a *class* with a rule, never a corrected sentence — one row covers every future instance. `Count` is what decides whether to restate the rule or just tick it. Retirement is part of the journal: three consecutive clean uses strikes the row with its date, and a struck row stays visible for one review cycle so a relapse is legible.
- **`## Vocabulary`**: store the whole chunk, never the bare word — "decision" is useless without "reach/make/take a decision". `Status` is one of `new` · `drilling` · `acquired` · `rejected`, and a rejected chunk keeps its row with the reason, because the point of the row is that it never gets suggested again. `Say it` is a respelling, not IPA, unless the user reads IPA.
- **`## Phrasebook`**: keyed by situation ("decline a meeting"), never by date, or it becomes a diary nobody searches. Only lines the user actually approved or used.
- **`## Glossary`**: the rejected alternative goes in the same row. Without it the same term is re-argued every quarter.
- **`## Registers In Use`**: the pattern across people. A specific person's rung, greeting and preferences belong to their row in `contacts.md` — one home per fact, and that home is the shared one.
- These headings are exactly the ones `errors.md`, `vocabulary.md`, `phrasebook.md` and `glossary.md` get when their sections outgrow this file, so each split stays a copy-paste.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still learning their English, their varieties and their people |
| `complete` | Know their level, house style and regular readers well |

## Shared contacts inventory

Lives at `~/Clawic/data/contacts/contacts.md` and is shared with every skill that deals with people — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Contacts

| Name | Key | Role | Preferred channel | Context | Last contact | File |
|------|-----|------|-------------------|---------|--------------|------|
| Marta Ruiz | marta.ruiz@acme.com | Acme, procurement | email | rung 4, "Dear Marta", bottom line first, no idioms — she reads in her L2 | 2026-07-22 | — |
| Sam Okafor | sam-okafor | teammate | chat | rung 2, first names, fine with fragments and swearing | 2026-07-25 | — |
```

- **Identity is `Key`**, in this order: lowercase email, else the handle they are known by, else `<kebab-name>` with a stable disambiguator (`sam-okafor-acme`). The key is a column of the row — never implicit, never left to the filename. `Preferred channel` is the *type* of channel, not an address, so it can never serve as the key.
- **Read the file before adding.** If the key is already there, update the row in place; only its absence justifies a new row. Never rewrite a row another skill wrote — add what you learned to `Context` and leave the rest alone.
- **What this skill contributes** is the `Context` column: the rung that works, the greeting they use, whether they want the bottom line first, what they reacted badly to. Keep it to one clause per fact.
- **Removal is on request only.** A person the user no longer deals with keeps their row — the context is the value. When the user asks for someone to be removed, delete the row and note the date in `memory.md`.
- **Scale cut**: one row per person while there are ≤15, or until a person no longer fits in one row. Past that, one file per person at `~/Clawic/data/contacts/<name>.md` with the same fields, and `contacts.md` becomes the index with the `File` column filled in. If you arrive and the folder already looks like that, follow it — never start a parallel `contacts.md`.
- **Foreign columns win.** If `contacts.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- No addresses, no passwords, no answers to security questions. A mailbox credential is a pointer or it is nowhere: `keychain:work-mail`.

## Shared projects

Lives at `~/Clawic/data/projects/<project>.md`, one file per project from the first, shared with every skill that touches the same work. This skill writes **one line** into it — the English decisions that anyone else on that project would need:

```markdown
English: en-GB, Oxford spelling, sentence case, ISO dates. Style sheet and glossary in `~/Clawic/data/english/artifacts/style-sheet.md`.
```

- **Identity is the project name**, which is the filename slug. Read the file before writing; if an `English:` line is already there, replace it, never add a second.
- **Never duplicate the style sheet or the glossary here** — the project file carries the decision and the pointer, the content stays in this skill's box. Duplicating it is how two skills start giving contradictory house rules.
- **Closing a project never deletes its file**: the owning skill writes `status: done — <date>` or `status: cancelled — <date>` inside it. Past roughly 20 closed projects they move to `~/Clawic/data/projects/archive/<project>.md` without being renamed.
- If the file does not exist and the user has not framed this work as a project, do not create one. A project file with a single English line in it is scaffolding.

## artifacts/

One file per thing, at `~/Clawic/data/english/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **the house style sheet**, **a speech or talk script**, **a template set**, **a written level assessment**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn. Every secret inside is already a pointer.

```markdown
# House style sheet
*Read before settling any mechanics, variety or word-choice question. Current as of 2026-07-26.*

Variety: en-GB, Oxford spelling (-ize), because the client publishes with OUP.
Deliberate exceptions: ISO dates everywhere; US spelling inside product UI strings — do not "correct" either.
Titles: sentence case, including headings in docs.
Quotes: double, punctuation outside unless it belongs to the quoted matter.
Banned beyond `banned_words`: any sentence opening with "In today's".
Serial comma: yes (`oxford_comma`).
```

```markdown
# Speech — best man, Ana's wedding
*Read when that speech comes up again, or when writing any other speech for this user. 2026-07-26.*

Final text, plus the two jokes that were cut and why, plus the timing note: 4 min at their reading pace.
```

```markdown
# Level assessment — 2026-07
*Read before setting a new focus or claiming progress. 2026-07-26.*

Writing B2+ / speaking B1+ / reading C1, on the evidence below, not on self-report.
Evidence: three samples, the errors they contained, and what they could not yet do.
Next focus, and the observable that would prove it moved.
```

## sessions/

The practice record. Append-only, one file per year, never rewritten. This is a log, so it never lives inside `memory.md`.

```markdown
# Sessions — 2026

| Date | Type | What was worked | Errors caught | Outcome |
|------|------|-----------------|---------------|---------|
| 2026-07-19 | call debrief | standup in English, 12 min | articles ×3, "I am agree" ×1, /θ/ | interrupted twice, both landed |
| 2026-07-22 | writing | 4 client emails, rung 4 | present perfect ×2 | two sent unedited |
```

- Every error caught here also goes to `## Recurring Errors` if it is the second sighting of its class. The session row is the evidence; the journal row is the thing that gets acted on.
- `Outcome` is what the user could do that they could not before, or the word `none`. A log of attendance measures nothing.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`errors.md` — `## Recurring Errors`, plus `## Retired` once struck rows outnumber live ones. This file is the reason the same article mistake is not explained for the tenth time.

`vocabulary.md` — `## Vocabulary`, grouped under `## Acquired`, `## Drilling`, `## Rejected` once the flat table stops being scannable. The rejected group is not dead weight: it is what stops a chunk the user hates from being suggested again.

`phrasebook.md` — `## Phrasebook`, one `## <channel>` heading (email, chat, calls, speeches) above it once more than one channel is in play.

`glossary.md` — `## Glossary`, one `## <domain>` heading per domain when the user works across more than one.
