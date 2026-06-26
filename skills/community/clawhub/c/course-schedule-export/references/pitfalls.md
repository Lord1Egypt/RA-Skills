# Pitfalls

Use this file as a pre-flight and pre-export checklist.

## High-Risk Failure Modes

### 1. Missing a non-empty cell

Symptom:
- a course appears in the raw timetable but never shows up in the final calendar

Common cause:
- assuming a repeated course name means the later cell is redundant

Mitigation:
- compare final course groups against every non-empty source cell
- keep a checklist keyed by source cell or source note

### 2. Over-interpreting ugly week notation

Symptom:
- a cleaner-looking week range appears in the calendar than in the source

Common cause:
- converting punctuation noise into a guessed range

Mitigation:
- preserve literal meaning unless the source is truly explicit
- if punctuation can mean more than one thing, mark `needs_confirmation`

### 3. Losing the second half of a merged class

Symptom:
- a class that spans adjacent slots appears as only one shorter event

Common cause:
- reading only one source cell, or merging without checking the adjacent cell

Mitigation:
- check adjacent slot cells for same-course continuations
- merge only after metadata equality is confirmed

### 4. Wrong week-1 baseline

Symptom:
- all generated dates are shifted by a week

Common cause:
- using the semester start date instead of the Monday of week 1

Mitigation:
- explicitly ask for the week-1 anchor if not given
- restate the interpreted baseline before export
- do not require week-1 at all when the manifest is entirely date-based

### 5. Wrong period-time table

Symptom:
- events have correct day and week but wrong clock times

Common cause:
- reusing a previous semester's period table

Mitigation:
- require a period-time table for the current export unless already explicit
- record the exact slot mapping in the manifest

### 5.5. Forcing dated sessions into a week-based pattern

Symptom:
- a one-off makeup class or special session is exported on the wrong dates or repeats unexpectedly

Common cause:
- trying to convert an explicit calendar date into week/day recurrence

Mitigation:
- preserve explicit dates as dated course groups
- only use week-based recurrence when the source itself is week-based

### 6. Supplemental source silently overwriting the main source

Symptom:
- weekend or lab sessions disappear or replace the main timetable without explanation

Common cause:
- treating the latest message as authoritative without preserving provenance

Mitigation:
- keep per-course source references
- surface source conflicts instead of auto-overwriting

### 7. Building the workflow around non-portable dependencies

Symptom:
- the export process only works on the author's machine

Common cause:
- requiring packages such as spreadsheet parsers or YAML helpers for the main happy path

Mitigation:
- keep the final `.ics` generation path standard-library-only
- treat third-party parsing helpers as optional accelerators
- ask before installing packages on the user's machine
- document clearly which step needs the dependency and why

## Recommended Check Order

1. Confirm week-1 Monday and slot times.
2. Normalize all non-empty source cells.
3. Compare the normalized manifest to the primary source.
4. Add supplemental sources and mark conflicts.
5. Ask only the minimum ambiguity questions.
6. Re-run coverage checks.
7. Generate `.ics`.
8. Spot-check representative classes:
   - one normal weekly lecture
   - one odd/even or parity-based class
   - one merged cross-slot class
   - one supplemental or weekend class
