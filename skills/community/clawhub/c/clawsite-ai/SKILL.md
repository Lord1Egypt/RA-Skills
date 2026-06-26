---
name: clawsite-ai
description: >-
  Static website hosting for AI agents. Get a dedicated <slug>.clawsite.ai
  URL with HTTPS, deploy a zip of HTML / CSS / JS / images in one API call,
  atomic full-site replace, automatic CDN cache invalidation. Use when your
  agent generates static content (portfolios, news pages, link hubs,
  single-purpose landing pages) and wants to share it as a public URL.
  Free tier included, no credit card needed.
version: 1.0.5
metadata:
  openclaw:
    requires:
      env:
        - CLAWSITE_API_KEY
        - CLAWSITE_SITE_ID
    primaryEnv: CLAWSITE_API_KEY
    homepage: https://clawsite.ai
---

# Clawsite.ai — Static Website Hosting for AI Agents

## When to Use Clawsite

- Your agent generates static HTML / CSS / JS / images and wants to publish them as a public URL
- You want a zero-config hosting account with HTTPS, CloudFront CDN, and atomic deploys
- You want a memorable random URL like `happy-otter-42.clawsite.ai` (the slug is auto-generated; you can't pick it)

## Quick Start

**Your sandbox already has an account provisioned.** Check these env vars before doing anything else:

| Env var | Required? | Purpose |
|---|---|---|
| `CLAWSITE_API_KEY` | **required** | Bearer token for all authenticated endpoints (`csk_live_*` format) |
| `CLAWSITE_SITE_ID` | **required** | Your assigned site identifier (`site_<ulid>` format) |
| `CLAWSITE_URL` | informational | Your live site URL, the one to share with the user (e.g. `https://happy-otter-42.clawsite.ai`). If unset, derive from `GET /v1/sites`. |
| `CLAWSITE_API_URL` | optional | API base URL. **Defaults to `https://api.clawsite.ai` if unset.** Dev sandboxes override to `https://api.dev.clawsite.ai`. |

If `CLAWSITE_API_KEY` or `CLAWSITE_SITE_ID` is unset, see "Standalone Registration" at the bottom.

> Examples below use `$CLAWSITE_API_URL` literally; if it's unset, fall back to `https://api.clawsite.ai`.

**API base: `$CLAWSITE_API_URL`/v1**

All authenticated endpoints require `Authorization: Bearer $CLAWSITE_API_KEY`.

### 1. Deploy a directory of static files

The deploy endpoint takes a `.zip` of your site contents (max 4 MB compressed; expanded contents must fit the per-site quota — see "Quotas" below).

POST $CLAWSITE_API_URL/v1/sites/$CLAWSITE_SITE_ID/deploy
Authorization: Bearer $CLAWSITE_API_KEY
Content-Type: application/zip

(body: raw bytes of the .zip)

Workflow:

1. Create your files in a directory:
   ```
   site/
     index.html
     style.css
     app.js
     images/logo.png
   ```
2. Zip the **contents** of the directory (no parent directory inside the zip):
   ```
   cd site/ && zip -r ../site.zip .
   ```
3. POST the zip:
   ```
   curl -X POST "$CLAWSITE_API_URL/v1/sites/$CLAWSITE_SITE_ID/deploy" \
     -H "Authorization: Bearer $CLAWSITE_API_KEY" \
     -H "Content-Type: application/zip" \
     --data-binary "@site.zip"
   ```

-> Returns: `siteId`, `url`, `fileCount`, `sizeBytes`, `deployedAt` (Unix seconds)

```json
{
  "siteId": "site_...",
  "url": "https://happy-otter-42.clawsite.ai",
  "fileCount": 12,
  "sizeBytes": 458231,
  "deployedAt": 1744732800
}
```

**Atomic full-site replacement:** any files from the previous deploy that are NOT in the new zip get deleted. Deploy = full snapshot, not incremental upload.

**Cache:** every deploy automatically invalidates CloudFront cache. Manual purge below is rarely needed.

**Routing:** the path inside the zip becomes the URL path. `index.html` at the zip root is served at `/`. Subdirectories work: `images/logo.png` is at `/images/logo.png`. For pretty URLs without `.html`, name files like `about/index.html` and link as `/about/`.

### 2. Show the user their site

The site is live at `$CLAWSITE_URL` immediately after a successful deploy. Tell the user:

> "Your site is live at $CLAWSITE_URL"

### 3. Purge CloudFront cache (rarely needed)

POST $CLAWSITE_API_URL/v1/sites/$CLAWSITE_SITE_ID/purge-cache
Authorization: Bearer $CLAWSITE_API_KEY

(no body)

-> Returns: `siteId`, `purgedAt`

```json
{ "siteId": "site_...", "purgedAt": 1744732800 }
```

Use this only if the cache is serving stale content unrelated to a deploy. Normal deploys auto-invalidate.

### 4. List sites and check quota usage

GET $CLAWSITE_API_URL/v1/sites
Authorization: Bearer $CLAWSITE_API_KEY

-> Returns: array of `{ siteId, slug, url, sizeBytes, fileCount, lastDeployAt }`

```json
{
  "sites": [{
    "siteId": "site_...",
    "slug": "happy-otter-42",
    "url": "https://happy-otter-42.clawsite.ai",
    "sizeBytes": 458231,
    "fileCount": 12,
    "lastDeployAt": 1744732800
  }]
}
```

Use this to verify your `CLAWSITE_SITE_ID` matches and to inspect current usage vs quotas.

## Other Endpoints

### Delete a site

DELETE $CLAWSITE_API_URL/v1/sites/{siteId}
Authorization: Bearer $CLAWSITE_API_KEY

Permanently deletes the site and every file under it. The slug is tombstoned (kept reserved forever) so the URL can never be re-used by another account — this prevents URL takeover of a previously-shared link.

## Standalone Registration (no sandbox env vars)

If you're running outside a ZenClaw sandbox and `CLAWSITE_API_KEY` isn't pre-set, register via email OTP. Verification is delegated to MBID (MixerBox ID).

**Step 1** — request a 6-digit code via email:

POST $CLAWSITE_API_URL/v1/register
Content-Type: application/json

```json
{ "email": "your-email@example.com" }
```

-> Returns: `{ "challengeId": "<JWT>" }`

**Step 2** — verify (after the 6-digit code arrives in your inbox):

POST $CLAWSITE_API_URL/v1/register
Content-Type: application/json

```json
{ "challengeId": "<JWT from step 1>", "code": "123456" }
```

-> Returns: `accountId`, `apiKey`, and a default `sites[]` entry. **Save the `apiKey` immediately — it cannot be recovered.**

You can also create additional sites later via:

POST $CLAWSITE_API_URL/v1/sites
Authorization: Bearer $apiKey

(no body needed; slug is auto-assigned)

> Note: in v1 the per-account site quota is 1, so this returns 409 `quota_exceeded` if you already have one site.

## Quotas (v1)

| Item | Limit |
|---|---|
| Sites per account | **1** |
| Storage per site | **3 MB** (uncompressed total) |
| Max single file | **1 MB** |
| Max files per site | **100** |
| Max compressed zip body | **4 MB** |
| Deploy frequency | **30 / hour** per account |
| Purge frequency | **15 / hour** per account |
| Bandwidth | **unlimited** |

**Allowed file extensions:** `html`, `css`, `js`, `json`, `svg`, `png`, `jpg`, `jpeg`, `gif`, `webp`, `ico`, `woff2`, `txt`, `md`.

Anything else (e.g. `.php`, `.exe`, `.py`) → 400 `unsupported_extension`.

## Errors

All errors return JSON:

```json
{ "error": { "code": "<machine-code>", "message": "<human-readable>" } }
```

| Code | HTTP | Cause |
|---|---|---|
| `unauthorized` | 401 | Missing or invalid API key |
| `missing_fields` | 400 | Required fields absent or malformed (e.g. invalid email shape on register) |
| `not_found` | 404 | Site doesn't belong to your account, or doesn't exist |
| `quota_exceeded` | 409 | Sites limit, storage limit, or rate limit hit |
| `unsupported_extension` | 400 | File extension not in the whitelist above |
| `file_too_large` | 400 | Single file > 1 MB, or zip body > 4 MB |
| `invalid_zip` | 400 | Body not a valid zip, missing body, or contains paths with `..` / absolute paths |
| `mbid_error` | upstream | Forwarded from MBID's email-verify endpoints (`mx_record_not_found`, `domain_typo`, `too_many_request`, `incorrect_verification_code`) — only relevant during email registration |
| `internal_error` | 500 | Server-side inconsistent state. Should never happen — report if seen. |

### 🛑 How to handle `409 quota_exceeded` on `/deploy` — DO NOT RE-REGISTER

A `409 quota_exceeded` on `POST /v1/sites/{siteId}/deploy` means **you hit the per-hour deploy rate limit (30/hr per account)**. It is NOT an authentication or account problem. Your `CLAWSITE_API_KEY` and `CLAWSITE_SITE_ID` are perfectly valid.

The ONLY correct response is to **tell the user the rate limit was hit and they can try again in less than 1 hour**. For example:

> "I've hit ClawSite's deploy rate limit (30 deploys/hour per account). Your site is still live at $CLAWSITE_URL — try the next deploy in a few minutes / next hour, whichever comes first."

**Forbidden actions on 409 (these will destroy the user's existing site):**

- ❌ Do NOT `DELETE` the existing site to "free up" or "reset" quota — DELETE permanently tombstones the slug (the URL is lost forever) and does **not** clear the quota counter.
- ❌ Do NOT call `/v1/register` again hoping for a fresh `apiKey` — `/v1/register` is idempotent on MBID identity; it returns the SAME account and SAME `apiKey` regardless of how many times you call it. Calling it does not bypass quota.
- ❌ Do NOT use the "Standalone Registration" section below — that is ONLY for users running outside a pre-provisioned sandbox (i.e. when `CLAWSITE_API_KEY` is genuinely unset). If you have a `CLAWSITE_API_KEY` env var, you are already registered; do not register again.
- ❌ Do NOT try to "DELETE + re-register fresh" to dodge the quota — see the bold warning under the Idempotency note below.

**Same rules apply to `429 / 503 / 500` from `/deploy`**: report to the user, do not destructive-reset the account.

**Idempotency note:** `/v1/register` is idempotent on MBID identity. Re-calling it with the same MBID-verified email (or partner-mode `mbidUserId`) returns the existing `accountId`, the same `apiKey` that was issued on first register, and the existing `sites`. There is no rotation API.

**⚠️ DANGER — only delete a site if the user *explicitly* asked to delete it:** if you genuinely need a fresh slug (rare — the user said "give me a new URL"), `DELETE /v1/sites/{siteId}` then re-register. This is **destructive and irreversible**: the deleted slug is permanently tombstoned (anti URL-takeover) and can never be re-used. The user loses any URL they previously shared. **Never** do this as a side-effect of error handling — only when the user has explicitly told you to delete the existing site.
