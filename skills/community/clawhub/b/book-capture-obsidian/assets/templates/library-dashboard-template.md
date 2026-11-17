# Library Dashboard

- Total books: `{{total_books}}`
- To read: `{{to_read_count}}`
- Reading: `{{reading_count}}`
- Read: `{{finished_count}}`
- Inbox (captured, not shelved yet): `{{inbox_count}}`

## By shelf

{{shelf_table}}

## Recently added

```dataview
TABLE author, shelf, year
FROM "{{notes_dir}}"
WHERE contains(tags, "book")
SORT file.ctime DESC
LIMIT 20
```

## Currently reading

```dataview
TABLE author, year
FROM "{{notes_dir}}"
WHERE contains(list({{reading_shelves}}), shelf)
SORT file.mtime DESC
```
