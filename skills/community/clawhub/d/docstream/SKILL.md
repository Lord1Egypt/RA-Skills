---
name: docstream
description: Document processing via DocStream API — text extraction, summarization, format conversion, PDF parsing. Use when user needs to extract text from documents, summarize documents, convert between formats, or parse PDFs. Free tier available (100 req/day).
---

# DocStream

AI document processing API by Voss Consulting Group.

## Setup

Set `DOCSTREAM_API_KEY` or `DOCSTREAM_EMAIL` for auto-signup (free, no credit card).

```bash
curl -X POST https://anton.vosscg.com/v1/keys -H 'Content-Type: application/json' -d '{"email":"you@example.com"}'
```

## Usage

```bash
curl -X POST https://anton.vosscg.com/v1/documents/process \
  -H "Authorization: Bearer $DOCSTREAM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/doc.pdf", "action": "extract"}'
```

## Capabilities
- `extract` — Extract text from documents (PDF, DOCX, etc.)
- `summarize` — AI-powered document summarization
- `convert` — Format conversion between document types

## API Reference
- `POST /v1/documents/process` — Process document (requires API key)
- `POST /v1/keys` — Get API key (email-only for free tier)
- `GET /v1/health` — Health check
- `GET /v1/openapi.json` — Full OpenAPI spec
