---
name: bohrium-pdf-parser
description: "Parse PDF documents via open.bohrium.com. Use when: user asks about extracting text, tables, charts, formulas, or molecules from PDF files on Bohrium, submitting PDFs by URL or file upload. NOT for: file management, dataset management, or knowledge base operations."
---

# SKILL: Bohrium PDF Parser

## Overview

Parse PDF documents using the `open.bohrium.com` PDF parsing service. Extract text, tables, charts, formulas, and molecular structures from PDFs. Two submission methods:

- **URL submission** — provide a PDF download link (e.g. arXiv link)
- **File upload** — upload a local PDF file

**No CLI support** — all operations use the HTTP API.

## Authentication

ACCESS_KEY is read from the OpenClaw config `~/.openclaw/openclaw.json`:

```json
"bohrium-pdf-parser": {
  "enabled": true,
  "apiKey": "YOUR_ACCESS_KEY",
  "env": {
    "ACCESS_KEY": "YOUR_ACCESS_KEY"
  }
}
```

OpenClaw automatically injects `env.ACCESS_KEY` into the runtime.

## Common Code Template

```python
import os, time, requests

AK = os.environ.get("ACCESS_KEY", "")
BASE = "https://open.bohrium.com/openapi/v1/parse"
HEADERS = {"accessKey": AK}
HEADERS_JSON = {**HEADERS, "Content-Type": "application/json"}
```

---

## Parsing Workflow

```
1. Submit PDF (URL or file upload) → get token
2. Poll result with token → complete when status == "success"
```

Synchronous mode (`sync=true`) blocks until parsing completes but does not include content in the response — you still need `get-result` to retrieve it. Asynchronous mode (`sync=false`, default) requires polling `get-result` until status is `success`.

---

## URL Submission

```python
r = requests.post(f"{BASE}/trigger-url-async", headers=HEADERS_JSON, json={
    "url": "https://arxiv.org/pdf/2107.06922",
    "sync": False,
    "textual": True,
    "table": True,
    "molecule": True,
    "chart": True,
    "figure": False,
    "expression": True,
    "equation": True,
    "pages": [0],           # 0-indexed, omit to parse all pages
    "timeout": 1800
})
data = r.json()
token = data["token"]
print(f"Token: {token}, Status: {data['status']}")
# Token: 57d12c5a-..., Status: undefined
```

**Response Fields:**

| Field | Description |
|-------|-------------|
| `token` | Task identifier for querying results |
| `status` | Initial status is `undefined` |
| `created_time` | Creation time |
| `time_dict` | Per-stage timing (only `download_pdf` at this point) |

---

## File Upload

```python
from pathlib import Path

pdf_path = Path("./paper.pdf")
with open(pdf_path, "rb") as f:
    r = requests.post(f"{BASE}/trigger-file-async",
        headers=HEADERS,       # No Content-Type; requests handles multipart automatically
        files={"file": (pdf_path.name, f, "application/pdf")},
        data={
            "sync": "false",
            "textual": "true",
            "table": "true",
            "molecule": "true",
            "chart": "true",
            "figure": "false",
            "expression": "true",
            "equation": "true",
            "pages": 0,         # multipart only accepts a single integer
            "timeout": 1800
        })
token = r.json()["token"]
```

> **Important**: `pages` in multipart/form-data only accepts a **single integer** (e.g. `0`), not a JSON array `[0]`, or you'll get an `int_parsing` error. In JSON request bodies, arrays like `[0, 1, 2]` are supported.

---

## Query Parse Result

```python
r = requests.post(f"{BASE}/get-result", headers=HEADERS_JSON, json={
    "token": token,
    "content": True,        # Return extracted text
    "objects": False,        # Return extracted objects (tables, figures, etc.)
    "pages_dict": True       # Return per-page results
})
data = r.json()
print(f"Status: {data['status']}, Content length: {len(data.get('content', ''))}")
```

**Response Fields:**

| Field | Description |
|-------|-------------|
| `status` | `success` / `undefined` (processing) / `failed` |
| `token` | Task identifier |
| `content` | Extracted text (LaTeX markup format) |
| `pages_dict` | Per-page result dictionary |
| `lang` | Detected language (`en` / `zh` etc.) |
| `proc_page` / `total_page` | Processed / total pages |
| `proc_textual` / `total_textual` | Processed / total text blocks |
| `proc_table` / `total_table` | Processed / total tables |
| `proc_mol` / `total_mol` | Processed / total molecules |
| `proc_equa` / `total_equa` | Processed / total equations |
| `time_dict` | Per-stage timing details |
| `cost` | Cost |

---

## Full Async Polling Example

```python
import os, time, requests

AK = os.environ.get("ACCESS_KEY", "")
BASE = "https://open.bohrium.com/openapi/v1/parse"
HEADERS = {"accessKey": AK}
HEADERS_JSON = {**HEADERS, "Content-Type": "application/json"}

# 1. Submit
r = requests.post(f"{BASE}/trigger-url-async", headers=HEADERS_JSON, json={
    "url": "https://arxiv.org/pdf/2107.06922",
    "sync": False,
    "textual": True, "table": True, "molecule": False,
    "chart": False, "figure": False,
    "expression": True, "equation": True,
    "pages": [0],
    "timeout": 1800
})
submit = r.json()
if submit.get("code"):
    print(f"Submit failed: {submit.get('message')}")
    exit(1)

token = submit["token"]
print(f"Submitted, token={token}")

# 2. Poll for result
for attempt in range(30):
    time.sleep(2)
    r = requests.post(f"{BASE}/get-result", headers=HEADERS_JSON, json={
        "token": token,
        "content": True,
        "objects": False,
        "pages_dict": False
    })
    result = r.json()
    status = result.get("status", "")
    print(f"  [{attempt+1}] status={status}")

    if status == "success":
        print(f"Done! Content length: {len(result.get('content', ''))}")
        print(f"Language: {result.get('lang')}, Cost: {result.get('cost')}")
        print(f"Preview: {result.get('content', '')[:200]}")
        break
    elif status == "failed":
        print(f"Failed: {result.get('description', 'unknown error')}")
        break
else:
    print("Timeout: task did not complete within 60 seconds")
```

---

## Synchronous Mode Example

Synchronous mode (`sync=true`) blocks until parsing completes, so no polling is needed. However, the **response does not include the `content` field** — you still need to call `get-result` to retrieve the parsed content:

```python
# 1. Synchronous submit — blocks until parsing completes
r = requests.post(f"{BASE}/trigger-url-async", headers=HEADERS_JSON, json={
    "url": "https://arxiv.org/pdf/2107.06922",
    "sync": True,           # Wait for completion
    "textual": True, "table": True,
    "molecule": False, "chart": False, "figure": False,
    "expression": True, "equation": True,
    "pages": [0],
    "timeout": 1800
})
submit = r.json()
token = submit["token"]
# submit["status"] == "success", but no content field

# 2. Retrieve content
r = requests.post(f"{BASE}/get-result", headers=HEADERS_JSON, json={
    "token": token,
    "content": True, "objects": False, "pages_dict": False
})
result = r.json()
print(f"Content: {result['content'][:200]}")
```

---

## Parse Options Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `sync` | bool | `false` | `true` blocks until complete (still need `get-result` for content), `false` requires polling |
| `textual` | bool | - | Extract text content |
| `table` | bool | - | Extract tables |
| `molecule` | bool | - | Extract molecular structures |
| `chart` | bool | - | Extract charts |
| `figure` | bool | - | Extract figures/images |
| `expression` | bool | - | Extract math expressions |
| `equation` | bool | - | Extract equations |
| `pages` | list[int] | all | Pages to parse (0-indexed) |
| `timeout` | int | - | Timeout in seconds |

---

## curl Examples

```bash
AK="YOUR_ACCESS_KEY"
BASE="https://open.bohrium.com/openapi/v1/parse"

# URL submission
curl -s -X POST "$BASE/trigger-url-async" \
  -H "Content-Type: application/json" \
  -H "accessKey: $AK" \
  -d '{"url":"https://arxiv.org/pdf/2107.06922","sync":false,"textual":true,"table":true,"molecule":false,"chart":false,"figure":false,"expression":true,"equation":true,"pages":[0],"timeout":1800}'

# File upload
curl -s -X POST "$BASE/trigger-file-async" \
  -H "accessKey: $AK" \
  -F "file=@paper.pdf" \
  -F "sync=false" -F "textual=true" -F "table=true" \
  -F "pages=0"

# Query result
curl -s -X POST "$BASE/get-result" \
  -H "Content-Type: application/json" \
  -H "accessKey: $AK" \
  -d '{"token":"YOUR_TOKEN","content":true,"objects":false,"pages_dict":true}'
```

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `AccessKey is required` | Missing or incorrect accessKey | Header name is `accessKey` (case-sensitive), not `Authorization: Bearer` |
| `int_parsing` error | `pages` sent as JSON array in file upload | Use a single integer for `pages` in multipart form |
| `status: undefined` | Async task not yet complete | Poll `get-result` again; recommended interval: 2 seconds |
| Connection timeout | Domain/network issue | Use `open.bohrium.com`; test connectivity via `curl -I https://open.bohrium.com/openapi` |
| Content has LaTeX markup | Normal behavior | Results use `\begin{title}` etc. to mark structure; post-process to extract plain text |
| Large file parses slowly | Many pages or complex content | Use `pages` parameter to limit scope |
