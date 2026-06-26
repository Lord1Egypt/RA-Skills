---
name: bookify
description: Convert Markdown files to styled PDF or EPUB ebook using md-bookify. Use when the user wants to generate a PDF document or EPUB ebook from markdown content or files.
source: https://www.npmjs.com/package/md-bookify
version: 2.2.1
argument-hint: <file.md> [pdf|epub]
allowed-tools:
  - Bash(npx md-bookify@2.2.1 *)
  - Bash(npx puppeteer@24 browsers install chrome)
  - Read
  - Glob
---

# Convert Markdown to PDF or EPUB

Use the `md-bookify` npm package via `npx` to convert Markdown files to styled PDF documents or EPUB ebooks.

## Interpreting Arguments

- If `$ARGUMENTS` contains a file path (ends in `.md` or `.markdown`), convert that file
- If `$ARGUMENTS` includes `pdf` or `epub`, use that format (default: PDF)
- If `$ARGUMENTS` is descriptive (e.g. "convert the README to elegant PDF"), parse the intent
- If no file is specified, use Glob to find markdown files and ask which to convert

## PDF Conversion

```bash
npx md-bookify@2.2.1 <input.md> [options]
```

**Options:**
- `-o, --output <path>` — Output PDF file path (default: same name with .pdf extension)
- `-t, --title <title>` — Document title (default: filename)
- `--author <name>` — Author name
- `-f, --format <format>` — Page format: `A4` (default), `Letter`, `Legal`
- `-s, --style <name>` — Style name or path to .css file (see Styles below)
- `--landscape` — Landscape orientation (good for wide tables or code)
- `--margin-top <margin>` — Top margin (e.g. `20mm`)
- `--margin-right <margin>` — Right margin
- `--margin-bottom <margin>` — Bottom margin
- `--margin-left <margin>` — Left margin

## EPUB Conversion

```bash
npx md-bookify@2.2.1 epub <input.md> [options]
```

**Options:**
- `-o, --output <path>` — Output EPUB file path (default: same name with .epub extension)
- `-t, --title <title>` — Document title (default: filename)
- `--author <name>` — Author name
- `--language <code>` — Language code (default: `en`)
- `--publisher <name>` — Publisher metadata
- `--description <text>` — Book description metadata
- `--cover <path>` — Path to cover image file

**Important:** EPUB ignores `--style`, `--format`, `--landscape`, and `--margin-*` flags — those are PDF-only.

## Built-in Styles (PDF only)

| Style | Description |
|-------|-------------|
| `default` | Clean, modern sans-serif styling |
| `serif` | Traditional book appearance with serif fonts |
| `elegant` | Refined typography with tasteful spacing |
| `eink` | Optimized for e-ink displays, high contrast |
| `eink-serif` | Serif variant optimized for e-ink readers |

Use with `-s`: `npx md-bookify@2.2.1 file.md -s elegant`

You can also pass a path to any `.css` file: `npx md-bookify@2.2.1 file.md -s ./custom.css`

## Supported Markdown Features

- GitHub Flavored Markdown (tables, task lists, strikethrough)
- Fenced code blocks with syntax highlighting (TypeScript, JavaScript, Python, Go, Rust, Java, Bash, JSON, CSS, HTML, YAML, SQL, Diff)
- KaTeX math: `$inline$` and `$$block$$`
- Images with relative paths (resolved from source file directory)

## Error Recovery

- **Chromium not found:** Run `npx puppeteer@24 browsers install chrome`
- **File not found:** Verify the path exists. Use Glob to search for markdown files if needed.
- **Node version:** Requires Node >= 20

## Examples

```bash
# Basic PDF
npx md-bookify@2.2.1 README.md

# Styled PDF with author
npx md-bookify@2.2.1 report.md -s elegant --author "Jane Doe" -o output/report.pdf

# US Letter format, landscape
npx md-bookify@2.2.1 data.md -f Letter --landscape

# EPUB ebook with cover
npx md-bookify@2.2.1 novel.md epub --author "Author Name" --cover cover.jpg

# EPUB with metadata
npx md-bookify@2.2.1 docs.md epub -t "User Guide" --publisher "Acme Corp" --description "Complete user guide"
```
