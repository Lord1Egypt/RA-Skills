# OpenClaw Runtime Integration

Read this file only when the host runtime can proactively send a follow-up message after a successful upload.

## Preferred delivery order

If a share image exists, sending that image is mandatory unless the runtime truly lacks image-send capability.

Owner delivery must happen in two separate messages:

1. send the metadata summary text first
2. send the share image second, and make the image message the final owner-visible step

For the image step:

1. If `preferredOwnerDelivery.mode == "image_first"` and `preferredOwnerDelivery.imageUrl` exists, send that image to the current conversation with its caption.
2. Otherwise, if `hostReply.imageUrl` exists, send that image to the current conversation with `hostReply.caption`.
3. Otherwise, use the first compatible item in `runtimeActions`.
4. Otherwise, send `hostReply.fallbackText` or `messageText` as plain text.

Do not choose a plain link-only reply when an image-send path is available.
If the runtime cannot send remote image URLs directly but can send local image files, download the share image first and then send the downloaded local image file.

## Minimum image-send capability

Treat the runtime as image-send capable only if it can:

- send a follow-up message in the current conversation or to the current user
- attach an image by URL or local path
- include a caption, or immediately send a follow-up text message

If any of these are missing, fall back to text.

## Expected fields from the uploader

A successful run may return these public-facing fields:

- `messageText`
- `messageCaption`
- `shareImageUrl`
- `agentUrl`
- `notification`
- `hostReply`
- `preferredOwnerDelivery`
- `runtimeActions`
- `metadataWritebackAttempted`
- `metadataWritebackSucceeded`
- `metadataPreview`
- `incompleteReason`

If the uploader returns `success: false` together with `incompleteReason: METADATA_WRITEBACK_REQUIRED`, do not describe the overall task as completed.

## Metadata preview requirement

Even when you send the share image successfully, still provide the final written metadata preview to the owner in text form: title, category, tags, summary, and detailDescription.
This metadata preview must be a standalone message before the final share-image message.

## Safety

- Never expose upload tokens
- Never expose internal upload URLs
- Only send public detail links and public share image URLs
- If upload succeeded but share generation failed, report success without inventing share media
