---
name: chrome-bookmarks
description: Search, browse, and open Chrome bookmarks via AI assistant. Trigger when user asks to find/open a bookmarked URL, search their Chrome bookmarks by keyword, browse bookmark folders, or says something like "open my TAPD bookmark" or "find the bookmark for X". Reads the local Chrome Bookmarks JSON file directly — no extensions or external services required.
description_zh: Chrome 书签搜索与打开
description_en: Chrome Bookmark Search & Open
license: MIT
version: "1.0.0"
disable: false
agent_created: true
metadata:
  openclaw:
    emoji: "🔖"
    category: productivity
  clawdbot:
    emoji: "🔖"
    requires:
      bins:
        - python3
---

# chrome-bookmarks

Search, browse, and open Chrome bookmarks directly from the local Bookmarks JSON file.

## When to use

- User asks to find or search their Chrome bookmarks by keyword
- User wants to open a bookmarked URL (e.g., "打开我收藏的 TAPD 链接", "open my GitHub bookmark")
- User wants to browse bookmark folders (e.g., "看看我书签栏 Code 文件夹下有什么")
- User wants to see the overall bookmark tree structure

## Prerequisites

- Chrome browser installed (data at `~/Library/Application Support/Google/Chrome/`)
- macOS (uses `open` command to launch URLs) — for Linux, replace `open` with `xdg-open`
- Python 3.8+ (system python3)

## Steps

### 1. Search bookmarks by keyword

```bash
python3 @scripts/chrome_bookmarks.py search "<keyword>" --limit 10
```

- `--limit N`: max results (default 20)
- `--folder <name>`: restrict search to a specific folder

Example: Search for TAPD-related bookmarks

```bash
python3 @scripts/chrome_bookmarks.py search "TAPD" --limit 10
```

### 2. Browse bookmark folder contents

```bash
python3 @scripts/chrome_bookmarks.py list --folder "<folder_name>" --depth 2
```

- Omit `--folder` to list all top-level items
- `--depth N`: how deep to traverse the tree (default 2)

Example: List items in the "Code" folder

```bash
python3 @scripts/chrome_bookmarks.py list --folder "Code" --depth 2
```

### 3. Show bookmark tree structure

```bash
python3 @scripts/chrome_bookmarks.py tree --depth 1
```

Shows top-level folders with bookmark counts. Increase `--depth` for more detail.

### 4. Open a bookmark in the browser

```bash
python3 @scripts/chrome_bookmarks.py open "<keyword>"
```

Opens the **first matching** bookmark URL in the default browser using the `open` command.

Example:

```bash
python3 @scripts/chrome_bookmarks.py open "iWiki"
```

This will find the first bookmark whose name or URL contains "iWiki" and open it.

## Typical workflow

1. **User asks to find a bookmark** → run `search` with the keyword
2. **Present results to user** — show name, URL, and folder path
3. **User picks one** → run `open` with a more specific keyword or confirm the exact name
4. **Bookmark opens in Chrome**

## Pitfalls

- Chrome must not be running a profile lock that prevents reading the Bookmarks file (rare on macOS — the file is always readable)
- The Bookmarks file is only updated when Chrome writes it (on bookmark changes or browser close). Very recent additions may not appear until Chrome flushes to disk.
- For users with multiple Chrome profiles, the script auto-detects `Default` first, then `Profile 1`, etc.
- The `open` command only works on macOS. On Linux, the script would need to use `xdg-open` instead.
- With large bookmark collections, the `open` command opens the **first** match. Use `search` first to verify the right bookmark if unsure.

## Verification

After running `search`, confirm the output is a JSON array of bookmark objects with `name`, `url`, `folder`, and `path` fields. After running `open`, confirm the output contains `"opened": true`.

## Script reference

- `@scripts/chrome_bookmarks.py` — Main CLI script (Python 3, zero external dependencies)
