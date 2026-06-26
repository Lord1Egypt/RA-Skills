---
name: edgebric
description: Search and manage your private knowledge base. Find documents, query knowledge, upload files, and manage data sources in Edgebric.
version: 0.9.6
author: jerv
homepage: https://edgebric.com
repository: https://github.com/jerv/edgebric
license: AGPL-3.0
requires:
  env:
    - name: EDGEBRIC_API_KEY
      description: API key starting with "eb_", created in Edgebric Settings > API Keys
      required: true
      scope: read-only (minimum), read-write (for uploads/deletes)
    - name: EDGEBRIC_URL
      description: Base URL of the Edgebric instance (e.g. http://localhost:3001)
      required: true
primary_credential: EDGEBRIC_API_KEY
user-invocable: true
model-invocable: true
---

# Edgebric Knowledge Base

Use this skill when the user asks about documents, files, knowledge, policies, notes, records, or any information that might be stored in their private knowledge base. Also use it when they want to save, upload, or organize documents.

## Setup

Two environment variables are required:
- `EDGEBRIC_URL`: The base URL of the Edgebric instance (e.g. `http://localhost:3001` or `https://edgebric.company.com:3001`)
- `EDGEBRIC_API_KEY`: An API key starting with `eb_`, created in Edgebric Settings > API Keys

All requests use `Authorization: Bearer $EDGEBRIC_API_KEY` header.

## When to Use

- User asks about documents, files, knowledge, policies, procedures, notes, records
- User says "check my docs", "what do we know about...", "find the policy for..."
- User wants to save/upload a document ("save this to my Edgebric", "upload this file")
- User asks to create a new knowledge source or manage their data

## Endpoints

### Discovery

```
GET $EDGEBRIC_URL/api/v1/discover
```
Returns API version, available sources, capabilities, and endpoint map. Call this first if unsure what sources exist.

### List Sources

```
GET $EDGEBRIC_URL/api/v1/sources
```
Returns all data sources the API key has access to, with document counts.

### List Documents in a Source

```
GET $EDGEBRIC_URL/api/v1/sources/{sourceId}/documents
```
Returns documents with name, type, size, upload date, and processing status.

### Search (Preferred)

```
POST $EDGEBRIC_URL/api/v1/search
Content-Type: application/json

{
  "query": "what is the vacation policy?",
  "sourceIds": ["optional-source-id"],
  "topK": 5
}
```

Returns ranked chunks with citations. **Prefer this over /query** -- it returns raw search results without LLM synthesis, letting you (the smart model) do the synthesis with full context of the conversation.

Response:
```json
{
  "results": [
    {
      "content": "The vacation policy allows...",
      "relevanceScore": 0.92,
      "citation": {
        "documentName": "HR Handbook.pdf",
        "page": 12,
        "section": "Benefits > Time Off",
        "sourceId": "abc-123",
        "sourceName": "HR Documents"
      }
    }
  ]
}
```

### Query (Full RAG)

```
POST $EDGEBRIC_URL/api/v1/query
Content-Type: application/json

{
  "query": "what is the vacation policy?",
  "sourceIds": ["optional-source-id"],
  "stream": false
}
```

Returns a synthesized answer from the local LLM with citations. Use this only when you specifically need the local model's interpretation, or when /search returns results and you want a pre-formatted answer.

Response:
```json
{
  "answer": "According to the HR Handbook...",
  "citations": [
    {
      "documentName": "HR Handbook.pdf",
      "page": 12,
      "section": "Benefits > Time Off",
      "sourceId": "abc-123",
      "sourceName": "HR Documents"
    }
  ]
}
```

Set `stream: true` for SSE streaming (Server-Sent Events).

### Create a Source

```
POST $EDGEBRIC_URL/api/v1/sources
Content-Type: application/json

{
  "name": "Project Alpha Docs",
  "description": "Documentation for Project Alpha"
}
```

Requires read-write or admin permission.

### Upload a Document

```
POST $EDGEBRIC_URL/api/v1/sources/{sourceId}/upload
Content-Type: multipart/form-data

file: <binary file data>
```

Supported types: PDF, DOCX, TXT, MD (max 50MB).
Returns document ID and job ID. The document will be processed asynchronously (text extraction, chunking, embedding, PII detection).

Requires read-write or admin permission.

### Check Job Status

```
GET $EDGEBRIC_URL/api/v1/jobs/{jobId}
```

Check if a document upload/ingestion job is complete.

### Delete a Document

```
DELETE $EDGEBRIC_URL/api/v1/documents/{documentId}
```

Requires read-write or admin permission. **Always confirm with the user before deleting.** Never delete documents without explicit user approval.

### Delete a Source

```
DELETE $EDGEBRIC_URL/api/v1/sources/{sourceId}
```

Deletes the source and ALL its documents. Requires admin permission. **Always confirm with the user before deleting a source — this is a destructive, irreversible operation.** Never delete sources without explicit user approval.

## Formatting Results

When presenting search results or query answers to the user, always include citations:

> According to **HR Handbook.pdf** (p. 12, Benefits > Time Off), the vacation policy allows...

Format: **Document Name** (p. Page, Section Path)

If multiple sources contribute to an answer, cite each one.

## Error Handling

All errors return JSON:
```json
{
  "error": "Human-readable message",
  "code": "MACHINE_CODE",
  "status": 401
}
```

Common codes:
- `AUTH_REQUIRED` (401): Missing or invalid API key
- `INVALID_KEY` (401): Key is revoked or malformed
- `INSUFFICIENT_PERMISSION` (403): Key doesn't have required permission level
- `NOT_FOUND` (404): Resource doesn't exist or is outside key's scope
- `RATE_LIMITED` (429): Too many requests, check Retry-After header
- `INFERENCE_UNAVAILABLE` (503): Local LLM not running

## Tips

- `/search` is almost always better than `/query` -- you can synthesize better answers with more context
- Check `/discover` first to see what sources are available
- Source IDs filter searches to specific collections -- omit to search everything
- The API key's scope may limit which sources are visible
- Documents take a few seconds to process after upload (extraction + embedding)
- Works with both localhost and network URLs
