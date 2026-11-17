---
name: bulk-publish
description: Upload media files (local or URL), manage media library, and batch-create posts via BulkPublish. Use when the user wants to upload files or publish content in bulk.
---

# BulkPublish — Media & Bulk Publishing Reference

## upload_media parameters

```
url       (string, optional) — public URL to download from
filePath  (string, optional) — absolute local file path (e.g. /Users/me/photo.png)
filename  (string, optional) — override filename, otherwise derived from url/path
```

Provide either `url` OR `filePath`, not both.

## Supported formats

| Type | Formats | Max size |
|---|---|---|
| Image | JPEG, PNG, WebP, GIF | 100MB |
| Video | MP4, MOV, WebM | 100MB (up to 1GB via multipart — see below) |

## Response

Returns: `id` (use this in `mediaFileIds` when creating posts), `fileName`, `mimeType`, `sizeBytes`, `width`, `height`, `duration` (video), `originalUrl`, `thumbnailUrl`, `previewUrl`.

## Other media tools

| Tool | Use for | Key params |
|---|---|---|
| `list_media` | Browse uploaded files | `search`, `page`, `limit` |
| `get_media` | Single file details | `mediaId` |
| `delete_media` | Remove a file | `mediaId` |

## Media requirements by platform

| Platform | Image | Video | Notes |
|---|---|---|---|
| Instagram Reels | — | MP4, 9:16 | 3 seconds–15 minutes |
| Instagram Stories | JPEG/PNG, 9:16 | MP4, 9:16 | 1080x1920 recommended; video 3–60 seconds |
| Instagram Carousel | JPEG/PNG | — | 2-10 images |
| TikTok | — | MP4 | Up to 3 minutes for every account; some accounts 5 or 10 |
| YouTube | — | MP4 | Requires title in platformSpecific |
| Pinterest | JPEG/PNG, 2:3 | MP4 | 1000x1500 recommended; video pins at least 4 seconds |
| Facebook/X/LinkedIn | JPEG/PNG | MP4 | Most formats accepted |

## Large files — multipart upload (REST API)

For videos over 100MB (up to **1GB**), use the chunked multipart flow: MCP tools `create_multipart_upload`, `complete_multipart_upload`, `abort_multipart_upload`, or the REST API (`Authorization: Bearer bp_your_key`, base `https://app.bulkpublish.com`):

1. `POST /api/media/multipart/create` — body `{contentType, sizeBytes}` (exact size) → `{r2Key, uploadId, partSize, partUrls, expiresIn}`. `partSize` is fixed at 10MB (10485760); `partUrls` is one presigned PUT URL per part, in order; URLs expire in 3600s.
2. `PUT` each 10MB slice of the file to its `partUrl` and save the `ETag` response header per part. A failed part can be retried alone — a network drop never restarts the whole file.
3. `POST /api/media/multipart/complete` — body `{r2Key, uploadId, parts: [{partNumber, etag}], fileName, mimeType, sizeBytes, width?, height?, duration?}` → `{file}` (same media object as a normal upload; its `id` goes in `mediaFileIds`). Failed assembly auto-aborts the upload.

- To cancel mid-flight: `POST /api/media/multipart/abort` — body `{r2Key, uploadId}` (frees stored parts)
- 400 = disallowed type or too large; 403 with `error.code: "QUOTA_EXCEEDED"` = storage quota exceeded

## Bulk actions and approval

`bulk_posts` (`delete` | `retry` | `reschedule`) does not take `requestApproval`.
A bulk `retry` on posts whose role lacks `post:publish` fails with **403
`APPROVAL_REQUIRED`** — those posts must be submitted for team approval instead
(create/update with `requestApproval: true`, then a teammate calls
`approve_post`). Posts with `approvalStatus` `"pending"` or `"rejected"` do
not publish, even after a `reschedule`, until they are approved.

A bulk `reschedule` counts against the same scheduling limits as creating a
post: moving drafts past the pending-scheduled cap, or more posts onto one day
than the per-day cap allows, returns **403** `QUOTA_EXCEEDED` and changes
nothing. It returns **400** when `scheduledAt` is missing or not an ISO 8601
date-time, or when none of the posts is a draft or scheduled. See
the `schedule-post` skill for the full approval flow.

## Bulk pattern

For multiple files: call `upload_media` for each file, collect the returned IDs, then pass all IDs in `mediaFileIds` when creating the post.
