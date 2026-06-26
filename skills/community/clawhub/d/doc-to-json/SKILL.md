---
name: doc-to-json
description: "Convert documents (docx, doc, PDF, xlsx, xls) to structured JSON via MinerU. Full pipeline: file to mineru-open-api extract to Markdown then to JSON. Use when user wants to convert a document to JSON, prepare files for local knowledge base RAG, extract structured data from course materials, standards, or reports. Triggers: 转JSON, 转markdown, 知识库素材, doc转json, PDF转JSON, MinerU, 文档解析, extract to json, course standard JSON."
---

# Doc to JSON

Convert office documents to structured JSON using MinerU as the extraction engine.

## Supported Formats

- `.doc` / `.docx` — Word documents
- `.pdf` — PDF files
- `.xlsx` / `.xls` — Excel spreadsheets

## Prerequisites

- **mineru-open-api CLI** must be installed (v0.5+)
- **MINERU_TOKEN** environment variable must be set
- Check: `mineru-open-api version`

## Quick Usage

```bash
# Full pipeline: document -> MinerU Markdown -> JSON
python3 scripts/doc_to_json.py /path/to/file.docx -o output.json

# Keep temp files for debugging
python3 scripts/doc_to_json.py /path/to/file.pdf -o out.json --keep-temp
```

## Manual Two-Step Pipeline

If the full pipeline script fails, run steps manually:

### Step 1: MinerU Extract

```bash
export MINERU_TOKEN="your_token"
mineru-open-api extract input_file.pdf -o /tmp/mineru_out/
```

Output: `.md` file in the output directory.

### Step 2: Markdown -> JSON

```bash
python3 scripts/markdown_to_json.py /tmp/mineru_out/output.md -o output.json
```

## JSON Structure

The output JSON preserves:
- **Metadata fields** — course name, code, credits, hours, etc. (extracted from plain text)
- **Heading hierarchy** — 一、二、三... sections become nested keys
- **Tables** — stored as array of arrays (row cells), keyed as `"表格"`
- **Numbered lists** — stored as array of strings under section title
- **Paragraph text** — merged into `"text"` field per section

## For Knowledge Base Preparation

After JSON conversion, common next steps:

1. **Chunk by section** — split the JSON into per-section documents for embedding
2. **Table extraction** — convert `"表格"` arrays to flattened rows for database import
3. **Metadata extraction** — pull course code, name, etc. as document metadata
4. **Embedding** — feed cleaned text chunks into vector database

See `references/kb-prep.md` for detailed KB preparation patterns.
