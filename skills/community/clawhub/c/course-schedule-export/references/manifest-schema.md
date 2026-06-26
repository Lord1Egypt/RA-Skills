# Manifest Schema

Use a JSON file with this shape before generating `.ics`.

```json
{
  "calendar_name": "2026 Spring Schedule",
  "timezone": "Asia/Shanghai",
  "week1_monday": "2026-03-09",
  "sources": [
    {
      "id": "main-xls",
      "kind": "xls",
      "path": "/path/to/timetable.xls",
      "role": "primary"
    },
    {
      "id": "weekend-image",
      "kind": "image",
      "path": "/path/to/weekend.png",
      "role": "supplemental"
    }
  ],
  "slots": {
    "1-2": {"start": "08:00", "end": "09:45"},
    "3-4": {"start": "10:00", "end": "11:45"},
    "5-6": {"start": "13:45", "end": "15:30"},
    "7-8": {"start": "15:45", "end": "17:30"},
    "9-10": {"start": "18:30", "end": "20:15"},
    "11-12": {"start": "20:30", "end": "22:15"},
    "5-8": {"start": "13:45", "end": "17:30"},
    "9-12": {"start": "18:30", "end": "22:15"}
  },
  "courses": [
    {
      "name": "Compiler Principles",
      "teacher": "Teacher Name",
      "location": "Building 101",
      "mode": "recurring",
      "day": "tuesday",
      "slot": "3-4",
      "weeks": [1, 2, 3, 4, 5],
      "note": "Optional note shown in DESCRIPTION",
      "sources": ["main-xls"],
      "status": "confirmed"
    },
    {
      "name": "Makeup Lab",
      "teacher": "Teacher Name",
      "location": "Building 202",
      "mode": "dated",
      "dates": ["2026-04-18", "2026-04-25"],
      "slot": "5-8",
      "sources": ["weekend-image"],
      "status": "confirmed"
    }
  ]
}
```

## Field Rules

- `calendar_name`
  Human-facing calendar title written into the `.ics`.

- `timezone`
  IANA timezone such as `Asia/Shanghai`.
  Do not guess from a different school or past export if the current user has not provided it.

- `week1_monday`
  ISO date for the Monday of week 1.
  Do not infer from semester start prose unless the mapping to week 1 is explicit.
  Required only when the manifest contains recurring course groups.

- `slots`
  Mapping from normalized slot keys to `HH:MM` start and end times.
  Treat these as school-specific. If the current timetable does not provide them and the user has not given them, ask first.

- `sources`
  Optional but strongly recommended. Track every source used in extraction, including supplemental screenshots and pasted text.

- `courses`
  One object per normalized course group.
  A course group can be either recurring or dated.

## Course Rules

- `name`
  Required.

- `teacher`
  Optional string. Use `""` if unavailable.

- `location`
  Required. Use a stable string; do not encode week rules here.

- `day`
  Required for recurring course groups. Lowercase day name:
  - `monday`
  - `tuesday`
  - `wednesday`
  - `thursday`
  - `friday`
  - `saturday`
  - `sunday`

- `slot`
  Required slot key present in `slots`.

- `weeks`
  Required for recurring course groups. List of explicit integers. Expand ranges before writing the manifest.

- `mode`
  Optional but recommended:
  - `recurring`
  - `dated`
  If omitted, infer `recurring` when `weeks` and `day` are present, or `dated` when `date` or `dates` is present.

- `date`
  Optional for dated course groups when there is exactly one explicit date. ISO date such as `2026-04-18`.

- `dates`
  Optional for dated course groups. Use this when one course group applies to multiple explicit dates.
  At least one of `date` or `dates` must be present for dated course groups.

- `note`
  Optional. Use for attendance warnings, source caveats, or extra context.

- `sources`
  Recommended list of source ids that support this course group. Use this to trace conflicts and review late edits.

- `status`
  Optional but recommended:
  - `confirmed`
  - `needs_confirmation`
  - `derived`
  Mark anything ambiguous as `needs_confirmation` until the user answers.

## Source Rules

Each source entry should include:
- `id`
  Stable local identifier used by course objects.
- `kind`
  Example values: `xls`, `xlsx`, `pdf`, `image`, `ocr-text`, `chat-text`.
- `path`
  Filesystem path when applicable.
- `role`
  Example values: `primary`, `supplemental`, `cross-check`.

## Verification Checklist

Round 1:
- every non-empty timetable cell maps to at least one course object
- merged periods only combine adjacent slots with identical metadata
- odd/even weeks are expanded explicitly
- week lists are sorted and deduplicated
- explicit calendar-date sessions stay explicit instead of being forced into week-based recurrence
- supplemental screenshots are either encoded as extra course objects or explicitly ignored
- the week-1 Monday aligns with the user's stated semester baseline
- every course object has either a source reference or an explicit explanation for why it was derived

Round 2, after ambiguity polling:
- any `needs_confirmation` item was resolved or remains explicitly blocked
- cross-source conflicts are either resolved or carried forward as caveats
- the final export excludes unresolved guesses
