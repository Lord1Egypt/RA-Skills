# API Reference

## Endpoints

### GET /health

Health check. Returns `{"status": "ok"}` if running.

### POST /api/analyze

Main research endpoint.

**Request body:**
```json
{
  "question": "搜索问题"
}
```

**Response:**
```json
{
  "answer": "结构化答案",
  "sources": [
    {"title": "...", "url": "...", "source": "baidu"}
  ],
  "confidence": 0.85,
  "contradictions": [],
  "trace": {
    "elapsed_seconds": 12.5,
    "steps": ["web_search", "vector_search", "..."]
  }
}
```

### POST /search

Raw search without RAG pipeline. Returns unprocessed search results.

**Request body:** Same as `/api/analyze`.

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 422 | Invalid request body |
| 500 | Internal error |
| 503 | Service unavailable |
