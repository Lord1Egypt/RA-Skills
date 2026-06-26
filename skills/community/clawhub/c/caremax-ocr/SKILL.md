---
name: caremax-ocr
description: "Upload medical reports and run OCR recognition via CareMax Health API. After upload succeeds, agents MUST immediately run OCR on the same session unless the user explicitly asked for upload-only. Session-based: upload creates a session, OCR processes all files, confirm saves all reports atomically. Resumes incomplete sessions. Trigger terms: upload report, scan report, OCR, recognize report, extract indicators, health report image, check-up photo, upload, scan, extract, resume upload, continue upload, pending session, unfinished upload, 继续上传, 未完成."
license: MIT
---

# CareMax Upload & OCR

> **Requires `caremax-auth` as a sibling directory** (`../caremax-auth/`). If missing, tell the user to install caremax-auth first (e.g. `npx skills add KittenYang/caremax-skills`).

Upload medical report files (PDF, JPG, PNG, HEIC) and extract structured data via AI-powered OCR.

**Session-based workflow**: upload → OCR → review → confirm. All operations are on a single session.

**Checkpoint & resume**: Every pipeline step saves progress to the database. If OCR fails mid-way (LLM timeout, worker crash, network error), retrying automatically resumes from the last checkpoint — no work is lost.

## Agent default behavior (MANDATORY)

1. **Upload and OCR are one continuous workflow.** When the user uploads report files (or asks you to upload/扫描/识别体检报告等), after `$UPLOAD` returns successfully you **must in the same turn** run `$OCRSTREAM <session_id>` using the returned `session_id`. **Do not** end the task after `upload.sh` alone.
2. **Upload-only exception:** Skip immediate OCR only if the user **explicitly** asked to upload without recognition (e.g. 只上传、不要识别、别跑 OCR、只存文件). If unclear, default to running OCR after upload.
3. **Progress:** Stream each SSE line to the user as it arrives (normalize / ocr / structure / …).
4. **After `step=done`:** Always continue to Step 3 (review). **Do not** auto-call confirm — wait for user approval before Step 4.

## Prerequisites — Auto-Auth (MANDATORY)

```bash
APICALL="bash ../caremax-auth/scripts/api-call.sh"
UPLOAD="bash ../caremax-auth/scripts/upload.sh"
OCRSTREAM="bash ../caremax-auth/scripts/ocr-stream.sh"
```

If any script returns `no_credentials` → run `bash ../caremax-auth/scripts/auth-flow.sh [base_url]` (from this skill’s root, sibling of `caremax-auth/`).

## Step 1: Upload (creates session)

```bash
$UPLOAD /path/to/report1.jpg /path/to/report2.jpg /path/to/report.pdf
```

Returns:
```json
{
  "session_id": "uuid-xxx",
  "member_id": "uuid-yyy",
  "files": [
    { "id": "file-1", "original_name": "report1.jpg" },
    { "id": "file-2", "original_name": "report2.jpg" },
    { "id": "file-3", "original_name": "report.pdf" }
  ]
}
```

Save the `session_id`.

## Step 2: OCR with real-time progress

```bash
$OCRSTREAM <session_id>
```

Outputs one JSON per line:
```json
{"step":"resume","progress":1,"message":"Resuming from checkpoint (last completed: ocr)..."}
{"step":"normalize","progress":5,"message":"Loading file 1/3..."}
{"step":"ocr","progress":30,"message":"OCR page 2/3: report2.jpg"}
{"step":"ocr_retry","progress":35,"message":"Retrying OCR page 1/1: report1.jpg"}
{"step":"structure","progress":62,"message":"Detecting report groups..."}
{"step":"structure","progress":75,"message":"Structuring report 2/2..."}
{"step":"normalize_indicators","progress":88,"message":"Standardizing..."}
{"step":"done","progress":100,"data":{"session_id":"...","reports":[...],"resumed":true}}
```

Display progress to the user as each line arrives.

### Key progress events

| step | meaning |
|------|---------|
| `resume` | Pipeline is resuming from a saved checkpoint (not starting from zero) |
| `info` | Informational message (e.g. which step was resumed from) |
| `normalize` | Loading and preprocessing files |
| `ocr` | OCR text extraction per page |
| `ocr_retry` | Retrying previously failed pages only |
| `structure` | AI analyzing and grouping reports |
| `normalize_indicators` | Standardizing indicator names |
| `done` | Complete — `data` field contains the full results |
| `error` | Pipeline failed — check `message` for details |

If `step=resume` appears, tell the user: "正在从上次的进度继续处理（不需要重新开始）"

### Error responses from `$OCRSTREAM`

| code | meaning | action |
|------|---------|--------|
| `processing_in_progress` | Another OCR run is still active | Wait and retry, or poll `/status` |
| `ocr_limit_exceeded` | Free OCR quota exhausted | Tell user to upgrade |
| (no code) | Pipeline error (LLM timeout etc.) | Retry — will auto-resume from checkpoint |

### Step 2b: Poll status (when SSE disconnects)

If the SSE stream disconnects (network timeout, terminal closed), use the status endpoint to check progress:

```bash
$APICALL GET "/api/skill/sessions/<session_id>/status"
```

Returns:
```json
{
  "session_id": "uuid",
  "status": "processing",
  "pipeline": {
    "completedStep": "ocr",
    "pageCount": 5,
    "ocrCompleted": 4,
    "ocrFailed": 1,
    "reportCount": 0,
    "errors": [{"step":"ocr","pageIndex":2,"message":"PaddleOCR timeout"}]
  },
  "error": null,
  "is_stale": false
}
```

**Field guide:**
- `status = processing` + `is_stale = false` → OCR is still running normally
- `status = processing` + `is_stale = true` → Worker crashed/timed out, safe to retry OCR
- `status = awaiting_confirm` → OCR completed! Fetch session detail for results
- `status = uploading` + `error` present → Last OCR attempt failed, retry will resume from checkpoint
- `pipeline.completedStep` → How far the pipeline got (normalize → ocr → structure → done)
- `pipeline.ocrFailed` → Number of pages that failed OCR (will be retried on next attempt)

**Polling workflow:**
```
1. Call $OCRSTREAM → SSE disconnects mid-way
2. Poll GET /sessions/<id>/status every 5-10 seconds
3. When status = "awaiting_confirm" → fetch full results with GET /sessions/<id>
4. If status = "uploading" (failed) → retry with $OCRSTREAM (auto-resumes)
5. If is_stale = true → retry with $OCRSTREAM (auto-resumes from checkpoint)
```

## Step 3: Review results (MANDATORY)

Parse the `step=done` data. Show formatted summary. **Do NOT auto-confirm.**

Each report has a `reportType` field: `lab`, `genetic`, `imaging`, `pathology`, or `other`.

### Lab reports (reportType = "lab")
Show indicators table:
```
📋 报告 1: [lab] 尿生化 (编号: 114431194)
   日期: 2025-02-05  医生: 俞海瑾
   指标: 12 个 (3 个异常)
   ┌──────────────────────┬────────┬──────────┬────────────┬──────┐
   │ 指标                 │ 结果   │ 单位     │ 参考范围   │ 异常 │
   ├──────────────────────┼────────┼──────────┼────────────┼──────┤
   │ 24H尿钠              │ 130.0  │ mmol/24h │ 137-257    │  ⬇   │
   └──────────────────────┴────────┴──────────┴────────────┴──────┘
```

### Non-lab reports (reportType = "genetic" / "imaging" / etc.)
Show summary + sections:
```
📋 报告 1: [genetic] 基因检测报告
   日期: 2025-09-12  检测机构: 南京申友医学检验所
   摘要: 心血管18项基因检测...高血压、冠心病风险一般...
   段落: 18 sections
     [gene_variant] 高血压 — 风险: 正常
     [gene_variant] 冠心病 — 风险: 一般
     [medication] ACEI类降压药 — 正常代谢型
     ...
```

### Supported file types
- **Images** (JPG/PNG/HEIC): PaddleOCR → structure
- **PDF** (any size): Azure Mistral Document AI page-split → structure
  - Large PDFs (e.g. 23-page gene report, 9.6MB) are fully supported

## Step 4: Confirm and save

After user confirms:

```bash
$APICALL POST "/api/skill/sessions/<session_id>/confirm" '{"reports":[<reports from step 2>]}'
```

Returns: `{"success":true,"message":"2 report(s) saved","recordIds":[...]}`

## Resuming incomplete sessions

When the user asks to continue/resume a previous upload, or when checking for unfinished work:

### Step A: Find pending sessions

```bash
# List sessions that need OCR (uploaded but not processed)
$APICALL GET "/api/skill/sessions?status=uploading"

# List sessions stuck in processing (user exited mid-OCR)
$APICALL GET "/api/skill/sessions?status=processing"

# List sessions with OCR done but not yet confirmed
$APICALL GET "/api/skill/sessions?status=awaiting_confirm"
```

Show a summary of pending sessions to the user (file names, dates, status).

### Step B: Resume based on status

- **`uploading`**: Start OCR directly → go to Step 2 (`$OCRSTREAM <session_id>`)
  - If there's a saved checkpoint (previous failed attempt), OCR auto-resumes from it
- **`processing`**: Check with status endpoint first:
  ```bash
  $APICALL GET "/api/skill/sessions/<session_id>/status"
  ```
  - `is_stale = false` → still running, wait or poll
  - `is_stale = true` → worker died, safe to retry: `$OCRSTREAM <session_id>` (auto-resumes from checkpoint)
- **`awaiting_confirm`**: Get session detail → show results → go to Step 3 (review & confirm)

```bash
# Get full detail of a pending session (includes OCR results if awaiting_confirm)
$APICALL GET "/api/skill/sessions/<session_id>"
```

If the session is `awaiting_confirm`, the response includes `ocr_result` with the previously parsed reports — display them for review and proceed to Step 3 (confirm).

### Resume-aware response handling

When `$OCRSTREAM` outputs `step=done`:
- `resumed = true` in the data → tell user: "已从上次的进度恢复，OCR 结果已就绪"
- `resumed = false` (or absent) → normal fresh run

When `$OCRSTREAM` outputs `step=error`:
- `code = processing_in_progress` → tell user OCR is still running, poll `/status` instead
- `code = ocr_limit_exceeded` → tell user to upgrade
- No code → LLM/network error, safe to retry (will auto-resume from checkpoint)

### Step C: Delete individual reports or stale sessions

Delete a single report (does NOT affect other reports in the same session):

```bash
$APICALL DELETE "/api/skill/sessions/<session_id>/records/<record_id>"
```

Delete an entire session (cascade deletes ALL files + reports):

```bash
$APICALL DELETE "/api/skill/sessions/<session_id>"
```

## Other session operations

```bash
# List all sessions (all statuses)
$APICALL GET /api/skill/sessions

# List sessions filtered by status: uploading | processing | awaiting_confirm | completed
$APICALL GET "/api/skill/sessions?status=<status>"

# Get session detail (includes OCR results if awaiting_confirm, saved reports if completed)
$APICALL GET "/api/skill/sessions/<session_id>"

# Poll OCR progress (lightweight, use when SSE disconnects)
$APICALL GET "/api/skill/sessions/<session_id>/status"

# Delete single report (keeps session and other reports intact)
$APICALL DELETE "/api/skill/sessions/<session_id>/records/<record_id>"

# Delete entire session (undo everything: files + reports)
$APICALL DELETE "/api/skill/sessions/<session_id>"
```
