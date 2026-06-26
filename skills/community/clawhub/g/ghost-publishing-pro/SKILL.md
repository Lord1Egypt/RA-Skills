---
name: ghost-publishing-pro
version: 2.4.0
description: "Headless Ghost publishing. Write, audit, and automate your entire Ghost operation from your AI workflow — 17 workflows covering article publishing, batch imports, site health audits, email performance, bulk excerpt push, and GSC indexing repair. Admin API only. No browser, no dashboard, no context switching."
homepage: https://github.com/highnoonoffice/hno-skills
source: https://github.com/highnoonoffice/hno-skills/tree/main/ghost-publishing-pro
credentials:
  - name: ghost-admin.json
    description: "JSON file at ~/.openclaw/credentials/ghost-admin.json with two fields: url (your Ghost site URL) and key (Admin API key in id:secret format — Ghost Admin > Settings > Integrations > Add custom integration)"
    required: true
binaries:
  - node
  - curl
  - python3
license: MIT
metadata: ~
---

# Ghost Publishing Pro

## Execution Gates

```xml
<skill_gates version="1.0" mode="mandatory_pre_execution" evaluation="sequential" on_violation="stop_and_report">

  <gate id="credentials_check" priority="1" severity="hard" scope="session_start">
    <condition>About to make any Ghost API call</condition>
    <question>Have I confirmed ~/.openclaw/credentials/ghost-admin.json exists and contains both `url` and `key` fields?</question>
    <pass_action>Proceed.</pass_action>
    <fail_action>Stop. Read the credentials file first. If missing, run Credentials Setup. Do not attempt any API call without confirmed credentials.</fail_action>
  </gate>

  <gate id="fetch_before_put" priority="2" severity="hard" scope="pre_update">
    <condition>About to PUT (update) any post</condition>
    <question>Have I fetched the current post this session and captured its `updated_at` value?</question>
    <pass_action>Proceed with PUT including `updated_at`.</pass_action>
    <fail_action>Stop. Fetch the post first. A PUT without `updated_at` returns 409. No exceptions.</fail_action>
  </gate>

  <gate id="publish_email_atomic" priority="3" severity="hard" scope="pre_publish">
    <condition>About to publish a post that should go to subscribers</condition>
    <question>Is `email_segment` included in the same API call as `"status": "published"`?</question>
    <pass_action>Proceed.</pass_action>
    <fail_action>Stop. Add `email_segment` to this call. Email cannot be triggered after the fact via API — only Ghost Admin manual resend. This is a one-shot gate.</fail_action>
  </gate>

  <gate id="bulk_write_approval" priority="4" severity="hard" scope="pre_bulk">
    <condition>About to run any bulk operation (batch update, batch tag, batch excerpt, migration import)</condition>
    <question>Has the user explicitly approved this bulk operation — scope, post count, and what will change?</question>
    <pass_action>Proceed.</pass_action>
    <fail_action>Stop. State the scope (how many posts, what changes), and wait for explicit approval. Bulk writes are irreversible without manual rollback.</fail_action>
  </gate>

  <gate id="settings_wall" priority="5" severity="soft" scope="pre_settings">
    <condition>About to write to Ghost site settings, code injection, redirects, or staff</condition>
    <question>Does the task require owner-level access that integration tokens cannot provide?</question>
    <pass_action>Stop. This operation is a Ghost platform limitation — outside the scope of this skill. Flag it to the user: this endpoint returns 403 for integration tokens by design and cannot be automated via the Admin API.</pass_action>
    <fail_action>Do not attempt. Do not suggest browser fallback. State the platform limitation clearly and stop.</fail_action>
  </gate>

  <gate id="image_upload_method" priority="6" severity="soft" scope="pre_image">
    <condition>About to upload an image to Ghost via the /images/upload/ endpoint</condition>
    <question>Am I using Python requests with multipart/form-data for this specific upload call?</question>
    <pass_action>Proceed. All other API calls (posts, tags, analytics) use curl or Node.js as normal.</pass_action>
    <fail_action>Switch to Python requests for the image upload only. curl multipart fails silently on macOS zsh for this endpoint. Browser fetch is blocked by CORS. Everything else in this skill uses curl or Node.js — this exception applies to image upload only.</fail_action>
  </gate>

</skill_gates>
```

---

### Before You Install

This skill has three hard requirements:

- **Node.js** installed locally (`node --version` to verify)
- **curl** installed (`curl --version` to verify — standard on macOS/Linux)
- **Ghost Admin API key** stored at `~/.openclaw/credentials/ghost-admin.json`

If those three aren't ready, start with the **Credentials Setup** section below. Everything else in this skill assumes they're in place.

---

### Start Here

**Most users want two things:** publish a post and send it to subscribers in one call, and update existing posts without breaking them. Start with **Core Operations** below — that covers 90% of day-to-day use.

**Also here if you need it:** batch imports, site health audits, email analytics, excerpt management, GSC indexing repair, and full Squarespace/WordPress/Substack migrations. All 17 workflows are in `references/workflows.md`.

If you're new: do **Credentials Setup**, then go straight to **Core Operations**. Skip everything else until you need it.

---

A full Ghost CMS publishing skill built from real production use — not a generic API wrapper.

This contains proven workflows, hard-won pitfalls, and patterns from actually running a Ghost Pro newsletter and migrating an entire Squarespace blog in an afternoon.

### Dependencies

Most workflows use only Node.js built-ins (`fs`, `https`, and the standard HMAC module) and `curl` — no npm packages required.

The **Squarespace/WordPress XML migration** workflow optionally uses one npm package:

```bash
npm install fast-xml-parser@5.7.2
```

Install this only if you are running a migration script. All other workflows (publish, update, schedule, image upload, analytics) require no third-party packages.

### Required Access

This skill uses Ghost's Admin API. Here's exactly what it does with your credentials:

**Reads:** Post list, member count, analytics, post content, image URLs.

**Writes:** Creates and updates posts, uploads images, schedules content, sends newsletters.

**Recommended setup:** Create a dedicated integration key (Settings > Integrations > Add custom integration > Admin API Key). This covers the full publishing workflow with minimal scope.

The skill never stores credentials beyond the file you configure. Tokens are captured to shell variables and never logged or printed to stdout. No external calls outside your Ghost instance.

### Security Model

This skill is designed around minimal-scope credential use. Here's exactly how credential access is scoped and why it's safe:

**Use a dedicated integration key, not your owner credentials.** Ghost Admin → Settings → Integrations → Add custom integration → copy the Admin API Key. This key is isolated to the integration, fully revocable, and scoped to post/image/member operations — your owner account is never exposed.

**The credentials file is read-only at runtime.** The skill reads `~/.openclaw/credentials/ghost-admin.json` to generate a short-lived JWT (5-minute expiry). Nothing is written back to the file. Tokens are captured to shell variables, never logged or persisted.

**No external calls outside your Ghost instance.** Every API call targets your Ghost domain only. No third-party services, no telemetry, no data leaves your site.

**Revocation is instant.** If you need to cut access, delete the integration in Ghost Admin → Settings → Integrations. All tokens derived from that key immediately stop working.

Keep the credentials file out of shared folders and version control. Restrict access to your user account only using your OS file permission settings.

### Ghost Platform Limitations (Out of Scope)

These operations return `403` for integration tokens — they are Ghost platform restrictions, not skill gaps. This skill does not cover them and does not provide browser workarounds:

- **Staff management** — owner-only, no API path
- **Site settings / code injection** — `403 NoPermissionError` by design
- **Redirects and routes files** — `POST /ghost/api/admin/redirects/` returns `403` with integration tokens

Theme management (upload + activation) is fully supported via the Admin API — see Workflow 15 below.

If you hit a `NoPermissionError` on settings write endpoints, that is expected Ghost behavior — not a bug in this skill.

### Credentials Setup

Create a credentials file at `~/.openclaw/credentials/ghost-admin.json`:

```json
{
  "url": "https://your-site.ghost.io",
  "key": "id:secret"
}
```

Stored at: `~/.openclaw/credentials/ghost-admin.json` (fields: `url`, `key`)

Get your key: Ghost Admin > Settings > Integrations > Add custom integration > Admin API Key.

Covers: all post operations, image uploads, scheduling, newsletters, analytics, batch updates.

### Authentication

Ghost uses short-lived JWT tokens. Generate one before every API call — they expire in 5 minutes.

**Pure Node.js — no npm required.**

Token generation uses Node.js built-ins (`fs` and the standard HMAC module) and the Admin API key format (`id:secret`). The full implementation is in `references/api.md` under Authentication — copy the token generation script into your workflow, capture the output to a shell variable, and pass it as `Authorization: Ghost {token}` on all requests.

Tokens expire in 5 minutes. Regenerate before each API call or every 50 posts in batch operations.

### Core Operations

**Publish a post + send as newsletter (one call)**

```bash
curl -s -X POST "{url}/ghost/api/admin/posts/?source=html" \
  -H "Authorization: Ghost {token}" \
  -H "Content-Type: application/json" \
  -d '{"posts":[{
    "title": "Your Title",
    "html": "<p>Your content</p>",
    "status": "published",
    "email_segment": "all"
  }]}'
```

This is the killer feature — one API call publishes to the web and sends to all subscribers simultaneously. Do not publish first and try to send separately. If you miss the `email_segment` field on first publish, the newsletter cannot be resent via API — it is a one-shot operation.

**Create a draft**

Same as above with `"status": "draft"`. No email sent.

**Update an existing post**

```bash
# 1. Fetch post to get updated_at (required)
curl -s "{url}/ghost/api/admin/posts/{id}/" -H "Authorization: Ghost {token}"

# 2. Update with updated_at included
curl -s -X PUT "{url}/ghost/api/admin/posts/{id}/?source=html" \
  -H "Authorization: Ghost {token}" \
  -H "Content-Type: application/json" \
  -d '{"posts":[{"html":"<p>New content</p>","updated_at":"{fetched_updated_at}"}]}'
```

**List posts**

```bash
curl -s "{url}/ghost/api/admin/posts/?limit=15&filter=status:draft&fields=id,title,slug,status,updated_at" \
  -H "Authorization: Ghost {token}"
```

**Upload image**

```bash
curl -s -X POST "{url}/ghost/api/admin/images/upload/" \
  -H "Authorization: Ghost {token}" \
  -F "file=@/path/to/image.jpg" \
  -F "purpose=image"
# Returns URL — use as feature_image value
```

**Schedule a post**

Add `"status": "scheduled"` and `"published_at": "2026-03-20T18:00:00.000Z"` (UTC).

### HTML Content

Always use `?source=html` in the request URL. Ghost accepts raw HTML in the `html` field.

**Standard article:** `<p>`, `<h2>`, `<h3>`, `<hr>`, `<blockquote>`, `<ul>`, `<ol>`

**Book-style literary typography** — ideal for fiction, essays, and long-form literary content:

```html
<div style="font-family: Georgia, serif; text-align: justify; hyphens: auto; -webkit-hyphens: auto;" lang="en">
  <p style="text-indent: 2em; margin-bottom: 0; margin-top: 0;">Paragraph one.</p>
  <p style="text-indent: 2em; margin-bottom: 0; margin-top: 0;">Paragraph two — no gap, indent only.</p>
</div>
```

**YouTube embed:**

```html
<figure class="kg-card kg-embed-card">
  <iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/{VIDEO_ID}"
    frameborder="0" allowfullscreen></iframe>
</figure>
```

**Email rules — critical:**

- JS is stripped in email delivery. No scripts or interactive elements.
- Subscribe widgets are web-only — stripped from email.
- Ghost wraps content in its own email template. Don't add headers or footers.
- The `email_segment` field only fires on first publish. It must be in the same API call as `"status": "published"`.

### Migration Workflows

See `references/workflows.md` for full migration playbooks:

- Squarespace XML export > Ghost batch import (proven — full blog migrated in one afternoon)
- WordPress XML migration
- Substack CSV + HTML migration
- Batch feature image updates
- DOCX > book-style Ghost posts with YouTube embeds
- Native audio card embedding (upload MP3, embed as Ghost audio card)
- Theme management (JWT upload via Admin API)
- **Site audit** — scan all published posts for missing feature images, excerpts, meta descriptions, tags, stale slugs, and untouched content (Workflow 14)
- **Content performance intelligence** — three-section report: email performance (open rate, click rate, CTO, divergence analysis), web-only post health + amplification candidates, pages health snapshot. Audience snapshot with subscriber tier breakdown. (Workflow 15)
- **Batch excerpt push** — write custom excerpts to all posts in a single run. 300-char hard cap, slug-based targeting, skip/fail reporting. Proven on 65 posts in production. (Workflow 16)
- **GSC → Ghost indexing & SEO repair loop** — triage GSC coverage report, classify unindexed URLs, submit real posts for indexing, accelerate discovery with internal links. Note: redirect rule writes are blocked by Ghost's API for integration tokens — redirect management is outside this skill's scope. (Workflow 17)

See `references/api.md` for complete endpoint documentation, error codes, and token generation details.

### Common Pitfalls

- `409 on PUT` — must include `updated_at` from a fresh fetch
- Email not sending — `email_segment` only fires on first publish; use Ghost admin to resend
- Rate limiting — add 500ms delay between calls in batch scripts
- Token expired mid-batch — regenerate every 50 posts in long operations
- `tags` in `fields` param causes `400 BadRequestError` — use `&include=tags` instead
- External script tag in code injection pointing to a local/LAN hostname will silently fail on the live HTTPS site — mixed content + Private Network Access policy blocks it. All search/widget JS must be inline in the code injection block.
- `PUT /admin/settings/` always returns `403` with integration tokens — site settings are outside this skill's scope
- `GET /admin/integrations/` also returns `403` — get Content API key from site HTML source instead (`data-key=` attribute on portal/search script tags)
- **Custom theme: `{{content}}` must be triple-braced** — in any custom `.hbs` template, always use `{{{content}}}` (three braces). Double-braced `{{content}}` escapes the HTML and renders `undefined` instead of the post body.
- **Custom excerpts drive search** — Ghost's Content API `fields=excerpt` returns the custom excerpt, not body text. If a post needs to surface in client-side search for a keyword, that keyword must appear in the custom excerpt.
- **Links inside HTML cards in Lexical are double-escaped** — regex on `"url":"..."` fields won't find them. Use `json.dumps(lexical)` → string replace → `json.loads()` to safely find and replace any URL pattern inside embedded HTML.
- **Ghost's sitemap is always clean** — Ghost Pro auto-generates sitemaps using the configured site URL. No manual sitemap editing needed.
- **Squarespace migration leaves /blog/ links** — batch imports preserve old internal link paths with the `/blog/` prefix. After any Squarespace import, audit all posts for `/blog/` references and fix them via the API.
- **`POST /admin/redirects/upload/` returns `403`** — redirect management is blocked for integration tokens by Ghost's platform design. Outside the scope of this skill.


### Tag Management

Ghost's Admin API supports full tag CRUD. These endpoints require an **Admin-level token** (owner or staff with Admin role). Integration tokens return `403` — if that happens, see the safe-mode note below.

**List all tags**

```python
r = requests.get(
    f'{GHOST_URL}/ghost/api/admin/tags/?limit=all',
    headers=headers
)
tags = r.json().get('tags', [])
for tag in tags:
    print(tag['id'], tag['name'], tag['slug'])
```

**Create a tag**

```python
r = requests.post(
    f'{GHOST_URL}/ghost/api/admin/tags/',
    headers=headers,
    json={"tags": [{"name": "Your Tag", "slug": "your-tag"}]}
)
if r.status_code == 403:
    print("Safe-mode: Admin token requires owner-level permissions for tag endpoints. Add tags manually in Ghost Admin or use an owner token.")
else:
    tag = r.json()['tags'][0]
    print(tag['id'], tag['name'])
```

**Update a tag**

```python
# Fetch tag id first via list, then:
r = requests.put(
    f'{GHOST_URL}/ghost/api/admin/tags/{TAG_ID}/',
    headers=headers,
    json={"tags": [{"id": TAG_ID, "name": "Updated Name", "slug": "updated-slug"}]}
)
if r.status_code == 403:
    print("Safe-mode: owner-level token required for tag updates.")
```

**Delete a tag**

```python
r = requests.delete(
    f'{GHOST_URL}/ghost/api/admin/tags/{TAG_ID}/',
    headers=headers
)
if r.status_code == 403:
    print("Safe-mode: owner-level token required for tag deletion.")
elif r.status_code == 204:
    print("Tag deleted.")
```

**Bulk assign a tag to multiple posts**

```python
# Fetch posts, then PATCH each with the tag added
posts = requests.get(
    f'{GHOST_URL}/ghost/api/admin/posts/?limit=all&include=tags',
    headers=headers
).json()['posts']

for post in posts:
    existing_tags = [{"id": t["id"]} for t in post.get("tags", [])]
    if not any(t["id"] == TAG_ID for t in existing_tags):
        existing_tags.append({"id": TAG_ID})
        requests.put(
            f'{GHOST_URL}/ghost/api/admin/posts/{post["id"]}/',
            headers=headers,
            json={"posts": [{"id": post["id"], "updated_at": post["updated_at"], "tags": existing_tags}]}
        )
        print(f"Tagged: {post['title']}")
```

> **Safe-mode note:** All tag write endpoints (`POST`, `PUT`, `DELETE`) require owner-level Admin API credentials. If you get a `403`, either switch to an owner token or manage tags manually in Ghost Admin → Settings → Tags. The list endpoint (`GET`) works with standard integration tokens.

### License

MIT. Copyright (c) 2026 @highnoonoffice. Retain this notice in any distributed version.
