# Uploads API

The Uploads API enables you to upload documents to your team. These uploaded files can then be referenced when creating or updating Chat Apps, creating Agent App tasks, and using RAG Apps and Extract Apps.

**Important**: This API is required for all apps except PDF Parser (which has its own upload endpoint). You must upload files first and use the returned `upload_id` when creating/updating apps or Agent App tasks.

## Base Path

```
/uploads
```

## Upload Document

### Upload File

Upload a document file to your team.

**Endpoint:** `POST /uploads/`

**Request:** (multipart/form-data)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | File | Yes | Document file (PDF, DOC, DOCX, MD, TXT) |

**Supported File Types:**

| File Type | Extensions | MIME Types |
|-----------|------------|------------|
| PDF | `.pdf` | `application/pdf` |
| DOC | `.doc` | `application/msword` |
| DOCX | `.docx` | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` |
| Markdown | `.md` | `text/markdown` |
| Text | `.txt` | `text/plain` |

**Response:**

| Field | Type | Description |
|-------|------|-------------|
| `upload_id` | string | Upload ID - save this for app creation |
| `name` | string | File name |
| `file_type` | string | File type (pdf, docx, md, txt, etc.) |
| `status` | string | Document processing status: `chunking`, `indexed`, `failed`, `chunked` |
| `created_at` | integer | Upload timestamp |

**Document Status After Upload:**

| Status | Description |
|--------|-------------|
| `chunking` | File uploaded, not yet parsed (this is the initial status) |

**Important**: This upload endpoint does **NOT** trigger document parsing. The file will remain at status `chunking` after upload.

**When does parsing happen?**

Parsing is automatically triggered when the `upload_id` is referenced in an app:
- When creating a Chat App with the document
- When creating an Agent App task with the document
- When creating/updating a RAG App with the document
- When uploading a file to an Extract App

If the document status is not `indexed` when referenced in an app, the system will automatically start parsing it.

**Status Codes:**

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 201 | - | Success |
| 400 | `not_support_file_format` | Unsupported file type |
| 400 | `file_too_large` | File size exceeds limit |
| 400 | `empty_file` | File is empty |
| 402 | - | Insufficient credits |
| 413 | - | Payload too large |

## Usage Flow

1. **Upload file**: Call `POST /uploads/` with your file
2. **Get upload_id**: Save the `upload_id` field from response (file is at status `chunking`)
3. **Use in app or task**: Reference the `upload_id` when creating/updating apps or creating Agent tasks
4. **Automatic parsing**: The system will automatically trigger parsing when the document is referenced in an app or task (if not already parsed)
5. **Wait for readiness**: After creating the app or task, wait until downstream processing completes before fetching results

**Simplified workflow**: Since parsing is automatic when referenced in apps or Agent tasks, you don't need to manually trigger parsing or wait before creating them. Just upload, get the `upload_id`, and use it immediately.

## Important Notes

1. **No parsing on upload**: This endpoint only uploads the file; it does NOT trigger parsing
2. **Automatic parsing**: Parsing starts automatically when the `upload_id` is referenced in an app or Agent task
3. **Store upload_id**: The API doesn't provide a list-all-documents endpoint, so save the `upload_id` in your database
4. **Ready status matters**: Documents must finish downstream processing before app or Agent task results are available
5. **File size limits**: Check your plan for maximum file size limits
6. **Credit consumption**: Each upload consumes credits based on file size and page count
7. **Multiple files**: Upload multiple files separately to get multiple `upload_id` values

## Integration with App APIs

### Chat App

```json
{
  "name": "My Chat App",
  "instruction": "Answer questions about the documents",
  "sources": [
    {"id": "UPLOAD_ID_1"},
    {"id": "UPLOAD_ID_2"}
  ]
}
```

### Agent App Task

```json
{
  "app_id": "AGENT_APP_ID",
  "upload_ids": ["UPLOAD_ID_1"]
}
```

### RAG App

```json
{
  "name": "My RAG App",
  "sources": [
    {"id": "UPLOAD_ID_1"},
    {"id": "UPLOAD_ID_2"}
  ]
}
```

## File Processing Timeline

1. **Upload (immediate)**: File uploaded, `upload_id` returned (status: `chunking`)
2. **Reference in app or task**: When you use the `upload_id` in an app or Agent task, parsing is triggered
3. **Processing (seconds to minutes)**: File is parsed (status: `chunking`)
4. **Ready**: File ready for app features (status: `indexed`)

The processing time depends on file size and type:
- Small PDFs (< 10 pages): ~30 seconds
- Medium PDFs (10-50 pages): ~1-2 minutes
- Large PDFs (50+ pages): ~3+ minutes

**Key Point**: You can create your app or Agent task immediately after upload. The system handles parsing in the background. Just check task/app status before fetching final outputs.

## Related Documentation

- [Document Status](../docs/document_status.md) - Understanding document processing states
- [Chat App API](../chat/chat_app.md) - Creating chat applications with documents
- [Agent App API](../agent/agent_app.md) - Creating Agent App tasks with documents
- [RAG App API](../retrieval/rag_app.md) - Creating retrieval applications with documents
- [Extract App API](../extraction/extract_app.md) - Creating extraction applications
