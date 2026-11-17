---
name: "drop-files"
description: "Upload generated HTML/Markdown files to DropFiles and get a shareable public link. Invoke when the user wants to share, publish, or generate a public link for any HTML or Markdown content they produced."
---

# DropFiles

Upload HTML or Markdown content to the DropFiles service and return a public shareable link. The service is free, globally accessible, and hosted on Cloudflare's edge network.

## When to Invoke

Invoke this skill when the user wants to:
- Share generated HTML or Markdown content via a public link
- Publish a document, report, or page and get a URL to distribute
- Upload any text-based artifact (HTML/Markdown) for online viewing
- Generate a shareable preview link for content the agent just produced

## How to Upload

**Use the bundled wrapper script. Do NOT construct curl commands or JSON payloads manually.**

```bash
python3 scripts/upload.py [OPTIONS]
```

The script handles content reading, JSON serialization, temp-file management, curl invocation (Cloudflare WAF blocks non-curl HTTP clients), response parsing, and temp-file cleanup. Run `python3 scripts/upload.py --help` for the full interface.

### Content Source (priority: `--file` > `--content` > stdin)

- **stdin (preferred for piped content)**: `cat file.md | python3 scripts/upload.py --json`
- **`--file PATH`**: `python3 scripts/upload.py --file report.md --json`
- **`--content TEXT`**: only for short inline content

### Options

| Option | Values | Default | Notes |
|---|---|---|---|
| `--type` | `html` \| `markdown` \| `auto` | `auto` | `auto` detects HTML by `<html` / `<!doctype` prefix, else Markdown. |
| `--expire` | `1h` \| `1d` \| `7d` \| `30d` | `7d` | Link lifetime. |
| `--title` | string | — | Optional title shown on the share page. |
| `--lang` | `en` \| `zh` \| `auto` | `auto` | Language hint for the share page. |
| `--json` | flag | off | Output full JSON response (recommended for agents). Without it, prints human-readable `URL:` / `Preview:` / `Expires:` lines. |

### Password Policy

The default is **no password** — the share link is publicly accessible by anyone with the URL.

- **No password (default)**: omit both password flags.
- **User-supplied password**: pass `--password "the password"`.
- **Skill-generated 6-digit password**: pass `--generate-password`. The script generates a random 6-digit numeric code (e.g. `482917`), includes it in the upload, and surfaces it in the output. **Always relay the generated password back to the user** so they can share it with viewers.

## Workflow

1. Confirm the content to upload (HTML or Markdown). If the user just generated a document/page, use that content directly — write it to a temp file or pipe via stdin.
2. Determine options:
   - `type`: use `auto` unless the user specifies.
   - `expire`: default `7d` unless the user requests a different lifetime.
   - `title`: optional, set if the user provides one.
3. Determine password:
   - Default: no password.
   - If the user explicitly provides a password, pass it via `--password`.
   - If the user asks for protection without providing a password, pass `--generate-password`.
4. Call the wrapper script (use `--json` for reliable parsing):
   ```bash
   python3 scripts/upload.py --file content.html --type html --expire 7d --json
   ```
5. Parse the JSON output:
   - On success: `{"success": true, "data": {"url": "...", "preview_url": "...", "expire_at": "...", ...}}` (plus a top-level `password` field if `--generate-password` was used).
   - On failure: `{"success": false, "error": {"code": "...", "message": "..."}}`.
6. Return the `url` (and `preview_url` if relevant) to the user. If a password was generated, prominently display it: `Generated password: XXXXXX`.
7. On error, surface `error.message` to the user and suggest fixes (see error codes below).

## Error Codes

| Code | Meaning |
|---|---|
| `CONTENT_REQUIRED` | `content` field is empty. |
| `CONTENT_TOO_LARGE` | Content exceeds 5 MB. |
| `INVALID_TYPE` | `type` is not `html` / `markdown` / `auto`. |
| `INVALID_EXPIRE` | `expire` is not `1h` / `1d` / `7d` / `30d`. |
| `RATE_LIMIT_EXCEEDED` | Too many requests from the same IP — wait and retry. |
| `NETWORK_ERROR` | curl could not reach the server (local script-side). |
| `PARSE_ERROR` | Response could not be parsed (local script-side). |

## Limits

- Max content size: **5 MB** (UTF-8 bytes).
- Max expiry: **30 days**.
- Rate limiting applies per IP; if you hit `RATE_LIMIT_EXCEEDED`, wait and retry.

## Notes

- The share link is public (unless password-protected). Anyone with the URL can view the content.
- Viewers do not need an account.
- HTML content is sanitized server-side: `<script>` tags and event handlers are removed.
- Markdown supports standard GitHub-flavored Markdown including code blocks, tables, and images.
- The `preview_url` adds `?preview=1` and is useful when embedding the link in a context that should not inflate the access counter on initial load.
