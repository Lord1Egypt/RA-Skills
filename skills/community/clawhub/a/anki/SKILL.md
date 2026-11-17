---
name: Anki
slug: anki
version: 1.0.3
description: >-
  Builds and repairs Anki decks: card writing, FSRS and SM-2 deck options, leeches, review
  workload, imports, and sync. Use when making cards from notes, PDFs, lectures, textbooks, or
  vocabulary lists; when reviews pile up, take too long, or a backlog builds after time off; when
  retention drops, cards keep failing, or a deck falls into ease hell; when choosing FSRS vs SM-2,
  or setting desired retention, new cards per day, learning steps, and leech thresholds; when a
  deck asks to upload or download in a one-way sync, loses media, or fails Check Database; when
  importing CSV/TSV, an .apkg, or a shared deck, or migrating from Quizlet, Memrise, or SuperMemo;
  when cards are due but nothing appears; and when a fixed exam date forces a study plan. Covers
  language decks, medical and board decks, code and math material, and personal decks such as names
  and faces or poetry. Not for generic flashcard writing outside Anki, spaced-repetition algorithm
  theory, study-session planning, or add-on development.
homepage: https://clawic.com/skills/anki
changelog: "Display name shown correctly"
metadata:
  clawdbot:
    emoji: 🧠
    os:
    - linux
    - darwin
    - win32
    displayName: Anki
    configPaths:
    - ~/Clawic/data/anki/
---

User preferences and memory live in `~/Clawic/data/anki/` (see `setup.md` on first use, `memory-template.md` for the file format). If you have data at an old location (`~/anki/` or `~/clawic/anki/`), move it to `~/Clawic/data/anki/`. Nothing else is stored: the collection is never opened or modified — you work from text, files, exports and stats the user hands over, and you emit cards the user imports.

## When To Use

- Turning source material (notes, lecture slides, PDFs, textbook chapters, word lists) into importable cards
- Diagnosing a deck: reviews exploding, retention sliding, leeches piling up, "I study daily and still forget"
- Configuring deck options: FSRS vs SM-2, desired retention, daily limits, learning steps, leech action
- Anki-the-application problems: one-way sync prompts, missing media, nothing due, broken imports, add-on breakage
- Deadline work: an exam date, a backlog to clear, a shared deck to unsuspend by topic
- Non-academic memory work: names and faces, poetry, music theory, professional facts
- Not for flashcard theory outside Anki (`flashcards`), spacing-algorithm theory for its own sake (`spaced-repetition`), study scheduling and technique choice (`studying`), or writing add-on code

## Quick Reference

| Situation | Play |
|---|---|
| "Make cards from this" | Extract atomic facts, one per card, then state the intake cost of rule 5 → `bulk-generation.md`; how to word each card → `cards.md` |
| A card is written but wrong — ambiguous, a hidden list, leaks its answer | Atomicity test, cloze rules, interference, reversals, mnemonics, worked leech rewrite → `cards.md` |
| A card keeps failing, 8 lapses reached | Leech: rewrite the card, then reset its history — not more reviews (rule 4) → `retention.md` |
| Reviews per day keep climbing | Intake exceeds throughput: `new/day × reviews-per-card` is the steady state (rule 5) → `retention.md` |
| Retention below 0.85 while desired is 0.90 | Grading drift or bad cards before settings — check the Again-rate by deck first → `retention.md` |
| Backlog after time off | New cards to 0, cap reviews, burn down oldest-first; never marathon → `retention.md` |
| "Which numbers do I set?" | Every default and what changes it → `scheduling.md` |
| Ease hell (core band 130-180%, screened with `prop:ease<2.0`) | SM-2 artifact: move to FSRS, or reset ease AND fix the cards → `retention.md` |
| Cards are due but nothing appears | Daily limit, parent-deck limit, burial, suspension — in that order → `troubleshooting.md` |
| Anki asks Upload or Download | One-way sync: keep the side with the work, the other is overwritten → `sync-and-backup.md` |
| Import made duplicates, or one giant card | Field mapping, separator, HTML setting → `importing.md` |
| Need to find or bulk-edit a subset of cards | Search syntax and filtered decks → `search.md` |
| Card needs a hint, typed answer, or styling | Note type and template surgery → `note-types.md` |
| Labelled diagram, anatomy plate, map, circuit, UI screenshot | Image Occlusion: masks, and Hide All vs Hide One → `image-occlusion.md` |
| Deck structure, tags, merges, duplicates | `organization.md` |
| Vocabulary, audio, conjugation, false friends | `language.md` |
| Med school, boards, AnKing-style shared decks | `medicine.md` |
| Programming, syntax, math, theorems | `code-and-math.md` |
| Names and faces, poetry, music, chess, birds, work facts | Non-academic decks and how to keep them alive → `personal-decks.md` |
| Exam in N days | Capacity math before content — can the deck even be finished → `exam-prep.md` |
| Which add-ons, and what breaks on upgrade | `addons.md` |
| Anything else | Ask what the user sees on screen — a count, a button, an exact error — map it to a row above, then propose one change at a time |

Depth on demand — read SKILL.md alone by default, then exactly one of these: `cards.md` (wording a card that survives) · `bulk-generation.md` (source material → importable batch) · `note-types.md` (fields, templates, CSS, typed answers) · `image-occlusion.md` (masking a labelled image, and the Hide All / Hide One choice) · `scheduling.md` (every deck-options number) · `retention.md` (deck diagnosis, ease hell, leeches, backlog) · `search.md` (query syntax, bulk edits, filtered decks) · `organization.md` (decks vs tags, duplicates, maintenance) · `importing.md` (CSV/TSV, .apkg, migrations, media, export) · `sync-and-backup.md` (one-way sync, .colpkg, corruption) · `troubleshooting.md` (the app misbehaving) · `addons.md` (what to install, what is already built in) · `exam-prep.md` (fixed date, capacity math, triage) · `language.md` · `medicine.md` · `code-and-math.md` · `personal-decks.md` (the four subject guides) · `setup.md` (first-use preference loading).

## Core Rules

1. **One retrievable fact per card.** Test: the answer fits in a few words and only one answer is right. A four-item list is one card that fails on item four forever; split it into four cards, plus a "how many" card only if the count is itself testable. Ignore this and the card becomes a leech that drags its whole review history down.
2. **Every question carries its own context.** Cards resurface years later, shuffled, far from the chapter that made them obvious. "What does ACE stand for?" competes with every other ACE you will ever learn; "[Cardio] In blood-pressure regulation, ACE stands for…" does not. Context lives in the question text or a visible field, never in the deck name alone.
3. **Grade recall, not feeling.** Again = could not retrieve it. Hard = retrieved, slowly and painfully — a PASS, not a failure. Good = retrieved. Easy = instant, and the interval was clearly too short. Pressing Easy to shed workload, or Hard to "keep it close", feeds the scheduler false data; the buttons are the only signal it has.
4. **Fix the card, not the schedule.** Default leech threshold: 8 lapses. Eight failures means the card is unanswerable as written — interference, ambiguity, or a hidden list. Rewrite it, then reset its history so the scheduler stops carrying the old card's difficulty. Piling reviews on a bad card buys permanent daily cost and no memory.
5. **Workload is decided at intake.** Steady-state daily reviews ≈ `new_per_day × reviews_per_card`. Read `reviews_per_card` from your own collection (Stats: total reviews ÷ total cards; commonly 8-15 after the first year on defaults). 20 new/day × 10 = ~200 reviews/day, indefinitely. Work backwards from time you will actually spend: `new_per_day = (minutes_available × 60 / seconds_per_review) / reviews_per_card`.
6. **Desired retention is a workload dial, not a quality dial.** FSRS (built in, `anki >=23.10`) defaults to 0.90. Pushing to 0.95 buys a few points of recall for roughly double the daily reviews; dropping under 0.80 spends the savings on relearning. Do not guess the trade — deck options ships a simulator that prices it against your own history (`scheduling.md`).
7. **A preset is shared; a deck is not.** Deck options live in presets attached to many decks. Raising "new cards/day" while looking at one subdeck raises it everywhere on that preset. Read the preset name and its usage count first, and clone the preset when the change is meant for one deck.
8. **Cards are cheap to make and expensive to own.** Lifetime cost ≈ `reviews_per_card × seconds_per_review / 60` minutes. At 10 reviews × 8 s, one card ≈ 1.3 minutes of your life, so 500 cards ≈ 11 hours. The filter for adding a card is "worth 1-2 minutes of review time", not "is true".

## The Four Buttons

The scheduler sees nothing but which button you pressed. Grading drift is the most common cause of "the algorithm is broken".

| Button | Means | SM-2 effect | FSRS effect | Misuse |
|---|---|---|---|---|
| Again | Retrieval failed | Ease −20pp, lapse counted, card returns to relearning | Difficulty up, stability collapses | Pressing it for "knew it, but slowly" — that is Hard |
| Hard | Retrieved with effort | Ease −15pp, interval ×1.2 | Small stability gain, difficulty up | Using it as a soft fail; habitual Hard ratchets intervals back toward daily |
| Good | Retrieved normally | Interval × ease | Normal stability gain | None — this is the default answer |
| Easy | Instant; the interval was too short | Ease +15pp, interval × ease × 1.3 | Large stability jump, difficulty down | Farming Easy to shrink today's queue, then losing the card for months |

Consistency beats correctness: one grading standard applied the same way daily gives FSRS something to fit. Changing your standard mid-collection is what makes optimized parameters stop matching.

## Workload Math

Every workload question is one of these four, and none of them needs a guess.

- **Steady state**: `daily_reviews ≈ new_per_day × reviews_per_card` (rule 5) — the number you are signing up for, not today's count.
- **Time**: `minutes/day = daily_reviews × seconds_per_review / 60`. Stats reports seconds/review directly; 5-8 s is typical for vocabulary, 10-20 s for reasoning-heavy cloze.
- **Finishing a deck by a date**: `new_per_day = remaining_new / (days_until_exam − 21)`. The 21 days are deliberate: a card first seen inside the last three weeks never reaches mature interval (`interval >= 21 days`) and will not hold through exam day (`exam-prep.md`).
- **Burning down a backlog**: at a fixed daily cap, `days_to_clear ≈ backlog / (cap − incoming_due)`. If `cap <= incoming_due` the backlog never clears — set new cards to 0 first, which is what removes tomorrow's incoming (`retention.md`).

## Card Diseases

Symptom on the review screen → what is actually wrong → what to change. Writing the replacement card — atomicity test, cloze rules, interference, reversals, worked leech rewrite: `cards.md`.

| Symptom | Diagnosis | Fix |
|---|---|---|
| Fails every time, feels unlearnable | The card holds a list or two facts | Split into atoms (rule 1) |
| "I know this but can't say it" | The answer is a paragraph, not a fact | Cut the answer to its testable core; move the prose to a source field |
| Right answer, wrong card | Interference with a near-identical sibling | Put the discriminator in BOTH questions, or merge them into one contrast card |
| Passes in the deck, fails in the exam | Recognition: the phrasing gave it away | Rephrase; kill giveaway wording and blanks sized to the answer |
| Always Easy, never forgotten | Below your knowledge floor | Delete it — a card you cannot fail teaches nothing and still costs reviews |
| Correct only because its sibling came first | Sibling ordering leak | Turn on sibling burying (`scheduling.md`) |
| Several answers would be accepted | The question underspecifies the domain | Add the context prefix (rule 2) |
| Passes alone, useless in practice | Isolated fact with no network | Add its cause, contrast and use — or accept it is trivia and cut it |

## When Anki Is The Wrong Tool

Saying this early saves more time than any card-writing tip.

- **Procedures and skills** — writing proofs, debugging, speaking fluently, playing a passage — need repetition of the ACT. Anki holds the ingredients (a theorem statement, an API signature, a phrase), never the performance.
- **Material not yet understood.** An unexplained cloze becomes a leech within a month. Understand first, card second; that ordering predicts whether a deck survives better than any setting.
- **Facts with a lookup always at hand and rarely needed.** If retrieval speed barely matters and you check it twice a year, a note file beats a card.
- **A three-day deadline on conceptual material.** Spacing has no room to work; worked problems and practice tests dominate. Anki pays off when the first exposure is ≥3 weeks out (`exam-prep.md`).
- **Escape hatch**: high-stakes recall under time pressure — drug doses, kanji, case names, vocabulary, anatomy labels — is what Anki is unbeaten at. There, under-carding is the bigger risk.

## Output Gates

Before handing over a batch of generated cards, verify:

- Every card has exactly one answer, stateable in a few words?
- Every question readable in isolation, with its domain context visible (rule 2)?
- No answer guessable from phrasing, blank length, or the shape of the options?
- Multiple clozes on one note all test the SAME fact; separate facts got separate notes?
- Tags taken from the user's existing scheme rather than a new one you invented?
- Count reported with its cost: "N cards ≈ N × 1.3 min of lifetime review, +X reviews/day at current settings" (rule 8)?
- Output in the user's `card_format`, with separator and field order stated so the import maps correctly?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/anki/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| scheduler | fsrs \| sm2 | fsrs | Selects which settings advice applies: desired retention and the optimizer (FSRS) vs ease factor and interval modifier (SM-2), in `scheduling.md` and `retention.md` |
| desired_retention | number (0.70-0.97) | 0.90 | The FSRS workload dial (rule 6); every review-count estimate in Workload Math scales with it |
| new_per_day | number (0-9999) | 20 | Drives the steady-state projection of rule 5 and the deadline math in `exam-prep.md` |
| card_format | tsv \| csv \| markdown \| apkg-notes | tsv | Shape of every generated batch: separator, field order, and whether HTML is emitted (`importing.md`) |
| tag_style | hierarchical \| flat | hierarchical | Whether generated tags read `subject::topic::subtopic` or single-level (`organization.md`) |
| note_type | text (note type name) | Basic | Which note type generated cards target; sets the field names in the output header (`note-types.md`) |
| batch_size | number (5-200) | 25 | Cards produced per pass before pausing for the user's review, instead of dumping a whole chapter |
| audio_source | none \| tts \| forvo \| user-supplied | none | Whether language cards carry an audio field and what fills it (`language.md`) |

Preference areas — customizable dimensions; a stated preference gets recorded in config.yaml and applied:

- **Tooling** — desktop Anki, AnkiMobile, AnkiDroid or AnkiWeb as the primary client; add-ons allowed or forbidden (affects every workflow that assumes a browser or an add-on, `addons.md`)
- **Conventions** — deck naming and depth, tag vocabulary, note-type choice, whether cards carry source references (`organization.md`, `note-types.md`)
- **Thresholds** — daily review cap, session length, leech threshold and action, maximum interval (`scheduling.md`)
- **Risk posture** — confirmation before destructive operations: Forget, Reposition, Set Due Date, reschedule-on-FSRS-change, deleting duplicates, one-way sync (`sync-and-backup.md`)
- **Output format** — target language of card text, answer verbosity, whether explanations ride in an extra field, images and audio included or not
- **Work order** — generate-then-review in batches vs card-by-card approval; duplicate check before or after generation
- **Restrictions** — copyright limits on shared material, no-images or no-audio constraints, subjects deliberately left uncarded
- **Cadence** — study time of day, weekly maintenance day, exam dates that trigger the deadline math (`exam-prep.md`)

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Answering Hard to keep a card close | Hard is a pass with a shrinking multiplier; used habitually it drives intervals toward daily and inflates difficulty | Again for failures, Good for successes; Hard only for genuine slow retrievals |
| Deleting a leech | Removes the evidence and the fact; the same gap reappears from the source material next month | Suspend, rewrite, reset history, unsuspend (rule 4) |
| Studying a giant shared deck as-is | Thousands of unsuspended cards on material not yet taught — a backlog by day three | Unsuspend by lecture or topic tag as you cover it (`medicine.md`) |
| Editing deck options from a subdeck | Presets are shared; the edit hits every deck using that preset | Check the usage count, clone the preset first (rule 7) |
| Fixing retention by raising desired retention | The recall gap is usually card quality or grading; the dial only buys reviews | Diagnose the Again-rate by deck first (`retention.md`) |
| Enabling FSRS and skipping Optimize | Default parameters model an average stranger, not you | Optimize once real history exists, then periodically (`scheduling.md`) |
| Treating AnkiWeb as a backup | Sync mirrors deletions and corruption to every device | Keep local `.colpkg` exports; automatic backups are per-profile and local (`sync-and-backup.md`) |
| Importing with "update existing notes" on the wrong key | Silently overwrites edited notes that match on the first field | Dry-run on a copy of the collection and verify the key column (`importing.md`) |
| One deck per lecture, five levels deep | Navigation and per-deck limits become the thing you manage | Shallow decks, hierarchical tags (`organization.md`) |
| Carding a textbook you have not read | Produces recognition of phrasing, not knowledge | Understand first, card second (When Anki Is The Wrong Tool) |

## Where Experts Disagree

- **FSRS vs SM-2.** FSRS is the default for anyone with review history and no add-on constraints; SM-2 stays defensible for very small collections, for old clients kept in sync across devices, and for people who deliberately hand-tune ease. The boundary is history volume, not taste: with only a few hundred reviews the optimizer has nothing to fit.
- **Sentence cards vs word cards** (languages). Sentence-first argues context is the unit of meaning; word-first measures faster coverage of high-frequency vocabulary. Resolved by goal: reading speed → word cards with an example field; production and listening → sentence cards (`language.md`).
- **Premade decks vs your own.** Writing cards is itself encoding, and self-made decks match your syllabus; premade decks are professionally written and your time is finite. The line is volume: medicine and law load beyond what a student can author (`medicine.md`).
- **How aggressively to delete.** One school deletes any card that lapses twice; the other rewrites everything. Both beat the middle position — reviewing bad cards forever.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/anki (install if the user confirms):
- `flashcards` — card writing when the tool is not Anki, or not yet decided
- `studying` — study plans, technique choice, exam countdown beyond deck math
- `spaced-repetition` — the scheduling theory behind these settings
- `usmle` — board-exam content strategy that `medicine.md` here plugs into

## Feedback

- If useful, star it: https://clawic.com/skills/anki
- Latest version: https://clawic.com/skills/anki

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/anki.
