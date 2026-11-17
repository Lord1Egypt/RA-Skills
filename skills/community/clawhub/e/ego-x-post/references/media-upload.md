# Media upload (captured 2026-11-04)

Source: Ego Lite on a logged-in `https://x.com` page. The composer uploaded one PNG. The same bytes were then uploaded from inside the page (`page.evaluate` + `fetch`) as one segment and as three 32 KiB segments. No Post button was clicked. No CreateTweet was sent by that capture. Client bundle: `main.0a76dc3677efe2b2a.js`.

This file is the contract for `--image`. Do not add hosts, commands, or body fields that are not listed here.

## What `--image` accepts

| Rule | Value |
|------|--------|
| Flag | repeatable `--image <path>` |
| Count | at most 4 |
| Types | png, jpeg (`.jpg` / `.jpeg`), webp |
| GIF | rejected. `media_category=tweet_gif` and STATUS polling were not exercised |
| Size | each file ≤ 5 MiB (5242880 bytes) |
| When | existence, type, size, and count are checked before any network call. A bad file exits 1 |
| Gate | without `--yes`, print path, bytes, and md5. Do not upload and do not post |

The file extension and the leading magic bytes must agree (`image/png`, `image/jpeg`, `image/webp`). `media_type` in INIT is that MIME type. `media_category` is always `tweet_image`.

## Endpoint

`https://upload.x.com/i/media/upload.json`

Every parameter is in the query string. The body is empty except APPEND.

| Step | Request | Status |
|------|---------|--------|
| INIT | `POST ?command=INIT&total_bytes=N&media_type=image%2Fpng&media_category=tweet_image` | **202** `{ media_id_string, expires_after_secs, media_key }` |
| APPEND | `POST ?command=APPEND&media_id=ID&segment_index=i` | **204** empty |
| FINALIZE | `POST ?command=FINALIZE&media_id=ID&original_md5=<hex md5 of the whole file>` | **201** JSON |
| STATUS | `GET ?command=STATUS&media_id=ID` | only when FINALIZE includes `processing_info` |

Use `media_id_string`. Do not use the numeric `media_id` (a snowflake does not fit in a JS number).

APPEND is one multipart part: name `media`, filename `blob`, content-type `application/octet-stream`. The browser sets the multipart boundary. Do not set `content-type` yourself.

Chunks are 1 MiB, and never larger than 5 MiB. One `page.evaluate` call sends one command, so a multi-megabyte file does not cross the bridge as a single argument. Images at the 5 MiB cap therefore take at most five APPENDs. Segment indexes start at 0. A three-segment upload was verified.

FINALIZE `original_md5` is the md5 of the original file, lowercase hex. The capture had `responsive_web_media_upload_md5_hashing_enabled` on, and the composer sent it.

Images in the capture returned 201 with no `processing_info`. Do not call STATUS in that case. A manual STATUS on a finalized image returned 404 code 34. If FINALIZE does include `processing_info`, poll STATUS after `check_after_secs` (default 10) while `state` is `pending` or `in_progress`. `succeeded` is done. `failed` uses `error.code` 0..4: INTERNAL_ERROR, INVALID_MEDIA, FILE_TOO_LARGE, UNSUPPORTED_MEDIA, TIMEOUT. This branch is for video/GIF and was not hit by the image capture. This skill stops after 30 polls.

INIT and FINALIZE are tried twice (one retry). APPEND is tried up to 5 times. HTTP 401 and 429 are not retried. 401 is exit 2 (login). Other upload failures are exit 1 and the tweet is not sent.

## Headers

Same public web bearer as CreateTweet, `x-csrf-token` = `ct0`, `x-twitter-auth-type: OAuth2Session`. Cookies ride on `credentials: "include"`.

Do **not** send `x-client-transaction-id` on INIT, APPEND, FINALIZE, or STATUS. That header belongs only to the later GraphQL POST.

The call has to run in the page. `page.fetch` from the Ego Node side can send INIT and FINALIZE (empty body) but cannot carry a `FormData` file. CORS from `https://x.com` allows the upload host with credentials. The skill therefore runs every step, including INIT and FINALIZE, inside `page.evaluate`: base64 in, `Uint8Array` → `Blob` → `FormData`, then `fetch`. Node-side upload was not tested and would need the HttpOnly `auth_token`, which stays in the browser.

## CreateTweet / CreateNoteTweet

After every image has a `media_id_string`:

```json
"media": {
  "media_entities": [
    { "media_id": "<media_id_string>", "tagged_users": [] }
  ],
  "possibly_sensitive": false
}
```

Order is the `--image` order. `tagged_users` stays empty. No alt text, crop, or sensitive flag is sent. The rest of the body is unchanged (`references/create-tweet.md`).

CreateNoteTweet uses the same `media` object. `references/create-tweet.md` says note variables match CreateTweet except `semantic_annotation_options` (`composition_signal_1: true` plus `source`). The note capture itself was text-only, and the media-entity builder in the capture notes was read from the CreateTweet path. A long post with an image was not verified on the wire. `--long --image` still sends this object rather than inventing a second shape. Live acceptance still has to confirm it.

There is no captured call that deletes an orphan upload. A file that uploads and then fails to post expires in about 24 hours (`expires_after_secs` 86400).

## Not in this skill

GIF, video, `upload2.json`, `APPENDMULTI`, tagging, alt text, and clicking the file input or the Post button.
