# Field Mapping

## Request contract

- Endpoint: `https://api.iyiou.com/skill/info`
- Query params:
- `page={1..5}` for single-day mode
- `page={1..25}` for recent-N-days mode (`N=2..7`)
- `pageSize=10`
- Response schema (strict):
- top-level object with `code`, `data`, `message`
- success condition: `code == 0`
- event list path: `data.posts` (must be array)
- Stop rule:
- Single-day mode: stop when `page > 5`
- Recent-N-days mode: stop when `page > 25` (hard limit: 250 records)
- Stop early when the current page returns an empty event list

## Date filtering

- Single-day mode: keep events where `createdAt[:10] == report_date`
- Recent-N-days mode: keep events where `range_start_date <= createdAt[:10] <= report_date`
- `report_date` defaults to yesterday unless the caller explicitly asks for today
- `recent_days` supports `1..7`; `7` maps to "最近一周"

## Source to normalized fields

| Output field | Source field(s) | Rule |
| --- | --- | --- |
| `brief` | `brief`, `description` | Prefer `brief` |
| `createdAt` | `createdAt` | Keep raw timestamp string |
| `originalLink` | `originalLink` | Source detail URL |
| `postTitle` | `postTitle`, `originalTitle` | Prefer `postTitle` |
| `tags` | `tags[].tagName` | Keep unique tag names only |

## Output schema

Output JSON file contains:

- `meta`: run metadata and page-level errors
- `meta.recent_days`, `meta.range_start_date`, `meta.report_date`: time window metadata
- `events`: compact event list (only 5 fields)
