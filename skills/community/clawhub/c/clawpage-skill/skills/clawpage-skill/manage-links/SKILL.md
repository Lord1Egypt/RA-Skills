---
name: manage-links
description: Create, list, update, or delete short links that map https://clawpage.ai/s/<slug> → a *.clawpage.ai URL. Use when the user wants to share a cleaner/shorter URL for their own Clawpage page (public page, preview with pagecode, home page, etc.). Target URLs are restricted to *.clawpage.ai only — external URLs are rejected.
---

# manage-links

Short links shorten any `*.clawpage.ai` URL to `https://clawpage.ai/s/<7-char slug>` (302 redirect).

- **Resolution** (public, anonymous): `GET https://clawpage.ai/s/<slug>`
- **Management** (owner token): `https://<username>.clawpage.ai/api/links/*`

## When to use

- User wants a cleaner URL to share a Clawpage page
- User wants to hide a `?pagecode=...` parameter behind a neutral short URL
- User has a generated page name (like `page-a1b2c3`) and wants something shorter

**Don't** use for:
- External URLs (YouTube, Twitter, etc.) — **target must be `*.clawpage.ai`** or creation fails 400
- Any scheme other than `https`

> **Management pages:** if rendering link data in a pagecode-protected management page, use `c.links` from the Clawpage JS SDK — see `${CLAUDE_SKILL_DIR}/use-sdk/SKILL.md`. Raw `fetch('/api/links/...')` in page JS is forbidden.

## CLI usage

Run from any directory containing `keys.local.json` with a valid `clawpage.token`.

### Create a short link
```bash
npx -y @clawpage.ai/cli links --create https://alice.clawpage.ai/p/some-long-name
# → prints JSON with { slug, shortUrl, target, createdAt, updatedAt }
```

### List my short links
```bash
npx -y @clawpage.ai/cli links --list
```

### Update a link's target
```bash
npx -y @clawpage.ai/cli links --update-slug aB3kFq9 --target https://alice.clawpage.ai/p/new-destination
```

### Delete
```bash
npx -y @clawpage.ai/cli links --delete aB3kFq9
```

## Quotas

- 100 short links per user
- Target URL length <= 2048 chars

## Error codes

| Code | HTTP | Action |
|---|---|---|
| `INVALID_TARGET_URL` | 400 | Make sure target is an `https://` URL on `clawpage.ai` (or a subdomain) |
| `SHORTLINK_NOT_FOUND` | 404 | Slug doesn't exist OR is not yours |
| `TOO_MANY_SHORTLINKS` | 413 | Delete unused ones via `--list` then `--delete` |
| `PERMISSION_DENIED` | 403 | Token's owner doesn't match the current host — fix `keys.local.json` |
| `UNAUTHORIZED` | 401 | Missing/invalid Bearer token |

## Integration with publish flow

Typical usage after publishing a page with a long name:

```bash
# publish
npx -y @clawpage.ai/cli publish --page-dir .pages/my-article

# shorten its URL
npx -y @clawpage.ai/cli links --create https://<user>.clawpage.ai/p/my-long-article-name-that-is-ugly
```
