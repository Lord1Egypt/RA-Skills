---
name: callsync
description: Look up a team's business calls, recordings and AI call summaries in CallSync, and keep its CRM up to date (contacts, follow-up tasks, notes). Use when the user asks about calls their team made or received, what a customer said, missed calls to return, call summaries, or wants to add a contact, a note or a follow-up task in CallSync.
version: 1.0.1
author: CallSync
license: MIT
homepage: https://callsyncapp.com
required_environment_variables:
  - name: CALLSYNC_API_KEY
    prompt: CallSync API key
    help: Sign in to https://dash.callsyncapp.com as the workspace owner, open API & Apps and copy the API key.
    required_for: every CallSync request
metadata:
  openclaw:
    emoji: "📞"
    homepage: https://callsyncapp.com
    primaryEnv: CALLSYNC_API_KEY
    requires:
      env:
        - CALLSYNC_API_KEY
      bins:
        - curl
    envVars:
      - name: CALLSYNC_API_KEY
        required: true
        description: CallSync API key, from the CallSync dashboard under API & Apps.
  hermes:
    tags: [crm, sales, calls, call-tracking, call-recording]
---

# CallSync

[CallSync](https://callsyncapp.com) syncs a sales team's business calls and recordings from their Android phones, writes AI call summaries, and keeps a light CRM of contacts, tasks and notes. This skill uses the CallSync REST API with the workspace API key in `CALLSYNC_API_KEY`.

## Setup

1. Sign in to the [CallSync dashboard](https://dash.callsyncapp.com) as the workspace owner.
2. Open **API & Apps** and copy the API key. Integrations need to be on in an active plan.
3. Make it available to the agent as `CALLSYNC_API_KEY`. Never print the key or put it in a URL.

## Calling the API

Base URL: `https://mcp.callsyncapp.com/api/v1`. Every request sends the key as a Bearer token. Pass user-supplied text with `--data-urlencode`, and send JSON bodies through a quoted here-document so the shell never expands what the user typed:

```bash
curl -sS --get "https://mcp.callsyncapp.com/api/v1/calls" \
  -H "Authorization: Bearer $CALLSYNC_API_KEY" \
  --data-urlencode "search=Rahul" --data-urlencode "limit=10"

curl -sS -X POST "https://mcp.callsyncapp.com/api/v1/crm/activities" \
  -H "Authorization: Bearer $CALLSYNC_API_KEY" -H "Content-Type: application/json" \
  -d @- <<'JSON'
{"person_id": 3, "type": "NOTE", "title": "Asked for a quote"}
JSON
```

Responses are JSON with `"status": "success"`. Errors are JSON with `"status": "error"` and a `message`, except HTTP `401` (plain text `Unauthorized`), which means the key is wrong or integrations are off for the workspace: ask the user to check the key, and do not retry.

## What you can do

| Task | Request |
| --- | --- |
| Find calls | `GET /calls` with `search` (phone, name, notes, team member, AI summary), `direction` (`incoming`, `outgoing`, `missed`, `rejected`, `blocked`), `page`, `limit` |
| Get a call's AI analysis | `GET /analysis?call_id=<call id>` |
| List callers with call counts | `GET /callers` with `search`, `page`, `limit` |
| List team members | `GET /employees` with `search` |
| Find CRM contacts | `GET /crm/contacts` with `search` (name, phone, email, sales note), `stage_id`, `label`, `page`, `limit` |
| See a contact's history | `GET /crm/timeline?person_id=<contact id>` |
| Read stages, priorities, segments, sources | `GET /crm/config` |
| Create a contact | `POST /crm/contacts` |
| Update a contact | `PUT /crm/contacts` with `id` and only the fields to change |
| Find tasks | `GET /crm/tasks` with `person_id`, `status` (`PENDING`, `COMPLETED`, `CANCELLED`), `due_date` (`YYYY-MM-DD`) |
| Create a follow-up task | `POST /crm/tasks` |
| Update or complete a task | `PUT /crm/tasks` with `id` and the fields to change |
| Add a note to a contact | `POST /crm/activities` |

Field lists and response shapes are in [references/api.md](references/api.md), in this skill's folder.

## How to work

- **Pages are small.** List endpoints return at most 10 rows per request (default 5). Read `pagination.total` (calls, callers) or `total` (contacts) and ask for the next `page` only when the user needs more.
- **Find the contact first.** Tasks, notes and timelines take a CRM contact `id` as `person_id`. Search `GET /crm/contacts` by name or phone and use the `id`; if several match, ask the user which one.
- **Stage, priority, segment and source are ids.** Read `GET /crm/config` and use the `id` of the label the user named.
- **Due dates stay as given.** Send `due_date` as `YYYY-MM-DD` and `due_time` as `HH:MM:SS` in the team's local time; do not convert time zones.
- **Send only what changes.** On updates, leave out fields the user did not mention, so saved data is not wiped.
- **Confirm before writing.** Creating or changing contacts, tasks and notes changes the team's CRM. Say what you will write and to whom, and go ahead once the user agrees. Each note request adds a new entry, so do not retry a note that may have gone through.
- **No deleting.** This skill never deletes contacts or tasks. To remove one, the user can do it in the CallSync dashboard.
- **Keep call data private.** Phone numbers, transcripts and recording links belong to the team's customers. Recording links can be opened by anyone who has them, so share them only with the user who asked, never in public channels.

## Examples

- "Who called us yesterday that we missed?" → `GET /calls` with `direction=missed`, then report caller name, phone, time and the team member.
- "What did Rahul say on his last call?" → `GET /calls` with `search=Rahul`, take the newest call's `id`, then `GET /analysis?call_id=…` and report its `summary` and the suggested follow-ups in `analysis.tasks`. If the analysis is not `completed` yet, say so.
- "Remind Priya to call Rahul back tomorrow at 11" → find Rahul with `GET /crm/contacts`, confirm, then `POST /crm/tasks` with `person_id`, `type: CALL`, a description naming Priya, and tomorrow's `due_date` with `due_time: 11:00:00`.
- "Move Demo Buyer to Qualified" → read the stage id from `GET /crm/config`, confirm, then `PUT /crm/contacts` with `id`, `stage_id` and `is_in_pipeline: true`.

## Other ways to connect

CallSync is also a hosted remote MCP server at `https://mcp.callsyncapp.com/connect` (Streamable HTTP, OAuth sign-in), for agents that support remote MCP servers. For automations there are an [n8n node](https://www.npmjs.com/package/n8n-nodes-callsync) and an [Activepieces piece](https://www.npmjs.com/package/@callsyncapp/piece-callsync).
