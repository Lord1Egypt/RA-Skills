# Learning — Signals and the Preference Ladder

The digest's edge over any feed is that it learns. This file is the canonical home of signal counting and ladder mechanics; `preferences.md` in the data folder holds the state, `dimensions.md` lists what can be learned.

## Signal Counting (canonical)

- An **explicit statement** ("shorter", "drop sports") counts as **2 signals**.
- One **behavioral observation** (skipped, forwarded, asked a follow-up, stopped reacting) counts as **1 signal**.
- Signals accumulate per entry (per topic, per format dimension, per timing slot) — never globally.

## The Ladder (canonical)

```
[none] → [pattern] → [confirmed] → [locked]
```

- **2+ signals** → mark `pattern`. Ask once before acting on format or timing patterns.
- **Exclusions are the fast path**: apply at pattern strength immediately (SKILL.md rule 3) — still confirm before locking.
- User explicitly approves when asked → `confirmed`. Interrupt rules require `confirmed` minimum before any interrupt fires (`delivery.md`).
- Confirmed + **3 deliveries without contradiction** → `locked`.
- **Demotion**: any contradicting signal drops the entry one level. An explicit reversal ("actually, include sports again") replaces the entry the same day, at `confirmed`.

Worked example: user skips sports items in two digests → `exclude: sports (pattern)`, sports dropped now → ask once: "drop sports going forward?" → "yes" → `(confirmed)` → three digests later, no pushback → `(locked)`.

## Reading Reactions

| Signal | Adjustment |
|---|---|
| "Too long" / stops reacting after item N | Cut item count next digest; log a length signal |
| "Missed X" | Add X's sources and keywords; diagnose WHY it was filtered (dead source? recency window? exclusion collision?) — the diagnosis is the fix, `sources.md` |
| "Don't care about Y" | Exclusion at pattern strength immediately (SKILL.md rule 3) |
| "Love this" / forwards an item | Reinforce that topic and format; note what was different about that item |
| Asks follow-ups on a topic | Depth signal: raise per-topic depth (`dimensions.md` → Depth) |
| Reacts only to one section | Structure signal: that section is the digest for them — consider leading with it |
| Changes reply register (formal ↔ casual) | Tone signal; mirror it (`writing.md` → Tone) |

## The Silence Protocol

- No reaction for **3 consecutive digests** → ask exactly one concrete, closed question ("keep the morning slot?" / "still want the crypto items?"). Never a "any feedback?" open question — those get politeness, not signal.
- Silence is ambiguous by nature: an ignored digest and a loved-but-busy digest look identical. That is why silence only ever triggers a question, never an automatic preference change.

## Drift and Decay

- Interests drift. A `locked` topic with no positive signal across many digests is a demotion candidate — but locked entries never decay automatically: ask first, then demote on the answer.
- Life events reset preferences wholesale (new job, new project, moved timezone). When the user mentions one, offer a one-question re-check of topics and timing instead of waiting for the ladder to catch up entry by entry.

## Mood vs Preference

- One grumpy "too much today" on a heavy news day is mood; the same comment on a normal day is signal. Weigh signals against context before counting them.
- Never learn from your own guesses: an item YOU chose to include that got no reaction says nothing about the topic — only user-initiated signals count toward exclusions.

## What Lives Where

| Store | Content | Written when |
|---|---|---|
| `config.yaml` | Declared variables (SKILL.md → Configuration) | User states a preference outright |
| `preferences.md` | Ladder state per dimension, context profiles, entity notes | After every delivery with new signals |
| `sent-log.md` | Shipped items with dates (SKILL.md rule 7) | Every delivery |

A declared preference (config) is never overwritten by an observed pattern (ladder) without the user confirming — observation proposes, the user disposes.

## Context Profiles

Users with split contexts (work morning vs personal evening) get per-profile overrides in `preferences.md` → Context Profiles; anything unset in a profile falls through to the main sections. Signals learned during a profile's digest count toward that profile only.
