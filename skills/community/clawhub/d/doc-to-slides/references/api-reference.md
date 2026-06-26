# Ruyi Converter API Reference — doc-to-slides

## Base info

- **Base URL**: `https://www.nyoi.io`
- **Auth**: `X-Api-Key: rk_xxx` or `Authorization: Bearer rk_xxx`
- **Content-Type**: `application/json`

---

## 1. Claim invite code

```
GET /api/agent/invite-code
```

No auth required. Returns one available invite code (not consumed until activation).

**Success** (200):
```json
{
  "success": true,
  "data": {
    "code": "inv_aBcDeFgHiJkLmNoP"
  }
}
```

**No codes available** (404):
```json
{
  "success": false,
  "error": "No invite codes available, please contact administrator"
}
```

---

## 2. Activate agent

```
POST /api/agent/activate
```

No auth required. Consumes an invite code and creates a temporary agent identity with an API Key.

**Request body**:
```json
{
  "inviteCode": "inv_aBcDeFgHiJkLmNoP",
  "name": "my_agent"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `inviteCode` | string | yes | Code from the claim endpoint |
| `name` | string | yes | 3-32 chars, alphanumeric + underscore |

**Success** (201):
```json
{
  "success": true,
  "data": {
    "name": "my_agent",
    "apiKey": "rk_aBcDeFgHiJkLmNoPqRsTuVwXyZ012345",
    "allowedTools": ["doc-to-slides"],
    "rateLimit": 20,
    "expiresAfterDays": 3
  }
}
```

> `data.apiKey` is the full API Key. **Shown only once.**

**Errors**:
- 400: Invalid name format or missing fields
- 409: Name already taken (pick a different name), invite code invalid or already used

---

## 3. Check identity

```
GET /api/agent/identity
X-Api-Key: rk_xxx
```

Check whether the current API Key's agent identity is still valid. **Does not reset the inactivity timer.**

**Valid** (200):
```json
{
  "success": true,
  "data": {
    "name": "my_agent",
    "status": "active",
    "expiresAt": "2026-03-20T10:00:00.000Z",
    "expiresIn": "2d 18h"
  }
}
```

**Expired** (403):
```json
{
  "success": false,
  "error": "Agent identity expired due to inactivity"
}
```

**Invalid key** (401):
```json
{
  "success": false,
  "error": "Invalid API Key"
}
```

---

## 4. Execute conversion

```
POST /api/tools/doc-to-slides/execute
X-Api-Key: rk_xxx
Content-Type: application/json
```

### 4a. Plain text input

```json
{
  "text": "# Title\n\n## Chapter 1\nContent...\n\n## Chapter 2\nContent...",
  "title": "Presentation Title",
  "language": "en"
}
```

### 4b. File URL input

```json
{
  "files": [
    "https://example.com/report.docx",
    "https://example.com/appendix.pdf"
  ],
  "title": "Project Report",
  "language": "en"
}
```

### 4c. Base64 encoded input

```json
{
  "files": [
    "data:text/plain;base64,IyBUaXRsZQo..."
  ],
  "title": "My Presentation"
}
```

### 4d. Presign upload (large files)

First obtain a pre-signed upload URL:

```
POST /api/upload/presign
X-Api-Key: rk_xxx
Content-Type: application/json
```

```json
{
  "fileName": "report.docx",
  "toolId": "doc-to-slides",
  "contentType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
}
```

Response:
```json
{
  "success": true,
  "data": {
    "uploadUrl": "https://cos.example.com/...?sign=xxx",
    "fileUrl": "https://cos.example.com/ruyi/doc-to-slides/input/...",
    "cosKey": "ruyi/doc-to-slides/input/..."
  }
}
```

PUT the file to `uploadUrl`, then pass `fileUrl` in the `files` array when calling the execute endpoint.

### Parameter summary

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `text` | string | either text or files | - | Text content (auto-uploaded as TXT) |
| `files` | string[] | either text or files | - | File URLs or Base64 strings |
| `title` | string | no | `"Presentation"` | Slide deck title |
| `language` | string | no | `"en"` | Output language (ISO 639-1 code) |
| `outputFormat` | string | no | `"pdf"` | Output format (currently fixed to pdf) |
| `webhookUrl` | string | no | - | Completion callback URL |
| `webhookSecret` | string | no | auto-generated | Webhook signature secret |

**Success** (200):
```json
{
  "success": true,
  "data": {
    "jobId": "job_abc123def456",
    "toolId": "doc-to-slides",
    "status": "pending",
    "progress": 0,
    "executionMode": "worker"
  }
}
```

**Errors**:
- 401: Invalid API Key
- 403: Agent identity expired / Tool not allowed for this key
- 429: Daily request limit reached

---

## 5. Query job status

```
GET /api/jobs/{jobId}
```

**No auth required.** Slide generation typically takes **8–16 minutes** (up to 30 min for large documents). Poll every 30 seconds until terminal status.

**In progress** (200):
```json
{
  "success": true,
  "data": {
    "jobId": "job_abc123def456",
    "toolId": "doc-to-slides",
    "status": "running",
    "progress": 50,
    "executionMode": "worker"
  }
}
```

**Completed** (200):
```json
{
  "success": true,
  "data": {
    "jobId": "job_abc123def456",
    "toolId": "doc-to-slides",
    "status": "completed",
    "progress": 100,
    "output": {
      "pageCount": 12
    },
    "artifacts": [
      {
        "type": "slides",
        "url": "https://cos.example.com/output/slides.pdf?sign=xxx",
        "expiresAt": "2026-03-17T20:00:00.000Z",
        "expiresIn": 7200
      }
    ],
    "completedAt": "2026-03-17T10:05:00.000Z"
  }
}
```

**Failed** (200):
```json
{
  "success": true,
  "data": {
    "jobId": "job_abc123def456",
    "status": "failed",
    "error": "Worker processing failed: ..."
  }
}
```

### Status values

| Status | Description |
|--------|-------------|
| `pending` | Created, awaiting scheduling |
| `queued` | Queued, waiting for a worker |
| `assigned` | Assigned to a worker |
| `running` | Processing |
| `completed` | Done |
| `failed` | Failed |
| `cancelled` | Cancelled |

---

## 6. Download links

- `artifacts[0].url` is a COS pre-signed link
- Valid for 2 hours (`expiresIn: 7200`)
- After expiry, re-request `GET /api/jobs/{jobId}` for a fresh link
- Files are not deleted when the link expires

---

## 7. Supported languages

Use ISO 639-1 codes for the `language` parameter:

| Code | Language |
|------|----------|
| `en` | English |
| `zh-CN` | 中文（简体） |
| `zh-TW` | 中文（繁體） |
| `ja` | 日本語 |
| `ko` | 한국어 |
| `es` | español |
| `fr` | français |
| `de` | Deutsch |
| `it` | italiano |
| `pt` | português |
| `ru` | русский |
| `ar` | العربية |
| `hi` | हिन्दी |
| `vi` | Tiếng Việt |
| `th` | ไทย |
| `id` | Bahasa Indonesia |
| `ms` | Bahasa Melayu |
| `nl` | Nederlands |
| `pl` | polski |
| `sv` | svenska |
| `no` | norsk |
| `da` | dansk |
| `fi` | suomi |
| `cs` | čeština |
| `hu` | magyar |
| `ro` | română |
| `uk` | українська |
| `el` | ελληνικά |
| `he` | עברית |
| `tr` | Türkçe |
| `fa` | فارسی |

---

## 8. Limits

| Item | Limit |
|------|-------|
| Agent daily requests | 20 |
| Agent identity inactivity expiry | Configurable (default 3 days) |
| Single file size (URL) | 100MB |
| Single file size (Base64) | 10MB |
| Max files per request | 20 |
| Supported formats | DOCX, MD, TXT, PDF |
| Download link validity | 2 hours |

Agent identities expire after a configurable period of inactivity. Each successful API call resets the timer. When expired, the agent name is released and can be re-registered with a new invite code via `POST /api/agent/activate`.
