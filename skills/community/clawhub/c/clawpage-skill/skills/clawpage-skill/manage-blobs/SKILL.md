---
name: manage-blobs
description: Upload images and files to Cloudflare R2 storage, get public URLs to embed in HTML pages. Use when the user wants to "upload a photo", "add an image to my page", "share a PDF", "replace the image", or needs persistent file storage for their Clawpage site. All uploads are public (anyone with the URL can view).
---

# manage-blobs

Clawpage stores blobs (images, documents, any binary file) in Cloudflare R2. Access URLs look like `https://blob.clawpage.ai/<random-id>.<ext>` — public, CDN-cached, zero bandwidth cost.

- **Upload**: `POST <user>.clawpage.ai/api/blobs` (multipart, owner Bearer)
- **Serve**: `GET blob.clawpage.ai/<r2Key>` (no auth, R2 direct via CDN)
- **All blobs are public**: if you need private files, don't upload them here

## When to use

- Embed images in Clawpage HTML pages: `<img src="https://blob.clawpage.ai/abc.png">`
- Share downloadable files (PDFs, ZIPs)
- Store avatars, icons, favicons
- Any binary file ≤ 10 MB

**Don't** upload: anything confidential; anything that must be auth-gated; files > 10 MB.

> **Management pages:** if rendering blob data in a pagecode-protected management page, use `c.blobs` from the Clawpage JS SDK — see `${CLAUDE_SKILL_DIR}/use-sdk/SKILL.md`. Raw `fetch('/api/blobs/...')` in page JS is forbidden.

## Quotas

- **Per file**: 10 MB max
- **Per user total**: 500 MB
- **Rate limit**: 60 uploads per hour per user

## CLI usage

```bash
# Upload
npx -y @clawpage.ai/cli blobs --upload ./photo.png
# → returns { blobId, url, filename, size, ... }

# List
npx -y @clawpage.ai/cli blobs --list

# Delete
npx -y @clawpage.ai/cli blobs --delete aB3kFq9N2p

# Check usage
npx -y @clawpage.ai/cli blobs --usage
```

## Typical workflow: add an image to a page

1. Upload: `npx -y @clawpage.ai/cli blobs --upload ./hero.jpg`
2. Copy the returned `url` (e.g. `https://blob.clawpage.ai/aB3kFq9N2p.jpg`)
3. In your HTML: `<img src="https://blob.clawpage.ai/aB3kFq9N2p.jpg" alt="Hero" />`
4. Publish the page as usual via `npx -y @clawpage.ai/cli publish ...`

## Important limitations

- **No image transformations**: if you need thumbnails or resized variants, do it before upload
- **All uploads public**: the URL is all the access control; don't upload anything you wouldn't paste publicly
- **No download counting**: we can't track views of direct-R2 URLs (lives outside our server)
- **Extension auto-inferred**: from filename then MIME; we only keep `[a-z0-9]{1,10}` — weird extensions become no extension
- **Orphan risk**: in a rare failure scenario a blob might exist in R2 but not Redis. Use CLI --list to see your accessible blobs.

## Error codes

| Code | HTTP | Fix |
|---|---|---|
| `BLOB_TOO_LARGE` | 413 | File > 10 MB; resize/recompress before upload |
| `BLOB_QUOTA_EXCEEDED` | 413 | You're at 500 MB; `--delete` old blobs |
| `BLOB_RATE_LIMITED` | 429 | Wait up to an hour; uploads are capped at 60/h |
| `BLOB_NOT_FOUND` | 404 | Wrong blobId or not yours |
| `INVALID_UPLOAD` | 400 | Check that the file exists and the CLI command is well-formed |
| `PERMISSION_DENIED` | 403 | Token's owner doesn't match the host subdomain — check keys.local.json |
| `UNAUTHORIZED` | 401 | Missing / invalid token |
