---
name: agenthost
version: 0.1.0
description: >-
  Publishes a static site or a folder of Markdown docs to a hosted URL and returns a private, pre-authenticated share link. Use when the user wants to publish a site/html/markdowns or share with someone else.
metadata:
  homepage: https://agenthost.page
  hermes:
    category: publishing
    tags: [hosting, static-site, publish, share, docs, cloudflare]
  openclaw:
    emoji: "🚀"
    requires:
      bins: [tar, curl]
---

Publish static files or Markdown, get back a **private, pre-authenticated share link** for a human. No signup, no key to start. `id` becomes the subdomain: `{username}-{id}.agenthost.page`.

## Publish

**Single file** — pipe a `.md` or `.html` in with its `Content-Type`. Markdown renders, HTML is served as-is; the file lands at `/`.

```bash
curl -s --data-binary @report.md \
  -H 'Content-Type: text/markdown' \
  'https://agenthost.page/publish?id=report'
```

**Folder** — pipe a gzipped tar of the directory.

```bash
tar czf - -C ./dist . | curl -s --data-binary @- \
  -H 'Content-Type: application/gzip' \
  'https://agenthost.page/publish?id=myblog'
```

The JSON response has two fields that matter:

- **`shareUrl`** — hand THIS to the human. Opening it logs the visitor in via a cookie on first load.
- **`ownerToken`** — save it. Shown **once**; the only way to redeploy to the same URL.

Both absolute (`/css/app.css`) and relative (`./css/app.css`) asset paths
resolve, since each site is its own subdomain root.

## Redeploy the same URL

Reuse the `ownerToken` and `username` from the first publish:

```bash
tar czf - -C ./dist . | curl -s --data-binary @- \
  -H 'Content-Type: application/gzip' \
  -H 'Authorization: Bearer <ownerToken>' \
  'https://agenthost.page/publish?id=myblog&username=<username>'
```

## Notes

- **Markdown docs**: a folder of `.md` renders GitBook-style (sidebar + `README.md` home). Add `SUMMARY.md` for ordering. GFM and ` ```mermaid ` render; mixed `.html`+`.md` works.
- **Limits (free tier)**: 50 files · 5 MB/file · 250 MB/site · 500 MB/account. Sites carry `noindex` and are deleted 15 days after their last publish.
- Making a site public, key rotation, recovery email, full field list, and error codes: [references/http-api.md](references/http-api.md).
