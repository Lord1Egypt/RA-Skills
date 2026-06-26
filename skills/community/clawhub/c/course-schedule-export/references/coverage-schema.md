# Coverage Schema

Use a separate JSON file to verify that each prepared source entry was mapped into the manifest.

```json
{
  "source_entries": [
    {
      "id": "cell-r3c4",
      "source_id": "main-xls",
      "description": "Compiler Principles in Tuesday 3-4 slot",
      "matches": [
        {
          "name": "Compiler Principles",
          "mode": "recurring",
          "day": "tuesday",
          "slot": "3-4",
          "weeks": [1, 2, 3, 4, 5]
        }
      ]
    },
    {
      "id": "weekend-image-1",
      "source_id": "weekend-image",
      "description": "Weekend lab announcement",
      "matches": [
        {
          "name": "Weekend Lab",
          "mode": "dated",
          "dates": ["2026-04-18", "2026-04-25"],
          "slot": "5-8"
        }
      ]
    }
  ]
}
```

## Model

- `source_entries`
  One item per raw source unit you want to account for.
  Typical units:
  - a non-empty timetable cell
  - a supplemental screenshot item
  - a pasted text block that introduces a concrete class

- `id`
  Stable identifier for the source entry.

- `source_id`
  Optional source id from the manifest `sources` list.
  When present, the checker only accepts manifest course groups whose `sources` list includes this `source_id`.

- `description`
  Short human-facing description used in failure output.

- `matches`
  Required list of expected manifest course-group shapes.
  Use more than one match when a single source entry intentionally splits into multiple manifest course groups.

## Match Rules

Each item in `matches` is a partial manifest-course matcher.

Supported fields:
- `name`
- `location`
- `mode`
- `day`
- `slot`
- `weeks`
- `date`
- `dates`

Matching is exact on any field you include.
Do not include fields you do not want to constrain.
If `source_id` is present on the source entry, source provenance is also checked in addition to the field matcher.

## Recommended Use

Prepare the coverage checklist after you normalize the raw sources but before final export.
The checker enforces both directions:
- every source entry must match at least one manifest course group
- every manifest course group must be covered by at least one source entry
Then run:

```bash
python3 scripts/check_manifest_coverage.py manifest.json coverage.json
```

Use failures as a prompt to re-check the relevant source entry before exporting.
Typical failure labels:
- `entry`: the coverage checklist itself is incomplete or the matcher did not hit any manifest course group
- `provenance`: the matcher hit a course shape, but the course cites different sources than the source entry claimed
- `sources`: manifest course-source metadata is missing or references unknown source ids
- `uncovered`: a manifest course group exists without any source entry explaining it
