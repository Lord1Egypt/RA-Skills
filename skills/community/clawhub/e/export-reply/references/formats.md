# Format Reference

## Markdown (`md`)

- **Zero install** — always available
- Preserves all headings, code blocks, tables, bold/italic
- Best for: developers, version control, Obsidian/Notion import
- Output encoding: UTF-8
- Filename suffix: `.md`

## Plain Text (`txt`)

- **Zero install** — always available
- Strips all Markdown syntax → plain text
- Best for: email body, legacy systems, minimal readers
- Output encoding: UTF-8
- Filename suffix: `.txt`

## HTML (`html`)

- **Zero install** — graceful degradation if `markdown` lib absent
  - With `pip3 install markdown`: full Markdown rendering (fenced code, tables, TOC)
  - Without: content wrapped in `<pre>` with HTML-escaped text
- Self-contained single file with embedded CSS (clean typography, responsive)
- Best for: browser viewing, sharing, archiving with styling
- Filename suffix: `.html`

```bash
pip3 install markdown   # optional — improves rendering quality
```

## PDF (`pdf`)

Four-tier fallback strategy (tries in order):

### Tier 1: Chrome / Chromium headless (recommended, zero extra install)
Renders the HTML export through a real browser engine. Best CJK support, best typography.
- Detected automatically from common install paths:
  - macOS: `/Applications/Google Chrome.app`
  - Linux: `/usr/bin/google-chrome`, `/usr/bin/chromium-browser`
- No extra Python packages needed
- Produces compressed, multi-page PDF with embedded fonts

### Tier 2: weasyprint
```bash
pip3 install weasyprint
```
Full CSS support, pure Python, good CJK via system fonts.

### Tier 3: pdfkit (requires system binary)
```bash
pip3 install pdfkit
brew install wkhtmltopdf   # macOS
# or: apt install wkhtmltopdf  (Linux)
```

### Tier 4: fpdf2 (pure Python, always installable)
```bash
pip3 install fpdf2
```
Plain-text rendering. CJK auto-detected from system fonts:
- macOS: `/Library/Fonts/Arial Unicode.ttf`
- Linux: `/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc`

Falls back to Helvetica (ASCII placeholder `[CJK]`) if no CJK font found.

**Known fpdf2 limitation**: Fullwidth punctuation (：，。) is normalized to ASCII equivalents.

If no PDF method available → error message with install commands; offer HTML as immediate alternative.

## DOCX (`docx`)

- Requires `python-docx`
  ```bash
  pip3 install python-docx
  ```
- Parses Markdown headings (H1–H6), bullet lists, numbered lists, paragraphs
- Adds title + export timestamp metadata
- Best for: MS Word, WPS Office, Google Docs import
- Filename suffix: `.docx`

## All (`all`)

Exports all five formats into the target directory.
- Creates directory if needed
- Reports success/failure per format independently
- Returns list of successfully created paths
