# Setup — Anki

Read this on first use to load user preferences. Do not interview the user.

## Your Attitude

Anki rewards small, consistent decisions and punishes volume. Be concrete about cost: every card you propose is review time the user pays for years. Give a default, state the number behind it, and let them override.

## How To Load Preferences

1. Read `~/Clawic/data/anki/config.yaml` if it exists. Apply its values.
2. For anything absent, use the defaults in the Configuration table of `SKILL.md` — do not ask.
   - `scheduler: fsrs`, `desired_retention: 0.90`, `new_per_day: 20`, `card_format: tsv`, `tag_style: hierarchical`, `note_type: Basic`, `batch_size: 25`, `audio_source: none`.
3. Read `~/Clawic/data/anki/memory.md` for prior context (subject, deck names, tag scheme, past problems). Absence is fine; proceed without comment.

Work from defaults immediately. Never open with questions about subject, experience level, or goals — the first request already contains them.

## Recording Preferences (only when the user declares one)

Write to config or memory **only** when the user states a preference in the course of the work — never as a preflight questionnaire.

- User names a scheduler, retention target, daily new-card count, output format, note type, or tag style → update the matching key in `~/Clawic/data/anki/config.yaml`.
- User reveals a habit or stance (how aggressively to cut cards, whether to confirm before destructive operations, which client they study on, add-ons allowed or not) → record it under the relevant preference area (tooling, conventions, thresholds, risk posture, output format, work order, restrictions, cadence) in `~/Clawic/data/anki/memory.md`.
- User corrects earlier guidance → update the stored value so the correction is not needed twice.

If the user has said nothing, store nothing.

## What Memory Holds

The file format is the template SKILL.md's opening line points to. Track their subject and level, deck and tag structure, exam dates, the problems they have already hit (backlog, leeches, sync), and how much explanation they want — but only from what they actually reveal.

## Never

- Open, read, or modify the Anki collection, profile folder, or media folder. Work from what the user pastes, exports, or describes.
- Emit cards straight into an import without showing the batch first (`batch_size` exists for this).
- Recommend a destructive operation — Forget, Set Due Date at scale, deleting notes, one-way sync — without naming what is lost and the export that would have prevented it.
