# FormatFerry CLI Reference

## Full Help Output (v1.0.27)

```
Usage: formatferry [options] [command]

Convert documents (HTML, DOCX, PDF, XLSX, CSV, JSON, XML, PPTX) to Markdown

Options:
  -V, --version            output the version number
  -i, --input <path>       Input file path
  -o, --output <path>      Output file path
  -f, --flavour <format>   Markdown flavour (github, commonmark, slack, discord,
                           reddit, confluence, rmarkdown, custom) (default:
                           "github")
  --url <url>              Fetch article from URL (requires FORMATFERRY_API_KEY)
  --batch <glob>           Batch convert files (requires FORMATFERRY_LICENSE_KEY)
  --output-dir <dir>       Output directory for batch mode
  --offline                Skip entitlement check (use cached or free tier)
  --timeout <ms>           License server timeout in milliseconds (default: 2000)
  -h, --help               display help for command

Commands:
  auth [options]           Manage API key and license key authentication
```

## Auth Commands

```
Usage: formatferry auth [options]

Manage API key and license key authentication

Options:
  --api-key <key>        Set API key (for --url extraction)
  --license-key <key>    Set license key (for --batch mode)
  --status               Show current authentication status
  --logout               Remove stored credentials
  -h, --help             display help for command
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

| Flavour | Flag | Notes |
|---------|------|-------|
| GitHub | `-f github` | Default — GitHub Flavored Markdown |
| CommonMark | `-f commonmark` | Standard CommonMark spec |
| Slack | `-f slack` | Slack-compatible markdown |
| Discord | `-f discord` | Discord-compatible markdown |
| Reddit | `-f reddit` | Reddit-compatible markdown |
| Confluence | `-f confluence` | Confluence wiki markup |
| R Markdown | `-f rmarkdown` | R Markdown format |
| Custom | `-f custom` | User-defined format |

## Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `FORMATFERRY_API_KEY` | No | Required for `--url` flag (URL extraction). Not needed for local files. |
| `FORMATFERRY_LICENSE_KEY` | No | Required for `--batch` mode (premium feature). |

## Example Outputs

### Input (HTML)
```html
<h1>Title</h1>
<p>A paragraph with <strong>bold</strong> and <em>italic</em>.</p>
<ul>
  <li>Item 1</li>
  <li>Item 2</li>
</ul>
```

### Output (GitHub format — default)
```markdown
# Title

A paragraph with **bold** and _italic_.

- Item 1
- Item 2
```

### Output (Slack format)
```markdown
*Title*

A paragraph with *bold* and _italic_.

• Item 1
• Item 2
```

### Output (Discord format)
```markdown
**Title**

A paragraph with **bold** and *italic*.

• Item 1
• Item 2
```

## Exit Codes

- `0` — Success
- `1` — Error (invalid input, missing file, auth failure, etc.)

## Version History

- **1.0.27** — Current release. Added JSON, XML, PPTX support; `FORMATFERRY_LICENSE_KEY` env var; batch mode improvements.
- **1.0.x** — Added OCR for scanned PDFs, expanded flavour support.
- **0.1.x** — Initial releases (basic HTML/DOCX/PDF/XLSX/CSV conversion).
