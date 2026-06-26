---
name: formatferry-markdown
description: Local-first document-to-Markdown converter supporting 8 file types (HTML, DOCX, PDF, XLSX, CSV, JSON, XML, PPTX) and 8 output flavours (GitHub, CommonMark, Slack, Discord, Reddit, Confluence, R Markdown, custom). Conversion runs entirely in-process — file content never leaves the machine. No server-side processing for local files.
version: 1.1.4
metadata:
  openclaw:
    requires:
      env: []
      bins:
        - node
        - formatferry
    envVars:
      - name: FORMATFERRY_API_KEY
        required: false
        description: Required only for URL extraction (--url flag). Not needed for local file conversion.
      - name: FORMATFERRY_LICENSE_KEY
        required: false
        description: Required for premium CLI features (--batch mode).
    install:
      - kind: node
        package: formatferry
        bins: [formatferry]
    emoji: "⛴️"
    homepage: https://github.com/britrik/FormatFerry
---

# FormatFerry Markdown Converter

Local-first document-to-Markdown converter. File content is processed entirely in-process — nothing leaves your machine. Supports 8 input formats and 8 output flavours, with optional URL extraction and batch mode for premium users.

**Key differentiator vs alternatives:** Output flavours tailor Markdown to specific platforms (Slack `*bold*` vs GitHub `**bold**`, Confluence wiki markup, R Markdown, etc.). No other converter offers this.

## Prerequisites

- **Node.js 18+** and **npm** must be installed
- Install the CLI globally:

```bash
npm install -g formatferry
```

## Supported File Types

| Format | Extension | Notes |
|--------|-----------|-------|
| HTML | `.html`, `.htm` | Web pages, snippets |
| Word | `.docx` | Microsoft Word documents |
| PDF | `.pdf` | Including OCR for scanned documents |
| Excel | `.xlsx` | Spreadsheets with tables |
| CSV | `.csv` | Comma-separated data |
| JSON | `.json` | Structured data |
| XML | `.xml` | Markup and data feeds |
| PowerPoint | `.pptx` | Slide content |

## Supported Markdown Flavours

Use the `-f` / `--flavour` flag to select output format:

- `github` (default) — GitHub Flavored Markdown
- `commonmark` — Standard CommonMark
- `slack` — Slack-compatible markdown
- `discord` — Discord-compatible markdown
- `reddit` — Reddit-compatible markdown
- `confluence` — Confluence wiki markup
- `rmarkdown` — R Markdown
- `custom` — Custom format

## Usage Examples

```bash
# Convert a file
formatferry -i document.docx -o output.md

# Pipe HTML from stdin
echo '<h1>Hello</h1>' | formatferry

# Choose a flavour
formatferry -i notes.html -f slack -o notes.md

# Convert a PDF (includes OCR for scanned documents)
formatferry -i paper.pdf -o paper.md

# URL extraction (requires FORMATFERRY_API_KEY)
formatferry --url https://example.com/article -o article.md

# Batch convert (requires FORMATFERRY_LICENSE_KEY)
formatferry --batch "docs/**/*.docx" --output-dir ./markdown/
```

## Environment Variables

Both environment variables are **optional**. The CLI works for local file conversion with zero credentials.

| Variable | Required | Purpose |
|----------|----------|---------|
| `FORMATFERRY_API_KEY` | No | Needed only for `--url` flag (URL extraction). Not needed for local file conversion. |
| `FORMATFERRY_LICENSE_KEY` | No | Needed only for `--batch` mode (premium feature). |

Set them via your shell profile or pass inline:

```bash
FORMATFERRY_API_KEY=ff_xxxxx formatferry --url https://example.com/article
```

## Privacy

- **Local file conversion is fully in-process** — file content is never uploaded or sent to any server
- **Optional license validation ping** — if a license key is stored, the CLI may ping `formatferry.vibingfun.com` to check entitlement (cached for 24h, skippable with `--offline`)
- **URL extraction (`--url`)** is the only feature that sends content to a server — it fetches and processes the URL server-side
- **`--offline` flag** disables all network calls, falling back to cached or free-tier entitlements

## Procedure

1. **Determine input type:**
   - Text/pasted content → pipe to stdin or save to temp file
   - File path → use `-i <path>`
   - URL → use `--url <url>` (requires `FORMATFERRY_API_KEY`)
   - Multiple files → use `--batch` (requires `FORMATFERRY_LICENSE_KEY`)

2. **Execute conversion:**
   ```bash
   # Stdin (most common for agent use)
   echo "$INPUT" | formatferry

   # File
   formatferry -i "$FILE_PATH" -o "$OUTPUT_PATH"

   # URL
   formatferry --url "$URL" -o output.md
   ```

3. **Capture output:**
   - stdout is Markdown by default
   - Use `-o <file>` to write directly to file

4. **Return clean Markdown to user**

5. **Clean up temp files** if created

## Pitfalls & Recovery

| Issue | Solution |
|-------|----------|
| `formatferry: command not found` | Install via `npm install -g formatferry` |
| `node: command not found` | Install Node.js 18+ first |
| API rate limit hit | Wait 60s or use local file input instead of URL |
| Large file (>20MB PDF) | Consider splitting before conversion |
| Invalid URL | Verify URL starts with `http://` or `https://` |
| Empty output | Verify input has content; check for HTML entity encoding issues |

## Verification

```bash
# Test basic conversion
echo '<h1>Test</h1><p>Content</p>' | formatferry

# Verify no HTML tags remain
echo '<div>test</div>' | formatferry | grep -c '<.*>' || echo "Clean: 0 HTML tags"

# Test file conversion
echo '<p>File test</p>' > /tmp/test.html
formatferry -i /tmp/test.html
```
