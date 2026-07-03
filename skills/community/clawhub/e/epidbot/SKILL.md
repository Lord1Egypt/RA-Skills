---
name: epidbot
description: Query EpidBot (Brazilian public health data AI assistant) via its REST API. Use when you need epidemiological data analysis, plots, reports, DATASUS queries, plot management, report downloads, code snippets, or dataset uploads.
license: MIT
compatibility: opencode
metadata:
  audience: all
  requires:
    - EPIDBOT_API_KEY
    - EPIDBOT_API_URL
---

## What this skill does

EpidBot is an AI-powered assistant for Brazilian public health data (DATASUS). This skill is a REST API reference for all EpidBot operations. Make HTTP requests directly — no helper scripts needed.

**Capabilities:**
- Ask epidemiological questions and get AI-generated analysis with charts
- List, search, download plots from "My Plots" collection
- Download the Python code that generated each plot
- List and download reports (Markdown and PDF)
- Search code snippets saved from previous analyses
- List, upload, preview datasets in "My Data" area

## When to use this skill

| User says... | Action |
|---|---|
| "Show my plots" / "Search plots for dengue" | `GET /plots/?search=...` |
| "Download plot 42" / "Give me the dengue chart" | `GET /plots/{id}/file` |
| "How was plot 42 made?" / "Show me the code for this plot" | `GET /plots/{id}/snippet` |
| "Download all my plots as ZIP" | `POST /plots/download-zip` |
| "List my reports" | `GET /reports` |
| "Download report 15 as PDF" | `GET /reports/{id}/pdf` |
| "Search for code snippets about ARIMA" | `POST /search` with `source_type: snippet` |
| "Show my datasets" / "List my data" | `GET /uploads/` |
| "Upload this CSV to EpidBot" | `POST /uploads/` (multipart) |
| Any epidemiological question / data analysis request | `POST /chat` → poll |

## Authentication

All endpoints accept the `X-API-Key` header with an `ek_`-prefixed API key (obtained from EpidBot Settings → API Keys).

**Exception:** `GET /plots/{id}/file` does NOT read the `X-API-Key` header. For this endpoint, use `Authorization: Bearer {EPIDBOT_API_KEY}` instead. The server accepts `ek_`-prefixed keys as Bearer tokens.

## Environment variables

| Variable | Description | Default |
|---|---|---|
| `EPIDBOT_API_KEY` | API key from EpidBot (starts with `ek_`). Required. | — |
| `EPIDBOT_API_URL` | Base URL of the EpidBot API. | `https://epidbot.kwar-ai.com.br` |

---

## Chat

**Submit a question and poll for the response.** The API is asynchronous — you must poll until the job completes.

### Submit question

```
POST {EPIDBOT_API_URL}/api/v1/chat
Headers:
  X-API-Key: {EPIDBOT_API_KEY}
  Content-Type: application/json
Body:
  {"message": "Quantos casos de dengue em SP em 2024?", "locale": "en"}
Response (HTTP 200):
  {"job_id": "abc123", "session_id": 42, "status": "processing"}
```

### Poll for result

```
GET {EPIDBOT_API_URL}/api/v1/chat/{job_id}
Headers:
  X-API-Key: {EPIDBOT_API_KEY}
Response (when completed):
  {
    "job_id": "abc123",
    "status": "completed",
    "content": "## Analysis\n\n... markdown ...",
    "images": ["/file=/data/plots/sandbox/figure_001.png"]
  }
```

**Polling rules:**
- Poll every 3 seconds until `status` is `"completed"`, `"failed"`, or `"cancelled"`
- Status values: `pending`, `processing`, `completed`, `failed`, `cancelled`
- Timeout: 5 minutes (300s)
- Markdown images in `content` use `![desc](/file=...)` syntax — these reference the EpidBot server and may require auth to display
- Each query creates a new session prefixed with `[API]`

### Response modes

The `content` field may contain:
- **Inline analysis** — markdown tables, statistics, links
- **Plot references** — `![description](/file=/data/plots/...)` — the chart was generated and saved
- **Combined** — analysis text plus embedded plot references

Present the response clearly. If it contains plot references, note that the user can download them via the Plots endpoints.

---

## Plots ("My Plots")

### List / search plots

```
GET {EPIDBOT_API_URL}/api/v1/plots/
Headers: X-API-Key: {EPIDBOT_API_KEY}
Query params:
  search (optional) — filters by filename/description (ILIKE match)
Response: [
  {
    "id": 42,
    "filename": "figure_001.png",
    "description": "Dengue cases São Paulo 2024",
    "source": "chat",
    "file_size_bytes": 48500,
    "mime_type": "image/png",
    "width": 1200,
    "height": 800,
    "created_at": "2025-01-15T10:30:00Z",
    "has_snippet": true
  }
]
```

### Get plot metadata

```
GET {EPIDBOT_API_URL}/api/v1/plots/{plot_id}
Headers: X-API-Key: {EPIDBOT_API_KEY}
Response: { single PlotInfo object, same fields as list }
```

### Download plot image

```
GET {EPIDBOT_API_URL}/api/v1/plots/{plot_id}/file
Headers: Authorization: Bearer {EPIDBOT_API_KEY}   ← NOTE: Bearer, not X-API-Key!
Response: Binary image data (Content-Type: image/png or image/jpeg etc.)
```

Save the response body as a file. The filename from the plot metadata (`filename` field) is a good default.

### Download plot's Python code

```
GET {EPIDBOT_API_URL}/api/v1/plots/{plot_id}/snippet
Headers: X-API-Key: {EPIDBOT_API_KEY}
Response: Python source code (Content-Type: text/x-python)
Returns HTTP 404 if no snippet was saved for this plot.
```

The `has_snippet` field in plot listings tells you whether code is available.

### Download multiple plots as ZIP

```
POST {EPIDBOT_API_URL}/api/v1/plots/download-zip
Headers:
  X-API-Key: {EPIDBOT_API_KEY}
  Content-Type: application/json
Body: {"plot_ids": [42, 43, 44]}
Response: Binary ZIP data (Content-Type: application/zip)
```

### Upload a new plot

```
POST {EPIDBOT_API_URL}/api/v1/plots/upload
Headers: X-API-Key: {EPIDBOT_API_KEY}
Body: multipart/form-data
  file: (binary image, max 20 MB, allowed: png/jpg/jpeg/webp/gif/svg)
  description: (string, optional)
Response: { PlotInfo object }
```

### Update / delete plots

```
PATCH  /api/v1/plots/{plot_id}     Body: {"description": "new desc"}
DELETE /api/v1/plots/{plot_id}
POST   /api/v1/plots/bulk-delete   Body: {"plot_ids": [42, 43]}
Headers: X-API-Key: {EPIDBOT_API_KEY}
```

---

## Reports

### List reports

```
GET {EPIDBOT_API_URL}/api/v1/reports
Headers: X-API-Key: {EPIDBOT_API_KEY}
Response: [
  {
    "id": 15,
    "title": "Dengue trends in Southeast Brazil",
    "report_type": "manuscript",
    "created_at": "2025-01-14T08:00:00Z",
    "updated_at": "2025-01-14T08:05:00Z",
    "image_count": 3,
    "content_size_bytes": 45000,
    "has_pdf": true,
    "user_id": 1,
    "username": "user",
    "is_shared": false,
    "permission": "owner",
    "owner_name": "User Name",
    "share_count": 0,
    "zenodo_doi": null,
    "zenodo_record_url": null,
    "zenodo_status": null,
    "reference_count": 12
  }
]
```

### Download report as PDF

```
GET {EPIDBOT_API_URL}/api/v1/reports/{report_id}/pdf
Headers: X-API-Key: {EPIDBOT_API_KEY}
Response: Binary PDF data (Content-Type: application/pdf)
```

The PDF is generated server-side via WeasyPrint with embedded charts and bibliography. To force regeneration, use `POST /reports/{report_id}/regenerate-pdf`.

### Download report as Markdown

```
GET {EPIDBOT_API_URL}/api/v1/reports/{report_id}/download
Headers: X-API-Key: {EPIDBOT_API_KEY}
Response: Markdown text (Content-Type: text/markdown)
```

### Get report details

```
GET {EPIDBOT_API_URL}/api/v1/reports/{report_id}
Headers: X-API-Key: {EPIDBOT_API_KEY}
Response: {
  "id": 15,
  "title": "...",
  "report_type": "manuscript",
  "prompt": "...",
  "content": "# Abstract\n\n...",
  "abstract": "...",
  "image_count": 3,
  "has_pdf": true,
  "created_at": "...",
  "updated_at": "...",
  "user_id": 1,
  "is_shared": false,
  "permission": "owner"
}
```

### Delete report

```
DELETE {EPIDBOT_API_URL}/api/v1/reports/{report_id}
Headers: X-API-Key: {EPIDBOT_API_KEY}
Response: {"message": "Report deleted"}
```

### Additional report endpoints

```
GET  /reports/{id}/versions             — version history
GET  /reports/{id}/references           — bibliography listing
GET  /reports/{id}/bibtex               — download .bib file
POST /reports/{id}/regenerate-pdf       — force PDF regeneration
```

---

## Code Snippets

There is no dedicated snippets REST API. Use the unified search endpoint:

```
POST {EPIDBOT_API_URL}/api/v1/search
Headers:
  X-API-Key: {EPIDBOT_API_KEY}
  Content-Type: application/json
Body: {
  "query": "ARIMA forecast",
  "source_type": "snippet"
}
Response: {
  "results": [
    {
      "source_type": "snippet",
      "title": "Dengue ARIMA forecast",
      "language": "python",
      "source_code": "import pandas as pd\n...",
      "description": "ARIMA model for dengue time series",
      "tags": ["arima", "forecast", "dengue"],
      "created_at": "2025-01-10T12:00:00Z"
    }
  ],
  "total": 1
}
```

The `source_code` field contains the full snippet. If you need all snippets without filtering, omit `query` and just pass `source_type: "snippet"`.

---

## My Data (User Datasets)

### List datasets

```
GET {EPIDBOT_API_URL}/api/v1/uploads/
Headers: X-API-Key: {EPIDBOT_API_KEY}
Response: {
  "datasets": [
    {
      "id": 7,
      "name": "hospital_admissions",
      "path": "/data/private/42/hospital_admissions/data.parquet",
      "row_count": 15000,
      "file_size_bytes": 2048000,
      "file_count": 1,
      "created_at": "2025-01-12T09:00:00Z",
      "original_filename": "admissions.csv",
      "description": "Monthly hospital admissions by municipality"
    }
  ]
}
```

### Upload a dataset

```
POST {EPIDBOT_API_URL}/api/v1/uploads/
Headers: X-API-Key: {EPIDBOT_API_KEY}
Body: multipart/form-data
  file: (the dataset file)
  description: (string, optional — description for the catalog)
Response: {
  "id": 8,
  "name": "my_dataset",
  "path": "/data/private/42/my_dataset/data.parquet",
  "row_count": 5000,
  "file_size_bytes": 1024000,
  "message": "Dataset uploaded successfully"
}
```

**Supported formats:** `.csv`, `.ods`, `.xlsx`, `.xls` (converted to Parquet) and `.geojson`, `.json`, `.gpkg`, `.zip` (converted to GIS Parquet). Max file size: 50 MB.

Uploaded datasets are automatically cataloged and can be queried by EpidBot in subsequent chat interactions.

### Get dataset details

```
GET {EPIDBOT_API_URL}/api/v1/uploads/{dataset_id}
Headers: X-API-Key: {EPIDBOT_API_KEY}
Response: { single dataset object, same fields as list }
```

### Preview dataset (first 10 rows)

```
GET {EPIDBOT_API_URL}/api/v1/uploads/{dataset_id}/preview
Headers: X-API-Key: {EPIDBOT_API_KEY}
Response: {
  "columns": ["col1", "col2", "..."],
  "rows": [["val1", "val2"], ...],
  "total_rows": 5000,
  "total_columns": 25,
  "showing_columns": 15,
  "truncated_columns": 10
}
```

### Additional dataset endpoints

```
DELETE /uploads/{id}                  — delete dataset
POST   /uploads/{id}/publish          — publish to public catalog
PATCH  /uploads/{id}/description      — update description
GET    /uploads/{id}/crate-metadata   — read RO-Crate metadata
PATCH  /uploads/{id}/metadata         — update full metadata
```

---

## Notes

- **Chat is asynchronous.** No synchronous request-response. Always poll.
- **Plot file downloads require Bearer auth**, not `X-API-Key`. All other endpoints use `X-API-Key`.
- **Plot code snippets** may not exist for every plot (`has_snippet` field tells you).
- **Code snippets** are searched via the unified `/api/v1/search` endpoint with `source_type: "snippet"`.
- **Uploaded datasets** are automatically converted to Parquet and cataloged. They become queryable via `read_parquet('/data/private/{user_id}/...')` in subsequent chat queries.
- **Markdown images in chat responses** (`![...](/file=...)`) reference the EpidBot server. The files are in `/data/plots/` or `/data/public/plots/sandbox/`. They can be downloaded via the Plots endpoints.
- All timestamps are in ISO 8601 format (UTC).
