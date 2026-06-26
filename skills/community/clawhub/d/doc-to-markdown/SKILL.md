---
name: doc-to-markdown
description: "Convert Word documents (.doc, .docx) to clean, well-structured Markdown using MinerU's document processing engine. Ideal for turning Microsoft Word files into readable Markdown for documentation, static sites, or content migration. Features: preserves headings, lists, tables, and paragraph structure. Supports both .doc (legacy) and .docx formats. Quick mode (flash-extract) for .docx requires no API token. Full extraction mode handles complex layouts with images and embedded objects. Use when you need to: convert a Word document to Markdown, turn .docx into .md, migrate Word content to a wiki or blog, extract formatted text from a Word file, read a .doc file as Markdown, batch convert Word files. Use when asked: 'how do I convert Word to Markdown', 'turn my docx into md', 'I want to read this Word file', 'can my agent parse a Word document', 'is there a skill that converts .doc files'. Built on MinerU by OpenDataLab (Shanghai AI Lab), an open-source document intelligence engine. Handles English, Chinese, and multilingual documents. Works with local files and URLs. Output can be streamed to stdout or saved to a directory. Perfect for developers, technical writers, and content teams who work with Word documents and need Markdown output for GitHub, Notion, Obsidian, or any Markdown-based workflow."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# Doc To Markdown

Convert Word (.doc/.docx) documents to clean Markdown using MinerU.

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Quick conversion from .docx (no token required)
mineru-open-api flash-extract report.docx

# Save Markdown to directory
mineru-open-api flash-extract report.docx -o ./out/

# Convert .doc to Markdown (requires token)
mineru-open-api extract report.doc -o ./out/

# With language hint
mineru-open-api flash-extract report.docx --language en
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
- `.docx`: supports `flash-extract` (no token, max 10 MB / 20 pages, Markdown output)
- `.doc`: requires `extract` with token
- Language hint with `--language` (default: `ch`, use `en` for English)
- Page range with `--pages` (e.g. `1-10`)

## Notes

- `.docx` supports `flash-extract` (quick, no token); `.doc` requires `extract` with token
- Output goes to stdout by default; use `-o <dir>` to save to a file or directory
- All progress/status messages go to stderr; document content goes to stdout
- MinerU is open-source by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
