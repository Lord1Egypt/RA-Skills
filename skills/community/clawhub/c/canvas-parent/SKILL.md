---
name: canvas-parent
description: This skill should be used when the user asks about Canvas LMS data — their own student account or any observed student. Triggers on phrases like "check Canvas", "what's my grade", "Canvas inbox", "what's due", "missing assignments", "Canvas LMS", "Instructure", "course announcements", "syllabus", or any request about courses, assignments, grades, conversations, announcements, planner items, or files in Canvas.
---

# canvas-parent-mcp

MCP server for Canvas LMS (Instructure) — read courses, grades, assignments, announcements, planner items, and conversations; download course files. Mirrors the parent/observer scope of the sibling `infinitecampus-mcp`.

- **npm:** [npmjs.com/package/canvas-parent-mcp](https://www.npmjs.com/package/canvas-parent-mcp)
- **Source:** [github.com/chrischall/canvas-parent-mcp](https://github.com/chrischall/canvas-parent-mcp)

## Setup

### Option A — npx (recommended)

Add to `.mcp.json` in your project or `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "canvas": {
      "command": "npx",
      "args": ["-y", "canvas-parent-mcp"],
      "env": {
        "CANVAS_BASE_URL": "https://cms.instructure.com"
      }
    }
  }
}
```

With the [ContextMint Bridge](https://github.com/nullnet-app/contextmint-bridge/releases) browser extension installed and a signed-in Canvas tab, that's enough — the MCP reads your session cookies from the browser on the first request and again whenever the session expires, so keep the extension installed and the browser running. Add `CANVAS_TOKEN`, `CANVAS_CLIENT_*`/`CANVAS_REFRESH_TOKEN`, or `CANVAS_USERNAME`/`CANVAS_PASSWORD` to the `env` block if you'd rather use one of those modes.

### Option B — from source

```bash
git clone https://github.com/chrischall/canvas-parent-mcp
cd canvas-parent-mcp
npm install && npm run build
```

## Authentication

**fetchproxy fallback (recommended, zero-config).** Set only `CANVAS_BASE_URL`. Install the [ContextMint Bridge](https://github.com/nullnet-app/contextmint-bridge/releases) browser extension, sign into your Canvas instance once. The MCP reads `canvas_session` + `pseudonym_credentials` cookies from your tab on the first request and re-reads them on every 401; API calls go directly from Node in between, but the extension must stay reachable to renew the session. Works with any auth flow (SSO/SAML/2FA included). It's the fetchproxy extension under its new name, same maintainer ([fetchproxy's README](https://github.com/chrischall/fetchproxy#extension) points to it); verify a release zip with `shasum -a 256 -c <zip>.sha256` or build it from [source](https://github.com/nullnet-app/contextmint-bridge).

### Alternatives (env-var)

- **Personal access token** — set `CANVAS_TOKEN`. Most institutions have disabled this for non-admins.
- **OAuth** — set `CANVAS_CLIENT_ID`, `CANVAS_CLIENT_SECRET`, `CANVAS_REFRESH_TOKEN`. Bootstrap via `canvas-parent-mcp-qr-login`.
- **Username/password (session-scrape)** — set `CANVAS_USERNAME` + `CANVAS_PASSWORD`. Direct Canvas accounts only (no SSO/2FA). Brittle.

Precedence when multiple are set: `CANVAS_TOKEN` > username/password > OAuth > fetchproxy. Set `CANVAS_DISABLE_FETCHPROXY=1` to opt out of the fallback.

## Tools (prefix `canvas_`)

### Profile & observees
- `canvas_get_profile` — your Canvas profile
- `canvas_healthcheck` — which auth path resolved and whether Canvas accepts it; registered even when auth is unconfigured, so it can say why
- `canvas_list_observees` — students linked to your observer account

### Courses
- `canvas_list_courses` — your active courses with grades
- `canvas_get_course(courseId, view?)` — course detail with syllabus + teachers

### Assignments & submissions
- `canvas_list_assignments(courseId)` — assignments in a course
- `canvas_list_missing_submissions` — past-due unsubmitted work
- `canvas_get_submission(courseId, assignmentId, view?)` — your submission with comments + rubric
- `canvas_list_recent_submissions(courseId, view?)` — recently graded submissions (default 14d)

### Grades
- `canvas_list_enrollments` — per-course grades

### Calendar & planner
- `canvas_list_calendar_events` — calendar events / assignments
- `canvas_list_upcoming_events` — server-curated next 7 days
- `canvas_list_planner_items(observeeId?, view?)` — unified to-do feed; `view: "brief"` gives one line per item, `title — <ISO date|no date> — <status>`, inside the untrusted-data envelope (`data: ["-- none"]` when empty)

### Communication
- `canvas_list_announcements(contextCodes, view?)` — course announcements
- `canvas_list_conversations` — inbox
- `canvas_get_conversation(id, view?)` — full conversation thread
- `canvas_list_discussion_topics(courseId, view?)` — course discussion topics

### Files
- `canvas_list_course_files(courseId)` — file metadata
- `canvas_download_file(url, destinationPath?)` — download a file. `url` must be a `/files/` URL on the configured Canvas host. Local install: written to disk; `destinationPath` must be inside `CANVAS_OUTPUT_DIR` (default `~/Downloads`, a relative path is resolved against it), or omit it to save under the file's own name. Hosted: returns a signed, expiring `url` (give it to the user) or, for a small image, the image inline; `destinationPath` is ignored

## Response shape (`view`)

Nine tools take `view: "compact" | "full"`, and **`compact` is the default** —
you get the slim shape without asking for it:

`canvas_get_profile`, `canvas_list_observees`, `canvas_get_course`,
`canvas_get_submission`, `canvas_list_recent_submissions`,
`canvas_list_announcements`, `canvas_list_conversations`,
`canvas_get_conversation`, `canvas_list_discussion_topics`.

**Compact here is media stripping, not a field projection — do not expect a
field list.** It removes the avatar URLs Canvas hangs on user objects
(`avatar_url`, `avatar_image_url`) and nothing else. This server hands back
Canvas's payload verbatim and holds no verified record of which of Canvas's
fields a caller needs, so it does not claim to keep some and drop others: a
record that came back with holes in it would read exactly like a verified
answer. Stripping is subtractive, so it cannot lose a field nobody knew about.
A conversation participant keeps their name and id on compact; they lose their
picture.

- **The link fields survive both rungs, named explicitly.** `url`, `html_url`
  and `preview_url` are kept by name — `html_url` opens the item in Canvas,
  `preview_url` renders a submission, and `url` is the download handle
  `canvas_list_course_files` emits and `canvas_download_file` consumes. On an
  `online_url` submission that `url` IS the student's submitted work. Without
  the name, a student who submitted a link ending in `.png` would have had
  their submission silently removed on the default rung.
- **Both avatar spellings really do appear.** One live
  `canvas_list_conversations` response carried a default avatar
  (`…/avatar-50.png`) on one participant and an uploaded, extension-less
  thumbnail id on another. They are dropped by NAME, so both go — not one kept
  and one lost depending on whether that person ever uploaded a photo.

Pass `view: "full"` when you want Canvas's payload untouched, avatars and all.
That is also why there is deliberately **no `raw` rung**: there is no
normalisation layer here for `full` to sit above, so `full` already IS the
untouched upstream payload and a third value would silently alias it.

The other ten tools take no avatar `view`, for two different reasons:

- **Nothing to strip.** `canvas_list_courses`, `canvas_list_assignments`,
  `canvas_list_missing_submissions`, `canvas_list_enrollments`,
  `canvas_list_calendar_events`, `canvas_list_upcoming_events` and
  `canvas_list_planner_items` (whose `view` is `full | brief` instead) embed no user object — a live
  `canvas_list_courses` over twelve courses carried no media field of any kind
  — and a knob that does not turn is worse than no knob. `canvas_healthcheck`
  returns a verdict, not a record.
- **The URL is the product.** `canvas_list_course_files` and
  `canvas_download_file` exist to hand you a file URL. Compact there would not
  shrink the response, it would empty it.

Passing `view` to one of those ten is not an error and not a warning: MCP tool
schemas are non-strict, so the key is dropped and you get that tool's ordinary
output.

## Notes

- Set `CANVAS_NAME` if you want a friendly label other than the host portion of the base URL.
- All read tools that target a user accept an optional `observeeId` parameter (defaults to `self`) — useful when an observer is checking on a linked student.
