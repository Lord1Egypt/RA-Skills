# Document Status

All documents uploaded to ChatDOC Studio go through a processing pipeline. Each document has a `status` field that indicates its current processing state.

## API Status Codes

The API uses simple string status codes to indicate document processing status.

| Status | Description |
|--------|-------------|
| `chunking` | Document is being processed (chunking in progress) |
| `indexed` | Document fully processed and ready for use in all apps |
| `chunked` | Chunking completed (PDF Parser API only) |
| `failed` | Processing failed |

## Usage by API Type

### PDF Parser API

Documents must have status `chunked` or `indexed` before calling:
- `GET /pdf/parser/{upload_id}/json`
- `GET /pdf/parser/{upload_id}/markdown`
- `GET /pdf/parser/{upload_id}/excel`

**Example workflow:**
```python
# Upload PDF to PDF Parser API
response = upload_to_pdf_parser("document.pdf", wait=True)
upload_id = response["upload_id"]
status = response["status"]

# Check if ready for JSON/Markdown/Excel extraction
if status in ["chunked", "indexed"]:
    json_data = get_pdf_json(upload_id)
else:
    print(f"Document status: {status}")
```

### Chat App API

Documents must have status `indexed` before:
- Creating conversations
- Sending messages

**Important**: When you create a Chat App with documents, the documents must be fully processed (`status == "indexed"`) before you can start conversations.

### RAG App API

Documents must have status `indexed` before:
- Creating retrieval queries
- Using the app for content search

### Extract App API

Documents need `status != "failed"` for upload. The extraction process will automatically trigger parsing if the document hasn't been parsed yet.

## Status Flow

```
chunking → chunked → indexed
   ↓
 failed
```

1. **chunking**: Initial state when document is uploaded and being processed
2. **chunked**: Chunking is complete (PDF Parser API intermediate state)
3. **indexed**: Document is fully processed with embeddings, ready for all apps
4. **failed**: An error occurred during processing

## Error Handling

When `status == "failed"`, the document processing encountered an error. Common causes:
- File format not supported
- File corrupted or password-protected
- Page limit exceeded
- Network or server error

## Best Practices

1. **Check status before using**: Always verify document status before making API calls that require processed documents
2. **Handle pending state**: Implement retry logic with exponential backoff when status is `chunking`
3. **Handle failures**: Check for `failed` status and handle errors appropriately
4. **PDF Parser specific**: For PDF Parser API, both `chunked` and `indexed` are acceptable states
