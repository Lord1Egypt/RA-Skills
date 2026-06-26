---
name: doc-ocr
description: "OCR (Optical Character Recognition) for Word documents (.docx) containing scanned pages or image-embedded content. Uses MinerU to extract text from Word files that have poor or missing text layers. Features: OCR extraction for image-based .docx files. VLM (Vision Language Model) mode for complex layouts with mixed text and images. Handles scanned document pages embedded in Word files. Converts image content to searchable, editable Markdown. Use when you need to: OCR a Word document with scanned pages, extract text from image-based .docx, read scanned content inside Word files, convert image text in .docx to editable text. Use when asked: 'how do I OCR a Word file', 'extract text from scanned docx', 'my Word file has images instead of text', 'can my agent read scanned Word documents', 'is there a skill for Word document OCR'. Powered by MinerU (OpenDataLab, Shanghai AI Lab) with advanced OCR and VLM capabilities. Supports English, Chinese, and multilingual scanned content. Ideal for offices, legal teams, and archivists who receive Word files containing scanned pages or image-only content and need to extract readable, searchable text."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# Doc OCR

Use OCR to extract text from Word (.docx) files that contain scanned pages or image-embedded content, using MinerU.

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# OCR extraction from .docx (requires token)
mineru-open-api extract report.docx --ocr -o ./out/

# With VLM model for better accuracy on complex image layouts
mineru-open-api extract report.docx --ocr --model vlm -o ./out/
```

## Authentication

Token required:

```bash
mineru-open-api auth             # Interactive token setup
export MINERU_TOKEN="your-token" # Or via environment variable
```

Create token at: https://mineru.net/apiManage/token

## Capabilities

- Supported input: .docx (local file or URL)
- OCR is only available via `extract` (requires token)
- Use `--ocr` flag to enable OCR on image-embedded content
- Use `--model vlm` for complex or mixed-content documents
- Language hint with `--language` (default: `ch`, use `en` for English)

## Notes

- OCR is NOT available in `flash-extract` — use `extract` with `--ocr`
- If the `.docx` has a normal text layer, OCR is not needed — use `doc-extract` instead
- Output goes to stdout by default; use `-o <dir>` to save to a file or directory
- All progress/status messages go to stderr; document content goes to stdout
- MinerU is open-source by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
