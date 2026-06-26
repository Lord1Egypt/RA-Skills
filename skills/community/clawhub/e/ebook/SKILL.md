---
version: "1.0.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
description: "Manage ebook collections, track reading progress, and export highlights using bash and Python. Use when cataloging books, logging reading sessions, or organizing digital libraries."
---

# Ebook — Digital Book Collection & Reading Tracker

A comprehensive ebook management tool for cataloging digital books, tracking reading progress, managing highlights and annotations, rating and reviewing books, and exporting your library. All data is stored locally in JSONL format for portability and privacy.

## Prerequisites

- Python 3.6+
- Bash 4+

## Data Storage

All ebook records, reading sessions, highlights, and reviews are stored in `~/.ebook/data.jsonl`. Each record is a JSON object with fields including `id`, `type` (book, session, highlight, review), `title`, `author`, `format`, `pages`, `progress`, `created_at`, and additional type-specific fields.

## Commands

Run via: `bash scripts/script.sh <command> [options]`

| Command | Description |
|---|---|
| `add` | Add a new ebook to the collection with title, author, format, and page count |
| `list` | List all ebooks in the collection with optional filters by author, format, or status |
| `search` | Search ebooks by title, author, tag, or keyword across all fields |
| `update` | Update metadata for an existing ebook (title, author, tags, status) |
| `delete` | Remove an ebook from the collection by ID |
| `read` | Log a reading session with start page, end page, and duration |
| `progress` | Show reading progress for a specific book or all books |
| `highlight` | Add a highlighted passage or annotation linked to a book and page |
| `review` | Add or update a rating (1-5 stars) and review text for a book |
| `stats` | Show reading statistics: total books, pages read, time spent, averages |
| `export` | Export the library or highlights to JSON, CSV, or Markdown format |
| `help` | Show usage information |
| `version` | Print the tool version |

## Usage Examples

```bash
# Add a new ebook
bash scripts/script.sh add --title "Deep Work" --author "Cal Newport" --format epub --pages 296 --tags "productivity,focus"

# List all books
bash scripts/script.sh list

# List only unread books
bash scripts/script.sh list --status unread

# Search by author
bash scripts/script.sh search --author "Newport"

# Search by keyword
bash scripts/script.sh search --query "productivity"

# Update book metadata
bash scripts/script.sh update --id abc123 --status reading --tags "self-help,focus"

# Delete a book
bash scripts/script.sh delete --id abc123

# Log a reading session (30 minutes, pages 1-45)
bash scripts/script.sh read --id abc123 --start-page 1 --end-page 45 --duration 30

# Check progress
bash scripts/script.sh progress --id abc123

# Add a highlight
bash scripts/script.sh highlight --id abc123 --page 42 --text "The key to developing deep work is..."

# Write a review
bash scripts/script.sh review --id abc123 --rating 5 --text "Transformative book on focused work"

# View reading stats
bash scripts/script.sh stats

# Export library to markdown
bash scripts/script.sh export --format md --output library.md

# Export highlights to CSV
bash scripts/script.sh export --format csv --type highlights --output highlights.csv
```

## Output Format

`list` and `search` return formatted tables to stdout. `progress` shows a progress bar with percentage. `stats` returns a summary with totals and averages. `export` writes to the specified file and confirms the path. All metadata commands return JSON.

## Notes

- Supported ebook formats: `epub`, `pdf`, `mobi`, `azw3`, `txt`, `djvu`.
- Book statuses: `unread`, `reading`, `finished`, `abandoned`, `wishlist`.
- Reading sessions are linked to books by ID; multiple sessions per book are supported.
- Highlights include page number, text content, and optional color tag.
- The `stats` command calculates: total books, books by status, total pages read, total reading time, average pages per session, and reading streak.
- Export formats: `json` (full data), `csv` (tabular), `md` (Markdown with headers and lists).
- All IDs are auto-generated 8-character hex strings.

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
