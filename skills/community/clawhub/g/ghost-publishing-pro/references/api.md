# Ghost Admin API Reference

## Authentication

Ghost Admin API keys have the format `{id}:{secret}` (split on first `:`).

Tokens expire in 5 minutes. Regenerate before every API call.

**Generate token — pure Node.js (no npm required):**
```js
const crypto = require('crypto');
const key = 'id:secret';
const [id, secret] = key.split(':');
const header = Buffer.from(JSON.stringify({alg:'HS256',typ:'JWT',kid:id})).toString('base64url');
const now = Math.floor(Date.now()/1000);
const payload = Buffer.from(JSON.stringify({iat:now,exp:now+300,aud:'/admin/'})).toString('base64url');
const sig = crypto.createHmac('sha256',Buffer.from(secret,'hex')).update(header+'.'+payload).digest('base64url');
const token = header+'.'+payload+'.'+sig;
```

Run inline with credentials file:
```bash
node -e "
const crypto=require('crypto');
const creds=JSON.parse(require('fs').readFileSync(process.env.HOME+'/.openclaw/credentials/ghost-admin.json','utf8'));
const [id,secret]=creds.key.split(':');
const h=Buffer.from(JSON.stringify({alg:'HS256',typ:'JWT',kid:id})).toString('base64url');
const n=Math.floor(Date.now()/1000);
const p=Buffer.from(JSON.stringify({iat:n,exp:n+300,aud:'/admin/'})).toString('base64url');
const s=crypto.createHmac('sha256',Buffer.from(secret,'hex')).update(h+'.'+p).digest('base64url');
const token=h+'.'+p+'.'+s;
const url=creds.url;
process.stdout.write(token);
"
export GHOST_URL=$(node -e "const creds=JSON.parse(require('fs').readFileSync(process.env.HOME+'/.openclaw/credentials/ghost-admin.json','utf8')); process.stdout.write(creds.url);")
# TOKEN and GHOST_URL are now separate shell variables — never printed together
```

**Request header:** `Authorization: Ghost {token}`
**Base URL:** `https://{ghost-domain}/ghost/api/admin/`
**Version header:** `Accept-Version: v5.0`

---

## Posts

### Create post
`POST /posts/?source=html`

```json
{
  "posts": [{
    "title": "Post title",
    "html": "<p>Content</p>",
    "status": "draft",
    "slug": "custom-slug",
    "custom_excerpt": "Optional excerpt",
    "feature_image": "https://url-to-image.jpg",
    "tags": [{"name": "tag-name"}],
    "email_segment": "all"
  }]
}
```

**status:** `draft` | `published` | `scheduled`
**email_segment:** `all` | `free` | `paid` (only fires when status=published)

### Publish + send email (one call)
```json
{
  "posts": [{
    "title": "Title",
    "html": "<p>Body</p>",
    "status": "published",
    "email_segment": "all"
  }]
}
```

### Update post
`PUT /posts/{id}/?source=html`

Must include `updated_at` from current post (optimistic locking). Re-fetch post first if uncertain.

```json
{
  "posts": [{
    "html": "<p>Updated content</p>",
    "updated_at": "2026-03-16T18:00:00.000Z"
  }]
}
```

### Get post by ID
`GET /posts/{id}/`

### Get post by slug
`GET /posts/slug/{slug}/`

### List posts
`GET /posts/?limit=15&page=1&filter=status:draft&fields=id,title,slug,status,updated_at`

Filter options: `status:draft`, `status:published`, `tag:name`

### Delete post
`DELETE /posts/{id}/`

---

## Pages

Identical to posts — replace `/posts/` with `/pages/`.

---

## Images

### Upload image
`POST /images/upload/` (multipart/form-data)

```bash
curl -X POST "{url}/ghost/api/admin/images/upload/" \
  -H "Authorization: Ghost {token}" \
  -F "file=@/path/to/image.jpg" \
  -F "purpose=image"
```

Returns: `{ "images": [{ "url": "https://..." }] }`

purpose options: `image` | `profile_image` | `icon`

---

## Tags

`GET /tags/?limit=all` — list all tags
`POST /tags/` — create: `{ "tags": [{ "name": "tag" }] }`

---

## Members / Subscribers

`GET /members/?limit=1` — check `meta.pagination.total` for subscriber count
`GET /members/?limit=15&filter=subscribed:true` — list subscribers

---

## Site info
`GET /site/` — returns title, description, url, version

---

## Batch operations

Ghost API has no native batch endpoint. Loop with a delay:
```js
for (const post of posts) {
  await apiCall(post);
  await new Promise(r => setTimeout(r, 500)); // 500ms between calls
}
```

---

## Backdate a post on publish

Set `published_at` to any past date in the same PUT call:

```json
{
  "posts": [{
    "id": "post-id",
    "status": "published",
    "published_at": "2023-07-12T12:00:00.000Z",
    "updated_at": "{fresh-updated_at}"
  }]
}
```

This prevents the post from surfacing as "new" on the site. Always fetch a fresh `updated_at` immediately before the PUT.

---

## Set feature image from body image

```json
{ "feature_image": "https://your-site.ghost.io/content/images/2026/02/image.jpg" }
```

Include in the same PUT call as status/published_at. No separate upload step needed if the image already exists in Ghost's content store.

---

## Bulk draft audit

Fetch all drafts with HTML for content review:

```
GET /posts/?limit=all&filter=status:draft&fields=id,title,slug,published_at,created_at,updated_at,html
```

Note: `tags` is NOT a valid `fields` param — use `&include=tags` as a separate param if you need tag data.

---

## Content API (public — read-only)

For client-side JS (e.g., homepage search), use the public Content API instead of Admin JWT:

**Key location:** Embedded in your site's HTML source — look for `data-key=` in script tags.

```bash
curl "https://your-site.ghost.io/ghost/api/content/posts/?key=YOUR_KEY&limit=all&fields=title,slug,excerpt,feature_image"
```

Safe to use in browser JS — read-only, published posts only. No JWT needed.
Do NOT use the Admin key in client-side code.

---

## Permission walls — do not re-attempt via API

These operations require owner-level access (browser only):

| Operation | Why blocked | Workaround |
|-----------|------------|------------|
| `PUT /admin/settings/` (code injection) | Integration tokens read-only on settings | Browser + CM6 dispatch pattern |
| `GET /admin/integrations/` | Integration tokens cannot list integrations | Extract Content key from site HTML source |

---

## Code injection via browser (CM6 pattern)

> ⚠️ **OWNER-ONLY MANUAL STEP — do not run autonomously.**
> This replaces site-wide JavaScript visible to all visitors. Before executing:
> 1. Back up the existing code injection content.
> 2. Review the exact script to be inserted.
> 3. Execute manually — never let the agent run this without explicit owner approval.

Ghost's code injection panel uses CodeMirror 6. Standard DOM input manipulation doesn't work.

Navigate to: `https://your-site.ghost.io/ghost/#/settings/code-injection`
Click the "Code injection" list item in the left nav, then click "Site footer" tab.

```js
// Read current value
const view = document.querySelector('.cm-content').cmView.view;
const current = view.state.doc.toString();

// Replace entire content
view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: newContent } });

// Append to end
const len = view.state.doc.length;
view.dispatch({ changes: { from: len, insert: appendedContent } });
```

Then click the Save button.

---

## Homepage search bar pattern

For client-side search across all published posts — inject into Ghost Site footer:

```html
<script>
(function(){
  var KEY='your-content-api-key';
  var GHOST='https://your-site.ghost.io';
  // Lazy-load all posts on first input focus
  // Filter client-side on every keystroke
  // Place above .site-title using insertBefore
})();
</script>
```

Key points:
- Use Content API key (safe for client-side), not Admin key
- Do NOT use an external script tag pointing to a LAN/private hostname — browsers block it (mixed content + Private Network Access policy)
- All CSS/JS must be inline in the code injection block
- Placement: `title.parentNode.insertBefore(wrap, title)` inserts ABOVE the site title

---

## Error codes

- `401` — expired/invalid token (regenerate)
- `404` — resource not found
- `409` — `updated_at` mismatch on PUT (re-fetch and retry)
- `422` — validation error (check required fields, HTML validity)
- `429` — rate limited (add delays between calls)
- `403 NoPermissionError` on settings write — integration token limitation, use browser fallback
