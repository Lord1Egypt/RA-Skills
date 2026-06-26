---
name: chrome-bookmark-summarizer
description: Reads Chrome bookmarks and extracts URLs by a user-provided folder name, then generates batch webpage summaries. Use when the user mentions Chrome bookmarks/favorites, bookmark folders, link summarization, or asks to summarize sites under a bookmark folder.
---

# Chrome Bookmark Summarizer

Extract webpages from a Chrome bookmark folder (based on the user-provided folder name) and produce structured summaries.

## When to Use

- The user mentions "Chrome bookmarks", "favorites", "bookmark folder", or "summarize saved links"
- You need to batch-read links by folder name and produce summaries
- You need to filter URLs from a local bookmarks file before summarizing webpage content

## Workflow

1. Confirm input parameters
   - Required: target folder name (for example, `AI Research`)
   - Optional: match mode (`exact` or `contains`)
   - Optional: whether to recurse into subfolders (default: recursive)

2. Run the extraction script (JSON output)

```bash
python3 "scripts/extract_chrome_bookmarks.py" --folder "AI Research"
```

Common options:

```bash
# Fuzzy folder-name matching
python3 "scripts/extract_chrome_bookmarks.py" --folder "AI" --match-mode contains

# If multiple folders share the same name, return only the first match
python3 "scripts/extract_chrome_bookmarks.py" --folder "AI Research" --pick-first

# Extract only direct links (no subfolders)
python3 "scripts/extract_chrome_bookmarks.py" --folder "AI Research" --non-recursive
```

3. Parse output and handle errors
   - `ok=false`: return a clear error to the user (folder not found, invalid path, etc.)
   - `ok=true`: read `results[].urls[]` for downstream summarization

4. Batch webpage summarization
   - Fetch page content for each URL (prefer full body text; fall back to title + short description on failure)
   - Recommended output structure:
     - Page title
     - Core takeaway (1-2 sentences)
     - Key points (2-4 bullets)
     - Relevance to user goal (one sentence)

5. Final aggregation
   - Keep the original bookmark order
   - Add a cross-page comparison at the end:
     - Shared themes
     - Differing viewpoints
     - Recommended reading order

## Output Template

```markdown
## Folder: {folder_name}

### 1) {page_title}
- URL: {url}
- Core takeaway: {summary}
- Key points:
  - {point_1}
  - {point_2}
  - {point_3}
- Relevance: {relevance}

### 2) {page_title}
...

## Cross-Page Summary
- Shared themes: ...
- Differences: ...
- Suggested reading order: ...
```

## Notes

- Default Chrome bookmarks path on macOS:
  - `~/Library/Application Support/Google/Chrome/Default/Bookmarks`
- If the user has multiple Chrome profiles, ask for a specific `Bookmarks` file path and pass it with `--bookmarks`.
- Duplicate folder names may exist; by default all matches are returned. Use `--pick-first` to keep only one.
