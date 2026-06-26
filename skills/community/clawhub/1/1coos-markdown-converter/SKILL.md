---
name: 1coos-markdown-converter
description: Convert files to beautifully formatted Markdown. TRIGGER when user asks to convert a file to Markdown, extract text from PDF/DOCX/PPTX/XLSX, or format a document as Markdown.
version: 1.0.1
metadata: {"openclaw":{"requires":{"bins":["bun","uvx"]},"install":[{"kind":"uv","package":"markitdown[all]","bins":["markitdown"]}],"emoji":"📝"}}
---

# Markdown Converter

Convert files to beautifully formatted Markdown in two steps: **convert** with `uvx markitdown[all]`, then **beautify** with configurable style formatting.

## Usage

```
/1coos-markdown-converter <file-path> [--style github|commonmark|clean|obsidian] [--output-dir path] [--convert-only]
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `<file-path>` | Yes | Path to the file to convert |
| `--style` | No | Formatting style: `github` (default), `commonmark`, `clean`, `obsidian` |
| `--output-dir` | No | Output directory (default: `skills/1coos-markdown-converter/output`) |
| `--convert-only` | No | Only convert, skip formatting step |
| `--config` | No | Path to config.json (default: skill directory config.json) |

## Supported Formats

- **Documents**: PDF, Word (.docx), PowerPoint (.pptx), Excel (.xlsx, .xls)
- **Web/Data**: HTML, CSV, JSON, XML
- **Media**: Images (EXIF + OCR), Audio (EXIF + transcription)
- **Other**: ZIP (iterates contents), YouTube URLs, EPub

## Formatting Styles

### github (default)
GitHub Flavored Markdown — table column alignment, fenced code blocks, task lists.

### commonmark
Strict CommonMark — enforces sequential heading levels (no skipping h1 to h3).

### clean
Minimal style — removes excessive formatting, simplifies redundant links.

### obsidian
Obsidian Flavored Markdown — converts internal links to `[[wikilinks]]`, normalizes callout syntax (`> [!type]`), formats properties/frontmatter, normalizes `==highlight==` syntax, and aligns tables. Ideal for notes destined for Obsidian vaults.

## Configuration

Core parameters are configurable via `config.json` in the skill directory:

```json
{
  "style": "github",
  "outputDir": null,
  "convertOnly": false,
  "formatting": {
    "maxWidth": 80,
    "listMarker": "-",
    "emphasisMarker": "*",
    "strongMarker": "**",
    "codeBlockStyle": "fenced"
  },
  "converter": {
    "timeout": 60000,
    "charset": "UTF-8"
  }
}
```

CLI arguments always override config.json values.

## Execution Instructions

When the user invokes this skill:

1. **Check prerequisites**: Verify `uvx` is available. If not, instruct the user to install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. **Run conversion**: Execute the script:
   ```bash
   bun run ${CLAUDE_SKILL_DIR}/scripts/main.ts $ARGUMENTS
   ```
3. **Report results**: Show the output file path and a brief summary of the conversion.
4. **Handle errors**:
   - Exit code 2: argument error — show the specific error message
   - Exit code 3: missing dependency — guide user to install uv
   - Exit code 4: conversion failure — suggest checking file format support

## Examples

```bash
# Convert a PDF with default github style
/1coos-markdown-converter report.pdf

# Convert Word document with clean style
/1coos-markdown-converter document.docx --style clean

# Convert Excel to markdown without formatting
/1coos-markdown-converter data.xlsx --convert-only

# Specify output directory
/1coos-markdown-converter slides.pptx --output-dir ~/notes
```

## Notes

- First run caches `markitdown[all]` dependencies; subsequent runs are faster
- Uses `markitdown[all]` to ensure full format support (PDF, OCR, audio transcription)
- Output preserves document structure: headings, tables, lists, links
- For complex PDFs with poor extraction, consider using Azure Document Intelligence
