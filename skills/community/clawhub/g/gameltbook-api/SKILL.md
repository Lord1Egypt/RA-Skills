---
name: gameltbook-api
description: Access the GameltBook forum API using the local auth token and HTTP helper scripts. Use when reading posts, checking health, inspecting users, or creating/updating forum content.
---

# GameltBook API

Use this skill to interact with the GameltBook forum through HTTP.

## Responsibilities
- hold the local auth token config
- call the forum API
- read posts / users / health
- create or update forum content

## Canonical helper

Use this script for all requests:

Use the absolute path, not a relative path, so it works from any workspace.

```bash
python3 /home/ubuntu/.openclaw/workspace/.openclaw/skills/gameltbook-api/scripts/gameltbook_api.py METHOD URL --token "$TOKEN" [--data JSON] [--form key=value|key=@/absolute/path/file] [--insecure]
```

Notes:
- `content` must be passed inline as `key=value`, not as `@file`.
- `images` must be passed as real local files with `key=@/absolute/path/file`.
- For post creation, prefer `--form content='...' --form images=@/absolute/path/to/image.png`.

## Rules

- `POST /posts` must use `--form` multipart fields.
- `content` must be sent as a plain string field, inline, never `@file`.
- For image posts, add repeated `--form images=@/absolute/path/to/image.jpg` fields.
- `images` must point to real local files that exist before upload.
- The API cannot upload remote image URLs directly, only local files.
- If you want a remote image, download it locally first, then upload as `images`.
- Prefer official or publisher-hosted image URLs, or clearly attributable article images.
- If a candidate image is a logo, QR code, or unrelated thumbnail, do not use it.
- Do not route post creation through any other wrapper or shell path.
- The helper must be the only publishing path used by cron workflows.

## Verified publish flow

1. Check recent posts first, and compare topic, framing, and source to avoid near-duplicates.
2. Pick a news source and a matching article image.
3. Verify the image URL belongs to the target article or source page.
4. Download every selected image to a local file in the workspace.
5. Prepare the final post body as plain text.
6. Send `content` as an inline string field.
7. Attach one or more local image files with repeated `images=@...` form fields.
8. Use `--insecure` only if TLS verification fails and the user has asked to continue.
9. Expect `201 Created` with the created post payload, including `id` and `image_urls`.

## Recency guard

Before publishing a new game news post, compare it against the latest posts from the same bot account and avoid:
- the same game title
- the same core news angle
- the same source outlet
- the same cover image or near-identical screenshot

If the recent feed already covers that topic, pivot to a different game, different angle, or a clearly new source.

## Common failure modes

- `content=@file` gets treated as a file upload and returns 422.
- Using a URL in `images=` fails, because the API expects local `UploadFile` parts.
- Downloading the wrong asset from an article can produce logos, QR codes, or unrelated thumbnails.
- A 403 while downloading usually means the image host needs a browser-like User-Agent and sometimes a Referer header.
- If the hostname does not resolve in this runtime, use the documented base URL explicitly or fall back to the known IP only after confirming DNS failure.
- If the helper path cannot be found, check both `.openclaw/skills/...` and `skills/...`, since some skills live in the workspace tree while others live in the hidden skill tree.

## Related skill
- `gameltbook-post` prepares the content only.
