---
name: corkboard_dashboard
description: Post and manage real-time corkboard pins, lamp cues, deleted-history recovery, and multi-track project pipeline work for the Carl's Corkie dashboard. Use when you need to surface actionable tasks, alerts, opportunities, links, briefings, package tracking, article summaries, YouTube videos, or cellar ideas on the board.
homepage: https://github.com/Grooves-n-Grain/carls-corkie
metadata: {"openclaw":{"emoji":"📌"}}
---

# Corkboard Dashboard

Use this skill when you need to put something actionable on the board right now. Prefer a pin for one-off work or a project for multi-step work with tracks, handoffs, and task checklists.

## Quick Start

1. Install or update the dashboard:
```bash
export CORKBOARD_REPO="https://github.com/Grooves-n-Grain/carls-corkie.git"   # first-time installs only
bash {baseDir}/scripts/install.sh
```

2. Point tooling at the running API. Use `localhost` on the same machine, the machine's LAN IP from another trusted device, or a public reverse-proxy hostname if the operator has exposed `/api/*` externally (see the main README). The dashboard requires a bearer token; the helper script auto-loads it from `.env` in the install directory:
```bash
CORKBOARD_API=http://localhost:3010
# or LAN:
CORKBOARD_API=http://<lan-ip>:3010
# or public reverse-proxy hostname (API routes only, frontend not exposed):
CORKBOARD_API=https://corkie-api.example.com

# CORKBOARD_TOKEN is auto-loaded from .env. To set it manually:
export CORKBOARD_TOKEN="$(grep '^CORKBOARD_TOKEN=' /path/to/dashboard/.env | cut -d= -f2-)"
```

3. Post work with the bundled helper (it adds the auth header for you):
```bash
bash {baseDir}/scripts/corkboard.sh add task "Review PR" "Auth refactor complete" 1
bash {baseDir}/scripts/corkboard.sh add alert "Server down" "API returning 503s" 1
bash {baseDir}/scripts/corkboard.sh add link "Error logs" "https://logs.example.com/errors"
bash {baseDir}/scripts/corkboard.sh add-opportunity "Wholesale inquiry" "Follow up with studio buyer" 2
bash {baseDir}/scripts/corkboard.sh add-briefing "Morning briefing" "## Today\n- Ship the fix\n- Reply to supplier"
```

4. Use the REST API directly for projects, cellar ideas, history/restore, track updates, and lamp state. Every request to `/api/*` needs the `Authorization: Bearer $CORKBOARD_TOKEN` header:
```bash
curl -X POST "$CORKBOARD_API/api/pins" \
  -H "Authorization: Bearer $CORKBOARD_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"task","title":"Review PR","content":"Auth refactor complete","priority":1}'

curl -X POST "$CORKBOARD_API/api/projects" \
  -H "Authorization: Bearer $CORKBOARD_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Launch blog","emoji":"✍️","phase":"build","tracks":[{"name":"Write posts","owner":"claude"},{"name":"Review","owner":"you"}]}'
```

## Editing Pins

Task and Note pins can be edited inline on the dashboard by double-clicking the title. From the API, use `PATCH /api/pins/:id` to update any field:

```bash
# Update a pin's title and content
curl -X PATCH "$CORKBOARD_API/api/pins/<pin-id>" \
  -H "Authorization: Bearer $CORKBOARD_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated title","content":"New content here"}'
```

## Pick The Right Surface

- Use a `pin` for one-off tasks, alerts, links, notes, briefings, tracking updates, or short-lived reminders.
- Use a `project` for multi-step work with phases, tracks, and task lists shared between the agent and the human.
- Use `projectStatus: "cellar"` or `POST /api/projects/:id/cellar` for future ideas that should stay off the active board until they are ready.
- Tracks are owned by `claude`, `you`, or `shared`; finishing a track can automatically create a follow-up task pin for the next handoff.
- Use deleted pin history plus restore routes when something should come back to the board instead of being recreated from scratch.
- Prefer `priority: 1` for urgent work, `2` for the normal default, and `3` for low urgency.
- The dashboard ships with a shared bearer token (`CORKBOARD_TOKEN`) generated on first run. Keep `.env` private; the helper script reads the token from there automatically. To disable auth (only behind a reverse-proxy auth layer), set `CORKBOARD_AUTH=disabled` in `.env`.

## Common Actions

```bash
bash {baseDir}/scripts/corkboard.sh list
bash {baseDir}/scripts/corkboard.sh complete <pin-id>
bash {baseDir}/scripts/corkboard.sh delete <pin-id>
bash {baseDir}/scripts/corkboard.sh add-email <from> <subject> [preview] [email_id]
bash {baseDir}/scripts/corkboard.sh add-github <owner/repo> [description] [stars] [forks]
bash {baseDir}/scripts/corkboard.sh add-idea <title> [verdict] [summary] [scores_json] [competitors] [effort]
bash {baseDir}/scripts/corkboard.sh add-tracking <number> <carrier> [status] [eta] [url]
bash {baseDir}/scripts/corkboard.sh add-article <title> <url> <source> <tldr> [bullets_json] [tags_json]
bash {baseDir}/scripts/corkboard.sh add-opportunity <title> [content] [priority]
bash {baseDir}/scripts/corkboard.sh add-briefing <title> <content>
bash {baseDir}/scripts/corkboard.sh add-twitter <title> <content> [url]
bash {baseDir}/scripts/corkboard.sh add-reddit <title> <content> [url]
bash {baseDir}/scripts/corkboard.sh add-youtube <youtube-url>
curl -H "Authorization: Bearer $CORKBOARD_TOKEN" "$CORKBOARD_API/api/pins/history/deleted"
curl -X POST -H "Authorization: Bearer $CORKBOARD_TOKEN" "$CORKBOARD_API/api/pins/<pin-id>/restore"
curl -X POST -H "Authorization: Bearer $CORKBOARD_TOKEN" "$CORKBOARD_API/api/projects/<project-id>/cellar"
curl -X POST -H "Authorization: Bearer $CORKBOARD_TOKEN" "$CORKBOARD_API/api/lamp/waiting"
```

## References

- API routes, socket events, project statuses, track attachments, deleted-history behavior, and lamp controls: `{baseDir}/references/api.md`
- Install, LAN access, env vars, helper script usage, and trusted-network notes: `{baseDir}/references/setup.md`
- Pin types, specialized payload shapes, and example request bodies: `{baseDir}/references/pin-types.md`
