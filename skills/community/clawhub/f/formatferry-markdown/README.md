# formatferry-markdown

Convert documents (HTML, DOCX, PDF, XLSX, CSV, JSON, XML, PPTX) and web content to clean Markdown using FormatFerry CLI.

## Install

```bash
npm install -g formatferry
```

Requires Node.js 18+.

## Usage

```bash
# Convert a file
formatferry -i document.docx -o output.md

# Pipe HTML from stdin
echo '<h1>Hello</h1>' | formatferry

# Choose a flavour
formatferry -i notes.html -f slack -o notes.md

# Convert a PDF
formatferry -i paper.pdf -o paper.md

# URL extraction (requires FORMATFERRY_API_KEY)
formatferry --url https://example.com/article -o article.md

# Batch convert (requires FORMATFERRY_LICENSE_KEY)
formatferry --batch "docs/**/*.docx" --output-dir ./markdown/
```

## Supported File Types

HTML, DOCX, PDF (including OCR), XLSX, CSV, JSON, XML, PPTX

## Markdown Flavours

`github` (default), `commonmark`, `slack`, `discord`, `reddit`, `confluence`, `rmarkdown`, `custom`

## Environment Variables

Both are optional — the CLI works for local file conversion with zero credentials.

| Variable | Needed For |
|----------|------------|
| `FORMATFERRY_API_KEY` | `--url` flag only |
| `FORMATFERRY_LICENSE_KEY` | `--batch` mode only |

## License

MIT-0
