---
name: formatferry-markdown
description: "Converts local HTML, DOCX, PDF, XLSX, CSV, JSON, XML and PPTX files (or stdin) to Markdown in 8 flavours (GitHub, CommonMark, Slack, Discord, Reddit, Confluence, Google Docs, R Markdown). Local conversion runs in-process and, with --offline, makes no network calls. Two optional features use the network: --url sends the URL to the FormatFerry API for server-side fetching (needs FORMATFERRY_API_KEY and the user's explicit go-ahead), and a stored license key triggers an entitlement check against formatferry.vibingfun.com unless --offline is passed."
version: 1.1.6
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
        package: formatferry@1.0.51
        bins: [formatferry]
    emoji: "⛴️"
    homepage: https://github.com/britrik/FormatFerry
---

# FormatFerry Markdown Converter

Document-to-Markdown converter. Local files and stdin are converted in-process and never uploaded. Supports 8 input formats and 8 output flavours, with optional network-backed URL extraction and premium batch mode.

**Network use at a glance**

| Mode | Network | What is sent |
|------|---------|--------------|
| Local file / stdin with `--offline` | None | Nothing |
| Local file / stdin without `--offline`, license key stored | `formatferry.vibingfun.com` | License key for an entitlement check (cached 24h) |
| `--url <url>` | FormatFerry API | The URL and API key; the page is fetched and processed server-side |

**Key differentiator vs alternatives:** Output flavours tailor Markdown to specific platforms (Slack `*bold*` vs GitHub `**bold**`, Confluence wiki markup, R Markdown, etc.). No other converter offers this.

## Prerequisites

- **Node.js 18+** and **npm** must be installed
- Install the CLI globally:

```bash
npm install -g formatferry@1.0.51
```

The skill is tested against CLI 1.0.51; install that exact version rather than the latest.

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
echo '<h1>Hello</h1>' | formatferry --offline

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
- **Optional license validation ping** — if a license key is stored, the CLI may contact `formatferry.vibingfun.com` to check entitlement (cached for 24h). `--offline` skips this check
- **URL extraction (`--url`)** sends the URL to the FormatFerry API, which fetches and processes the page server-side. `--offline` does not change this. Never use `--url` for internal, private or signed URLs
- **Credentials** — `formatferry auth` stores API and license keys in the CLI's local config. Prefer the `FORMATFERRY_API_KEY` / `FORMATFERRY_LICENSE_KEY` environment variables for one-off use, and run `formatferry auth --logout` to remove stored keys

## Procedure

1. **Determine input type:**
   - Text/pasted content → pipe to stdin or save to temp file
   - File path → use `-i <path>`
   - URL → only when the user explicitly asks to convert a web page and agrees that the URL is sent to FormatFerry's server; then use `--url <url>` (requires `FORMATFERRY_API_KEY`). Otherwise ask the user for the file
   - Multiple files → use `--batch` (requires `FORMATFERRY_LICENSE_KEY`)

2. **Execute conversion:**
   ```bash
   # Stdin (most common for agent use): always offline
   echo "$INPUT" | formatferry --offline

   # File: always offline
   formatferry --offline -i "$FILE_PATH" -o "$OUTPUT_PATH"

   # URL: only after the user has agreed to server-side fetching
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
| `formatferry: command not found` | Install via `npm install -g formatferry@1.0.51` |
| `node: command not found` | Install Node.js 18+ first |
| API rate limit hit | Wait 60s or use local file input instead of URL |
| Large file (>20MB PDF) | Consider splitting before conversion |
| Invalid URL | Verify URL starts with `http://` or `https://` |
| Empty output | Verify input has content; check for HTML entity encoding issues |

## Verification

```bash
# Test basic conversion
echo '<h1>Test</h1><p>Content</p>' | formatferry --offline

# Verify no HTML tags remain
echo '<div>test</div>' | formatferry --offline | grep -c '<.*>' || echo "Clean: 0 HTML tags"

# Test file conversion
TMP_DIR=$(mktemp -d)
echo '<p>File test</p>' > "$TMP_DIR/test.html"
formatferry --offline -i "$TMP_DIR/test.html"
rm -rf "$TMP_DIR"
```
