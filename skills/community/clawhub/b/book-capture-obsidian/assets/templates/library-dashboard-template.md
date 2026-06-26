# Library Dashboard

## Overview

- Total books: `{{total_books}}`
- To read: `{{to_read_count}}`
- Reading: `{{reading_count}}`
- Finished: `{{finished_count}}`
- Needs review: `{{needs_review_count}}`

## Recently Added

```dataview
TABLE author, status, shelf, date_read
FROM "6. Library"
SORT file.ctime DESC
LIMIT 20
```

## Currently Reading

```dataview
TABLE author, shelf, year
FROM "6. Library"
WHERE status = "reading"
SORT file.mtime DESC
```

## Needs Review

```dataview
TABLE author, source, shelf
FROM "6. Library"
WHERE needs_review = true
SORT file.mtime DESC
```
