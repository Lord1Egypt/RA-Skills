---
name: dropage-deploy
description: Deploy an HTML page to the internet and return a public URL. Use when the user asks to deploy, host, share, or publish an HTML file or a zip / tar / tar.gz / tgz archive containing an index.html. Triggers on phrases like "deploy this page", "host this online", "share this HTML", "upload to web", "get a link".
disable-model-invocation: true
allowed-tools: Bash(curl *)
---

# Deploy to Dropage

Upload an HTML file or a zip / tar / tar.gz / tgz archive to `dropage.online` and return a public URL. Default expiry is 1 hour; the user may also choose 6 hours, 24 hours, 7 days, or 14 days, and optionally have the page disabled after 1 or 10 visits. Uploaded files are retained until 30 days after upload, independently of public link expiry.

## Platform Detection

Before running the upload command, detect the user's platform and use the appropriate curl command:

- **Windows**: `curl.exe`
- **macOS/Linux**: `curl`

## Optional upload fields

Both are optional; omit to use defaults.

- `expiry` — one of `1h` (default), `6h`, `24h`, `7d`, `14d`
- `max_visits` — `0` (default, unlimited), `1`, or `10`. Page is disabled after the limit is reached.

## Daily quotas and user reminders

| Expiry | Site-wide successful uploads/day | Successful uploads/IP/day |
| --- | --- | --- |
| `7d` | 50 | 5 |
| `14d` | 10 | 1 |

The tiers have separate quotas. Each resets at 00:00 UTC+8 on the next calendar day. Only successful uploads count, including records later expired or cleaned; deletion does not refund quota. The `1h`, `6h`, and `24h` tiers have no extra daily quota. All tiers still follow per-IP rate limits and the site-wide 1,000 uploads/hour limit.

Before a 7-day or 14-day upload, tell the user the selected tier's site-wide and per-IP daily limits and reset time. Use the requested expiry; if it is unspecified, use 1 hour. Never silently shorten a requested expiry to bypass an exhausted quota. Existing uploaded pages keep their expiration times; use the five current values for new uploads. The API still accepts legacy `10m`, `3h`, and `12h` for old clients. A successful legacy response adds `warning: {code: "LEGACY_EXPIRY", message: "...", skill_url: "https://dropage.online/dropage-deploy.md"}`. Report that the upload succeeded, ask the user to update their installed skill from `skill_url`, and do not retry the successful upload.

## Steps

1. Identify the file to deploy. Accept a single `.html` file or an archive (`.zip`, `.tar`, `.tar.gz`, `.tgz`) whose root contains `index.html`.

   **Archive packaging requirements:**
   - Supported formats: `.zip`, `.tar`, `.tar.gz`, `.tgz` (NOT `.7z`, `.rar`, `.tar.bz2`, `.tar.xz`)
   - `index.html` must be at the **root** level of the archive, not inside a subfolder
   - Correct: `site.zip` → `index.html`, `style.css`, `js/`
   - Wrong: `site.zip` → `my-site/index.html`, `my-site/style.css`
   - If all entries share a single top-level directory (e.g. `my-site/`), it is auto-stripped during extraction
   - Max 50 files per archive
   - Avoid Chinese or special characters in filenames to prevent encoding issues

2. Detect platform and run the upload command:

### Windows (PowerShell / CMD)

```bash
curl.exe -s -F "file=@<filepath>" -F "expiry=1h" -F "max_visits=0" https://dropage.online/api/upload
```

### macOS / Linux (Bash / Zsh)

```bash
curl -s -F "file=@<filepath>" -F "expiry=1h" -F "max_visits=0" https://dropage.online/api/upload
```

3. Parse the JSON response and report the result to the user.

## Response format

Success (HTTP 201):
```json
{"success": true, "url": "https://dropage.online/a1b2c3d4e5f6/", "expires_at": "2026-06-29T14:00:00+08:00", "max_visits": 0, "id": "a1b2c3d4e5f6"}
```

Failure (HTTP 4xx):
```json
{"success": false, "error": "reason"}
```

### 14-day upload: concrete quota failure examples

Use `-i` to include the HTTP status and `Retry-After` header:

```bash
# Windows
curl.exe -sS -i -F "file=@page.html" -F "expiry=14d" https://dropage.online/api/upload

# macOS/Linux
curl -sS -i -F "file=@page.html" -F "expiry=14d" https://dropage.online/api/upload
```

The following examples assume a request at **2026-09-05 23:00 UTC+8**. The actual reset is **2026-09-06 00:00 UTC+8**, returned as `2026-09-05T16:00:00.000Z` (UTC). `Retry-After: 3600` is illustrative; use the actual server response. The API's `error` text is currently Chinese regardless of the page language; interpret the structured fields and explain them in the user's language.

**Per-IP daily allowance exhausted:** this IP has already successfully uploaded one `14d` page today. Another `14d` upload is rejected:

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json; charset=utf-8
Retry-After: 3600
```

```json
{
  "success": false,
  "error": "14 天档当前 IP今日配额已用完（每天 1 个）。请在 UTC+8 次日 00:00 后重试，或选择其他有效期；仍受通用上传频率限制。",
  "code": "DAILY_QUOTA_EXCEEDED",
  "expiry": "14d",
  "scope": "ip",
  "limit": 1,
  "reset_at": "2026-09-05T16:00:00.000Z"
}
```

Tell the user: “The upload failed because this IP has used today's one-upload allowance for the 14-day tier. It resets at 2026-09-06 00:00 UTC+8. No new page was created.”

**Site-wide daily allowance exhausted:** ten `14d` uploads have already succeeded today. An additional request from an IP that has not used its own allowance is rejected:

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json; charset=utf-8
Retry-After: 3600
```

```json
{
  "success": false,
  "error": "14 天档全站今日配额已用完（每天 10 个）。请在 UTC+8 次日 00:00 后重试，或选择其他有效期；仍受通用上传频率限制。",
  "code": "DAILY_QUOTA_EXCEEDED",
  "expiry": "14d",
  "scope": "global",
  "limit": 10,
  "reset_at": "2026-09-05T16:00:00.000Z"
}
```

Tell the user: “The upload failed because today's site-wide allowance of ten 14-day pages is exhausted. It resets at 2026-09-06 00:00 UTC+8. No new page was created.”

When both daily limits are exhausted, the API reports `scope: "ip"` first. The general upload rate limiter runs before daily quota checks and can instead return a generic HTTP 429 without `DAILY_QUOTA_EXCEEDED`; do not assume every 429 is a daily quota error. A rejected upload returns no public URL, creates no upload record, and consumes no additional daily quota. Do not loop retries or silently change `expiry`. Wait until the reported reset, or let the user choose another tier.

## Report to the user

On success, show:
- The public URL
- Expiration time (per the chosen expiry; default 1 hour from upload)
- Visit limit, if any (disabled after 1 or 10 visits)

On failure, show the error reason. For HTTP 429, inspect `code` and `Retry-After`. When `code` is `DAILY_QUOTA_EXCEEDED`, report the affected `expiry`, `scope` (`ip` or `global`), `limit`, and `reset_at` to the user. Wait until reset, or let the user choose another suitable tier; do not immediately retry.

## Limits

- File types: `.html`, `.zip`, `.tar`, `.tar.gz`, `.tgz` only
- Max size: 30 MB
- Archive must contain `index.html` at the root level
- Max 50 files per archive
- Expiry: `1h` (default) / `6h` / `24h` / `7d` / `14d`
- Max visits: `0` (unlimited, default) / `1` / `10`
- Storage retention: uploaded files are physically deleted 30 days after upload; database metadata is retained. Expiry and visit limits still disable public access earlier.
- Access log retention: 30 days
- Rate limit: 3 per minute, 30 per half hour, 45 per hour per IP

## Examples

### Deploy a single HTML file (defaults)

```bash
# Windows
curl.exe -s -F "file=@index.html" https://dropage.online/api/upload

# macOS/Linux
curl -s -F "file=@index.html" https://dropage.online/api/upload
```

### Deploy a zip archive

```bash
# Windows
curl.exe -s -F "file=@site.zip" https://dropage.online/api/upload

# macOS/Linux
curl -s -F "file=@site.zip" https://dropage.online/api/upload
```

### Deploy a tar.gz archive (Linux/macOS common)

```bash
# Windows
curl.exe -s -F "file=@site.tar.gz" https://dropage.online/api/upload

# macOS/Linux
curl -s -F "file=@site.tar.gz" https://dropage.online/api/upload
```

### Deploy with 1-hour expiry, disabled after 1 visit

```bash
# Windows
curl.exe -s -F "file=@index.html" -F "expiry=1h" -F "max_visits=1" https://dropage.online/api/upload

# macOS/Linux
curl -s -F "file=@index.html" -F "expiry=1h" -F "max_visits=1" https://dropage.online/api/upload
```

### Deploy with long expiry (daily quotas apply)

`7d`: 50 successful uploads/day site-wide, 5/IP/day. `14d`: 10 site-wide, 1/IP/day. Reset: 00:00 UTC+8.

```bash
# Windows: 7 days
curl.exe -s -F "file=@index.html" -F "expiry=7d" https://dropage.online/api/upload
# macOS/Linux: 14 days
curl -s -F "file=@index.html" -F "expiry=14d" https://dropage.online/api/upload
```

For 6-hour or 24-hour expiry, use `-F "expiry=6h"` or `-F "expiry=24h"` respectively.

### Deploy from specific path

```bash
# Windows
curl.exe -s -F "file=@C:\Users\me\project\index.html" https://dropage.online/api/upload

# macOS/Linux
curl -s -F "file=@/home/user/project/index.html" https://dropage.online/api/upload
```

## Troubleshooting

### "file not found" error
- Verify the file path is correct and the file exists
- On Windows PowerShell, use backward slashes or absolute paths: `@C:\path\to\file.html`
- On macOS/Linux, use forward slashes: `@/home/user/file.html`
- If the path contains spaces, quote it: `@"C:\path with spaces\file.html"` (Windows) or `@"/path/with spaces/file.html"` (macOS/Linux)

### Empty file or wrong file type
- File must be non-empty and have one of these extensions: `.html`, `.zip`, `.tar`, `.tar.gz`, `.tgz` (case-insensitive)
- Hidden files (e.g. `.html` files starting with a dot) are not supported

### HTTP 400 (Bad Request) — "不支持的文件格式"
- File extension must be one of: `.html`, `.zip`, `.tar`, `.tar.gz`, `.tgz`
- Do not use `.htm`, `.xhtml`, `.rar`, `.7z`, `.tar.bz2`, `.tar.xz`, or other formats

### HTTP 400 (Bad Request) — Archive errors
- Archive does not contain `index.html` at the root level (after top-level directory stripping)
- Archive has more than 50 files
- Archive is corrupted, truncated, or uses unsupported compression
- For tar.gz: ensure the file is a valid gzip-compressed tar (not raw gzip of a single file)

### HTTP 413 (Payload Too Large)
- File exceeds the 30 MB limit
- Compress images or assets before deploying
- For large projects, consider splitting into multiple deployments

### HTTP 429 (Too Many Requests)
- Rate limit exceeded: 3 per minute, 30 per 30 minutes, 45 per hour per IP
- Wait for the cooldown period before retrying
- Daily quota errors have `code: DAILY_QUOTA_EXCEEDED` plus `expiry`, `scope`, `limit`, and `reset_at`. Tell the user whether the site-wide or per-IP allowance is exhausted and show the reset time (00:00 UTC+8). Honor `Retry-After`; do not loop retries or silently choose a shorter expiry.
- An expired or cleaned page still counts toward the day on which it was successfully uploaded. Failed uploads do not consume daily quota.
