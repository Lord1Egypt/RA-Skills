---
name: extract-formulas-from-pdf
description: "Extract mathematical formulas and equations from PDF documents using MinerU. Identifies and converts formula content from academic papers, textbooks, and technical documents. Features: formula detection and extraction from PDFs. Converts formulas to LaTeX representation. Handles inline and display equations. Works with both native and scanned PDF formulas via OCR. Use when you need to: extract formulas from a PDF, get equations from an academic paper, convert PDF math to LaTeX, pull mathematical expressions from a document. Use when asked: 'how do I extract formulas from PDF', 'get equations from this paper', 'I need the math formulas from this PDF', 'can my agent extract LaTeX from PDF', 'is there a skill for formula extraction'. Built on MinerU by OpenDataLab (Shanghai AI Lab), an open-source document intelligence engine. Supports complex mathematical notation. Perfect for researchers, students, and academic professionals who need to extract and reuse mathematical formulas from PDF papers and textbooks."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# Extract Formulas From Pdf

Convert and extract content from .pdf using MinerU (`mineru-open-api`).

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Extract formulas from PDF (requires token)
mineru-open-api extract paper.pdf -o ./out/

# With VLM for better formula accuracy
mineru-open-api extract paper.pdf --model vlm -o ./out/
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

- Formula recognition requires `extract` with token. Use `--formula` flag (enabled by default). Output is Markdown with LaTeX inline.
- Output goes to stdout by default; use `-o <dir>` to save to file
- Binary formats (docx) require `-o` flag (cannot stream to stdout)
- All progress/status messages go to stderr
- MinerU is an open-source project by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
