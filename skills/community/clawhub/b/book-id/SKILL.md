---
name: book-id
description: "Catalog books from photos or text. Trigger on: book photo, catalog book, log book, add to library."
---
# Book Cataloger

## ICM Contract
| | |
|---|---|
| **Layer 3 inputs** | `SOUL.md` (32-property book schema) |
| **Layer 4 inputs** | Photo from `media/inbound/` or user-provided text |
| **Process** | Identify book → web search OpenLibrary/Wikipedia → check for duplicates in `Files/Books/` → write note → save photo → run fix-md.sh |
| **Layer 4 outputs** | `Files/Books/Title - Author.md`, photo saved to `Files/Photos/Books/Title - Author.jpg` → vault-push to `HumanVault/Knowledge Atlas/Outside Knowledge/Books/` |

---

## STEP 0 — READ THE COVER FIRST (mandatory before anything else)

A photo was provided. Before doing anything:
1. Look at the book cover in the image
2. Read the TITLE exactly as printed on the cover
3. Read the AUTHOR exactly as printed on the cover
4. State them explicitly: "I can see: Title = X, Author = Y"

If you cannot read the cover clearly → say "I cannot read the cover. Please send a clearer photo." DO NOT proceed.
NEVER catalog a book you have not confirmed from the image. NEVER guess or substitute another book.

---

## NON-NEGOTIABLE: WRITE ALL 32 PROPERTIES

Every single one of the 32 properties below MUST appear in the output, in exact order.
Empty value = leave blank after the colon. DO NOT omit any property line.
A note with missing properties is BROKEN. Obsidian will silently fail.

WRONG — omitting unknowns:
```yaml
type: book
title: The Stranger
author:
  - "Camus, Albert"
tags:
  - book
```

WRONG — inline arrays:
```yaml
author: ["Camus, Albert"]
tags: [book, fiction]
```

RIGHT — all 32 properties, 2-space indent lists, blanks included:
```yaml
type: book
title: The Stranger
subtitle:
original_title: L'Étranger
author:
  - "Camus, Albert"
translator:
publisher: Vintage International
year: 1989
year_original: 1942
edition:
isbn_13: "9780679720201"
isbn_10:
pages: 123
language: English
original_language: French
format: Paperback
series:
genre:
  - fiction
category:
subjects:
  - absurdism
audience: Adult
condition:
status: owned
rating:
cover: https://covers.openlibrary.org/b/isbn/9780679720201-L.jpg
date_added: 2026-04-22
wikipedia: https://en.wikipedia.org/wiki/The_Stranger_(Camus_novel)
goodreads: https://www.goodreads.com/book/show/49552.The_Stranger
openlibrary: https://openlibrary.org/works/OL46933W
aliases:
cssclass: book
tags:
  - book
  - fiction
  - author/camus
```

WRITE THE BODY SECTION TOO. Do not skip it. The body section is mandatory.

## WORKFLOW
1. **READ THE COVER** — state title and author explicitly (Step 0 above)
2. Web search: title + author on OpenLibrary, Wikipedia, Goodreads
3. Check workspace/Files/Books/ for duplicates (title + author match)
4. If duplicate: tell Pooh. If new: write file.
5. Save to: `workspace/Files/Books/Title - Author.md` (filename format: Title first, then Author, ASCII only)
   Save photo: cp "/home/node/.openclaw/media/inbound/[FILE]" "/home/node/.openclaw/workspace/Files/Photos/Books/Title - Author.jpg"
6. Run: bash /home/node/.openclaw/workspace/fix-md.sh "[FILEPATH]"
7. Reply with the full file path and a one-line summary
8. Ask: "Push to vault? (yes/no)" — do NOT push unless Pooh confirms

## FRONTMATTER TEMPLATE - COPY EXACTLY

---
type: book
title: "Book Title"
subtitle:
original_title:
author:
  - "LastName, FirstName"
translator:
publisher:
year: 1956
year_original:
edition:
isbn_13:
isbn_10:
pages: 147
language: Spanish
original_language:
format: Paperback
series:
genre:
  - "Fiction"
  - "Philosophy"
category:
subjects:
  - "French literature"
audience: Adult
condition:
status: owned
rating:
cover:
date_added: 2026-04-06
wikipedia:
goodreads:
openlibrary:
aliases:
cssclass: book
tags:
  - book
  - fiction
  - author/camus
---

## BODY TEMPLATE - COPY EXACTLY

# Title

**By** [[LastName, FirstName]]
**Published** YEAR by Publisher
**Format** Paperback | **Language** Spanish

## Synopsis

2-3 sentences about the book from web search.

## About the Author

[[LastName, FirstName]] 1-2 sentence bio from web search.

## Details

| Field | Value |
| --- | --- |
| Publisher | Name |
| Pages | 000 |
| Language | Language |
| Format | Format |
| ISBN | 0000000000000 |

## Themes

Keywords: theme1, theme2, theme3.

## Personal Notes

Photo: [[Photos/Books/Title - Author.jpg]]

## Quotes



## Related

- [[Related Book]]

## CRITICAL REMINDERS
- author MUST be a list: 2-space indent, dash, space, quoted name
- genre MUST be a list: 2-space indent, dash, space, quoted genre
- tags MUST be a list: 2-space indent, dash, space, lowercase no quotes
- status: always "owned"
- cssclass: always "book"
- rating: always empty
- year and pages: numbers only, no quotes
- No parentheses () or brackets [] in any values
- Filenames: `Title - Author.md` format — Title first, then Author. ASCII only, no accents.
- Leave blank for unknown. NEVER write "Unknown"
- ALWAYS web search before writing

## COVER IMAGE
1. Search: https://openlibrary.org/search.json?title=[TITLE]&author=[AUTHOR]&limit=5
2. Verify title AND author match in results
3. Build URL: https://covers.openlibrary.org/b/isbn/[ISBN]-M.jpg or /b/id/[COVER_ID]-M.jpg
4. Any size works (-S, -M, -L) — pick whichever is clear and available
5. Exact edition match is ideal, but a generic relevant cover is acceptable
6. ONLY use OpenLibrary URLs. NEVER Amazon, Google, or descriptions.
7. If no covers exist at all on OpenLibrary, leave cover: blank

## FORBIDDEN
- No parentheses () or brackets [] in property values
- No accented characters in filenames
- No "Unknown" or "N/A" anywhere
- No guessing. If unsure, ASK Pooh.
- No skipping web search
- No writing author/genre/tags as plain strings instead of lists
