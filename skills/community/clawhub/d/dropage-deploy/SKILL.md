---
name: dropage-deploy
description: Deploy an HTML page to the internet and return a public URL. Use when the user asks to deploy, host, share, or publish an HTML file or a zip / tar / tar.gz / tgz archive containing an index.html. Triggers on phrases like "deploy this page", "host this online", "share this HTML", "upload to web", "get a link".
disable-model-invocation: true
allowed-tools: Bash(curl *)
---

# Deploy to Dropage

Upload an HTML file or a zip / tar / tar.gz / tgz archive to `dropage.online` and return a public URL. Default expiry is 1 hour; the user may also choose 10 minutes, 3 hours, or 12 hours, and optionally have the page deleted after 1 or 10 visits.

## Platform Detection

Before running the upload command, detect the user's platform and use the appropriate curl command:

- **Windows**: `curl.exe`
- **macOS/Linux**: `curl`

## Optional upload fields

Both are optional; omit to use defaults.

- `expiry` — one of `10m`, `1h` (default), `3h`, `12h`
- `max_visits` — `0` (default, unlimited), `1`, or `10`. Page is disabled after the limit is reached.

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

## Report to the user

On success, show:
- The public URL
- Expiration time (per the chosen expiry; default 1 hour from upload)
- Visit limit, if any (deleted after 1 or 10 visits)

On failure, show the error reason. If HTTP 429, tell the user to wait and retry.

## Limits

- File types: `.html`, `.zip`, `.tar`, `.tar.gz`, `.tgz` only
- Max size: 10 MB
- Archive must contain `index.html` at the root level
- Max 50 files per archive
- Expiry: `10m` / `1h` (default) / `3h` / `12h`
- Max visits: `0` (unlimited, default) / `1` / `10`
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

### Deploy with 10-minute expiry, deleted after 1 visit

```bash
# Windows
curl.exe -s -F "file=@index.html" -F "expiry=10m" -F "max_visits=1" https://dropage.online/api/upload

# macOS/Linux
curl -s -F "file=@index.html" -F "expiry=10m" -F "max_visits=1" https://dropage.online/api/upload
```

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
- File exceeds the 10 MB limit
- Compress images or assets before deploying
- For large projects, consider splitting into multiple deployments

### HTTP 429 (Too Many Requests)
- Rate limit exceeded: 3 per minute, 30 per 30 minutes, 45 per hour per IP
- Wait for the cooldown period before retrying
- Common when repeatedly deploying with incorrect settings — check the file first to avoid wasted attempts