---
name: doc-to-slides
description: Convert documents or text into PDF slide presentations via the Ruyi Converter API at nyoi.io. Use this skill whenever the user wants to create slides, presentations, PPTs, or slide decks from text, markdown, or document files (DOCX, PDF, TXT, MD). Also trigger when user mentions keywords like "slides", "presentation", "PPT", "slide deck", "pitch deck", or wants to turn notes/content into a visual presentation format.
---

# Doc to Slides

Convert text content or document files into PDF slide presentations using the Ruyi Converter API.

**Base URL**: `https://www.nyoi.io`

## Credential check

1. If you have an API key (`rk_` prefix) from a previous interaction:
   a. Check identity: `GET https://www.nyoi.io/api/agent/identity` (X-Api-Key header)
   b. If valid → proceed to "Core workflow"
   c. If 403 (expired) or 401 (invalid) → obtain a new credential (step 2)
2. To obtain a new credential:
   a. `GET https://www.nyoi.io/api/agent/invite-code` → get an invite code
   b. `POST https://www.nyoi.io/api/agent/activate`
      Body: `{ "inviteCode": "<code>", "name": "<choose a name>" }`
      → returns apiKey (`rk_xxx`, shown only once)
   c. If 409 (name taken), pick a different name
   d. If 404 (no invite codes), ask user to contact the administrator
3. Tell the user the API key so they can note it if desired

The agent identity expires after a period of inactivity (configured by the server).
Each API call resets the inactivity timer. If expired, the name is released and
can be re-registered with a new invite code.

---

## Core workflow

### Input formats

Three ways to provide content:

**Option 1: Plain text** (most common)
```json
{
  "text": "# Heading\n\n## Section 1\nContent...\n\n## Section 2\nContent...",
  "title": "My Presentation",
  "language": "en"
}
```

**Option 2: File URLs**
```json
{
  "files": ["https://example.com/report.docx"],
  "title": "Project Report",
  "language": "en"
}
```

**Option 3: Base64 encoded** (< 10MB)
```json
{
  "files": ["data:application/pdf;base64,AAAA..."],
  "title": "My Presentation"
}
```

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `text` | string | either text or files | - | Text content |
| `files` | string[] | either text or files | - | File URLs or Base64 strings |
| `title` | string | no | `"Presentation"` | Slide deck title |
| `language` | string | no | `"en"` | Output language (ISO 639-1 code) |

### Submit job

```bash
curl -s -X POST https://www.nyoi.io/api/tools/doc-to-slides/execute \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: <API_KEY>" \
  -d '<JSON body>'
```

Response:
```json
{
  "success": true,
  "data": {
    "jobId": "job_xxx",
    "toolId": "doc-to-slides",
    "status": "pending"
  }
}
```

### Poll job status

```bash
curl -s https://www.nyoi.io/api/jobs/<jobId>
```

No authentication required. Slide generation typically takes **8–16 minutes** and may take up to **30 minutes** for large documents. Poll every 30 seconds until `status` is `completed` or `failed`.

Status flow: `pending` -> `queued` -> `assigned` -> `running` -> `completed` / `failed`

### Download result

On completion, `artifacts[0].url` contains a pre-signed download link (PDF), valid for 2 hours.

```json
{
  "data": {
    "status": "completed",
    "artifacts": [{
      "type": "slides",
      "url": "https://cos.example.com/output/slides.pdf?sign=xxx",
      "expiresAt": "2026-03-17T20:00:00Z",
      "expiresIn": 7200
    }]
  }
}
```

### Deliver the file to the user

> **IMPORTANT**: Do NOT just output the URL as text. You must send the PDF file through your messaging platform.

1. Check what tools you have for sending messages or files (e.g. a `message` / `send` / `reply` tool that accepts `media`, `file`, `file_url`, or similar parameters).
2. Use that tool to send `artifacts[0].url` as a **file or media attachment** so the user receives the PDF directly in the chat.
3. Only fall back to displaying the URL as text if you truly have no file-sending capability.

The link is valid for 2 hours. If it expires, re-request `GET /api/jobs/<jobId>` for a fresh URL.

---

## Error handling

| Scenario | Status | Action |
|----------|--------|--------|
| No invite codes available | 404 | Ask user to join the Discord for help: https://discord.gg/uk6q2uPfpg |
| Invite code already used | 409 | Claim a new code and retry |
| Name already taken | 409 | Pick a different name |
| Agent identity expired | 403 | Activate with a new invite code |
| Invalid API Key | 401 | Activate with a new invite code |
| Daily quota exhausted (20/day) | 429 | Inform user to try again tomorrow |
| Tool not allowed for agent | 403 | Agent accounts can only use doc-to-slides |
| Job still running after 30 min | - | Ask user to check service status or join Discord: https://discord.gg/uk6q2uPfpg |
| Job failed | - | Read the error field from the job response |

---

## Supported languages

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

---

## Support

If something isn't working or you need invite codes, join our Discord: https://discord.gg/uk6q2uPfpg

---

For full API reference with request/response examples, read `{baseDir}/references/api-reference.md`.
