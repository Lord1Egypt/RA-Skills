---
name: feishu-sheet-links
description: Extract all hyperlinks from a public Feishu spreadsheet across all sheet tabs, and optionally batch-download the linked articles as Markdown files. Use when the user shares a Feishu URL (feishu.cn/wiki or feishu.cn/sheets) and wants to extract links, scrape article titles, collect URLs from a Feishu doc, download content from Feishu, or build a local copy of Feishu articles. Also use when the user says things like "帮我下载飞书的链接", "把飞书表格里的链接提取出来", or "下载飞书文章".
---

# feishu-sheet-links

Extracts all hyperlinks from every sheet tab of a public Feishu spreadsheet, then optionally batch-downloads the linked articles as Markdown files.

## Workflow

When invoked, follow these steps:

### Step 1 — Get the URL

If the user has already provided a Feishu URL, use it. Otherwise ask:
> "请提供飞书多维表格的链接（公开可访问的）"

Confirm the URL looks like `https://*.feishu.cn/wiki/...` or `https://*.feishu.cn/sheets/...`.

### Step 2 — Extract links

Resolve the skill directory:
```bash
SKILL_DIR="$(find ~/.claude/skills /workspace/.claude/skills -maxdepth 1 -name feishu-sheet-links -type d 2>/dev/null | head -1)"
```

Run the extraction script:
```bash
npx -y bun "${SKILL_DIR}/scripts/main.ts" "<spreadsheet-url>" -o feishu-links.json
```

Each sheet tab takes 8–15 seconds to load — let the user know it may take a moment.

### Step 3 — Show a summary

After extraction, show the user a summary:
- How many sheets were found
- How many links per sheet (with sheet names)
- Total link count

Example:
```
Found 4 sheets, 127 links total:
- 1月: 32 links
- 2月: 28 links
- 3月: 35 links
- 4月: 32 links

Saved to: feishu-links.json
```

### Step 4 — Offer to download articles

Ask the user if they want to download the linked articles as Markdown:
> "是否需要批量下载这些文章为 Markdown 文件？"

If yes, ask for an output directory (default: `./feishu-articles`), then run:
```bash
npx -y bun "${SKILL_DIR}/scripts/download.ts" feishu-links.json \
  -o <output-dir> \
  -c 5 \
  --max-wait 20000
```

Download supports resume — if interrupted, re-running skips already-downloaded files.

## Error Handling

| Situation | Action |
|-----------|--------|
| Document is private / requires login | Tell the user — this tool only works with public Feishu docs |
| Chrome not found | Ask user to install Chrome, or set `FEISHU_CHROME_PATH` |
| A sheet times out | Warn and continue — other sheets will still be extracted |
| Zero links found | Confirm the URL is correct and the doc is publicly accessible |

## How It Works

1. Reuses an existing Chrome instance if available (ports 64023, 9222, 9229), otherwise launches its own isolated instance
2. Opens the spreadsheet to discover all sheet IDs from `spreadApp.collaborativeSpread._spread.sheetIdToIndexMap`
3. For each sheet, opens a dedicated tab at `?sheet=<id>`, calls `setActiveSheetIndex()` to trigger lazy loading, and waits for `sheet._dataModel.contentModel` to populate
4. Extracts links from two Feishu storage formats:
   - **url-type** — `contentModel.link.idToRef._map` (whole-cell hyperlinks)
   - **mention-type** — `contentModel.segmentModel.table` (inline rich-text links)

## Environment Variables

| Variable | Description |
|----------|-------------|
| `FEISHU_CHROME_PATH` | Custom Chrome executable path |
| `FEISHU_CHROME_PROFILE` | Custom Chrome profile directory |
