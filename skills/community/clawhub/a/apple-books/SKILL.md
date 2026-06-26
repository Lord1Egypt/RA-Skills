---
name: apple-books
description: Read your Apple Books library, highlights, notes, and reading progress directly from the local SQLite databases on macOS.
homepage: https://clawhub.ai/alexissan/apple-books
metadata: {"clawdbot":{"emoji":"📚","requires":{"bins":["sqlite3"],"os":"darwin"}}}
---

# Apple Books

Query your local Apple Books library on macOS. Read-only access to books, highlights, notes, collections, and reading progress.

## Requirements

- **macOS only** — Apple Books stores data in `~/Library/Containers/com.apple.iBooksX/`
- **Full Disk Access** required for the process running queries (System Settings → Privacy & Security → Full Disk Access)
- **sqlite3** (pre-installed on macOS)
- Apple Books must have been opened at least once (databases are created on first launch)

## Database discovery

The database filenames are consistent across macOS installs, but always resolve them dynamically in case Apple changes them in future versions:

```bash
BKLIBRARY_DB="$(ls ~/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/*.sqlite 2>/dev/null | head -1)"
AEANNOTATION_DB="$(ls ~/Library/Containers/com.apple.iBooksX/Data/Documents/AEAnnotation/*.sqlite 2>/dev/null | head -1)"
```

If either variable is empty, Apple Books has not been set up on this Mac.

> **Important:** These are read-only queries. Never INSERT, UPDATE, or DELETE rows — doing so may corrupt Apple Books data or cause iCloud sync issues.

## List all books

```bash
BKLIBRARY_DB="$(ls ~/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/*.sqlite 2>/dev/null | head -1)"
sqlite3 "$BKLIBRARY_DB" \
  "SELECT ZTITLE, ZAUTHOR, ZGENRE, ZPAGECOUNT, ZREADINGPROGRESS, ZISFINISHED, ZASSETID
   FROM ZBKLIBRARYASSET
   WHERE ZTITLE IS NOT NULL
   ORDER BY ZLASTOPENDATE DESC;"
```

## Search books by title or author

```bash
BKLIBRARY_DB="$(ls ~/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/*.sqlite 2>/dev/null | head -1)"
sqlite3 "$BKLIBRARY_DB" \
  "SELECT ZTITLE, ZAUTHOR, ZGENRE, ZREADINGPROGRESS, ZASSETID
   FROM ZBKLIBRARYASSET
   WHERE ZTITLE IS NOT NULL AND (ZTITLE LIKE '%SEARCH_TERM%' OR ZAUTHOR LIKE '%SEARCH_TERM%')
   ORDER BY ZLASTOPENDATE DESC;"
```

Replace `SEARCH_TERM` with the user's query.

## Currently reading (in progress, not finished)

```bash
BKLIBRARY_DB="$(ls ~/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/*.sqlite 2>/dev/null | head -1)"
sqlite3 "$BKLIBRARY_DB" \
  "SELECT ZTITLE, ZAUTHOR, ZGENRE,
          printf('%.0f%%', ZREADINGPROGRESS * 100) AS progress,
          datetime(ZLASTOPENDATE + 978307200, 'unixepoch', 'localtime') AS last_opened
   FROM ZBKLIBRARYASSET
   WHERE ZTITLE IS NOT NULL
     AND ZREADINGPROGRESS > 0.0
     AND (ZISFINISHED IS NULL OR ZISFINISHED = 0)
   ORDER BY ZLASTOPENDATE DESC;"
```

## Finished books

```bash
BKLIBRARY_DB="$(ls ~/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/*.sqlite 2>/dev/null | head -1)"
sqlite3 "$BKLIBRARY_DB" \
  "SELECT ZTITLE, ZAUTHOR, ZGENRE,
          datetime(ZDATEFINISHED + 978307200, 'unixepoch', 'localtime') AS finished_date
   FROM ZBKLIBRARYASSET
   WHERE ZISFINISHED = 1
   ORDER BY ZDATEFINISHED DESC;"
```

## Get all highlights and notes for a specific book

```bash
AEANNOTATION_DB="$(ls ~/Library/Containers/com.apple.iBooksX/Data/Documents/AEAnnotation/*.sqlite 2>/dev/null | head -1)"
sqlite3 "$AEANNOTATION_DB" \
  "SELECT ZANNOTATIONSELECTEDTEXT, ZANNOTATIONNOTE, ZANNOTATIONSTYLE,
          datetime(ZANNOTATIONCREATIONDATE + 978307200, 'unixepoch', 'localtime') AS created
   FROM ZAEANNOTATION
   WHERE ZANNOTATIONDELETED = 0
     AND ZANNOTATIONASSETID = 'ASSET_ID'
     AND length(ZANNOTATIONSELECTEDTEXT) > 0
   ORDER BY ZPLLOCATIONRANGESTART ASC;"
```

Replace `ASSET_ID` with the book's `ZASSETID` from the library query.

## Get all highlights across all books (with book titles)

```bash
BKLIBRARY_DB="$(ls ~/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/*.sqlite 2>/dev/null | head -1)"
AEANNOTATION_DB="$(ls ~/Library/Containers/com.apple.iBooksX/Data/Documents/AEAnnotation/*.sqlite 2>/dev/null | head -1)"
sqlite3 "$AEANNOTATION_DB" \
  "ATTACH DATABASE '$BKLIBRARY_DB' AS lib;
   SELECT lib.ZBKLIBRARYASSET.ZTITLE, lib.ZBKLIBRARYASSET.ZAUTHOR,
          ZAEANNOTATION.ZANNOTATIONSELECTEDTEXT, ZAEANNOTATION.ZANNOTATIONNOTE,
          datetime(ZAEANNOTATION.ZANNOTATIONCREATIONDATE + 978307200, 'unixepoch', 'localtime') AS created
   FROM ZAEANNOTATION
   JOIN lib.ZBKLIBRARYASSET ON ZAEANNOTATION.ZANNOTATIONASSETID = lib.ZBKLIBRARYASSET.ZASSETID
   WHERE ZAEANNOTATION.ZANNOTATIONDELETED = 0
     AND length(ZAEANNOTATION.ZANNOTATIONSELECTEDTEXT) > 0
   ORDER BY ZAEANNOTATION.ZANNOTATIONCREATIONDATE DESC
   LIMIT 50;"
```

## List collections (shelves)

```bash
BKLIBRARY_DB="$(ls ~/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/*.sqlite 2>/dev/null | head -1)"
sqlite3 "$BKLIBRARY_DB" \
  "SELECT c.ZTITLE, c.ZCOLLECTIONID, COUNT(m.Z_PK) AS book_count
   FROM ZBKCOLLECTION c
   LEFT JOIN ZBKCOLLECTIONMEMBER m ON m.Z_PK IN (
     SELECT Z_PK FROM ZBKCOLLECTIONMEMBER
   )
   WHERE c.ZDELETEDFLAG = 0 AND c.ZTITLE IS NOT NULL
   GROUP BY c.ZCOLLECTIONID
   ORDER BY c.ZTITLE;"
```

## Reading stats

```bash
BKLIBRARY_DB="$(ls ~/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/*.sqlite 2>/dev/null | head -1)"
sqlite3 "$BKLIBRARY_DB" \
  "SELECT
     COUNT(*) AS total_books,
     SUM(CASE WHEN ZISFINISHED = 1 THEN 1 ELSE 0 END) AS finished,
     SUM(CASE WHEN ZREADINGPROGRESS > 0 AND (ZISFINISHED IS NULL OR ZISFINISHED = 0) THEN 1 ELSE 0 END) AS in_progress,
     SUM(CASE WHEN ZREADINGPROGRESS = 0 OR ZREADINGPROGRESS IS NULL THEN 1 ELSE 0 END) AS not_started,
     printf('%.0f%%', AVG(ZREADINGPROGRESS) * 100) AS avg_progress
   FROM ZBKLIBRARYASSET
   WHERE ZTITLE IS NOT NULL;"
```

## Annotation styles

| Style value | Color     |
|-------------|-----------|
| 1           | Green     |
| 2           | Blue      |
| 3           | Yellow    |
| 4           | Pink      |
| 5           | Purple    |

## Annotation types

| Type value | Meaning     |
|------------|-------------|
| 2          | Highlight   |
| 3          | Bookmark    |

## Date handling

Apple Books uses Core Data timestamps (seconds since 2001-01-01). To convert to human-readable:
```sql
datetime(TIMESTAMP_COLUMN + 978307200, 'unixepoch', 'localtime')
```

## Troubleshooting

- **"unable to open database file"** — Grant Full Disk Access to the process (OpenClaw gateway / node) in System Settings → Privacy & Security → Full Disk Access
- **Empty results** — Open Apple Books at least once so macOS creates the databases
- **Stale data** — Apple Books may hold a write lock while open; queries still work in WAL mode but data may lag a few seconds behind the UI

## Notes

- `ZASSETID` is the key that links books to their annotations
- `ZREADINGPROGRESS` is a float from 0.0 to 1.0
- `ZISFINISHED` is 1 when marked as finished, NULL or 0 otherwise
- The `ZLASTOPENDATE` field tracks when the book was last opened
- All queries are **read-only** — never modify these databases
- Audiobooks from Apple Books also appear in this database (`ZISSTOREAUDIOBOOK = 1`)
