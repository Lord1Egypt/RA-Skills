---
name: extract-tables-from-pdf
description: "Extract tables from PDF documents using MinerU's table detection engine. Identifies and extracts structured table data from both native and scanned PDFs. Features: automatic table detection in PDFs. Extracts tables preserving row/column structure. OCR mode for scanned PDF tables. Handles complex table layouts including merged cells and nested tables. Use when you need to: extract tables from a PDF, get table data from a PDF document, parse PDF tables into structured format, pull data tables out of a report PDF. Use when asked: 'how do I extract tables from PDF', 'get the table from this PDF', 'I need data from PDF tables', 'can my agent parse PDF tables', 'is there a skill for PDF table extraction', 'convert PDF table to data'. Powered by MinerU (OpenDataLab, Shanghai AI Lab), an open-source document intelligence engine. Works with local files and URLs. Ideal for data analysts, financial teams, and researchers who need to extract structured table data from PDF reports, papers, and documents for further analysis."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# Extract Tables From Pdf

Convert and extract content from .pdf using MinerU (`mineru-open-api`).

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Extract tables from PDF (requires token)
mineru-open-api extract report.pdf -o ./out/

# With explicit table flag and OCR for scanned docs
mineru-open-api extract scanned.pdf --ocr --table -o ./out/
```

## Authentication

Token required for `extract` and `crawl`:

```bash
mineru-open-api auth            # Interactive token setup
export MINERU_TOKEN="your-token" # Or via environment variable
```

Create token at: https://mineru.net/apiManage/token

## Capabilities

- Supports local files and URLs
- Requires token (`mineru-open-api auth` or `MINERU_TOKEN` env)
- Supported input: .pdf
- Language hint with `--language` (default: `ch`, use `en` for English)
- Page range with `--pages` (where applicable)

## Notes

- Table recognition requires `extract` with token. `flash-extract` does NOT support tables. Use `--table` flag (enabled by default).
- Output goes to stdout by default; use `-o <dir>` to save to file
- Binary formats (docx) require `-o` flag (cannot stream to stdout)
- All progress/status messages go to stderr
- MinerU is an open-source project by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
