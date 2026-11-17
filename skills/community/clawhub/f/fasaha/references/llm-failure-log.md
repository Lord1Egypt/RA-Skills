# LLM Arabic Failure Log (Accumulating)

A **living log** of real Arabic errors caught by fasaha. Each entry records a case where
AI output was wrong, what correct Arabic looks like, and which fasaha section caught it.

**Purpose:** builds a growing corpus of actual failure patterns so the skill improves over
time and so similar errors are caught faster. Any agent appends an entry when it catches a new
pattern. Do not delete entries — add to the log.

## Entry schema

```
## YYYY-MM-DD — <short title>

- source (EN): <original English where applicable>
- bad (AI output): <the wrong Arabic>
- good (corrected): <the corrected Arabic>
- section: <1 Latin leakage | 2 calque | 3 word choice | 4 morphology/agreement |
           5 punctuation/hamza/numbers | 6 dialect > MSA | 7 LLM-specific gap | R register>
- note: <brief why it failed / the fix>
```

## Entries

## 2026-08-19 — RESOLVED: dialect negation mapping (was مش/موش → لم)

- source (EN): n/a (MSA target)
- bad (AI output): `مش`/`موش` → `لم` (from original reference)
- good (corrected): `مش`/`موش` → `ليس` generally; `لم` only when negating a past action
  (e.g. `هو مش طويل` → `ليس طويلاً`; `هو مش راح` → `لم يذهب`).
- section: 6
- note: Fixed in `dialect-classification.md` 5.6.5 and SKILL.md Section 6. Don't blanket-replace
  with `لم`; match the mapping to the predicate.

[Add new entries above this line when a fresh error is caught.]
