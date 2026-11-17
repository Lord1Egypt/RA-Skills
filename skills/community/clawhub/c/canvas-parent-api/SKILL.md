---
name: canvas-parent-api
description: "Query Canvas LMS (Instructure) from a shell with curl and a bearer access token instead of running the canvas-parent-mcp server — courses, grades, assignments, submissions, calendar, planner, announcements, conversations, discussions, and files for yourself or a linked observee. Use when you want Canvas data without the MCP, in a script, or on a machine where the MCP isn't installed."
---

# Canvas LMS via curl (no MCP)

Canvas's REST API (`/api/v1/...`) is a normal per-institution API reachable
directly with `curl` — no browser bridge, no bot wall. Every request needs an
`Authorization: Bearer <token>` header; there is no anonymous access. The
host is **per-institution** (`https://<district>.instructure.com`, or a
self-hosted domain) — always read it from `$CANVAS_BASE_URL`, never hardcode
one tenant.

This is the same data the `canvas_*` MCP tools return, reached with plain
`curl` instead of a running server.

## One-time setup — get a bearer token

Pick whichever your institution allows (mirrors `canvas-parent-mcp`'s
`CANVAS_TOKEN` / OAuth modes — the session-cookie and fetchproxy modes need
the MCP or a browser and are out of scope here):

**A. Personal access token (simplest, if allowed)**

Canvas web UI → Account → Settings → **+ New Access Token**. Most
institutions disable this for non-admins, so try B if it's not offered.

```sh
export CANVAS_BASE_URL=https://<district>.instructure.com   # per-institution, no trailing slash
export CANVAS_TOKEN=<token from the UI>
```

**B. OAuth via the mobile QR-login flow**

In the Canvas mobile app: Account → **QR for Login** (or "Pair with
Observer/QR Login"), scan it with any camera to get the URL it encodes
(`https://sso.canvaslms.com/canvas/login?domain=...&code=...`). Exchange it
once for OAuth credentials with the helper this same repo ships (no MCP
server needs to be *running* — it's a one-off CLI).

It prints four `NAME=value` lines to stdout
(`CANVAS_BASE_URL`/`CANVAS_CLIENT_ID`/`CANVAS_CLIENT_SECRET`/`CANVAS_REFRESH_TOKEN`)
— **export them into the shell**, since the next `curl` reads them as env
vars and this step can't be skipped:

```sh
eval "$(npx canvas-parent-mcp-qr-login "<qr-url>" | sed 's/^/export /')"
```

Then mint (and later re-mint) a short-lived access token from the refresh
token with `curl` directly — no need to re-scan the QR each time:

```sh
curl -s -X POST "$CANVAS_BASE_URL/login/oauth2/token" \
  -d grant_type=refresh_token \
  -d client_id="$CANVAS_CLIENT_ID" \
  -d client_secret="$CANVAS_CLIENT_SECRET" \
  -d refresh_token="$CANVAS_REFRESH_TOKEN" \
  | jq -r '.access_token'
```

Export the result as `CANVAS_TOKEN` (access tokens expire in ~1h — re-run
this when calls start 401ing).

## Core call pattern

```sh
curl -s \
  -H "Authorization: Bearer $CANVAS_TOKEN" \
  -H "Accept: application/json+canvas-string-ids, application/json" \
  "$CANVAS_BASE_URL/api/v1/users/self/profile" \
  | sed 's/^while(1);//' | jq .
```

Two quirks every call needs:

- **`Accept: application/json+canvas-string-ids, application/json`** — without
  it, large numeric IDs can silently round-trip wrong (JS `2^53` overflow).
- **XSSI prefix** — some endpoints prepend `while(1);` to the JSON body.
  Strip it before piping to `jq` (`sed 's/^while(1);//'`), or it'll fail to
  parse.

## Resolve-first rule: get IDs before detail

Most detail/list-by-course endpoints need a `courseId` and (for parents) an
observee's user ID — get those first, then substitute them into the paths in
`references/canvas-endpoints.md`:

```sh
# Your own profile (sanity-check the token works)
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" -H "Accept: application/json+canvas-string-ids, application/json" \
  "$CANVAS_BASE_URL/api/v1/users/self/profile" | sed 's/^while(1);//' | jq '{id, name, primary_email}'

# Students linked to your observer account (empty array for a plain student token)
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" -H "Accept: application/json+canvas-string-ids, application/json" \
  "$CANVAS_BASE_URL/api/v1/users/self/observees?include[]=avatar_url" | sed 's/^while(1);//' | jq '.[] | {id, name}'

# Your (or an observee's) active courses, with grades
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" -H "Accept: application/json+canvas-string-ids, application/json" \
  "$CANVAS_BASE_URL/api/v1/users/self/courses?enrollment_state=active&state[]=available&include[]=total_scores&include[]=current_grading_period_scores&include[]=term" \
  | sed 's/^while(1);//' | jq '.[] | {id, name}'
```

For an observee, swap `users/self` for `users/<observeeId>` in any path that
starts that way (per-user endpoints); course-scoped endpoints
(`/api/v1/courses/<courseId>/...`) don't need the observee ID at all — Canvas
scopes them to whichever user the token belongs to.

## Pagination

Canvas paginates with an RFC 5988 `Link` header, not a body field. Fetch
headers separately to follow `rel="next"`:

```sh
url="$CANVAS_BASE_URL/api/v1/courses/123/students/submissions?student_ids[]=self&per_page=100"
while [ -n "$url" ]; do
  headers=$(curl -sD - -o page.json -H "Authorization: Bearer $CANVAS_TOKEN" \
    -H "Accept: application/json+canvas-string-ids, application/json" "$url")
  sed 's/^while(1);//' page.json | jq -c '.[]' >> all.jsonl
  url=$(echo "$headers" | grep -i '^link:' | grep -oE '<[^>]+>; rel="next"' | grep -oE 'https?://[^>]+')
done
```

Bumping `per_page` (Canvas allows up to 100) is usually enough for one-off
queries; only bother with the loop for genuinely large collections.

## Auth expiry

- **Personal token**: a 401 means it's expired or revoked — mint a fresh one
  in the Canvas UI (tokens don't self-refresh).
- **OAuth access token**: expires in ~1h — re-run the `refresh_token`
  exchange above; the refresh token itself is long-lived.

All 18 endpoints (courses, assignments, submissions, grades, calendar,
planner, announcements, conversations, discussions, files) are in
`references/canvas-endpoints.md` with the real query params and a `jq`
projection for each.
