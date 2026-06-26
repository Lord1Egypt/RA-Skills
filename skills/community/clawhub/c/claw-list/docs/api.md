# Claw-List API Reference

Base URL: `{CLAW_LIST_URL}` from `claw-list.conf`.
All endpoints (except self-registration) require: `X-Agent-Id: {AGENT_ID}` · `Content-Type: application/json`

---

## Self-Registration

Called once when `REGISTERED=false`. Do not send `X-Agent-Id` on this call.

```
POST /admin/agents
{"agent_id": "{AGENT_ID}", "display_name": "{DISPLAY_NAME}", "scope": "own"}
```

Response 201 (created) or 409 (already exists) → write `REGISTERED=true` to conf.
Any other status → API unreachable, stop and inform the user.

---

## Lists

### Get lists
```
GET /lists
```
Returns all lists owned by this agent. If scope is `all`, returns lists from all agents.

Response: `[{"id": 1, "agent_id": "...", "name": "Shopping", "created_at": "..."}]`

### Create list
```
POST /lists
{"name": "Shopping"}
```
Response 201: list object.

### Delete list
```
DELETE /lists/{id}
```
Cascades to all items in the list. 403 if not owner.

---

## Items

### Get items
```
GET /lists/{list_id}/items
```
403 if scope is `own` and list belongs to another agent.

Response: array of item objects (see fields below).

### Add item
```
POST /lists/{list_id}/items
{"title": "Buy milk", "notes": "...", "priority": 2, "due_date": "2026-04-10", "category": "errands"}
```
Only `title` is required. 403 if list belongs to another agent.
Response 201: item object.

### Update item
```
PUT /items/{id}
{"title": "...", "notes": "...", "priority": 3, "due_date": "2026-04-15", "category": "...", "done": true}
```
All fields optional. 403 if list belongs to another agent.

### Delete item
```
DELETE /items/{id}
```
403 if list belongs to another agent.

---

## Item Fields

| Field | Type | Notes |
|---|---|---|
| `id` | int | Read-only |
| `list_id` | int | Read-only |
| `title` | string | Required on create |
| `notes` | text | Free-text; store conversation context here |
| `priority` | int 1–5 | 1 = highest, 5 = lowest; nullable |
| `due_date` | ISO date | e.g. `2026-04-10`; nullable |
| `category` | string | Nullable |
| `done` | bool | Default false |
| `created_at` | datetime | Read-only |
| `updated_at` | datetime | Read-only, auto-updated |

---

## Scope Behaviour

Scope is set per-agent in the `agents` table. Change it via the web UI or `PUT /admin/agents/{id}`.

- `own` (default): agent reads and writes only its own lists and items
- `all`: agent can read all agents' lists and items, but can only write to its own

**Write operations always enforce ownership** regardless of scope.

---

## Error Codes

| Code | Meaning |
|---|---|
| 201 | Created |
| 204 | Deleted |
| 403 | Unknown agent, or trying to write another agent's data |
| 404 | List or item not found |
| 409 | Agent already registered (treat same as 201 during self-reg) |

---

## Admin Endpoints

No `X-Agent-Id` required. Intended for human/UI use.

```
GET    /admin/agents              # list all agents
POST   /admin/agents              # register agent (same as self-reg above)
PUT    /admin/agents/{agent_id}   # update display_name and/or scope
DELETE /admin/agents/{agent_id}   # remove agent (does not delete their lists)
```
