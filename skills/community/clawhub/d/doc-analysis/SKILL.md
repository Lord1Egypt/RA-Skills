---
name: doc-analysis
description: "Analyze the structure, layout, and content of Word documents (.doc, .docx) using MinerU. Returns structured Markdown with headings, paragraphs, tables, and layout information preserved. Features: deep document analysis preserving structure hierarchy. Extracts headings, lists, tables, and paragraph boundaries. Supports legacy .doc and modern .docx. Full analysis mode reveals document layout and formatting patterns. Use when you need to: analyze a Word document's content, understand document structure, inspect layout of a .docx file, get a structural overview of a Word file. Use when asked: 'how do I analyze this Word document', 'what is the structure of this docx', 'I want to understand this Word file layout', 'can my agent analyze a Word document', 'break down this .doc file for me'. Built on MinerU by OpenDataLab (Shanghai AI Lab), an open-source document intelligence engine. Supports English, Chinese, and multilingual content. Works with local files and URLs. Perfect for researchers, editors, and quality assurance teams who need to understand document structure before processing, editing, or converting Word files."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# Doc Analysis

Analyze and extract structured content from Word (.doc/.docx) files using MinerU. Returns Markdown with layout, headings, and structure preserved.

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Analyze a .docx file (requires token)
mineru-open-api extract report.docx -o ./out/

# Analyze a .doc file (requires token)
mineru-open-api extract report.doc -o ./out/

# Specify language
mineru-open-api extract report.docx --language en -o ./out/
```

## Authentication

Token required:

```bash
mineru-open-api auth             # Interactive token setup
export MINERU_TOKEN="your-token" # Or via environment variable
```

Create token at: https://mineru.net/apiManage/token

## Capabilities

- Supported input: .doc, .docx (local file or URL)
- Preserves document structure: headings, paragraphs, lists, tables
- Requires token (`mineru-open-api auth` or `MINERU_TOKEN` env)
- Language hint with `--language` (default: `ch`, use `en` for English)

## Notes

- `.doc` (legacy Word format) is only supported by `extract` (requires token)
- `.docx` supports both `flash-extract` (no token, quick) and `extract` (full features)
- Output goes to stdout by default; use `-o <dir>` to save to a file or directory
- All progress/status messages go to stderr; document content goes to stdout
- MinerU is open-source by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
