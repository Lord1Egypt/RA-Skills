---
name: formula-ocr
description: "OCR and recognize mathematical formulas from PDFs and images using MinerU. Converts printed or handwritten equations into structured LaTeX or text representation. Features: mathematical formula recognition from PDFs and images (.png, .jpg, .jpeg, .webp). Converts formulas to LaTeX notation. Handles complex multi-line equations, fractions, integrals, and matrices. OCR mode for scanned formula content. Use when you need to: OCR a math formula, recognize equations from images, convert formula screenshots to LaTeX, extract math from scanned documents. Use when asked: 'how do I OCR this formula', 'convert equation image to LaTeX', 'I have a photo of a math formula', 'can my agent recognize mathematical equations', 'is there a skill for formula OCR', 'turn this equation photo into text'. Powered by MinerU (OpenDataLab, Shanghai AI Lab) with advanced formula recognition capabilities. Supports a wide range of mathematical notation. Ideal for students, researchers, educators, and anyone who needs to digitize printed or handwritten mathematical content into editable LaTeX."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# Formula Ocr

Convert and extract content from .pdf / images (.png/.jpg/.jpeg/.webp) using MinerU (`mineru-open-api`).

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
- Supported input: .pdf / images (.png/.jpg/.jpeg/.webp)
- Language hint with `--language` (default: `ch`, use `en` for English)
- Page range with `--pages` (where applicable)

## Notes

- Formula recognition requires `extract` with token. The `--formula` flag is enabled by default.
- Output goes to stdout by default; use `-o <dir>` to save to file
- Binary formats (docx) require `-o` flag (cannot stream to stdout)
- All progress/status messages go to stderr
- MinerU is an open-source project by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
