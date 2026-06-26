# Content Retrieval App API (RAG App)

The Content Retrieval App API enables semantic search and content retrieval from your documents.

## Base Path

```
/rag/apps
```

## App Management

### 1. Create App

Create a new content retrieval application.

**Endpoint:** `POST /rag/apps`

**Request:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | App name (1-30 characters) |
| `sources` | array | Yes | Array of `{"id": "upload_id"}` objects (max 300) |

**Response:**

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `id` | string | No | App ID |
| `name` | string | No | App name |
| `documents` | array | No | Connected documents |

**Document Object:**

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `id` | string | No | Document ID |
| `name` | string | No | Document name |
| `status` | string | No | Processing status |

**Status Codes:**

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 200 | - | Success |
| 400 | `unsupported_file_type` | Unsupported file type (only PDF, DOC, DOCX) |
| 400 | `contain_not_parsed_file` | Contains documents not yet parsed |
| 402 | - | Insufficient credits |

### 2. Get App

Retrieve app details.

**Endpoint:** `GET /rag/apps/{app_id}`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `app_id` | string | App ID |

**Response:**

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `id` | string | No | App ID |
| `name` | string | No | App name |
| `documents` | array | No | Connected documents |

**Status Codes:**

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad request syntax or unsupported method |
| 404 | `not_found` | App not found |

### 3. Update App

Update app configuration and documents.

**Endpoint:** `PUT /rag/apps/{app_id}`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `app_id` | string | App ID |

**Request:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | App name (1-30 characters) |
| `sources` | array | Yes | Array of `{"id": "upload_id"}` objects (max 300) |

**Response:**

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `id` | string | No | App ID |
| `name` | string | No | App name |
| `documents` | array | No | Connected documents |

**Status Codes:**

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 200 | - | Success |
| 400 | `already_published` | Cannot update published app |
| 400 | `unsupported_file_type` | Unsupported file type |
| 400 | `contain_not_parsed_file` | Contains documents not yet parsed |
| 404 | `not_found` | App not found |

## Content Retrieval

### 4. Retrieval Query

Execute a semantic search query to retrieve relevant content.

**Endpoint:** `POST /rag/apps/{app_id}/retrieval`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `app_id` | string | App ID |

**Request:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | string | Yes | Search query (1-3000 characters) |
| `retrieval_token_length` | integer | No | Max response token length (1000-30000, default: 6000) |
| `retrieval_mode` | string | No | `basic`, `contextual` (default), or `expanded` |

**Retrieval Modes:**

| Mode | Description |
|------|-------------|
| `basic` | Fast and efficient. Combines Embedding and BM25 hybrid retrieval, followed by a non-contextual reranker to reorder the results |
| `contextual` | More precise. Combines Embedding and BM25 hybrid retrieval, followed by a contextual reranker to reorder the results for better accuracy |
| `expanded` | More comprehensive and highly accurate, with increased latency. After the initial contextual reranking, surrounding context from the top relevant segments is added to the candidate set for a second round of reranking |

**Response:** Array of retrieval results

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `upload_id` | string | No | Source document ID |
| `document_name` | string | No | Source document name |
| `elements` | array | No | Retrieved content elements |

**Element Object:**

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `index` | integer | No | Element index |
| `type` | string | No | Element type: `paragraph`, `table`, `figure`, `shape`, `image`, `page_header`, `page_footer` |
| `page` | array[int] | No | Page numbers |
| `outline` | object | No | Element bounding boxes |
| `is_chapter_title` | boolean | No | Whether this element is a chapter title (default: `false`) |
| `parent_chapter` | integer | No | Parent chapter index (default: `-1`) |
| `rotation` | number | No | Rotation angle in degrees (default: `0`) |
| `text` | string | No | Text content (for `paragraph`, `figure`, `shape`, `page_header`, `page_footer`) |
| `markdown` | string | Yes | Markdown content (for `paragraph`, `figure`, `shape`, `table`, `page_header`, `page_footer`) |
| `cells` | object | No | Table cell data (for `table`) |
| `grid` | object | No | Table grid definition (for `table`) |
| `title` | string | No | Table title text (for `table`) |
| `title_index` | integer | No | Table title element index (for `table`) |
| `merged` | array | No | Merged table cell regions (for `table`) |

**Note:** `elements` is a union type. Different element types include different subsets of the fields above.

**Status Codes:**

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 200 | - | Success |
| 400 | `invalid_retrieval_mode` | Invalid retrieval mode |
| 400 | `retrieval_failed` | Retrieval operation failed |
| 404 | `not_found` | App not found |

## Important Notes

1. **Document Status**: All connected documents must have `status == "indexed"` before using retrieval
2. **Supported File Types**: Only PDF, DOC, and DOCX files are supported for content retrieval apps
3. **Training Time**: After creating/updating an app, there may be a brief training period before retrieval is available
4. **Query Length**: Maximum query length is 3000 characters
5. **Token Length**: Adjust `retrieval_token_length` based on your needs (default 6000, range 1000-30000)
6. **Retrieval Modes**: Choose based on your needs - `basic` for speed, `contextual` for accuracy, `expanded` for comprehensive results
