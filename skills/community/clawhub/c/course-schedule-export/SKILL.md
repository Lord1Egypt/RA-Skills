---
name: course-schedule-export
description: Turn school or university timetables into checked .ics calendars. Use when an agent needs to normalize and verify schedules from xls/xlsx, screenshots, PDFs, OCR text, or pasted timetable text before exporting for Apple Calendar, Google Calendar, or similar apps. Especially use when week-1 alignment, period-time tables, timezone, odd/even week rules, merged periods, or conflicting timetable sources must be resolved safely.
---

# Course Schedule Export

Convert messy timetable inputs into a checked calendar export. Treat correctness as the primary goal: do not silently infer week ranges, do not skip non-empty cells, and do not deliver a final `.ics` until the normalized schedule has been cross-checked against the source. Prefer a multi-round workflow: normalize, verify, resolve ambiguities, verify again, then export.

Do not assume that another school's calendar dates, slot times, timezone, or semester structure apply here. If the user has not provided a week-1 anchor, period-time table, timezone, or any other school-specific calendar setting needed for deterministic export, ask for it before generating the final `.ics`.

## Workflow

1. Gather the authoritative inputs.
   Require:
   - at least one primary timetable source
   - the class-period time table
   - the week-1 anchor date, ideally the Monday of week 1, if any recurring week-based classes exist
   Optional:
   - supplemental screenshots for labs, makeup classes, or weekend sessions
   - a second timetable source for cross-checking
   - a previously exported calendar or manifest to diff against
   If any required item is missing, ask for it explicitly instead of reusing values from a previous school or previous export.

2. Build a normalized schedule manifest before generating calendar output.
   Use the schema in `references/manifest-schema.md`.
   Support both of these shapes:
   - recurring course groups keyed by day + slot + week set
   - dated course groups keyed by explicit calendar date + slot
   Capture one course group per distinct combination of:
   - course name
   - location
   - recurrence basis
   Split a source cell into multiple course groups if it contains multiple courses with different week rules.
   Preserve source provenance for each course group so later review can tell which source introduced it.

3. Preserve literal meaning from the source.
   - Expand explicit ranges such as `1-8`.
   - Expand explicit parity rules such as `9-16 even` or `5-11 odd`.
   - Preserve explicit calendar dates as dated course groups instead of trying to force them into week math.
   - If the source text is ambiguous, stop and surface the ambiguity instead of guessing.
   - Example of unsafe guessing: converting `5,9 odd` into `5-9 odd`.

4. Merge only when the source supports it.
   Merge consecutive slots into one longer event only when all of these match:
   - same course name
   - same teacher if present
   - same location
   - same day
   - same week set
   Keep them separate otherwise.

5. Run round-1 verification against the source.
   Before asking follow-up questions or exporting, verify:
   - every non-empty timetable cell was accounted for
   - every manifest course group is explained by at least one prepared source entry
   - no course group was dropped
   - week-1 Monday maps to the intended calendar week
   - odd/even handling matches the source text
   - merged periods really come from adjacent matching slots
   - supplemental screenshots were either incorporated or explicitly excluded
   - the manifest contains source references for every derived course group
   Run `scripts/check_manifest_coverage.py` when you have prepared a source-entry coverage checklist. Treat it as a two-way check:
   - each prepared source entry must map to at least one manifest course group
   - each manifest course group must be covered by at least one prepared source entry
   - if a coverage entry specifies `source_id`, only manifest course groups that cite that source may satisfy it

6. Resolve ambiguities by polling in small rounds.
   Ask only the minimum unresolved questions for the current blocker set.
   Good polling pattern:
   - round 1: timezone and period-time table, plus week-1 date if recurring classes exist
   - round 2: conflicting week notation or source conflicts
   - round 3: any remaining merge/split decisions
   Do not dump all possible questions at once. Batch only related ambiguities that are necessary for the next deterministic step.

7. Run round-2 verification after user answers.
   Re-check the exact course groups touched by the answers, then re-run a full coverage pass.
   If a change fixes one ambiguity but creates another inconsistency, stop and surface it.
   Re-run `scripts/check_manifest_coverage.py` after any manifest edits caused by user answers.

8. Generate the `.ics`.
   Run `scripts/generate_ics.py` against the normalized manifest.
   This script must stay standard-library-only so it can run on a typical local machine without extra installs.

9. Report with explicit caveats.
   In the final response:
   - give the output path
   - call out any ambiguous items that required user confirmation
   - mention any manual interpretations that remain
   - mention whether the export was checked against one source or multiple sources

## Extraction Rules

- Prefer direct extraction from the primary source over OCR from screenshots when both exist.
- Treat timetable screenshots as secondary unless they clearly override the primary source.
- Support multiple timetable inputs in the same job. Typical source priority:
  - machine-readable timetable export
  - timetable PDF or screenshot
  - supplemental notices for labs, weekends, or makeup sessions
  - pasted text supplied later in chat
- Support both recurring semester schedules and one-off dated sessions.
- If two sources disagree, keep both claims visible until one is resolved. Do not silently let the later source overwrite the earlier one.
- Preserve a separate note for comments such as attendance reminders or prerequisite warnings; do not encode those notes as fake course meetings.
- Keep calendar event summaries short. Put week rules, teacher, and warnings into the description.
- Prefer built-in tooling and the Python standard library for export steps.
- Treat any parser that needs third-party libraries as optional, not baseline.
- If source extraction would require installing packages, first try a no-install path.
- If installation is still the best option, ask the user before installing anything and explain why the built-in path is insufficient.

## Ambiguity Rules

Stop and ask the user when any of these appear:
- punctuation makes a week rule unclear
- a cell mixes multiple locations without clear week partitioning
- a supplemental image conflicts with the primary timetable
- the source gives a week number but not the week-1 anchor date
- the source gives period numbers but not start/end times
- the timezone is missing and cannot be safely inferred from context
- a school-specific holiday, makeup-teaching rule, or semester boundary is needed for correctness
- the source mixes week-based classes with explicit calendar dates and the intended precedence is unclear
- two timetable sources disagree on the same course group
- a class appears in one source but disappears in another
- the same course appears in adjacent slots but with slightly different metadata, making merge unsafe

Do not ask when the information is explicit in the source and can be normalized deterministically.
Do not ask broad catch-all questions such as "anything else I should know?" until the concrete blockers are exhausted.

## Pitfalls

Read `references/pitfalls.md` before doing a non-trivial export. Use it as a pre-flight checklist.

Common failures to avoid:
- dropping a non-empty cell because a previous cell already mentioned the same course
- expanding a broken week string into a nicer-looking but unsupported range
- forgetting the second half of a cross-slot course
- applying one source's period times to another semester without checking
- exporting after only one verification pass
- losing track of which source introduced a weekend or lab session
- baking third-party Python dependencies into the core export path

## Resources

- `references/manifest-schema.md`
  Read this before writing the normalized schedule manifest or reviewing someone else's manifest.

- `references/coverage-schema.md`
  Read this when preparing a source-entry checklist for coverage verification.

- `references/pitfalls.md`
  Read this before extraction and again before final export.

- `scripts/generate_ics.py`
  Use this to turn a normalized manifest JSON file into a deterministic `.ics` file.

- `scripts/check_manifest_coverage.py`
  Use this to enforce two-way coverage between prepared source entries and manifest course groups.

## Minimal Deliverable

If the user only wants guidance, do not generate files. Give them:
- the missing inputs you still need
- the exact ambiguity list
- the next deterministic step

If the user wants the export completed, do the normalization and generate the `.ics` instead of only describing how.
