# agenthost HTTP API

The publish contract. Base URL: `https://agenthost.page`. Plain `curl` throughout.

## Authentication

Two secrets, returned **once** by a site's first publish:

- **`ownerToken`** — account credential. Sent as `Authorization: Bearer <token>` on redeploys and owner endpoints. Only its SHA-256 is stored; lose it and you can only publish a new URL.
- **`accessKey`** — per-site password gating the private site. Embedded in `shareUrl` as `?k=<accessKey>`. Persists across redeploys.

Authenticated requests also need the account `username`, as `?username=<name>` or the `x-agenthost-user` header.

## POST /publish

Body is either a **gzipped tar** of a directory or a **single raw file**, selected by `Content-Type`.

| Param | Where | Notes |
|---|---|---|
| `id` | `?id=` or `x-agenthost-site` header | Subdomain label (`{username}-{id}.agenthost.page`). Generated if omitted. |
| `username` | `?username=` or `x-agenthost-user` header | Required **only** with `Authorization` (redeploys). |
| `file` | `?file=` | Single-file mode: names the stored file (sanitized). Optional. |
| `Authorization: Bearer <ownerToken>` | header | Omit for a first/anonymous publish (mints an account); include to redeploy. |

**Body format by `Content-Type`:**

- `application/gzip` (or any unrecognized/binary type) → **gzipped tar** of the site directory. Default.
- `text/html` / `application/xhtml+xml` → **single HTML file**, stored as `index.html` (serves at `/`).
- `text/markdown` / `text/x-markdown` → **single Markdown file**, stored as `README.md` (rendered at `/`).
- Any request with `?file=<name>` → **single file** under that name, regardless of `Content-Type`.

Single-file publish replaces the whole site with that one file; use a tar body for multiple files. Curl examples for all three modes are in [SKILL.md](../SKILL.md).

### Response (200)

```jsonc
{
  "url":        "https://cleverotter4f2-myblog.agenthost.page/", // bare URL (prompts for the key)
  "shareUrl":   "https://cleverotter4f2-myblog.agenthost.page/?k=<accessKey>", // give THIS to a human
  "username":   "cleverotter4f2",      // account name (auto-generated, no hyphens)
  "siteId":     "myblog",
  "generation": 2,                     // deploy counter (cache versioning)
  "fileCount":  12,
  "bytes":      48213,
  "accessKey":  "<shown once — first publish only>",
  "ownerToken": "<shown once — SAVE to redeploy>",
  "claimUrl":   "https://agenthost.page/claim?username=cleverotter4f2" // new accounts only
}
```

`accessKey` and `ownerToken` are returned **only on a site's first publish**; redeploys preserve them silently.

## Owner endpoints

All require `Authorization: Bearer <ownerToken>` + `username`, and (except `/claim`) the site `id`.

**`POST /key/public`** — drop or restore the access gate.

```bash
curl -s -X POST -H 'Authorization: Bearer <ownerToken>' \
  'https://agenthost.page/key/public?username=<username>&id=myblog&public=true'
# → { "ok": true, "public": true }
```

**`POST /key/rotate`** — new `accessKey`, **invalidates all existing share links**, flips back to private.

```bash
curl -s -X POST -H 'Authorization: Bearer <ownerToken>' \
  'https://agenthost.page/key/rotate?username=<username>&id=myblog'
# → { "ok": true, "accessKey": "<new key>", "public": false, "shareUrl": "…/?k=<new key>" }
```

**`POST /claim`** — attach an unverified recovery/abuse-contact email.

```bash
curl -s -X POST -H 'Authorization: Bearer <ownerToken>' \
  'https://agenthost.page/claim?username=<username>&email=you@example.com'
# → { "ok": true, "username": "<username>", "email": "you@example.com" }
```

## Errors

JSON `{ "error": "<message>" }` with the status:

| Status | Cause |
|---|---|
| 400 | Empty body, nameless single file, archive with no files, unsafe path (`..`), or symlink/hardlink entry. |
| 401 | Missing `username` with a Bearer token. |
| 403 | Invalid username or owner token (indistinguishable — no enumeration). |
| 405 | Non-POST to `/publish`. |
| 413 | Over per-file cap, too many files, or over the size budget. |
| 429 | Rate limit exceeded (per IP). Back off and retry. |

## URL & path rules

- Served at `https://{username}-{id}.agenthost.page/…`; each site is its subdomain root.
- `username` is `[a-z0-9]`, 2–30 chars (**no hyphens** — it separates `{username}-{id}`).
- `siteId` is lowercased, sanitized to `[a-z0-9._-]`, ≤32 chars (so the label fits 63 chars).
- macOS cruft (`.DS_Store`, `._*`) and directory entries are skipped silently.
- Absolute (`/css/app.css`) and relative (`./css/app.css`) asset paths both work.
- All sites send `X-Robots-Tag: noindex, nofollow`.

## Limits

| Limit | Free | Paid |
|---|---|---|
| Per file | 5 MB | 25 MB |
| Files per site | 50 | 1000 |
| Size per site | 250 MB | 1 GB |
| Total per account | 500 MB | effectively unlimited |
| Retention | 15 days since last publish | infinite |

Caps are enforced *during* the upload stream, so an over-limit publish fails fast. The paid tier (custom username / domain) is operator-enabled, not self-serve.
