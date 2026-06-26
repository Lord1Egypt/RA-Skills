---
name: frompdf
description: PDF extraction API for AI agents and LLM pipelines. Converts any PDF into semantic AST, markdown, HTML, plain text, or LLM-ready chunks — no page limit. Also supports semantic diff between two PDFs and readability scoring. Use when you need structured, typed content from a PDF (headings, paragraphs, tables, lists) instead of raw text, or when OpenClaw's native PDF tool hits its 20-page limit. Requires FROMPDF_API_KEY. PDF contents are uploaded to api.frompdf.dev for processing.
homepage: https://api.frompdf.dev
metadata: {"clawdbot":{"emoji":"📄","requires":{"env":["FROMPDF_API_KEY"]}}}
---

# frompdf

Convert any PDF into structured, LLM-ready content via a single API call. Returns a semantic AST with every element — headings, paragraphs, tables, lists, metadata — properly typed and nested. No page limit. Handles encrypted PDFs, complex layouts, and multi-hundred-page documents.

## Quick start

```bash
# Register (10 free credits, no credit card)
curl -s -X POST https://api.frompdf.dev/register \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "password": "yourpassword"}'
# → {"api_key": "frompdf_..."}

# Extract a PDF (returns JSON semantic AST by default)
curl -s -X POST https://api.frompdf.dev/v1/extract \
  -H "Authorization: Bearer $FROMPDF_API_KEY" \
  -F "file=@document.pdf"
```

## Output formats

```bash
# Semantic AST — typed elements: headings, paragraphs, tables, lists (default)
-F "format=json"

# Markdown — structure preserved, human-readable
-F "format=markdown"

# HTML — full document with tags intact
-F "format=html"

# Plain text — clean extraction, no markup
-F "format=text"

# LLM-ready chunks — pre-split for RAG / vector store ingestion
-F "format=chunks"
```

## All endpoints

```bash
# Extract content from a PDF (1 credit)
curl -s -X POST https://api.frompdf.dev/v1/extract \
  -H "Authorization: Bearer $FROMPDF_API_KEY" \
  -F "file=@document.pdf" \
  -F "format=chunks"

# Encrypted PDF
curl -s -X POST https://api.frompdf.dev/v1/extract \
  -H "Authorization: Bearer $FROMPDF_API_KEY" \
  -F "file=@protected.pdf" \
  -F "password=secret"

# Semantic diff — compare two PDFs, get structured changes (2 credits)
curl -s -X POST https://api.frompdf.dev/v1/diff \
  -H "Authorization: Bearer $FROMPDF_API_KEY" \
  -F "file_a=@v1.pdf" \
  -F "file_b=@v2.pdf"

# Readability score — returns 0-100 score for a PDF (1 credit)
curl -s -X POST https://api.frompdf.dev/v1/score \
  -H "Authorization: Bearer $FROMPDF_API_KEY" \
  -F "file=@document.pdf"

# Check credits and subscription status (free)
curl -s https://api.frompdf.dev/v1/usage \
  -H "Authorization: Bearer $FROMPDF_API_KEY"
```

## Example output (JSON)

```json
{
  "title": "AWS Lambda Developer Guide",
  "pages": 87,
  "sections": [
    { "type": "heading", "level": 1, "text": "Getting Started" },
    { "type": "paragraph", "text": "AWS Lambda is a serverless compute service..." },
    {
      "type": "table",
      "headers": ["Runtime", "Version", "Status"],
      "rows": [["Node.js 20", "20.x", "Active"], ["Python 3.12", "3.12", "Active"]]
    },
    { "type": "list", "items": ["Function", "Trigger", "Execution role"] }
  ],
  "metadata": { "author": "Amazon Web Services", "created": "2024-01-15" }
}
```

## Pricing

$0.01/credit — extract (1), diff (2), score (1). First 10 credits free, no credit card required.

## Data & privacy

PDF contents are uploaded to `api.frompdf.dev` for processing. Do not use with confidential documents unless you have reviewed the [privacy policy](https://api.frompdf.dev). Requires `FROMPDF_API_KEY` env var — register free at `/register`.
