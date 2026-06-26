---
name: caremax-auth
description: "OAuth Device Flow authentication for CareMax Health API. This skill is a PREREQUISITE for all other caremax-* skills — invoke it automatically when no token is found. Do NOT ask the user, just run the auth flow. Trigger terms: caremax login, caremax auth, health API token, authorize caremax, connect health data, health indicator, blood test, medical record, upload report."
license: MIT
---

# CareMax Authentication

## CRITICAL RULES

1. This is a **silent prerequisite** for ALL caremax-* skills. Do NOT ask "do you want to authenticate?" — just execute.
2. **NEVER write your own curl commands**. Only use the scripts below.
3. **NEVER split auth into multiple steps manually**. Use `./scripts/auth-flow.sh` (from this skill root) — it opens browser AND auto-polls until done.
4. **BASE URL DETECTION**: If the user specifies a custom URL (local dev 默认 `http://localhost:8788`，须与后端 wrangler `[dev]` 端口一致), you MUST:
   - Pass it as the first argument: `bash ./scripts/auth-flow.sh http://localhost:8788` (run from **this** skill root — see path convention below)
   - After auth completes, `credentials.json` will have `base_url` set to that URL
   - All subsequent `api-call.sh`, `list-system-presets.sh`, `quick-log.sh`, `upload.sh`, `ocr-stream.sh` will auto-use it
   - Look for URL patterns like `http://localhost:XXXX`, `caremax(http://...)`, or explicit "use local" / "use localhost"

## Scripts

### Path convention (no `~/.claude` — product-agnostic)

- **This skill (`caremax-auth`):** run commands with **current working directory** = this folder (the directory that contains `SKILL.md` and `scripts/`). Invoke scripts as **`./scripts/<name>.sh`**.
- **Other `caremax-*` skills** sit as **sibling directories** next to `caremax-auth` (e.g. `skills/caremax-indicators/` and `skills/caremax-auth/` in the repo, or `~/.agents/skills/<name>/` after install). From those folders, call auth as **`../caremax-auth/scripts/<name>.sh`**.

Credentials file location is unchanged: **`~/.caremax/credentials.json`** (not under any product’s config dir).

### api-call.sh — Make authenticated API calls (PRIMARY TOOL)

This is what you should use for all API calls. It auto-checks token, auto-refreshes if expired.

```bash
bash ./scripts/api-call.sh GET /api/skill/indicators
bash ./scripts/api-call.sh POST /api/skill/records/search '{"query":"血常规"}'
bash ./scripts/api-call.sh GET "/api/skill/indicators/trend?id=xxx"
```

If it returns `{"error":"no_credentials",...}` → run `./scripts/auth-flow.sh` (see below), then retry.

### list-system-presets.sh — 当前账号可快捷记录的指标列表

与 App **「快捷记一笔」** 芯片一致：先看有哪些 `preset_key` / 显示名 / 默认单位，再调用 `quick-log.sh`。

```bash
bash ./scripts/list-system-presets.sh
```

### quick-log.sh — 快捷记一笔（单条数值）

```bash
bash ./scripts/quick-log.sh <preset_key> <value>
bash ./scripts/quick-log.sh weight 72.5 --unit kg --date 2026-03-29
bash ./scripts/quick-log.sh height 175 --member <family_member_uuid>
```

可选参数：`--unit`、`--date`（`YYYY-MM-DD`）、`--member`（家庭成员 UUID）。底层走 `api-call.sh`，自动带用户 OAuth token。

### upload.sh — Upload files (images/PDFs) to CareMax

```bash
bash ./scripts/upload.sh /path/to/report.jpg
bash ./scripts/upload.sh /path/to/img1.jpg /path/to/img2.png
```

Returns: `{"files":[{"id":"...","member_id":"...","original_name":"..."}]}`

Use the returned `id` values as `fileIds` for `ocr-stream.sh`.

**IMPORTANT**: Do NOT use `api-call.sh` for file uploads — it only supports JSON body. Always use `upload.sh` for multipart file uploads.

### download-file.sh — Download a source file from a session

```bash
bash ./scripts/download-file.sh <file_id> [output_path]
# Example:
bash ./scripts/download-file.sh abc-123 ~/Downloads/report.jpg
```

Get `file_id` from session detail (`source_files[].id` in reports, or `files[].id` in session).

### ocr-stream.sh — OCR with real-time SSE progress (for caremax-ocr skill)

```bash
bash ./scripts/ocr-stream.sh <session_id>
```

Outputs one JSON per line as OCR progresses. Last line (step=done) has the full results.
Read each line and display progress to the user. See caremax-ocr skill for details.

Handles errors gracefully:
- **409** (session already processing) → outputs `{"step":"error","code":"processing_in_progress",...}`
- **403** (quota exceeded) → outputs `{"step":"error","code":"ocr_limit_exceeded",...}`
- Pipeline auto-resumes from saved checkpoint on retry (no work is lost)

### auth-flow.sh — One-shot full authorization (opens browser + auto-polls)

```bash
# Default (production)
bash ./scripts/auth-flow.sh

# Custom base URL (localhost / staging)
bash ./scripts/auth-flow.sh http://localhost:8788
```

This script does EVERYTHING in one shot:
1. Requests device code from the API
2. Opens the user's browser to the authorize page
3. **Automatically polls every 5 seconds** until the user approves (up to 15 min)
4. Saves token to `~/.caremax/credentials.json`

Output when done: `{"status":"authorized","access_token":"sk-caremax-...","base_url":"..."}`

**Run this in the background** so you can tell the user what's happening while it polls:
```bash
bash ./scripts/auth-flow.sh &
```
Then tell the user: "I've opened the authorization page in your browser. Please log in and click Allow. I'll detect it automatically."

Wait for the background job to finish — it will output the result.

### check-token.sh — Check token status (used internally by api-call.sh)

```bash
bash ./scripts/check-token.sh
```

Output: `{"status":"valid"|"expired"|"missing", ...}`

### refresh-token.sh — Refresh expired token (used internally by api-call.sh)

```bash
bash ./scripts/refresh-token.sh
```

## Standard Workflow

### Quick vitals (快捷记一笔)
```
User wants to log height / weight / etc.
  → ./scripts/list-system-presets.sh  →  pick preset_key from JSON
  → ./scripts/quick-log.sh <preset_key> <value> [--unit ...] [--date ...] [--member ...]
```

### Query data
```
User asks about health data
  → run: ./scripts/api-call.sh GET /api/skill/xxx
      ├── token valid → returns data → done
      ├── token expired → auto-refreshes → returns data → done
      └── no token → returns error
          → run: ./scripts/auth-flow.sh [base_url] (background)
          → auth-flow.sh auto-polls and saves token
          → retry: ./scripts/api-call.sh → returns data → done
```

### Upload + OCR (save medical reports from images)

This is a **session-based multi-step workflow**. One upload session groups all files + reports together.

#### Step 1: Upload → creates a session
```bash
bash ./scripts/upload.sh /path/to/image1.jpg /path/to/image2.jpg
```
Returns:
```json
{ "session_id": "uuid", "member_id": "uuid", "files": [{ "id": "...", "original_name": "..." }] }
```
Save `session_id` — it's used for all subsequent steps.

#### Step 2: OCR (with real-time progress)
```bash
bash ./scripts/ocr-stream.sh <session_id>
```

Each output line is a JSON progress event. Relay to the user:
- `step=normalize` → "正在预处理文件..."
- `step=ocr` → "正在 OCR 识别第 X/Y 页..."
- `step=structure` → "AI 正在分析报告结构..."
- `step=normalize_indicators` → "正在标准化指标名称..."
- `step=done` → OCR complete, `data` contains reports array

#### Step 3: Present results for user review (MANDATORY)

**Do NOT call confirm automatically.** Parse the `step=done` data and show:

```
识别到 N 份报告：

📋 报告 1: {report_title}
   来源: {sourcePages.join(', ')}
   日期: {test_date}  医生: {doctor}  科室: {department}
   ┌──────────────────┬────────┬────────┬──────────┬──────┐
   │ 指标名称         │ 结果   │ 单位   │ 参考范围 │ 异常 │
   ├──────────────────┼────────┼────────┼──────────┼──────┤
   │ xxx              │ 1.23   │ mg/L   │ 0-5      │      │
   │ yyy              │ 9.99   │ mmol/L │ 1-8      │  ⬆   │
   └──────────────────┴────────┴────────┴──────────┴──────┘

📋 报告 2: ...

确认保存吗？
```

Wait for user to say 确认/保存/OK.

#### Step 4: Confirm and save
```bash
bash ./scripts/api-call.sh POST /api/skill/sessions/<session_id>/confirm '{"reports":[<reports array from step 2>]}'
```

Returns: `{"success":true,"message":"2 report(s) saved","recordIds":["uuid1","uuid2"]}`

After success: "已保存 N 份报告。"

### Query sessions
```bash
bash ./scripts/api-call.sh GET /api/skill/sessions
bash ./scripts/api-call.sh GET "/api/skill/sessions/<session_id>"
bash ./scripts/api-call.sh GET "/api/skill/sessions/<session_id>/status"   # lightweight progress polling
```

### Delete session (undo entire upload)
```bash
bash ./scripts/api-call.sh DELETE /api/skill/sessions/<session_id>
```
Deletes the session + all files + all reports atomically.
