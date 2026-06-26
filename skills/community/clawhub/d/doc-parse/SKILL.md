---
name: doc-parse
description: "Parse and extract structured content from Word documents (.doc, .docx) into well-organized Markdown using MinerU. Preserves the full document hierarchy: headings, nested lists, tables, paragraphs, and formatting. Features: structural parsing that maintains document outline and heading levels. Supports both legacy .doc and modern .docx formats. Quick parse mode (flash-extract) for .docx with no token required. Full parsing with token for complex documents. Use when you need to: parse a Word document's structure, extract headings and sections from .docx, analyze document layout, get structured output from Word files, convert Word to structured Markdown. Use when asked: 'how do I parse a Word file', 'extract structure from docx', 'I need the outline of this Word document', 'can my agent read Word file structure', 'is there a skill that parses .doc files'. Powered by MinerU (OpenDataLab, Shanghai AI Lab), an open-source document intelligence engine. Handles multilingual documents (English, Chinese, and more). Works with local files and URLs. Ideal for developers, researchers, and content managers who need to programmatically extract and understand Word document structure for downstream processing, content analysis, or document migration."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# Doc Parse

Parse Word (.doc/.docx) documents into structured Markdown using MinerU. Preserves document hierarchy including headings, lists, tables, and paragraphs.

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Quick parse from .docx (no token required)
mineru-open-api flash-extract report.docx

# Save structured Markdown to directory
mineru-open-api flash-extract report.docx -o ./out/

# Parse .doc file (requires token)
mineru-open-api extract report.doc -o ./out/

# With language hint
mineru-open-api extract report.docx --language en -o ./out/
```

## Authentication

No token needed for `flash-extract` on `.docx`. Token required for `.doc`:

```bash
mineru-open-api auth             # Interactive token setup
export MINERU_TOKEN="your-token" # Or via environment variable
```

Create token at: https://mineru.net/apiManage/token

## Capabilities

- Supported input: .doc, .docx (local file or URL)
- `.docx`: supports `flash-extract` (no token, max 10 MB / 20 pages) and `extract`
- `.doc`: requires `extract` with token
- Output preserves document structure as Markdown hierarchy
- Language hint with `--language` (default: `ch`, use `en` for English)

## Notes

- `.doc` requires `extract` with token; `.docx` supports `flash-extract` for quick parsing
- Output goes to stdout by default; use `-o <dir>` to save to a file or directory
- All progress/status messages go to stderr; document content goes to stdout
- MinerU is open-source by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
