# Files — Uploads and Downloads

## Multipart Uploads

- Never hand-set `Content-Type: multipart/form-data`: the boundary parameter must match the body, and a hand-set header omits it — the top cause of a 400 on an upload that "looks right". Let the HTTP client generate the header from the parts.
- The file part carries its own `Content-Type`; a default `application/octet-stream` gets rejected by APIs that validate media types — set the real type on the part.
- Field order can matter: some upload targets (S3 POST policies) require the file field last, after the policy fields.
- Non-ASCII filenames need RFC 6266 `filename*=` encoding; naive clients send mojibake and some servers reject the part.

## Large Files

- Prefer the provider's direct-upload flow when offered: request a presigned/upload URL from the API, then PUT the bytes straight to storage — it bypasses the API server's body-size limit entirely. Presigned URLs expire (S3 caps at 7 days; most providers issue minutes-to-hours): generate one per upload, never store one.
- Base64-in-JSON inflates size by 4/3 (~33%): a 5 MB request limit fits only ~3.75 MB of file. Hitting a size limit "early" is usually this.
- Unreliable links or multi-GB files → resumable protocols (S3 multipart, Google resumable, tus): retrying one chunk beats retrying the whole file.
- Some services require `Content-Length` up front and reject chunked transfer encoding with a 411 — know the file size before streaming the request body, or use the provider's multipart-upload API.

## Downloads

- APIs that 302 to storage (release assets, export files): many HTTP clients forward your `Authorization` header to the redirect host, and S3 rejects a request carrying both an auth header and presigned query params — strip auth when following a cross-host redirect, or read the `Location` and fetch it with a clean client.
- Stream to disk; buffering a multi-GB export in memory is an OOM that dev-sized data never showed (SKILL.md Traps).
- Verify completeness: compare received bytes against `Content-Length`, or the checksum when provided — a dropped connection can return success with a truncated file.
- Resume with `Range` plus `If-Range: <etag>` so a file that changed server-side restarts cleanly instead of splicing two versions together.
- A `.gz` file served with `Content-Encoding: gzip` arrives already decompressed by auto-decoding clients — saving those bytes with a `.gz` name produces a "corrupt" archive. Disable auto-decode for archive downloads or drop the extension.
- Write bytes, not text: text-mode writes translate line endings and corrupt binaries on Windows.
