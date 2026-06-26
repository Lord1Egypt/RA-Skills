### Example Long-PDF Reading Plan

Input file:

`/path/to/report.pdf`

Planning result:

- Total pages: 60
- Mode: `segmented_read`
- Recommended segment length: 10 pages
- Total segments: 6
- Checkpoint frequency: every 3 segments

Recommended next steps:

- Read segment 1 first
- Update session state after completion
- Continue segment by segment instead of processing all 60 pages at once

If the file exceeds 500 pages:

- the mode will switch to `book_mode`
- the skill will prefer sequential segmented reading
- the full book will not be extracted into context by default
