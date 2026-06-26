---
name: feishu-book-match
description: Fill book match results (匹配结果) and Amazon links (书籍链接) into a Feishu Bitable by querying Amazon with ISBN. Use when asked to match books, fill 匹配结果, 填充书籍链接, Amazon matching, or similar tasks involving batch-updating a Feishu Bitable with Amazon search results.
---

# Feishu Book Match

Fill 匹配结果 (match color) and 书籍链接 (Amazon detail link) for books in a Feishu Bitable by querying Amazon UK/US with ISBN.

## Step-by-Step Workflow

### 1. Parse the Bitable URL

Use `feishu_bitable_get_meta` on the Feishu wiki/base URL to get `app_token` and `table_id`.

### 2. Confirm Field IDs

Use `feishu_bitable_list_fields` to find the field IDs. Expected field names:
- `ISBN` → field_id (e.g. `fldbjxXubv`)
- `Title` → field_id (e.g. `fld8AkZOXn`)
- `Author` → field_id (e.g. `fldEVOXS5u`)
- `匹配结果` → field_id (e.g. `fldrgtxF6l`)
- `书籍链接` → field_id (e.g. `fldxZrhJeG`)

### 3. Find Unprocessed Records

Use `feishu_bitable_list_records` with `page_size=100`. Filter to records where `匹配结果` is empty. Process in batches.

### 4. Query Amazon (Browser Relay)

Use Chrome browser relay (`profile: "chrome-relay"`):

**Step A: Amazon UK search**
URL: `https://www.amazon.co.uk/s?k={ISBN}`

**Step B: Check results**
- If page shows "No results for your search query in Books" → try Amazon US:
  `https://www.amazon.com/s?k={ISBN}`
- If Amazon US also shows no results → mark 匹配结果 = `🔴 未匹配` → update Bitable → stop for this ISBN

**Step C: Get first result info**
Take the first search result (usually `div[data-cy="title-recipe"]`). Extract:
- **Title**: from the heading inside `div[data-cy="title-recipe"]` or `h2 a span`
- **Author**: from the author line (often contains `by ` text or a link)

### 5. Determine Match Color

Compare Amazon result with Excel `Title` and `Author`:
- 🟢 **完全一致** (green): Title AND Author both match exactly
- 🟡 **可能一致** (yellow): Title matches, Author similar or slightly different
- 🔴 **很可能不同** (red): Title or Author clearly different

**Common causes of yellow:**
- Amazon shows audiobook narrator alongside author (e.g., "Ian Rankin and James Macpherson" where Macpherson is the narrator)
- Slight title variations (subtitle differences, punctuation)
- Author name formatting differences

### 6. Get Detail Link

Execute in the browser tab:
```javascript
() => {
  const el = document.querySelector('div[data-cy="title-recipe"] a');
  return el ? el.href : null;
}
```

**Strip query parameters** — keep only the clean path:
```
# FROM: https://www.amazon.co.uk/Art-Edible-Flowers-.../dp/B07BQD9D5N?ref=...&dib=...
# TO:   https://www.amazon.co.uk/Art-Edible-Flowers-.../dp/B07BQD9D5N
```

### 7. Update Bitable Record

Use `feishu_bitable_update_record`:
```json
{
  "匹配结果": "完全一致",
  "书籍链接": "https://www.amazon.co.uk/.../dp/ASIN"
}
```

## Known Field IDs (RIVERSIDE_BOOKS Table)

| Field | field_id |
|-------|----------|
| ISBN | fldbjxXubv |
| Title | fld8AkZOXn |
| Author | fldEVOXS5u |
| 匹配结果 | fldrgtxF6l |
| 书籍链接 | fldxZrhJeG |

> These are stable for the specific table `tblskx3DEQkwhc9r`. Always verify with `feishu_bitable_list_fields` if unsure.

## Batch Processing

For large tables (2000+ records):
1. Process in batches of 20–50
2. Use `feishu_bitable_list_records` with `page_token` for pagination
3. Filter out already-processed records (匹配结果 not empty)
4. Report progress after each batch
5. Use background exec or cron if the task needs to run unattended

## Tips

- **ISBN normalization**: Some ISBNs have dashes; Amazon search works better with dashes removed (e.g., `978-0857834768` → `9780857834768`)
- **CD/audiobook**: Category 1 = "CD" often indicates audiobook — author on Amazon may differ (narrator vs author)
- **No results on .co.uk**: Always fall back to `.com` before marking as unmatched
- **Chrome relay tab reuse**: If a tab is already on the right URL, navigate to the new ISBN URL directly rather than opening a new tab
