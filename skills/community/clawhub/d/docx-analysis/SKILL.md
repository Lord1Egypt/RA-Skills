---
name: docx-analysis
description: "Analyze the structure and content of .docx (Word) files using MinerU. Returns structured Markdown preserving headings, tables, lists, and layout for content understanding. Features: structural analysis of .docx files. Quick analysis mode (flash-extract) without token. Full analysis with token for complex documents with tables and formulas. Page range selection for large files. Use when you need to: analyze a .docx file structure, understand content layout of a Word document, inspect .docx headings and sections, get an overview of a Word file. Use when asked: 'how do I analyze this docx', 'what is inside this Word file', 'I want to understand this .docx structure', 'can my agent analyze docx files', 'break down this docx for me'. Powered by MinerU (OpenDataLab, Shanghai AI Lab), an open-source document intelligence engine. Supports multilingual content. Ideal for content reviewers, editors, and automated quality checks on Word documents."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# Docx Analysis

Analyze the structure and content of Word (.docx) files using MinerU. Returns structured Markdown with headings, tables, and layout preserved.

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Quick analysis (no token required)
mineru-open-api flash-extract report.docx

# Save to directory
mineru-open-api flash-extract report.docx -o ./out/

# Full analysis with tables and formulas (requires token)
mineru-open-api extract report.docx -o ./out/

# With language hint
mineru-open-api flash-extract report.docx --language en
```

## Authentication

No token needed for `flash-extract`. Token required for `extract`:

```bash
mineru-open-api auth             # Interactive token setup
export MINERU_TOKEN="your-token" # Or via environment variable
```

Create token at: https://mineru.net/apiManage/token

## Capabilities

- Supported input: .docx (local file or URL)
- `flash-extract`: no token, max 10 MB / 20 pages, Markdown output
- `extract`: token required, full features (tables, formulas, multi-format output)
- Language hint with `--language` (default: `ch`, use `en` for English)
- Page range with `--pages` (e.g. `1-10`)

## Notes

- For `.doc` (legacy format), use `doc-analysis` skill instead
- Output goes to stdout by default; use `-o <dir>` to save to a file or directory
- All progress/status messages go to stderr; document content goes to stdout
- MinerU is open-source by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
