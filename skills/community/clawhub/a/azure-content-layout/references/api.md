# Azure Content Understanding Layout API Reference

## Endpoint

```
POST {endpoint}/contentunderstanding/analyzers/prebuilt-layout:analyze?api-version={version}
```

## API Versions

| Version | Status | Request Body Format |
|---------|--------|-------------------|
| `2025-05-01-preview` | Preview | `{"url": "..."}` |
| `2025-11-01` | GA | `{"inputs": [{"url": "..."}]}` |

## Authentication

```
Ocp-Apim-Subscription-Key: YOUR_KEY_HERE
```

## Request (URL source)

**Preview (2025-05-01-preview):**
```json
{"url": "https://example.com/document.pdf"}
```

**GA (2025-11-01):**
```json
{"inputs": [{"url": "https://example.com/document.pdf"}]}
```

## Request (File upload)

```
Content-Type: application/octet-stream
Body: <binary file data>
```

## Response Flow

1. **POST** returns `202 Accepted` with `Operation-Location` header
2. **GET** the `Operation-Location` URL to poll for results
3. Status transitions: `Running` → `Succeeded` / `Failed`

## Result Structure

```json
{
  "id": "...",
  "status": "Succeeded",
  "result": {
    "analyzerId": "prebuilt-layout",
    "contents": [{
      "markdown": "# Document Title\n\nExtracted content...",
      "kind": "document",
      "pages": [...],
      "paragraphs": [...],
      "tables": [...],
      "figures": [...],
      "sections": [...]
    }]
  }
}
```

## Key Output Fields

- **markdown** — Full document content as GitHub Flavored Markdown (headings, tables as HTML, checkboxes as ☒/☐)
- **pages** — Per-page metadata (dimensions, word count)
- **paragraphs** — Individual text blocks with bounding regions and roles
- **tables** — Structured table data with cells, spans, and content
- **figures** — Detected figures/images with bounding regions
- **sections** — Hierarchical document structure

## Supported File Types

PDF, JPEG, PNG, BMP, TIFF, HEIF, DOCX, XLSX, PPTX, HTML

## Limits

- Max file size: 500 MB (paid tier), 4 MB (free tier)
- Max pages: 2,000 per document
- Image dimensions: 50×50 to 10,000×10,000 pixels
- Processing time: typically 5–60 seconds depending on document size
