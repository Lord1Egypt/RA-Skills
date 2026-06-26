---
name: canvas-parent-mcp
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

With the [fetchproxy extension](https://github.com/chrischall/fetchproxy) installed and a signed-in Canvas tab, that's enough — the MCP reads your session cookies at startup. Add `CANVAS_TOKEN`, `CANVAS_CLIENT_*`/`CANVAS_REFRESH_TOKEN`, or `CANVAS_USERNAME`/`CANVAS_PASSWORD` to the `env` block if you'd rather use one of those modes.

### Option B — from source

```bash
git clone https://github.com/chrischall/canvas-parent-mcp
cd canvas-parent-mcp
npm install && npm run build
```

## Authentication

**fetchproxy fallback (recommended, zero-config).** Set only `CANVAS_BASE_URL`. Install the [fetchproxy](https://github.com/chrischall/fetchproxy) browser extension, sign into your Canvas instance once. The MCP reads `canvas_session` + `pseudonym_credentials` cookies from your tab at startup; all API calls go directly from Node after that. Works with any auth flow (SSO/SAML/2FA included).

### Alternatives (env-var)

- **Personal access token** — set `CANVAS_TOKEN`. Most institutions have disabled this for non-admins.
- **OAuth** — set `CANVAS_CLIENT_ID`, `CANVAS_CLIENT_SECRET`, `CANVAS_REFRESH_TOKEN`. Bootstrap via `canvas-parent-mcp-qr-login`.
- **Username/password (session-scrape)** — set `CANVAS_USERNAME` + `CANVAS_PASSWORD`. Direct Canvas accounts only (no SSO/2FA). Brittle.

Precedence when multiple are set: `CANVAS_TOKEN` > username/password > OAuth > fetchproxy. Set `CANVAS_DISABLE_FETCHPROXY=1` to opt out of the fallback.

## Tools (prefix `canvas_`)

### Profile & observees
- `canvas_get_profile` — your Canvas profile
- `canvas_list_observees` — students linked to your observer account

### Courses
- `canvas_list_courses` — your active courses with grades
- `canvas_get_course(courseId)` — course detail with syllabus + teachers

### Assignments & submissions
- `canvas_list_assignments(courseId)` — assignments in a course
- `canvas_list_missing_submissions` — past-due unsubmitted work
- `canvas_get_submission(courseId, assignmentId)` — your submission with comments + rubric
- `canvas_list_recent_submissions(courseId)` — recently graded submissions (default 14d)

### Grades
- `canvas_list_enrollments` — per-course grades

### Calendar & planner
- `canvas_list_calendar_events` — calendar events / assignments
- `canvas_list_upcoming_events` — server-curated next 7 days
- `canvas_list_planner_items` — unified to-do feed

### Communication
- `canvas_list_announcements(contextCodes)` — course announcements
- `canvas_list_conversations` — inbox
- `canvas_get_conversation(id)` — full conversation thread
- `canvas_list_discussion_topics(courseId)` — course discussion topics

### Files
- `canvas_list_course_files(courseId)` — file metadata
- `canvas_download_file(url, destinationPath)` — download a file to disk

## Notes

- Set `CANVAS_NAME` if you want a friendly label other than the host portion of the base URL.
- All read tools that target a user accept an optional `observeeId` parameter (defaults to `self`) — useful when an observer is checking on a linked student.
