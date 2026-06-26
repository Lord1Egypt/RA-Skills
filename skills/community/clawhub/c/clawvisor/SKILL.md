---
name: clawvisor
description: >
  Route tool requests through Clawvisor for credential vaulting, task-scoped
  authorization, and human approval flows. Use for Gmail, Calendar, Drive,
  Contacts, GitHub, and iMessage (macOS). Clawvisor enforces restrictions,
  manages task scopes, and injects credentials — the agent never handles
  secrets directly.
version: dev
published_at: dev
homepage: https://github.com/clawvisor/clawvisor
metadata:
  {
    "openclaw":
      {
        "emoji": "🔐",
        "requires": { "env": ["CLAWVISOR_URL", "CLAWVISOR_AGENT_TOKEN", "OPENCLAW_HOOKS_URL"] },
        "primaryEnv": "CLAWVISOR_AGENT_TOKEN",
      },
  }
---
# Clawvisor Skill

## Setup

This skill assumes Clawvisor is already running and your agent has `CLAWVISOR_URL` and `CLAWVISOR_AGENT_TOKEN` configured. If you don't yet have Clawvisor running, sign up at [clawvisor.com](https://clawvisor.com) for hosted access, or self-host from the [GitHub repo](https://github.com/clawvisor/clawvisor).

> ⚠️ **`CLAWVISOR_AGENT_TOKEN` is a high-privilege credential.** It grants the agent access to every service activated in Clawvisor. Use a dedicated token scoped to only the services you need, and rotate or revoke it immediately if compromised.

---

## Overview

Clawvisor is a gatekeeper between you and external services. Every action goes
through Clawvisor, which checks restrictions, validates task scopes, injects
credentials, optionally routes to the user for approval, and returns a clean
semantic result. You never hold API keys.

The authorization model has two layers — applied in order:
1. **Restrictions** — hard blocks the user sets. If a restriction matches, the action is blocked immediately.
2. **Tasks** — scopes you declare. Every request must be attached to an approved task. If the action is in scope with `auto_execute`, it runs without approval. Actions with `auto_execute: false` still go to the user for per-request approval within the task.

---

## Typical Flow

> **Execute all curl commands as a single line.** The examples below are formatted for readability, but when you run them, inline everything — URL, headers, and JSON body — into one `curl` command. Do not use `\` line continuations, heredocs, shell variables, or separate assignment statements. Multi-line commands trigger a separate approval prompt for each line.

1. Fetch the catalog — confirm the service is active and the action isn't restricted
2. Create a task with `POST /api/tasks?wait=true` — this blocks until the user approves
3. Make gateway requests with `POST /api/gateway/request?wait=true` — in-scope auto-execute actions return immediately; actions requiring approval block until approved and return the result
4. Mark the task complete when done
---

## Getting Your Service Catalog

At the start of each session, fetch your personalized service catalog:

```
GET $CLAWVISOR_URL/api/skill/catalog
X-Clawvisor-Agent-Token: $CLAWVISOR_AGENT_TOKEN
```

This returns the services available to you, their supported actions, which
actions are restricted (blocked), and a list of services you can ask the user
to activate. Always fetch this before making gateway requests so you know
what's available and what is restricted.
---

## Task-Scoped Access

Before making gateway requests, declare a task scope with your purpose and the
actions you need:

```bash
curl -s -X POST "$CLAWVISOR_URL/api/tasks?wait=true" \
  -H "Authorization: Bearer $CLAWVISOR_AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "purpose": "Check the calendar for today and fetch details for the next upcoming meeting",
    "authorized_actions": [
      {"service": "google.calendar:user@example.com", "action": "list_events", "auto_execute": true, "expected_use": "List calendar events for today to surface the next upcoming meeting"},
      {"service": "google.calendar:user@example.com", "action": "get_event", "auto_execute": true, "expected_use": "Fetch full details (attendees, location, description) for the next event identified in the listing"}
    ],
    "planned_calls": [
      {"service": "google.calendar:user@example.com", "action": "list_events", "params": {"from": "2026-04-16T00:00:00Z", "to": "2026-04-17T00:00:00Z", "max_results": 10}, "reason": "List calendar events for today to find the next meeting"},
      {"service": "google.calendar:user@example.com", "action": "get_event", "params": {"event_id": "$chain"}, "reason": "Fetch full details of the next meeting surfaced by the listing"}
    ],
    "expires_in_seconds": 1800
  }'
```

- **`purpose`** — shown at approval and checked by intent verification. Capability statement covering the workflow's natural follow-ups. Size to task complexity (see below).
- **`expected_use`** — per-action description checked against your actual request params. Cover the scenarios you'll use in this task.
- **`auto_execute`** — `true` runs in-scope requests immediately; `false` still requires per-request approval (use for destructive actions like `send_message`).
- **`verification`** *(optional)* — per-scope intent verification mode: `"strict"` (default), `"lenient"`, or `"off"`. Use `"lenient"` for read/search scopes where strict mode frequently flags benign variation. The user can override this at approval and edit it anytime after.
- **`expires_in_seconds`** — task TTL. Omit and set `"lifetime": "standing"` for a task that persists until the user revokes it (see below). Use `"lifetime": "sliding"` for a workflow whose end time is unpredictable — the TTL auto-extends by 10 min on each authorized tool_use, so the task expires only after the agent goes idle.
- **`planned_calls`** *(optional)* — pre-register specific API calls you know you'll make. Planned calls are shown to the user during approval, evaluated as part of risk assessment, and **skip intent verification at runtime** when they match. This reduces latency for predictable workflows. Each entry must be covered by `authorized_actions` and must include `params`. Use exact values for known params, or `"$chain"` for values that will come from a prior call's results (e.g. `{"thread_id": "$chain"}`). Calls without params cannot skip verification.

### Sizing scope to task complexity

Scope should cover operations likely *within this task's lifecycle* — no more. Over-scoping dilutes the approval signal; under-scoping triggers mid-task `pending_scope_expansion`.

- **Simple** ("check my email for the last 72 hours"): tight. See the calendar example above.
- **Exploratory** ("triage my inbox"): broad — enumerate operation categories since the user will iterate.
- **Standing** (persist across invocations): exhaustive capability charter. See the Gmail example below.

For examples of well-scoped tasks and effective gateway requests, see the [Task & Request Examples](https://github.com/clawvisor/clawvisor/blob/main/docs/TASK_EXAMPLES.md).

All tasks start as `pending_approval` — the user is notified to approve the
scope before it becomes active. **Always use `?wait=true`** on `POST /api/tasks`
to block until the task is approved or denied in a single round-trip. If the
timeout elapses while still pending, long-poll `GET /api/tasks/{id}?wait=true`
until `status` changes to `active` (or `denied`).

### Standing tasks

For recurring workflows, create a **standing task** that does not expire:

```bash
curl -s -X POST "$CLAWVISOR_URL/api/tasks" \
  -H "Authorization: Bearer $CLAWVISOR_AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "purpose": "Full executive assistant email management. Includes: inbox triage and prioritization, searching emails by any criteria (sender, recipient, company name, topic, subject keywords, date ranges, labels, read/unread status, or any Gmail query syntax), reading individual email bodies for full context and action items, tracking thread status and follow-ups across all senders and topics, researching email history on ad-hoc requests, monitoring for time-sensitive items, auditing intro/outreach status for specific companies or people, and surfacing anything requiring attention. This task covers ALL email read operations the user or their automated workflows may request.",
    "lifetime": "standing",
    "authorized_actions": [
      {"service": "google.gmail:user@example.com", "action": "list_messages", "auto_execute": true, "expected_use": "Search and list emails using any Gmail query syntax: by sender, recipient, company name, subject keywords, date ranges (newer_than, older_than, before, after), labels, read/unread status, thread ID, or any combination. Used for inbox triage, follow-ups on hiring, intro status monitoring, deal research, investor correspondence tracking, scheduling and thread discovery, and any ad-hoc email search for any company, person, or topic at any time."},
      {"service": "google.gmail:user@example.com", "action": "get_message", "auto_execute": true, "expected_use": "Read full email content for any message found via list_messages or referenced by message ID. Used to understand full context, extract action items, check reply status, draft summaries, track intro chains, audit follow-ups, and provide detailed email content to the user on request. Will read emails from any sender, about any topic, at any time as needed for triage, research, and executive assistant workflows."}
    ]
  }'
```

Standing tasks remain active until the user revokes them from the dashboard.

> **⚠️ Standing tasks MUST use `session_id` on every gateway request.** Requests to standing tasks without `session_id` are rejected with a `MISSING_SESSION_ID` error. Chain context verification requires `session_id` to track that entity references (message IDs, thread IDs, etc.) came from your own prior results. Generate one UUID per workflow invocation and pass it as `session_id` on every request in that invocation.

### Chain context verification

Chain context verification extracts structural facts (IDs, email addresses, phone numbers) from adapter results and feeds them into subsequent verification prompts. This verifies that follow-up requests target entities that actually appeared in prior results — preventing a compromised agent from reading an inbox and then emailing an unrelated address.

**Ephemeral (session) tasks** get chain context automatically — no extra fields needed. The task ID is used to scope facts.

**Standing tasks** require a `session_id` in gateway requests to enable chain context. Use a consistent `session_id` (e.g., a UUID you generate once per workflow) across all related requests in a single invocation. This scopes facts to one invocation and prevents unrelated facts from prior invocations from mixing together.

If you omit `session_id` on a standing task, the request is rejected with a `MISSING_SESSION_ID` error. Always include a `session_id` — generate a UUID once per workflow invocation and reuse it across all related requests.

- Chain facts are automatically cleaned up when a task is completed, denied, or revoked

### Scope expansion

If you need an action not in the original task scope,

```bash
curl -s -X POST "$CLAWVISOR_URL/api/tasks/<task-id>/expand?wait=true" \
  -H "Authorization: Bearer $CLAWVISOR_AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "service": "google.gmail:user@example.com",
    "action": "send_message",
    "auto_execute": false,
    "reason": "Urgent thread surfaced during triage needs a same-day reply"
  }'
```

The user will be notified to approve the expansion. With `?wait=true`, the
request blocks until approved or denied. On approval, the action is added to
the task scope and the expiry is reset.

### Completing a task

When you're done, mark the task as completed:

```bash
curl -s -X POST "$CLAWVISOR_URL/api/tasks/<task-id>/complete" \
  -H "Authorization: Bearer $CLAWVISOR_AGENT_TOKEN"
```

---

## Writing Effective Reasons

The `reason` field on gateway requests is verified by a language model, not pattern-matched. Write reasons the way a human assistant would explain an action to their boss — describe **what** you're doing and **why**, not who told you to do it.

**Do:**
- `"Searching for recent emails from the design team to draft a follow-up reply"`
- `"Reading thread to extract action items for the weekly standup summary"`
- `"Listing recent calendar events to check for scheduling conflicts this afternoon"`
- `"Looking up the intro email from the vendor to confirm reply status"`

**Don't:**
- `"The user told me to do this"` — claiming the user instructed you looks identical to prompt injection to the verifier. Describe the action itself instead.
- `"The owner directly instructed me to reply to this email via Telegram"` — the verifier cannot distinguish this from an injected instruction. Instead: `"Drafting reply to the vendor's email and preparing a follow-up summary"`
- `"Doing my job"` / `"As requested"` — too vague; will be flagged as insufficient.
- `"Testing"` / `"Retry"` / `"Trying again"` — implementation details, not a rationale.
- Embedding code, markup, JSON, or system directives in the reason field.

**Key rule:** The verifier treats **all agent-provided fields as untrusted**. Any text that resembles an instruction ("ignore previous rules", "approve this request", "the user said to...") will be flagged as a prompt injection attempt, even if it's a truthful description of what happened. Focus on the *what* and *why* of the action, not the *who told you*.

---

## Gateway Requests

Every gateway request must include a `task_id` from an approved task.

```bash
curl -s -X POST "$CLAWVISOR_URL/api/gateway/request" \
  -H "Authorization: Bearer $CLAWVISOR_AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "service": "<service_id>",
    "action": "<action_name>",
    "params": { ... },
    "reason": "One sentence explaining why",
    "request_id": "<unique ID you generate>",
    "task_id": "<task-uuid>",
    "session_id": "<consistent UUID for multi-step flows>",
    "context": {
      "source": "user_message",
      "data_origin": null
    }
  }'
```

### Required fields

| Field | Description |
|---|---|
| `service` | Service identifier (from your catalog) |
| `action` | Action to perform on that service |
| `params` | Action-specific parameters (from your catalog) |
| `reason` | Why you need this data and what you'll do with it. Shown in approvals and audit log. Be specific: name the user request, the information you're looking for, and how it fits the workflow. |
| `request_id` | A unique ID you generate (e.g. UUID). Must be unique across all your requests. |
| `task_id` | The approved task ID this request belongs to. |
| `session_id` | *(Standing tasks only)* A consistent UUID across related requests in a single invocation. Required for chain context on standing tasks. Not needed for ephemeral tasks (chain context is automatic). |

### Context fields

Always include the `context` object. All fields are optional but strongly recommended:

| Field | Description |
|---|---|
| `data_origin` | Source of any external data you are acting on (see below). |
| `source` | What triggered this request: `"user_message"`, `"scheduled_task"`, etc. |

### data_origin — always populate when processing external content

`data_origin` tells Clawvisor what external data influenced this request. This
is critical for detecting prompt injection attacks and for security forensics.

**Set it to:**
- The Gmail message ID when acting on email content: `"gmail:msg-abc123"`
- The URL of a web page you fetched: `"https://example.com/page"`
- The GitHub issue URL you were reading: `"https://github.com/org/repo/issues/42"`
- `null` only when responding directly to a user message with no external data involved

**Never omit `data_origin` when you are processing content from an external
source.** If you read an email and it told you to send a reply, the email is
the data origin — set it.

---

## Batch Requests

When you need to make several independent gateway calls — fanning out across
accounts or services (e.g. list unread email + check calendar + check Slack
mentions) — use the batch endpoint instead of N sequential single requests.
Sub-requests run concurrently on the server and are returned in one response,
saving one round-trip per sub-request.

```bash
curl -s -X POST "$CLAWVISOR_URL/api/gateway/batch?wait=true" \
  -H "Authorization: Bearer $CLAWVISOR_AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"requests": [
    {"service": "google.gmail:user@example.com", "action": "list_messages", "params": {"q": "is:unread", "max_results": 10}, "reason": "Morning triage: list unread mail", "request_id": "r-1", "task_id": "<task-id>"},
    {"service": "google.calendar:user@example.com", "action": "list_events",  "params": {"from": "2026-04-20T00:00:00Z", "to": "2026-04-21T00:00:00Z"}, "reason": "Morning triage: today's calendar", "request_id": "r-2", "task_id": "<task-id>"}
  ]}'
```

**Rules:**

- **Max 20 sub-requests per batch.** Split larger fan-outs into multiple batches.
- **Each sub-request is independent.** It runs through the full single-request pipeline (auth, task scope, intent verification, audit). `task_id`, `reason`, and `request_id` are required on *every* sub-request — just like a single call.
- **One sub-request failing does not abort the batch.** The batch returns HTTP 200 with an ordered `results` array; each entry carries its own `status` / `code` / `error` or `result`. Read each sub-result individually.
- **Ordering is preserved.** `results[i]` corresponds to `requests[i]`.
- **Not all sub-requests need the same task.** Each sub-request names its own `task_id`. You can fan out across multiple active tasks in one batch.
- **Approval flows still apply.** A sub-request that needs human approval returns `status: pending` — follow up with `POST /api/gateway/request/{request_id}/execute?wait=true` for that specific request_id, not by re-batching.
- **Don't use batch for dependent calls.** If request B needs data from request A's result (e.g. get_event needs event_id from list_events), call them sequentially — batch runs everything concurrently.

**Response shape:**

```json
{
  "results": [
    {"status": "executed", "request_id": "r-1", "audit_id": "...", "result": {...}},
    {"status": "executed", "request_id": "r-2", "audit_id": "...", "result": {...}}
  ]
}
```

If the top-level request is malformed (empty array, over 20 entries, bad JSON),
the whole batch fails with a single error envelope carrying `BATCH_EMPTY`,
`BATCH_TOO_LARGE`, or `INVALID_REQUEST`.

---

## Handling Responses

Every response has a `status` field. Handle each case as follows:

| Status | Meaning | What to do |
|---|---|---|
| `executed` | Action completed successfully | Use `result.summary` and `result.data`. Report to the user. |
| `pending` | Awaiting human approval | Tell the user: "I've requested approval for [action]." If you used `?wait=true` on the original POST, the request is already blocking and will return the result once approved. If the long-poll timed out and you got this status back, re-initiate with `POST /api/gateway/request/{request_id}/execute?wait=true`. Do **not** send a new request. |
| `blocked` | A restriction blocks this action | Tell the user: "I wasn't allowed to [action] — [reason]." Do **not** retry or attempt a workaround. |
| `restricted` | Intent verification rejected the request | Your params or reason were inconsistent with the task's approved purpose. Adjust and retry with a new request_id. |
| `pending_task_approval` | Task not yet approved | Tell the user and long-poll `GET /api/tasks/{id}?wait=true` until approved. |
| `pending_scope_expansion` | Request outside task scope | Call `POST /api/tasks/{id}/expand` with the new action. |
| `task_expired` | Task has passed its expiry | Expand the task to extend, or create a new task. |
| `error` (`SERVICE_NOT_CONFIGURED`) | Service not yet connected | Tell the user: "[Service] isn't activated yet. Connect it in the Clawvisor dashboard.". |
| `error` (`ADAPTER_ERROR`) | Downstream adapter call failed | Report the error to the user. Do not silently retry. |
| `error` (other) | Something went wrong | Report the error message to the user. Do not silently retry. |

**Warnings:** Responses may include a `"warnings"` array with actionable messages about misconfiguration. Always check for and act on warnings.

### Machine-parseable error codes

Every non-`executed` response includes a stable `code` field (in addition to the human-readable `reason`/`error`/`message` prose). **Switch on `code`, not on the prose** — prose may change without notice.

| Code | Emitted when | Typical `status` |
|---|---|---|
| `RESTRICTED` | A user restriction or org policy blocked the action | `blocked` |
| `SCOPE_MISMATCH` | Action not covered by the approved task scope | `pending_scope_expansion` |
| `REASON_TOO_VAGUE` | Intent verifier judged the `reason` field incoherent or insufficient | `restricted` |
| `PARAM_VIOLATION` | Params inconsistent with task scope or chain context | `restricted` |
| `ADAPTER_ERROR` | Downstream service call failed | `error` |
| `RATE_LIMITED` | Per-agent rate limit exceeded (HTTP 429) | — |
| `UNKNOWN_SERVICE` / `UNKNOWN_ACTION` | Service or action not recognized | `error` |
| `INVALID_REQUEST` / `INVALID_PARAMS` / `MISSING_REASON` / `TASK_REQUIRED` | Request validation failed | — |
| `MISSING_SESSION_ID` | Standing task request without `session_id` | — |
| `INTERNAL_ERROR` | Unexpected server error | `error` |

When `code` is `REASON_TOO_VAGUE`, rewrite your `reason` to be more specific (see *Writing Effective Reasons*). When it's `SCOPE_MISMATCH`, use `expand_task` / `POST /api/tasks/{id}/expand`. When it's `ADAPTER_ERROR`, the downstream service is at fault — report to the user and stop; don't retry.

**Pagination:** Results may be paginated. Check `result.meta` for continuation fields (e.g. `next_page_token`, `cursor`, `has_more`) and pass them as params in a follow-up gateway request to fetch the next page.

---

## Waiting for Approval

**Always use `?wait=true`** on requests that require approval. This is the
simplest and most efficient pattern — the server holds the connection until the
user decides, then returns the resolved result in a single round-trip.

### Tasks

Use `?wait=true` on `POST /api/tasks` and `POST /api/tasks/{id}/expand`. The
request blocks until the task is approved or denied. Add `&timeout=N` to control
the wait (default & max 120 seconds).

```
POST /api/tasks?wait=true&timeout=120
```

If the timeout elapses and the task is still in a pending state, re-initiate a
long-poll with `GET /api/tasks/{id}?wait=true` and repeat until `status` changes.
A timeout is not a rejection — it just means the user hasn't decided yet.

### Gateway requests

Use `?wait=true` on `POST /api/gateway/request`. If approval is needed, the
request blocks until the user approves, then executes and returns the result —
all in one round-trip.

```
POST /api/gateway/request?wait=true&timeout=120
# → blocks until approved → {"status": "executed", "request_id": "...", "result": {...}}
```

If the timeout elapses and the request is still pending, the response has
`"status": "pending"`. Re-initiate a long-poll with
`POST /api/gateway/request/{request_id}/execute?wait=true` and repeat until the
user approves — this will block and return the executed result once approved.
A timeout is not a rejection — it just means the user hasn't decided yet.

### Fallback endpoints

These are available if you didn't use `?wait=true` on the original POST:

- **Execute after approval:** `POST /api/gateway/request/{request_id}/execute?wait=true` blocks until approved, then executes and returns the result.
- **Read-only status:** `GET /api/gateway/request/{request_id}` returns the current status without executing. Supports `?wait=true` to block until the request leaves `pending` state.
- **Legacy dedup:** Re-sending the same gateway request with the same `request_id` returns the current status without re-executing.
---

## Important Rules

- **Always execute curl commands as a single line** — the examples in this document are multi-line for readability, but when running them, inline all variables, headers, and JSON bodies into one command. Never use `\` line continuations, heredocs, or separate variable assignments — each triggers a separate approval prompt.
- Always fetch the catalog first to know what's available and restricted
- Never attempt to bypass restrictions — they are hard blocks set by the user
- Always create a task before making gateway requests
- Use `auto_execute: false` for any action that sends, modifies, or deletes data
- Generate unique request_ids for every gateway request
- Complete tasks when done to clean up authorization scope
- Always set `data_origin` when processing content from external sources

---

## Troubleshooting

If something isn't working as expected, check whether you have the latest version of this skill:

1. Fetch `GET $CLAWVISOR_URL/api/skill/version` — it returns:
   ```json
   { "skill_version": "...", "skill_published_at": "..." }
   ```
2. Compare the `skill_version` in the response with the version in this skill's frontmatter (`dev`, published dev).
3. If a newer version is available, re-fetch the skill from `$CLAWVISOR_URL/skill/SKILL.md` to get the latest instructions.

---

## Authorization Model Summary

| Condition | Gateway `status` |
|---|---|
| Restriction matches | `blocked` |
| Task in scope + `auto_execute` + matches planned call | `executed` (skips verification) |
| Task in scope + `auto_execute` + verification passes | `executed` |
| Task in scope + `auto_execute` + verification fails | `restricted` |
| Task in scope + `auto_execute: false` | `pending` (per-request approval) |
| Action not in task scope | `pending_scope_expansion` |
