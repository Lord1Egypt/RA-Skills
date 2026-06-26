# Task Decomposition: 15-Minute Unit Principle

## The Rule

Each task should be independently verifiable, have a single dominant risk, and expose a clear done condition.

**Target:** ~15 minutes of focused work per unit.

## Why This Matters

- **Independent verification:** Can you test this unit without depending on adjacent units being done first?
- **Single risk:** If it fails, what's the one most likely cause? (If you can't answer in one sentence, the unit is too big.)
- **Clear done condition:** Can you write a test/acceptance criterion that proves completion? (If it's fuzzy, the unit is too vague.)

## Examples

### ✅ Good Decomposition

**Unit 1: "Parse CSV upload and validate rows"**
- Risk: CSV format malformed → validation logic catches and reports
- Done: Validation function returns list of valid rows + error list
- Test: `test_parse_valid_csv()`, `test_parse_malformed_csv()`
- Time: ~10 minutes (parser + basic validation)

**Unit 2: "Write valid rows to database"**
- Risk: Duplicate key constraint → should log and skip, not crash
- Done: All valid rows inserted; duplicates logged; error count matches expected
- Test: `test_insert_valid_rows()`, `test_handle_duplicate_keys()`
- Time: ~12 minutes (insert logic + error handling)

### ❌ Bad Decomposition

**"Implement user import feature"**
- Risk: Too many things (parsing, validation, database, error handling, rollback logic, user notification) — which will actually fail?
- Done: Undefined (works sometimes? all cases? what about edge cases?)
- Time: Could be 30 minutes or 3 hours — no clear scope

## Decomposition Checklist

For each proposed unit, ask:

1. **Independent?** Can this be tested without waiting for other units?
2. **Single dominant risk?** Can I describe the most likely failure in one sentence?
3. **Clear done?** Can I write a test that proves completion?
4. **15-ish minutes?** Does it feel scoped correctly or is it a placeholder?

If you answer "no" to any of these, split the unit further.

## Model Routing by Decomposition Size

- **Haiku:** <200 tokens of context, <15 minutes, boilerplate or narrow edit (parse CSV row, format error message)
- **Sonnet:** 200-1000 tokens context, 15-45 minutes, feature implementation (build parser + validator, handle edge cases)
- **Opus:** >1000 tokens context, 45+ minutes, multi-file changes, architecture questions, root-cause analysis

Smaller units unlock faster, cheaper execution with lower-tier models.
