# Command Map

| Command | Description | Required Flags | Optional Flags |
| --- | --- | --- | --- |
| `info` | Check if a specific date is a holiday/workday/调休 | `--date` | - |
| `year` | List all holidays and 调休 for a year | - | `--year` |
| `batch` | Check multiple dates at once | `--dates` | - |
| `next` | Find the next holiday or workday after a date | `--date` | `--type` |

## Flag Details

| Flag | Format | Example |
| --- | --- | --- |
| `--date` | `YYYY-MM-DD` | `2026-02-17` |
| `--year` | `YYYY` (defaults to current year) | `2026` |
| `--dates` | Comma-separated `YYYY-MM-DD` | `2026-02-16,2026-02-17,2026-02-18` |
| `--type` | `Y` (holiday) or `N` (workday) | `Y` |

## Exit Codes
- `0`: success
- `2`: input or config error
- `3`: network / timeout / HTTP transport error
- `4`: API business error
- `5`: unexpected internal error

## API Base URL
- `https://timor.tech/api/holiday`
- No API key required.
