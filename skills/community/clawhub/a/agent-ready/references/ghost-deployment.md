# Ghost Deployment Reference

Complete Ghost Pro API and browser-session patterns for this skill. Read this before
executing any of the checklist items in `SKILL.md` that touch Ghost — the split between
what a token can do and what needs a browser session is the source of most avoidable
failures here.

## Authentication: two separate scopes

Ghost Pro exposes two completely different authentication paths, and they are not
interchangeable:

**Integration token scope (Admin API):**
- Works for: posts, pages, images, members, tags.
- Does not work for: code injection, site settings, redirects. These endpoints return
  `403` for a token even when the token is valid and has admin-level permissions in the
  Ghost UI — the 403 is a scope limitation, not a permissions error, and increasing the
  integration's stated permissions in the dashboard does not fix it.
- Token format: an Admin API key (`{id}:{secret}`), used to sign a short-lived JWT per
  request. Never hardcode a decoded token or secret into a committed file.

**Browser session scope:**
- Required for: code injection (head/footer), site settings, the redirects UI.
- Achieved by an authenticated login session against the Ghost Admin UI itself — there
  is no API equivalent for these surfaces on Ghost Pro.

Before starting any checklist item, confirm which scope it needs (`SKILL.md`'s Ghost
Pro Constraints section maps each item) so credential setup isn't discovered mid-task.

## Page creation

Endpoint: `POST /ghost/api/admin/pages/?source=html`

- Send the page body in the `html` field of the request payload; `source=html` tells
  Ghost to accept raw HTML rather than its internal mobiledoc/lexical format.
- Required fields: `title`, `html`. `slug` is optional — if omitted, Ghost derives it
  from the title; set it explicitly when the target path matters (e.g., the `llms.txt`
  page, where the slug must be exactly `llms.txt`).
- Set `status: "published"` explicitly — pages default to draft otherwise and won't be
  reachable at their public URL.
- This endpoint is reachable with an integration token — no browser session needed.
  This is why checklist item 1 (trust anchor pages) and the Option A path for item 3
  (`llms.txt` as a Ghost page) are achievable purely through the API.

## Code injection (browser session pattern)

Code injection has no dedicated Admin API endpoint on Ghost Pro — it is part of the
general settings surface, which requires an authenticated browser session:

1. Authenticate via the browser login flow (below) to establish a valid session.
2. Navigate to the site's Code Injection settings screen in the Ghost Admin UI.
3. **Fetch and read the current header/footer content first** — this is Gate 3 in
   `SKILL.md`, not optional. Code injection is a single free-text field per
   location (header/footer); writing to it without reading first risks silently
   deleting whatever else lives there (analytics snippets, other schema blocks, etc).
4. Construct the new content as the existing content plus the new script block
   appended — never a replacement.
5. Submit the settings update through the same session.
6. Verify via `curl -s https://yourdomain.com | grep -o 'application/ld+json'` (or the
   equivalent check for whatever was injected) once the change is live — see Gate 4.
   Expect a short propagation delay; see the CDN caching note below before concluding a
   verification failure means the write failed.

## Redirect rules

Ghost Pro's redirect rules live in the Admin UI (Settings → Redirects on most Ghost Pro
dashboards), not behind a documented public API endpoint. Same browser-session
requirement as code injection applies.

- Redirects are defined as `from` / `to` path pairs, with an option for permanent
  (301) vs temporary (302).
- Relevant to checklist item 3, Option B: if `llms.txt` content needs to live in a git
  repo rather than as a Ghost page, a redirect rule pointing `/llms.txt` at the raw
  file URL is how that gets wired up — set it as a permanent redirect.
- Changes here take effect quickly but should still be verified directly (Gate 4)
  rather than assumed from the UI showing "saved."

## Browser login flow, step by step

Ghost Pro does not use a password for this flow:

1. Navigate to the Ghost Admin login screen for the target site
   (`https://yourdomain.com/ghost/`).
2. Submit the email address for the dedicated staff account (see `SKILL.md`'s Ghost
   Pro Constraints — use a staff account, not the owner's own login).
3. Ghost sends a 6-digit numeric code to that inbox. There is no password step; the
   code itself authenticates the session.
4. Enter the 6-digit code on the verify screen that follows.
5. On success, an authenticated session is established for that browser context — this
   session is what code injection and settings writes ride on for the rest of the
   task.
6. Sessions expire; if a settings write starts returning an auth/redirect-to-login
   response mid-task, re-run this flow rather than assuming the earlier session is
   still valid.

## Common errors

- **`409` on PUT to posts/pages, "updated_at" missing or stale.** Ghost's PUT endpoints
  are optimistic-locked on `updated_at`. Always `GET` the resource immediately before a
  `PUT` to get its current `updated_at`, and include that exact value in the PUT body.
  A `409` here almost always means this step was skipped, not that something else is
  wrong with the request.
- **`403` on settings/code-injection endpoints with a valid integration token.** This
  is expected, not a bug — these surfaces are browser-session-only on Ghost Pro (see
  Authentication above). The fix is switching to the browser-session flow, not
  regenerating or re-scoping the token.
- **A write returns success but the live site doesn't reflect it yet.** Ghost Pro sits
  behind CDN caching, and there can be a short delay between a successful write and
  the public-facing response reflecting it. Before concluding a verification step
  (Gate 4) has failed, retry the check after a short wait rather than immediately
  treating a stale response as a broken write.
