[中文](README_CN.md) | English

# feishu-sheet-links

Extract all hyperlinks from a public Feishu spreadsheet — across **all sheet tabs** — and optionally batch-download the linked articles as Markdown files.

## Why This Exists

Feishu spreadsheets lazy-load each sheet's data model only when that tab is activated in the browser. Standard scraping approaches miss every sheet except the first one. This tool uses Chrome DevTools Protocol (CDP) to programmatically activate each sheet, wait for its internal JavaScript model to populate, then extract links from two different Feishu storage formats (`url-type` and `mention-type`).

## Requirements

- [Bun](https://bun.sh) runtime
- Google Chrome (or Chromium)

**Zero npm dependencies.** No `npm install` needed — only Bun and Chrome.

## Use as a Claude Code Skill

Copy the entire repo into your Claude Code skills directory:

```bash
cp -r feishu-sheet-links ~/.claude/skills/
```

Then invoke it in Claude Code:

```
/feishu-sheet-links https://your-feishu-doc.feishu.cn/wiki/...
```

See [SKILL.md](SKILL.md) for the full skill interface.

## Use as Standalone Scripts

**Step 1 — Extract links from all sheets:**

```bash
npx -y bun scripts/main.ts "https://your-feishu-doc.feishu.cn/wiki/..." -o links.json
```

**Step 2 — Batch download the linked articles as Markdown:**

```bash
npx -y bun scripts/download.ts links.json -o ./articles -c 5
```

## Usage

### main.ts — Extract links

```
bun scripts/main.ts <spreadsheet-url> [-o output.json]
```

| Argument | Default | Description |
|----------|---------|-------------|
| `<spreadsheet-url>` | — | Public Feishu wiki or spreadsheet URL |
| `-o <file>` | `feishu-sheet-links.json` | Output JSON path |

**Output format:**

```json
{
  "Sheet1": [{ "text": "Article Title", "url": "https://..." }],
  "Sheet2": [...]
}
```

### download.ts — Batch download articles

```
bun scripts/download.ts <links.json> [-o output-dir] [-c concurrency] [--max-wait ms]
```

| Option | Default | Description |
|--------|---------|-------------|
| `-o <dir>` | `./feishu-articles` | Output directory |
| `-c <n>` | `5` | Concurrent downloads |
| `--max-wait <ms>` | `20000` | Per-URL timeout |

**Resume support:** Progress is saved after each URL. Re-running skips already-downloaded files.

## How It Works

1. Connects to an existing Chrome instance if one is already running (ports 64023, 9222, 9229), otherwise launches its own
2. Opens the spreadsheet to discover all sheet IDs from `spreadApp.collaborativeSpread._spread.sheetIdToIndexMap`
3. For each sheet, opens a dedicated tab at `?sheet=<id>`, calls `setActiveSheetIndex()` to trigger lazy loading, and waits for `sheet._dataModel.contentModel` to populate
4. Extracts links from both storage formats:
   - **url-type:** `contentModel.link.idToRef._map` (whole-cell hyperlinks)
   - **mention-type:** `contentModel.segmentModel.table` (inline rich-text links)

## Environment Variables

| Variable | Description |
|----------|-------------|
| `FEISHU_CHROME_PATH` | Custom Chrome executable path |
| `FEISHU_CHROME_PROFILE` | Custom Chrome profile directory |

## Notes

- Works with **public** Feishu documents (no login required)
- Each sheet tab takes 8–15 seconds to load; timeouts are set generously
- Chrome profile is isolated from your default profile: `~/Library/Application Support/feishu-sheet-links/chrome-profile` (macOS)

## License

MIT
