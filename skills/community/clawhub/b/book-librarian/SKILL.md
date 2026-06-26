---
name: book-librarian
version: 1.0.1
description: "Manage reading life: recommend books, track reads, move wishlist to library, and suggest what to read next based on mood."
---

# Book Librarian

Use when the user asks about books, reading recommendations, what to read next, or wants to update their reading tracker.

## Initialization

**Only runs if files are missing.** Existing users skip this entirely.

When ANY book-related trigger fires:
1. Check if `books/books_library.csv` exists
2. Check if `books/books_wishlist.csv` exists
3. Check if `memory/library.md` exists
4. If **any** are missing:
   - Ask: *"Your reading tracker isn't set up yet. Want me to create it?"*
   - If **no**: say *"No problem. Just ask again when you're ready."* and stop.
   - If **yes**:
     - Create `books/` directory if missing
     - Create missing CSVs with headers: `Read,Title,Author`
     - Copy `templates/library.md` to `memory/library.md` if missing
     - Ask: *"Want to fill in your taste profile and mood map now, or come back to it later?"*
     - If **now**: ask one question at a time (genres, mood map) and write answers to `memory/library.md`
     - If **later**: say *"Got it. I'll use what I learn from your recommendations to fill it in over time."*
5. Proceed with the triggered workflow.

## Files

- `books/books_library.csv` — owned books. Columns: `Read` (Y/blank), `Title`, `Author`
- `books/books_wishlist.csv` — wanted books. Columns: `Title`, `Author`
- `memory/library.md` — taste profile, mood map, reading notes, patterns
- `templates/library.md` — starter template for new users (copied to `memory/library.md` on init)

## Triggers

- "What should I read?"
- "Recommend a book"
- "I finished..." / "I started..."
- "Add to wishlist" / "Move to library"
- "What's on my wishlist?"
- "I bought..."
- "Mark as read"

## Workflows

### Recommendation Priority Rules

**Default order for all recommendations:** `library → wishlist → new`

1. **Library first** — Check `books/books_library.csv` for unread books (Read != Y)
2. **Wishlist second** — Check `books/books_wishlist.csv` for wanted books
3. **New last** — Only search for and recommend books not in either file

### Recommend what to read next

1. Check `library.md` for current book and estimated finish
2. Ask or read stated mood if not provided
3. Check `books/books_library.csv` for **unread books** (Read != Y) — suggest from library first
4. If no good match in library, check `books/books_wishlist.csv`
5. If still no match, search for new books not in either CSV
6. Match mood to `library.md` mood map

### Recommend new books (not in CSVs)

1. Read `library.md` taste profile and reading patterns
2. Read `books/books_library.csv` and `books/books_wishlist.csv` to avoid duplicates
3. Search web for books matching taste + **not already in either file**
4. Return 2-3 recommendations with *why* they fit

### Recommend for a specific mood or genre

1. Match mood/genre to `library.md` mood map
2. Check `books/books_library.csv` for unread books matching the mood — suggest from library first
3. If no good match, check `books/books_wishlist.csv`
4. If still no match, search for new books
5. Reference the mood explicitly ("Since you wanted something gothic...")

### Mark as read

1. Read `books/books_library.csv` — set `Read` = Y for matching Title/Author
2. Append one-line note to `library.md` under `## Reading Log` with date + brief thought/rating
3. If part of a series, update series progress in `library.md`

### Move wishlist → library

1. Read `books/books_wishlist.csv` and `books/books_library.csv`
2. Append book to `books/books_library.csv` with Read = blank
3. Remove from `books/books_wishlist.csv`
4. Update `library.md` acquisition queue if present

## Response Style

- **NO SPOILERS.** Never reveal plot points, twists, endings, or character fates. Hooks and premise only.
- Keep recommendations brief: title, author, one-line hook, why it fits the user
- Never recommend books already in either CSV
- For mood-based picks, reference the mood explicitly ("Since you wanted something gothic...")
- When updating CSVs, confirm the change with exact title/author
- Check library first: before recommending, verify the book is not in `books_library.csv` or `books_wishlist.csv`

## Taste Drift

If the user mentions loving/hating a book outside the normal pattern, append a note to `library.md` taste profile. This is how the system learns.
